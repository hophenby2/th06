# 东方 Project TH06～TH20 Replay 格式与混淆方式分析

本文分析整数编号官方 STG 作品的 `.rpy` 文件，重点是磁盘容器、校验、混淆/“加密”、LZSS、关卡块和逐帧输入流。结论日期为 2026-07-24。

## 1. 结论可信度与样本范围

本文用以下标记区分证据强度：

- **A：样本闭环验证**。能够按声明长度解密、解压并解析到文件末尾；旧格式还校验了 checksum。
- **B：程序行为确认**。由原版 EXE 反汇编、th06/th08 匹配反编译源码或 thtk 实现确认。
- **C：参考信息**。只有第三方解析器或结构定义，没有本地/下载样本闭环。

实际验证了 **57 份 replay**：

| 作品 | 本地官方 demo | 下载的全关 replay | 合计 | 结论 |
|---|---:|---:|---:|---|
| th06 | 0 | 1 | 1 | A+B |
| th07 | 3 | 1 | 4 | A+B |
| th08 | 4 | 1 | 5 | A+B |
| th09 | 0 | 1 | 1 | A+B |
| th10 | 4 | 1 | 5 | A+B |
| th11 | 4 | 1 | 5 | A+B |
| th12 | 4 | 1 | 5 | A+B |
| th13 | 4 | 1 | 5 | A+B |
| th14 | 3 | 1 | 4 | A+B |
| th15 | 3 | 1 | 4 | A+B |
| th16 | 4 | 2 | 6 | A+B |
| th17 | 3 | 1 | 4 | A+B |
| th18 | 4 | 1 | 5 | A+B |
| th20 | 0 | 3 | 3 | A+C |

本地 40 份样本来自：

```text
/Users/happyelements/crack/thtkGUI-th20tr/**/data/*.rpy
```

全关样本主要来自 `https://thscore.pndsng.com/`。该站没有 th09，因此 th09 全关样本取自 Silent Selene 的公开下载接口。两个站点都没有 th19 可用样本，Silent Selene 的 th19 页面也返回 404。

不在本文范围内：th09.5、th12.5、th12.8、th14.3、th16.5、th18.5 等小数编号作品，以及格斗作的独立 replay 系统。

## 2. 格式谱系总览

| 作品 | magic | 格式版本 | 磁盘头大小 | checksum | 压缩 | 主体混淆 |
|---|---|---:|---:|---|---|---|
| th06 | `T6RP` | `0x0102` | `0x50` | 加法和 | 无 | 连续字节加法 |
| th07 | `T7RP` | `0x1100` | `0x54` | 加法和 | LZSS | 连续字节加法 |
| th08 | `T8RP` | `6` | `0x68` | 加法和 | LZSS | 连续字节加法 |
| th09 | `T9RP` | `2` | `0xC0` | 加法和 | LZSS | 连续字节加法 |
| th10 | `t10r` | `5` | `0x24` | 未发现 | LZSS | 两层块置换 + XOR |
| th11 | `t11r` | `4` | `0x24` | 未发现 | LZSS | 两层块置换 + XOR |
| th12 | `t12r` | `4` | `0x24` | 未发现 | LZSS | 两层块置换 + XOR |
| th13 | `t13r` | `2` | `0x24` | 未发现 | LZSS | 两层块置换 + XOR |
| th14 | `t13r` | `2` | `0x24` | 未发现 | LZSS | 两层块置换 + XOR |
| th15 | `t15r` | `3` | `0x24` | 未发现 | LZSS | 两层块置换 + XOR |
| th16 | `t16r` | `2` | `0x24` | 未发现 | LZSS | 两层块置换 + XOR |
| th17 | `t17r` | `2` | `0x24` | 未发现 | LZSS | 两层块置换 + XOR |
| th18 | `t18r` | `6` | `0x24` | 未发现 | LZSS | 两层块置换 + XOR |
| th19 | 未验证 | 未验证 | 未验证 | 未验证 | 未验证 | 未验证 |
| th20 | `t20r` | `1` | `0x30` | 未发现 | LZSS | 两层块置换 + XOR |

需要特别注意：**th14 原版就是 `t13r`**。原版 th14 EXE 内也只包含并检查 `t13r`，不是样本放错。

## 3. th06～th09 的连续字节混淆与校验

这四代使用同一类可逆加法混淆，不是密码学加密。设起始 key 为 `K`，从起始偏移开始的第 `i` 个字节为：

```text
cipher[i] = (plain[i] + K + 7*i) mod 256
plain[i]  = (cipher[i] - K - 7*i) mod 256
```

各代参数如下：

| 作品 | key 偏移 | 混淆起点 | 混淆终点 | checksum 覆盖起点 |
|---|---:|---:|---:|---:|
| th06 | `0x0E` | `0x0F` | EOF | `0x0E` |
| th07 | `0x0D` | `0x10` | EOF | `0x0D` |
| th08 | `0x15` | `0x18` | `core_end` | `0x15` |
| th09 | `0x15` | `0x18` | `core_end` | `0x15` |

checksum 在解密后的字节上计算：

```text
checksum = (0x3F000318 + sum(plain[checksum_start:end])) mod 2^32
```

- th06、th07 的 checksum 位于 `0x08`。
- th08、th09 的 checksum 位于 `0x10`。
- th08、th09 的 `end` 是 `u32 @ 0x0C` 指向的 core 末尾；未加密 USER 块不参与 checksum。

