# ECL IR 当前架构

本文描述 `ecl_ir` 当前已经实现的架构，而不是最终愿景。状态基线为
2026-07-15。设计背景、游戏资料和后续路线分别见：

- [`../ecl-cross-game-ir-design.md`](../ecl-cross-game-ir-design.md)：跨游戏设计与语义背景。
- [`../ecl-reference-by-game.md`](../ecl-reference-by-game.md)：分游戏 opcode、变量和资料索引。
- [`standalone-ir-roadmap.md`](standalone-ir-roadmap.md)：已完成不变量和后续工作。
- [`backend-special-cases.md`](backend-special-cases.md)：兼容后端中特化逻辑的迁移清单。

## 1. 架构结论

当前系统采用“源工件层、源方言结构层、canonical 语义层、派生分析层、
目标 lowering 层”五层结构：

```text
source .decl bytes
  |
  v
SourceDocument + source layout          artifact / byte ownership
  |
  v
Program                                 source-dialect structural IR
  |  \
  |   -> legacy object projections -> schema-v1 objects
  v
SemanticModule                          ordered canonical lowering IR
  |                         \
  |                          -> analysis projections (non-owning)
  v
LoweringPlanner + GameProfile
  |  uses CanonicalBackendEmitter
  |
  v
CapabilityDecision / LoweringResult
  |
  v
TargetAstBuilder
  |
  v
TargetModule -> DeclTextCodec -> target .decl bytes -> thecl
```

独立 `.eclir.json` envelope 同时保存原始字节、布局、`Program`、
`SemanticModule`、派生分析和旧 object projection。普通 lowering 的源侧信息只
从这个 envelope 读取。跨游戏 ANM lowering 是明确的例外依赖：它按 stage id
读取仓库内源/目标游戏原版 stage package，分别取得 purpose/调用边界证据和
manifest-scoped 目标候选；这些 package corpus 不是 envelope 的一部分。

架构上的权威关系是：

1. `SemanticModule` 是唯一拥有 canonical 顺序、节点身份和 lowering ownership
   的中间语义对象。
2. `Program` 是源方言结构 IR，不是 canonical 语义，也不是完整 lossless AST。
3. `analysis_projections` 是可重算的只读视图，只能通过 `NodeId` 引用 canonical
   节点，不能拥有或替换节点。
4. `IRObject`、`BulletEmitter`、`BossPattern` 等 `legacy/model.py` 对象属于 schema-v1
   兼容路径，不是 canonical IR。
5. 游戏差异应进入 profile、dialect、semantic registry 或 target encoder，不能
   进入 `SemanticModule`，也不应新增“源游戏 A 到目标游戏 B”的一对一表。

## 2. 分层职责

| 层 | 主要对象 | 职责 | 不负责 |
| --- | --- | --- | --- |
| 工件层 | `SourceDocument`、`DeclTextCodec`、`source_layout` | 字节、字符集、异常字节、行尾和精确恢复 | opcode 语义、游戏能力 |
| 源方言层 | `Program`、`Function`、`Statement`、`Instruction` | 解析源码结构，保留 routine 内语句顺序和原始文本 | 跨游戏语义等价 |
| canonical 层 | `SemanticModule`、`SemanticOperation`、`RawInstructionOp`、`SyntaxStatement` | 稳定语义、身份、provenance、ownership 和 lowering 顺序 | 目标 opcode、lossy 策略 |
| 分析层 | bullet state、CFG、transform index projection、ANM target candidate plan | 从 canonical 节点与目标原版包推导跨语句状态或 lowering 证据 | 源码所有权、直接输出 |
| profile/registry 层 | `GameProfile`、`VariableDialect`、semantic/reference catalogs | 描述每个游戏的编码、能力和工具 ABI | 修改 canonical 节点 |
| lowering 层 | `LoweringPlanner`、`CapabilityDecision`、`TargetModule` | 判断可表示性、生成结构化诊断、编码目标方言 | 猜测未证实等价 |
| 兼容层 | schema-v1 objects、legacy backend、`--legacy-patterns` | 保留旧实验路径和尚未迁移的 codegen | 充当 canonical 权威层 |

