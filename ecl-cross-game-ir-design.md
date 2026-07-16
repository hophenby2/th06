# Touhou ECL 跨游戏抽象分析与 IR 设计报告

> 范围：基于 `th062/th06` 到 `th062/th18` 下所有 `.decl` 反编译 ECL 脚本，结合 `th062/ecl*.txt` 的 THBWiki 世代说明、Priw8 指令/变量/eclmap 资料进行归纳。本文重点不是逐条 opcode 解释，而是总结“ECL 汇编组合结构”以及如何提升为可跨游戏编译的高级对象/模块。

## 0. 重要结论

- ECL 的跨游戏迁移不应以“单条 opcode 一对一翻译”为核心，而应以“语义对象 + 后端 lowering”为核心。
- 最稳定的抽象单元是：`Enemy`、`Movement`、`BulletEmitter`、`BulletTransform`、`LaserEmitter`、`BossPattern`、`Timeline/Loop`、`DifficultySwitch`、`Resource/Animation`、`Flags/Collision`。
- 第一世代 TH06/TH07/TH08、第二世代 TH10/TH11、第三世代 TH12/TH12.5/TH12.8、第四世代 TH13+ 的 opcode 编号差异很大，但组合模式高度相似：
  - “设置属性 → 配置参数 → 激活/发射 → 等待/循环”是发弹、移动、激光、Boss 卡的共同骨架。
  - TH13+ 的子弹系统最像对象 API：`etNew → etAim → etSprite → etCount → etAngle → etSpeed → etEx* → etOn`。
  - TH10/TH11/TH12 的子弹系统以“弹幕槽/弹幕编号”为中心，使用 `set field + transform list + on`。
  - TH08 及第一世代更像宏 opcode：一次 `ins_96/97/98/99...` 就包含 style/color/way/layer/speed/angle/flags，变换由 `ins_111` 预置。
- 移植例如“TH15 发弹逻辑到 TH12”可行，但不是所有语义都可无损：TH15 的 `etEx/etExSet2`、部分 flags、游戏特有资源、取消/道具/灵击/季节/动物灵等需要降级、模拟或忽略。

### 0.1 当前 `ecl_ir` 实现基线

本文后续不少段落保留了早期对象 IR 设计草案。与当前实现冲突时，以已经落地的统一链路为准：

```text
SourceDocument
  -> Program
  -> DialectDecoder
  -> SemanticModule
       -> ExpressionIR
            -> VariableUse -> VariableRef
            -> StackUse    -> StackRef
  -> derived analyses (bullet state / CFG / target ANM candidates / patterns)
  -> LoweringPlanner(GameProfile)
  -> TargetModule
  -> .decl
```

- `SemanticModule` 是唯一拥有 lowering 顺序的 canonical effect stream；对象、状态和 CFG 都是引用 `NodeId` 的派生分析，不重复拥有源指令。
- `DifficultyGuard` 固定为八个独立 lane：`E/N/H/L/X/O/6/7`。旧作的 `4/5`、TH18.5 的 `0..7` 和现代的 `X/O` 只是方言拼写，raw marker 仍会保留。
- 运行时按难度选择的 literal table 使用 `SelectedValue(selector=difficulty)` 和 `SelectionCase`，并归实际消费它的 `SemanticOperation`、`RawInstructionOp` 或 `SyntaxStatement` 所有，不再只靠占位符文本。同游戏 identity lowering 会按原顺序重建所有表；尚未实现的跨游戏选择 lowering 会给出 `value_selection.unsupported`。
- `game_profile.TransformForm` 是 transform 具体布局的唯一 registry：记录 `opcode`、`write_kind`、`parameter_set` 和 operand 顺序。`BulletTransformIR` 统一承载 canonical operand state 与 semantic mode，避免维护游戏对游戏的 opcode 特化表。
- routine CFG 使用 Tarjan SCC 标记循环。循环内的 append cursor 是 loop-carried state，resolved index 强制为未知；降到只支持显式 index 的目标时给出结构化 unsupported，而不是猜一个槽位。
- 同游戏编译走 provenance opcode + canonical operands 的 identity 路径，不经过跨代 backend；selected values 也在该路径恢复。
- bullet shape 先按源游戏 catalog 解码为语义名称，再按目标 catalog 编码。TH06、TH07、TH08 分开，TH13/14 的 pre-TH15 插号与 TH15+ 现代表分开；目标没有条目或发生视觉合并时显式报告 unsupported/lossy。
- transform sentinel 由 `(game, semantic mode, operand role)` 共同解释。`unused`、`keep_current` 与引擎动态值互不混用；live player/random angle 使用 `EngineValueKind` 和 `PER_FRAME` evaluation time，在目标存在编码时重编码。
- `ExpressionIR` 以 source-preserving text 加 typed `VariableUse` / `StackUse` span 统一承载 instruction、selected value 与 syntax expression 中的引用。`VariableRef` 区分 semantic ID、value/storage type、scope、access、propagation、confidence 和结构化 source encoding；`StackRef` 表示 TH13+ routine ABI 的相对槽位，不冒充可以按 semantic ID 重编码的游戏变量。每个 `GameProfile` 持有独立 `VariableDialect` 与 `RoutineDialect`。跨游戏找不到同语义目标、数值碰撞、写权限收窄或 routine ABI 不兼容时 structured unsupported，TH06/07 不套用 TH08 表。
- 未识别的 `[number]` 也不会留作裸文本：它成为 `Confidence.UNKNOWN` 的 opaque reference，只允许同游戏 identity。legacy timeline 成员则携带 typed `DialectRegion`，整个 game-specific timeline opcode block 跨游戏统一拒绝。
- target opcode 必须在目标游戏 registry 中有同一 semantic key 的明确条目；不能从 TH13/TH15/TH08 借一个同世代数字。canonical 默认关闭 lossy/drop 与跨游戏 RAW，只有显式 policy opt-in 才开放，并把 warning 写在对应目标语句旁。
- ANM bank/script ID 当前通过目标同关卡原版 ECL 的 manifest-scoped candidate pool 投影：连续 `select + set_main/set_sprite` 保持原子组合，`play*` 只替换资源参数，目标 `anim` 声明同步投影；动态或无法证明的选择仍按 lossy/unsupported 处理。完整的 CFG/difficulty-aware typed resource flow 尚未完成。
- 当前 `TargetStatement` 仍以 `lines: tuple[str, ...]` 为 envelope，并非完整 typed target AST；完整 expression node union 与 typed target statement union 仍属于下一阶段。