下载的 th06～th09 全关样本和本地所有旧格式 demo 的 checksum 均逐字节通过。

## 4. th06：未压缩、输入变化记录

### 4.1 固定头 `0x50`

| 偏移 | 类型 | 含义 |
|---:|---|---|
| `0x00` | `char[4]` | `T6RP` |
| `0x04` | `u16` | 版本，1.02h 为 `0x0102` |
| `0x06` | `u8` | 机体/子机组合 |
| `0x07` | `u8` | 难度 |
| `0x08` | `u32` | checksum |
| `0x0C` | `u8` | 随机填充值 1 |
| `0x0D` | `u8` | 随机填充值 2 |
| `0x0E` | `u8` | 混淆 key |
| `0x0F` | `u8` | 随机填充值 3，混淆从此开始 |
| `0x10` | `char[9]` | 日期，ASCII |
| `0x19` | `char[8]` | 玩家名，Shift-JIS |
| `0x24` | `u32` | 最终分数 |
| `0x28` | `float` | slowdown 的冗余值 |
| `0x2C` | `float` | slowdown |
| `0x30` | `float` | slowdown 的冗余值 |
| `0x34` | `u32[7]` | 7 个 stage 的文件内偏移，0 表示不存在 |

### 4.2 Stage 与按键流

stage 固定前缀为 `0x10`：

| 相对偏移 | 类型 | 含义 |
|---:|---|---|
| `+0x00` | `i32` | 分数 |
| `+0x04` | `i16` | RNG seed |
| `+0x06` | `i16` | point item 累计数 |
| `+0x08` | `u8` | power |
| `+0x09` | `i8` | lives |
| `+0x0A` | `i8` | bombs |
| `+0x0B` | `u8` | rank |
| `+0x0C` | `i8` | 与 power item 计分有关的计数 |
| `+0x10` | 记录数组 | 输入变化记录 |

每条输入记录 8 字节：

```c
struct Th06Input {
    int32_t frame;
    uint16_t held_keys;
    uint16_t padding;
};
```

它是类似 RLE 的“状态变化表”：只有按键状态变化时才新增记录。每关最后一条记录的 `frame` 固定为 `9999999`，前一条记录的 frame 是该关结束帧。

下载样本包含 6 关，所有关卡末尾都找到 `9999999`，总文件长度 `113040` 字节，checksum 也匹配。

## 5. th07：`0x54` 头、LZSS、双流帧数据

### 5.1 磁盘头

| 偏移 | 类型 | 含义 |
|---:|---|---|
| `0x00` | `char[4]` | `T7RP` |
| `0x04` | `u16` | `0x1100` |
| `0x06` | `u8[2]` | 未知/填充 |
| `0x08` | `u32` | checksum |
| `0x0C` | `u8` | 随机填充值 |
| `0x0D` | `u8` | key |
| `0x0E` | `u8[2]` | 随机/填充，不参与混淆但参与 checksum |
| `0x10` | `u32` | 解压后的完整长度，解密后读取 |
| `0x14` | `u32` | compressed size，解密后读取 |
| `0x18` | `u32` | decompressed body size，解密后读取 |
| `0x1C` | `u32[7]` | 主 stage 流偏移 |
| `0x38` | `u32[7]` | 对应 stage 的 FPS 流偏移 |
| `0x54` | bytes | 加密后的 LZSS 数据 |

严格关系：

```text
disk_size              = 0x54 + compressed_size
decoded_total_size     = 0x54 + decompressed_body_size
u32@0x10               = decoded_total_size
```

此前容易把运行时分配的 `0xE8` 误认为磁盘头。正确含义是：磁盘容器头只有 `0x54`；解压后还会得到 `0x54..0xE7` 的 replay 总信息区，首个 stage 通常从 `0xE8` 开始。头内 `0x10..0x53` 在磁盘上也处于混淆范围，并非全部明文。

### 5.2 解压后的总信息

已确认的字段：

| 偏移 | 类型 | 含义 |
|---:|---|---|
| `0x56` | `u8` | 机体/子机 |
| `0x57` | `u8` | 难度 |
| `0x58` | `char[6]` | 日期 |
| `0x5E` | `char[9]` | 玩家名 |
| `0x6C` | `u32` | 分数，显示时乘 10 |
| `0xCC` | `float` | slowdown |
| `0xE0` | `char[6+]` | 游戏版本字符串，如 `0100b` 或 `debug` |

### 5.3 Stage、主输入流与 FPS 流

stage 状态前缀的有效字段到 `+0x27`：

```text
+00 score                  u32
+04 point_items            i32
+08 cherry                 i32
+0C cherry_max             i32
+10 cherry_plus            i32
+14 graze                  i32
+18 point_extend_count     i32
+1C next_point_threshold   i32
+20 rng_seed               u16
+22 power                  u8
+23 lives                  u8
+24 bombs                  u8
+25 rank                   u8
+26 unknown                u8
+27 spell_bonus_count      u8
```

主按键记录 4 字节：

```c
struct Th07Input {
    uint16_t held_keys;
    uint16_t secondary_state;
};
```

- `+0x2C` 有一条初始 dummy 记录。
- 有效逐帧记录从 `+0x30` 开始，每帧一条。
- 所有主 stage 块连续存放，之后才是所有 FPS 块；两类 offset 数组不是把同一关的两块首尾相接。
- 当前主块的结束位置是下一个非零主 stage offset；最后一个主块以第一个非零 FPS offset 为界。若该边界为 `main_end`，有效帧数为 `(main_end - stage_offset - 0x30) / 4`。
- 当前 FPS 块以同数组的下一个非零 offset 为界，最后一块到解压体末尾。FPS 流约每 30 帧一个字节，正常值通常为 `0x3C`，即 60 FPS；还存在初始/前视字节及最高位状态标志。