## 3. 源工件与解析

### 3.1 `SourceDocument`

[`source/parser.py`](source/parser.py) 中的 `SourceDocument` 保存：

```text
source_bytes
text
encoding
decoding_mode
byte_escape_scope
```

解析优先尝试 UTF-8 BOM、UTF-8、CP932 和 Shift-JIS 的严格往返。不能严格解码
或重新编码的字节使用补充私用区 `U+F0000 + byte` 暂存，从而可以安全进入
UTF-8 JSON，之后再恢复原字节。

物理行切分只把 LF、CRLF，以及无 LF 文件中的 CR 视为换行。字符串中的
VT、FF、FS 等控制字节不会被 Python 的 Unicode 行切分规则误当作源码边界。

字符编码属于 `.decl` 工件契约。它不进入 `SemanticModule`，也不是
`GameProfile` 能力。目标源码最终由 [`artifact/ir_file.py`](artifact/ir_file.py) 的
`DeclTextCodec` 按 envelope 中保存的源 codec 写为 bytes。

### 3.2 `Program`

[`source/model.py`](source/model.py) 的源方言结构由以下对象组成：

- `Program(source, game, functions, resources, top_level, routine_signatures)`
- `Function(name, params, statements, body)`
- `Statement(kind, raw, text, difficulty, attrs)`
- `Instruction(opcode, args, raw, difficulty, difficulty_literals)`

`Function.statements` 是 routine 内完整的有序结构序列，也是 canonical lift 的
输入；`Function.body` 仅包含 instruction，是旧接口和计数兼容投影。一个
instruction 同时出现在这两个视图中，但只会 lift 为一个 canonical 节点。

`Program` 不承诺完整保存全文件排版。资源块被归并到 `resources`，函数和
顶层语句分别存放；精确字节、空行、行尾和原始全局布局由 `.eclir` envelope
中的 `source_bytes_base64` 与 `source_layout` 负责。

### 3.3 难度状态与选择值

parser 明确区分执行 guard 与运行时选择值：

- 普通 `!X` 更新持久 guard，直到后续 marker 改变。
- `!X:` 只作用于下一个有效语句，随后恢复无条件状态。
- `!*` 清除当前 guard；routine 和 legacy timeline 边界也会重置状态。
- 只有“rank marker + literal”序列完整闭合、不中断、存在 `!*` 且存在实际
  consumer 时，才折叠为一个选择值候选。

因此 `DifficultyGuard` 表示某节点在哪些 lane 执行，`SelectedValue` 表示该
节点消费的值如何按难度选择，两者不能合并成一个字段。

### 3.4 外部 routine 签名

部分后期游戏的 `default.decl` 不带完整参数，但兄弟 stage 文件含 prototype。
`emit-ir` 阶段会发现这些 `RoutineSignature` 并写入 envelope。之后
`compile-ir` 只使用序列化签名，不再依赖兄弟文件。目标参数与反编译器生成的
`var` 别名会在目标 frame 中协调，避免参数和 local 被分配两次。

## 4. Canonical 语义模型

### 4.1 容器与顺序

[`canonical/semantic_ir.py`](canonical/semantic_ir.py) 中的结构为：

```text
SemanticModule
  source / source_game / profile
  resources
  routine_signatures
  top_level: list[SyntaxStatement]
  routines: list[SemanticRoutine]

SemanticRoutine
  name / params
  body: list[SemanticNode]
```

`SemanticRoutine.body` 是该 routine 唯一的 lowering 顺序。lifter 按
`Program.functions` 和 `Function.statements` 的原顺序遍历，不按 opcode、语义
类别或对象聚类重新排序。

### 4.2 Canonical 节点联合

`SemanticNode` 当前只有三类：

| 节点 | 含义 | 默认 owner |
| --- | --- | --- |
| `SemanticOperation` | 语义和来源都已有证据的 effect | `semantic` |
| `RawInstructionOp` | opcode/参数已保留，但语义未确认 | `raw` |
| `SyntaxStatement` | label、time、branch、call、var、assign、return、raw syntax 等 | `syntax` |

