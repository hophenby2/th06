# TH12.8 妖精大战争 ECL 速查

> 根据 `th062/ecl-web.txt` 中列出的 Priw8 ECL 指令表、变量表、flags/MERLIN 文档，以及本地提供的 THBWiki 文本 `th062/ecl*.txt` 整理。具体 opcode/变量主表以 Priw8 源数据为准，THBWiki 中文说明作为代际补充与交叉索引。

## 阅读说明

- `ID` 为 ECL opcode 或变量编号；`助记名` 来自 priw8 的 eclmap。
- `参数` 中前半为格式串，括号内为参数名；`S/$` 常见为整数，`f/%` 常见为浮点，`o` 常见为跳转 offset/label。
- `来源` 表示该条在 Priw8 继承链中的定义来源；第四世代大量指令会从 TH13 继承。
- 变量表只列有记录的变量；范围内未列出的编号通常为空洞或未调查。

- 返回总表：`../ecl-reference-by-game.md`
- 本文包含：TH12.8 对应世代 THBWiki 中文代码表、全局 flags/常量、该游戏 Priw8 指令/变量主表。

## 本游戏概览

| 游戏 | 作品 | 代际/体系 | 指令表覆盖 | 变量表覆盖 | 摘要 |
| --- | --- | --- | --- | --- | --- |
| TH12.8 | 妖精大战争 | 第三世代 | 未列 | 有 | ecl-web.txt 未列出该作 Priw8 指令表；通常沿用相近世代/上一作格式，本文仅列变量。 变量范围 -10000..-9909；本文列出有说明/命名记录的 92 条，未列空洞/未知项。 |

## THBWiki 中文代际补充

这些表保留 THBWiki 中文页面中的签名和说明，便于和 Priw8 分游戏 opcode 表互查；同一 opcode 的英文精确定义仍见各游戏主表。

### THBWiki 第三世代 ECL

- 适用范围：星莲船、Double Spoiler、妖精大战争；THBWiki 以 TH12 为主体，DS/大战争有少量差异。
- 页面概述：本对照表是Zun的第三代ecl脚本的对照表,适用于星，ds，dzz3作 以下均是基于th12 星莲船的脚本制成， 文花帖DS和妖精大战争与有一小部分不同 对于其他作的参考 第一代ecl脚本红妖永花,文花帖.由于与此表差异很大,故不能作任何参考. 第二代ecl脚本对应风地 第二代中280对应此表中300，320对应此表中400，400对应此表中500，其余大体可以按顺序对照. 第三代ecl脚本对应星，文花帖ds和大战争 第四代ecl脚本对应城，天邪鬼，绀珠传 第四代中300对应此表中256,400对应此表中300，500对应此表中400，600对应此表中500，其余大体可以按顺序对照. 提取zun脚本的工具是touhou toolkit. 以下即是所有存在的ins,是读取汇编所获得的 红色代表功能未知，需要测试和研究 蓝色代表虽然并未完全解读，但是大体功能已经知道，且此函数用途十分有限 灰色代表是前作特殊地点使用过之后完全被抛弃的 棕色部分是文花帖DS新增 青色部分是妖精大战争新增
- 抽取 opcode：126 条。