全关样本的 6 个 stage 共精确解析到解压体末尾。本地三个 demo 也分别满足同一结构。

## 6. th08：`0x68` 头、压缩 core 与明文 USER

### 6.1 磁盘头

| 偏移 | 类型 | 含义 |
|---:|---|---|
| `0x00` | `char[4]` | `T8RP` |
| `0x04` | `u16` | 版本 `6` |
| `0x06` | `u8[6]` | 标志/保留字段 |
| `0x0C` | `u32` | `core_end`，第一个 USER 块偏移 |
| `0x10` | `u32` | checksum |
| `0x14` | `u8` | 随机/未知 |
| `0x15` | `u8` | key |
| `0x16` | `u8[2]` | 填充 |
| `0x18` | `u32` | compressed size，解密后读取 |
| `0x1C` | `u32` | decompressed body size，解密后读取 |
| `0x20` | `u32[9]` | 9 个主 stage 流偏移 |
| `0x44` | `u32[9]` | 9 个 FPS 流偏移 |
| `0x68` | bytes | 加密后的 LZSS 数据 |

```text
core_end          = 0x68 + compressed_size
decoded_core_size = 0x68 + decompressed_body_size
```

`core_end` 之后是未加密、未参与 checksum 的 USER 块。

### 6.2 解压后的 ReplayData

固定总信息区大小 `0x134`，关键字段：

```text
0x68  unknown/minor version/shot/difficulty
0x6C  date[6]
0x72  player_name[8]
0x7B  is_practice
0x7C  spellcard_number (i16)
0x7E  spellcard_name[48]
0xAE  major_version (u16)
0xB0  spellcard_score
0xB4  GameConfiguration
0x118 slowdown (float)
0x11C clear_state
0x124 exe_size
0x128 exe_checksum
0x12C exe_version[6]
```

stage 常从 `0x134` 开始。序列化的有效状态前缀为 `0x24` 字节：

```text
+00 score                  u32
+04 point_items            i32
+08 graze                  i32
+0C point_extend_count     i32
+10 next_point_threshold   i32
+14 point_item_value       i32
+18 youkai_gauge           i16
+1A rng_seed               u16
+1C power                  u8
+1D lives                  u8
+1E bombs                  u8
+1F rank                   u8
+20 character              u8
+21 unknown                u8
+22 clock_time             u8
+23 unknown/padding        u8
```

- `+0x24` 是一条初始 dummy `u16`。
- 有效输入从 `+0x26` 开始，每帧一个 `u16 held_keys`。
- 与 th07 相同，所有主 stage 块在前、所有 FPS 块在后。当前主块以同数组的下一个非零 stage offset 为界，最后一个主块以第一个非零 FPS offset 为界。
- 若上述边界为 `main_end`，帧数为 `(main_end - stage_offset - 0x26) / 2`。
- 对应 FPS 流仍约每 30 帧保存一个字节；其结束位置由下一个非零 FPS offset 或解压体末尾确定。

四个 demo 与一份全关 replay 均成功验证；全关样本包含 6 个实际 stage。

## 7. th09：双玩家 replay

th09 延续 th08 的 checksum、连续加法混淆、LZSS 和 USER 块，但固定头扩大到 `0xC0`。

### 7.1 磁盘头

| 偏移 | 类型 | 含义 |
|---:|---|---|
| `0x00` | `char[4]` | `T9RP` |
| `0x04` | `u16` | 版本 `2` |
| `0x0C` | `u32` | `core_end` |
| `0x10` | `u32` | checksum |
| `0x15` | `u8` | key |
| `0x18` | `u32` | compressed size，解密后读取 |
| `0x1C` | `u32` | decompressed body size，解密后读取 |
| `0x20` | `u32[10]` | P1 的 10 个 stage 偏移 |
| `0x48` | `u32[10]` | P2 的 10 个 stage 偏移 |
| `0x70` | `u32[10]` | 第三组同尺寸 stage 流，具体用途未定 |
| `0x98` | `u32[10]` | FPS 流偏移 |
| `0xC0` | bytes | 加密后的 LZSS 数据 |

```text
core_end          = 0xC0 + compressed_size
decoded_core_size = 0xC0 + decompressed_body_size
```

### 7.2 Stage

已知 stage 前缀：

```text
+00 score        u32
+04 rng_seed     u16
+06 character    u8
+07 cpu_player   u8
+08 lives        u8
+09 match_place  i8
+0A..+1F         unknown/state
+20              u16 held_keys per frame
```

四组流也分别按组连续存放。组内当前块以本组的下一个非零 offset 为界；本组最后一块以后一组的第一个非零 offset 为界，最后一组则到解压体末尾。没有 th07/th08 的 dummy 记录，前三组的帧数为 `(stage_size - 0x20) / 2`。下载样本有 9 个剧情 stage，P1 与 P2 每一关的帧数完全相同；第三组流也有对应的同尺寸块，原解析代码仅将其标为“可能是 checksum”。

该样本数据：

```text
file size       = 145055
core_end        = 144885
compressed      = 144693
raw body        = 1032017
decoded core    = 1032209
checksum        = 0x40444372 (匹配)
```