每个源 instruction 恰好生成一个 `SemanticOperation` 或一个
`RawInstructionOp`。普通语句生成一个 `SyntaxStatement`。被折叠的 rank literal
行不再成为独立节点，而由实际 consumer 的 `SelectedValue` 拥有。

### 4.3 节点身份与来源

每个 canonical 节点包含：

- `NodeId`：模块内唯一身份，当前格式为
  `<routine-or-<module>>:<physical-line>:<ordinal>`。
- `Provenance`：source game、routine、source span、原 opcode、助记名、签名、
  原始文本和 confidence。
- `NodeOwnership`：明确指定 semantic/raw/syntax lowerer，防止两个 lowerer
  同时消费一个节点。

`NodeId` 不是内容 hash，也不包含 source path；它只在模块内唯一，并在源码
行位置不变时保持稳定。跨模块关联必须同时使用模块身份或 provenance。

### 4.4 值与表达式

核心值对象包括：

- `SemanticOperand(name, value)`：operand 名称表达语义角色，而不是位置编号。
- `OperandValue`：区分普通值、unused、keep-current、default 和 engine sentinel。
- `ExpressionIR`：保留原表达式文本，同时附带 typed variable/stack span。
- `VariableRef`：包含 semantic ID、value/storage type、scope、access、
  propagation、confidence 和 source encoding。
- `StackRef`：表示 TH13+ routine ABI 中的相对栈槽，不冒充游戏变量。
- `DifficultyGuard`：八 lane `E/N/H/L/X/O/6/7` 执行 mask。
- `SelectedValue` / `SelectionCase`：consumer 所拥有的运行时难度选择表。
- `EngineValue`：live player/random angle 等按帧求值的引擎值。

`ExpressionIR` 当前仍是“原文本 + typed spans”，不是完整的 literal/unary/
binary/cast/call AST。这是结构化语法跨 ABI lowering 的主要限制之一。

### 4.5 命名规则

Canonical operation 使用稳定的领域路径，例如：

```text
flow.wait
movement.velocity.tween
bullet.transform.append
anm.set_sprite
enemy.create
```

命名必须描述 effect，而不是来源 opcode、游戏编号或目标实现。opcode 只存在于
provenance、reference registry 和目标 encoding 中。新增语义时应优先扩展现有
领域词汇，不应建立 `th12_to_th15_*` 一类 canonical 类型。

## 5. 游戏差异与注册表

### 5.1 `GameProfile`

[`dialects/game_profile.py`](dialects/game_profile.py) 的 `GameProfile` 聚合每个游戏的目标契约：

```text
game / generation / opcode_family
capabilities
SentinelCodec
BulletDialect
TransformDialect
RoutineDialect
VariableDialect
extension_namespace
```

其中：

- `generation` 仅用于语法和大类能力，不证明 opcode 相同。
- `opcode_family` 只控制 raw passthrough 风险边界。
- `capabilities` 描述目标能否原生表达某类语义。
- `RoutineDialect` 描述 call、local、structured syntax 和 relative-stack ABI。
- `TransformDialect.forms` 是 transform opcode、write kind、参数集和 operand 顺序
  的唯一具体布局注册表。
- `VariableDialect` 负责数值变量编码与语义变量之间的双向投影。

TH06、TH07、TH08 即使同属第一世代，也使用独立 opcode family、bullet dialect、
transform dialect 和变量证据，不互相继承。

内部 game ID 和公开编译目标不是同一范围。parser/registry 还识别部分 side-game
ID；当前 `compile-ir --target` 的公开 choices 是 TH06、TH07、TH08、TH10 至
TH18 的十二个正作目标，不包含 TH09 和 side games。

### 5.2 Registry 职责

