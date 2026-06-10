# TH08 东方永夜抄 ECL 速查

> 根据 `th062/ecl-web.txt` 中列出的 Priw8 ECL 指令表、变量表、flags/MERLIN 文档，以及本地提供的 THBWiki 文本 `th062/ecl*.txt` 整理。具体 opcode/变量主表以 Priw8 源数据为准，THBWiki 中文说明作为代际补充与交叉索引。

## 阅读说明

- `ID` 为 ECL opcode 或变量编号；`助记名` 来自 priw8 的 eclmap。
- `参数` 中前半为格式串，括号内为参数名；`S/$` 常见为整数，`f/%` 常见为浮点，`o` 常见为跳转 offset/label。
- `来源` 表示该条在 Priw8 继承链中的定义来源；第四世代大量指令会从 TH13 继承。
- 变量表只列有记录的变量；范围内未列出的编号通常为空洞或未调查。

- 返回总表：`../ecl-reference-by-game.md`
- 本文包含：TH08 对应世代 THBWiki 中文代码表、全局 flags/常量、该游戏 Priw8 指令/变量主表。

## 本游戏概览

| 游戏 | 作品 | 代际/体系 | 指令表覆盖 | 变量表覆盖 | 摘要 |
| --- | --- | --- | --- | --- | --- |
| TH08 | 东方永夜抄 | 第一世代 | 有 | 有 | 普通指令 185 条，时间轴指令 17 条；已说明 171/202。主要分组：普通指令 / Normal。 变量范围 10000..10100；本文列出有说明/命名记录的 100 条，未列空洞/未知项。 |

## THBWiki 中文代际补充

这些表保留 THBWiki 中文页面中的签名和说明，便于和 Priw8 分游戏 opcode 表互查；同一 opcode 的英文精确定义仍见各游戏主表。

### THBWiki 第一世代 ECL

- 适用范围：红魔乡、妖妖梦、永夜抄、花映塚、文花帖；其中妖妖梦/永夜抄/花映塚/文花帖存在新增差异。
- 页面概述：本对照表是Zun的第一代ecl脚本的对照表,适用于红妖永花,文花帖 妖妖梦妖妖梦单独的ecl脚本表 粉色代表妖妖梦新增 深紫色代表永夜抄新增 绿色代表花映塚新增 棕色代表文花帖新增 红色代表功能未知，需要测试和研究 蓝色代表虽然并未完全解读，但是大体功能已经知道，且此函数用途十分有限 灰色代表是前作特殊地点使用过之后完全被抛弃的 注：永夜抄中单关脚本和符卡练习脚本是分开的
- 抽取 opcode：12 条。

| ID | THBWiki 参数签名 | 章节 | 中文说明摘要 |
| --- | --- | --- | --- |
| 10 | ? | 通用 | 参数不明，最后一个float与循环次数相关 |
| 52 | int a | 通用 | 调用ID为a的函数（子例程） 如ins_52(9961)即为调用反编译后名为sub_9961的函数 注意：子例程ID与函数名无关 |
| 53 | — | 通用 | 返回调用函数 |
| 96 | int style, int color, int way, int layer, float minspeed, float maxspeed, float angle, float angle_dif, int flags | 弹幕系 | 立即发射自机狙开扇弹，style为子弹类型，color为颜色，way和layer的定义与后续世代的脚本一致，minspeed和maxspeed分别为最小速度和最大速度，angle为发射角度（实际角度为angle+发弹点与自机的夹角），angle_dif为每层角度差，flags为子弹flag |
| 97 | int style, int color, int way, int layer, float minspeed, float maxspeed, float angle, float angle_dif, int trans_flags | 子弹类型列表 | 同96，但不是自机狙，角度变为angle |
| 111 | int index, int type, int channel, int a, int b, float x, float y | 子弹类型列表 | 为弹幕设置变换，index为变换序号，type为变换类型，channel为通道，a、b、x、y为变换参数，其余未知 |
| 80 | int a | 单位系 | 设置当前单位flag |
| 124 | int a | 单位系 | 播放ID为a的音效 |
| 155 | int a | 单位系 | 设置当前符卡是否为时符 |
| 173 | int a | 单位系 | 设置boss是否对bomb免疫 |
| 176 | int a | 特殊系 | 永夜抄中用于设置当前模式是否为Last Spell |
| 179 | int a | 特殊系 | 永夜抄中用于控制时间的显示，如“子时一刻” a为1时则显示 |

## 敌机 Flags 速查

### TH13-TH17/第四世代常用 Flags（MERLIN 常量）

| Bit | 十进制 | MERLIN 常量 | 效果 |
| --- | --- | --- | --- |
| 0 | 1 | FLAG_NO_HURTBOX | 禁用 hurtbox，不能被自机子弹击中。 |
| 1 | 2 | FLAG_NO_HITBOX | 禁用 hitbox，不能通过撞击击杀玩家。 |
| 2 | 4 | FLAG_OFFSCREEN_LR | 离开屏幕左右边界时不删除敌机。 |
| 3 | 8 | FLAG_OFFSCREEN_UD | 离开屏幕上下边界时不删除敌机。 |
| 4 | 16 | FLAG_INVINCIBLE | 敌机无敌；若为 Boss，会隐藏血条。 |
| 5 | 32 | FLAG_INTANGIBLE | 无形：同时具备 bit0/bit1 效果，并防止被部分清敌 opcode 删除。 |
| 6 | 64 | — | 未知效果。 |
| 7 | 128 | FLAG_NO_DELETE | 防止被 518/525 等清敌 opcode 删除。 |
| 8 | 256 | FLAG_ALWAYS_DELETE | 保证会被 518/525 删除，无视其他 flag。 |
| 9 | 512 | FLAG_GRAZE | 敌机可擦弹，类似激光的连续擦弹。 |
| 10 | 1024 | FLAG_ONLY_DIALOG_DELETE | 防止被 525 删除，但对话出现时死亡。 |
| 11 | 2048 | FLAG_ETCLEAR_DIE | 被 615 等清弹类处理杀死。 |
| 12 | 4096 | FLAG_RECT_HITBOX | 敌机碰撞盒改为矩形而非椭圆。 |
| 13 | 8192 | FLAG_NO_TIMESTOP | TH14.3 中不受 547 影响；其他作品未知/无效果。 |

补充常量：`FLAG_NO_COLLISION = FLAG_NO_HURTBOX | FLAG_NO_HITBOX`；`FLAG_OFFSCREEN_UDLR = FLAG_OFFSCREEN_LR | FLAG_OFFSCREEN_UD`。

### TH08 Flags

| Bit | 十进制 | 效果 |
| --- | --- | --- |
| 0 | 1 | 禁用 hurtbox，不能被自机子弹击中。 |
| 1 | 2 | 禁用 hitbox，不能通过撞击击杀玩家。 |
| 2 | 4 | 无敌/不受伤害。 |
| 3 | 8 | 敌机不可见，且 hitbox/hurtbox 都禁用。 |
| 4 | 16 | 敌机离开屏幕也不删除。 |
| 5 | 32 | 类似或等同于十进制 4，差异未知。 |

