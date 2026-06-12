# LuaSTG/THlib → 语义 IR 的可行方案

## 设计原则

目标不是反编译任意 Lua，而是把常见 LuaSTG 弹幕写法提升成和 ECL 转换共用的语义对象：

```text
LuaSTG source → Lua AST/模式识别 → 语义 IR → ECL/其他 LuaSTG 后端
```

要避免“一对一翻译 Lua 调用”，应把 LuaSTG 中的低级 API 归并成跨平台对象：

- `BulletEmitter`
- `LaserEmitter`
- `Movement`
- `Timeline/Task`
- `BossPattern/Card`
- `EffectEmitter`

## 已实现原型

新增：`th062/ecl_ir/luastg_lifter.py`

CLI：

```sh
python3 -m th062.ecl_ir.cli luastg-lift path/to/script.lua --output out.json
```

当前识别：

| LuaSTG 模式 | 提升对象 | 备注 |
| --- | --- | --- |
| `ecl_shot(...)` | `BulletEmitter` | 生成后端专用 helper，可无损回收大部分参数 |
| `_create_bullet_group(...)` | `BulletEmitter` | THlib editor 公共发弹 API |
| `New(_straight, ...)` | `Bullet` | 单发直线弹 |
| `task._Wait(n)` / `task.Wait(n)` | `Wait` | timeline 基础节点 |
| `task.MoveTo(x,y,t,mode)` | `Movement` | 坐标移动 |
| `SetV2(obj,v,ang,...)` | `Movement` | 速度移动 |
| `boss.card.New(...)` | `BossPattern` | card 元信息 |

## 关键语义归并

### BulletEmitter

统一字段建议：

```json
{
  "kind": "BulletEmitter",
  "shape": "style/imgclass",
  "color": "index/color",
  "origin": {"x": "...", "y": "...", "dx": "...", "dy": "..."},
  "aim": "absolute|player|ring|player_ring|random",
  "count": {"ways": "...", "layers": "..."},
  "speed": {"base": "...", "step": "..."},
  "angle": {"base": "...", "step": "...", "unit": "degree"},
  "delay": "...",
  "transforms": []
}
```

LuaSTG 的 `_create_bullet_group(style,color,x,y,n,t,v1,v2,angle,da,aim,...)` 可以直接映射到：

- `shape=style`
- `color=color`
- `ways=n`
- `interval=t`
- `speed.base=v1`
- `speed.step=v2-v1`
- `angle.base=angle`
- `angle.spread=da`
- `aim=player` when `aim=true`

生成器产出的 `ecl_shot(...)` 则更接近 ECL emitter，可以保留：

- `mode`
- `emitter id`
- `way/layer`
- `speed/speed_step`
- `angle/angle_step`
- `extra transforms`

### Timeline/Task

`task.New(self,function() ... end)` 应提升为一个 `Timeline` 子图：

- 顺序语句保持顺序。
- `task._Wait(n)` 变成 `Wait(n)`。
- `for`/`while` 变成 `Loop(count|infinite)`。
- `task.New` 内嵌任务变成 `AsyncCall` 或 `ParallelTimeline`。

如果只用正则无法安全处理嵌套 function，下一步应接入 Lua parser（例如 tree-sitter-lua 或 Metalua 风格 AST），以 AST block 为单位识别。

### Movement

公共归并：

- `task.MoveTo(x,y,t,mode)` → `MoveTo`。
- `SetV2(obj,v,ang,...)` → `SetVelocityPolar`。
- `self.x/self.y = ...` → `SetPosition`。
- 圆周运动若出现 `cos/sin` 同角同半径模式，提升为 `CircularOffset`。

### LaserEmitter

LuaSTG 公共库可识别：

- `New(laser,index,x,y,rot,l1,l2,l3,w,node,head)` → `LaserEmitter(type="line")`
- `laser_bent` / `laser_bent_death_ef` → `LaserEmitter(type="curved")`