## 8. 输入记录数值与实际按键映射

### 8.1 解码原则：记录的是逻辑动作位，不是键盘扫描码

replay 中的输入值是 `u16` 位掩码。每一位代表游戏已经归一化后的逻辑动作，而不是 Windows VK、DirectInput DIK 或手柄按钮编号。下表里的实体键是原版默认键位；玩家改键或使用手柄后，写入 replay 的仍是同一个逻辑动作位。

一个数值可以同时包含多项输入。例如旧位序和现代位序中的方向位相同：

```text
0x0051 = 0x0001 | 0x0010 | 0x0040
       = 射击 + 上 + 左
```

解析时必须按位判断，不能把整个值当枚举：

```c
bool left = (held & 0x0040) != 0;
```

现代记录的 `held`、`pressed`、`released` 共用同一张位表，分别表示本帧保持、刚按下和刚松开。th06～th09 只有保存当前状态的字段。

### 8.2 th06～th09

四作的主输入状态使用同一位序：

| 位值 | 逻辑动作 | 原版默认实体键 |
|---:|---|---|
| `0x0001` | 射击/确认 | Z |
| `0x0002` | Bomb/取消 | X |
| `0x0004` | 低速移动 | Shift |
| `0x0008` | 暂停/菜单 | Esc |
| `0x0010` | 上 | ↑，小键盘 8 也可产生同一位 |
| `0x0020` | 下 | ↓，小键盘 2 也可产生同一位 |
| `0x0040` | 左 | ←，小键盘 4 也可产生同一位 |
| `0x0080` | 右 | →，小键盘 6 也可产生同一位 |
| `0x0100` | 对话快进/跳过 | Ctrl |

th06 的录制掩码只包含射击、Bomb、低速、方向和对话跳过，明确排除了 `0x0008`，所以磁盘 replay 中暂停位恒为 0。th07～th09 会保存暂停位；暂停画面本身不推进游戏帧，但恢复游戏时可能在输入字中看到该位。th07 每帧的第二个 `u16 secondary_state` 不属于上述主按键位，具体语义仍未完全确认。

### 8.3 th10

th10 虽然已经换成现代容器和 6 字节帧记录，但磁盘输入仍沿用旧的低速位序：

| 位值 | 逻辑动作 | 原版默认实体键 |
|---:|---|---|
| `0x0001` | 射击 | Z |
| `0x0002` | Bomb/SPECIAL | X |
| `0x0004` | 低速移动 | Shift |
| `0x0010` | 上 | ↑ |
| `0x0020` | 下 | ↓ |
| `0x0040` | 左 | ← |
| `0x0080` | 右 | → |
| `0x0100` | 对话快进/跳过 | Ctrl |

`0x0008` 是实时输入中的暂停/系统位，但测试的 5 份 th10 replay 均未在逐帧流中出现它，不能假定暂停期间会产生 replay 帧。最重要的版本边界是：**th10 的 `0x0004` 仍是 Shift；th11～th18 以及 th20 的 Shift 是 `0x0008`。**

### 8.4 th11～th18

这些作品的稳定公共位如下：

| 位值 | 逻辑动作 | 原版默认实体键 |
|---:|---|---|
| `0x0001` | 射击 | Z |
| `0x0002` | Bomb/SPECIAL | X |
| `0x0008` | 低速移动 | Shift |
| `0x0010` | 上 | ↑ |
| `0x0020` | 下 | ↓ |
| `0x0040` | 左 | ← |
| `0x0080` | 右 | → |

公共表之外还有一个有范围限制的映射：

| 适用作品 | 位值 | 逻辑动作 | 原版默认实体键 |
|---|---:|---|---|
| th11～th17 | `0x0200` | Ctrl 输入通道 | Ctrl |

th13 按 C 时还会把 `0x0200` 作为组合值的一部分。th18 的帮助、输入显示实现和现有样本均没有给出同样映射，因此不能把 `0x0200=Ctrl` 继续无条件外推到 th18。

`0x0100` 在 th11 以后不应再统一解释成 Ctrl：它只在少数样本中零星出现，属于系统/内部输入，当前没有足够证据给它命名。样本中还观察到 th11、th12 的 `0x0400`，同样没有唯一确认的实体键或游戏动作，解析器应保留而不是丢弃。

作品专用键必须按游戏解释：

| 作品 | replay 值 | 逻辑动作 | 原版默认实体键 | 说明 |
|---|---:|---|---|---|
| th13 | `0x0A00` | 灵界 Trance | C | 磁盘值同时置 `0x0200` 与 `0x0800`；测试样本中的 57 次上升沿均为完整组合值 |
| th16 | `0x0800` | 季节释放 | C | 原版帮助写作 RELEASE；EXE 的配置输入路径也直接生成 `0x0800` |
| th18 | `0x0400` | 使用当前能力卡 | C | 原版帮助写作 ITEM |
| th18 | `0x0800` | 切换当前能力卡 | D | 原版帮助写作 CHANGE |

因此，解析 th13 时不能把 `0x0A00` 显示成“Ctrl + C”两个独立操作；这个组合整体就是一次 C/Trance 输入。反过来，未知作品或未知高位不能仅凭数值相似度套用其他作品的动作名称。

