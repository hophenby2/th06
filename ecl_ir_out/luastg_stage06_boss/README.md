# TH12 stage06 Boss ECL → LuaSTG 复刻草案

## 产物

- `ecl_stage06_boss.lua`：由 `th062/th12/stage06.decl` 的 boss 相关 sub 生成的 LuaSTG 模块。
- 生成命令：

```sh
python3 -m th062.ecl_ir.cli luastg th062/th12/stage06.decl \
  --output th062/ecl_ir_out/luastg_stage06_boss/ecl_stage06_boss.lua \
  --module-name ecl_stage06_boss
```

## LuaSTG 侧依赖

该模块假定已经处于 `144th_weekend_liu_10_mc.lua` 的运行环境中，依赖以下全局对象/库：

- `task.New` / `task._Wait`：对应 ECL 的异步 sub 和 `ins_83` 等待。
- `boss.card.New` 创建的 card/self：作为 ECL boss sub 的 `self`。
- `liu_10_mc.bullet.ShotBulletMode`：作为 ECL bullet emitter 的主要后端。
- `_editor_class` / `Class(bullet)` / `bullet.init`：合成 ECL bullet style/color 对应的 LuaSTG bullet class。
- `_editor_tasks["liu_10_mc_moveRand"]`：近似映射 TH12 的随机移动。

## ECL 到 LuaSTG 的主要对应

| ECL 语义 | TH12 opcode | LuaSTG 复刻方式 |
| --- | --- | --- |
| 等待 | `ins_83(n)` | `task._Wait(n)` |
| 同步调用 | `@Sub()` | `ecl_Sub(self, ...)` |
| 异步调用 | `@Sub() async` | `task.New(self, function() ecl_Sub(self, ...) end)` |
| 直接设坐标 | `ins_300/400(x,y)` | `self.x,self.y=x,y` 并同步 `[-9997]/[-9996]` |
| 时间移动 | `ins_301/401(t,mode,x,y)` | `task.MoveTo(x,y,t,mode)` |
| 速度方向 | `ins_304/404(angle,speed)` | `SetV2(self, speed, ecl_rad(angle), true, false)` |
| 圆周坐标 | `ins_81(outX,outY,ang,r)` | `math.cos/sin` 弧度计算 |
| boss HP | `ins_411(hp)` | `self.hp,self.maxhp=hp,hp` |
| boss/card 元信息 | `ins_413/414/423/424/427/437...` | 暂以注释保留，部分可手工接入 `boss.card.New` |
| 弹幕 emitter 新建 | `ins_500` | 维护 `EmitterState` |
| 弹型/颜色 | `ins_502` | 合成 `_editor_class["...Bullet_style_color"]` |
| 发弹角 | `ins_504` | 转为 LuaSTG 角度制 `ecl_rad` |
| 速度 | `ins_505` | `ShotBulletMode` 的 `spd1/spd2` |
| 数量/层数 | `ins_506` | `ShotBulletMode` 的 `way/layer` |
| 难度速度表 | `ins_521` | `ecl_pick_rank(E,N,H,L)` 选择 `speed/speed_step` |
| 难度数量表 | `ins_522` | `ecl_pick_rank(E,N,H,L)` 选择 `way/layer` |
| 发弹基准点 | `ins_503/525` | `dx/dy` 或绝对点减 `self.x/y` |
| 发弹距离 | `ins_524` | `ShotBulletMode` 的 `dis` |
| 实际发弹 | `ins_501` | `liu_10_mc.bullet.ShotBulletMode(...)` |

## 已实现的结构化降级

- 识别 boss 相关函数：`Boss`、`Boss1..Boss6`、`BossCard*`、`Boss*_at*`、`BossEyes*`、`HPWait`。
- 常见 ECL 控制流：
  - `goto End; LabelBody: ... End: if ($D--) goto LabelBody` 降为 `for`。
  - `goto End; LabelBody: ... End: if (1) goto LabelBody` 降为 `while true`，无等待时补 `task._Wait(1)` 防止卡死。
- 难度选择：优先读取 `_G.difficulty`，其次读取 `lstg.var.difficulty/lstg.var.rank`，默认 Normal。
- ECL 坐标变量：函数入口与移动后同步 `ecl_var[-9997] = self.x`、`ecl_var[-9996] = self.y`。

## 当前限制

- 激光 `ins_600..611` 仍只保留注释，下一步应封装为 `LaserEmitter` 再映射到 `liu_10_mc.bullet.LineLaser/InfLaser/CurvedLaser`。
- `ins_509` 变换参数目前以表传入 bullet class，但未完整复刻 ECL 的加速度、延迟、变形、边界行为。
- boss 符卡声明、SCB、计时、对话、转阶段中断仅保留注释；要完整接入需从 `ins_414/437/438/439/522` 提取 card 元信息生成 `boss.card.New` 包装。
- 条件分支只重建了最常见循环；复杂 `unless/if` 跳转仍以注释保留。
- ANM/resource 没有自动移植，bullet style/color 只生成近似 class。

## 推荐接入方式

在 `144th_weekend_liu_10_mc.lua` 的某个 boss card `init()` 中加载模块，然后把 card/self 交给生成函数：

```lua
local ecl_stage06_boss = require("ecl_stage06_boss")
function _tmp_sc:init()
    task.New(self, function()
        ecl_stage06_boss.Boss(self)
    end)
end
```

也可以只调用单个符卡或攻击函数：

```lua
task.New(self, function() ecl_stage06_boss.BossCard1(self) end)
task.New(self, function() ecl_stage06_boss.Boss1_at1(self) end)
```

## 验证

已执行：

```sh
python3 -m py_compile th062/ecl_ir/luastg_backend.py th062/ecl_ir/cli.py
python3 -m th062.ecl_ir.cli luastg th062/th12/stage06.decl --output th062/ecl_ir_out/luastg_stage06_boss/ecl_stage06_boss.lua --module-name ecl_stage06_boss
lua -e 'assert(loadfile("th062/ecl_ir_out/luastg_stage06_boss/ecl_stage06_boss.lua"))'
```

结果：生成脚本通过 Lua 语法解析。
