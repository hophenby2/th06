# TH10 东方风神录 ECL 速查

> 根据 `th062/ecl-web.txt` 中列出的 Priw8 ECL 指令表、变量表、flags/MERLIN 文档，以及本地提供的 THBWiki 文本 `th062/ecl*.txt` 整理。具体 opcode/变量主表以 Priw8 源数据为准，THBWiki 中文说明作为代际补充与交叉索引。

## 阅读说明

- `ID` 为 ECL opcode 或变量编号；`助记名` 来自 priw8 的 eclmap。
- `参数` 中前半为格式串，括号内为参数名；`S/$` 常见为整数，`f/%` 常见为浮点，`o` 常见为跳转 offset/label。
- `来源` 表示该条在 Priw8 继承链中的定义来源；第四世代大量指令会从 TH13 继承。
- 变量表只列有记录的变量；范围内未列出的编号通常为空洞或未调查。

- 返回总表：`../ecl-reference-by-game.md`
- 本文包含：TH10 对应世代 THBWiki 中文代码表、全局 flags/常量、该游戏 Priw8 指令/变量主表。

## 本游戏概览

| 游戏 | 作品 | 代际/体系 | 指令表覆盖 | 变量表覆盖 | 摘要 |
| --- | --- | --- | --- | --- | --- |
| TH10 | 东方风神录 | 第二世代 | 未列 | 有 | ecl-web.txt 未列出该作 Priw8 指令表；通常沿用相近世代/上一作格式，本文仅列变量。 变量范围 -10000..-9950；本文列出有说明/命名记录的 51 条，未列空洞/未知项。 |

## THBWiki 中文代际补充

这些表保留 THBWiki 中文页面中的签名和说明，便于和 Priw8 分游戏 opcode 表互查；同一 opcode 的英文精确定义仍见各游戏主表。

### THBWiki 第二世代 ECL

- 适用范围：风神录、地灵殿；地灵殿存在新增指令。
- 页面概述：本对照表是Zun的第二代ecl脚本的对照表,适用于风神录和地灵殿 对于其他作的参考 第一代ecl脚本红妖永花,文花帖.由于与此表差异很大,故不能作任何参考. 第三代ECL脚本对应星，文花帖ds和大战争 第四代ECL脚本对应城，天邪鬼，绀珠传 第四代中300对应此表中256,400对应此表中300，500对应此表中400，600对应此表中500，其余大体可以按顺序对照. 以下即是所有存在的ins,是读取汇编所获得的 绿色代表地灵殿中新增，风神录中不存在 红色代表功能未知，需要测试和研究 蓝色代表虽然并未完全解读，但是大体功能已经知道，且此函数用途十分有限 灰色代表是前作特殊地点使用过之后完全被抛弃的
- 抽取 opcode：95 条。