| 模块 | 当前职责 |
| --- | --- |
| [`dialects/reference.py`](dialects/reference.py) | 汇总 eclmap、文档和 thtk format arrays，提供带来源的 opcode 名称、签名及 tool ABI 校验 |
| [`canonical/op_ir.py`](canonical/op_ir.py) | 从每游戏证据生成 `OpSpec`，把方言名称规范化为 semantic operation key |
| [`dialects/semantics.py`](dialects/semantics.py) | 跨方言 semantic opcode/value、bullet shape、transform mode、spread 和 flag 词汇 |
| [`target/arg_adapter.py`](target/arg_adapter.py) | 按 semantic operand 名称适配目标参数布局和默认值 |
| [`canonical/variable_ir.py`](canonical/variable_ir.py) | 每游戏变量目录、表达式扫描和跨游戏变量/stack 投影 |
| [`dialects/anm_catalog.py`](dialects/anm_catalog.py) | 源 bank 的 role/purpose 语义证据和已观察 inventory；具体目标数字仍必须来自目标同关卡候选池 |

目标 opcode 必须在目标游戏的 `OpSpec` 或目标 dialect 中有明确条目。共享世代或
共享数字不是语义证据，不能作为 fallback。

当前 semantic decoder、generation mapping 和 argument layout 仍分散在
`canonical/op_ir.py`、`dialects/semantics.py`、`target/arg_adapter.py`。计划中的 `OperationSchema` 会把
canonical key、operand roles、source forms 和 target layouts 合并为单一 schema；
在此之前，新增映射需要同步检查这三个边界。

### 5.3 变量投影

数值 ID 先由源 `VariableDialect` 解码为 `VariableRef.semantic_id`，再由目标
dialect 按语义重新编码。跨游戏编码必须同时满足：

- 源和目标语义都有 documented confidence。
- value/storage type 兼容。
- storage scope 与 propagation 不冲突。
- 目标 access 不收窄当前 read/write use。
- routine local 和 relative stack ABI 兼容。

缺少目标槽位、语义碰撞、未知 bracket number、写权限不兼容或 ABI 不兼容都会
返回结构化 issue，而不是保留源数字让目标游戏重新解释。

### 5.4 ANM 资源边界

ANM 的 bank/script 数字不是跨游戏稳定 ID。当前 canonical 路径不再一律丢弃
`anm.select`、`anm.set_main`、`anm.set_sprite` 和 `anm.play*`，而是在
[`analysis/anm_resources.py`](analysis/anm_resources.py) 中为每次跨游戏 lowering
建立目标候选计划：

```text
target stage manifest
  -> root stage .decl + manifest ecli siblings
  -> AnmCandidatePool
       -> AnmCombinationCandidate
  + source canonical ANM groups
  -> AnmCandidateSelection / AnmCallSiteMaterialization
  -> AnmLoweringPlan
```

`stage01.decl` 与 `st01.decl` 都归一到 stage id `01`。候选只从目标游戏该关卡
主文件和其 `ecli` manifest 引用的兄弟模块提取；`default.ecl` 不作为关卡候选
来源。无法识别 stage id、目标不存在同编号 root，或 manifest 内没有合适组合
时返回空候选/structured unsupported，不会退回全游戏 corpus，也不会跨关卡借
数字。因此原版 ECL 在这里证明的是“这组 bank/script 确实由目标包加载并使用”，
不是源动画与目标动画视觉等价。

`AnmCombinationCandidate` 把一个 bank 与连续出现的 `set_main/set_sprite` 动作
序列作为一个原子组合保存。lowering 选择组合后，会一起发射所需的
`select + set`，而不是分别挑选 bank、slot 和 script 后拼出目标原版从未出现的
组合。`play/play_abs/play_high/play_pos/play_rotate/selected_play` 也从同一包收集；
候选只替换资源 bank/script。`play_pos/play_rotate` 的位置、角度等非资源参数仍
取自源节点，并先经过目标变量方言投影；无法投影时返回 structured unsupported。
`layer/alpha/scale/rotate` 等本身不引用资源 ID 的 ANM 操作不受候选 gate 影响。