## TH08 东方永夜抄

- 体系：第一世代
- 指令：普通指令 185 条，时间轴指令 17 条；已说明 171/202。主要分组：普通指令 / Normal。
- 变量：变量范围 10000..10100；本文列出有说明/命名记录的 100 条，未列空洞/未知项。

### TH08 指令：普通指令 / Normal

| ID | 助记名 | 参数 | 说明 | 文档化 | 来源 |
| --- | --- | --- | --- | --- | --- |
| 0 | nop | — | Does nothing. | 是 | 本作 |
| 1 | delete | — | Immediately deletes the caller. | 是 | 本作 |
| 2 | wait | S (t) | Stops sub execution time for %1 frames. | 是 | 本作 |
| 3 | nop3 | S (A) | Does nothing. Parameter %1 is not even accessed by the game. | 是 | 本作 |
| 4 | jmp | So (t, target) | Unconditionally jumps to label %1 and sets time to %2. | 是 | 本作 |
| 5 | loop | SoS (t, target, &var) | If (%3 != 0), jumps to label %2, sets time to %1 and decrements %3 by 1. | 是 | 本作 |
| 6 | iset | SS (&var, val) | Sets %1 to %2. | 是 | 本作 |
| 7 | fset | ff (&var, val) | Sets %1 to %2. | 是 | 本作 |
| 8 | iset_rand_sign | SS (&var, val) | Sets %1 to either %2 or -%2 at random. | 是 | 本作 |
| 9 | fset_rand_sign | ff (&var, val) | Sets %1 to either %2 or -%2 at random. | 是 | 本作 |
| 10 | iadd | SS (&var, val) | Adds %2 to %1. | 是 | 本作 |
| 11 | isub | SS (&var, val) | Subtracts %2 from %1. | 是 | 本作 |
| 12 | imul | SS (&var, val) | Multiplies %1 by %2. | 是 | 本作 |
| 13 | idiv | SS (&var, val) | Divides %1 by %2. | 是 | 本作 |
| 14 | imod | SS (&var, val) | %1 = %1 % %2 (modulo) | 是 | 本作 |
| 15 | fadd | ff (&var, val) | Adds %2 to %1. | 是 | 本作 |
| 16 | fsub | ff (&var, val) | Subtracts %2 from %1. | 是 | 本作 |
| 17 | fmul | ff (&var, val) | Multiplies %1 by %2. | 是 | 本作 |
| 18 | fdiv | ff (&var, val) | Divides %1 by %2. | 是 | 本作 |
| 19 | fmod | ff (&var, val) | %1 = %1 % %2 (modulo) | 是 | 本作 |
| 20 | iset_add | SSS (&var, val1, val2) | Sets %1 to (%2 + %3). | 是 | 本作 |
| 21 | iset_sub | SSS (&var, val1, val2) | Sets %1 to (%2 - %3). | 是 | 本作 |
| 22 | iset_mul | SSS (&var, val1, val2) | Sets %1 to (%2 * %3). | 是 | 本作 |
| 23 | iset_div | SSS (&var, val1, val2) | Sets %1 to (%2 / %3). | 是 | 本作 |
| 24 | iset_mod | SSS (&var, val1, val2) | Sets %1 to (%2 % %3). | 是 | 本作 |
| 25 | fset_add | fff (&var, val1, val2) | Sets %1 to (%2 + %3). | 是 | 本作 |
| 26 | fset_sub | fff (&var, val1, val2) | Sets %1 to (%2 - %3). | 是 | 本作 |
| 27 | fset_mul | fff (&var, val1, val2) | Sets %1 to (%2 * %3). | 是 | 本作 |
| 28 | fset_div | fff (&var, val1, val2) | Sets %1 to (%2 / %3). | 是 | 本作 |
| 29 | fset_mod | fff (&var, val1, val2) | Sets %1 to (%2 % %3) | 是 | 本作 |
| 30 | inc | S (&var) | Increments %1 by 1. | 是 | 本作 |
| 31 | dec | S (&var) | Decrements %1 by 1. | 是 | 本作 |
| 32 | fset_sin | ff (&var, val) | Sets %1 to sin(%2). | 是 | 本作 |
| 33 | fset_cos | ff (&var, val) | Sets %1 to cos(%2). | 是 | 本作 |
| 34 | mathAngle | fffff (&var, x1, y1, x2, y2) | Calculates the angle from (%2, %3) to (%4, %5) and stores it in %1. | 是 | 本作 |
| 35 | ins_35 | — | Unknown & unused. | 否/待确认 | 本作 |
| 36 | floatTime | fSSSffff (&var, t, b, m, init, final, p1, p2) | In %2 frames using mode %4, %1 changes from %5 to %6. If (%3 == 7), the interpolation changes to a bézier curve where x0 = %5, x1 = %7, x2 = -%8 and x3 = %6. Note that %8 needs to have its sign reversed for the curve to go as expected (why ZUN). | 是 | 本作 |
| 37 | normRad | f (&var) | Normalizes %1 to a value between -pi and pi. | 是 | 本作 |
| 38 | mathCirclePos | ffff (&var_x, &var_y, ang, dist) | Performs the following operations: (%1 = cos(%3) * %4; %2 = sin(%3) * %4) | 是 | 本作 |
| 39 | mathDistance | fffff (&var, x1, y1, x2, y2) | Calculates the distance from (%2, %3) to (%4, %5) and stores it in %1. | 是 | 本作 |
| 40 | jmp_equ | SSSo (a, b, t, target) | If (%1 == %2), jumps to label %4 and sets time to %3. | 是 | 本作 |
| 41 | jmp_equ_f | ffSo (a, b, t, target) | If (%1 == %2), jumps to label %4 and sets time to %3 (float version). | 是 | 本作 |
| 42 | jmp_neq | SSSo (a, b, t, target) | If (%1 != %2), jumps to label %4 and sets time to %3. | 是 | 本作 |
| 43 | jmp_neq_f | ffSo (a, b, t, target) | If (%1 != %2), jumps to label %4 and sets time to %3 (float version). | 是 | 本作 |
| 44 | jmp_lss | SSSo (a, b, t, target) | If (%1 < %2), jumps to label %4 and sets time to %3. | 是 | 本作 |
| 45 | jmp_lss_f | ffSo (a, b, t, target) | If (%1 < %2), jumps to label %4 and sets time to %3 (float version). | 是 | 本作 |
| 46 | jmp_leq | SSSo (a, b, t, target) | If (%1 <= %2), jumps to label %4 and sets time to %3. | 是 | 本作 |
| 47 | jmp_leq_f | ffSo (a, b, t, target) | If (%1 <= %2), jumps to label %4 and sets time to %3 (float version). | 是 | 本作 |
| 48 | jmp_gre | SSSo (a, b, t, target) | If (%1 > %2), jumps to label %4 and sets time to %3. | 是 | 本作 |
| 49 | jmp_gre_f | ffSo (a, b, t, target) | If (%1 > %2), jumps to label %4 and sets time to %3 (float version). | 是 | 本作 |
| 50 | jmp_geq | SSSo (a, b, t, target) | If (%1 >= %2), jumps to label %4 and sets time to %3. | 是 | 本作 |
| 51 | jmp_geq_f | ffSo (a, b, t, target) | If (%1 >= %2), jumps to label %4 and sets time to %3 (float version). | 是 | 本作 |
| 52 | call | S (sub) | Calls sub %1. | 是 | 本作 |
| 53 | ret | — | Returns from the current sub. | 是 | 本作 |
| 54 | anmSet | S (id) | Sets the ANM script of the caller to script %1 in `enemy.anm` | 是 | 本作 |
| 55 | anmSetEx | S (id) | Sets multiple ANM scripts of the caller to scripts (%1) to (%1 + 5) in `enemy.anm`. For movement and other animations. | 是 | 本作 |
| 56 | anmSetEx2 | SSSSSS (id1, id2, id3, id4, id5, id6) | Same as ins_55, but instead of using sequential script IDs, all are specified manually. | 是 | 本作 |
| 57 | anmSetSlot | SS (slot, id) | Sets the ANM script on slot %1 of the caller to script %2 in `enemy.anm` | 是 | 本作 |
| 58 | anmSetBoss | S (id) | Sets the ANM script of the caller to script %1 in this stage's `stg(x)enm.anm`. | 是 | 本作 |
| 59 | anmSetBossEx | S (id) | Sets multiple ANM scripts of the caller to scripts (%1) to (%1 + 5) in this stage's `stg(x)enm.anm`. For movement and other animations. | 是 | 本作 |
| 60 | anmSetBossEx2 | SSSSSS (id1, id2, id3, id4, id5, id6) | Same as ins_59, but instead of using sequential script IDs, all are specified manually. | 是 | 本作 |
| 61 | anmSetBossSlot | SS (slot, id) | Sets the ANM script on slot %1 of the caller to script %2 in this stage's `stg(x)enm.anm` | 是 | 本作 |
| 62 | anmPlayAttack | — | Plays the attack animation of the caller's boss ANM script. Unexpected results if the script is not from `stg(x)enm.anm` | 是 | 本作 |
| 63 | movePos | ff (x, y) | Sets caller's position to (%1,%2). | 是 | 本作 |
| 64 | movePosTime | SSff (t, m, x, y) | In %1 frames using mode %2, move the caller's position to (%3,%4). | 是 | 本作 |
| 65 | moveDir | ff (ang, spd) | Sets caller's movement angle to %1 and speed to %2. | 是 | 本作 |
| 66 | moveDirTime | SSff (t, m, ang, spd) | In %1 frames using mode %2, change caller's movement angle to %3 and speed to %4. | 是 | 本作 |
| 67 | moveRandTime | SSf (t, m, spd) | In %1 frames using mode %2, move the caller in a random direction based on the player's position and the movement boundary with speed %3. Does not work correctly if no movement boundary is set with ins_75. | 是 | 本作 |
| 68 | ins_68 | — | Unknown & unused. | 否/待确认 | 本作 |
| 69 | ins_69 | — | Unknown & unused. | 否/待确认 | 本作 |
| 70 | moveCurve | f (ang) | Sets caller's angular velocity to %1 (adds %1 to the caller's movement angle every frame). | 是 | 本作 |
| 71 | moveAccel | f (spd) | Sets caller's acceleration to %1 (adds %1 to caller's movement speed every frame) | 是 | 本作 |
| 72 | moveCircleAbs | Sffffff (t, x, y, theta, angSpd, rad, radSpd) | For %1 frames, moves the caller in a circle around absolute position (%2,%3), where %4 is the starting angle, %5 is the rotation speed, %6 is the starting radius, and %7 is the radius increase speed. | 是 | 本作 |
| 73 | moveCircle | Sfff (t, theta, angSpd, radSpd) | For %1 frames, moves the caller in a circle around its current position, where %2 is the starting angle, %3 is the rotation speed, and %4 is the radius increase speed. | 是 | 本作 |
| 74 | moveCircleChange | Sff (t, angSpd, radSpd) | Changes the caller's circle movement time to %1, rotation speed to %2, and radius speed to %3. Does not work correctly if ins_72 or ins_73 have not been called earlier. | 是 | 本作 |
| 75 | moveLimit | ffff (left, top, right, bottom) | Limits the caller's movement to a rectangular boundary. | 是 | 本作 |
| 76 | moveLimitReset | — | Removes the caller's movement limit. | 是 | 本作 |
| 77 | hitboxSet | ff (width, height) | Sets the caller's hitbox (player collision) and hurtbox (player shot collision) size to %1, %2. | 是 | 本作 |
| 78 | hurtboxSet | ff (width, height) | Sets the caller's hurtbox (player shot collision) size to %1, %2. | 是 | 本作 |
| 79 | ins_79 | S (A) | Unknown. Argument is always 16. Only used in stage 1. | 否/待确认 | 本作 |
| 80 | flagSet | S (flags) | Sets enemy flags. Refer to [flag table](#s=modding/flags) for details. | 是 | 本作 |
| 81 | flagClear | S (flags) | Clears enemy flags. Refer to [flag table](#s=modding/flags) for details. | 是 | 本作 |
| 82 | etProtectRange | f (rad) | Makes bullets of the caller not spawn if they are within %1 radius of the player. | 是 | 本作 |
| 83 | trailFamiliarSet | S (a) | If (%1 == 1) and the caller is a familiar, adds a trail effect to the caller. | 是 | 本作 |
| 84 | nop84 | — | Unused. Does nothing. | 是 | 本作 |
| 85 | nop85 | — | Unused. Does nothing. | 是 | 本作 |
| 86 | iset_bossvar | SSS (&var, &bossVar, bossId) | Sets %1 to the specified boss' variable %2. Example: <br>[code][ins_notip=86,8](var_10000, var_10051, 1)[/code]<br> would set var_10000 to the life of boss 1 | 是 | 本作 |
| 87 | fset_bossvar | ffS (&var, &bossVar, bossId) | Sets %1 to the specified boss' variable %2. Example: <br>[code][ins_notip=87,8](var_10016, var_10042, 1)[/code]<br> would set var_10016 to the X-Coordinate of boss 1 | 是 | 本作 |
| 88 | bossCall | SS (id, sub) | Calls sub %2 on another boss with boss id %1. | 是 | 本作 |
| 89 | ins_89 | — | Unknown & unused. | 否/待确认 | 本作 |
| 90 | familiarCreateA | SffSSS (sub, x, y, life, item, score) | In absolute position (%2,%3), creates a familiar with %1, %4, %5, and %6. Familiars turn invincible when focusing and clear bullets when destroyed. | 是 | 本作 |
| 91 | familiarCreate | SffSSS (sub, x, y, life, item, score) | Same as ins_90, but the position is relative to the caller instead. | 是 | 本作 |
| 92 | familiarCreateF | SffSSS (sub, x, y, life, item, score) | In position (%2,%3) relative to the caller, creates a familiar that follows the caller with %1, %4, %5, and %6. | 是 | 本作 |
| 93 | enmCreateA | SfffSSS (sub, x, y, z, life, item, score) | In absolute position (%2,%3), creates an enemy with %1, %4, %5, and %6. | 是 | 本作 |
| 94 | enmCreate | SfffSSS (sub, x, y, z, life, item, score) | Samea as ins_93, but the position is relative to the caller instead.. | 是 | 本作 |
| 95 | enmKillAll | — | Kills all active enemies excluding bosses. | 是 | 本作 |
| 96 | etFanAimed | SSSSffffS (spr, col, cnt1, cnt2, spd1, spd2, ang1, ang2, exFlags) | Set bullet attributes: sets aimmode to 0 (aimed fan), sprite and hitbox to %1, color to %2, bullets per layer to %3, layer count to %4, first layer speed to %5, last layer speed to %6, aim offset to %7, angle between bullets to %8, and transform flags to %9. | 是 | 本作 |
| 97 | etFan | SSSSffffS (spr, col, cnt1, cnt2, spd1, spd2, ang1, ang2, exFlags) | Set bullet attributes: sets aimmode to 1 (unaimed fan), sprite and hitbox to %1, color to %2, bullets per layer to %3, layer count to %4, first layer speed to %5, last layer speed to %6, aim direction to %7, angle between bullets to %8, and transform flags to %9. | 是 | 本作 |
| 98 | etRingAimed | SSSSffffS (spr, col, cnt1, cnt2, spd1, spd2, ang1, ang2, exFlags) | Set bullet attributes: sets aimmode to 2 (aimed ring), sprite and hitbox to %1, color to %2, bullets per layer to %3, layer count to %4, first layer speed to %5, last layer speed to %6, aim offset to %7, angle between layers to %8, and transform flags to %9. | 是 | 本作 |
| 99 | etRing | SSSSffffS (spr, col, cnt1, cnt2, spd1, spd2, ang1, ang2, exFlags) | Set bullet attributes: sets aimmode to 3 (unaimed ring), sprite and hitbox to %1, color to %2, bullets per layer to %3, layer count to %4, first layer speed to %5, last layer speed to %6, aim direction to %7, angle between layers to %8, and transform flags to %9. | 是 | 本作 |
| 100 | etRingAimedAway | SSSSffffS (spr, col, cnt1, cnt2, spd1, spd2, ang1, ang2, exFlags) | Set bullet attributes: sets aimmode to 4 (offset aimed ring), sprite and hitbox to %1, color to %2, bullets per layer to %3, layer count to %4, first layer speed to %5, last layer speed to %6, aim offset to %7, angle between layers to %8, and transform flags to %9. | 是 | 本作 |
| 101 | etRingAway | SSSSffffS (spr, col, cnt1, cnt2, spd1, spd2, ang1, ang2, exFlags) | Set bullet attributes: sets aimmode to 5 (offset unaimed ring), sprite and hitbox to %1, color to %2, bullets per layer to %3, layer count to %4, first layer speed to %5, last layer speed to %6, aim direction to %7, angle between layers to %8, and transform flags to %9. | 是 | 本作 |
| 102 | etRandAng | SSSSffffS (spr, col, cnt1, cnt2, spd1, spd2, ang1, ang2, exFlags) | Set bullet attributes: sets aimmode to 6 (random angles), sprite and hitbox to %1, color to %2, bullets per layer to %3, layer count to %4, first layer speed to %5, last layer speed to %6, maximum direction to %7, minimum direction to %8, and transform flags to %9. | 是 | 本作 |
| 103 | etRandSpd | SSSSffffS (spr, col, cnt1, cnt2, spd1, spd2, ang1, ang2, exFlags) | Set bullet attributes: sets aimmode to 7 (random speeds ring), sprite and hitbox to %1, color to %2, bullets per layer to %3, layer count to %4, maximum speed to %5, minimum speed to %6, aim direction to %7, angle between layers to %8, and transform flags to %9. | 是 | 本作 |
| 104 | etRand | SSSSffffS (spr, col, cnt1, cnt2, spd1, spd2, ang1, ang2, exFlags) | Set bullet attributes: sets aimmode to 7 (random angles and speeds), sprite and hitbox to %1, color to %2, bullets per layer to %3, layer count to %4, maximum speed to %5, minimum speed to %6, maximum direction to %7, minimum direction to %8, and transform flags to %9. | 是 | 本作 |
| 105 | etOnAuto | S (t) | Automatically shoots bullets with set attributes every %1 frames. | 是 | 本作 |
| 106 | etOnAutoDelay | S (t) | Automatically shoots bullets with set attributes every %1 frames and delays the first shot by a random value between 0 and %1. | 是 | 本作 |
| 107 | etDelay | — | Sets it so setting bullet attributes does not immediately shoot. | 是 | 本作 |
| 108 | etOn | — | Sets the bullet shoot flag. | 是 | 本作 |
| 109 | etNow | — | Shoots bullets immediately, without any regard for the flag set by ins_108 or the timer set by ins_105. | 是 | 本作 |
| 110 | etOffset | ff (x, y) | Sets the shooting offset to (%1,%2) relative to the caller. | 是 | 本作 |
| 111 | etEx | SSSSSff (slot, id, async, a, b, r, s) | Set bullet transformations. Refer to transform table for details (Note: not on this site yet, will be added soon). | 是 | 本作 |
| 112 | etCancel | — | Clears all bullets on screen and turns them into star items. | 是 | 本作 |
| 113 | etSound | SS (sfxOn, sfxEx) | Sets the sound when a bullet is fired to %1 and the sound when certain transforms are triggered to %2. -1 for defaults. Bullet ex flag 512 needs to be set for any sound to be heard. | 是 | 本作 |
| 114 | laserOn | SSffffffSSSSSS (spr, col, ang, spd, unk1, len1, len2, width, spawnTime, duration, endTime, grazeDelay, grazeSpd, unk2) | Shoots a laser with sprite %1, color %2, angle %3, speed %4, initial length %6, final length %7, width %8, activates after %9 frames, is active for %10 frames, despawns for %11 frames, and can be grazed every %13 frames, after %12 frames. %5 and %14 are unknown. | 是 | 本作 |
| 115 | laserOnAimed | SSffffffSSSSSS (spr, col, ang, spd, unk1, len1, len2, width, spawnTime, duration, endTime, grazeDelay, grazeSpd, unk2) | Same as ins_114, except the laser is aimed at the player. | 是 | 本作 |
| 116 | laserId | S (id) | Sets the index where the next laser shot will be stored to %1. | 是 | 本作 |
| 117 | laserRotate | Sf (id, ang) | Rotates laser of id %1 by %2. | 是 | 本作 |
| 118 | laserAim | Sf (id, ang) | Aims laser of id %1 towards the player and offsets it further by %2. | 是 | 本作 |
| 119 | laserOffset | Sfff (id, x, y, z) | Offsets laser of id %1 by (%2,%3) from its origin. %4 is always `0.0f`. | 是 | 本作 |
| 120 | laserTest | S (id) | Checks if a laser of id %1 is active, and stores the result in var_10038. | 是 | 本作 |
| 121 | laserBreak | S (id) | Instantly cancels laser of id %1. | 是 | 本作 |
| 122 | spell | SSS (unknown, id, score, name, user, desc1, desc2) | Starts a spellcard of id %2 and name %4. %5, %6 and %7 are part of the spell description in spell practice. | 是 | 本作 |
| 123 | spellEnd | — | Ends a spellcard. Also clears all bullets on screen. | 是 | 本作 |
| 124 | playSound | S (sfx) | Plays a sound of id %1. | 是 | 本作 |
| 125 | ins_125 | — | Unknown & unused. | 否/待确认 | 本作 |
| 126 | valSet | SS (val, i) | Writes value %1 at index %2 (in some internal array of the caller). Mainly used to assign subs to be called when a timeline event is triggered. | 是 | 本作 |
| 127 | setBoss | S (id) | Sets the boss id of the caller to %1. Also enables healthbar, timer, and other things. -1 to disable. | 是 | 本作 |
| 128 | cardEff | Sfff (unknown, x, y, z) | Creates a card effect that spins around the caller based on (%2,%3,%4). (x,y,z are not radian values but something else entirely?) | 是 | 本作 |
| 129 | ins_129 | S (A) | Unknown. Used very frequently. | 否/待确认 | 本作 |
| 130 | setInterrupt | S (sub) | Set the sub to be called when health reaches 0. Only works if the caller is a boss. | 是 | 本作 |
| 131 | lifeSet | S (life) | Sets the life of the caller to %1. | 是 | 本作 |
| 132 | timerSet | S (time) | Sets the timer of the caller to %1. The timer increases every frame and attack timer is (timerThreshold - timer). | 是 | 本作 |
| 133 | lifeThreshold | SSS (unknown, life, sub) | Sets the life threshold of the caller to %2. When life reaches this value, call sub %3. | 是 | 本作 |
| 134 | timerThreshold | SS (time, sub) | Sets the attack timer to %1. When the caller's timer reaches this value, call the sub %2. | 是 | 本作 |
| 135 | callAsync | SS (slot, sub) | Asynchronously calls sub %2 at slot %1. | 是 | 本作 |
| 136 | funcCall | SS (func, param) | Calls a function of id %1 from a set of hardcoded functions with the specified parameter. Use %1 = -1 to disable. | 是 | 本作 |
| 137 | funcSet | SS (func, param) | Same as ins_136, but calls the function every frame instead of just once. | 是 | 本作 |
| 138 | ins_138 | — | Unknown & unused. | 否/待确认 | 本作 |
| 139 | effCreate | SSS (id, amt, col) | Creates %2 effects of script (%1 + 28) in `etama.anm` with color %3 at the caller's position. | 是 | 本作 |
| 140 | effCreateAngle | SSSfSS (id, amt, col, ang, unk1, unk2) | Creates %2 effects of script (%1 + 28) in `etama.anm` with color %3 and angle %4 at the caller's position. %5 and %6 are unknown. | 是 | 本作 |
| 141 | dropItemId | S (id) | Instantly item of a given id at caller's position. | 是 | 本作 |
| 142 | dropItems | S (cnt) | Instantly drops %1 items around the enemy. Drops power items if not at max power, otherwise drops point items. | 是 | 本作 |
| 143 | dropMain | S (item) | Set main drop of the caller to the given item (same value that's used by ins_0 timeline instructions). | 是 | 本作 |
| 144 | dropExtra | SS (point, power) | When health reaches 0, drop %1 extra point items and %2 extra power items around the caller's position. | 是 | 本作 |
| 145 | anmRotSet | S (a) | Makes the caller's main ANM script rotate in the direction it's moving if (%1 == 1). | 是 | 本作 |
| 146 | ins_146 | — | Unknown & unused. | 否/待确认 | 本作 |
| 147 | callSTD | S (id) | Calls script ID %1 in the stage's STD file (unconfirmed, thstd crashes on these files). | 是 | 本作 |
| 148 | setLives | S (amt) | Sets the amount of healthbars visible in the top left of the screen to %1. | 是 | 本作 |
| 149 | ins_149 | — | Unknown & unused. | 否/待确认 | 本作 |
| 150 | ins_150 | — | Unknown & unused. | 否/待确认 | 本作 |
| 151 | ins_151 | — | Unknown & unused. | 否/待确认 | 本作 |
| 152 | etRankBoost | ffSSSS (speedMin, speedMax, cnt1Min, cnt1Max, cnt2Min, cnt2Max) | Uses rank to increase speed, bullets per layer, and number of layers for all bullets fired by this enemy. %1, %3, and %5 are the values that are added at 0 rank, while %2, %4, and %6 are the values added at 32 rank. | 是 | 本作 |
| 153 | ins_153 | — | Unknown. Used at the start of every spell. | 否/待确认 | 本作 |
| 154 | ins_154 | — | Unknown & unused. | 否/待确认 | 本作 |
| 155 | spellTimeout | S (a) | Turns the current spell into a timeout spell if (%1 == 1). Timeout spells do not drop in score value and can be captured by timing it down. | 是 | 本作 |
| 156 | ins_156 | — | Unknown & unused. | 否/待确认 | 本作 |
| 157 | trailSet | SSSS (flags, t, unknown, d) | Gives the caller a trail effect with the same sprite as the caller. It spawns a sprite every %4 frames that lasts %2 frames before it disappears. Flags determine the visuals of the trail:<br>1 - display sprite<br>2 - sprite shrinks away<br>4 - sprite fades away<br>Set to 0 to disable entirely, Using flags higher than these explodes the game. | 是 | 本作 |
| 158 | setLifeBar | SSSS (id, lifeMin, lifeMax, col) | Sets lifebar color from %2 to %3 to %4. %1 is used for multiple colors in one lifebar (higher ids for lower life, and need to be set in order). | 是 | 本作 |
| 159 | zIndex | S (layers) | Increases layer of all ANM scripts used by the caller by %1. Negative values turn the caller invisible, and values higher than 3 crash the game. | 是 | 本作 |
| 160 | setInvuln | S (t) | Makes the caller invulnerable to damage for %1 frames. | 是 | 本作 |
| 161 | ins_161 | — | Unknown & unused. | 否/待确认 | 本作 |
| 162 | etClear | — | Clears all bullets on screen without turning them into star items. | 是 | 本作 |
| 163 | ins_163 | — | Unknown & unused. | 否/待确认 | 本作 |
| 164 | ins_164 | — | Unknown & unused. | 否/待确认 | 本作 |
| 165 | anmRotate | f (ang) | Rotates the main ANM script of the caller by %1 if the ANM script allows rotation. | 是 | 本作 |
| 166 | ins_166 | — | Unknown & unused. | 否/待确认 | 本作 |
| 167 | laserAngle | Sf (id, ang) | Sets angle of laser with id %1 to %2. | 是 | 本作 |
| 168 | dropPointItems | S (cnt) | Instantly drops %1 point items around the caller's position regardless of player power. | 是 | 本作 |
| 169 | ins_169 | — | Unknown & unused. | 否/待确认 | 本作 |
| 170 | ins_170 | — | Unknown & unused. | 否/待确认 | 本作 |
| 171 | ins_171 | — | Unknown & unused. | 否/待确认 | 本作 |
| 172 | ins_172 | — | Unknown & unused. | 否/待确认 | 本作 |
| 173 | ins_173 | S (A) | Unknown. Argument is always 0 or 1. | 否/待确认 | 本作 |
| 174 | anmFamiliar | S (id) | Sets some special ANM slot (investigation needed) on the caller to ANM script (%1 + 48) from etama.anm. Should only be used to change the sprite familiars use when the player is focusing. Crashes if id is higher than 2. | 否/待确认 | 本作 |
| 175 | enmSpawnPrevent | S (a) | Prevents enemies from being spawned through the timeline if (%1 == 1). Resumes enemy spawning otherwise. | 是 | 本作 |
| 176 | playerNullify | S (a) | Activates the nullify effect on the player if (%1 == 1). Used in last spells and spell practice. When the player is in nullify state, the next hit will not reduce the player's lives and will activate spell dissolve, which freezes the player and the caller for some time and makes the player invincible. After this time, the screen is cleared of all bullets and the player unfreezes. The caller will remain frozen until the player invincibility runs out. The caller will then unfreeze. | 是 | 本作 |
| 177 | ins_177 | S (A) | Unknown. Argument is always var_10051. | 否/待确认 | 本作 |
| 178 | moveRandTime2 | SSf (t, m, spd) | Similar to ins_67, difference unknown. Used by Reimu in stage 4. | 否/待确认 | 本作 |
| 179 | timeShow | — | Shows the current time in the top right corner of the playing area. Only used by Kaguya when starting her last spells. | 是 | 本作 |
| 180 | ins_180 | — | Unknown & unused. | 否/待确认 | 本作 |
| 181 | timeAdd30 | — | Adds 30 minutes to the time and plays a sound effect. Only used by Kaguya in between her last spells. | 是 | 本作 |
| 182 | anmFollowMain | S (a) | Makes the boss ANM scripts not on the main slot (like Mokou's phoenix) follow the boss sprite bobbing up and down. Only used for Mokou, Yuyuko and Yukari. Might need more research. | 否/待确认 | 本作 |
| 183 | ins_183 | S (A) | Unknown. Argument is always 0 or 1. | 否/待确认 | 本作 |
| 184 | ins_184 | S (A) | Unknown. Argument is always 1. | 否/待确认 | 本作 |

### TH08 时间轴指令

| ID | 助记名 | 参数 | 说明 | 文档化 | 来源 |
| --- | --- | --- | --- | --- | --- |
| 0 | enmCreate | — | Does nothing. | 是 | 本作 |
| 1 | enmCreateM | — | Immediately deletes the caller. | 是 | 本作 |
| 2 | enmCreateRand | S (t) | Stops sub execution time for %1 frames. | 是 | 本作 |
| 3 | enmCreateRand2 | S (A) | Does nothing. Parameter %1 is not even accessed by the game. | 是 | 本作 |
| 4 | enmCreateRandM | So (t, target) | Unconditionally jumps to label %1 and sets time to %2. | 是 | 本作 |
| 5 | enmCreateRand2M | SoS (t, target, &var) | If (%3 != 0), jumps to label %2, sets time to %1 and decrements %3 by 1. | 是 | 本作 |
| 6 | readMsg | SS (&var, val) | Sets %1 to %2. | 是 | 本作 |
| 7 | waitMsg | ff (&var, val) | Sets %1 to %2. | 是 | 本作 |
| 8 | runEvent | SS (&var, val) | Sets %1 to either %2 or -%2 at random. | 是 | 本作 |
| 9 | collectItems | ff (&var, val) | Sets %1 to either %2 or -%2 at random. | 是 | 本作 |
| 10 | waitEnemy | SS (&var, val) | Adds %2 to %1. | 是 | 本作 |
| 11 | enmCreateDropExtra | SS (&var, val) | Subtracts %2 from %1. | 是 | 本作 |
| 12 | enmCreateDropExtraM | SS (&var, val) | Multiplies %1 by %2. | 是 | 本作 |
| 13 | waitTimeline | SS (&var, val) | Divides %1 by %2. | 是 | 本作 |
| 14 | resumeTimeline | SS (&var, val) | %1 = %1 % %2 (modulo) | 是 | 本作 |
| 15 | enmCreateForce | ff (&var, val) | Adds %2 to %1. | 是 | 本作 |
| 16 | showRetryMenu | ff (&var, val) | Subtracts %2 from %1. | 是 | 本作 |

### TH08 变量

| ID | 名称 | 类型 | 访问 | 作用域 | 说明 | 文档化 | 来源 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 10000 | I0 | int | 读写 | local/敌机局部 | Integer variable local to the enemy. Inherited by spawned enemies. | 是 | 本作 |
| 10001 | I1 | int | 读写 | local/敌机局部 | Integer variable local to the enemy. Inherited by spawned enemies. | 是 | 本作 |
| 10002 | I2 | int | 读写 | local/敌机局部 | Integer variable local to the enemy. Inherited by spawned enemies. | 是 | 本作 |
| 10003 | I3 | int | 读写 | local/敌机局部 | Integer variable local to the enemy. Inherited by spawned enemies. | 是 | 本作 |
| 10004 | I8 | int | 读写 | local/敌机局部 | Integer variable local to the enemy. Inherited by spawned enemies. | 是 | 本作 |
| 10005 | I9 | int | 读写 | local/敌机局部 | Integer variable local to the enemy. Inherited by spawned enemies. | 是 | 本作 |
| 10006 | I10 | int | 读写 | local/敌机局部 | Integer variable local to the enemy. Inherited by spawned enemies. | 是 | 本作 |
| 10007 | I11 | int | 读写 | local/敌机局部 | Integer variable local to the enemy. Inherited by spawned enemies. | 是 | 本作 |
| 10008 | LI0 | int | 读写 | local/敌机局部 | Integer variable local to the enemy. Does NOT get inherited by spawned enemies. | 是 | 本作 |
| 10009 | LI1 | int | 读写 | local/敌机局部 | Integer variable local to the enemy. Does NOT get inherited by spawned enemies. | 是 | 本作 |
| 10010 | LI2 | int | 读写 | local/敌机局部 | Integer variable local to the enemy. Does NOT get inherited by spawned enemies. | 是 | 本作 |
| 10011 | LI3 | int | 读写 | local/敌机局部 | Integer variable local to the enemy. Does NOT get inherited by spawned enemies. | 是 | 本作 |
| 10012 | LI4 | int | 读写 | local/敌机局部 | Integer variable local to the enemy. Does NOT get inherited by spawned enemies. | 是 | 本作 |
| 10013 | LI5 | int | 读写 | local/敌机局部 | Integer variable local to the enemy. Does NOT get inherited by spawned enemies. | 是 | 本作 |
| 10014 | LI6 | int | 读写 | local/敌机局部 | Integer variable local to the enemy. Does NOT get inherited by spawned enemies. | 是 | 本作 |
| 10015 | LI7 | int | 读写 | local/敌机局部 | Integer variable local to the enemy. Does NOT get inherited by spawned enemies. | 是 | 本作 |
| 10016.0f | F0 | float | 读写 | local/敌机局部 | Float variable local to the enemy. Inherited by spawned enemies. | 是 | 本作 |
| 10017.0f | F1 | float | 读写 | local/敌机局部 | Float variable local to the enemy. Inherited by spawned enemies. | 是 | 本作 |
| 10018.0f | F2 | float | 读写 | local/敌机局部 | Float variable local to the enemy. Inherited by spawned enemies. | 是 | 本作 |
| 10019.0f | F3 | float | 读写 | local/敌机局部 | Float variable local to the enemy. Inherited by spawned enemies. | 是 | 本作 |
| 10020.0f | F4 | float | 读写 | local/敌机局部 | Float variable local to the enemy. Inherited by spawned enemies. | 是 | 本作 |
| 10021.0f | F5 | float | 读写 | local/敌机局部 | Float variable local to the enemy. Inherited by spawned enemies. | 是 | 本作 |
| 10022.0f | F6 | float | 读写 | local/敌机局部 | Float variable local to the enemy. Inherited by spawned enemies. | 是 | 本作 |
| 10023.0f | F7 | float | 读写 | local/敌机局部 | Float variable local to the enemy. Inherited by spawned enemies. | 是 | 本作 |
| 10024.0f | LF2 | float | 读写 | local/敌机局部 | Float variable local to the enemy. Does NOT get inherited by spawned enemies. | 是 | 本作 |
| 10025.0f | LF3 | float | 读写 | local/敌机局部 | Float variable local to the enemy. Does NOT get inherited by spawned enemies. | 是 | 本作 |
| 10026.0f | LF4 | float | 读写 | local/敌机局部 | Float variable local to the enemy. Does NOT get inherited by spawned enemies. | 是 | 本作 |
| 10027.0f | LF5 | float | 读写 | local/敌机局部 | Float variable local to the enemy. Does NOT get inherited by spawned enemies. | 是 | 本作 |
| 10028.0f | LF6 | float | 读写 | local/敌机局部 | Float variable local to the enemy. Does NOT get inherited by spawned enemies. | 是 | 本作 |
| 10029.0f | LF7 | float | 读写 | local/敌机局部 | Float variable local to the enemy. Does NOT get inherited by spawned enemies. | 是 | 本作 |
| 10030.0f | LF0 | float | 读写 | local/敌机局部 | Float variable local to the enemy. Does NOT get inherited by spawned enemies. | 是 | 本作 |
| 10031.0f | LF1 | float | 读写 | local/敌机局部 | Float variable local to the enemy. Does NOT get inherited by spawned enemies. | 是 | 本作 |
| 10032 | RAND | int | 只读 | global/全局 | Random integer, very large range. | 是 | 本作 |
| 10033.0f | RANDF | float | 只读 | global/全局 | Random float between 0.0f and 1.0f. | 是 | 本作 |
| 10035.0f | RANDF2 | float | 只读 | global/全局 | Random float between -1.0f and 1.0f | 是 | 本作 |
| 10036 | I4 | int | 读写 | local/敌机局部 | Integer variable local to the enemy. Inherited by spawned enemies. | 是 | 本作 |
| 10037 | I5 | int | 读写 | local/敌机局部 | Integer variable local to the enemy. Inherited by spawned enemies. | 是 | 本作 |
| 10038 | I6 | int | 读写 | local/敌机局部 | Integer variable local to the enemy. Inherited by spawned enemies. | 是 | 本作 |
| 10039 | I7 | int | 读写 | local/敌机局部 | Integer variable local to the enemy. Inherited by spawned enemies. | 是 | 本作 |
| 10040 | DIFF | int | 读写 | global/全局 | Difficulty. (0 = easy, 1 = normal, 2 = hard, 3 = lunatic, 4 = extra) | 是 | 本作 |
| 10041 | RANK | int | 读写 | global/全局 | Current rank value | 是 | 本作 |
| 10042.0f | SELF_X | float | 读写 | local/敌机局部 | X position of the enemy. | 是 | 本作 |
| 10043.0f | SELF_Y | float | 读写 | local/敌机局部 | Y position of the enemy. | 是 | 本作 |
| 10044.0f | SELF_Z | float | 读写 | local/敌机局部 | Z position of the enemy. (unused) | 是 | 本作 |
| 10045.0f | PLAYER_X | float | 读写 | local/敌机局部 | X position of the player. | 是 | 本作 |
| 10046.0f | PLAYER_Y | float | 读写 | local/敌机局部 | Y position of the player. | 是 | 本作 |
| 10047.0f | PLAYER_Z | float | 读写 | local/敌机局部 | Z position of the player. (unused) | 是 | 本作 |
| 10048.0f | ANGLE_PLAYER | float | 读写 | local/敌机局部 | Angle from the enemy to the player. | 是 | 本作 |
| 10049 | TIME | int | 读写 | local/敌机局部 | Time elapsed since enemy spawn, in frames. | 是 | 本作 |
| 10050.0f | DIST_PLAYER | float | 读写 | local/敌机局部 | Distance from the enemy to the player. | 是 | 本作 |
| 10051 | LIFE | int | 读写 | local/敌机局部 | Current life of the enemy. | 是 | 本作 |
| 10052 | SHOT | int | 只读 | global/全局 | Shottype. (0 = Border Team, 1 = Magic Team, 2 = Scarlet team, 3 = Netherworld Team, 4 = solo Reimu, 5 = solo Yukari, etc.. | 是 | 本作 |
| 10053 | ARG_A | int | 读写 | local/敌机局部 | Function-Wide integer. | 是 | 本作 |
| 10054 | ARG_B | int | 读写 | local/敌机局部 | Function-Wide integer. | 是 | 本作 |
| 10055 | ARG_C | int | 读写 | local/敌机局部 | Function-Wide integer. | 是 | 本作 |
| 10056 | ARG_D | int | 读写 | local/敌机局部 | Function-Wide integer. | 是 | 本作 |
| 10057.0f | ARG_R | float | 读写 | local/敌机局部 | Function-Wide float. | 是 | 本作 |
| 10058.0f | ARG_S | float | 读写 | local/敌机局部 | Function-Wide float. | 是 | 本作 |
| 10059.0f | ARG_M | float | 读写 | local/敌机局部 | Function-Wide float. | 是 | 本作 |
| 10060.0f | ARG_N | float | 读写 | local/敌机局部 | Function-Wide float. | 是 | 本作 |
| 10061 | A | int | 读写 | local/敌机局部 | Function-Wide integer. When a sub is called, the value is copied to var_10053 in the called sub. | 是 | 本作 |
| 10062 | B | int | 读写 | local/敌机局部 | Function-Wide integer. When a sub is called, the value is copied to var_10054 in the called sub. | 是 | 本作 |
| 10063 | C | int | 读写 | local/敌机局部 | Function-Wide integer. When a sub is called, the value is copied to var_10055 in the called sub. | 是 | 本作 |
| 10064 | D | int | 读写 | local/敌机局部 | Function-Wide integer. When a sub is called, the value is copied to var_10056 in the called sub. | 是 | 本作 |
| 10065.0f | R | float | 读写 | local/敌机局部 | Function-Wide float. When a sub is called, the value is copied to var_10057 in the called sub. | 是 | 本作 |
| 10066.0f | S | float | 读写 | local/敌机局部 | Function-Wide float. When a sub is called, the value is copied to var_10058 in the called sub. | 是 | 本作 |
| 10067.0f | M | float | 读写 | local/敌机局部 | Function-Wide float. When a sub is called, the value is copied to var_10059 in the called sub. | 是 | 本作 |
| 10068.0f | N | float | 读写 | local/敌机局部 | Function-Wide float. When a sub is called, the value is copied to var_10060 in the called sub. | 是 | 本作 |
| 10069.0f | SELF_ANGLE | float | 读写 | local/敌机局部 | Angle of the enemy's movement. | 是 | 本作 |
| 10070.0f | SELF_ANGLE_VEL | float | 读写 | local/敌机局部 | Angular velocity of the enemy. | 是 | 本作 |
| 10071.0f | SELF_SPEED | float | 读写 | local/敌机局部 | Speed of the enemy. | 是 | 本作 |
| 10072.0f | SELF_ACCEL | float | 读写 | local/敌机局部 | Acceleration of the enemy. | 是 | 本作 |
| 10073.0f | CIRCLE_RADIUS | float | 读写 | local/敌机局部 | Radius of enemy's circle movement. | 是 | 本作 |
| 10074.0f | ORIGIN_X | float | 读写 | local/敌机局部 | Spawn X of the enemy. | 是 | 本作 |
| 10075.0f | ORIGIN_Y | float | 读写 | local/敌机局部 | Spawn Y of the enemy. | 是 | 本作 |
| 10076.0f | ORIGIN_Z | float | 读写 | local/敌机局部 | Spawn Z of the enemy. (unused) | 是 | 本作 |
| 10077.0f | CIRCLE_ANGLE | float | 读写 | local/敌机局部 | Current angle in circle movement. | 是 | 本作 |
| 10078.0f | CIRCLE_SPEED | float | 读写 | local/敌机局部 | Current rotation speed in circle movement. | 是 | 本作 |
| 10079.0f | TARGET_X | float | 读写 | local/敌机局部 | Movement Target X of the enemy. | 是 | 本作 |
| 10080.0f | TARGET_Y | float | 读写 | local/敌机局部 | Movement Target Y of the enemy. | 是 | 本作 |
| 10081.0f | TARGET_Z | float | 读写 | local/敌机局部 | Movement Target Z of the enemy. | 是 | 本作 |
| 10082.0f | RANDRAD | float | 只读 | global/全局 | Random float between -pi and pi | 是 | 本作 |
| 10083.0f | LAST_FRAME_DAMAGE | float | 只读 | local/敌机局部 | Amount of damage the enemy received on the previous frame. | 是 | 本作 |
| 10084 | BOSS_ID | int | 只读 | local/敌机局部 | If enemy is a boss, then it's the argument passed to ins_127. If enemy is not a boss, this could be whatever (but 0 by default). | 是 | 本作 |
| 10085.0f | UNUSED_X | float | 读写 | global/全局 | Some X coordinate? | 否/待确认 | 本作 |
| 10086.0f | UNUSED_Y | float | 读写 | global/全局 | Some Y coordinate? | 否/待确认 | 本作 |
| 10087.0f | UNUSED_Z | float | 读写 | global/全局 | Some Z coordinate? | 否/待确认 | 本作 |
| 10088 | LIFE_THRES | int | 读写 | local/敌机局部 | Life threshold of the enemy. Set with ins_133. | 是 | 本作 |
| 10089 | [10089] | int | 只读 | local/敌机局部 | Unknown. | 否/待确认 | 本作 |
| 10090 | [10090] | int | 只读 | local/敌机局部 | Unknown. | 否/待确认 | 本作 |
| 10091 | [10091] | int | 只读 | local/敌机局部 | Unknown. | 否/待确认 | 本作 |
| 10092 | DROP_MAIN | int | 读写 | local/敌机局部 | Value set by ins_143. | 是 | 本作 |
| 10093 | SCORE_REWARD | int | 读写 | local/敌机局部 | The score reward upon killing the enemy. | 是 | 本作 |
| 10094.0f | F8 | float | 读写 | local/敌机局部 | Float variable local to the enemy. Inherited by spawned enemies. | 是 | 本作 |
| 10095.0f | F9 | float | 读写 | local/敌机局部 | Float variable local to the enemy. Inherited by spawned enemies. | 是 | 本作 |
| 10096 | FAMILIAR_COUNT | int | 只读 | local/敌机局部 | Amount of familiars active that were spawned by the enemy. | 是 | 本作 |
| 10097 | PLAYER_IS_YOUKAI | int | 只读 | global/全局 | Set to 1 if player is currently a Youkai. | 是 | 本作 |
| 10098 | TIME_THRES_MET | int | 只读 | global/全局 | Set to 1 if time threshold for the current stage has been met. | 是 | 本作 |
| 10099 | CAPTURE | int | 只读 | global/全局 | Set to 0 when the player dies, bombs or anything else that would fail a spell. Otherwise 1. | 是 | 本作 |
| 10100 | SPELL_TIMER | int | 只读 | global/全局 | Current timer value. | 是 | 本作 |

