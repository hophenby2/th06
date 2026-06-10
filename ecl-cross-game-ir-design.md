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

### 2.2 时间结构

跨游戏常见：

- `wait(t)`：第四世代 `ins_23` 极高频；第一世代/TH08 以时间标签 `+N`、`ins_2/ins_105/ins_106` 等表达等待。
- `goto label @ time` + `if counter-- goto`：所有世代都存在循环结构。
- 难度块：`!E !N !H !L/!LO !*` 在反编译脚本中作为条件覆盖参数。应抽象为 `DifficultyValue<T>`。
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
509 etExSet
510 etExSet2
511 etEx
512 etEx2
513 etClearAll
514 etCopy
515 etCancel
516 etClear
...
```

组合与 TH13+ 基本同构，但编号整体少 100，参数顺序/细节可能不同。

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
    easy: partial BulletEmitter
    normal: partial BulletEmitter
    hard: partial BulletEmitter
    lunatic: partial BulletEmitter
```

`null`/缺省表示“不使用”；编译到旧游戏时不可支持字段应进入 lowering 策略：忽略、近似、展开成多个 emitter、或报错。

### 3.3 BulletTransform 并集

```yaml
BulletTransform:
  index: int
  channel: int = 0
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
- TH12 `ins_509/510/511/512` → `BulletTransform`。
- TH13+ `ins_609/610/611/612` → `BulletTransform`。

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

建议设计一个跨游戏 DSL/IR，分三层：

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

### 4.2 Object IR 层：把 opcode 组合提升为对象

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

### 4.3 Backend lowering 层：按目标游戏生成 opcode

每个目标游戏一个 backend：

```text
BackendTH08
BackendTH10
BackendTH12
BackendTH13Plus
```

职责：

1. 选择 opcode 族。
2. 把对象字段降到目标支持的 opcode 参数。
3. 处理缺省值与 sentinel：第四世代常用 `-999999` / `-999999.0f` 表示“不变/未用”；旧作可能用 `-1` 或根本无字段。
4. 对不支持字段进行策略处理：
   - `ignore`: 忽略非关键视觉字段。
   - `approximate`: 近似，例如把复杂 transform 展开为多个简单变换。
   - `expand`: 展开成多个 emitter/subtask。
   - `error`: 无法正确移植时报错。

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
  收集 502/503/504/505/506/507/508/509/510/511/512
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

应恢复为：

```yaml
speed.first: DifficultyValue({E:1.5,N:1.5,H:2.0,L:3.0})
```

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
ins_511(...);               // etEx, 若 type 支持
ins_501(0);                 // etOn
```

注意：上面是语义 lowering 示例，实际参数顺序必须以目标 eclmap/THBWiki 对照表核验。

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
  backend: th12
  policy:
    unsupported: warn
    sentinelInt: -999999
    sentinelFloat: -999999.0
    resourceMap:
      bulletStyle: th15_to_th12_bullet_style.yaml
      color: common
```

## 8. 指令组合到对象的建议映射表

| 组合 | 高级对象 | 说明 |
| --- | --- | --- |
| `302 → 303/306 → 307` | `AnimationController` | 选择 ANM、设置 slot、播放动画 |
| `500 → 501 → 502/503` | `CollisionProfile/Flags` | hurtbox/hitbox/flag 设置 |
| `400/401/404/405` | `MovementController` | 位置/速度/插值移动 |
| `600 → 607 → 602 → 606 → 604 → 605 → 611* → 601` | `BulletEmitter` | TH13+ 标准发弹对象 |
| `500 → 507 → 502 → 506 → 504 → 505 → 509/511* → 501` | `BulletEmitter` | TH12 标准发弹对象 |
| `400/402/404/405/406/407 → 409* → on` | `BulletEmitter + BulletTransform` | TH10/11 弹幕槽对象 |
| `111* → 96/97/98/99` | `BulletEmitter + BulletTransform` | TH08 宏发弹对象 |
| `700 → 701 → 704/705/706/707/708/709 → 702/711` | `LaserEmitter` | TH13+ 激光对象 |
| `600 → 601/602/604...` in TH12 laser range | `LaserEmitter` | TH12 激光对象 |
| `511/512/513/514/521/523/537/538/539` | `BossPattern` | Boss 血量、timer、spell、interrupt |
| `535/536/548 + !E/!N/!H/!L` | `DifficultyValue` | 难度参数选择/插值 |
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
ecl-ir/
  schema/
    program.schema.yaml
    bullet.schema.yaml
    laser.schema.yaml
    boss.schema.yaml
  frontends/
    decl_parser.py
    pattern_lifter.py
  backends/
    th08_backend.py
    th10_backend.py
    th12_backend.py
    th13plus_backend.py
  maps/
    opcode_map.yaml
    bullet_style_map.yaml
    color_map.yaml
    transform_map.yaml
    movement_mode_map.yaml
  stdlib/
    bullet.yaml
    laser.yaml
    boss.yaml
  reports/
    unsupported.md
```

### 10.2 编译流程

```text
DECL/ECL 汇编
  ↓ parse
AST: functions, labels, vars, raw ins
  ↓ pattern lifting
Object IR: BulletEmitter/LaserEmitter/BossPattern/Movement...
  ↓ normalization
Canonical IR: 难度值、循环、资源、表达式统一
  ↓ target lowering
Target ECL AST
  ↓ emit
目标游戏 .decl/.ecl
```

### 10.3 设计原则

1. **保留 raw escape hatch**：每个对象都允许 `rawInsBefore/rawInsAfter/rawArgs`，避免无法表达的游戏特有细节丢失。
2. **字段取并集，后端取交集**：IR 字段覆盖所有游戏，编译目标只消化其支持子集。
3. **显式 unsupported**：不可无损移植的字段必须输出 warning/error，而不是静默生成错误弹幕。
4. **资源映射独立**：style/color/anm/script 在不同游戏不等价，必须有 `resourceMap`。
5. **参数语义优先于 opcode 编号**：不要做简单编号偏移；应先升格到语义对象再 lowering。
6. **先支持第四代与第三代互转**：TH12 ↔ TH13+ 结构最接近，最适合作 MVP。
7. **TH08/第一世代作为宏后端处理**：它的发弹 opcode 更高层，但可表达字段较少，适合把多个 IR 字段折叠进 `ins_96..99`。

## 11. MVP 范围

建议第一阶段只做：

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

第二阶段再扩展 TH10/11 与 TH08。

## 12. 结语

把 ECL 当作“多平台汇编”是合理的：每个游戏/世代是一个 ISA，弹幕、移动、激光、Boss 是高级语义。真正可维护的移植器应采用“反编译到对象 IR → 目标后端编译”的方式，而不是维护大量 opcode-to-opcode 替换表。对于发弹逻辑，`BulletEmitter + BulletTransform + TimelineLoop + DifficultyValue` 足以覆盖大多数可移植语义；对于激光、Boss、游戏系统，需要明确能力矩阵和降级策略。