候选按 `common`、`stage`、`midboss`、`boss` role 隔离。`common` bank 由游戏
世代的已知布局识别（TH10-12 为 0，TH13+ 为 0/1），stage/boss bank 再结合
目标 artifact 身份判断，midboss 不会并入 boss。routine 名称可以给目标包中
已经存在的组合增加 purpose 排序
证据，例如 `stage_blue`，但名称本身不能授权包外 script，也不是 role 的唯一
依据。

`AnmCandidateSelection` 记录目标动作、匹配种类、目标 stage、源 bank/script
以及原版文件/routine evidence。同名 routine 中同类 play 的相同顺序位置优先
形成 `routine_sequence` 匹配；明确的 semantic purpose 也可走 strict lowering。
只有数字相同或包内频率 fallback 时标记 `LOSSY`，诊断码为
`anm.heuristic_package_candidate`；动态 script 若只能固定替代则使用
`anm.dynamic_script_candidate`。两者都需要 `--allow-lossy`。没有同 role 候选、
目标缺少对应 opcode，或 play 的上下文参数无法投影时仍是 unsupported。这里的
strict/direct 表示选择证据与发射条件可验证，不表示运行时动画已经等价。

有一类动态 script 可以安全前移到调用点。`AnmCallSiteMaterialization` 只在以下
条件全部满足时生成：callee 开头是连续且无难度 guard/selected value 的
`select + set` 组，之前只有 `var`/comment；script 只由 literal 或直接 formal
parameter 构成；当前源 package 除 `default.ecl` 外没有 sibling module；模块内
没有 routine 字符串 dispatch，且所有已见引用都是非递归同步直接调用；每个调用
点实参都是整数 literal；每个调用点都能按 semantic purpose 选到目标组合。分析
采用全有或全无策略：任一条件不满足，就不折叠 callee 中的原组。成功时在每个
call 前发射相应目标组合，并把 callee 原资源动作标记为 folded，而不是把某一个
固定 script 猜回动态参数。

`AnmLoweringPlan.target_anim` 取目标关卡主 manifest 的 `anim` 列表，
`TargetAstBuilder` 用它替换目标模块的 `anim` 声明，使已选组合对应的原版 ANM
文件确实被加载。当前只投影 `anim`，其他资源类别仍沿用原有资源路径。

当前候选提取会在 call/goto/label/return 等控制边界断开 bank 状态，并在 guard
变化时断开原子组；源 lowering 也不会把不同 difficulty guard 的动作折叠到同一
statement。不过它仍是保守的 routine 线性分析，尚未执行完整 CFG state join 或
逐 difficulty lane bank-flow。分支后 bank 不一致、难度专用资源状态和更复杂的
跨 routine 数据流会保留为 unsupported；这些情况需要后续 typed `AnmResourceRef`
与 CFG/difficulty-aware analysis。thecl 能编译候选输出只证明目标语法与资源编号
可接受，不能证明画面、时序或运行时行为等价。

## 6. 派生分析

canonical state 分析只读取 canonical IR；目标 ANM candidate analysis 还读取
目标原版 package evidence。两类结果都通过 `source_node_id` 关联 canonical
节点，不能改变源码顺序，也不能独立拥有 lowering。

当前 `.eclir` 中正式持久化的 canonical analysis projection 是
`bullet_manager`。CFG、transform index resolution 和目标相关的 ANM lowering
plan 都由目标端按需重算；它们尚未作为独立 projection schema 持久化。ANM
候选还依赖目标原版 package corpus，因此不是 `SemanticModule` 自身的一部分。

### 6.1 Bullet state projection

[`analysis/bullet_ir.py`](analysis/bullet_ir.py) 将多条 bullet manager 指令解释为统一状态：

- visual、formation、origin、sounds、auto-fire 和 deferred fire。
- 每个 manager、每个 difficulty lane 的持久定义状态。
- fire 时生成不可变 `BulletEmitterDefinition` snapshot。
- transform replace、append、cursor decrement、copy、string patch 和 holes。