与 ECL `ins_600..611` 对齐时建议字段：

```json
{
  "kind": "LaserEmitter",
  "type": "line|infinite|curved",
  "style": "...",
  "origin": {"x":"...","y":"..."},
  "angle": "...",
  "length": {"head":"l1","body":"l2","tail":"l3"},
  "width": "...",
  "timing": {"warmup":"...","active":"...","fade":"..."}
}
```

## 可落地流水线

1. **LuaSTG Lift**：`luastg_lifter.py` 读取 Lua，输出 JSON 语义对象。
2. **Normalize**：把 `_create_bullet_group`、`ecl_shot`、`New(_straight)` 统一成标准 `BulletEmitter` schema。
3. **Timeline Build**：根据 function/card 归组，重建 `Wait/Loop/Async`。
4. **Backend Compile**：复用现有 ECL backend，把标准对象编译到 TH08/TH10/TH12/TH15 或 LuaSTG。
5. **Round-trip Test**：ECL→LuaSTG(thlib)→IR，比较 `BulletEmitter/Movement/Wait` 数量和关键参数。

## 当前边界

- 正则原型不能完整解析 Lua 语义，复杂局部变量、闭包、表驱动参数需要 AST。
- 任意 Lua 表达式暂作为字符串表达式保存，不做求值。
- 资源名、图片 style 与 ECL style 的对应仍需资源映射表。
- LuaSTG 中自定义 bullet class 的 `frame()` 行为需要额外模式库或人工标注。

## 本轮新增实现

### 标准化层

新增 `th062/ecl_ir/luastg_normalizer.py`，把 `luastg_lifter.py` 的轻量对象转换为现有工程共用对象：

- `LuaSTGIRObject(kind="BulletEmitter")` → `model.BulletEmitter`
- `LuaSTGIRObject(kind="Movement")` → `model.MovementOp`
- `LuaSTGIRObject(kind="Wait")` → `model.TimelineOp`
- `LuaSTGIRObject(kind="LaserEmitter")` → `model.LaserEmitter`

新增 CLI：

```sh
python3 -m th062.ecl_ir.cli luastg-normalize script.lua --output normalized.json
python3 -m th062.ecl_ir.cli luastg-compile script.lua --target th12 --kind BulletEmitter --limit 5
python3 -m th062.ecl_ir.cli luastg-compile script.lua --target th12 --kind LaserEmitter --limit 5
```

### Round-trip 路径

目前可执行的闭环：

```text
TH12 ECL stage06.decl
  → luastg --runtime thlib
  → ecl_stage06_boss_thlib.lua
  → luastg-lift
  → luastg-normalize
  → luastg-compile --target th12
```

在 `ecl_stage06_boss_thlib.lua` 上当前识别统计：

- `BulletEmitter`: 71
- `Movement`: 47
- `LaserEmitter`: 13
- `Wait/Timeline`: 89

### 激光路径

THlib Lua 生成端新增：

```lua
ecl_laser(style, x, y, angle, length, width, warn_time, fade_in, active_time, fade_out, kind)
```

当前 LuaSTG → IR 识别：

- `ecl_laser(...)` → `LaserEmitter`
- `New(laser, style, x, y, angle, l1, l2, l3, width, node, head)` → `LaserEmitter`

当前 IR → TH12 ECL 编译草案：

```decl
ins_600(id, 0.0f, length, 0.0f, width);
ins_601(id, warn, fade_in, active, fade_out, 0);
ins_608(id, angle);
ins_602(id); // line
ins_611(id); // curve
```

注意：`ecl_laser` 的 THlib 运行行为仍是近似，主要用于语义占位与 round-trip，不是完整复刻 ECL 激光碰撞/预警线状态机。

## 本轮继续完善

### Timeline/Wait

`luastg-normalize` 现在把 `task._Wait(n)` / `task.Wait(n)` 标准化为 `TimelineOp(family="wait")`，`luastg-compile --target th12 --kind Timeline` 会输出：