## 1. 数据集概况

| 游戏目录 | 文件数 | 函数/子程序数 | 指令总数 | 唯一 opcode 数 | 世代 |
| --- | ---: | ---: | ---: | ---: | --- |
| `th06` | 7 | 321 | 10638 | 112 | 第一世代 |
| `th07` | 8 | 762 | 22429 | 141 | 第一世代 |
| `th08` | 24 | 1449 | 38696 | 149 | 第一世代 |
| `th10` | 8 | 654 | 9210 | 108 | 第二世代 |
| `th11` | 20 | 863 | 10985 | 122 | 第二世代 |
| `th12` | 9 | 854 | 12709 | 124 | 第三世代 |
| `th13` | 21 | 732 | 9922 | 143 | 第四世代 |
| `th14` | 24 | 827 | 10662 | 142 | 第四世代 |
| `th15` | 23 | 850 | 11112 | 136 | 第四世代 |
| `th16` | 22 | 826 | 10584 | 144 | 第四世代 |
| `th17` | 22 | 855 | 9931 | 119 | 第四世代 |
| `th18` | 22 | 838 | 10197 | 131 | 第四世代 |

说明：统计只按 `ins_N(...)` 形态计数，不包含 `goto`、`if`、变量赋值、难度标记等非 `ins_` 语句。

## 2. ECL 的组合结构

### 2.1 函数/子程序层

跨游戏稳定模式：

```text
sub/void PatternName() {
  初始化资源/敌机属性/碰撞/动画
  可选：创建异步子任务 @Pattern_at() async
  移动/等待/循环
  删除或 return
}

sub/void PatternName_at() {
  var loopCounter / temp vars
  预等待 wait
  配置发弹/激光对象
  loop:
    发射/激活
    wait(interval)
    if counter-- goto loop
  return
}
```

常见命名也反映语义：`*_at` 多为 attack task，`*func` 多为行为函数，`*Dead` 为死亡反击/清理，`BossCard*`/`MBossCard*` 为卡或非。

routine 语法不能只按文本直通。`RoutineDialect` 分别声明 call、local、structured-expression 与 relative-stack 编码：TH06-08 使用 numbered-call/fixed-register ABI，TH10+ 使用 named-call/named-stack ABI，TH13+ 另外支持相对栈槽。具名调用、局部变量、routine parameter、现代 goto/assign/return/raw-expression/prototype 或 `StackRef` 跨入不兼容 ABI 时分别产生结构化诊断，而不是为每对游戏维护特化转换。

### 2.2 时间结构

跨游戏常见：

- `wait(t)`：第四世代 `ins_23` 极高频；第一世代/TH08 以时间标签 `+N`、`ins_2/ins_105/ins_106` 等表达等待。
- `goto label @ time` + `if counter-- goto`：所有世代都存在循环结构。
- 难度块：`!E !N !H !L/!LO !*` 在反编译脚本中作为条件覆盖参数。canonical guard 应抽象为八 lane `DifficultyGuard(E/N/H/L/X/O/6/7)`；instruction 或 syntax consumer 的运行时难度选择则用 `SelectedValue<T>`，不能把两者混成一个四难度值。
- 异步任务：第四世代 `@Sub() async` / 调用子任务；第一世代也有子例程调用，但表示方式不同。

高级 IR 应把时间提升为：

```yaml
Timeline:
  - wait: 30
  - spawn_task: emitter_loop
  - move: {duration: 60, mode: 0, velocity: ...}
  - loop: {count: difficulty(...), body: [...]}
```

### 2.3 资源与动画组合

第四世代典型组合：

```text
ins_302(anmFile)      # anmSelect
ins_303(slot, script) # anmSetSprite
ins_306(slot, script) # anmSetMain / main animation
ins_307(a,b)          # anmPlay
```

第二/第三世代对应：`258/259/262/263/264...`。

第一世代/TH08 对应：`anmSet/anmSetEx/anmSetSlot` 一类 opcode，如 TH08 的 `54-62` 区间。

抽象为：

```yaml
AnimationState:
  file: enemy | stage_enemy | bullet | index
  slots:
    - slot: 0
      script: 80
      role: main
  play: optional
  mirrorPolicy: auto | fixed | no_mirror
```

当前实现没有把这个抽象做成一张“源游戏 A 到目标游戏 B”的映射表，而是为目标
关卡即时构建候选计划：