这不是把一组指令替换成一个 owning `BulletEmitter` 节点；原 canonical 节点仍然
逐条存在，analysis action 只引用其 `NodeId`。

### 6.2 CFG 与 transform index

[`analysis/control_flow.py`](analysis/control_flow.py) 在 routine 内构建 label、goto、conditional
goto 和 fallthrough 边，并使用 Tarjan SCC 标记循环节点。当前 CFG 是保守分析：

- 循环内 append cursor 被视为 loop-carried state，不能静态猜测 index。
- 当 TH13+ append transform 降到只支持显式 index 的目标时，只有所有活跃难度
  lane 都解析到同一 index 才允许输出。
- 当前尚未实现完整的分支状态 join 和跨 routine 数据流。

[`analysis/transform_ir.py`](analysis/transform_ir.py) 的 `BulletTransformIR` 把 source opcode 与
canonical write kind、parameter set、mode semantic、operand state 分离。目标端
最后才根据 `TransformDialect.forms` 选择 opcode 和字段布局。

## 7. Lowering 与目标输出

### 7.1 Planner 与 policy

[`target/lowering.py`](target/lowering.py) 的 `LoweringPlanner` 对每个 canonical 节点生成一个
`CapabilityDecision`。policy 独立于 canonical IR：

```text
allow_lossy = false
preserve_syntax = true
preserve_raw_same_family = false
preserve_raw_cross_family = false
```

四种 strategy 为：

| Strategy | 含义 |
| --- | --- |
| `direct` | 目标有已验证的等价表示 |
| `raw` | 保留结构语法或显式允许的 raw 方言；跨游戏 raw 会带 warning |
| `lossy` | 使用已登记近似，必须显式 `--allow-lossy` |
| `unsupported` | 无法证明安全表示，保留诊断和源文本注释，不生成该行为 |

主要决策顺序为：

1. 验证 node kind 与 ownership。
2. 同游戏优先使用 provenance opcode + canonical operands 的 identity 路径。
3. 检查 selected value、ANM candidate、变量、routine ABI 和 legacy timeline
   dialect region 等前置条件。
4. 按 semantic feature 匹配 capability rule。
5. 调用目标 emitter 选择具体 opcode、参数布局或 state-aware lowering。
6. 把 backend 无结果、非法参数或显式近似转换为结构化 decision/diagnostic。

`LoweringResult.successful` 要求所有 decision supported，且没有 error diagnostic。
不能只根据目标文本是否被 thecl 接受判断 lowering 成功。

### 7.2 Target 层

[`target/target_ir.py`](target/target_ir.py) 当前提供：

- `TargetStatement(source_node_id, strategy, lines, guard, diagnostics)`
- `TargetRoutine(name, params, params_inferred, body)`
- `TargetModule(source_game, target_game, resources, top_level, routines, diagnostics)`

`TargetAstBuilder` 保持 canonical routine/statement 顺序，并协调外部推断参数。
`CanonicalBackendEmitter` 使用 bullet/CFG analysis 处理隐式 manager 初始化、
transform append index 和 bullet visual catalog，并使用 manifest-scoped
`AnmLoweringPlan` 发射目标原版 ANM 候选；其他 operation 暂时通过 typed
`BackendEmission` 接入 legacy text backend。

`TargetModule.resources` 默认复制 `SemanticModule.resources`，但 ANM plan 有目标
关卡 manifest 时会把 `anim` 投影为目标原版列表。其他资源声明尚无通用跨游戏
投影；没有候选或缺少必要上下文的资源相关 instruction 仍由 strict planner
拒绝。

`TargetStatement` 目前仍以 `tuple[str, ...]` 承载目标文本，不是完整 typed target
AST。unsupported 节点会渲染为：

```text
// [diagnostic.code] node=... operation=...: reason
// source: original source text
```

这保证失败可见，但也意味着含 unsupported 的 `.decl` 可能仍被 thecl 编译；
thecl 成功只说明剩余文本语法成立，不说明被注释行为已经迁移。

### 7.3 CLI 成功语义

推荐的 canonical 工作流是：

