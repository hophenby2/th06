# TH14.3 弹幕天邪鬼 ECL 速查

> 根据 `th062/ecl-web.txt` 中列出的 Priw8 ECL 指令表、变量表、flags/MERLIN 文档，以及本地提供的 THBWiki 文本 `th062/ecl*.txt` 整理。具体 opcode/变量主表以 Priw8 源数据为准，THBWiki 中文说明作为代际补充与交叉索引。

## 阅读说明

- `ID` 为 ECL opcode 或变量编号；`助记名` 来自 priw8 的 eclmap。
- `参数` 中前半为格式串，括号内为参数名；`S/$` 常见为整数，`f/%` 常见为浮点，`o` 常见为跳转 offset/label。
- `来源` 表示该条在 Priw8 继承链中的定义来源；第四世代大量指令会从 TH13 继承。
- 变量表只列有记录的变量；范围内未列出的编号通常为空洞或未调查。

- 返回总表：`../ecl-reference-by-game.md`
- 本文包含：TH14.3 对应世代 THBWiki 中文代码表、全局 flags/常量、该游戏 Priw8 指令/变量主表。

## 本游戏概览

| 游戏 | 作品 | 代际/体系 | 指令表覆盖 | 变量表覆盖 | 摘要 |
| --- | --- | --- | --- | --- | --- |
| TH14.3 | 弹幕天邪鬼 | 第四世代 | 有 | 有 | 普通指令 319 条；已说明 257/319。主要分组：系统/流程/栈/算术 / System；敌机创建与 ANM 管理 / Enemy creation and ANM script management；移动管理 / Movement management；敌机属性与杂项 / Enemy property management and other miscellaneous things；子弹创建与删除 / Bullet creation and deletion；激光创建 / Laser creation；敌机交互 / Enemy interaction；调试 / Debug；游戏特有 / Game specific。 变量范围 -10000..-9907；本文列出有说明/命名记录的 94 条，未列空洞/未知项。 |

## THBWiki 中文代际补充

这些表保留 THBWiki 中文页面中的签名和说明，便于和 Priw8 分游戏 opcode 表互查；同一 opcode 的英文精确定义仍见各游戏主表。

### THBWiki 第四世代 ECL

- 适用范围：神灵庙之后的整数作与小数作；页面标注辉针城、天邪鬼、绀珠传、天空璋、噩梦日记、鬼形兽等新增差异。
- 页面概述：本对照表是ZUN的第四代ECL脚本的对照表,适用于神之后的所有作品 红色代表功能未知，需要测试和研究 蓝色代表虽然并未完全解读，但是大体功能已经知道，且此函数用途十分有限 灰色代表是前作特殊地点使用过之后完全被抛弃的 棕色部分是辉针城新增 青色部分是天邪鬼新增 绿色部分是绀珠传新增 紫色部分是天空璋新增 洋红部分是鬼形兽新增
- 抽取 opcode：209 条。