```text
目标 stage 主 manifest + 其 ecli 兄弟模块
  -> AnmCandidatePool
       combinations: AnmCombinationCandidate[]
  -> AnmCandidateSelection
  -> AnmLoweringPlan
       callSites: AnmCallSiteMaterialization[]
       targetAnim: string[]
```

候选池的 scope 是目标 package，不是整个游戏的 bank/script 并集。同关卡原版
ECL 中连续出现的 `select + set_main/set_sprite` 被视为一个原子 preset；选择器
不能分别取 bank、slot、script 后拼接成原版未出现的组合。候选按 `common`、
`stage`、`midboss`、`boss` role 隔离，routine 名称只用于给包内候选提供弱 purpose
排序证据，不能单独证明资源身份。

`play/play_abs/play_high/play_pos/play_rotate/selected_play` 的候选同样来自目标包。
bank/script 使用目标候选；位置、角度等非资源参数保留源语义并投影到目标变量
方言，无法投影时显式 unsupported。资源无关的 `layer/alpha/scale/rotate` 不需要
通过这个候选 gate。

callee 入口处由 formal parameter 决定 script 时，`AnmCallSiteMaterialization`
可以把目标组合前移到每个调用点，但安全条件是全有或全无：入口组合必须连续、
无 guard/selected value，源 package 除 `default.ecl` 外没有 sibling，模块内没有
routine 字符串 dispatch，所有已见引用必须是非递归同步直接调用，每个相关实参
必须是整数 literal，并且每个调用点都能得到 semantic-purpose 候选。任一条件
失败，就不折叠 callee 原组合。

semantic-purpose 或目标同名 routine 的同序 play 候选可在 strict 模式发射；
仅数字相同/频率 fallback，以及把真正动态的 script 固定成某个目标候选，都属于
`LOSSY`，必须显式开启 `--allow-lossy`。目标原版 evidence 证明该组合被目标包
加载和使用，不证明它与源动画在画面、碰撞时序或其他运行时行为上等价。无法
识别目标 stage package 时返回空候选，不允许退回全游戏并集。

### 2.4 碰撞、flag、掉落、属性组合

第四世代典型：

```text
ins_500(w,h)   # setHurtbox
ins_501(w,h)   # setHitbox
ins_502(flags) # flagSet
ins_503(flags) # flagClear
ins_507(...)   # dropExtra / drop related
ins_510/511    # drop/life 等，视世代不同
```

TH13+ 的 flags 可抽象为统一位集：`NO_HURTBOX`、`NO_HITBOX`、`OFFSCREEN_LR`、`OFFSCREEN_UD`、`INVINCIBLE`、`NO_DELETE`、`GRAZE`、`RECT_HITBOX` 等。第一世代 flags 与第四世代不完全同构，需要后端映射表。

### 2.5 移动组合

第四世代典型：

```text
ins_400(x,y)              # movePos
ins_401(t, mode, x, y)    # movePosTime
ins_404(angle, speed)     # moveVel
ins_405(t, mode, angle, speed) # moveVelTime
ins_424/425/426...        # mirror/bezier 等版本
```

TH12 第三世代是同语义但编号整体提前：`300..327` 一带；第二世代常见 `300/320` 体系；第一世代/TH08 为 `movePos/moveDir/moveCurve` 等低编号。

应抽象为：

```yaml
Movement:
  position:
    mode: absolute | relative | add | boss_area | random_area | bezier | circle | ellipse
    x, y, z: expr?
    duration: int?
    interp: linear | ease | bezier_mode | raw_mode
  velocity:
    angle: expr?
    speed: expr?
    duration: int?
  bounds:
    rect: [l,t,r,b]
    clear: bool
```

### 2.6 发弹组合

这是最适合封装为对象的部分。

#### 第四世代 TH13+

统计中最稳定的三元组是：

```text
600,607,602
607,602,606
602,606,604
606,604,605
604,605,611
```

对应语义：

```text
ins_600(id)                  # etNew
ins_607(id, aimMode)          # etAim
ins_602(id, sprite, color)    # etSprite
ins_606(id, ways, layers)     # etCount
ins_604(id, angle, angleStep) # etAngle
ins_605(id, speed, speedStep) # etSpeed
ins_608(id, sound, unknown)   # etSound，可选
ins_609/610/611/612(...)      # ex/transform，可多条
ins_601(id)                  # etOn / fire
```

也常见 `625/624` 这类 rank/difficulty 版本，例如 TH15/TH18：

```text
ins_625(id, count/rank params...)
ins_624(id, speed/rank params...)
```

#### 第三世代 TH12

TH12 eclmap 显示：

```text
500 etNew
501 etOn
502 etSprite
503 etOffset
504 etAngle
505 etSpeed
506 etCount
507 etAim
508 etSound
509 etEx
510 etClearAll
511 etCopy
512 etCancel
513 etClear
...
```

其中只有 `509` 是 indexed transform write。`510` 是全屏清弹，`511` 是 manager copy，`512` 是范围消弹；它们不能作为 `609/610/611/612` 的四个旧版对应项。基础 manager 配置与 TH13+ 接近，但 transform form、cursor 模型和参数能力必须分别 lowering。

#### 第二世代 TH10/TH11

典型片段：

```text
ins_400(slot) / ins_401(slot)     # 选择/激活弹幕槽，具体依世代表
ins_402(slot, sprite, color)
ins_404(slot, angle, angleStep)
ins_405(slot, speed, speedStep)
ins_406/407(...)                  # count/aim/offset 等
ins_409(slot, index, mode, type, a, b, x, y) # transform list
ins_401(slot) 或相关 opcode 发射
```