```decl
ins_83(n);
```

这使 LuaSTG→ECL 草案不再只包含发弹对象，也能保留基础时序。

### Movement

`task.MoveTo(x,y,time,mode)` 已标准化为：

```json
{"op_key":"movement.position.tween", "args":[time, mode, x, y]}
```

编译到 TH12 时输出：

```decl
ins_301(time, mode, x, y);
```

`SetV2(self, speed, angle, ...)` 已标准化为：

```json
{"op_key":"movement.velocity.set", "args":[angle_rad, speed]}
```

编译到 TH12 时输出：

```decl
ins_304(angle_rad, speed);
```

### 角度单位规则

- ECL 原始角度是弧度。
- LuaSTG/THlib `SetV2`、`Angle`、`cos/sin` 使用角度制。
- ECL→LuaSTG 生成时用 `ecl_rad(x) = x * 180 / math.pi`。
- LuaSTG→ECL 标准化时：
  - `ecl_shot(ecl_rad(x))` 会还原为 `x`。
  - 普通 LuaSTG 度数表达式会转为 `(expr * 0.017453292519943295)`。

### 多 kind 编译

`luastg-compile` 现在支持多个 kind 或 `all`：

```sh
python3 -m th062.ecl_ir.cli luastg-compile script.lua --target th12 --kind all --output out.decl
python3 -m th062.ecl_ir.cli luastg-compile script.lua --target th12 --kind Timeline,Movement,BulletEmitter,LaserEmitter --output out.decl
```

当前 `all` 的输出顺序仍按 Lua 源文件扫描顺序，不等价于完整结构化 sub；下一步应按函数重建 `sub`/`task.New` 嵌套结构。

## 本轮新增：LuaSTG → 语义 IR → 函数分组 ECL 导出

新增 `luastg-export` 命令，用于把 LuaSTG/THlib 脚本先提升为共享语义对象，再按 Lua 函数重新导出为目标游戏 ECL 函数草案，而不是原来的平铺对象列表。

示例：

```bash
python3 -m th062.ecl_ir.cli luastg-export \
  th062/ecl_ir_out/luastg_stage06_boss_thlib/ecl_stage06_boss_thlib.lua \
  --target th12 --kind all \
  --output th062/ecl_ir_out/luastg_roundtrip/stage06_boss_thlib_to_th12_grouped.decl
```

实现要点：

- `ecl_shot` / `_create_bullet_group` 在 normalizer 中标记为 `bullet.fire_at_definition`，后端按目标代自动追加 `ins_501` / `ins_601` 等发射指令。
- `luastg-export` 按 `obj.function` 分组，过滤 `ecl_shot`、`ecl_laser`、`ecl_pick_rank` 等运行时 helper 函数，输出 `void ecl_xxx(...) { ... }`。
- LuaSTG 生成器产生的 `v_A/i_A/ecl_var[-9997]` 表达式会在 normalizer 中反解回 `%A/$A/[-9997.0f]`，函数参数也从 Lua 函数签名恢复为 `var A` 等 ECL 参数。
- TH12 后端新增轻量类型规范化：浮点角度/除法表达式补 `_f(...)` 和 `f` 后缀；整数槽位把 `[-9985.0f]` 规范化为 `[-9985]`，同时保留 difficulty dict 以生成 `ins_521/ins_522`。

当前验证：

```bash
wine thtkGUI-th20tr/thtk/thtk12/thecl.exe -c 12 \
  th062/ecl_ir_out/luastg_roundtrip/stage06_boss_thlib_to_th12_grouped.decl \
  /tmp/luastg_roundtrip_stage06.ecl
```

上述命令已通过，生成 `/tmp/luastg_roundtrip_stage06.ecl`。这说明当前 TH12 目标语法/参数表已能接受该函数分组草案；但控制流仍是语义对象近似重建，Lua 循环/赋值未完整反编译回 ECL timeline，因此还不能宣称与原版 boss 流程完全等价。