| ID | THBWiki 参数签名 | 章节 | 中文说明摘要 |
| --- | --- | --- | --- |
| 256 | "xxx", float x, float y, int life, int bonus, int item | 2系 设置贴图，播放特效动画，创建单位 | 以相对召唤者为基准点在位置xy，创建一个单位xxx，设置血量，分数以及基本掉落。 |
| 257 | "xxx", float x, float y, int life, int bonus, int item | 2系 设置贴图，播放特效动画，创建单位 | 在绝对位置xy，创建一个单位xxx，设置血量，分数以及基本掉落。用于boss |
| 258 | int | 2系 设置贴图，播放特效动画，创建单位 | 选择ANM文件。一般来说0即是Bullet.anm，1即是Enemy.anm,2开始就是当面的boss相关anm |
| 259 | int slot,int a | 2系 设置贴图，播放特效动画，创建单位 | 在相应slot上,设置单位贴图,a对应由上一个258选择的ANM文件中的SCRIPT号 若使用529则单位不会因为左右移动而改变贴图 |
| 260 | "xxx", float x, float y, int life, int bonus, int item | 2系 设置贴图，播放特效动画，创建单位 | 和256的基本功能一样，但是移动方式为左右镜像。 |
| 261 | "xxx", float x, float y, int life, int bonus, int item | 2系 设置贴图，播放特效动画，创建单位 | 和257的基本功能一样，但是移动方式为左右镜像。 |
| 262 | int slot,int a | 2系 设置贴图，播放特效动画，创建单位 | 在相应slot上,设置单位贴图,a对应由上一个258选择的ANM文件中的SCRIPT号 若使用262且slot 0，则单位会因为左右移动而改变贴图, 若slot不为0，则和259无区别. |
| 263 | int a,int b | 2系 设置贴图，播放特效动画，创建单位 | 在单位当前位置播放ANM文件a的第b个动画效果，b对应由上一个258选择的ANM文件的 script号 |
| 264 | int a,int b | 2系 设置贴图，播放特效动画，创建单位 | 在左上角播放ANM文件a的第b个动画效果，b对应由上一个258选择的ANM文件的 script号 |
| 265 | "xxx", float x, float y, int life, int bonus, int item | 2系 设置贴图，播放特效动画，创建单位 | 用于增员(boss存在时不执行)，其余和256一样 |
| 266 | "xxx", float x, float y, int life, int bonus, int item | 2系 设置贴图，播放特效动画，创建单位 | 用于增员，其余和257一样 |
| 267 | "xxx", float x, float y, int life, int bonus, int item | 2系 设置贴图，播放特效动画，创建单位 | 用于增员，其余和260一样 |
| 268 | "xxx", float x, float y, int life, int bonus, int item | 2系 设置贴图，播放特效动画，创建单位 | 用于增员，其余和261一样 |
| 269 | int a | 2系 设置贴图，播放特效动画，创建单位 | 在单位当前位置播放之前选择的ANM文件的第a个动画效果，a对应由上一个258选择的ANM文件的 script号 |
| 270 | "xxx", float x, float y, int life, int bonus, int item | 2系 设置贴图，播放特效动画，创建单位 | 一种未知的创建单位函数 |
| 271 | "xxx", float x, float y, int life, int bonus, int item | 2系 设置贴图，播放特效动画，创建单位 | 用于增员,其余和270一样 |
| 272 | int a,int b | 2系 设置贴图，播放特效动画，创建单位 | 和263功能基本一样,区别未知 |
| 273 | int a,int b,float c | 2系 设置贴图，播放特效动画，创建单位 | 选择a号贴图文件的b号单位贴，旋转至c方向贴出。此贴图不会消失而是一直存在于屏幕上。（配合自带延迟消失指令的单位贴可以做出类似残影效果。） |
| 274 | int slot,int b | 2系 设置贴图，播放特效动画，创建单位 | 发弹时(应为循环时)，在相应slot播放动作 b，b对应由上一个258选择的ANM文件的 script号 |
| 275 | int slot,int b | 2系 设置贴图，播放特效动画，创建单位 | 播放slot预选好的动画,并且遇到anmins_64时,选择b号执行 注：anmins_64是一种switch分支结构,默认选择0号。 |
| 276 | — | 2系 设置贴图，播放特效动画，创建单位 | 重置所有动画相关.移除flag0x80000 |
| 277 | int slot,float b | 2系 设置贴图，播放特效动画，创建单位 | 旋转在相应slot的贴图至b方向。会旋转方形判定和612的方形消弹。 |
| 278 | int slot,float b,float c | 2系 设置贴图，播放特效动画，创建单位 | 用于改变slot位置贴图的大小 倍率为 b和c |
| 279 | int slot,float x,float y | 2系 设置贴图，播放特效动画，创建单位 | 把相应slot的贴图移动到相对位置,x,y.高速来回运动可制造震动效果 |
| 280 | "xxx", float x, float y, int life, int bonus, int item | 2系 设置贴图，播放特效动画，创建单位 | 用于创建mapleenemy,即背景的枫叶动画效果 |
| 281 | int slot,int b | 2系 设置贴图，播放特效动画，创建单位 | 只有在莲妈身后的花和翅膀使用，用途不明 |
| 282 | int slot,int b | 2系 设置贴图，播放特效动画，创建单位 | 文花帖DS新增，设置本单位被拍掉时候显示的动画，从bullet.anm里的script b号 |
| 283 | float a,float b,int c | 2系 设置贴图，播放特效动画，创建单位 | DZZ新增 |
| 314 | — | 3系 单位移动 | 将单位移动至boss的位置,此函数若在无boss时使用会导致严重误访问而爆炸 |
| 315 | — | 3系 单位移动 | 和314成对 |
| 316 | float x,float y,float height | 3系 单位移动 | 瞬间移动到与当前位置偏移x,y的位置,并且改变单位深度，此深度只适用于风神录（296）四面的潜水怪 |
| 317 | float x,float y,float height) | 3系 单位移动 | 和316成对 |
| 318 | float x,float y | 3系 单位移动 | 仅在前作FSL（298）6面神妈的圈圈移动上使用 |
| 319 | float x,float y | 3系 单位移动 | 和318成对 |
| 320 | float θ,float speed,float radius,float,rspeed,float dir,float rate | 3系 单位移动 | 使单未进行椭圆运动,曲线的极坐标（原点为单位之前的位置）(radius,θ) θ的增速为speed，radius增速为 rspeed,dir为 椭圆偏离的方向，rate为长半轴与短半轴的比例 |
| 321 | int time,int mode, float speed, float radius, float rspeed,float dir,float rate | 3系 单位移动 | time帧之内改变单位圆周运动的参数,方式为mode.各参数参考320 |
| 322 | float θ,float speed,float radius,float,rspeed,float dir,float rate | 3系 单位移动 | 和320成对 |
| 323 | int time,int mode, float speed, float radius, float rspeed,float dir,float rate | 3系 单位移动 | 和321成对 |
| 324 | int a | 3系 单位移动 | 当a =1的时候赋予单位flag（ins_402中的）0x00040000,a=0的是消除 此flag会赢304和305,效果为左右翻转 |
| 325 | int time,float x1,float y1,float x2,float y2,float x3,float y3 | 3系 单位移动 | 在time时间内将单位最终移动至点x2,y2. 期间首先向点x1,y1移动和一点时间再向 终点偏差x3,y3移动一段时间再移动至终点x2,y2. |
| 326 | int time,float x1,float y1,float x2,float y2,float x3,float y3 | 3系 单位移动 | 和325成对 |
| 327 | — | 3系 单位移动 | 初始化和清零移动相关参数有关 |
| 328 | int)304的无视flag0x40000(左右翻转 | 3系 单位移动 | 版 |
| 329 | int)305的无视flag0x40000(左右翻转 | 3系 单位移动 | 版 |
| 330 | int)306的无视flag0x40000(左右翻转 | 3系 单位移动 | 版 |
| 331 | int)307的无视flag0x40000(左右翻转 | 3系 单位移动 | 版 |
| 332 | int | 3系 单位移动 | 未知 |
| 333 | int | 3系 单位移动 | 未知 |
| 405 | — | 4系 单位固有属性 | 移除boss移动范围限制 406 ClearDrops()清除掉落 407 SetDrops(int type,int amount) 目标掉落道具及数量 1.p点 2蓝点 3.大p 4.残碎片 5B碎片，6残机 7Bomb 8大F 9小最大得点，每100个加10得点 10固红11固蓝12固绿13变红14变蓝15变绿 16是击破碟给的那一坨红点，没东西估计还要加别的参数，17是那一坨蓝点，里面也没东西，18是一坨红蓝点 408 SetDropArea(float width,float height)设置掉落区域 409 Drop()掉落所有道具 410 SetBasicDrop(int type) 设置目标基本掉落，数量是1. 4… |
| 412 | int a | 4系 单位固有属性 | a=0，设为boss战模式（血条，名字等），赋予单位flag0x00400000 ，a=-1，结束boss。消除单位flag0x00400000 |
| 413 | — | 4系 单位固有属性 | boss 重置时间 414 SetNextPattern(int a，血量，时间，“阶段变量名”), 当血量和或时间达到此数值时 载入下一阶段（符卡或非符） a的作用未知 415 Invisible(int time) 无敌时间， 416 PlaySE(int)播放音效 |
| 417 | int a，int b，int c | 4系 单位固有属性 | 震屏特效。a为持续时间（帧），bc均与震屏强度有关，都是越大震动越强，区别不明。 418 Talk（int） 读取对话，参数对应msg文件 419 AfterTalk（）对话后进行下一条 420 AfterKill（）击破后进行下一条 421 TimeOut（int a，“func”） 时间到0时进行func的内容，a作用未知 422 SetSpellCard(int a, int life, int score, "X符:XXXX"); 进入符卡模式，设置符卡宣言后右上角 符卡时间，scb，符卡名，a和符卡序号有关 EX面使用 423 EndSpellCard() 结束符卡模式 424 SetChapter(int) 设置gzz里… |
| 429 | %N，float a,b,c | 4系 单位固有属性 | 根据RANK决定变量N |
| 430 | %N，float a,b,c,d,e | 4系 单位固有属性 | 根据RANK决定变量N |
| 431 | %N，float a,b | 4系 单位固有属性 | 根据RANK决定变量N |
| 432 | $M，int a,b,c | 4系 单位固有属性 | 根据RANK决定变量M |
| 433 | $M，int a,b,c,d,e | 4系 单位固有属性 | 根据RANK决定变量M |
| 434 | $M，int a,b | 4系 单位固有属性 | 根据RANK决定变量M |
| 435 | $M,int a,b,c,d | 4系 单位固有属性 | 根据难度将数据写入整数M中 |
| 436 | %N,float a,b,c,d | 4系 单位固有属性 | 根据难度将数据写入浮点数N中 437 SetSpellCard(int a, int time, int score, "X符:XXXX"); 进入符卡模式，设置符卡宣言后右上角 符卡时间，scb，符卡名，a和符卡序号有关 非EX面关底使用 438 SetSpellCard(int a, int time, int score, "X符:XXXX"); 进入符卡模式，设置符卡宣言后右上角 符卡时间，scb，符卡名，a和符卡序号有关 未使用 439 SetSpellCard(int a, int time, int score, "X符:XXXX"); 进入符卡模式，设置符卡宣言后右上角 符卡时间，scb，符卡名，a和符卡序号有关 非… |
| 441 | int)仅在风神录(对应ins_361)使用过,为4,5,6面某些效果设置, 和415(int | 4系 单位固有属性 | 无敌类似 442 Survival() 设置符卡为时符 |
| 443 | — | 4系 单位固有属性 | 星莲船的三个时符均使用.具体效果未知 |
| 444 | int a | 4系 单位固有属性 | 当a =1的时候赋予单位flag（ins_402中的）0x04000000,a=0的是消除 |
| 445 | — | 4系 单位固有属性 | 清楚特定内存并重置boss一些参数， 除了boss1非以外，每一张非和卡都出现和,boss逃跑和死亡也会出现 |
| 446 | int a,int b | 4系 单位固有属性 | 当a =1的时候赋予单位flag（ins_402中的）0x08000000,a=0的是消除 此flag会使boss对Bomb免疫,并且由b来决定放b时的播放的动画 同时会消除单位flag（ins_402中的）0x10000000, |
| 447 | float | 4系 单位固有属性 | 设置时间倍率，1.0是正常，击破后减速可以设成0.5，咲夜时停是设成0.0 |
| 448 | int a,b,c,d | 4系 单位固有属性 | 根据难度等待x帧 |
| 449 | int a | 4系 单位固有属性 | 当a =1的时候赋予单位flag（ins_402中的）0x40000000,a=0的是消除 |
| 450 | int a)仅在地灵殿(对应ins_370 | 4系 单位固有属性 | 四面道中boss的鬼火使用过,效果不明.即使删除也没有任何影响.之后被zun遗弃 ebx+234= a |
| 451 | int a)仅在地灵殿(对应ins_371 | 4系 单位固有属性 | 四面道中2boss离场时使用.之后被zun遗弃,ebx+238= a |
| 452 | int a | 4系 单位固有属性 | 提高贴图图层a层,对时间值为0的贴图没用 |
| 453 | int a | 4系 单位固有属性 | 设置打击音效 |
| 454 | — | 4系 单位固有属性 | 显示logoenemy |
| 455 | int %A,int b | 4系 单位固有属性 | 检查第b号单位是否存活，若存活测A=1,否则A=0.单位的编号就是单位登场的顺序.main为0号， |
| 456 | float %A,float %B,int c | 4系 单位固有属性 | 将第c号单位的坐标存入A 和B |
| 457 | — | 4系 单位固有属性 | 文花帖DS新增 |
| 458 | int a | 4系 单位固有属性 | 文花帖DS新增 单个关卡的时间,a=时间,单位为帧,一般在开头就有宣称 |
| 459 | int a | 4系 单位固有属性 | 文花帖DS新增 创建一个高分圈,高分圈起始半径大小为固定值,a=高分圈缩小速度.即a值越高,收缩速度越慢 |
| 460 | float a | 4系 单位固有属性 | 文花帖DS新增 具体未知,跟分值有关.一般在DS的ecl开头设置,a的值越大分值（倍率）越高 |
| 461 | float a | 4系 单位固有属性 | 文花帖DS新增 |
| 462 | int a | 4系 单位固有属性 | 文花帖DS新增（注：灵梦大方札卡里有，不明） |
| 463 | CString | 4系 单位固有属性 | 文花帖DS新增 |
| 512 | float r | 5系 弹幕相关 | 消掉半径为r范围内的弹幕,消掉的弹幕变为最大得点 |
| 513 | float r | 5系 弹幕相关 | 消掉半径为r范围内的弹幕,不增加得点 风开始zun放弃使用rank，但是rank这个变量依旧存在于程序中且和红魔乡的增减方法相同 故以下函数仍然可以使用 |
| 514 | 弹幕编号，float a,b,c,d,e,f | 5系 弹幕相关 | 根据Rank的值512个-512比较来决定弹速 |
| 515 | 弹幕编号，float a,b,c,d,e,f,g,h,i,j | 5系 弹幕相关 | 根据Rank，和各种值来决定弹速 |
| 516 | 弹幕编号，float a,b,c,d | 5系 弹幕相关 | 未知,根据Rank决定弹速 |
| 517 | 弹幕编号，int a,b,c,d,e,f | 5系 弹幕相关 | 根据Rank值和512个-512比较来决定way数和层数 |
| 518 | 弹幕编号，int a,b,c,d,e,f,g,h,i,j | 5系 弹幕相关 | 和514类似,比较Rank，和各种值来决定way数和层数 |
| 519 | 弹幕编号，int a,b,c,d | 5系 弹幕相关 | 未知,根据内存Rank决定way数和层数 |
| 520 | %N,float x,float y | 5系 弹幕相关 | 计算 点x,y到 自机到角度并存入N中 |
| 521 | 弹幕编号，float a,b,c,d,e,f,g,h | 5系 弹幕相关 | 505的难度结合版，即如果难度为Easy 则相当于ins_505(弹幕编,a,e) |
| 522 | 弹幕编号，int a,b,c,d,e,f,g,h | 5系 弹幕相关 | 506的难度结合版，即如果难度为Easy 则相当于ins_506(弹幕编,a,e) |
| 523 | 弹幕编号，float o，float r | 5系 弹幕相关 | 以基准发弹点用极坐标的方式偏移发弹点，角度为o，半径为r。 |
| 524 | 弹幕编号，float dis | 5系 弹幕相关 | 设置发弹点。以boss为半径为dis的圆形边上发弹。 |
| 525 | 弹幕编号，float x，float y | 5系 弹幕相关 | 设置发弹基准点 |
| 526 | flout r,int color | 5系 弹幕相关 | 设置boss周围的纹理变化特性，影响半径为r，颜色为 color，对应RGB颜色， |
| 527 | int a | 5系 弹幕相关 | 执行STD背景脚本a |
| 528 | int a | 5系 弹幕相关 | 当a=1时 隐藏boss血量和 时间（是否无敌和锁时间待测试） |
| 529 | int a | 5系 弹幕相关 | 根据a赋予某种特殊效果，和534使用同一列表 534是一次性执行某种效果，而529是赋予一种属性 具体参考534 |
| 530 | int a | 5系 弹幕相关 | 封装函数，当a=1时，单位的被弹判定采用特殊方式 |
| 531 | int a | 5系 弹幕相关 | 封装函数，当a=1时，单位的体术判定采用特殊方式 |
| 532 | float r | 5系 弹幕相关 | 消掉半径为r范围内的弹幕,消掉的弹幕变为最大得点,与512还有一处不同 |
| 533 | float r | 5系 弹幕相关 | 消掉半径为r范围内的弹幕,不增加得点,与513还有一处不同，仅在前作dld（447）三面勇仪1符圈圈消蛋使用，此圈圈不会消自身的大玉 |
| 534 | int a | 5系 弹幕相关 | 根据立即执行某种效果a=0,则无 1.船长时符使用 额外参数无 2.exboss符卡中，显示飞碟击破后的分数 额外参数9985=未知（例1） 3.exboss 5卡弹幕奇美拉 激光变成光弹 额外参数无,是个完全封装好没法修改的函数 4.exboss 5卡弹幕奇美拉 光弹变成激光 额外参数无,是个完全封装好没法修改的函数 5.exboss终符恨弓激光变米蛋, 额外参数9980.0f =弹速，9981.0f=未知（例40.0f），9985=未知（例60） a =6，推测效果为飞钵子弹和线的互动相关（此由529赋予） a=7，生成ds里早苗的雷的周围的线（由529赋予） |
| 535 | int a | 5系 弹幕相关 | 未知 |
| 536 | int a | 5系 弹幕相关 | 文花帖DS新增 |
| 537 | int a,b,c,d,e,f,g,h,float i,l,k,l | 5系 弹幕相关 | DZZ新增 |
| 538 | int a,int b | 5系 弹幕相关 | DZZ新增 |
| 600 | 弹幕编号,float a,float length,float b,float width | 6系 激光相关 | 使弹幕变成激光，设置长度和宽度，a和b是开始位置的参数，一般激光设成0就行 17条爆弹那种预警线+直接生产的设置成和长度一样 若要发射曲线激光，则a,length,b 都是无关参数，设成-1.0f,曲线激光只可以设置宽度. |
| 601 | 弹幕编号,int a,int b,int c,int d, int e | 6系 激光相关 | 设置预警线持续时间a和激光的持续时间c. b和d分别是从预警线变为实际激光和激光消失过程需要的时间，e一般为0 用途未知 若发射曲线激光则，则b,c,d,都是无关参数，a是激光发射持续时间（决定其长度） e让然是迷之0 |
| 602 | 弹幕编号 | 6系 激光相关 | 普通激光的发弹函数 |
| 603 | 弹幕编号,int a | 6系 激光相关 | 发射预警线激光专用，a为激光编号，区别于弹幕编号 |
| 604 | 激光编号,float x,float y | 6系 激光相关 | 改变激光的起点为x,y |
| 605 | 激光编号,float speed,float direction | 6系 激光相关 | 赋予激光起点一个速度和方向 |
| 606 | 激光编号,float lenth | 6系 激光相关 | 改变激光的宽度为lenth |
| 607 | 激光编号,float width | 6系 激光相关 | 改变激光的宽度为width |
| 608 | 激光编号,float a | 6系 激光相关 | 改变激光的角度为a |
| 609 | 激光编号,float a | 6系 激光相关 | 赋予激光一个顺时针的角速度a |
| 610 | 激光编号 | 6系 激光相关 | 消除激光 |
| 611 | 弹幕编号 | 6系 激光相关 | 曲线激光用发弹函数 |
| 612 | float length,float width | 6系 激光相关 | 文花帖DS新增 ，沿slot 0贴图方向length x width矩形范围内消弹 |
| 613 | int a,? | 6系 激光相关 | DZZ新增 |
| 614 | int a,int b | 6系 激光相关 | DZZ新增 |
| 615 | int a,int b | 6系 激光相关 | DZZ新增 7 Debug |
| 700 | int a | 6系 激光相关 | Debug相关，我们用不到 |

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

## TH12.8 妖精大战争

- 体系：第三世代
- 指令：ecl-web.txt 未列出该作 Priw8 指令表；通常沿用相近世代/上一作格式，本文仅列变量。
- 变量：变量范围 -10000..-9909；本文列出有说明/命名记录的 92 条，未列空洞/未知项。

### TH12.8 变量

| ID | 名称 | 类型 | 访问 | 作用域 | 说明 | 文档化 | 来源 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| -10000 | [-10000] | int | 只读 | global/全局 | Random integer, very large range. | 是 | 继承自 TH10 |
| -9999.0f | [-9999] | float | 只读 | global/全局 | Random float from 0.0f to 1.0f. | 是 | 继承自 TH10 |
| -9998.0f | [-9998] | float | 只读 | global/全局 | Random float from -pi to pi. | 是 | 继承自 TH10 |
| -9997.0f | [-9997] | float | 只读 | local/敌机局部 | Final X position of the enemy. | 是 | 继承自 TH10 |
| -9996.0f | [-9996] | float | 只读 | local/敌机局部 | Final Y position of the enemy. | 是 | 继承自 TH10 |
| -9995.0f | [-9995] | float | 只读 | local/敌机局部 | Absolute X position of the enemy. | 是 | 继承自 TH10 |
| -9994.0f | [-9994] | float | 只读 | local/敌机局部 | Absolute Y position of the enemy. | 是 | 继承自 TH10 |
| -9993.0f | [-9993] | float | 只读 | local/敌机局部 | Relative X position of the enemy. | 是 | 继承自 TH10 |
| -9992.0f | [-9992] | float | 只读 | local/敌机局部 | Relative Y position of the enemy. | 是 | 继承自 TH10 |
| -9991.0f | [-9991] | float | 只读 | global/全局 | Player's X position. | 是 | 继承自 TH10 |
| -9990.0f | [-9990] | float | 只读 | global/全局 | Player's Y position. | 是 | 继承自 TH10 |
| -9989.0f | [-9989] | float | 只读 | local/敌机局部 | Angle from the enemy to the player. | 是 | 继承自 TH10 |
| -9988 | [-9988] | int | 只读 | local/敌机局部 | Time elapsed since the enemy spawned, in frames. | 是 | 继承自 TH10 |
| -9987.0f | [-9987] | float | 只读 | global/全局 | Random float from -1.0f to 1.0f. | 是 | 继承自 TH10 |
| -9986 | [-9986] | int | 只读 | global/全局 | Set to 1 by the engine when a timeout occurs. | 是 | 继承自 TH10 |
| -9985 | [-9985] | int | 读写 | local/敌机局部 | Local integer variable, inherited by spawned enemies. | 是 | 继承自 TH10 |
| -9984 | [-9984] | int | 读写 | local/敌机局部 | Local integer variable, inherited by spawned enemies. | 是 | 继承自 TH10 |
| -9983 | [-9983] | int | 读写 | local/敌机局部 | Local integer variable, inherited by spawned enemies. | 是 | 继承自 TH10 |
| -9982 | [-9982] | int | 读写 | local/敌机局部 | Local integer variable, inherited by spawned enemies. | 是 | 继承自 TH10 |
| -9981.0f | [-9981] | float | 读写 | local/敌机局部 | Local float variable, inherited by spawned enemies. | 是 | 继承自 TH10 |
| -9980.0f | [-9980] | float | 读写 | local/敌机局部 | Local float variable, inherited by spawned enemies. | 是 | 继承自 TH10 |
| -9979.0f | [-9979] | float | 读写 | local/敌机局部 | Local float variable, inherited by spawned enemies. | 是 | 继承自 TH10 |
| -9978.0f | [-9978] | float | 读写 | local/敌机局部 | Local float variable, inherited by spawned enemies. | 是 | 继承自 TH10 |
| -9977.0f | [-9977] | float | 只读 | local/敌机局部 | Same as var_-9997. | 是 | 继承自 TH10 |
| -9976.0f | [-9976] | float | 只读 | local/敌机局部 | Same as var_-9996. | 是 | 继承自 TH10 |
| -9975.0f | [-9975] | float | 只读 | local/敌机局部 | Same as var_-9995. | 是 | 继承自 TH10 |
| -9974.0f | [-9974] | float | 只读 | local/敌机局部 | Same as var_-9994. | 是 | 继承自 TH10 |
| -9973.0f | [-9973] | float | 只读 | local/敌机局部 | Same as var_-9993. | 是 | 继承自 TH10 |
| -9972.0f | [-9972] | float | 只读 | local/敌机局部 | Same as var_-9992. | 是 | 继承自 TH10 |
| -9971.0f | [-9971] | float | 只读 | local/敌机局部 | Angle of enemy's absolute movement. | 是 | 继承自 TH10 |
| -9970.0f | [-9970] | float | 只读 | local/敌机局部 | Angle of enemy's relative movement. | 是 | 继承自 TH10 |
| -9969.0f | [-9969] | float | 只读 | local/敌机局部 | Speed of enemy's absolute movement. | 是 | 继承自 TH10 |
| -9968.0f | [-9968] | float | 只读 | local/敌机局部 | Speed of enemy's relative movement. | 是 | 继承自 TH10 |
| -9967.0f | [-9967] | float | 只读 | local/敌机局部 | Distance from the origin of enemy's absolute circular movement (radius of the circle). | 是 | 继承自 TH10 |
| -9966.0f | [-9966] | float | 只读 | local/敌机局部 | Distance from the origin of enemy's relative circular movement (radius of the circle). | 是 | 继承自 TH10 |
| -9965.0f | [-9965] | float | 只读 | global/全局 | Same as var_-9991. | 是 | 继承自 TH10 |
| -9964.0f | [-9964] | float | 只读 | global/全局 | Same as var_-9990. | 是 | 继承自 TH10 |
| -9963.0f | [-9963] | float | 只读 | global/全局 | Final X position of the boss. | 是 | 继承自 TH10 |
| -9962.0f | [-9962] | float | 只读 | global/全局 | Final Y position of the boss. | 是 | 继承自 TH10 |
| -9961 | [-9961] | int | 只读 | local/敌机局部 | Is the current script on anm slot 0 of the enemy. | 是 | 继承自 TH10 |
| -9960 | [-9960] | int | 只读 | global/全局 | Numeric value of rank, ranging from -1024 to 1024. Increases over time and decreases when player bombs/dies etc. | 是 | 继承自 TH10 |
| -9959 | [-9959] | int | 只读 | global/全局 | Difficulty (E=0, N=1, H=2, L=3, EX=4) | 是 | 继承自 TH10 |
| -9958.0f | [-9958] | float | 只读 | local/敌机局部 | Final angle of enemy's movement. | 是 | 继承自 TH10 |
| -9957 | [-9957] | int | 只读 | global/全局 | Always returns 1. | 是 | 继承自 TH10 |
| -9956.0f | [-9956] | float | 只读 | local/敌机局部 | Angle to the player from enemy's absolute position. | 是 | 继承自 TH10 |
| -9955.0f | [-9955] | float | 只读 | local/敌机局部 | Angle to the player from enemy's relative position. | 是 | 继承自 TH10 |
| -9954 | [-9954] | int | 只读 | local/敌机局部 | Enemy's current HP. | 是 | 继承自 TH10 |
| -9953 | [-9953] | int | 只读 | global/全局 | Set to 1 if difficulty is easy, otherwise it's 0. | 是 | 继承自 TH10 |
| -9952 | [-9952] | int | 只读 | global/全局 | Set to 1 if difficulty is normal, otherwise it's 0. | 是 | 继承自 TH10 |
| -9951 | [-9951] | int | 只读 | global/全局 | Set to 1 if difficulty is hard, otherwise it's 0. | 是 | 继承自 TH10 |
| -9950 | [-9950] | int | 只读 | global/全局 | Set to 1 if difficulty is lunatic, otherwise it's 0. | 是 | 继承自 TH10 |
| -9949 | [-9949] | int | 读写 | global/全局 | Increased by 1 every time the player dies. | 是 | 继承自 TH11 |
| -9948 | [-9948] | int | 读写 | global/全局 | Increased by 1 every time the player bombs. | 是 | 继承自 TH11 |
| -9947 | [-9947] | int | 读写 | global/全局 | Set to 0 when the player dies, bombs, or uses a game-specific mechanic that "fails" a spell. | 是 | 继承自 TH11 |
| -9946 | [-9946] | int | 只读 | global/全局 | Amount of enemies alive (including main and MapleEnemy). | 是 | 继承自 TH11 |
| -9945 | [-9945] | int | 只读 | global/全局 | Numeric value that represents player's shottype, the first shottype is 0. | 是 | 继承自 TH11 |
| -9944.0f | [-9944] | float | 只读 | local/敌机局部 | Distance from the enemy to the player. | 是 | 继承自 TH11 |
| -9943 | [-9943] | int | 读写 | local/敌机局部 | Is the same as the I0 variable of boss 0. | 是 | 继承自 TH11 |
| -9942 | [-9942] | int | 读写 | local/敌机局部 | Is the same as the I1 variable of boss 0. | 是 | 继承自 TH11 |
| -9941 | [-9941] | int | 读写 | local/敌机局部 | Is the same as the I2 variable of boss 0. | 是 | 继承自 TH11 |
| -9940 | [-9940] | int | 读写 | local/敌机局部 | Is the same as the I3 variable of boss 0. | 是 | 继承自 TH11 |
| -9939.0f | [-9939] | float | 读写 | local/敌机局部 | Is the same as the F0 variable of boss 0. | 是 | 继承自 TH11 |
| -9938.0f | [-9938] | float | 读写 | local/敌机局部 | Is the same as the F1 variable of boss 0. | 是 | 继承自 TH11 |
| -9937.0f | [-9937] | float | 读写 | local/敌机局部 | Is the same as the F2 variable of boss 0. | 是 | 继承自 TH11 |
| -9936.0f | [-9936] | float | 读写 | local/敌机局部 | Is the same as the F3 variable of boss 0. | 是 | 继承自 TH11 |
| -9935.0f | [-9935] | float | 读写 | local/敌机局部 | Local float variable inherited by spawned enemies, just like F0-F3 and I0-I3. | 是 | 继承自 TH11 |
| -9934.0f | [-9934] | float | 读写 | local/敌机局部 | Local float variable inherited by spawned enemies, just like F0-F3 and I0-I3. | 是 | 继承自 TH11 |
| -9933.0f | [-9933] | float | 读写 | local/敌机局部 | Local float variable inherited by spawned enemies, just like F0-F3 and I0-I3. | 是 | 继承自 TH11 |
| -9932.0f | [-9932] | float | 读写 | local/敌机局部 | Local float variable inherited by spawned enemies, just like F0-F3 and I0-I3. | 是 | 继承自 TH11 |
| -9931 | [-9931] | int | 只读 | global/全局 | ID of the last spawned enemy. | 是 | 继承自 TH12 |
| -9930 | [-9930] | int | 只读 | global/全局 | Player's power (4.00 => 400) | 是 | 继承自 TH12 |
| -9929 | [-9929] | int | 只读 | global/全局 | Used in Double Spoiler, unknown. | 否/待确认 | 继承自 TH12.5 |
| -9928 | [-9928] | int | 只读 | global/全局 | Used in Double Spoiler, unknown. | 否/待确认 | 继承自 TH12.5 |
| -9927 | [-9927] | int | 只读 | global/全局 | Used in Double Spoiler, unknown. | 否/待确认 | 继承自 TH12.5 |
| -9926 | [-9926] | int | 读写 | global/全局 | Global integer variable. | 是 | 继承自 TH12.5 |
| -9925 | [-9925] | int | 读写 | global/全局 | Global integer variable. | 是 | 继承自 TH12.5 |
| -9924 | [-9924] | int | 读写 | global/全局 | Global integer variable. | 是 | 继承自 TH12.5 |
| -9923 | [-9923] | int | 读写 | global/全局 | Global integer variable. | 是 | 继承自 TH12.5 |
| -9922.0f | [-9922] | float | 读写 | global/全局 | Global float variable. | 是 | 继承自 TH12.5 |
| -9921.0f | [-9921] | float | 读写 | global/全局 | Global float variable. | 是 | 继承自 TH12.5 |
| -9920.0f | [-9920] | float | 读写 | global/全局 | Global float variable. | 是 | 继承自 TH12.5 |
| -9919.0f | [-9919] | float | 读写 | global/全局 | Global float variable. | 是 | 继承自 TH12.5 |
| -9918.0f | [-9918] | float | 读写 | global/全局 | Global float variable. | 是 | 继承自 TH12.5 |
| -9917.0f | [-9917] | float | 读写 | global/全局 | Global float variable. | 是 | 继承自 TH12.5 |
| -9916.0f | [-9916] | float | 读写 | global/全局 | Global float variable. | 是 | 继承自 TH12.5 |
| -9915.0f | [-9915] | float | 读写 | global/全局 | Global float variable. | 是 | 继承自 TH12.5 |
| -9914 | [-9914] | int | 只读 | local/敌机局部 | ID of the enemy. | 是 | 继承自 TH12.5 |
| -9913 | [-9913] | int | 只读 | global/全局 | Used in Double Spoiler, amount of photos taken. | 是 | 继承自 TH12.5 |
| -9912 | [-9912] | int | 只读 | global/全局 | Used in Double Spoiler, unknown. | 否/待确认 | 继承自 TH12.5 |
| -9911.0f | [-9911] | float | 只读 | global/全局 | Angle at which the boss moves. | 是 | 继承自 TH12.5 |
| -9910.0f | [-9910] | float | 只读 | global/全局 | Speed at which the boss moves. | 是 | 继承自 TH12.5 |
| -9909 | [-9909] | int | 只读 | local/敌机局部 | Enemy ID of the parent enemy. | 是 | 本作 |