统计显示 TH10/TH11 的 `409,409` 极高，说明 bullet transform 是核心表达方式。TH10 中常见：

```text
ins_409(0, 0, 1, 4, ...)
ins_409(0, 1, 1, 1, ...)
ins_409(0, 2, 0, 8192, 100, ...)
```

#### 第一世代 TH08/TH06/TH07

TH08 典型：

```text
ins_96(style, color, way, layer, minSpeed, maxSpeed, angle, angleDif, flags) # aimed fan
ins_97(...) # unaimed fan
ins_98(...) # aimed ring
ins_99(...) # unaimed ring
ins_111(index,type,channel,a,b,x,y) # transform
ins_107/108 # 自动/延迟发射控制
```

TH06/TH07 的 opcode 编号与 TH08 又不同，但仍能抽象为“一条宏发弹 opcode + 可选变换 + 等待/循环”。

### 2.7 激光组合

第四世代：

```text
ins_700(id)                  # laserNew
ins_701(id, startup, expand, duration, shrink, flags) # laserTiming
ins_704(id, x, y)            # laserOffset
ins_705(id, angle, speed...) # trajectory
ins_706/707/708/709/710      # straight laser length/width/angle/rotation/end
ins_702(id)                  # laserOn
ins_711(id)                  # laserCuOn / curve laser on
```

第三世代 TH12 对应 `600..611`，整体少 100。第二世代/第一世代激光能力更受限，应以 `LaserEmitter` 降级到可支持字段。

### 2.8 Boss/Spell 组合

第四世代 Boss 脚本常见结构：

```text
ins_511(life)
ins_512(bossId / boss mode)
ins_513()                 # timer reset / phase reset
ins_514(slot, life, time, subName) # interrupt/pattern setup
ins_521(slot, escapeSub)
ins_523() / ins_524(...)  # spell end/chapter/marker 等
ins_537/538/539(...)      # spell/card declaration variants
```

抽象为：

```yaml
BossPattern:
  bossId: 0
  hp: 2500
  timeout: 2400
  type: nonspell | spell | timeout_spell | survival
  spellName: string?
  spellId: int?
  onTimeout: sub?
  onDeath: sub?
  onEscape: sub?
  score: int?
  hideLife: bool?
  chapters: [...]
```

## 3. 跨游戏 opcode 对应关系

### 3.1 大类编号迁移

| 语义 | 第一世代/TH08 | 第二世代 TH10/11 | 第三世代 TH12 | 第四世代 TH13+ |
| --- | --- | --- | --- | --- |
| 敌机创建/ANM | TH08 `54-62`, `90-94` 等；TH06/07 不同 | `256-279` | `256-335` | `300-337/340` |
| 移动 | TH08 `63-76` 等 | `300-336` | `300-327` | `400-447` |
| 碰撞/属性/掉落/Boss | TH08 `77-95`, `120+` 等 | `400+` | `400-456/562` | `500-572` |
| 子弹 | TH08 `96-113` 等宏发弹 | `400-419`，尤其 `409` transform | `500-535` | `600-641` |
| 激光 | TH08 `114-121` 等 | 视作品，能力较有限 | `600-611` | `700-714` |
| 敌机交互 | 少量 boss/enemy call | 少量 | 少量 | `800-802` |
| 调试/备用/游戏特有 | 分散 | 分散 | `700+`/特殊 | `900+`, `1000+` |

THBWiki 第四代页也指出了大致偏移：第四代 `300/400/500/600` 对应第三/第二世代的创建、移动、属性、子弹区间。实际移植时不能只做 `+100`，因为参数顺序、拆分粒度、游戏特有 opcode 会变。

### 3.2 子弹语义字段并集

建议用统一 `BulletEmitter` 覆盖所有世代：

```yaml
BulletEmitter:
  id: int = 0
  coordinateSpace: enemy | absolute | relative | boss | custom
  origin:
    x: expr = 0
    y: expr = 0
    polarOffsetAngle: expr? = null
    polarOffsetRadius: expr? = null
  appearance:
    style: int
    color: int
    hitboxStyle: int? = null
    spriteSource: enemy_anm | bullet_anm | game_default
  aim:
    mode: aimed_fan | fan | aimed_ring | ring | offset_aimed_ring | offset_ring | random_angle | random_speed | random_angle_speed | custom
    baseAngle: expr = 0
    angleStep: expr = 0
    aimOffset: expr = 0
    target: player | boss | point | none
  count:
    ways: expr = 1
    layers: expr = 1
    bulletsPerLayer: expr? = ways
    layerStepAngle: expr? = angleStep
  speed:
    first: expr = 1
    last: expr? = null
    step: expr? = null
    randomMin: expr? = null
    randomMax: expr? = null
  timing:
    fireDelay: int = 0
    repeat: int = 1
    interval: int = 0
    autoFire: bool = false
    life: int? = null
    offscreenTime: int? = null
  sound:
    id: int? = null
    mode: int? = null
  flags:
    raw: int = 0
    transformFlags: int = 0
    clearable: bool? = null
    grazeable: bool? = null
  transforms:
    - BulletTransform
  difficultyOverrides:
    E: partial BulletEmitter
    N: partial BulletEmitter
    H: partial BulletEmitter
    L: partial BulletEmitter
    X: partial BulletEmitter
    O: partial BulletEmitter
    6: partial BulletEmitter
    7: partial BulletEmitter
```