thprac 当前的按键显示辅助代码把 th16 的 C 写成 `0x0A00`，但这与磁盘 replay 和原版 EXE 不符：全部 6 份 th16 样本中 `0x0800` 有 1361 次上升沿而 `0x0200` 一次未见，原版 `th16.exe` 的配置输入分支也直接生成 `0x0800`。因此本文对 replay 采用 `C=0x0800`；thprac 此处只视为显示层实现差异，不能覆盖原版证据。

### 8.5 th20

三份 th20 全关样本与 thprac 的输入显示实现一致：X 动作从此前常见的 `0x0002` 改到了 `0x0004`。

| 位值 | 逻辑动作 | 原版默认实体键 |
|---:|---|---|
| `0x0001` | 射击 | Z |
| `0x0004` | th20 作品专用 X 动作 | X |
| `0x0008` | 低速移动 | Shift |
| `0x0010` | 上 | ↑ |
| `0x0020` | 下 | ↓ |
| `0x0040` | 左 | ← |
| `0x0080` | 右 | → |

测试的三份 th20 replay 共在 `held` 中看到 794 帧 `0x0004`、179 次该位上升沿，而 `0x0002` 一次也没有出现。由于本地没有 th20 原版 EXE，本文只把它命名为“作品专用 X 动作”，不猜测更细的机制名称。`0x0100` 仅出现 2 帧，也暂列为未知/系统输入。

### 8.6 `0xFFFF` 边界哨兵

本地全部 29 份 th11～th18 官方 demo 的 stage 最后一条记录为：

```text
held = pressed = released = 0xFFFF
```

这是 demo 的结束边界哨兵，不表示 16 个键同时按下。它包含在 `frame_count` 和 `stage_data_size` 中，所以结构解析时仍须计入一条 6 字节记录；做按键统计或 edge 一致性检查时则应排除。未知的单独高位仍应按普通位原样保留。

## 9. th10～th18 通用现代容器

### 9.1 明文头 `0x24`

| 偏移 | 类型 | 含义 |
|---:|---|---|
| `0x00` | `char[4]` | 游戏 magic |
| `0x04` | `u16` | replay 格式版本 |
| `0x06` | `u16` | padding，样本为 0 |
| `0x08` | `u32` | 未知/保留，样本通常为 0 |
| `0x0C` | `u32` | `core_end`，第一个 USER 块偏移 |
| `0x10` | `u32` | 游戏版本；官方 demo 常为 0，零售版常为 `0x100` |
| `0x14` | `u32` | 保留，样本为 0 |
| `0x18` | `u32` | 保留，样本为 0 |
| `0x1C` | `u32` | compressed size |
| `0x20` | `u32` | decompressed size |

```text
0x24-byte clear header
encrypted LZSS body               compressed_size bytes
plaintext USER chunks             from core_end to EOF

core_end = 0x24 + compressed_size
```

没有发现独立 checksum 字段。所有样本加载链路都是直接解两层混淆再 LZSS 解压；`0x08` 不是旧格式的加法 checksum。

### 9.2 两层块置换 + XOR 参数

这不是 AES、RC4 或标准密码，而是 `thcrypt.c` 中的自定义可逆置换。解码时先 outer 后 inner；编码时顺序相反。

| 作品 | outer `(key, step, block)` | inner `(key, step, block)` |
|---|---|---|
| th10 | `(0xAA, 0xE1, 0x400)` | `(0x3D, 0x7A, 0x80)` |
| th11 | `(0xAA, 0xE1, 0x800)` | `(0x3D, 0x7A, 0x40)` |
| th12 | `(0x5E, 0xE1, 0x800)` | `(0x7D, 0x3A, 0x40)` |
| th13～th18 | `(0x5C, 0xE1, 0x400)` | `(0x7D, 0x3A, 0x100)` |
| th20 | `(0x5C, 0xE1, 0x400)` | `(0x7D, 0x3A, 0x100)` |

每个块的核心行为：

1. 把块从末尾向前读取。
2. 将奇偶位置拆成两半并重新排列。
3. 每字节 XOR 当前 key。
4. key 每处理一字节加 `step`，按 8 位回绕。

尾块规则也必须复现：

- 若 `size % block < block/4`，最后这个短尾完全不处理。
- 否则处理尾块的偶数字节部分；单独的最后一个奇数字节保持原样。
- replay 调用中的 `limit` 等于 compressed size。

完整解码顺序：

```text
read clear header
take body[compressed_size]
decrypt outer
decrypt inner
LZSS decompress to decompressed_size
parse payload
parse USER chunks from core_end
```

保存顺序：

```text
serialize payload
LZSS compress
encrypt inner
encrypt outer
write clear header + body + USER chunks
```

## 10. LZSS 细节

th07～th20 本文覆盖的压缩 replay 使用相同参数：

```text
bit order            MSB first
dictionary size      8192 (0x2000)
dictionary init      all zero
initial write head   1
flag 1               next 8 bits are one literal byte
flag 0               13-bit dictionary offset + 4-bit encoded length
actual match length  encoded_length + 3, range 3..18
offset 0             end marker
```

允许前向重叠复制，因此解码 match 时必须逐字节同时写回字典，不能先把整个源片段静态切片。

## 11. 现代解压 payload

### 11.1 总信息头

解压体开头就是玩家名区域。官方 demo 常以 ASCII `ZUN     ` 开始，这是玩家名，不是另一个容器 magic。