| ID | THBWiki 参数签名 | 章节 | 中文说明摘要 |
| --- | --- | --- | --- |
| 256 | "xxx", float x, float y, int life, int bonus, int item | 设置贴图，播放特效动画，创建单位 | 以相对召唤者为基准点在位置xy，创建一个单位xxx，设置血量，分数以及基本掉落。 |
| 257 | "xxx", float x, float y, int life, int bonus, int item | 设置贴图，播放特效动画，创建单位 | 在绝对位置xy，创建一个单位xxx，设置血量，分数以及基本掉落。用于boss |
| 258 | int | 设置贴图，播放特效动画，创建单位 | 选择ANM文件。一般来说0即是Bullet.anm，1即是Enemy.anm,2开始就是当面的boss相关anm |
| 259 | int slot,int a | 设置贴图，播放特效动画，创建单位 | 在相应slot上,设置单位贴图,a对应由上一个258选择的ANM文件中的SCRIPT号 若使用529则单位不会因为左右移动而改变贴图 |
| 260 | "xxx", float x, float y, int life, int bonus, int item | 设置贴图，播放特效动画，创建单位 | 和256的基本功能一样，但是移动方式为左右镜像。 |
| 261 | "xxx", float x, float y, int life, int bonus, int item | 设置贴图，播放特效动画，创建单位 | 和257的基本功能一样，但是移动方式为左右镜像。 |
| 262 | int slot,int a | 设置贴图，播放特效动画，创建单位 | 在相应slot上,设置单位贴图,a对应由上一个258选择的ANM文件中的SCRIPT号 若使用262且slot 0，则单位会因为左右移动而改变贴图, 若slot不为0，则和259无区别. |
| 263 | int a,int b | 设置贴图，播放特效动画，创建单位 | 在单位当前位置播放ANM文件a的第b个动画效果，b对应由上一个258选择的ANM文件的 script号 |
| 264 | int a,int b | 设置贴图，播放特效动画，创建单位 | 在左上角播放ANM文件a的第b个动画效果，b对应由上一个258选择的ANM文件的 script号 |
| 265 | "xxx", float x, float y, int life, int bonus, int item | 设置贴图，播放特效动画，创建单位 | 用于增员(boss存在时不执行)，其余和256一样 |
| 266 | "xxx", float x, float y, int life, int bonus, int item | 设置贴图，播放特效动画，创建单位 | 用于增员，其余和257一样 |
| 267 | "xxx", float x, float y, int life, int bonus, int item | 设置贴图，播放特效动画，创建单位 | 用于增员，其余和260一样 |
| 268 | "xxx", float x, float y, int life, int bonus, int item | 设置贴图，播放特效动画，创建单位 | 用于增员，其余和261一样 |
| 269 | int a | 设置贴图，播放特效动画，创建单位 | 在单位当前位置播放之前选择的ANM文件的第a个动画效果，a对应由上一个258选择的ANM文件的 script号 |
| 270 | "xxx", float x, float y, int life, int bonus, int item | 设置贴图，播放特效动画，创建单位 | 一种未知的创建单位函数 |
| 271 | "xxx", float x, float y, int life, int bonus, int item | 设置贴图，播放特效动画，创建单位 | 用于增员,其余和270一样 |
| 272 | int a,int b | 设置贴图，播放特效动画，创建单位 | 和263功能基本一样,只用于风神录4面潜水怪 |
| 273 | int a,int b,float c | 设置贴图，播放特效动画，创建单位 | 选择a号贴图文件的b号单位贴，旋转至c方向贴出。此贴图不会消失而是一直存在于屏幕上。（配合自带延迟消失指令的单位贴可以做出类似残影效果。） |
| 274 | int slot,int b | 设置贴图，播放特效动画，创建单位 | 发弹时(应为循环时)，在相应slot播放动作 b，b对应由上一个258选择的ANM文件的 script号 |
| 275 | int slot,int b | 设置贴图，播放特效动画，创建单位 | 播放slot预选好的动画,并且遇到anmins_64时,选择b号执行 注：anmins_64是一种switch分支结构,默认选择0号。 |
| 276 | — | 设置贴图，播放特效动画，创建单位 | 重置所有动画相关.移除flag0x10000 |
| 294 | — | 单位移动 | 将单位移动至boss的位置,此函数若在无boss时使用会导致严重误访问而爆炸 |
| 295 | — | 单位移动 | 和314成对 |
| 296 | float x,float y,float height | 单位移动 | 瞬间移动到与当前位置偏移x,y的位置,并且改变单位深度，此深度只适用于风神录四面的潜水怪 |
| 297 | float x,float y,float height) | 单位移动 | 和316成对 |
| 298 | float x,float y | 单位移动 | 6面神妈的圈圈移动上使用 |
| 299 | float x,float y | 单位移动 | 和318成对 |
| 300 | float θ,float speed,float radius,float,rspeed,float dir,float rate | 单位移动 | 使单未进行椭圆运动,曲线的极坐标（原点为单位之前的位置）(radius,θ).θ的增速为speed，radius增速为 rspeed,dir为 椭圆偏离的方向， rate为长半轴与短半轴的比例 |
| 301 | int time,int mode, float speed, float radius, float rspeed,float dir,float rate | 单位移动 | time帧之内改变单位圆周运动的参数,方式为mode.各参数参考320 |
| 302 | float θ,float speed,float radius,float,rspeed,float dir,float rate | 单位移动 | 和320成对 |
| 303 | int time,int mode, float speed, float radius, float rspeed,float dir,float rate | 单位移动 | 和321成对 |
| 304 | int a | 单位移动 | 当a =1的时候赋予单位flag（ins_402中的）0x8000,a=0的是消除 此flag会赢284和285,效果为左右翻转 |
| 305 | int time,float x1,float y1,float x2,float y2,float x3,float y3 | 单位移动 | 在time时间内将单位最终移动至点x2,y2. 期间首先向点x1,y1移动和一点时间再向 终点偏差x3,y3移动一段时间再移动至终点x2,y2. |
| 306 | int time,float x1,float y1,float x2,float y2,float x3,float y3 | 单位移动 | 和325成对 |
| 307 | — | 单位移动 | 初始化和清零移动相关参数有关 |
| 325 | — | 单位固有属性 | 移除boss移动范围限制,移除flag 512 326 ClearDrops()清除掉落 327 SetDrops(int type,int amount) 设定目标掉落道具及数量，风神录中type的含义详见下面表格（type大于11时，不掉落任何道具，是无效的type值） type 道具 type 道具 type 道具 type 道具 type 道具 type 道具 type 道具 type 道具 type 道具 type 道具 type 道具 1 小p点 2 蓝点 3 大绿点 4 大p点 5 金边蓝点（风神录）/残机碎片（地灵殿） 6 F点 7 1up 8 消弹点（+10信仰） 9 小绿点（+100信仰） 10 小p点 11 大… |
| 332 | int a | 单位固有属性 | a=0，设为boss战模式（血条，名字等），赋予单位flag0x00400000 ，a=-1，结束boss。消除单位flag0x00400000 |
| 333 | — | 单位固有属性 | boss 重置时间 334 SetNextPattern(int a，血量，时间，“阶段变量名”), 当血量和或时间达到此数值时 载入下一阶段（符卡或非符） a的作用未知 335 Invisible(int time) 无敌时间， 336 PlaySE(int)播放音效 |
| 337 | int a，int b，int c | 单位固有属性 | 震屏特效。a为持续时间（帧），bc均与震屏强度有关，都是越大震动越强，区别不明。 338 Talk（int） 读取对话，参数对应msg文件 339 AfterTalk（）对话后进行下一条 340 AfterKill（）击破后进行下一条 341 TimeOut（int a，“func”） 时间到0时进行func的内容，a作用未知 342 SetSpellCard(int a, int life, int score, "X符:XXXX"); 进入符卡模式，设置符卡宣言后右上角 符卡时间，scb，符卡名，a和符卡序号有关 EX面使用 343 EndSpellCard() 结束符卡模式 344 SetChapter(float) 设置gz… |
| 349 | %N，float a,b,c | 单位固有属性 | 根据RANK决定变量N |
| 350 | %N，float a,b,c,d,e | 单位固有属性 | 根据RANK决定变量N |
| 351 | %N，float a,b | 单位固有属性 | 根据RANK决定变量N |
| 352 | $M，int a,b,c | 单位固有属性 | 根据RANK决定变量M |
| 353 | $M，int a,b,c,d,e | 单位固有属性 | 根据RANK决定变量M |
| 354 | $M，int a,b | 单位固有属性 | 根据RANK决定变量M |
| 355 | $M,int a,b,c,d | 单位固有属性 | 根据难度将数据写入整数M中 |
| 356 | %N,float a,b,c,d | 单位固有属性 | 根据难度将数据写入浮点数N中 357 SetSpellCard(int a, int life, int score, "X符:XXXX"); 进入符卡模式，设置符卡宣言后右上角 符卡时间，scb，符卡名，a和符卡序号有关 非EX面关底使用 358 SetSpellCard(int a, int life, int score, "X符:XXXX"); 进入符卡模式，设置符卡宣言后右上角 符卡时间，scb，符卡名，a和符卡序号有关 未使用 359 SetSpellCard(int a, int life, int score, "X符:XXXX"); 进入符卡模式，设置符卡宣言后右上角 符卡时间，scb，符卡名，a和符卡序号有关 非… |
| 361 | int)仅在风神录使用过,为4,5,6面某些效果设置, 和335(int | 单位固有属性 | 无敌类似 362 Survival() 设置符卡为时符 |
| 363 | — | 单位固有属性 | 星莲船的三个时符均使用.具体效果未知 |
| 364 | int a | 单位固有属性 | 当a =1的时候赋予单位flag（ins_402中的）0x04000000,a=0的是消除 |
| 365 | — | 单位固有属性 | 清楚特定内存并重置boss一些参数， 除了boss1非以外，每一张非和卡都出现和,boss逃跑和死亡也会出现 |
| 366 | int a,int b | 单位固有属性 | 当a =1的时候赋予单位flag（ins_402中的）0x08000000,a=0的是消除 此flag会使boss对Bomb免疫,并且由b来决定放b时的播放的动画 同时会消除单位flag（ins_402中的）0x10000000, |
| 367 | float | 单位固有属性 | 设置时间倍率，1.0是正常，击破后减速可以设成0.5，咲夜时停是设成0.0 |
| 368 | int a,b,c,d | 单位固有属性 | 根据难度等待x帧 |
| 369 | int a | 单位固有属性 | 当a =1的时候赋予单位flag（ins_402中的）0x08000000,a=0的是消除 |
| 370 | int a | 单位固有属性 | 仅在地灵殿四面道中boss的鬼火使用过,效果不明.即使删除也没有任何影响.之后被zun遗弃 ebx+11c= a |
| 412 | int a, b,float c,d,e,f,g,h | 激光相关函数和移动类似，很多是成对的 | 激光相关 发射激光，a,b是402参数，表示将哪种子弹的贴图拉伸成激光；c角度，d速度，f长度，g存活时间，h宽度 |
| 413 | int a b,c float d,e,f int g,h,i,j float k,int l | 激光相关函数和移动类似，很多是成对的 | 发射预警线激光，a为此激光的弹幕编号，b，c为402参数，d为角度，e无用（猜测），f为长度，g，h，i，j为预警线激光四个阶段的时间，分别为预警线阶段、激光产生变粗直到指定宽度阶段、激光持续阶段和激光变细消失阶段，k为激光宽度。 |
| 414 | int a, float b,c | 激光相关函数和移动类似，很多是成对的 | 激光相关 |
| 415 | int a, float b,c | 激光相关函数和移动类似，很多是成对的 | 激光相关 |
| 416 | int a,float b | 激光相关函数和移动类似，很多是成对的 | 激光相关 |
| 417 | int a,float b | 激光相关函数和移动类似，很多是成对的 | 激光相关 |
| 418 | int a,float b | 激光相关函数和移动类似，很多是成对的 | 激光相关 |
| 419 | int a,float b | 激光相关函数和移动类似，很多是成对的 | 激光相关 |
| 420 | float r | 激光相关函数和移动类似，很多是成对的 | 消掉半径为r范围内的弹幕,消掉的弹幕变为最大得点 |
| 421 | float r | 激光相关函数和移动类似，很多是成对的 | 消掉半径为r范围内的弹幕,不增加得点 船开始zun放弃使用rank，但是rank这个变量依旧存在于程序中且和红魔乡的增减方法相同 故以下函数仍然可以使用 RANK =[474C98] |
| 422 | 弹幕编号，float a,b,c,d,e,f | 激光相关函数和移动类似，很多是成对的 | 根据Rank的值512个-512比较来决定弹速 |
| 423 | 弹幕编号，float a,b,c,d,e,f,g,h,i,j | 激光相关函数和移动类似，很多是成对的 | 根据Rank，和各种值来决定弹速 |
| 424 | 弹幕编号，float a,b,c,d | 激光相关函数和移动类似，很多是成对的 | 未知,根据Rank决定弹速 |
| 425 | 弹幕编号，int a,b,c,d,e,f | 激光相关函数和移动类似，很多是成对的 | 根据Rank值和512个-512比较来决定way数和层数 |
| 426 | 弹幕编号，int a,b,c,d,e,f,g,h,i,j | 激光相关函数和移动类似，很多是成对的 | 和514类似,比较Rank，和各种值来决定way数和层数 |
| 427 | 弹幕编号，int a,b,c,d | 激光相关函数和移动类似，很多是成对的 | 未知,根据内存Rank决定way数和层数 |
| 428 | int a b ,float c,d,e f,g,h | 激光相关函数和移动类似，很多是成对的 | 激光相关 |
| 429 | int a b,c float c,d,e, int f,g,h,i, float j,int k | 激光相关函数和移动类似，很多是成对的 | 激光相关 |
| 430 | int a, float b,c | 激光相关函数和移动类似，很多是成对的 | 激光相关 |
| 431 | int a,int b,float c,d,e,f,g,h | 激光相关函数和移动类似，很多是成对的 | 和412成对 |
| 432 | int a b,c float c,d,e, int f,g,h,i, float j,int k | 激光相关函数和移动类似，很多是成对的 | 激光相关 和413成对 |
| 433 | int a b ,float c,d,e f,g,h | 激光相关函数和移动类似，很多是成对的 | 激光相关 和428成对 |
| 434 | int a b,c float c,d,e, int f,g,h,i, float j,int k | 激光相关函数和移动类似，很多是成对的 | 激光相关 和429成对 |
| 435 | 弹幕编号，float a,b,c,d,e,f,g,h | 激光相关函数和移动类似，很多是成对的 | 405的难度结合版，a和e对应e难度，b和f对应n难度，以此类推 |
| 436 | 弹幕编号，int a,b,c,d,e,f,g,h | 激光相关函数和移动类似，很多是成对的 | 406的难度结合版，a和e对应e难度，b和f对应n难度，以此类推 |
| 437 | 弹幕编号，float o，float r | 激光相关函数和移动类似，很多是成对的 | 以基准发弹点用极坐标的方式偏移发弹点，角度为o，半径为r。 |
| 438 | 弹幕编号，float dis | 激光相关函数和移动类似，很多是成对的 | 设置发弹点。以boss为半径为dis的圆形边上发弹。 |
| 439 | 弹幕编号，float x，float y | 激光相关函数和移动类似，很多是成对的 | 设置发弹基准点 |
| 440 | flout r,int color | 激光相关函数和移动类似，很多是成对的 | 设置boss周围的纹理变化特性，影响半径为r，颜色为 color，对应RGB颜色， |
| 441 | int a | 激光相关函数和移动类似，很多是成对的 | 执行STD脚本A |
| 442 | int | 激光相关函数和移动类似，很多是成对的 | 隐藏boss血条以及时间（不使boss无敌，也不锁时间，只是不显示血条和时间） |
| 443 | int a | 激光相关函数和移动类似，很多是成对的 | 主要用于某些特殊攻击模式时启用，作为zun的补充函数 补充函数变和449共用一套 a=0时无效果 在DLD 小五1符激光使用了1， 猫车怨灵使用了2,3 4(2和4实际有449调用) 3的效果是是含有flag1024的单位的-9984的值变为1 4的效果是 删除含有flag1024的单位的flag1024，并赋予flag256 地底太阳吸引使用了5,这三个在本作中是否有效需要测试 恋恋则使用了 6-12，其中6,9,11是由449调用 |
| 444 | int a | 激光相关函数和移动类似，很多是成对的 | 封装函数，当a=1时，单位的被弹判定采用特殊方式 |
| 445 | int a | 激光相关函数和移动类似，很多是成对的 | 封装函数，当a=1时，单位的体术判定采用特殊方式 |
| 446 | float r | 激光相关函数和移动类似，很多是成对的 | 消掉半径为r范围内的弹幕,消掉的弹幕变为最大得点,与421还有一处不同 |
| 447 | float r | 激光相关函数和移动类似，很多是成对的 | 消掉半径为r范围内的弹幕,不增加得点,与421还有一处不同，仅在dld三面勇仪1符圈圈消弹使用，此圈圈不会消自身的大玉 |
| 448 | int a | 激光相关函数和移动类似，很多是成对的 | 3面boss二非阴阳玉使用 |
| 449 | int a | 激光相关函数和移动类似，很多是成对的 | 类似443， 立即执行一些特殊函数，具体参考443 |
| 450 | int a | 激光相关函数和移动类似，很多是成对的 | 仅仅在猫车的怨灵使用 |

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

## TH10 东方风神录

- 体系：第二世代
- 指令：ecl-web.txt 未列出该作 Priw8 指令表；通常沿用相近世代/上一作格式，本文仅列变量。
- 变量：变量范围 -10000..-9950；本文列出有说明/命名记录的 51 条，未列空洞/未知项。

### TH10 变量

| ID | 名称 | 类型 | 访问 | 作用域 | 说明 | 文档化 | 来源 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| -10000 | [-10000] | int | 只读 | global/全局 | Random integer, very large range. | 是 | 本作 |
| -9999.0f | [-9999] | float | 只读 | global/全局 | Random float from 0.0f to 1.0f. | 是 | 本作 |
| -9998.0f | [-9998] | float | 只读 | global/全局 | Random float from -pi to pi. | 是 | 本作 |
| -9997.0f | [-9997] | float | 只读 | local/敌机局部 | Final X position of the enemy. | 是 | 本作 |
| -9996.0f | [-9996] | float | 只读 | local/敌机局部 | Final Y position of the enemy. | 是 | 本作 |
| -9995.0f | [-9995] | float | 只读 | local/敌机局部 | Absolute X position of the enemy. | 是 | 本作 |
| -9994.0f | [-9994] | float | 只读 | local/敌机局部 | Absolute Y position of the enemy. | 是 | 本作 |
| -9993.0f | [-9993] | float | 只读 | local/敌机局部 | Relative X position of the enemy. | 是 | 本作 |
| -9992.0f | [-9992] | float | 只读 | local/敌机局部 | Relative Y position of the enemy. | 是 | 本作 |
| -9991.0f | [-9991] | float | 只读 | global/全局 | Player's X position. | 是 | 本作 |
| -9990.0f | [-9990] | float | 只读 | global/全局 | Player's Y position. | 是 | 本作 |
| -9989.0f | [-9989] | float | 只读 | local/敌机局部 | Angle from the enemy to the player. | 是 | 本作 |
| -9988 | [-9988] | int | 只读 | local/敌机局部 | Time elapsed since the enemy spawned, in frames. | 是 | 本作 |
| -9987.0f | [-9987] | float | 只读 | global/全局 | Random float from -1.0f to 1.0f. | 是 | 本作 |
| -9986 | [-9986] | int | 只读 | global/全局 | Set to 1 by the engine when a timeout occurs. | 是 | 本作 |
| -9985 | [-9985] | int | 读写 | local/敌机局部 | Local integer variable, inherited by spawned enemies. | 是 | 本作 |
| -9984 | [-9984] | int | 读写 | local/敌机局部 | Local integer variable, inherited by spawned enemies. | 是 | 本作 |
| -9983 | [-9983] | int | 读写 | local/敌机局部 | Local integer variable, inherited by spawned enemies. | 是 | 本作 |
| -9982 | [-9982] | int | 读写 | local/敌机局部 | Local integer variable, inherited by spawned enemies. | 是 | 本作 |
| -9981.0f | [-9981] | float | 读写 | local/敌机局部 | Local float variable, inherited by spawned enemies. | 是 | 本作 |
| -9980.0f | [-9980] | float | 读写 | local/敌机局部 | Local float variable, inherited by spawned enemies. | 是 | 本作 |
| -9979.0f | [-9979] | float | 读写 | local/敌机局部 | Local float variable, inherited by spawned enemies. | 是 | 本作 |
| -9978.0f | [-9978] | float | 读写 | local/敌机局部 | Local float variable, inherited by spawned enemies. | 是 | 本作 |
| -9977.0f | [-9977] | float | 只读 | local/敌机局部 | Same as var_-9997. | 是 | 本作 |
| -9976.0f | [-9976] | float | 只读 | local/敌机局部 | Same as var_-9996. | 是 | 本作 |
| -9975.0f | [-9975] | float | 只读 | local/敌机局部 | Same as var_-9995. | 是 | 本作 |
| -9974.0f | [-9974] | float | 只读 | local/敌机局部 | Same as var_-9994. | 是 | 本作 |
| -9973.0f | [-9973] | float | 只读 | local/敌机局部 | Same as var_-9993. | 是 | 本作 |
| -9972.0f | [-9972] | float | 只读 | local/敌机局部 | Same as var_-9992. | 是 | 本作 |
| -9971.0f | [-9971] | float | 只读 | local/敌机局部 | Angle of enemy's absolute movement. | 是 | 本作 |
| -9970.0f | [-9970] | float | 只读 | local/敌机局部 | Angle of enemy's relative movement. | 是 | 本作 |
| -9969.0f | [-9969] | float | 只读 | local/敌机局部 | Speed of enemy's absolute movement. | 是 | 本作 |
| -9968.0f | [-9968] | float | 只读 | local/敌机局部 | Speed of enemy's relative movement. | 是 | 本作 |
| -9967.0f | [-9967] | float | 只读 | local/敌机局部 | Distance from the origin of enemy's absolute circular movement (radius of the circle). | 是 | 本作 |
| -9966.0f | [-9966] | float | 只读 | local/敌机局部 | Distance from the origin of enemy's relative circular movement (radius of the circle). | 是 | 本作 |
| -9965.0f | [-9965] | float | 只读 | global/全局 | Same as var_-9991. | 是 | 本作 |
| -9964.0f | [-9964] | float | 只读 | global/全局 | Same as var_-9990. | 是 | 本作 |
| -9963.0f | [-9963] | float | 只读 | global/全局 | Final X position of the boss. | 是 | 本作 |
| -9962.0f | [-9962] | float | 只读 | global/全局 | Final Y position of the boss. | 是 | 本作 |
| -9961 | [-9961] | int | 只读 | local/敌机局部 | Is the current script on anm slot 0 of the enemy. | 是 | 本作 |
| -9960 | [-9960] | int | 只读 | global/全局 | Numeric value of rank, ranging from -1024 to 1024. Increases over time and decreases when player bombs/dies etc. | 是 | 本作 |
| -9959 | [-9959] | int | 只读 | global/全局 | Difficulty (E=0, N=1, H=2, L=3, EX=4) | 是 | 本作 |
| -9958.0f | [-9958] | float | 只读 | local/敌机局部 | Final angle of enemy's movement. | 是 | 本作 |
| -9957 | [-9957] | int | 只读 | global/全局 | Always returns 1. | 是 | 本作 |
| -9956.0f | [-9956] | float | 只读 | local/敌机局部 | Angle to the player from enemy's absolute position. | 是 | 本作 |
| -9955.0f | [-9955] | float | 只读 | local/敌机局部 | Angle to the player from enemy's relative position. | 是 | 本作 |
| -9954 | [-9954] | int | 只读 | local/敌机局部 | Enemy's current HP. | 是 | 本作 |
| -9953 | [-9953] | int | 只读 | global/全局 | Set to 1 if difficulty is easy, otherwise it's 0. | 是 | 本作 |
| -9952 | [-9952] | int | 只读 | global/全局 | Set to 1 if difficulty is normal, otherwise it's 0. | 是 | 本作 |
| -9951 | [-9951] | int | 只读 | global/全局 | Set to 1 if difficulty is hard, otherwise it's 0. | 是 | 本作 |
| -9950 | [-9950] | int | 只读 | global/全局 | Set to 1 if difficulty is lunatic, otherwise it's 0. | 是 | 本作 |