`null`/缺省表示“不使用”；编译到旧游戏时不可支持字段应进入 lowering 策略：忽略、近似、展开成多个 emitter、或报错。实际 canonical IR 中难度覆盖不以内嵌对象字典作为唯一真相：execution mask 使用 `DifficultyGuard`，literal selection 使用 `SelectedValue`，派生的 `BulletEmitter` state 只引用对应 canonical `NodeId`。

`appearance.style` 在上述并集草图里是源方言输入，不应成为跨游戏 identity。当前实现先用源游戏优先的 catalog 将它提升为 `bullet_shape` semantic，再查询目标 catalog；若没有经过验证的目标形状，则拒绝 direct lowering。这样可以区分 TH06/07/08 同一数字的不同含义，以及 TH13/14 与 TH15+ 插号造成的编号漂移。

### 3.3 BulletTransform 并集

```yaml
BulletTransform:
  writeKind: replace | append
  parameterSet: base | extended
  manager: expr? = null
  index: expr? = null       # replace 时显式；append 跨代 materialize 后才可能得到 resolved index
  channel: int = 0
  modeSemantic: string
  trigger:
    afterFrames: int? = null
    condition: none | distance | offscreen | graze | custom
  action:
    type: stop | changeVelocity | aimToPlayer | setAngleSpeed | accel | changeStyleColor | wait | spawnSubBullet | curve | customRaw
    angle: expr? = null
    speed: expr? = null
    accel: expr? = null
    style: int? = null
    color: int? = null
    duration: int? = null
    repeat: int? = null
  raw:
    th08Type: int? = null
    th10Type: int? = null
    th13ExType: int? = null
    args: []
```

映射：

- TH08 `ins_111(index,type,channel,a,b,x,y)` → `BulletTransform`。
- TH10/11 `ins_409(slot,index,mode,type,a,b,x,y)` → `BulletTransform`。
- TH12 只有 `ins_509` → indexed `replace/base` transform；`510/511/512` 分别是 clear-all、copy、cancel。
- TH13+ `ins_609/610/611/612` 正交为 `replace/base`、`replace/extended`、`append/base`、`append/extended`。

具体 opcode 布局由各游戏 `TransformDialect.forms: tuple[TransformForm, ...]` 统一注册。transform reducer 和 backend 都查询同一 registry，不再各自维护一份 layout 表。append 降到 TH10/11/12 时，只有 CFG/难度 lane 分析得到唯一静态 index 才能 materialize 为 `409/509`。

### 3.4 LaserEmitter 并集

```yaml
LaserEmitter:
  id: int = 0
  kind: straight | infinite | curve | beam_warning | custom
  origin: { x: expr = 0, y: expr = 0 }
  timing:
    startup: int = 0
    expand: int = 0
    active: int = 0
    shrink: int = 0
    delay: int = 0
  geometry:
    length: expr? = null
    width: expr? = null
    angle: expr = 0
    angularVelocity: expr = 0
    speed: expr = 0
    endLength: expr? = null
  appearance:
    laserId: int? = null
    color: int? = null
    sprite: int? = null
  flags:
    raw: int = 0
  curve:
    points: []
    nodeCount: int? = null
    mode: int? = null
  transforms:
    - LaserTransform
```

后端：TH13+ 直接降到 `700..711`；TH12 降到 `600..611`；TH08/早期如缺曲线激光则降级为直线激光或报 `unsupported(curveLaser)`。

## 4. 高级 IR 总体设计

概念上可分为源 AST、canonical effect stream、派生对象分析和目标 lowering。当前实现不把派生对象当作第二条 lowering 主链；它们只能引用 canonical `NodeId`。

### 4.1 AST 层：保留脚本结构

```yaml
Program:
  game: th15
  resources:
    anim: [enemy.anm, st01enm.anm]
    ecli: [default.ecl, st01bs.ecl]
  functions:
    - Function

Function:
  name: GirlA01_at
  locals: [A]
  body: [Statement]

Statement:
  kind: wait | loop | if | goto | call | async | setVar | rawIns | objectOp
```

### 4.2 派生 Object Analysis：把 opcode 组合投影为对象

核心对象：

```yaml
EnemyObject
MovementController
AnimationController
CollisionProfile
DropProfile
BulletEmitter
LaserEmitter
BossPattern
DialogueEvent
SoundEvent
ScreenEffect
DifficultySwitch
```

示例：TH15 片段

```text
ins_600(0);
ins_607(0, 0);
ins_602(0, 4, 6);
ins_606(0, 1, 1);
ins_604(0, 0.0f, 0.05235988f);
ins_605(0, speed, 1.0f);
ins_611(0, 0, 2, 1, ...);
ins_601(0);
```

提升为：

```yaml
BulletEmitter:
  id: 0
  appearance: {style: 4, color: 6}
  aim: {mode: aimed_fan, baseAngle: 0.0, angleStep: 0.05235988}
  count: {ways: 1, layers: 1}
  speed: {first: difficulty(E:1.5,N:1.5,H:2.0,L:3.0), step: 1.0}
  transforms:
    - {index: 0, action: {type: setAngleSpeed}, raw: {th13ExType: 2, args: [...]}}
  fire: once
```

该对象是便于状态分析和模式识别的 projection。真正的 source order、ownership 和 lowering owner 仍在 `SemanticModule`，避免 canonical node 与 object cluster 同时发射同一条指令。

### 4.3 Backend lowering 层：按目标游戏生成 opcode

当前 canonical 路径使用一个由 profile/registry 参数化的 emitter，不为每一对源/目标游戏复制 backend：