| 作品 | 总信息头大小 | 玩家名区 | 时间戳 | 分数 | flags | slowdown | stage count | shot | sub/equip/特殊 | 难度 | 最终 stage | spell practice |
|---|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| th10 | `0x64` | `0x00`, 12 | `u32 @ 0x0C` | `0x10` | `0x44` | `0x48` | `0x4C` | `0x50` | `0x54` | `0x58` | `0x5C` | 无 |
| th11 | `0x70` | `0x00`, 12 | `u64 @ 0x0C` | `0x14` | `0x50` | `0x54` | `0x58` | `0x5C` | `0x60` | `0x64` | `0x68` | 无 |
| th12 | `0x70` | `0x00`, 12 | `u64 @ 0x0C` | `0x14` | `0x50` | `0x54` | `0x58` | `0x5C` | `0x60` | `0x64` | `0x68` | 无 |
| th13 | `0x74` | `0x00`, 12 | `u64 @ 0x0C` | `0x14` | `0x50` | `0x54` | `0x58` | `0x5C` | `0x60` | `0x64` | `0x68` | `0x70` |
| th14 | `0x94` | `0x00`, 12 | `u64 @ 0x0C` | `0x14` | `0x50` | `0x74` | `0x78` | `0x7C` | `0x80` | `0x84` | `0x88` | `0x90` |
| th15 | `0xA4` | `0x00`, 12 | `u64 @ 0x0C` | `0x14` | `0x40` | `0x84` | `0x88` | `0x8C` | `0x90` | `0x94` | `0x98` | `0xA0` |
| th16 | `0xA0` | `0x00`, 12 | `u64 @ 0x0C` | `0x14` | `0x40` | `0x7C` | `0x80` | `0x84` | `0x88`/season `0x9C` | `0x8C` | `0x90` | `0x98` |
| th17 | `0xA0` | `0x00`, 16 | `u64 @ 0x10` | `0x18` | `0x44` | `0x80` | `0x84` | `0x88` | `0x8C` | `0x90` | `0x94` | `0x9C` |
| th18 | `0xC8` | `0x00`, 16 | `u64 @ 0x10` | `0x18` | 未定 | `0xA4` | `0xA8` | `0xAC` | `0xB0` | `0xB4` | `0xB8` | `0xC0` |

时间戳为 Unix epoch 秒。分数字段通常以显示值除 10 保存；PIV 等计分字段也有作品特定缩放，不能统一按显示值解释。

### 11.2 Stage 固定头

th10～th18 的每个 stage 都以共同的 12 字节头开始：

```c
struct ModernStagePrefix {
    uint16_t stage_number;     // 1 based
    uint16_t rng_seed;
    uint32_t frame_count;      // N
    uint32_t stage_data_size;  // 不含固定头，含输入和 FPS 流
};
```

不同作品的固定头总大小：

| 作品 | 固定头大小 | 代表性状态 |
|---|---:|---|
| th10 | `0x1C4` | score、power、faith、combo、位置、残机 |
| th11 | `0x90` | score、power、connect、位置、残机碎片、graze |
| th12 | `0xA0` | score、power、PIV、残机/炸弹碎片、UFO、graze |
| th13 | `0xC4` | PIV、power、残机/炸弹、trance、符卡时间 |
| th14 | `0xDC` | PIV、power、残机/炸弹、2.0 道具奖励、符卡时间 |
| th15 | `0x238` | chapter、miss、PIV、完美无缺模式重置、BGM 状态 |
| th16 | `0x294` | season、季节能量、PIV、符卡时间 |
| th17 | `0x158` | token、咆哮/暴走计时、PIV、符卡时间 |
| th18 | `0x126C` | start/end 两份大状态快照、卡牌与卡牌参数 |

固定头本质上是可恢复游戏状态的快照，而不是只有展示信息。因此跨作品转换时不能只复制公共字段。

### 11.3 每帧 6 字节输入记录

固定头之后有 `N` 条记录：

```c
struct ModernInput {
    uint16_t held;
    uint16_t pressed;
    uint16_t released;
};
```

普通帧满足：

```text
pressed  = held_now  & ~held_previous
released = held_prev & ~held_now
```

在 stage 边界或游戏强制清空输入时，可能保留/清空 `held` 而不生成对应 edge 位，解析器不应把不满足公式的边界记录判成损坏。

位值会随作品变化，完整的数值到默认实体键映射见第 8 节。尤其不能把所有现代作品统一解释成 `0x0004=低速`：th10 是 `0x0004=Shift`，th11～th18 以及 th20 是 `0x0008=Shift`，而 th20 又把 `0x0004` 用作 X 动作。

本地 th11～th18 的 29 份官方 demo 均以三字段全 `0xFFFF` 的记录结束 stage；它是结束边界哨兵，不参与普通按键和 edge 统计。

### 11.4 FPS 低频流与 stage 长度公式

`N * 6` 字节输入记录后紧跟 FPS 字节流，长度严格为 `ceil(N / 30)`。所有 43 份 th10～th18 样本均满足：

```text
stage_data_size = N * 6 + ceil(N / 30)
next_stage      = current_stage + fixed_header_size + stage_data_size
```

FPS 字节正常值多为 `0x3C`。它用于记录约每 30 帧的实际帧率并计算处理落率。

全关样本中，th10～th18 每份均有 6 个 stage，按上述公式逐块前进后恰好等于解压长度，没有剩余或越界。

## 12. th20：自描述尺寸的新容器

th20 继续使用 th13～th18 的两层块混淆参数与同一 LZSS，但把明文头扩到 `0x30`，并显式保存三种结构大小。