```bash
python3 -m ecl_ir.cli emit-ir source.decl -o source.eclir.json
python3 -m ecl_ir.cli validate-ir source.eclir.json
python3 -m ecl_ir.cli compile-ir source.eclir.json --target th15 -o target.decl
```

`compile-ir` 默认就是 strict 模式。三个 opt-in 分别为：

- `--allow-lossy`：启用已登记的近似或 drop policy。
- `--preserve-raw-same-family`：允许未类型化 opcode 在同 family 中警告直通。
- `--preserve-raw-cross-family`：允许跨 family 警告直通，不证明目标 opcode 兼容。

`compile-ir` 会先写目标 `.decl`，再在存在 statement-level unsupported 时返回
非零。当前 CLI 退出码不覆盖 module-only error diagnostic，因此 routine 参数
ABI 等模块诊断可能在退出码为 0 时仍然存在。完整成功应同时满足：

```text
validate-ir ok
LoweringResult 没有 error diagnostic
strategy_counts.unsupported == 0
thecl return code == 0
target ECL 非空
```

`transpile` 和 `--legacy-patterns` 属于兼容路径，不应作为 canonical 架构验证。

## 8. `.eclir` 独立工件

外层 schema 当前为 `th062.eclir` v2：

```json
{
  "schema": "th062.eclir",
  "schema_version": 2,
  "source_bytes_base64": "...",
  "source_text": "...",
  "source_decoding": {},
  "source_sha256": "...",
  "source_layout": {},
  "program": {},
  "canonical_ir": {},
  "canonical_summary": {},
  "analysis_projections": {},
  "analysis_summary": {},
  "objects": []
}
```

其中嵌套的 canonical schema 是 `th062.semantic-ir` v1。`objects` 是兼容数据，
canonical `compile-ir` 默认不读取它。

三种 roundtrip 的承诺不同：

| 模式 | 数据源 | 承诺 |
| --- | --- | --- |
| 默认 | `source_bytes_base64` | 原始字节完全相同 |
| `--layout` | `source_layout` + source codec | 原始行内容和行尾完全恢复 |
| `--canonical` | `Program` renderer + `DeclTextCodec` | 结构等价、排版规范化，不承诺原始字节 |

`validate-ir` 当前检查 source hash/layout、重解析结构、canonical 重建一致性、
summary、routine/instruction 数量、signature、NodeId 唯一性、owner 匹配，以及
bullet analysis 的 `source_node_id` 引用。

当前验证器尚未强制 NodeId 字符串格式、source span 有效性、routine 名唯一性、
`NodeOwnership.covered_by` 引用、legacy `objects` 可重建一致性，以及 bullet 之外
analysis projection 的完整 schema 一致性。

当前还没有正式 JSON Schema 和 migration runner；多数 `from_dict` 为兼容读取
提供默认值。修改 serialized node layout 前必须先定义 schema migration。

## 9. 当前统一程度与兼容债务

已经统一的部分：

- canonical 三类节点、身份、provenance 和 ownership。
- capability-driven planner 与四类 decision。
- 每游戏 profile 下的 routine、variable、bullet、transform 和 sentinel dialect。
- source-first bullet shape semantic catalog。
- transform replace/append/cursor/copy 的统一 state model。
- instruction、syntax、selected value 共用变量/stack projection。
- manifest-scoped ANM candidate pool、原子组合选择、调用点物化和目标 `anim`
  manifest 投影。
- unsupported/lossy/raw 的结构化诊断，不静默丢失。

仍处于过渡状态的部分：

- `CanonicalBackendEmitter` 仍调用 `compat/backend.py` 的 legacy text encoder。
- `canonical/op_ir.py` 仍包含少量历史 generation/policy sequence；`compat/backend.py` 仍有目标
  codegen 特化，详见 `backend-special-cases.md`。
- operation decoder、semantic mapping 与 argument layout 尚未合并为
  `OperationSchema`。
- movement、enemy、boss、laser 和其他 resource 的旧 Pattern analysis 尚未全部
  迁入 canonical non-owning analysis；ANM 候选已进入 canonical target 路径，但
  仍缺 CFG/difficulty-aware typed resource flow。