| ID | THBWiki 参数签名 | 章节 | 中文说明摘要 |
| --- | --- | --- | --- |
| 300 | "xxx", float x, float y, int life, int bonus, int item | 3系 设置贴图，播放特效动画，创建单位 | 以相对召唤者为基准点在位置xy，创建一个单位xxx，设置血量，分数以及基本掉落。 |
| 301 | "xxx", float x, float y, int life, int bonus, int item | 3系 设置贴图，播放特效动画，创建单位 | 在绝对位置xy，创建一个单位xxx，设置血量，分数以及基本掉落。用于boss |
| 302 | int | 3系 设置贴图，播放特效动画，创建单位 | 选择ANM文件。一般来说0即是Bullet.anm，1即是Enemy.anm,2开始就是当面的boss相关anm |
| 303 | int slot,int a | 3系 设置贴图，播放特效动画，创建单位 | 在相应slot上,设置单位贴图,a对应由上一个302选择的ANM文件中的SCRIPT号 一个单位拥有若干slot，每个slot对应一个SCRIPT，显示单位时所有slot会同时参与显示（参考神灵庙四面邪魂球，设置了多个slot以实现子弹前景和特效背景同时显示） 若使用529则单位不会因为左右移动而改变贴图 |
| 304 | "xxx", float x, float y, int life, int bonus, int item | 3系 设置贴图，播放特效动画，创建单位 | 和300的基本功能一样，但是移动方式为左右镜像。 |
| 305 | "xxx", float x, float y, int life, int bonus, int item | 3系 设置贴图，播放特效动画，创建单位 | 和301的基本功能一样，但是移动方式为左右镜像。 |
| 306 | int slot,int a | 3系 设置贴图，播放特效动画，创建单位 | 在相应slot上,设置单位贴图,a对应由上一个302选择的ANM文件中的SCRIPT号 若使用306且slot 0，则单位会因为左右移动而改变贴图 a为静止贴图，a+1，a+2为向左，右走，a+3，a+4为左面回来，右面回来 若slot不为0，则和303无区别. |
| 307 | int a,int b | 3系 设置贴图，播放特效动画，创建单位 | 在单位当前位置播放ANM文件a的第b个动画效果，b对应由上一个302选择的ANM文件的 script号 |
| 308 | int a,int b | 3系 设置贴图，播放特效动画，创建单位 | 在左上角播放ANM文件a的第b个动画效果，b对应由上一个302选择的ANM文件的 script号 |
| 309 | "xxx", float x, float y, int life, int bonus, int item | 3系 设置贴图，播放特效动画，创建单位 | 用于增员(boss存在时不执行)，其余和300一样 |
| 310 | "xxx", float x, float y, int life, int bonus, int item | 3系 设置贴图，播放特效动画，创建单位 | 用于增员，其余和301一样 |
| 311 | "xxx", float x, float y, int life, int bonus, int item | 3系 设置贴图，播放特效动画，创建单位 | 用于增员，其余和304一样 |
| 312 | "xxx", float x, float y, int life, int bonus, int item | 3系 设置贴图，播放特效动画，创建单位 | 用于增员，其余和305一样 |
| 313 | int a | 3系 设置贴图，播放特效动画，创建单位 | 在单位当前位置播放之前选择的ANM文件的第a个动画效果，a对应由上一个302选择的ANM文件的 script号 |
| 314 | int a, b | 3系 设置贴图，播放特效动画，创建单位 | 315(int a, b) |
| 316 | int a, b | 3系 设置贴图，播放特效动画，创建单位 | 播放boss施法动作 |
| 317 | int a, b | 3系 设置贴图，播放特效动画，创建单位 | 318() 重置动画相关,移除单位作用移动时贴图变化的flag |
| 319 | int slot,float b | 3系 设置贴图，播放特效动画，创建单位 | 旋转在相应slot的贴图至b方向。 |
| 320 | int slot,float x,float y | 3系 设置贴图，播放特效动画，创建单位 | 用于改变slot位置贴图的位置 x和y |
| 321 | "MapleEnemy", 0, 0, 100, 1000, 0 | 3系 设置贴图，播放特效动画，创建单位 | 插入mapleenemy专用 |
| 322 | int a,int b | 3系 设置贴图，播放特效动画，创建单位 | 323(int a,int b) 设置单位死亡效果，a为ANM编号，b为script号 |
| 324 | — | 3系 设置贴图，播放特效动画，创建单位 | 325 -333 以及335第一个参数一定是slot |
| 325 | int slot,int R,int G,int B | 3系 设置贴图，播放特效动画，创建单位 | 设置贴图颜色,若RGB为255 255 255（白），则维持原颜色 |
| 326 | int slot,int time,int mode,int R,int G,int B | 设置贴图颜色,若RGB为255 255 255（白），则维持原颜色 | time帧内以mode方式改变单位位于slot的贴图颜色为rgb |
| 327 | int slot,int a | 设置贴图颜色,若RGB为255 255 255（白），则维持原颜色 | 改变单位位于slot的贴图的不透明度为alpha. |
| 328 | int slot,int time,int mode,int alpha | 设置贴图颜色,若RGB为255 255 255（白），则维持原颜色 | time帧内改变单位位于slot的贴图的不透明度为alpha. |
| 329 | int slot,float lengthrate,float widthrate | 设置贴图颜色,若RGB为255 255 255（白），则维持原颜色 | 设置单位位于slot的贴图的大小比例,1.0f为正常大小，替换anmins里的402等anmins设置的倍数 |
| 330 | int slot,int time,int mode,float lengthrate,float widthrate | 设置贴图颜色,若RGB为255 255 255（白），则维持原颜色 | time帧内改变单位位于slot的贴图的大小比例为lengthrate,float widthrate. |
| 331 | int slot,int a | 设置贴图颜色,若RGB为255 255 255（白），则维持原颜色 | 332(int slot,int a,b,c) |
| 333 | int slot,int a,b.float c,d | 设置贴图颜色,若RGB为255 255 255（白），则维持原颜色 | 334(int a) 播放单位的动画效果，神灵庙娘娘的邪魂球附近的雷电效果使用 |
| 335 | int slot,float lengthrate,float widthrate | 设置贴图颜色,若RGB为255 255 255（白），则维持原颜色 | 设置位于slot的贴图的大小比例,1.0f为正常大小，与anmins里的402等anmins设置的倍数叠加 336（int int） 337（int int float float float） 337（int int） |
| 414 | — | 4系 单位移动 | 将单位移动至boss的位置,此函数若在无boss时使用会导致严重误访问而爆炸 |
| 415 | — | 4系 单位移动 | 和414成对 |
| 416 | float x,float y,float height | 4系 单位移动 | 瞬间移动到与当前位置偏移x,y的位置,并且改变单位深度，此深度只适用于风神录（296）四面的潜水怪 |
| 417 | float x,float y,float height) | 4系 单位移动 | 和416成对 |
| 418 | float x,float y | 4系 单位移动 | 仅在前作FSL（298）6面神妈的圈圈移动上使用 |
| 419 | float x,float y | 4系 单位移动 | 和418成对 |
| 420 | float θ,float speed,float radius,float,rspeed,float dir,float rate | 4系 单位移动 | 使单位进行椭圆运动,曲线的极坐标（原点为单位之前的位置）(radius,θ) θ的增速为speed，radius增速为 rspeed,dir为 椭圆偏离的方向，rate为长半轴与短半轴的比例 |
| 421 | int time,int mode, float speed, float radius, float rspeed,float dir,float rate | 4系 单位移动 | time帧之内改变单位圆周运动的参数,方式为mode.各参数参考420 |
| 422 | float θ,float speed,float radius,float,rspeed,float dir,float rate | 4系 单位移动 | 和420成对 |
| 423 | int time,int mode, float speed, float radius, float rspeed,float dir,float rate | 4系 单位移动 | 和421成对 |
| 424 | int a | 4系 单位移动 | 当a =1的时候赋予单位某flag(参考flag表),a=0的是消除 此flag会影响404和405等ins,效果为左右翻转 |
| 425 | int time,float x1,float y1,float x2,float y2,float x3,float y3 | 4系 单位移动 | 在time时间内将单位最终移动至点x2,y2. 期间首先向点x1,y1移动和一点时间再向 终点偏差x3,y3移动一段时间再移动至终点x2,y2. 注:(假设目前坐标为(x0,y0))运动轨迹实际是由(x0,y0)到(x2,y2)的贝塞尔曲线; 曲线的P1坐标为((x1-x0)*1/3,(y1-y0)*1/3);P2坐标为(-(x3-x2)*1/3+x2,-(y3-y2)*1/3+x2) (因此(x3,y3)这个点的坐标实际上是向左x正方向,向上y正方向) 2un你为啥要把坐标先乘上1/3啊,为啥坐标倒着的啊 |
| 426 | int time,float x1,float y1,float x2,float y2,float x3,float y3 | 4系 单位移动 | 和425成对 |
| 427 | — | 4系 单位移动 | 初始化和清零移动相关参数 |
| 428 | int | 4系 单位移动 | 404的无视左右翻转版 |
| 429 | int | 4系 单位移动 | 405的无视左右翻转版 |
| 430 | int | 4系 单位移动 | 406的无视左右翻转版 |
| 431 | int | 4系 单位移动 | 无视左右翻转版 |
| 432 | int | 4系 单位移动 | 未知 |
| 433 | int | 4系 单位移动 | 未知 |
| 434 | int a,int b,int c ,float x,float y | 4系 单位移动 | 未知移动函数 |
| 435 | int a,int b,int c ,float x,float y | 4系 单位移动 | 和434成对 |
| 436 | int time,int mode,float x,float y | 4系 单位移动 | 401的无视左右翻转版 |
| 437 | int time,int mode,float x,float y | 4系 单位移动 | 403的无视左右翻转版 |
| 438 | int a,int b,int c ,float x,float y | 4系 单位移动 | 434的无视左右翻转版 |
| 439 | int a,int b,int c ,float x,float y); 435的无视左右翻转版 440(float | 4系 单位移动 | 441(int time,int mode,float dir) time帧后移动方向角增加dir，方式为mode |
| 442 | float | 4系 单位移动 | 443(int time,int mode,float dir) time帧后移动方向角增加dir，方式为mode |
| 444 | float | 4系 单位移动 | 445(int time,int mode,float s) time帧内速度增加至s，方式为mode |
| 446 | float | 4系 单位移动 | 447(int time,int mode,float s) time帧内速度增加至s，方式为mode |
| 500 | float width,float height | 5系 单位固有属性 | 目标被弹判定 |
| 501 | float width,float height | 5系 单位固有属性 | 目标体术判定 |
| 502 | int flag | 5系 单位固有属性 | 设置单位的一些特定参数,a为2个4字节的开关参数0000000000000000 详细参考下方FLAG表 |
| 503 | int a | 5系 单位固有属性 | 取消502设置的参数,和502刚好相反 |
| 504 | float x,float y,float m,float n | 5系 单位固有属性 | 限制boss的移动范围，以x,y为基准+- n 和m的范围 |
| 505 | — | 5系 单位固有属性 | 移除移动范围限制 |
| 506 | — | 5系 单位固有属性 | 清除掉落 |
| 507 | int type,int amount | 5系 单位固有属性 | 目标掉落道具及数量 1.p点 2蓝点 3.大p 4.残碎片 5残机，6B碎片 7Bomb 8大F 9小最大得点，获得时无音效，每个增加2最大得点， 10.中最大得点，获取时有音效，每个增加2最大得点.11.中最大得点，获取时有音效，每个增加20最大得点. 12.B碎片(参与hzc收点系统的循环) 12.30得点 13.40得点 14.50得点 15.B碎片 16~22.固定狼獭鹰B残红蓝 23~29.七个隐藏灵 30~32.变色狼獭鹰 33.变色随机初始 34.不明灵状特效 |
| 508 | float width,float height | 5系 单位固有属性 | 设置掉落区域 |
| 509 | — | 5系 单位固有属性 | 掉落所有道具 |
| 510 | int type) 设置目标基本掉落(相当于ins_300的最后一个参数 | 5系 单位固有属性 | ，数量是1. |
| 511 | int life) 更改单位血量(总血量和当前血量 | 5系 单位固有属性 | 512(int a) 设为boss战模式（血条，名字等）并设置boss编号为a，a必须从0开始编号，否则爆炸（。a=-1，结束boss。 |
| 513 | — | 5系 单位固有属性 | 重置时间 |
| 514 | int slot，int hp，int time, string name | 5系 单位固有属性 | , 在slot处插入一个中断,使得当boss血量和或时间达到此数值时 载入下一阶段（符卡或非符） |
| 515 | int time | 5系 单位固有属性 | 无敌时间， |
| 516 | int index_SE | 5系 单位固有属性 | 播放音效 |
| 517 | int a，int b，int c | 5系 单位固有属性 | 震屏特效。a：持续时间（帧），b：震动强度从b逐渐减小到0，c：震动强度从0逐渐增加到c。 |
| 518 | int nMSG | 5系 单位固有属性 | 读取对话，参数对应msg文件,同时执行525 |
| 519 | — | 5系 单位固有属性 | 对话后进行下一条 |
| 520 | — | 5系 单位固有属性 | 击破后进行下一条 |
| 521 | int a,string func | 5系 单位固有属性 | 时间到0时进行func的内容，a作用未知 |
| 522 | int a, int time, int score, string spellName | 5系 单位固有属性 | 进入符卡模式，设置符卡宣言后右上角 符卡时间，scb，符卡名，a和符卡序号有关 Ex面使用 在tkz后参数变为a,scbDec,anmSerial,具体见ins_539 |
| 523 | — | 5系 单位固有属性 | 结束符卡模式 |
| 524 | int ch | 5系 单位固有属性 | 设置章节数,影响即将出现的符卡立绘,背景以及左上角boss的名字 在gzz里设置的结算点，影响全局变量[-9905] |
| 525 | — | 5系 单位固有属性 | 清除所有单位，有某些flag的不会被清除. |
| 526 | float | 5系 单位固有属性 | 设置弹幕生成保护范围（距离）自机在此范围内时不发弹 |
| 527 | int a, float b, int c | 5系 单位固有属性 | 设置血条上的标记点，a是标记序号，b是血量比例，c是RGB值 血量比例以5000为基数，从12点方向顺时针开始算，与血量无关 528 SetSpellCard(int a, int life, int score, string spellName); 进入符卡模式，设置符卡宣言后右上角 符卡时间，scb，符卡名，a和符卡序号有关 未使用 RANK一直存在于游戏程序中，收点+rank miss减rank |
| 529 | float& N，float a,float b,float c | 5系 单位固有属性 | 根据RANK决定变量N（此指令在锦上京中被移除） |
| 530 | float& N，float a,float b,float c,float d,float e | 5系 单位固有属性 | 根据RANK决定变量N（此指令在锦上京中被移除） |
| 531 | float& N，float a,float b | 5系 单位固有属性 | 根据RANK决定变量N（此指令在锦上京中被移除） |
| 532 | int& M，int a,int b,int c | 5系 单位固有属性 | 根据RANK决定变量M（此指令在锦上京中被移除） |
| 533 | int& M，int a,int b,int c,int d,int e | 5系 单位固有属性 | 根据RANK决定变量M（此指令在锦上京中被移除） |
| 534 | int& M，int a,int b | 5系 单位固有属性 | 根据RANK决定变量M（此指令在锦上京中被移除） |
| 535 | int& M,int a,int b,int c,int d | 5系 单位固有属性 | 根据难度将数据写入整数M中(在锦上京中为529） |
| 536 | float& N,float a,float b,float c,float d | 5系 单位固有属性 | 根据难度将数据写入浮点数N中(在锦上京中为530） |
| 537 | int a, int time, int score, string spellName | 5系 单位固有属性 | (在锦上京中为531） 进入符卡模式，设置符卡宣言后右上角 符卡时间，scb，符卡名，a和符卡序号有关 非ex面关底使用 |
| 538 | int a, int time, int score, string spellName | 5系 单位固有属性 | (在锦上京中为532） 进入符卡模式，设置符卡宣言后右上角 符卡时间，scb，符卡名，a和符卡序号有关 HZC中未使用. |
| 539 | int a, int timeScbDec, int score, string spellName | 5系 单位固有属性 | (在锦上京中为533） 进入符卡模式，设置符卡宣言后右上角 符卡时间，scb，符卡名，a和符卡序号有关 非ex面道中使用 在tkz后参数变为a,scbDec,anmSerial 其中a与符卡序号有关,timeScbDec为scb降低到0的时间参数,约4/3(timeScbDec-300)帧后scb降低到0,具体为每帧执行: curSCB-=(maxSCB-maxSCB>>2)/(timeScbDec-300),curSCB-=curSCB%10,其中curSCB为当前SCB,maxSCB为硬编码的符卡分数 anmSerial为硬编码的符卡背景/立绘参数,为0,1时分别对应关底/道中的符卡背景/立绘 |
| 540 | int)设置剩余阶段数(左上角的星星数 | 5系 单位固有属性 | (在锦上京中为534） |
| 541 | int)仅在风神录(对应ins_361 | 5系 单位固有属性 | 使用过,为4,5,6面某些效果设置,效果不明.之后被zun遗弃(在锦上京中为535） |
| 542 | — | 5系 单位固有属性 | 设置符卡为时符（符卡分始终维持最大值，此指令在锦上京为536） |
| 543 | — | 5系 单位固有属性 | 某些时符使用(在锦上京中为537 |
| 544 | int a | 5系 单位固有属性 | (在锦上京中为538） 当a=1时赋予单位某flag(参考下方flag表),a=0时取消 雷鼓的使魔们使用 |
| 545 | — | 5系 单位固有属性 | (在锦上京中为539） 重置boss一些参数，除了boss1非以外，每一张非和卡都出现和,boss逃跑和死亡也会出现 |
| 546 | int a,int b | 5系 单位固有属性 | (在锦上京中为540） 当a =1的时候赋予单位某flag,a=0的是消除 此flag会使boss对Bomb免疫,并且由b来决定放b时的播放的动画 同时会消除某单位flag 具体参照下方flag表 |
| 547 | float gameSpeed | 5系 单位固有属性 | 设置时间倍率，1.0是正常，击破后减速可以设成0.5，咲夜时停是设成0.0（(在锦上京中为541） |
| 548 | int a,int b, int c, int d);23(等待 | 5系 单位固有属性 | 的难度选择版(在锦上京中为542） |
| 549 | int a | 5系 单位固有属性 | (在锦上京中为543） 将某单位的flag 0x80000000设置为a |
| 550 | int)仅在地灵殿(对应ins_370 | 5系 单位固有属性 | 四面使用过,效果不明.之后被zun遗弃(在锦上京中为544） |
| 551 | int)仅在地灵殿(对应ins_371 | 5系 单位固有属性 | 四面使用过,效果不明.之后被zun遗弃(在锦上京中为545） |
| 552 | int a | 5系 单位固有属性 | (在锦上京中为546） 提高贴图图层a层,对时间值为0的贴图没用 |
| 553 | int index_SE | 5系 单位固有属性 | 设置被打击的音效(在锦上京中为547） |
| 554 | — | 5系 单位固有属性 | 显示logoenemy(在锦上京中为548） |
| 555 | int& A,int b | 5系 单位固有属性 | (在锦上京中为549） 检查第b号单位是否存活，若存活测A=1,否则A=0.单位的编号就是单位登场的顺序.main为0号， |
| 556 | string func | 5系 单位固有属性 | 设置死尸弹为func(在锦上京中为550） |
| 557 | int, int,int, float, float | 5系 单位固有属性 | 一些道中boss死亡时使用，效果未知(在锦上京中为551） |
| 558 | int a | 5系 单位固有属性 | (在锦上京中为552） a=1则赋予单位某flag,a=0消除,具体参照下方flag表 和424功能完全一样,此flag控制左右移动翻转 |
| 559 | int | 5系 单位固有属性 | 未知(在锦上京中为553） |
| 560 | float a,flaot b | 5系 单位固有属性 | 未知(在锦上京中为554 |
| 561 | — | 5系 单位固有属性 | 放出单位死亡特效（实际不死亡）庙道中击破大蝴蝶之后鬼火爆炸时发现(在锦上京中为555） |
| 562 | ) (hld中为 | 5系 单位固有属性 | 掉落所有物品,与ins_509不同的是ins_509会判断一个结果是否为true才决定掉落,但是该函数绝对会掉落(在锦上京中为556） |
| 563 | int is_rect | 5系 单位固有属性 | 设置判定点是否为方形(在锦上京中为557） |
| 564 | float angle | 5系 单位固有属性 | 设置判定点角度(在锦上京中为558） |
| 565 | float dmg_rate | 5系 单位固有属性 | （在锦上京中为559） 设置使用bomb时伤害倍率，0.0的话就是不掉血，1.0就是全额伤害（包括普通射击伤害与bomb伤害） |
| 566 | — | 5系 单位固有属性 | 没有在任何位置发现,可能zun设计之后未使用(在锦上京中为560 |
| 567 | int | 5系 单位固有属性 | 正邪使用，效果未知(在锦上京中为561） |
| 568 | int | 5系 单位固有属性 | 设置boss的伤害倍率，0为谱模式，1为符卡模式（用于双boss同时在场时，设置副boss的倍率）(在锦上京中为562） |
| 569 | int | 5系 单位固有属性 | 绀珠传新增，用来设置击破率(在锦上京中为563） |
| 570 | — | 5系 单位固有属性 | 绀珠传新增(在锦上京中为564） |
| 571 | — | 5系 单位固有属性 | 绀珠传新增(在锦上京中为565） |
| 572 | int hp)(tkz | 5系 单位固有属性 | 设置当前血量为hp,不同于ins_511的是不会修改最大血量(在锦上京中为566） |
| 573 | int index,int value) (hld | 5系 单位固有属性 | 修改关于时间减少的掉落类型index掉落为value,主要在boss处使用,控制boss随击破时间增加而减少的金数(在锦上京中为567） |
| 574 | int maxTime) (hld)修改随时间减少的掉落物的消失时间,设置后就会启动一计时器进行计时,当(击破/强制掉落)获得掉落时,会掉落ins_573设置的掉落物数量*max(0,1-当前时间/消失时间 | 5系 单位固有属性 | (在锦上京中为568） |
| 600 | int num | 6系 弹幕相关 | 创建一个弹幕，该弹幕编号为num。 |
| 601 | int num | 6系 弹幕相关 | 发射num号弹幕。 |
| 602 | int num, int a, int b | 6系 弹幕相关 | 给num号弹幕设置子弹类型和颜色，a和b与bullet.anm中的描述文件的内容存在对应关系。a为子弹类型，b为子弹颜色，详见下表： 子弹编号 弹型 子弹编号 弹型 子弹编号 弹型 子弹编号 弹型 0 点弹 1 高光点弹 2 葡萄弹 3 粒弹 4 小玉 5 高光小玉 6 环玉 7 高光环玉 8 米弹 9 链弹 10 针弹 11 札弹 12 鳞弹 13 铳弹 14 消弹效果 15 杆菌弹 16 顺时针旋转小星弹 17 钱币 18 中玉 19 高光中玉 20 椭弹 21 刀弹 22 蝶弹 23 顺时针旋转大星弹 24 逆时针旋转大星弹 25 红色炎弹 26 紫色炎弹 27 蓝紫炎弹 28 黄色炎弹 29 心弹 30 伸缩中玉 31 矢弹… |
| 603 | int num, float x, float y | 绀珠传以前，24是红色炎弹，25为原26，以此类推，相对顺序不变。44-47为虹龙洞加入，48-49为锦上京加入 | 以基准发弹点为基础，将num号弹幕的发弹点横纵坐标偏移x和y。基准发弹点默认为当前单位的位置。 |
| 604 | int num, float dir, float dif | 绀珠传以前，24是红色炎弹，25为原26，以此类推，相对顺序不变。44-47为虹龙洞加入，48-49为锦上京加入 | 设置num号弹幕的角度参数：dir为方向参数，dif为角度差参数，参数作用多样，详见607下表格。 |
| 605 | int num, float maxspd, float minspd | 绀珠传以前，24是红色炎弹，25为原26，以此类推，相对顺序不变。44-47为虹龙洞加入，48-49为锦上京加入 | 设置num号弹幕的速度参数：详见607下表格，若无特别说明，则maxspd代表最大速度，minspd代表最小速度，各层的速度在[minspd, maxspd]内均匀分布， 例如：对某一三层开花弹(style = 3)设定maxspd = 2.0，minspd = 1.0，则这三层子弹的速度分别为1.0、1.5、2.0。 （注：一般情况下，这两个参数位置可以随意调换，计算速度时是按两个数形成的闭区间计算，但为了方便说明，用了最大最小的描述。对于上例，设定maxspd = 1.0，minspd = 2.0，则结果不变。） |
| 606 | int num, int way, int layer | 绀珠传以前，24是红色炎弹，25为原26，以此类推，相对顺序不变。44-47为虹龙洞加入，48-49为锦上京加入 | 详见607指令下的表格，若无特别说明，则该指令作用为设置num号弹幕的way数(way)和每way中含有的层数(layer)， way一般指大方向，层是way内部的概念，是指way内部速度不同（方向也可能不同）的子弹。因为速度不同的子弹发射后呈现分层的形态，所以得名层。 |
| 607 | int num, int style | 绀珠传以前，24是红色炎弹，25为原26，以此类推，相对顺序不变。44-47为虹龙洞加入，48-49为锦上京加入 | 根据style设置num号弹幕的形状（展开方式），详见下表： 表中“示例”列一般会提供两张示例图，分别是偶数way和奇数way时的情形。少数style对应的形状不分奇数和偶数way，此时只提供一张示例图。 示例图中的中玉是札弹的发弹点。蓝色札弹表示本style下的示例子弹。 有些示例图中含有粉色的札弹，这是为方便辨别某些速度和角度关系而设计的，粉色札弹的性质将在“描述”列中说明。 表中第四列的参数列表中，如果含有“或”字，则表示此参数的值在奇数way和偶数way时不同。 style 描述 示例 示例所用参数值 0 普通自机狙， 中心方向为(自机方向 + dir)，dif为各way间角度差。 偶数way时中心方向无子弹。 粉色札弹为自… |
| 608 | int num, int a, int b | 绀珠传以前，24是红色炎弹，25为原26，以此类推，相对顺序不变。44-47为虹龙洞加入，48-49为锦上京加入 | 设置num号弹幕的音效，a表示发弹音效，b表示变速音效。参数为-1表示设置为无音效。 |
| 609 | int num，变换序号,通道,int mode,int a,int b,float r,float s | 绀珠传以前，24是红色炎弹，25为原26，以此类推，相对顺序不变。44-47为虹龙洞加入，48-49为锦上京加入 | 610(int num，变换序号,通道,int mode,int a,int b,int c,int d,float r,float s，float m,float n) |
| 611 | int num，通道,int mode,int a,int b,float r,float s | 绀珠传以前，24是红色炎弹，25为原26，以此类推，相对顺序不变。44-47为虹龙洞加入，48-49为锦上京加入 | 612(int num，通道,int mode,int a,int b,int c,int d,float r,float s，float m,float n) 609-612均为给弹幕设置变换的指令，具体解释请翻至最下面这里查看。 |
| 613 | — | 绀珠传以前，24是红色炎弹，25为原26，以此类推，相对顺序不变。44-47为虹龙洞加入，48-49为锦上京加入 | 全屏消弹，消去的子弹不转化为绿点。 |
| 614 | int numa, int numb | 绀珠传以前，24是红色炎弹，25为原26，以此类推，相对顺序不变。44-47为虹龙洞加入，48-49为锦上京加入 | 复制numb号弹幕的所有已设定的参数到numa号弹幕中。 |
| 615 | float r | 绀珠传以前，24是红色炎弹，25为原26，以此类推，相对顺序不变。44-47为虹龙洞加入，48-49为锦上京加入 | 消掉以当前单位位置为中心，半径r的圆形范围内的子弹，消去的子弹转化为绿点。 |
| 616 | float r | 绀珠传以前，24是红色炎弹，25为原26，以此类推，相对顺序不变。44-47为虹龙洞加入，48-49为锦上京加入 | 消掉以当前单位位置为中心，半径r的圆形范围内的子弹，但消去的子弹不转化为绿点。 |
| 617 | 弹幕编号，float a,b,c,d,e,f | 绀珠传以前，24是红色炎弹，25为原26，以此类推，相对顺序不变。44-47为虹龙洞加入，48-49为锦上京加入 | 根据rank的值来决定弹速 |
| 618 | 弹幕编号，float a,b,c,d,e,f,g,h,i,j | 绀珠传以前，24是红色炎弹，25为原26，以此类推，相对顺序不变。44-47为虹龙洞加入，48-49为锦上京加入 | 根据rank的值来决定弹速 |
| 619 | 弹幕编号，float a,b,c,d | 绀珠传以前，24是红色炎弹，25为原26，以此类推，相对顺序不变。44-47为虹龙洞加入，48-49为锦上京加入 | 根据rank的值来决定弹速 |
| 620 | 弹幕编号，int a,b,c,d,e,f | 绀珠传以前，24是红色炎弹，25为原26，以此类推，相对顺序不变。44-47为虹龙洞加入，48-49为锦上京加入 | 根据rank的值来决定way数和层数 |
| 621 | 弹幕编号，int a,b,c,d,e,f,g,h,i,j | 绀珠传以前，24是红色炎弹，25为原26，以此类推，相对顺序不变。44-47为虹龙洞加入，48-49为锦上京加入 | 根据rank的值来决定way数和层数 |
| 622 | 弹幕编号，int a,b,c,d | 绀珠传以前，24是红色炎弹，25为原26，以此类推，相对顺序不变。44-47为虹龙洞加入，48-49为锦上京加入 | 根据rank的值来决定way数和层数 |
| 623 | %N,float x,float y | 绀珠传以前，24是红色炎弹，25为原26，以此类推，相对顺序不变。44-47为虹龙洞加入，48-49为锦上京加入 | 计算 点x,y到 自机到角度并存入N中(在锦上京中为617） |
| 624 | int num, float a, b, c, d, e, f, g, h | 绀珠传以前，24是红色炎弹，25为原26，以此类推，相对顺序不变。44-47为虹龙洞加入，48-49为锦上京加入 | （此指令在锦上京中被移除） 605的难度融合版，在Easy难度下相当于执行ins_605(num, a, e)，Normal难度下相当于执行ins_605(num, b, f)，以此类推。 |
| 625 | int num, int a, b, c, d, e, f, g, h | 绀珠传以前，24是红色炎弹，25为原26，以此类推，相对顺序不变。44-47为虹龙洞加入，48-49为锦上京加入 | （此指令在锦上京中被移除） 606的难度融合版，在Easy难度下相当于执行ins_606(num, a, e)，Normal难度下相当于执行ins_606(num, b, f)，以此类推。 |
| 626 | int num, float o, float r | 绀珠传以前，24是红色炎弹，25为原26，以此类推，相对顺序不变。44-47为虹龙洞加入，48-49为锦上京加入 | (在锦上京中为618） 以基准发弹点为基础，将num号弹幕的发弹点偏移(o, r)，其中(o, r)为极坐标。基准发弹点默认为当前单位的位置。 |
| 627 | int num, float dis | 绀珠传以前，24是红色炎弹，25为原26，以此类推，相对顺序不变。44-47为虹龙洞加入，48-49为锦上京加入 | (在锦上京中为619） 设置发弹方式为从以当前发弹点为圆心，半径为dis的圆周上发弹，而不是从发弹点发弹。 |
| 628 | int num, float x, float y | 绀珠传以前，24是红色炎弹，25为原26，以此类推，相对顺序不变。44-47为虹龙洞加入，48-49为锦上京加入 | (在锦上京中为620） 设置基准发弹点为(x, y)。 |
| 629 | flout r,int color | 绀珠传以前，24是红色炎弹，25为原26，以此类推，相对顺序不变。44-47为虹龙洞加入，48-49为锦上京加入 | (在锦上京中为621） 设置boss周围的纹理变化特性，影响半径为r，颜色为color，对应RGB颜色。 |
| 630 | int a | 绀珠传以前，24是红色炎弹，25为原26，以此类推，相对顺序不变。44-47为虹龙洞加入，48-49为锦上京加入 | (在锦上京中为622） 执行STD脚本a。 |
| 631 | int a | 绀珠传以前，24是红色炎弹，25为原26，以此类推，相对顺序不变。44-47为虹龙洞加入，48-49为锦上京加入 | (在锦上京中为623，但是效果不明） a=时,隐藏boss血条以及时间，是否无敌和锁时间待测试 |
| 632 | int a | 绀珠传以前，24是红色炎弹，25为原26，以此类推，相对顺序不变。44-47为虹龙洞加入，48-49为锦上京加入 | （在锦上京中为624） boss每身重置为0，有些特殊攻击模式时启用， 使用一些封装函数，如雷鼓震屏，正邪翻转，和637共用一套函数， 637多为一次性的效果，632为长久效果 |
| 633 | int a | 绀珠传以前，24是红色炎弹，25为原26，以此类推，相对顺序不变。44-47为虹龙洞加入，48-49为锦上京加入 | (在锦上京中为625） 封装函数，当a=1时，将会每帧从[-9940]里取出值并作为伤害传递给Boss |
| 634 | int a | 绀珠传以前，24是红色炎弹，25为原26，以此类推，相对顺序不变。44-47为虹龙洞加入，48-49为锦上京加入 | (在锦上京中为626） 封装函数，当a=1时，单位的体术判定采用特殊方式 |
| 635 | float r | 绀珠传以前，24是红色炎弹，25为原26，以此类推，相对顺序不变。44-47为虹龙洞加入，48-49为锦上京加入 | (在锦上京中为627） 消掉半径为r范围内的弹幕,消掉的弹幕变为最大得点,与615还有一处不同 |
| 636 | float r | 绀珠传以前，24是红色炎弹，25为原26，以此类推，相对顺序不变。44-47为虹龙洞加入，48-49为锦上京加入 | (在锦上京中为628） 消掉半径为r范围内的弹幕,消掉的弹幕变为最大得点,与616还有一处不同 |
| 637 | int | 绀珠传以前，24是红色炎弹，25为原26，以此类推，相对顺序不变。44-47为虹龙洞加入，48-49为锦上京加入 | (在锦上京中为629） boss每身重置为0，有些特殊攻击模式时启用， 使用一些封装函数，如雷鼓震屏，正邪翻转，和632 共用一套函数， 637为一次性的效果，632为长久效果 |
| 638 | int | 绀珠传以前，24是红色炎弹，25为原26，以此类推，相对顺序不变。44-47为虹龙洞加入，48-49为锦上京加入 | 未知(在锦上京中为630） |
| 639 | int | 绀珠传以前，24是红色炎弹，25为原26，以此类推，相对顺序不变。44-47为虹龙洞加入，48-49为锦上京加入 | 未知(在锦上京中为631） |
| 640 | 弹幕编号,int a,"func" | 绀珠传以前，24是红色炎弹，25为原26，以此类推，相对顺序不变。44-47为虹龙洞加入，48-49为锦上京加入 | 由弹幕召唤使魔的时候使用，需要a= mode 16777216的弹幕编号2 |
| 641 | 弹幕编号 | 绀珠传以前，24是红色炎弹，25为原26，以此类推，相对顺序不变。44-47为虹龙洞加入，48-49为锦上京加入 | hzc6面时符大型刀弹使用，用途未知 |
| 700 | 弹幕编号,float a,float length,float b,float width | 7系 激光相关 | 使弹幕变成激光，设置长度和宽度，a和b是开始位置的参数，一般激光设成0就行 17条爆弹那种预警线+直接生产的设置成和长度一样 若要发射曲线激光，则a,length,b 都是无关参数，设成-1.0f,曲线激光只可以设置宽度. |
| 701 | 弹幕编号,int a,int b,int c,int d, int e | 7系 激光相关 | 设置预警线持续时间a和激光的持续时间c. b和d分别是从预警线变为实际激光和激光消失过程需要的时间，e一般为0 用途未知 若发射曲线激光则，则b,c,d,都是无关参数，a是激光发射持续时间（决定其长度） e让然是迷之0 |
| 702 | 弹幕编号 | 7系 激光相关 | 普通激光的发弹函数 |
| 703 | 弹幕编号,int a | 7系 激光相关 | 发射预警线激光专用，a为激光编号，区别于弹幕编号 |
| 704 | 激光编号,float x,float y | 7系 激光相关 | 改变激光的起点为x,y |
| 705 | 激光编号,float x,float y | 7系 激光相关 | 赋予激光起点一个速度 |
| 707 | 激光编号,float width | 7系 激光相关 | 改变激光的宽度为width |
| 708 | 激光编号,float a | 7系 激光相关 | 改变激光的角度为a |
| 709 | 激光编号,float a | 7系 激光相关 | 赋予激光一个顺时针的角速度a |
| 710 | 激光编号 | 7系 激光相关 | 消除激光 |
| 711 | 弹幕编号 | 7系 激光相关 | 曲线激光用发弹函数 |
| 712 | float length,float width | 7系 激光相关 | 改变单位判定，使其变成类似于激光的东西 |
| 713 | int | 7系 激光相关 | 714(int int ) |
| 800 | int,"subroutin" | 8系 单位互动 | 推测是同时开启另一个人的"subroutin"，第一个int参数与编号有关，不明。eg.比如绀珠传ex的纯狐与赫卡互动。 |
| 801 | float %X,float %Y,int n); 返回(X,Y | 8系 单位互动 | 等于第n号小怪的坐标。eg.比如神灵庙6道中判断大蝴蝶如果出屏则幽灵就不因大蝴蝶出屏消失而死亡 |
| 802 | int | 8系 单位互动 | 参数为0，立即击破场上boss当前阶段（用于多boss同台时，击破一个boss时另一个boss也同时击破，例hzcex道中1，2符） |
| 900 | — | 9系 Debug相关 | 仅仅在一面道中的GirlTest中出现一次，zun测试用 |
| 901 | — | 9系 Debug相关 | 仅在DebugSkipFunc 使用，zun用来跳过Debug |
| 902 | — | 9系 Debug相关 | zun为debug用。 |
| 1000 | int | 10系 备用 | 直接掉落一个指定类型的灵，0为红灵、1为蓝灵、2为绿灵、3为白灵、4为蓝灵、5为隐形灵、6以后会播放奇怪的音效并产生一个隐形的灵 |
| 1001 | int | 10系 备用 | 设置掉落的灵衰减为0的帧数 |
| 1002 | int | 10系 备用 | 设置掉落的灵的数量的最大值 |
| 1003 | int | 10系 备用 | 设置单位受到伤害时是否掉灵，奇数不掉，偶数掉 |
| 1001 | int | 辉针城 | 1002(int); |
| 1003 | int | 辉针城 | 天邪鬼 |
| 1001 | int | 天邪鬼 | 1002(int); |
| 1003 | int | 天邪鬼 | 1004(); |
| 1005 | — | 天邪鬼 | 直接通关 |
| 1006 | — | 天邪鬼 | 直接时间到gameover |
| 1001 | int | 绀珠传 | 1002(int); |
| 1000 | int a, int b, int c | 天空璋 | :天空璋中出现，用于控制单位掉落的季节道具。a为变化帧数，b为初始季节道具数，c为最终季节道具数。单位掉落的季节道具会在a帧内从b变为c。 |
| 1001 | int a | 天空璋 | 天空璋中可用于控制单位掉落的季节道具。单位每减少a血量掉落一个季节点。 |
| 1000 | — | 噩梦日记 | 结束本关 |
| 1002 | double a | 噩梦日记 | 控制照片分数倍率 |
| 1008 | int a | 噩梦日记 | a=0 没收相机 a=1 归还相机 |
| 1009 | int a | 噩梦日记 | 控制照相机伤害 |

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

## TH14.3 弹幕天邪鬼

- 体系：第四世代
- 指令：普通指令 319 条；已说明 257/319。主要分组：系统/流程/栈/算术 / System；敌机创建与 ANM 管理 / Enemy creation and ANM script management；移动管理 / Movement management；敌机属性与杂项 / Enemy property management and other miscellaneous things；子弹创建与删除 / Bullet creation and deletion；激光创建 / Laser creation；敌机交互 / Enemy interaction；调试 / Debug；游戏特有 / Game specific。
- 变量：变量范围 -10000..-9907；本文列出有说明/命名记录的 94 条，未列空洞/未知项。

### TH14.3 指令：系统/流程/栈/算术 / System

| ID | 助记名 | 参数 | 说明 | 文档化 | 来源 |
| --- | --- | --- | --- | --- | --- |
| 0 | ins_0 | — | Empty instruction, doesn't do anything. | 是 | 继承自 TH13 |
| 1 | ins_1 | — | Returns to the top of current call stack. | 是 | 继承自 TH13 |
| 2 | ins_2 | — |  | 否/待确认 | 继承自 TH-1 |
| 3 | ins_3 | — |  | 否/待确认 | 继承自 TH-1 |
| 4 | ins_4 | — |  | 否/待确认 | 继承自 TH-1 |
| 5 | ins_5 | — |  | 否/待确认 | 继承自 TH-1 |
| 6 | ins_6 | — |  | 否/待确认 | 继承自 TH-1 |
| 7 | ins_7 | — |  | 否/待确认 | 继承自 TH-1 |
| 8 | ins_8 | — |  | 否/待确认 | 继承自 TH-1 |
| 9 | ins_9 | — |  | 否/待确认 | 继承自 TH-1 |
| 10 | ins_10 | — | Returns from the current sub. | 是 | 继承自 TH13 |
| 11 | ins_11 | m (sub) | Calls a given sub. Can take additional parameters to pass as arguments to the sub. [c=orange]Direct Usage obsolete. Use `@subName()` syntax instead. | 是 | 继承自 TH13 |
| 12 | ins_12 | o (target) | Unconditionally jumps to the label %1. [c=orange]Direct usage obsolete. Use `goto label` syntax instead. | 是 | 继承自 TH13 |
| 13 | ins_13 | o (target) | Pops a number from the stack and if it evaluates to false (in this context, 0), jumps to label %1. [c=orange]Direct usage obsolete. Use if/unless statement instead. | 是 | 继承自 TH13 |
| 14 | ins_14 | o (target) | Pops a number from the stack and if it evaluates to true (in this context, anything non-0), jumps to label %1. [c=orange]Direct usage obsolete. Use if/unless statement instead. | 是 | 继承自 TH13 |
| 15 | ins_15 | m (sub) | Asynchronously calls a given sub. Can take additional parameters to pass as arguments to the sub. [c=orange]Direct usage obsolete. Use `@subName() async` syntax instead. | 是 | 继承自 TH13 |
| 16 | ins_16 | mS (sub, id) | Asynchronously calls a given sub and assigns it ID %2. Can take additional parameters to pass as arguments to the sub. [c=orange]Direct usage obsolete, use, `@subName() async id` syntax instead. | 是 | 继承自 TH13 |
| 17 | ins_17 | S (id) | Ends most recently called sub that has ID %1 (same ID as in ins_16). If no sub with the given ID is found, nothing happens. Using ID -1 can lead to various unexpected results, ranging from deleting the enemy to freezing the game. | 是 | 继承自 TH13 |
| 18 | ins_18 | S (id) | Let `vm` be the most recent async sub running with ID %1: this ins sets `vm[0x000011E4]` to 1. | 否/待确认 | 继承自 TH13 |
| 19 | ins_19 | S (id) | Let `vm` be the most recent async sub running with ID %1: this ins sets `vm[0x000011E4]` to 0. | 否/待确认 | 继承自 TH13 |
| 20 | ins_20 | SS (id, b) | Let `vm` be the most recent async sub running with ID %1: this ins sets `vm[0x0000101C]` to %2. | 否/待确认 | 继承自 TH13 |
| 21 | ins_21 | — | Ends all running async subs. Calling this in an async sub can lead to unexpected results, such as crashing the game. | 是 | 继承自 TH13 |
| 22 | ins_22 | Sm (a, b) | Debug instruction, code does not exist in the release builds of the game. Most likely used to call sub %2 if some variable set in a debug menu is equal to %1. | 是 | 继承自 TH13 |
| 23 | ins_23 | S (time) | Stops sub execution for %1 frames. | 是 | 继承自 TH13 |
| 24 | ins_24 | f (time) | ins_23, but time is given as a float instead of an int. Subframes do actually exist and affect ins_547. | 是 | 继承自 TH13 |
| 25 | ins_25 | — |  | 否/待确认 | 继承自 TH-1 |
| 26 | ins_26 | — |  | 否/待确认 | 继承自 TH-1 |
| 27 | ins_27 | — |  | 否/待确认 | 继承自 TH-1 |
| 28 | ins_28 | — |  | 否/待确认 | 继承自 TH-1 |
| 29 | ins_29 | — |  | 否/待确认 | 继承自 TH-1 |
| 30 | ins_30 | m (formatString) | Some sort of `printf` debug instruction, which can take additional float/int arguments after %1. Its code does not exist in the release builds. | 是 | 继承自 TH13 |
| 31 | ins_31 | — |  | 否/待确认 | 继承自 TH-1 |
| 32 | ins_32 | — |  | 否/待确认 | 继承自 TH-1 |
| 33 | ins_33 | — |  | 否/待确认 | 继承自 TH-1 |
| 34 | ins_34 | — |  | 否/待确认 | 继承自 TH-1 |
| 35 | ins_35 | — |  | 否/待确认 | 继承自 TH-1 |
| 36 | ins_36 | — |  | 否/待确认 | 继承自 TH-1 |
| 37 | ins_37 | — |  | 否/待确认 | 继承自 TH-1 |
| 38 | ins_38 | — |  | 否/待确认 | 继承自 TH-1 |
| 39 | ins_39 | — |  | 否/待确认 | 继承自 TH-1 |
| 40 | ins_40 | S (size) | Increases the ECL stack pointer by %1 bytes (probably), to make space for sub variables. [c=orange]Obsolete, thecl generates this instruction automatically. | 是 | 继承自 TH13 |
| 41 | ins_41 | — |  | 否/待确认 | 继承自 TH-1 |
| 42 | ins_42 | S (num) | Pushes an integer to the ECL stack. [c=orange]Obsolete, push values to stack by writing unassigned expressions instead. | 是 | 继承自 TH13 |
| 43 | ins_43 | S (var) | Pops an integer from the stack into variable %1. [c=orange]Obsolete, use assignment syntax instead. | 是 | 继承自 TH13 |
| 44 | ins_44 | f (num) | Pushes a float to the ECL stack. [c=orange]Obsolete, push values to stack by writing unassigned expressions instead. | 是 | 继承自 TH13 |
| 45 | ins_45 | f (var) | Pops a float from the stack into variable %1. [c=orange]Obsolete, use assignment syntax instead. | 是 | 继承自 TH13 |
| 46 | ins_46 | — |  | 否/待确认 | 继承自 TH-1 |
| 47 | ins_47 | — |  | 否/待确认 | 继承自 TH-1 |
| 48 | ins_48 | — |  | 否/待确认 | 继承自 TH-1 |
| 49 | ins_49 | — |  | 否/待确认 | 继承自 TH-1 |
| 50 | ins_50 | — | Sums integers on the stack. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 51 | ins_51 | — | Sums floats on the stack. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 52 | ins_52 | — | Subtracts integers on the stack. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 53 | ins_53 | — | Subtracts floats on the stack. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 54 | ins_54 | — | Multiplies integers on the stack. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 55 | ins_55 | — | Multiplies floats on the stack. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 56 | ins_56 | — | Divides integers on the stack. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 57 | ins_57 | — | Divides floats on the stack. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 58 | ins_58 | — | Modulo operation on integers on the stack. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 59 | ins_59 | — | Stack integer `==` comparison. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 60 | ins_60 | — | Stack float `==` comparison. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 61 | ins_61 | — | Stack integer `!=` comparison. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 62 | ins_62 | — | Stack float `!=` comparison. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 63 | ins_63 | — | Stack integer `<` comparison. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 64 | ins_64 | — | Stack float `<` comparison. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 65 | ins_65 | — | Stack integer `<=` comparison. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 66 | ins_66 | — | Stack float `<=` comparison. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 67 | ins_67 | — | Stack integer `>` comparison. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 68 | ins_68 | — | Stack float `>` comparison. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 69 | ins_69 | — | Stack integer `>=` comparison. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 70 | ins_70 | — | Stack float `>=` comparison. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 71 | ins_71 | — | Stack integer NOT operation (e.g. !1). [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 72 | ins_72 | — | Stack float NOT operation (e.g. !1.0f). [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 73 | ins_73 | — | Logical OR operation on the stack. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 74 | ins_74 | — | Logical AND operation on the stack. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 75 | ins_75 | — | Bitwise XOR operation on integers on the stack. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 76 | ins_76 | — | Bitwise OR operation on integers on the stack. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 77 | ins_77 | — | Bitwise AND operation on integers on the stack. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 78 | ins_78 | S (var) | Pushes variable %1 to the stack and then decrements it. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 79 | ins_79 | — | sin operation on a float on the stack. [c=orange]Obsolete, use `sin(floatVal)` instead. | 是 | 继承自 TH13 |
| 80 | ins_80 | — | cos operation on a float on the stack. [c=orange]Obsolete, use `cos(floatVal)` instead. | 是 | 继承自 TH13 |
| 81 | ins_81 | ffff (varX, varY, ang, radius) | Performs following operation: [code]%1 = cos(%3)*%4;<br>%2 = sin(%3)*%4;[/code] | 是 | 继承自 TH13 |
| 82 | ins_82 | f (var) | Normalizes angle in %1. | 是 | 继承自 TH13 |
| 83 | ins_83 | — | Negates an integer on the stack. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 84 | ins_84 | — | Negates a float on the stack. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 85 | ins_85 | fff (var, x, y) | Performs following operation: [code]%1 = %2*%2 + %3*%3;[/code] | 是 | 继承自 TH13 |
| 86 | ins_86 | fff (var, x, y) | Performs following operation: [code]%1 = sqrt(%2*%2 + %3*%3);[/code] | 是 | 继承自 TH13 |
| 87 | ins_87 | fffff (var, x1, y1, x2, y2) | Calculates angle from (%2,%3) to (%4,%5) and stores it in %1. | 是 | 继承自 TH13 |
| 88 | ins_88 | — | square root operation on a float on the stack. [c=orange]Obsolete, use `sqrt(floatVal)` instead. | 是 | 继承自 TH13 |
| 89 | ins_89 | fff (var, a, x) | Performs following operation: [code]%1 = %2*%3;[/code]<br>(what's the point of making this an instruction, ZUN?) | 是 | 继承自 TH13 |
| 90 | ins_90 | fffff (varX, varY, x, y, rad) | Rotates point (%3,%4) by angle %5 and stores the resulting coordinates in %1 and %2. | 是 | 继承自 TH13 |
| 91 | ins_91 | SfSSff (slot, var, time, mode, init, final) | In %3 frames using mode %4, variable %2 changes from %5 to %6. %1 is used to set the slot to be used by this ins, every enemy has 8 slots (0 to 7). | 是 | 继承自 TH13 |
| 92 | ins_92 | SfSSffff (slot, var, time, mode, init, final, m, n) | Same as ins_91, but takes 2 extra arguments of unknown meaning. Needs investigation. | 否/待确认 | 继承自 TH13 |
| 93 | ins_93 | ffff (varX, varY, r1, r2) | Gets a random point based on %3 and %4 and stores it on (%1,%2). Needs investigation. | 否/待确认 | 继承自 TH13 |

### TH14.3 指令：敌机创建与 ANM 管理 / Enemy creation and ANM script management

| ID | 助记名 | 参数 | 说明 | 文档化 | 来源 |
| --- | --- | --- | --- | --- | --- |
| 300 | ins_300 | mffSSS (sub, x, y, hp, score, item) | Creates an enemy using subroutine %1 at coordinates %2, %3 (relative to position of enemy that called it), health of created enemy is %4, score bonus is %5 and item drop is %6. | 是 | 继承自 TH13 |
| 301 | ins_301 | mffSSS (sub, x, y, hp, score, item) | Creates an enemy using subroutine %1 at coordinates %2, %3 (absolute position), health of created enemy is %4, score bonus is %5 and item drop is %6. | 是 | 继承自 TH13 |
| 302 | ins_302 | S (anmIndex) | Selects ANM file to be used by other instructions based on %1. | 是 | 继承自 TH13 |
| 303 | ins_303 | SS (slot, script) | Loads script %2 from ANM selected with ins_302 on slot %1. | 是 | 继承自 TH13 |
| 304 | ins_304 | mffSSS (sub, x, y, hp, score, item) | Creates a mirrored enemy using subroutine %1 at coordinates %2, %3 (relative to caller's position), health of created enemy is %4, score bonus is %5 and item drop is %6. | 是 | 继承自 TH13 |
| 305 | ins_305 | mffSSS (sub, x, y, hp, score, item) | Creates an mirrored enemy using subroutine %1 at coordinates %2, %3 (absolute position), health of created enemy is %4, score bonus is %5 and item drop is %6. | 是 | 继承自 TH13 |
| 306 | ins_306 | SS (slot, script) | Loads script %2 from ANM selected with ins_302 on slot %1. However, the script number provided will only be used when the enemy is not moving. When moving left %2+1 will be used, right %2+2, diagonal left %2+3, diagonal right %2+4. Might not work properly if %1 is not 0 according to THBWiki. | 是 | 继承自 TH13 |
| 307 | ins_307 | SS (anmIndex, script) | From ANM file selected based on %1, play script %2 at caller's current coordinates. The spawned script is completely independent, and will continue existing even if caller is deleted. | 是 | 继承自 TH13 |
| 308 | ins_308 | SS (anmIndex, script) | From ANM file selected based on %1, play script %2 at coordinates (0, 0). The spawned script is completely independent, and will continue existing even if caller is deleted. | 是 | 继承自 TH13 |
| 309 | ins_309 | mffSSS (sub, x, y, hp, score, item) | Creates a filler enemy using subroutine %1 at coordinates %2, %3 (relative to caller's position), health of created enemy is %4, score bonus is %5 and item drop is %6. | 是 | 继承自 TH13 |
| 310 | ins_310 | mffSSS (sub, x, y, hp, score, item) | Creates a filler enemy using subroutine %1 at coordinates %2, %3 (absolute position), health of created enemy is %4, score bonus is %5 and item drop is %6. | 是 | 继承自 TH13 |
| 311 | ins_311 | mffSSS (sub, x, y, hp, score, item) | Creates a mirrored filler enemy using subroutine %1 at coordinates %2, %3 (relative to caller's position), health of created enemy is %4, score bonus is %5 and item drop is %6. | 是 | 继承自 TH13 |
| 312 | ins_312 | mffSSS (sub, x, y, hp, score, item) | Creates a mirrored filler enemy using subroutine %1 at coordinates %2, %3 (absolute position), health of created enemy is %4, score bonus is %5 and item drop is %6. | 是 | 继承自 TH13 |
| 313 | ins_313 | S (script) | Same as ins_307, except it uses the ANM file selected by ins_302. | 是 | 继承自 TH13 |
| 314 | ins_314 | SS (anmIndex, script) | Same as ins_307, except it spawns the ANM with a higher layer? Needs further investigation. | 否/待确认 | 继承自 TH13 |
| 315 | ins_315 | SSf (anmIndex, script, angle) | Same as ins_307, except it sets rotation of spawned ANM to %3. | 是 | 继承自 TH13 |
| 316 | ins_316 | SS (a, b) | Unknown. | 否/待确认 | 继承自 TH13 |
| 317 | ins_317 | SS (slot, switch) | Sets the execution pointer of ANM script on slot %1 to where ANM `ins_5(a)` with `a` == `switch` is (the time is also changed to match time of `ins_5`). Doesn't work if the value is 0 apparently? | 是 | 继承自 TH13 |
| 318 | ins_318 | — | Resets some ANM-related parameters of the caller (TODO: what exactly?) | 是 | 继承自 TH13 |
| 319 | ins_319 | Sf (slot, r) | Set rotation of an ANM script on slot %1 to %2. | 是 | 继承自 TH13 |
| 320 | ins_320 | Sff (slot, x, y) | Set position of an ANM script on slot %1 to (%2,%3). This does not detach the script from the caller, so the actual position of the script will be position of the caller + position set here. | 是 | 继承自 TH13 |
| 321 | ins_321 | mffSSS (sub, x, y, hp, score, item) | ins_300, but used by 'MapleEnemy' (TODO: what's the difference from ins_300?) | 是 | 继承自 TH13 |
| 322 | ins_322 | SS (a, b) | Unknown. | 否/待确认 | 继承自 TH13 |
| 323 | ins_323 | SS (anmIndex, script) | Set the animation that will play when the enemy dies to script %2 from ANM file specified by %1. | 是 | 继承自 TH13 |
| 324 | ins_324 | — | Unknown. | 否/待确认 | 继承自 TH13 |
| 325 | ins_325 | SSSS (slot, R, G, B) | Modify color of ANM script on slot %1, %2, %3, [c=lightblue]%4 correspond to individual colors and have to be from 0 to 255. | 是 | 继承自 TH13 |
| 326 | ins_326 | SSSSSS (slot, time, mode, R, G, B) | Same as ins_325, but the change is applied in %2 frames using mode %3. | 是 | 继承自 TH13 |
| 327 | ins_327 | SS (slot, alpha) | Sets alpha of ANM script on slot %1 to %2 (must be a value between 0-255) | 是 | 继承自 TH13 |
| 328 | ins_328 | SSSS (slot, time, mode, alpha) | Same as ins_327, but the change is applied in %2 frames using mode %3. | 是 | 继承自 TH13 |
| 329 | ins_329 | Sff (slot, w, h) | Sets horizontal and vertical scaling of ANM script on slot %1 to %2 and %3 respectively. Overwrites scaling properties set by the ANM script. | 是 | 继承自 TH13 |
| 330 | ins_330 | SSSff (slot, time, mode, w, h) | Same as ins_329, but the change is applied in %2 frames using mode %3. | 是 | 继承自 TH13 |
| 331 | ins_331 | SS (slot, alpha) | Sets alpha2 (opacity of the gradient) of ANM script on slot %1 to %2. | 是 | 继承自 TH13 |
| 332 | ins_332 | SSSS (slot, time, mode, alpha) | Same as ins_331, but the change is applied in %2 frames using mode %3. | 是 | 继承自 TH13 |
| 333 | ins_333 | SSSff (a, b, c, r, s) | Unknown. Might be doing something to ANM script on slot %1. | 否/待确认 | 继承自 TH13 |
| 334 | ins_334 | S (a) | Hard to tell? THBWiki Google translate gives this: 'The animation effect of the playing unit (enemy), the lightning effect near the evil spirit ball of the god temple', which might be referring to lightning around Nue in TD extra stage. | 否/待确认 | 继承自 TH13 |
| 335 | ins_335 | Sff (slot, w, h) | Same as ins_329, except it doesn't overwrite the scaling set by the ANM script - instead, it multiplies it. | 是 | 继承自 TH13 |
| 336 | ins_336 | SS (slot, layer) | Set layer of ANM script on slot %1 to %2. | 是 | 继承自 TH14 |
| 337 | ins_337 | SSfff (anmIndex, script, x, y, z) | Same as ins_307, but the spawned script is offset by (%3,%4). For 3D objects, %5 is used too (TODO: verify that). | 是 | 继承自 TH14 |

### TH14.3 指令：移动管理 / Movement management

| ID | 助记名 | 参数 | 说明 | 文档化 | 来源 |
| --- | --- | --- | --- | --- | --- |
| 400 | ins_400 | ff (x, y) | Sets caller's absolute position to %1, %2. | 是 | 继承自 TH13 |
| 401 | ins_401 | SSff (time, mode, x, y) | Same as ins_400, but the change is applied in %1 frames using mode %2. | 是 | 继承自 TH13 |
| 402 | ins_402 | ff (x, y) | Sets caller's relative position to %1, %2. | 是 | 继承自 TH13 |
| 403 | ins_403 | SSff (time, mode, x, y) | Same as ins_402, but the change is applied in %1 frames using mode %2. | 是 | 继承自 TH13 |
| 404 | ins_404 | ff (r, spd) | Sets caller's absolute movement angle to %1 and speed to %2. | 是 | 继承自 TH13 |
| 405 | ins_405 | SSff (time, mode, r, spd) | Same as ins_404, but the change is applied in %1 frames using mode %2. | 是 | 继承自 TH13 |
| 406 | ins_406 | ff (r, spd) | Sets caller's relative movement angle to %1 and speed to %2. | 是 | 继承自 TH13 |
| 407 | ins_407 | SSff (time, mode, r, spd) | Same as ins_406, but the change is applied in %1 frames using mode %2. | 是 | 继承自 TH13 |
| 408 | ins_408 | ffff (θ, spd, rad, radInc) | Sets caller's absolute circle movement: %1 is the angle indicating initial position on the circle, %2 is the angular velocity, %3 is circle radius and %4 is by how much the radius increases each frame. | 是 | 继承自 TH13 |
| 409 | ins_409 | SSfff (time, mode, spd, rad, radInc) | Same as ins_408, but the change is applied in %1 frames using mode %2. There is also no initial angle parameter here for obvious reason. | 是 | 继承自 TH13 |
| 410 | ins_410 | ffff (θ, spd, rad, radInc) | Sets caller's relative circle movement: %1 is the angle indicating initial position on the circle, %2 is the angular velocity, %3 is circle radius and %4 is by how much the radius increases each frame. | 是 | 继承自 TH13 |
| 411 | ins_411 | SSfff (time, mode, spd, rad, radInc) | Same as ins_410, but the change is applied in %1 frames using mode %2. There is also no initial angle parameter here for obvious reason. | 是 | 继承自 TH13 |
| 412 | ins_412 | SSf (time, mode, spd) | Randomizes caller's absolute angle and sets absolute speed to %3. The speed changes back to 0 in %1 frames using mode %2. | 是 | 继承自 TH13 |
| 413 | ins_413 | SSf (time, mode, spd) | Randomizes caller's relative angle and sets relative speed to %3. The speed changes back to 0 in %1 frames using mode %2. | 是 | 继承自 TH13 |
| 414 | ins_414 | — | Sets caller's absolute position to the absolute position of the boss. If called without a boss, [tip=Google translated from THBWiki, I find this sentence funny]it will cause serious mis-access and explode[/tip]. | 是 | 继承自 TH13 |
| 415 | ins_415 | — | Sets caller's relative position to the relative position of the boss. If called without a boss, [tip=Google translated from THBWiki, I find this sentence funny]it will cause serious mis-access and explode[/tip]. | 是 | 继承自 TH13 |
| 416 | ins_416 | fff (x, y, z) | Same as ins_400, but takes a %3 parameter for the third dimension, which probably affects 3D ANM scripts used by the caller, or something. | 是 | 继承自 TH13 |
| 417 | ins_417 | fff (x, y, z) | Same as ins_402, but takes a %3 parameter for the third dimension, which probably affects 3D ANM scripts used by the caller, or something. | 是 | 继承自 TH13 |
| 418 | ins_418 | ff (x, y) | Increases caller's absolute position by %1 and %2. | 是 | 继承自 TH13 |
| 419 | ins_419 | ff (x, y) | While the code of this ins looks like it's supposed to be a relative version of ins_418, it doesn't seem to behave like that... | 否/待确认 | 继承自 TH13 |
| 420 | ins_420 | ffffff (θ, spd, rad, radInc, ellDir, ellRatio) | Sets caller's absolute ellipse movement: %1 is the angle indicating initial position on the ellipse, %2 is the angular velocity, %3 is the base circle radius and %4 is by how much the radius increases each frame. %6 is how much the base circle should be 'squished' to make it an ellipse, and %5 is the squishing angle (I don't know math terms in English, sorry) | 是 | 继承自 TH13 |
| 421 | ins_421 | SSfffff (time, mode, spd, rad, radInc, ellDir, ellRatio) | Same as ins_420, but the change is applied in %1 frames using mode %2. There is also no initial angle parameter here for obvious reason | 是 | 继承自 TH13 |
| 422 | ins_422 | ffffff (θ, spd, rad, radInc, ellDir, ellRatio) | Sets caller's relative ellipse movement: %1 is the angle indicating initial position on the ellipse, %2 is the angular velocity, %3 is the base circle radius and %4 is by how much the radius increases each frame. %6 is how much the base circle should be 'squished' to make it an ellipse, and %5 is the squishing angle (I don't know math terms in English, sorry) | 是 | 继承自 TH13 |
| 423 | ins_423 | SSfffff (time, mode, spd, rad, radInc, ellDir, ellRatio) | Same as ins_422, but the change is applied in %1 frames using mode %2. There is also no initial angle parameter here for obvious reason | 是 | 继承自 TH13 |
| 424 | ins_424 | S (state) | Sets caller's mirror flag to %1. | 是 | 继承自 TH13 |
| 425 | ins_425 | Sffffff (time, x1, y1, x2, y2, x3, y3) | In %1 frames, the enemy moves towards (%2,%3), then moves towards (%6,%7) for a while and finally moves to (%4,%5). Uses absolute position.<br>From THBWiki: <br>(assuming the current coordinates are (x0, y0)) the motion trajectory is actually a Bezier curve from (x0, y0) to (x2, y2);<br>The P1 coordinate of the curve is `((x1-x0)*1/3, (y1-y0)*1/3)`;<br>The P2 coordinate of the curve is `(-(x3-x2)*1/3+x2,-(y3-y2) *1/3+x2)` | 是 | 继承自 TH13 |
| 426 | ins_426 | Sffffff (time, x1, y1, x2, y2, x3, y3) | Same as ins_425, but uses relative position. | 是 | 继承自 TH13 |
| 427 | ins_427 | — | Resets some movement-related parameters (TODO: what exactly?) | 否/待确认 | 继承自 TH13 |
| 428 | ins_428 | ff (r, spd) | Same as ins_404, but ignores the mirror flag. | 是 | 继承自 TH13 |
| 429 | ins_429 | SSff (time, mode, r, spd) | Same as ins_405, but ignores the mirror flag. | 是 | 继承自 TH13 |
| 430 | ins_430 | ff (r, spd) | Same as ins_406, but ignores the mirror flag. | 是 | 继承自 TH13 |
| 431 | ins_431 | SSff (time, mode, r, spd) | Same as ins_407, but ignores the mirror flag. | 是 | 继承自 TH13 |
| 432 | ins_432 | S (id) | Sets caller's absolute position to absolute position of enemy with var_-9914 == %1. | 是 | 继承自 TH13 |
| 433 | ins_433 | S (id) | Sets caller's relative position to relative position of enemy with var_-9914 == %1. | 是 | 继承自 TH13 |
| 434 | ins_434 | SSSff (time, mode, c, x, y) | In %1 frames using mode %2, caller's absolute position is changed to (%4,%5). The movement trajectory is a curve based on %3, it is unknown how it works exactly. | 否/待确认 | 继承自 TH13 |
| 435 | ins_435 | SSSff (time, mode, c, x, y) | In %1 frames using mode %2, caller's relative position is changed to (%4,%5). The movement trajectory is a curve based on %3, it is unknown how it works exactly. | 否/待确认 | 继承自 TH13 |
| 436 | ins_436 | SSff (time, mode, x, y) | Same as ins_418, but the change is applied in %1 frames using mode %2. | 是 | 继承自 TH13 |
| 437 | ins_437 | SSff (time, mode, x, y) | Same as ins_419, but the change is applied in %1 frames using mode %2 (it also behaves as expected, unlike ins_419). | 是 | 继承自 TH13 |
| 438 | ins_438 | SSSff (time, mode, c, x, y) | Same as ins_434, but instead caller's current absolute coordinates are added to %4 and %5. | 是 | 继承自 TH13 |
| 439 | ins_439 | SSSff (time, mode, c, x, y) | Same as ins_435, but instead caller's current relative coordinates are added to %4 and %5. | 是 | 继承自 TH13 |
| 440 | ins_440 | f (r) | Sets caller's absolute movement angle to %1. | 是 | 继承自 TH14 |
| 441 | ins_441 | SSf (time, mode, r) | Same as ins_440, but the change is applied in %1 frames using mode %2. | 是 | 继承自 TH14 |
| 442 | ins_442 | f (r) | Sets caller's relative movement angle to %1. | 是 | 继承自 TH14 |
| 443 | ins_443 | SSf (time, mode, r) | Same as ins_442, but the change is applied in %1 frames using mode %2. | 是 | 继承自 TH14 |
| 444 | ins_444 | f (spd) | Sets caller's absolute movement speed to %1. | 是 | 继承自 TH14 |
| 445 | ins_445 | SSf (time, mode, spd) | Same as ins_444, but the change is applied in %1 frames using mode %2. | 是 | 继承自 TH14 |
| 446 | ins_446 | f (spd) | Sets caller's relative movement speed to %1. | 是 | 继承自 TH14 |
| 447 | ins_447 | SSf (time, mode, spd) | Same as ins_446, but the change is applied in %1 frames using mode %2. | 是 | 继承自 TH14 |

### TH14.3 指令：敌机属性与杂项 / Enemy property management and other miscellaneous things

| ID | 助记名 | 参数 | 说明 | 文档化 | 来源 |
| --- | --- | --- | --- | --- | --- |
| 500 | ins_500 | ff (w, h) | Sets caller's hurtbox width to %1 and height to %2. | 是 | 继承自 TH13 |
| 501 | ins_501 | ff (w, h) | Sets caller's hitbox width to %1 and height to %2. | 是 | 继承自 TH13 |
| 502 | ins_502 | S (n) | Sets flag(s) according to %1. Refer to the [flag table](#s=modding/flags) for exact values. | 是 | 继承自 TH13 |
| 503 | ins_503 | S (n) | Clears flag(s) according to %1. Refer to the [flag table](#s=modding/flags) for exact values. | 是 | 继承自 TH13 |
| 504 | ins_504 | ffff (x, y, w, h) | Sets caller's movement limit rectangle: (%1,%2) are the coordinates of the center of the rect, while %3, %4 are width and height of it. | 是 | 继承自 TH13 |
| 505 | ins_505 | — | Removes caller's movement limit. | 是 | 继承自 TH13 |
| 506 | ins_506 | — | Clears caller's extra item drop. | 是 | 继承自 TH13 |
| 507 | ins_507 | SS (type, amount) | Adds %2 items of type %1 to caller's extra drop. Item type table will be made in the future. | 是 | 继承自 TH13 |
| 508 | ins_508 | ff (w, h) | Sets caller's item drop area width to %1 and height to %2. | 是 | 继承自 TH13 |
| 509 | ins_509 | — | Drops all items the caller has. Has no effect in spell practice. | 是 | 继承自 TH13 |
| 510 | ins_510 | S (type) | Sets caller's main drop to %1. | 是 | 继承自 TH13 |
| 511 | ins_511 | S (hp) | Sets caller's current HP and max HP to %1. | 是 | 继承自 TH13 |
| 512 | ins_512 | S (a) | If %1 is 0, activates boss mode and makes the caller the main boss. If %1 > 0, it makes the caller the secondary boss. If %1 is -1, ends boss mode. | 是 | 继承自 TH13 |
| 513 | ins_513 | — | Resets boss timer. | 是 | 继承自 TH13 |
| 514 | ins_514 | SSSm (slot, hp, time, sub) | Sets an interrupt on slot %1 (not sure how many slots there are) - once caller's hp reaches %2 or %3 frames have passed since this was called, caller will terminate all subs it's currently running and execute sub %4. | 是 | 继承自 TH13 |
| 515 | ins_515 | S (time) | Makes the caller completely invulnerable for %1 frames. | 是 | 继承自 TH13 |
| 516 | ins_516 | S (id) | Plays sound %1. Sound id table will be added in the future. | 是 | 继承自 TH13 |
| 517 | ins_517 | SSS (time, startIntensity, endIntensity) | Activates screen shake for %1 frames. %2 is the starting intensity and %3 is the ending intensity. The larger the intensity, the more the screen shakes. | 是 | 继承自 TH13 |
| 518 | ins_518 | S (dialogueId) | Starts a dialogue, %1 is the ID of an entry in the .msg file. Apart from that, has the effect ins_525. | 是 | 继承自 TH13 |
| 519 | ins_519 | — | Waits until there are no dialogues active, or the running .msg script calls a certain instruction (which one?) | 否/待确认 | 继承自 TH13 |
| 520 | ins_520 | — | Waits until there are no boss enemies. | 是 | 继承自 TH13 |
| 521 | ins_521 | Sm (slot, sub) | Sets a timeout interrupt on slot %1 - when the timer reaches 0, caller will terminate all subs it's currently running and execute sub %2. | 是 | 继承自 TH13 |
| 522 | ins_522 | SSSm (id, time, unused, name) | Same as ins_537, but the difficulty number is NOT added to the id. | 是 | 继承自 TH13 |
| 523 | ins_523 | — | Ends currently active spellcard. | 是 | 继承自 TH13 |
| 524 | ins_524 | S (a) | Some jank that's responsible for showing boss name and possibly other things. In LoLK, it also ends the current chapter and begins a new one. | 否/待确认 | 继承自 TH13 |
| 525 | ins_525 | — | Kills all other enemies (unless they have a flag that prevents that set). | 是 | 继承自 TH13 |
| 526 | ins_526 | f (r) | Makes bullets generated by the caller not spawn if they are in radius %1 around the player. | 是 | 继承自 TH13 |
| 527 | ins_527 | SfS (slot, hp, c) | Sets a new life marker on slot %1, %2 determines where the marker will appear on the health bar (if %2=1000.0f and the enemy has 2000 hp, the marker will split the hp bar in half). %3 is an RGB value of unknown use (possibly leftover from earlier ECL versions) | 是 | 继承自 TH13 |
| 528 | ins_528 | SSSm (id, time, unused, name) | No difference from ins_522, unused. | 是 | 继承自 TH13 |
| 529 | ins_529 | ffff (var, a, b, c) | Sets %1 to %2 if rank is low, %3 if rank is average or %4 if rank is high. | 是 | 继承自 TH13 |
| 530 | ins_530 | ffffff (var, a, b, c, d, e) | Sets %1 to %2 if rank is very low, %3 if rank is low, %4 if rank is average, %5 if rank is high or %6 if rank is very high. | 是 | 继承自 TH13 |
| 531 | ins_531 | fff (var, a, b) | Sets %1 to %2 if rank is low or %3 if rank is high. | 是 | 继承自 TH13 |
| 532 | ins_532 | SSSS (var, a, b, c) | Sets %1 to %2 if rank is low, %3 if rank is average or %4 if rank is high. | 是 | 继承自 TH13 |
| 533 | ins_533 | SSSSSS (var, a, b, c, d, e) | Sets %1 to %2 if rank is very low, %3 if rank is low, %4 if rank is average, %5 if rank is high or %6 if rank is very high. | 是 | 继承自 TH13 |
| 534 | ins_534 | SSS (var, a, b) | Sets %1 to %2 if rank is low or %3 if rank is high. | 是 | 继承自 TH13 |
| 535 | ins_535 | SSSSS (var, E, N, H, L) | Sets %1 to one of values provided based on difficulty. | 是 | 继承自 TH13 |
| 536 | ins_536 | fffff (var, E, N, H, L) | Sets %1 to one of values provided based on difficulty. | 是 | 继承自 TH13 |
| 537 | ins_537 | SSSm (id, time, unused, name) | Declares a spellcard with id %1 and name %4. The actual ID passed to the spell-creating function is `id + difficulty`, with easy=0, normal=1, hard=2, lunatic=3, ex=4, overdrive=5. <br>%2 determines how much time the spell circle takes to shrink (in frames), as well as how fast the spell bonus decreases. The exact formula is as follows: <br>[code] int factor = maxSCB >> 2; // maxSCB is hardcoded<br> currSCB -= (maxSCB - factor) / (%2 - 300);<br> currSCB -= currSCB % 10; [/code] <br>As you can guess, setting %2 to 300 causes a division by 0 error and crashes the game, while setting it to a value smaller than 300 causes the SCB to increase over time, instead of decreasing. %3 is unused. | 是 | 继承自 TH13 |
| 538 | ins_538 | SSSm (id, time, unused, name) | Same as ins_537, except the ID used is `id - 1 + difficulty`. | 是 | 继承自 TH13 |
| 539 | ins_539 | SSSm (id, time, unused, name) | Same as ins_537, except the ID used is `id - 2 + difficulty`. | 是 | 继承自 TH13 |
| 540 | ins_540 | S (cnt) | Sets the amount of stars displayed in the top left corner. Stars might not appear at all if there is no boss active. | 是 | 继承自 TH13 |
| 541 | ins_541 | S (time) | Disables the hitbox (but not the hurtbox) for the given amount of frames. | 是 | 继承自 TH13 |
| 542 | ins_542 | — | Makes the current spell a timeout spell (prevent spell bonus from decreasing, give capture bonus if timed out). | 是 | 继承自 TH13 |
| 543 | ins_543 | — | Unknown. | 否/待确认 | 继承自 TH13 |
| 544 | ins_544 | S (a) | Unknown, sets or clears some flag? | 否/待确认 | 继承自 TH13 |
| 545 | ins_545 | — | Cancels all lasers. | 是 | 继承自 TH13 |
| 546 | ins_546 | SS (a, script) | Sets the bomb invulnerability flag (%1=1 set, %1=0 not set), the caller's ANM script will change to %2 when a bomb is active (how does it work with ANM slots exactly?) | 是 | 继承自 TH13 |
| 547 | ins_547 | f (s) | Sets game speed to %1 of the normal speed. In ISC, enemies with flag 13 (dec=8192) set will ignore effects of this opcode. | 是 | 继承自 TH13 |
| 548 | ins_548 | SSSS (e, n, h, l) | Same as ins_23, but the wait time is chosen from the given 4 based on the difficulty. | 是 | 继承自 TH13 |
| 549 | ins_549 | S (a) | Unknown. | 否/待确认 | 继承自 TH13 |
| 550 | ins_550 | S (a) | Unknown. | 否/待确认 | 继承自 TH13 |
| 551 | ins_551 | S (a) | Unknown. | 否/待确认 | 继承自 TH13 |
| 552 | ins_552 | S (layers) | Increases layer of all ANM scripts used by the caller by %1. | 是 | 继承自 TH13 |
| 553 | ins_553 | S (id) | Makes the caller play sound %1 when hit. Sound id table will be added in the future. | 是 | 继承自 TH13 |
| 554 | ins_554 | — | Shows the stage logo from an ANM of a hardcoded name. | 是 | 继承自 TH13 |
| 555 | ins_555 | SS (var, id) | Checks if enemy of var_-9914 == %2 is still alive, and sets %1 to 1 if it is or 0 if it isn't. | 是 | 继承自 TH13 |
| 556 | ins_556 | m (sub) | Makes the caller execute sub %1 when the HP reaches 0. Keep in mind that the caller is already marked for deletion at the point when the sub actually executes, so if you put waiting there the sub will not execute fully (because the caller will be deleted) | 是 | 继承自 TH13 |
| 557 | ins_557 | SSSff (time, mode, color, start, end) | Same as STD ins_9, that is, fogTime. Refer to [the STD instruction table](#s=modding/std-ins) for details. | 是 | 继承自 TH13 |
| 558 | ins_558 | S (state) | Literally the exact same instruction as ins_424. | 是 | 继承自 TH13 |
| 559 | ins_559 | S (limit) | Set the maximum number of enemies that can be present. New enemies will fail to spawn if the cap is reached. Default is 99999. | 是 | 继承自 TH13 |
| 560 | ins_560 | ff (r, s) | Unknown. | 否/待确认 | 继承自 TH13 |
| 561 | ins_561 | — | Makes the caller execute the sub set with ins_556. If there is no such sub set, the caller dies instead (exactly the same as if the player shot down the caller, that is, items are dropped, death sound plays etc) | 是 | 继承自 TH13 |
| 562 | ins_562 | — | Same as ins_509, but item spawning will not be blocked in spell practice. | 是 | 继承自 TH13 |
| 563 | ins_563 | S (flagState) | Sets [flag 12](#s=modding/flags) (decimal 4096), which controls whether the hitbox and hurtbox is a rectangle. If %1 is 1, collision is a rectangle. If %1 is 0, collision is elliptical. | 是 | 继承自 TH14 |
| 564 | ins_564 | f (angle) | Rotates the hitbox and hurtbox of the enemy (note: the hitbox rotation is really janky, but hurtbox rotates fine). Has no effect unless the enemy uses rectangular collision. | 是 | 继承自 TH14 |
| 565 | ins_565 | f (red) | Sets caller's damage reduction when a bomb is active, 0.0f means no damage at all, 1.0f is full damage, negative values will make the enemy heal when you bomb. | 是 | 继承自 TH14 |
| 566 | ins_566 | () | Unknown (does it even exist?) | 否/待确认 | 继承自 TH14 |
| 567 | ins_567 | S (a) | Unknown. | 否/待确认 | 继承自 TH14 |
| 568 | ins_568 | S (state) | Enables/disables spell card damage reduction, if %1 is 1 it's enabled, if it's 0 it's disabled. Can be used outside of spell cards. | 是 | 继承自 TH14 |

### TH14.3 指令：子弹创建与删除 / Bullet creation and deletion

| ID | 助记名 | 参数 | 说明 | 文档化 | 来源 |
| --- | --- | --- | --- | --- | --- |
| 600 | ins_600 | S (etId) | Resets bullet manager %1 to default properties. | 是 | 继承自 TH13 |
| 601 | ins_601 | S (etId) | Shoots bullet(s) using properties from bullet manager %1. | 是 | 继承自 TH13 |
| 602 | ins_602 | SSS (etId, type, color) | Sets bullet type and color of bullet manager %1. Pre-th15 bullet types are yet to be documented. | 是 | 继承自 TH13 |
| 603 | ins_603 | Sff (etId, x, y) | Sets the relative offset of bullets spawned by bullet manager %1 to (%2,%3). | 是 | 继承自 TH13 |
| 604 | ins_604 | Sff (etId, angle1, angle2) | Sets angle1 and angle2 of bullet manager %1. | 是 | 继承自 TH13 |
| 605 | ins_605 | Sff (etId, speed1, speed2) | Sets speed1 and speed2 of bullet manager %1. | 是 | 继承自 TH13 |
| 606 | ins_606 | SSS (etId, count1, count2) | Sets count1 and count2 of bullet manager %1. | 是 | 继承自 TH13 |
| 607 | ins_607 | SS (etId, aim) | Sets aim mode of bullet manager %1. | 是 | 继承自 TH13 |
| 608 | ins_608 | SSS (etId, sound1, sound2) | Sets sound1 and sound2 of bullet manager %1 (sound effect table is TODO). sound1 plays when the bullet manager fires a bullet, while sound2 plays when a bullet fired by the bullet manager does certain transformations. Set to -1 for no sound. | 是 | 继承自 TH13 |
| 609 | ins_609 | SSSSSSff (etId, index, async, type, a, b, r, s) | Sets bullet transformation of bullet manager %1, transformation explanation will be added in the future. | 是 | 继承自 TH13 |
| 610 | ins_610 | SSSSSSSSffff (etId, index, async, type, a, b, c, d, r, s, m, n) | Same as ins_609, but takes more arguments for certain transformation types. | 是 | 继承自 TH13 |
| 611 | ins_611 | SSSSSff (etId, async, type, a, b, r, s) | Adds bullet transformation to bullet manager %1, transformation explanation will be added in the future. | 是 | 继承自 TH13 |
| 612 | ins_612 | SSSSSSSffff (etId, async, type, a, b, c, d, r, s, m, n) | Same as ins_611, but takes more arguments for certain transformation types. | 是 | 继承自 TH13 |
| 613 | ins_613 | — | Clears all bullets. | 是 | 继承自 TH13 |
| 614 | ins_614 | SS (etIdDest, etIdSrc) | Copies everything from bullet manager %2 into bullet manager %1. Warning: this instruction is partially broken and does NOT copy the index next ins_611/ins_612 transformations will be added at. | 是 | 继承自 TH13 |
| 615 | ins_615 | f (r) | Clears all bullets in a circle of radius %1 around the caller, and turns them into cancel items. | 是 | 继承自 TH13 |
| 616 | ins_616 | f (r) | Clears all bullets in a circle of radius %1 around the caller without turning them into cancel items. | 是 | 继承自 TH13 |
| 617 | ins_617 | Sffffff (etId, spd1l, spd1m, spd1h, spd2l, spd2m, spd2h) | Sets speed1 and speed2 of bullet manager %1 to two of the values provided, based on ingame rank (l=low, m=medium, h=high) | 是 | 继承自 TH13 |
| 618 | ins_618 | Sffffffffff (etId, spd1l, spd1ml, spd1m, spd1mh, spd1h, spd2l, spd2ml, spd2m, spd2mh, spd2h) | Sets speed1 and speed2 of bullet manager %1 to two of the values provided, based on ingame rank (l=low, ml=medium-low, m=medium, mh=medium-high, h=high) | 是 | 继承自 TH13 |
| 619 | ins_619 | Sffff (etId, spd1l, spd1h, spd2l, spd2h) | Sets speed1 and speed2 of bullet manager %1 to two of the values provided, based on ingame rank (l=low, h=high) | 是 | 继承自 TH13 |
| 620 | ins_620 | SSSSSSS (etId, cnt1l, cnt1m, cnt1h, cnt2l, cnt2m, cnt2h) | Sets count1 and count2 of bullet manager %1 to two of the values provided, based on ingame rank (l=low, m=medium, h=high) | 是 | 继承自 TH13 |
| 621 | ins_621 | SSSSSSSSSSS (etId, cnt1l, cnt1ml, cnt1m, cnt1mh, cnt1h, cnt2l, cnt2ml, cnt2m, cnt2mh, cnt2h) | Sets count1 and count2 of bullet manager %1 to two of the values provided, based on ingame rank (l=low, ml=medium-low, m=medium, mh=medium-high, h=high) | 是 | 继承自 TH13 |
| 622 | ins_622 | SSSSS (etId, cnt1l, cnt1h, cnt2l, cnt2h) | Sets count1 and count2 of bullet manager %1 to two of the values provided, based on ingame rank (l=low, h=high) | 是 | 继承自 TH13 |
| 623 | ins_623 | fff (var, x, y) | Gets angle to the player from coordinates (%2,%3) and stores it in %1. | 是 | 继承自 TH13 |
| 624 | ins_624 | Sffffffff (etId, spd1e, spd1n, spd1h, spd1l, spd2e, spd2n, spd2h, spd2l) | Sets speed1 and speed2 of bullet manager %1 to 2 of the values provided, based on the difficulty (e=easy, n=normal, h=hard, l=lunatic) | 是 | 继承自 TH13 |
| 625 | ins_625 | SSSSSSSSS (etId, cnt1e, cnt1n, cnt1h, cnt1l, cnt2e, cnt2n, cnt2h, cnt2l) | Sets count1 and count2 of bullet manager %1 to 2 of the values provided, based on the difficulty (e=easy, n=normal, h=hard, l=lunatic) | 是 | 继承自 TH13 |
| 626 | ins_626 | Sff (etId, angle, radius) | Sets the relative offset of bullets spawned by bullet manager %1 to (cos(%2)\*%3,sin(%2)\*%3). Stacks with ins_603. | 是 | 继承自 TH13 |
| 627 | ins_627 | Sf (etId, dist) | Sets distance of bullets spawned by bullet manager %1 to %2 (that is, when a bullet is spawned it moves by %2 using its current angle). | 是 | 继承自 TH13 |
| 628 | ins_628 | Sff (etId, x, y) | Sets the absolute offset of bullets spawned by bullet manager %1 to (%2,%3). | 是 | 继承自 TH13 |
| 629 | ins_629 | fS (r, color) | Sets caller's fog's radius to %1 and color to %2 (RGB value in reverse order). This resets the fog completely, that is, every time it's called the fog spawn animation plays. | 是 | 继承自 TH13 |
| 630 | ins_630 | S (switch) | Sets execution pointer of the STD script to where STD ins_16(%1) is (%1 must be the same), basically same concept as ins_317. | 是 | 继承自 TH13 |
| 631 | ins_631 | S (time) | Hides boss lifebar for %1 frames. | 是 | 继承自 TH13 |
| 632 | ins_632 | S (id) | Sets a function that the game will execute every frame from a set of hardcoded functions that differs between games. | 是 | 继承自 TH13 |
| 633 | ins_633 | S (state) | Sets the external damage flag to %1. Caller probably needs to be the main boss for this to work - with this flag set, the caller gets damaged by the value stored in var_-9940 every frame, and then resets the value. This allows other enemies to damage the boss by incrementing the aforementioned variable, used in LoLK by Sagume (and also happens to be the main cause of the Sagume skip glitch) | 是 | 继承自 TH13 |
| 634 | ins_634 | S (id) | Make the caller use a special function for determining collision with the player. TODO: create a list of functions and their IDs | 是 | 继承自 TH13 |
| 635 | ins_635 | f (r) | Same as ins_615, but doesn't clear bullets with bomb invulnerability. | 是 | 继承自 TH13 |
| 636 | ins_636 | f (r) | Same as ins_616, but doesn't clear bullets with bomb invulnerability. | 是 | 继承自 TH13 |
| 637 | ins_637 | S (id) | Same as ins_632, except the function is called just once instead of every frame. | 是 | 继承自 TH13 |
| 638 | ins_638 | S (n) | Adds %1 to score (or subtracts if %1 is negative). There is no lower boundary check, so if this causes score to go below 0, an underflow happens. | 是 | 继承自 TH13 |
| 639 | ins_639 | S (id) | Same as ins_632, except it sets an unknown flag to 1 (ins_632 sets it to 0) | 是 | 继承自 TH13 |
| 640 | ins_640 | SSm (etId, index, s) | Sets the string parameter of transform on index %2 in bullet manager %1 to %3, transformations will be explained separately later. | 是 | 继承自 TH13 |
| 641 | ins_641 | S (etId) | Subtracts 1 from the index used by ins_611 and ins_612, unless it's already 0. This basically changes where the next transformation will be appended. | 是 | 继承自 TH14 |

### TH14.3 指令：激光创建 / Laser creation

| ID | 助记名 | 参数 | 说明 | 文档化 | 来源 |
| --- | --- | --- | --- | --- | --- |
| 700 | ins_700 | Sffff (etId, init_length, final_length, unknown_arg_3, width) | Sets basic parameters of the laser. %4 has something to do with the length of straight line lasers (investigation needed), but doesn't do anything for other laser types. For curvy lasers, the only used argument is %5, and length is specified with ins_701 instead. | 是 | 继承自 TH13 |
| 701 | ins_701 | SSSSSS (edId, startup_time, expand_time, duration, shrink_time, init_flags) | Sets timing for infinite lasers. %6 sets the initial flags for a laser, but these flags are unknown at the moment. For curvy lasers, the %2 argument instead specifies the length of the laser. | 是 | 继承自 TH13 |
| 702 | ins_702 | S (edId) | Shoots a straight line laser. | 是 | 继承自 TH13 |
| 703 | ins_703 | SS (etId, laser_id) | Shoots an infinite laser. %2 is a number that's used to identify this particular laser instance, so that it can be referred to in other instructions. | 是 | 继承自 TH13 |
| 704 | ins_704 | Sff (laser_id, x, y) | Sets the position of the infinite laser pointed to by %1. | 是 | 继承自 TH13 |
| 705 | ins_705 | Sff (laser_id, x_speed, y_speed) | Sets the offset velocity of the infinite laser pointed to by %1. The laser's position will change by %2 and %3 every frame. | 是 | 继承自 TH13 |
| 706 | ins_706 | Sf (laser_id, speed) | Sets the speed of the infinite laser pointed to by %1. | 是 | 继承自 TH13 |
| 707 | ins_707 | Sf (laser_id, width) | Sets the width of the infinite laser pointed to by %1. | 是 | 继承自 TH13 |
| 708 | ins_708 | Sf (laser_id, angle) | Sets the angle of the infinite laser pointed to by %1. | 是 | 继承自 TH13 |
| 709 | ins_709 | Sf (laser_id, angular_vel) | Sets the angular velocity of the infinite laser pointed to by %1. The laser's angle will change by %2 every frame. | 是 | 继承自 TH13 |
| 710 | ins_710 | S (laser_id) | Clears the laser pointed to by %1. | 是 | 继承自 TH13 |
| 711 | ins_711 | S (etId) | Shoots a curvy laser. | 是 | 继承自 TH13 |
| 712 | ins_712 | ff (w, h) | Cancels all bullets in rectangle of width %1 and height %2. The area is affected by rotation set by ins_564. | 是 | 继承自 TH14 |
| 713 | ins_713 | SS (etId, laser_id) | Shoots a laser 'beam', a laser type used by marisa in GFW. Broken since this laser type does not exist outside of GFW. | 是 | 继承自 TH13 |
| 714 | ins_714 | SS (laser_id, unknown) | Does something with a laser beam pointed to by %1. Broken since this laser type does not exist outside of GFW. | 是 | 继承自 TH13 |

### TH14.3 指令：敌机交互 / Enemy interaction

| ID | 助记名 | 参数 | 说明 | 文档化 | 来源 |
| --- | --- | --- | --- | --- | --- |
| 800 | ins_800 | Sm (id, sub) | Makes enemy with var_-9914 == %1 stop all subs it's running and execute sub %2 (works like an interrupt). This will NOT make the enemy execute the sub right as this instruction is called, the new sub will be executed when the game handles the given enemy, which might be later on the same frame or on the next frame. Using this to make the caller interrupt itself can make the game explode. | 是 | 继承自 TH13 |
| 801 | ins_801 | ffS (varX, varY, id) | Stores coordinates of enemy with var_-9914 == %3 in (%1,%2). | 是 | 继承自 TH13 |
| 802 | ins_802 | S (slot) | For all existing bosses, trigger the interrupt set by ins_514 on slot %1. Does not change the HP to the one set in ins_514. | 是 | 继承自 TH13 |

### TH14.3 指令：调试 / Debug

| ID | 助记名 | 参数 | 说明 | 文档化 | 来源 |
| --- | --- | --- | --- | --- | --- |
| 900 | ins_900 | — | 未在 Priw8 表中记录/待确认 | 否/待确认 | — |
| 901 | ins_901 | — | 未在 Priw8 表中记录/待确认 | 否/待确认 | — |
| 902 | ins_902 | — | 未在 Priw8 表中记录/待确认 | 否/待确认 | — |

### TH14.3 指令：游戏特有 / Game specific

| ID | 助记名 | 参数 | 说明 | 文档化 | 来源 |
| --- | --- | --- | --- | --- | --- |
| 1000 | ins_1000 | — | 未在 Priw8 表中记录/待确认 | 否/待确认 | — |
| 1001 | ins_1001 | — | 未在 Priw8 表中记录/待确认 | 否/待确认 | — |
| 1002 | ins_1002 | — | 未在 Priw8 表中记录/待确认 | 否/待确认 | — |
| 1003 | ins_1003 | — | 未在 Priw8 表中记录/待确认 | 否/待确认 | — |
| 1004 | ins_1004 | — | 未在 Priw8 表中记录/待确认 | 否/待确认 | — |
| 1005 | ins_1005 | — | 未在 Priw8 表中记录/待确认 | 否/待确认 | — |
| 1006 | ins_1006 | — | 未在 Priw8 表中记录/待确认 | 否/待确认 | — |

### TH14.3 变量

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
| -9959 | [-9959] | int | 只读 | global/全局 | Difficulty (E=0, N=1, H=2, L=3, EX=4, O=5) | 是 | 继承自 TH10 |
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
| -9909 | [-9909] | int | 只读 | local/敌机局部 | Enemy ID of the parent enemy. | 是 | 继承自 TH12.8 |
| -9908 | [-9908] | int | 只读 | global/全局 | Amount of killable enemies alive (that is, doesn't include hitboxless/intangible enemies etc). | 是 | 继承自 TH13 |
| -9907 | [-9907] | int | 只读 | global/全局 | Spellcard ID, used by spell practice. Unknown meaning in LoLK. | 是 | 继承自 TH13 |