### 12.1 磁盘头 `0x30`

| 偏移 | 类型 | 含义 |
|---:|---|---|
| `0x00` | `char[4]` | `t20r` |
| `0x04` | `u16` | replay 版本 `1` |
| `0x06` | `u16` | padding |
| `0x08` | `u32` | 未知/运行时值，不能要求为 0 |
| `0x0C` | `u32` | `core_end` |
| `0x10` | `u32` | 游戏版本，样本为 `0x100` |
| `0x14` | `u32` | 保留，样本为 0 |
| `0x18` | `u32` | 保留，样本为 0 |
| `0x1C` | `u32` | 磁盘头大小，样本为 `0x30` |
| `0x20` | `u32` | 解压后总信息头大小，样本为 `0x100` |
| `0x24` | `u32` | 每个 stage 固定头大小，样本为 `0x2A0` |
| `0x28` | `u32` | compressed size |
| `0x2C` | `u32` | decompressed size |
| `0x30` | bytes | 加密后的 LZSS 数据 |

```text
core_end = header_size + compressed_size
```

### 12.2 解压后的总信息头 `0x100`

```text
0x00 player_name[16]
0x10 timestamp u64
0x18 score u32
0x1C game/config state[180]
0xD0 slowdown float
0xD4 stage_count u32
0xD8 shot u32
0xDC stones[4] u32
0xEC unknown u32
0xF0 difficulty u32
0xF4 unknown u32
0xF8 unknown u32
0xFC spell_practice_id u32
```

### 12.3 Stage

th20 把共同 stage 前缀改为 4 个 `u32`：

```c
struct Th20StagePrefix {
    uint32_t stage_number;
    uint32_t rng_state;
    uint32_t frame_count;
    uint32_t stage_data_size;
};
```

stage 固定头为外层 `u32 @ 0x24` 声明的 `0x2A0`。其后仍是与 th10～th18 相同的 6 字节 `held/pressed/released` 记录和 `ceil(N/30)` 字节 FPS 流：

```text
stage_data_size = N * 6 + ceil(N / 30)
```

三份全关 replay 都有 6 个 stage，全部 transition 记录满足 edge 公式，最后一个 stage 结束位置与 decompressed size 完全相等：

| 样本 | compressed | decompressed | stage 数 |
|---|---:|---:|---:|
| `th20_ud1144.rpy` | 161320 | 1018537 | 6 |
| `th20_ud1172.rpy` | 138681 | 927910 | 6 |
| `th20_ud1244.rpy` | 155294 | 1008117 | 6 |

其中两份文件额外带有 thprac 的 `PRAC` USER 块；这不改变官方 core 格式。

逐帧输入的公共方向、射击和低速位与 th11～th18 相同，但三份样本中的 X 动作使用 `0x0004`，没有出现 `0x0002`；详见第 8.5 节。

## 13. USER 扩展块

th08 以后，core 末尾可以追加一个或多个未加密 USER 块：

```c
struct UserBlockHeader {
    char     magic[4];   // "USER"
    uint32_t length;     // 包含 12 字节头
    uint32_t id;         // 0=文本信息，1=注释；也可能是第三方 FourCC
};
```

布局：

```text
USER header (12 bytes)
payload (length - 12 bytes)
next USER header, if any
```

已观察到：

- `id=0`：Shift-JIS 文本 replay 信息，如 Version、Name、Date、Chara、Rank、Stage、Score、Slow Rate。
- `id=1`：用户注释。
- `id='PRAC'`：thprac JSON 扩展。
- th08/th09 的早期实现只可靠使用 id 的低 8 位，高 24 位可能是未初始化填充，不能要求整个 `u32` 为 0 或 1。
- USER 长度不是固定值。本地现代 demo 常见总尾长 200 字节，下载全关 replay 常见 208 字节，th18/th17 还有其他长度。
- 解析 core 时必须使用 `core_end`，不要把 USER 文本送进解密或 LZSS。

th06、th07 没有这种尾块。

## 14. th14 magic 冲突与异常样本

th13 和 th14 都是 `t13r`、格式版本 2。可靠区分方式包括：

- 外层 `game_version @ 0x10` 与解压后字段布局。
- th13 总信息头/首 stage 分别是 `0x74`/`0xC4`。
- th14 总信息头/首 stage 分别是 `0x94`/`0xDC`。
- USER 信息中的作品名只能作为辅助判断，不能代替结构校验。

从 thscore 下载的 `th16_ud0451.rpy` 实际 magic 为 `t13r`，USER 文本也写明“东方辉针城”和版本 `1.00b`，它是被误归到 th16 页面的 th14 replay。本文将它作为站点归类异常排除，没有据此修改 th16 的 `t16r` 结论。另两份 th16 下载文件均为正常 `t16r`。

## 15. th19 与未覆盖结论

当前证据不足以给出 th19 格式：

- 用户提供的本地目录没有 th19 游戏或 `.rpy`。
- thscore 的作品列表没有 th19。
- Silent Selene 的 `/replays/th19` 返回 404。
- 本次采用的公开解析器也没有可验证的 th19 定义。

因此本文不把 th18/th20 的参数外推为 th19，也不猜测其 magic、版本或 stage 布局。拿到一份原版 th19 replay 和对应 EXE 后，才能用同样方法补齐。

## 16. 解析器实现注意事项