- `TargetStatement.lines` 和 `ExpressionIR.text` 仍是 string-backed 边界。

新增实现时应遵守：

1. 先定义稳定 semantic key 和 typed operand roles。
2. 每个源游戏只负责“方言 -> semantic”，每个目标游戏只负责
   “semantic -> 方言”。
3. 状态型行为进入基于 canonical `NodeId` 的 analysis/reducer，不建立
   `source_game,target_game` 组合处理器。
4. 无法证明等价时返回 structured unsupported；近似必须有显式 policy 和
   warning。
5. 只有工具 ABI、目标 syntax 或真实能力差异可以留在 backend/profile。

普通无状态 operation 的扩展顺序应是：semantic key 与 operand roles -> 源方言
decoder -> target profile capability/dialect -> capability rule -> `arg_adapter`
layout -> target emitter。只有语义跨越多条语句、需要状态归约或需要多指令展开时，
才增加专用 analysis/lowerer。

## 10. 当前验证基线

截至本文状态基线：

- 107 项 Python 单元测试通过。
- 210 个仓库 `.decl` 均可 parse、构建 canonical IR 和 bullet analysis。
- 210 个 source document 与 source layout 均可逐字节 roundtrip。
- 同目标 canonical 覆盖 251,701 个节点，其中 160,275 个 instruction，statement
  顺序、instruction shape 和 effective guard mismatch 均为 0。
- Wine + Touhou Toolkit release 12 对 209/209 个可比较原始/canonical source
  生成逐字节相同 ECL；`th08/ecldata_yy.decl` 是原始 source 本身 malformed，
  两侧以相同诊断失败。
- 210 文件乘 12 目标的 strict planner matrix 完成 2,520 次 build，没有异常，
  但仍有 1,233,676 个 structured unsupported decision。

TH10-TH18 的 `stage01/st01.decl` 两两双向 Wine 检查覆盖 36 对、72 个方向：

- 72/72 IR validation 通过。
- 72/72 生成的 `.decl` 被 thecl 接受并产生非空 ECL。
- 64 个方向无 thecl 消息；8 个转 TH18 的方向有 opcode 535 参数不足警告。
- strict lowering 完整成功为 0/72，共有 10,074 个 unsupported 节点。

ANM 候选改造后另以 `--allow-lossy` 重跑同一组 10-18 `stage01/st01`，明确排除
`default.decl`：72/72 IR validation 和 72/72 Wine/thecl 编译通过，输出包含
4,232 处目标原版候选发射与 304 处源动作折叠；1,113 个仅有
package/frequency 证据的节点带 `anm.heuristic_package_candidate` 警告。8 个转
TH18 方向仍有共 117 条既有 opcode 535 参数不足提示，没有 ANM 指令参数数量
错误。

因此当前正确表述是：同游戏 canonical 行为已达到强二进制证据；跨游戏输出
已经普遍具备可编译语法，但尚未达到行为完整或运行时等价。

## 11. 主要后续边界

按架构依赖顺序，优先事项为：

1. 把 `TargetStatement.lines` 改为 typed instruction/syntax/comment/unsupported
   target node union。
2. 把 `ExpressionIR` 扩展为完整表达式 AST 和 routine symbol binding。
3. 合并 decoder、operand use 和 target layout 为一个 `OperationSchema`。
4. 在现有 ANM 候选计划之上引入 `AnmResourceRef` 与 difficulty/CFG-aware
   bank-flow analysis，处理分支和 lane 歧义。
5. 补全有证据的变量 catalog，尤其 TH06/07 和 side-game overlay。
6. 为 CFG 增加 divergent branch state join 和 difficulty-lane merge。
7. 将 laser lifecycle 及其他旧 Pattern 对象迁为 canonical action/reducer analysis。
8. 建立可重复的逐目标 thecl 集成测试与运行时等价测试。
9. 在改变 canonical serialized layout 前实现 schema migration。