```text
CanonicalBackendEmitter
  + GameProfile(capabilities, sentinels)
  + BulletDialect
  + TransformDialect(TransformForm registry)
  + semantic catalogs
```

职责：

1. 选择 opcode 族。
2. 把对象字段降到目标支持的 opcode 参数。
3. 按 `(game, transform semantic mode, operand role)` 处理缺省值与 sentinel，而不是全局替换某个数字：同一 token 可能是 `unused`、`keep_current` 或普通数值。
4. 对不支持字段进行策略处理：
   - `ignore`: 忽略非关键视觉字段。
   - `approximate`: 近似，例如把复杂 transform 展开为多个简单变换。
   - `expand`: 展开成多个 emitter/subtask。
   - `error`: 无法正确移植时报错。

transform operand 当前使用 `OperandState.VALUE/UNUSED/KEEP_CURRENT/ENGINE_SENTINEL`。引擎每帧求值的动态角度另有 typed 表示：

| 语义 | TH13/14 | TH15-17 | TH18/18.5 |
| --- | --- | --- | --- |
| `live_player_angle` | `999.0f` | `999999.0f` | `3000000.0f` |
| `live_random_angle` | 不支持 | 不支持 | `4000000.0f` |

这些 token 解码为 `EngineValueKind`，evaluation time 是 `PER_FRAME`。目标没有相应 token 时必须 structured unsupported，不能把它当普通 float 或 keep-current 值。

## 5. 反编译：从 ECL 汇编恢复高级对象

### 5.1 Pattern matching 规则

推荐先做规则引擎而非机器学习：

```text
TH13+ BulletEmitter 识别：
  起点：ins_600(id)
  收集直到 ins_601(id) 或函数结束
  中间允许：607/602/603/604/605/606/608/609/610/611/612/617-628/535/548/变量赋值/难度块
  输出 BulletEmitter object

TH12 BulletEmitter 识别：
  起点：ins_500(id)
  收集配置 502/503/504/505/506/507/508 与 transform 509
  将 510 clear-all、511 copy、512 cancel、513 clear 作为独立 manager/system action
  终点：ins_501(id)

TH10/11 BulletEmitter 识别：
  起点：ins_400/401(slot) 或成组 slot 初始化
  收集 402/404/405/406/407/409
  终点：激活 opcode 或 return

TH08 BulletEmitter 识别：
  直接识别 ins_96/97/98/99/100-104 等宏发弹；前置连续 ins_111 作为 transforms。
```

### 5.2 难度块恢复

反编译文本中的：

```text
!E  1.5f;
!N  1.5f;
!H  2.0f;
!LO 3.0f;
!*  ins_605(0, [-1.0f], 1.0f);
```

其中 `!E...!LO` 是各 literal case 的 guard，`!*` 是实际消费占位符的 instruction 或 syntax statement。literal group 直接附着到该 consumer，canonical 层应恢复为：

```yaml
SelectedValue:
  selector: difficulty
  cases:
    - {guard: E, value: 1.5f}
    - {guard: N, value: 1.5f}
    - {guard: H, value: 2.0f}
    - {guard: L, value: 3.0f}
```

`DifficultyGuard` 仍按 `E/N/H/L/X/O/6/7` 八 lane 建模；示例只出现四个 case 不代表 IR 只有四个 lane。原 marker spelling 同时保留，以便 identity rendering。

### 5.3 循环恢复

```text
ins_535($A, 1, 1, 4, 20);
loop:
  ins_601(0);
  ins_23(10);
if ($A--) goto loop
```

恢复为：

```yaml
Loop:
  count: difficulty_interpolate_int(E:1,N:1,H:4,L:20)
  body:
    - emitter.fire(0)
    - wait(10)
```

## 6. 编译：高级对象到目标 ECL

### 6.1 TH15 → TH12 发弹移植示例

源 IR：

```yaml
BulletEmitter:
  id: 0
  appearance: {style: 4, color: 6}
  aim: {mode: aimed_fan, baseAngle: 0, angleStep: 0.05235988}
  count: {ways: 1, layers: 1}
  speed: {first: 2.0, step: 1.0}
  transforms:
    - {action: {type: setAngleSpeed}, raw: {th13ExType: 2, args: [1, null, null]}}
  sound: null
  fire: once
```

TH15/TH13+ backend：

```text
ins_600(0);
ins_607(0, 0);
ins_602(0, 4, 6);
ins_606(0, 1, 1);
ins_604(0, 0.0f, 0.05235988f);
ins_605(0, 2.0f, 1.0f);
ins_611(0, 0, 2, 1, -999999, -999999.0f, -999999.0f);
ins_601(0);
```

TH12 backend 近似：

```text
ins_500(0);                 // etNew
ins_507(0, 0);              // etAim, 若参数同构需按实际 th12 签名适配
ins_502(0, 4, 6);           // etSprite
ins_506(0, 1, 1);           // etCount
ins_504(0, 0.0f, 0.05235988f); // etAngle
ins_505(0, 2.0f, 1.0f);     // etSpeed
ins_509(0, resolvedIndex, channel, mode, ...); // etEx，需唯一静态 index 且 mode 可编码
ins_501(0);                 // etOn
```

注意：上面是语义 lowering 示例，实际参数顺序必须以目标 eclmap/THBWiki 对照表核验。若源是 `611/612` append，而 CFG 或难度 lane 无法证明唯一 `resolvedIndex`，该 transform 必须 unsupported；`511` 是 manager copy，绝不能用于代替 transform。