1. 所有整数均为 little-endian；LZSS 位流则是 MSB-first。
2. 先验证文件实际长度，再使用头中的 offset/size，防止整数溢出和越界。
3. 给 LZSS 设置严格输出上限，且校验实际输出恰好等于声明的 decompressed size。
4. 旧格式 checksum 只是 32 位加法和，不能提供抗篡改安全性。
5. 现代块混淆没有 IV、随机 nonce 或认证标签，同样不具备密码学安全性。
6. `th_decrypt` 的短尾规则不可省略，否则部分文件末尾会解错。
7. stage 指针必须在解压体范围内并保持合理顺序；不要信任非零指针一定有效。
8. 不要假设 replay 只有一关。官方 demo 常是一关，全关 replay 通常有六关。
9. 不要假设 USER 恰好两个或固定 200 字节，应按 `length` 迭代到 EOF。
10. 玩家名、作品说明和注释通常是 Shift-JIS；ASCII 字段也可能带 NUL/padding。
11. th14 不能只按 magic 分派；th20 不能套用旧的 `0x24` 容器头。
12. 现代 stage 边界的输入 edge 可能被游戏强制重置，不能据此单独判坏。
13. 输入位表必须按作品选择，不能把 `0x0004`、`0x0008`、`0x0100` 或高位跨作品硬套同一含义。
14. 官方 demo 末尾三字段全 `0xFFFF` 的现代输入记录是结束哨兵；结构长度须计入，但不要统计成 16 键齐按，也不要用它验证普通 edge 公式。
15. 对尚未命名的高位应保留原值，并在输出中标为 unknown；不要静默清零。

## 17. 关键验证结果

- th06：1/1 checksum 通过，6 个 stage 的 `9999999` sentinel 全部存在。
- th07：4/4 checksum 通过，LZSS 输出长度全部精确匹配；全关 6 stage 精确落到末尾。
- th08：5/5 checksum 通过，LZSS 与 USER 边界全部匹配。
- th09：1/1 checksum 通过，P1/P2 九关帧数逐关相同，四组 offset 均在范围内。
- th10～th18：43/43 两层解密和 LZSS 成功；每个 stage 均满足 `6*N + ceil(N/30)`，逐块解析后等于 decompressed size。
- th20：3/3 两层解密和 LZSS 成功；`0x30/0x100/0x2A0` 三个尺寸字段与所有 stage 边界完全一致。
- 输入位：29/29 份 th11～th18 官方 demo 的最后一条记录均为三字段全 `0xFFFF`；th13 的 57 次 C 上升沿均为 `0x0A00`；th20 的 X 位为 `0x0004`，三份样本均未出现 `0x0002`。
- 所有现代样本解密后都能得到合理玩家名、时间戳、stage count 和状态快照，而不是仅靠“开头看起来像文本”判断成功。

## 18. 参考实现与证据位置

本地精确/匹配反编译源码：

```text
/Users/happyelements/crack/th062/src/ReplayData.hpp
/Users/happyelements/crack/th062/src/ReplayManager.cpp
/Users/happyelements/crack/th062/src/Controller.hpp
/Users/happyelements/crack/th062/src/Controller.cpp
/Users/happyelements/crack/th08/src/ReplayManager.hpp
/Users/happyelements/crack/th08/src/ReplayManager.cpp
/Users/happyelements/crack/th08/src/Global.hpp
/Users/happyelements/crack/th08/src/Global.cpp
/Users/happyelements/crack/th08/src/pbg/Lzss.cpp
/Users/happyelements/crack/th06-master/thprac/thprac/src/thprac/thprac_igi_key_render.cpp
```

作品专用键的原版帮助图：

```text
/Users/happyelements/crack/thtkGUI-th20tr/[th13] 东方神灵庙 (汉化版+日文版)/data/help_02.png
/Users/happyelements/crack/thtkGUI-th20tr/[th16] 东方天空璋 (汉化版+日文版)/[th16] 东方天空璋（汉化版+日文版）/data/help_03.png
/Users/happyelements/crack/thtkGUI-th20tr/[th18] 东方虹龙洞 (汉化版+日文版)/data/help_03.png
```

通用算法参考：

```text
/Users/happyelements/crack/thtk/thtk/thcrypt.c
/Users/happyelements/crack/thtk/thtk/thlzss.c
/Users/happyelements/crack/thtk/thtk/bits.c
```

其他交叉参考：

- `https://github.com/wz520/thhyl`
- `https://github.com/zero318/th-re-data`
- `https://github.com/hoangcaominh/thrpy-parser`
- `https://github.com/hoangcaominh/thrpy-decode`
- `https://thscore.pndsng.com/`
- `https://www.silentselene.net/replays/th09`

原版 EXE 反汇编重点：

```text
th07.exe 0x443040  replay 初始化与 0xE8 运行时结构
th07.exe 0x442CD0  逐帧记录
th07.exe 0x442EE0  逐帧播放
th07.exe 0x4433B0  加载、解密、checksum、LZSS
th07.exe 0x4444D0  保存、压缩、checksum、混淆

th08.exe 0x452310  录制
th08.exe 0x452550  播放
th08.exe 0x452830  初始化
th08.exe 0x452D60  demo 初始化

th13.exe 0x471620  键盘/手柄输入构造
th16.exe 0x4018E0  可配置动作到逻辑输入位；0x4019F0 分支生成 0x0800
th16.exe 0x401D50  键盘输入读取
th18.exe 0x401860  可配置动作到逻辑输入位；0x401969/0x401984 生成 0x0400/0x0800
```