### 6.2 若目标不支持某 transform

策略示例：

```yaml
loweringPolicy:
  unsupportedTransform: approximate
  complexCurveLaser: error
  missingSound: ignore
  unsupportedGameSystem: stub
```

例如 TH15 的月都/章节/pointdevice 相关 opcode 移植到 TH12，通常应标记为 `GameSpecificEffect` 并默认不编译，除非手写 runtime shim。

## 7. 模块/对象库设计

### 7.1 标准库模块

```text
std.enemy
  createEnemy, createBoss, setHitbox, setHurtbox, setFlags, setDrop, killAll

std.move
  moveTo, moveBy, setVelocity, interpolateVelocity, circle, ellipse, bezier, bossMove

std.bullet
  BulletEmitter, BulletTransform, fireFan, fireRing, fireRandom, cancelBullets, clearBullets

std.laser
  LaserEmitter, straightLaser, curveLaser, warningLaser

std.boss
  BossPattern, Nonspell, SpellCard, Timeout, setLife, setTimer, chapter, spellName

std.timeline
  wait, loop, async, difficulty, rand, rankValue

std.fx
  sound, shake, fog, dialogue, logo, backgroundStd
```

### 7.2 一个跨游戏 DSL 示例

```yaml
function: GirlA01_at
locals: [A]
body:
  - wait: difficulty({E:90, N:90, H:30, L:30})
  - let:
      A: difficultyInt({E:1, N:1, H:4, L:20})
  - object: BulletEmitter
    name: main
    id: 0
    appearance: {style: 4, color: 6}
    aim: {mode: aimed_fan, baseAngle: 0, angleStep: 0.05235988}
    count: {ways: 1, layers: 1}
    speed: {first: difficulty({E:1.5,N:1.5,H:2.0,L:3.0}), step: 1.0}
    transforms:
      - {index: 0, action: {type: changeVelocity, afterFrames: 1}}
  - loop:
      count: A
      body:
        - fire: main
        - wait: difficulty({E:30,N:30,H:20,L:5})
```

### 7.3 编译目标声明

```yaml
target:
  game: th12
  policy:
    unsupported: warn
    resourceMap:
      bulletStyle: th15_to_th12_bullet_style.yaml
      color: common
```

sentinel 不应作为一个全局 `sentinelInt/sentinelFloat` 开关暴露；它由目标 `GameProfile` 再结合 transform mode 和 operand role 编码。

## 8. 指令组合到对象的建议映射表

| 组合 | 高级对象 | 说明 |
| --- | --- | --- |
| `302 → 303/306 → 307` | `AnimationController` | 选择 ANM、设置 slot、播放动画 |
| `500 → 501 → 502/503` | `CollisionProfile/Flags` | hurtbox/hitbox/flag 设置 |
| `400/401/404/405` | `MovementController` | 位置/速度/插值移动 |
| `600 → 607 → 602 → 606 → 604 → 605 → 611* → 601` | `BulletEmitter` | TH13+ 标准发弹对象 |
| `500 → 507 → 502 → 506 → 504 → 505 → 509* → 501` | `BulletEmitter` | TH12 标准发弹对象；`511` 是 manager copy，不是 transform |
| `400/402/404/405/406/407 → 409* → on` | `BulletEmitter + BulletTransform` | TH10/11 弹幕槽对象 |
| `111* → 96/97/98/99` | `BulletEmitter + BulletTransform` | TH08 宏发弹对象 |
| `700 → 701 → 704/705/706/707/708/709 → 702/711` | `LaserEmitter` | TH13+ 激光对象 |
| `600 → 601/602/604...` in TH12 laser range | `LaserEmitter` | TH12 激光对象 |
| `511/512/513/514/521/523/537/538/539` | `BossPattern` | Boss 血量、timer、spell、interrupt |
| instruction/call/async consumer + difficulty literal table | `SelectedValue + DifficultyGuard` | 八 lane 难度参数选择/执行 guard；consumer 拥有 ordered tables |
| `23 + goto + if counter--` | `TimelineLoop` | 时间循环 |

## 9. 可移植性等级

| 语义 | TH08 ↔ TH10/12/13+ | TH10/11 ↔ TH12 | TH12 ↔ TH13+ | 备注 |
| --- | --- | --- | --- | --- |
| 基础 fan/ring 发弹 | 中 | 高 | 高 | 需 style/color 映射 |
| 多层/way/speed/angle | 中 | 高 | 高 | 参数可统一 |
| Bullet transform | 中低 | 中 | 中高 | type 编号和行为不完全一致 |
| 曲线/复杂激光 | 低 | 中低 | 高 | 老游戏可能无等价能力 |
| 基础移动/插值 | 中 | 高 | 高 | mode 编号需映射 |
| Boss spell 流程 | 中 | 中 | 高 | 名称/得分/UI 差异大 |
| 游戏特有系统 | 低 | 低 | 低 | 通常 stub 或重写 |

## 10. 最终设计建议

### 10.1 项目结构

```text
ecl_ir/
  source/              SourceDocument + Program
  canonical/           semantic nodes, lifter, operations, variables
  dialects/            profiles, references, catalogs, ANM data
  analysis/            bullet reducer, CFG, transform/spread analysis
  target/              capability planner + TargetModule renderer
  artifact/            standalone schema + validation
  compat/              text emitter still used by canonical lowering
  legacy/              schema-v1 object projections
  integrations/        optional external integrations
  commands/            CLI implementation
  deprecated/          unreferenced one-off code only
  cli.py               stable command facade
```

### 10.2 编译流程

```text
DECL/ECL 汇编
  ↓ parse
SourceDocument + Program: functions, labels, vars, raw ins
  ↓ DialectDecoder
SemanticModule: ordered canonical nodes + ownership/provenance
  ↓ derived analyses
Bullet state / CFG / target ANM candidate plan / Pattern projections
(reference NodeId only; ANM plan also reads target package evidence)
  ↓ target lowering
LoweringPlanner(GameProfile) -> TargetModule
  ↓ emit
目标游戏 .decl/.ecl
```

当前 `TargetModule` 的 statement payload 仍是字符串 lines；将其替换为 `TargetInstruction/TargetSyntax/TargetComment/TargetUnsupported` typed union 是后续工作，而不是已完成前提。

### 10.3 设计原则

1. **保留 raw 证据，不默认执行 raw**：无法表达的细节保留 source/provenance；同游戏可 identity，跨游戏 RAW 必须显式 opt-in 并带节点 warning。
2. **字段取并集，后端取交集**：IR 字段覆盖所有游戏，编译目标只消化其支持子集。
3. **显式 unsupported**：不可无损移植的字段必须输出 warning/error，而不是静默生成错误弹幕。
4. **资源映射独立**：style/color/anm/script 在不同游戏不等价。ANM 当前使用目标 package-scoped candidate plan；其他资源仍需要独立 `resourceMap`。
5. **参数语义优先于 opcode 编号**：不要做简单编号偏移；应先升格到语义对象再 lowering。
6. **先支持第四代与第三代互转**：TH12 ↔ TH13+ 结构最接近，最适合作 MVP。
7. **TH08/第一世代作为宏后端处理**：它的发弹 opcode 更高层，但可表达字段较少，适合把多个 IR 字段折叠进 `ins_96..99`。
8. **同游戏 identity 独立**：同目标重建应使用 provenance opcode 与 canonical operands，不要把数据送进跨游戏近似规则。
9. **变量与栈槽必须先分类再跨代**：当前实现使用 `VariableRef` + per-game `VariableDialect`，instruction operand、difficulty-selected value 和 syntax expression 共用 `ExpressionIR` 的 typed spans；TH13+ 相对槽位则使用独立 `StackRef` 并由 `RoutineDialect` 判断 ABI。数字相同不代表语义相同，例如 TH16/TH17 的 `-9903` 会得到 `variable.semantic_collision`；目标缺少 BF/GF 等槽位时得到 `variable.target_unavailable`。`INFERRED` 变量只允许同游戏 identity，不开放跨游戏 direct。完整的 literal/unary/binary/cast/call expression AST 仍需继续实现，但 typed relative-stack span 已经落地。
10. **资源 ID 必须有 typed context**：当前 `AnmCandidatePool`、`AnmCombinationCandidate`、`AnmCandidateSelection` 和 `AnmCallSiteMaterialization` 只提供目标 package 内可用组合及其 evidence；文件名、函数名和相同数字都不能作为运行时等价证明。下一步仍需让 bank/script/current-bank 进入 `AnmResourceRef` 与 CFG/difficulty-aware ordered analysis。

## 11. 阶段范围

以下是早期 MVP 建议，当前 canonical pipeline、bullet reducer、transform registry、八 lane difficulty 和 CFG cycle analysis 已经超过该范围：

- 解析 `.decl` 函数、label、变量、`ins_N`、难度块。
- Lifter 支持：
  - TH13+ `BulletEmitter`
  - TH12 `BulletEmitter`
  - TH13+/TH12 `Movement`
  - TH13+ `LaserEmitter`
- Backend 支持：
  - TH13+ → TH12 的基础 fan/ring 发弹。
  - TH12 → TH13+ 的基础 fan/ring 发弹。
- 报告所有 unsupported transforms/laser/game-specific opcodes。

下一阶段重点不是继续增加逐游戏替换表，而是完成统一 `OperationSchema`、typed target statement union、完整 expression node union、CFG state join，并在现有 ANM package candidate plan 上补齐 `AnmResourceRef`、逐 difficulty lane bank-flow 和运行时等价验证，以及 laser/movement 等 canonical analyses。TH10/11 与 TH08 的新增 lowering 只有在变量/资源语义和 operand predicate 可证明时才应开放。

最终验证基线：210 个源文件同目标 render/reparse 覆盖 251,710 个 canonical 节点，instruction/syntax/SelectedValue/timeline region 请求字段 mismatch 均为 0，且没有 unsupported/lossy。210×12 strict matrix 共处理 3,020,520 个节点和 2,520 次 build，无异常、无 lossy；1,233,676 个不可证明节点全部保留为 structured unsupported。

## 12. 结语

把 ECL 当作“多平台汇编”是合理的：每个游戏/世代是一个 ISA，弹幕、移动、激光、Boss 是高级语义。真正可维护的移植器应采用“源方言 → ordered canonical IR → 派生 analyses → capability lowering”的方式，而不是维护大量 opcode-to-opcode 替换表。对于发弹逻辑，`BulletEmitter + BulletTransform + TimelineLoop + DifficultyGuard + SelectedValue` 能覆盖大量可移植语义；ANM 已有目标 package 候选池和调用点物化基础，变量也已进入 typed dialect，但激光、Boss、完整资源流和游戏系统仍需要更完整的能力矩阵、CFG/difficulty analysis 和运行时验证。
