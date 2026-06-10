# ECL 分游戏速查表

> 根据 `th062/ecl-web.txt` 中列出的 Priw8 ECL 指令表、变量表、flags/MERLIN 文档，以及本地提供的 THBWiki 文本 `th062/ecl*.txt` 整理。具体 opcode/变量主表以 Priw8 源数据为准，THBWiki 中文说明作为代际补充与交叉索引。

## 阅读说明

- `ID` 为 ECL opcode 或变量编号；`助记名` 来自 priw8 的 eclmap。
- `参数` 中前半为格式串，括号内为参数名；`S/$` 常见为整数，`f/%` 常见为浮点，`o` 常见为跳转 offset/label。
- `来源` 表示该条在 Priw8 继承链中的定义来源；第四世代大量指令会从 TH13 继承。
- 变量表只列有记录的变量；范围内未列出的编号通常为空洞或未调查。

## 来源网页索引

| 序号 | 用途 | URL |
| --- | --- | --- |
| 1 | Priw8 指令表 | https://priw8.github.io/#s=modding/ins&table=8 |
| 2 | Priw8 指令表 | https://priw8.github.io/#s=modding/ins&table=13 |
| 3 | Priw8 指令表 | https://priw8.github.io/#s=modding/ins&table=14 |
| 4 | Priw8 指令表 | https://priw8.github.io/#s=modding/ins&table=14.3 |
| 5 | Priw8 指令表 | https://priw8.github.io/#s=modding/ins&table=15 |
| 6 | Priw8 指令表 | https://priw8.github.io/#s=modding/ins&table=16 |
| 7 | Priw8 指令表 | https://priw8.github.io/#s=modding/ins&table=16.5 |
| 8 | Priw8 指令表 | https://priw8.github.io/#s=modding/ins&table=17 |
| 9 | Priw8 指令表 | https://priw8.github.io/#s=modding/ins&table=18 |
| 10 | Priw8 指令表 | https://priw8.github.io/#s=modding/ins&table=18.5 |
| 11 | Priw8 变量表 | https://priw8.github.io/#s=modding/vars&table=8 |
| 12 | Priw8 变量表 | https://priw8.github.io/#s=modding/vars&table=10 |
| 13 | Priw8 变量表 | https://priw8.github.io/#s=modding/vars&table=11 |
| 14 | Priw8 变量表 | https://priw8.github.io/#s=modding/vars&table=12 |
| 15 | Priw8 变量表 | https://priw8.github.io/#s=modding/vars&table=12.5 |
| 16 | Priw8 变量表 | https://priw8.github.io/#s=modding/vars&table=12.8 |
| 17 | Priw8 变量表 | https://priw8.github.io/#s=modding/vars&table=13 |
| 18 | Priw8 变量表 | https://priw8.github.io/#s=modding/vars&table=14 |
| 19 | Priw8 变量表 | https://priw8.github.io/#s=modding/vars&table=14.3 |
| 20 | Priw8 变量表 | https://priw8.github.io/#s=modding/vars&table=15 |
| 21 | Priw8 变量表 | https://priw8.github.io/#s=modding/vars&table=16 |
| 22 | Priw8 变量表 | https://priw8.github.io/#s=modding/vars&table=16.5 |
| 23 | Priw8 变量表 | https://priw8.github.io/#s=modding/vars&table=17 |
| 24 | 敌机 flags | https://priw8.github.io/#s=modding/flags |
| 25 | MERLIN 敌机常量 | https://priw8.github.io/#s=MERLIN/doc/globals/enemy-etc |
| 26 | THBWiki ECL | https://www.thwiki.cc/%E8%84%9A%E6%9C%AC%E5%AF%B9%E7%85%A7%E8%A1%A8/ECL |
| 27 | THBWiki ECL | https://www.thwiki.cc/%E8%84%9A%E6%9C%AC%E5%AF%B9%E7%85%A7%E8%A1%A8/ECL/%E7%AC%AC%E4%B8%80%E4%B8%96%E4%BB%A3 |
| 28 | THBWiki ECL | https://www.thwiki.cc/%E8%84%9A%E6%9C%AC%E5%AF%B9%E7%85%A7%E8%A1%A8/ECL/%E7%AC%AC%E4%BA%8C%E4%B8%96%E4%BB%A3 |
| 29 | THBWiki ECL | https://www.thwiki.cc/%E8%84%9A%E6%9C%AC%E5%AF%B9%E7%85%A7%E8%A1%A8/ECL/%E7%AC%AC%E4%B8%89%E4%B8%96%E4%BB%A3 |
| 30 | THBWiki ECL | https://www.thwiki.cc/%E8%84%9A%E6%9C%AC%E5%AF%B9%E7%85%A7%E8%A1%A8/ECL/%E7%AC%AC%E5%9B%9B%E4%B8%96%E4%BB%A3 |

## THBWiki 本地文本索引

| 代际 | 标题 | 文件 | 适用范围 | 抽取 opcode 数 | 概述摘要 |
| --- | --- | --- | --- | --- | --- |
| 总览 | 脚本对照表/ECL 总览 | th062/ecl.txt | 见总览页面。 | 0 | 文件为空。 |
| 第一世代 | THBWiki 第一世代 ECL | th062/ecl1.txt | 红魔乡、妖妖梦、永夜抄、花映塚、文花帖；其中妖妖梦/永夜抄/花映塚/文花帖存在新增差异。 | 12 | 本对照表是Zun的第一代ecl脚本的对照表,适用于红妖永花,文花帖 妖妖梦妖妖梦单独的ecl脚本表 粉色代表妖妖梦新增 深紫色代表永夜抄新增 绿色代表花映塚新增 棕色代表文花帖新增 红色代表功能未知，需要测试和研究 蓝色代表虽然并未完全解读，但是大体功能已经知道，且此函数用途十分有限 灰色代表是前作特殊地点使用过之后完全被抛弃的 注：永夜抄中单关脚本和符卡练习脚本是分开的 |
| 第二世代 | THBWiki 第二世代 ECL | th062/ecl2.txt | 风神录、地灵殿；地灵殿存在新增指令。 | 95 | 本对照表是Zun的第二代ecl脚本的对照表,适用于风神录和地灵殿 对于其他作的参考 第一代ecl脚本红妖永花,文花帖.由于与此表差异很大,故不能作任何参考. 第三代ECL脚本对应星，文花帖ds和大战争 第四代ECL脚本对应城，天邪鬼，绀珠传 第四代中300对应此表中256,400对应此表中300，500对应此表中400，600对应此表中500，其余大体可以按顺序对照. 以下即是所有存在的ins,是读取汇编所获得的 绿色代表地灵殿中新增，风神录中不存在 红色代表功能未知，需要测试和研究 蓝色代表虽然并未完全解读，但是大体功能已经知道，且此函数用途十分有限 灰色代表是前作特殊地点使用过之后完全被抛弃的 |
| 第三世代 | THBWiki 第三世代 ECL | th062/ecl3.txt | 星莲船、Double Spoiler、妖精大战争；THBWiki 以 TH12 为主体，DS/大战争有少量差异。 | 126 | 本对照表是Zun的第三代ecl脚本的对照表,适用于星，ds，dzz3作 以下均是基于th12 星莲船的脚本制成， 文花帖DS和妖精大战争与有一小部分不同 对于其他作的参考 第一代ecl脚本红妖永花,文花帖.由于与此表差异很大,故不能作任何参考. 第二代ecl脚本对应风地 第二代中280对应此表中300，320对应此表中400，400对应此表中500，其余大体可以按顺序对照. 第三代ecl脚本对应星，文花帖ds和大战争 第四代ecl脚本对应城，天邪鬼，绀珠传 第四代中300对应此表中256,400对应此表中300，500对应此表中400，600对应此表中500，其余大体可以按顺序对照. 提取zun脚本的工具是touhou toolkit. 以下即是所有存在的ins,是读取汇编所获得的 红色代表功能未知，需要测试和研究 蓝色代表虽然并未完全解读，但是大体功能已经知道，且此函数用途十分有限 灰色代表是前作特殊地点使用过之后完全被抛弃的 棕色部分是文花帖DS新增 青色部分是妖精大战争新增 |
| 第四世代 | THBWiki 第四世代 ECL | th062/ecl4.txt | 神灵庙之后的整数作与小数作；页面标注辉针城、天邪鬼、绀珠传、天空璋、噩梦日记、鬼形兽等新增差异。 | 209 | 本对照表是ZUN的第四代ECL脚本的对照表,适用于神之后的所有作品 红色代表功能未知，需要测试和研究 蓝色代表虽然并未完全解读，但是大体功能已经知道，且此函数用途十分有限 灰色代表是前作特殊地点使用过之后完全被抛弃的 棕色部分是辉针城新增 青色部分是天邪鬼新增 绿色部分是绀珠传新增 紫色部分是天空璋新增 洋红部分是鬼形兽新增 |

## 分游戏文档索引

| 游戏 | 作品 | 独立文档 | 包含内容 |
| --- | --- | --- | --- |
| TH08 | 东方永夜抄 | th062/ecl-by-game/th08-ecl.md | 对应世代 THBWiki 中文表、全局 flags、该游戏 Priw8 指令/变量 |
| TH10 | 东方风神录 | th062/ecl-by-game/th10-ecl.md | 对应世代 THBWiki 中文表、全局 flags、该游戏 Priw8 指令/变量 |
| TH11 | 东方地灵殿 | th062/ecl-by-game/th11-ecl.md | 对应世代 THBWiki 中文表、全局 flags、该游戏 Priw8 指令/变量 |
| TH12 | 东方星莲船 | th062/ecl-by-game/th12-ecl.md | 对应世代 THBWiki 中文表、全局 flags、该游戏 Priw8 指令/变量 |
| TH12.5 | Double Spoiler | th062/ecl-by-game/th12_5-ecl.md | 对应世代 THBWiki 中文表、全局 flags、该游戏 Priw8 指令/变量 |
| TH12.8 | 妖精大战争 | th062/ecl-by-game/th12_8-ecl.md | 对应世代 THBWiki 中文表、全局 flags、该游戏 Priw8 指令/变量 |
| TH13 | 东方神灵庙 | th062/ecl-by-game/th13-ecl.md | 对应世代 THBWiki 中文表、全局 flags、该游戏 Priw8 指令/变量 |
| TH14 | 东方辉针城 | th062/ecl-by-game/th14-ecl.md | 对应世代 THBWiki 中文表、全局 flags、该游戏 Priw8 指令/变量 |
| TH14.3 | 弹幕天邪鬼 | th062/ecl-by-game/th14_3-ecl.md | 对应世代 THBWiki 中文表、全局 flags、该游戏 Priw8 指令/变量 |
| TH15 | 东方绀珠传 | th062/ecl-by-game/th15-ecl.md | 对应世代 THBWiki 中文表、全局 flags、该游戏 Priw8 指令/变量 |
| TH16 | 东方天空璋 | th062/ecl-by-game/th16-ecl.md | 对应世代 THBWiki 中文表、全局 flags、该游戏 Priw8 指令/变量 |
| TH16.5 | 秘封噩梦日记 | th062/ecl-by-game/th16_5-ecl.md | 对应世代 THBWiki 中文表、全局 flags、该游戏 Priw8 指令/变量 |
| TH17 | 东方鬼形兽 | th062/ecl-by-game/th17-ecl.md | 对应世代 THBWiki 中文表、全局 flags、该游戏 Priw8 指令/变量 |
| TH18 | 东方虹龙洞 | th062/ecl-by-game/th18-ecl.md | 对应世代 THBWiki 中文表、全局 flags、该游戏 Priw8 指令/变量 |
| TH18.5 | 弹幕狂们的黑市 | th062/ecl-by-game/th18_5-ecl.md | 对应世代 THBWiki 中文表、全局 flags、该游戏 Priw8 指令/变量 |

## 游戏总览

| 游戏 | 作品 | 代际/体系 | 指令表覆盖 | 变量表覆盖 | 摘要 |
| --- | --- | --- | --- | --- | --- |
| TH08 | 东方永夜抄 | 第一世代 | 有 | 有 | 普通指令 185 条，时间轴指令 17 条；已说明 171/202。主要分组：普通指令 / Normal。 变量范围 10000..10100；本文列出有说明/命名记录的 100 条，未列空洞/未知项。 |
| TH10 | 东方风神录 | 第二世代 | 未列 | 有 | ecl-web.txt 未列出该作 Priw8 指令表；通常沿用相近世代/上一作格式，本文仅列变量。 变量范围 -10000..-9950；本文列出有说明/命名记录的 51 条，未列空洞/未知项。 |
| TH11 | 东方地灵殿 | 第二世代 | 未列 | 有 | ecl-web.txt 未列出该作 Priw8 指令表；通常沿用相近世代/上一作格式，本文仅列变量。 变量范围 -10000..-9932；本文列出有说明/命名记录的 69 条，未列空洞/未知项。 |
| TH12 | 东方星莲船 | 第三世代 | 未列 | 有 | ecl-web.txt 未列出该作 Priw8 指令表；通常沿用相近世代/上一作格式，本文仅列变量。 变量范围 -10000..-9930；本文列出有说明/命名记录的 71 条，未列空洞/未知项。 |
| TH12.5 | Double Spoiler | 第三世代 | 未列 | 有 | ecl-web.txt 未列出该作 Priw8 指令表；通常沿用相近世代/上一作格式，本文仅列变量。 变量范围 -10000..-9910；本文列出有说明/命名记录的 91 条，未列空洞/未知项。 |
| TH12.8 | 妖精大战争 | 第三世代 | 未列 | 有 | ecl-web.txt 未列出该作 Priw8 指令表；通常沿用相近世代/上一作格式，本文仅列变量。 变量范围 -10000..-9909；本文列出有说明/命名记录的 92 条，未列空洞/未知项。 |
| TH13 | 东方神灵庙 | 第四世代 | 有 | 有 | 普通指令 297 条；已说明 242/297。主要分组：系统/流程/栈/算术 / System；敌机创建与 ANM 管理 / Enemy creation and ANM script management；移动管理 / Movement management；敌机属性与杂项 / Enemy property management and other miscellaneous things；子弹创建与删除 / Bullet creation and deletion；激光创建 / Laser creation；敌机交互 / Enemy interaction；调试 / Debug；游戏特有 / Game specific。 变量范围 -10000..-9907；本文列出有说明/命名记录的 94 条，未列空洞/未知项。 |
| TH14 | 东方辉针城 | 第四世代 | 有 | 有 | 普通指令 316 条；已说明 257/316。主要分组：系统/流程/栈/算术 / System；敌机创建与 ANM 管理 / Enemy creation and ANM script management；移动管理 / Movement management；敌机属性与杂项 / Enemy property management and other miscellaneous things；子弹创建与删除 / Bullet creation and deletion；激光创建 / Laser creation；敌机交互 / Enemy interaction；调试 / Debug；游戏特有 / Game specific。 变量范围 -10000..-9907；本文列出有说明/命名记录的 94 条，未列空洞/未知项。 |
| TH14.3 | 弹幕天邪鬼 | 第四世代 | 有 | 有 | 普通指令 319 条；已说明 257/319。主要分组：系统/流程/栈/算术 / System；敌机创建与 ANM 管理 / Enemy creation and ANM script management；移动管理 / Movement management；敌机属性与杂项 / Enemy property management and other miscellaneous things；子弹创建与删除 / Bullet creation and deletion；激光创建 / Laser creation；敌机交互 / Enemy interaction；调试 / Debug；游戏特有 / Game specific。 变量范围 -10000..-9907；本文列出有说明/命名记录的 94 条，未列空洞/未知项。 |
| TH15 | 东方绀珠传 | 第四世代 | 有 | 有 | 普通指令 319 条；已说明 257/319。主要分组：系统/流程/栈/算术 / System；敌机创建与 ANM 管理 / Enemy creation and ANM script management；移动管理 / Movement management；敌机属性与杂项 / Enemy property management and other miscellaneous things；子弹创建与删除 / Bullet creation and deletion；激光创建 / Laser creation；敌机交互 / Enemy interaction；调试 / Debug；游戏特有 / Game specific。 变量范围 -10000..-9904；本文列出有说明/命名记录的 97 条，未列空洞/未知项。 |
| TH16 | 东方天空璋 | 第四世代 | 有 | 有 | 普通指令 321 条；已说明 262/321。主要分组：系统/流程/栈/算术 / System；敌机创建与 ANM 管理 / Enemy creation and ANM script management；移动管理 / Movement management；敌机属性与杂项 / Enemy property management and other miscellaneous things；子弹创建与删除 / Bullet creation and deletion；激光创建 / Laser creation；敌机交互 / Enemy interaction；调试 / Debug；游戏特有 / Game specific。 变量范围 -10000..-9903；本文列出有说明/命名记录的 98 条，未列空洞/未知项。 |
| TH16.5 | 秘封噩梦日记 | 第四世代 | 有 | 有 | 普通指令 334 条；已说明 271/334。主要分组：系统/流程/栈/算术 / System；敌机创建与 ANM 管理 / Enemy creation and ANM script management；移动管理 / Movement management；敌机属性与杂项 / Enemy property management and other miscellaneous things；子弹创建与删除 / Bullet creation and deletion；激光创建 / Laser creation；敌机交互 / Enemy interaction；调试 / Debug；游戏特有 / Game specific。 变量范围 -10000..-9903；本文列出有说明/命名记录的 98 条，未列空洞/未知项。 |
| TH17 | 东方鬼形兽 | 第四世代 | 有 | 有 | 普通指令 347 条；已说明 260/347。主要分组：系统/流程/栈/算术 / System；敌机创建与 ANM 管理 / Enemy creation and ANM script management；移动管理 / Movement management；敌机属性与杂项 / Enemy property management and other miscellaneous things；子弹创建与删除 / Bullet creation and deletion；激光创建 / Laser creation；敌机交互 / Enemy interaction；调试 / Debug；游戏特有 / Game specific。 变量范围 -10000..-9899；本文列出有说明/命名记录的 102 条，未列空洞/未知项。 |
| TH18 | 东方虹龙洞 | 第四世代 | 有 | 未列 | 普通指令 325 条；已说明 260/325。主要分组：系统/流程/栈/算术 / System；敌机创建与 ANM 管理 / Enemy creation and ANM script management；移动管理 / Movement management；敌机属性与杂项 / Enemy property management and other miscellaneous things；子弹创建与删除 / Bullet creation and deletion；激光创建 / Laser creation；敌机交互 / Enemy interaction；调试 / Debug；游戏特有 / Game specific。 ecl-web.txt 未列出该作变量表。 |
| TH18.5 | 弹幕狂们的黑市 | 第四世代 | 有 | 未列 | 普通指令 347 条；已说明 271/347。主要分组：系统/流程/栈/算术 / System；敌机创建与 ANM 管理 / Enemy creation and ANM script management；移动管理 / Movement management；敌机属性与杂项 / Enemy property management and other miscellaneous things；子弹创建与删除 / Bullet creation and deletion；激光创建 / Laser creation；敌机交互 / Enemy interaction；调试 / Debug；游戏特有 / Game specific。 ecl-web.txt 未列出该作变量表。 |

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

## TH11 东方地灵殿

- 体系：第二世代
- 指令：ecl-web.txt 未列出该作 Priw8 指令表；通常沿用相近世代/上一作格式，本文仅列变量。
- 变量：变量范围 -10000..-9932；本文列出有说明/命名记录的 69 条，未列空洞/未知项。

### TH11 变量

| ID | 名称 | 类型 | 访问 | 作用域 | 说明 | 文档化 | 来源 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| -10000 | RAND | int | 只读 | global/全局 | Random integer, very large range. | 是 | 继承自 TH10 |
| -9999.0f | RANDF | float | 只读 | global/全局 | Random float from 0.0f to 1.0f. | 是 | 继承自 TH10 |
| -9998.0f | RANDRAD | float | 只读 | global/全局 | Random float from -pi to pi. | 是 | 继承自 TH10 |
| -9997.0f | FINAL_X | float | 只读 | local/敌机局部 | Final X position of the enemy. | 是 | 继承自 TH10 |
| -9996.0f | FINAL_Y | float | 只读 | local/敌机局部 | Final Y position of the enemy. | 是 | 继承自 TH10 |
| -9995.0f | ABS_X | float | 只读 | local/敌机局部 | Absolute X position of the enemy. | 是 | 继承自 TH10 |
| -9994.0f | ABS_Y | float | 只读 | local/敌机局部 | Absolute Y position of the enemy. | 是 | 继承自 TH10 |
| -9993.0f | REL_X | float | 只读 | local/敌机局部 | Relative X position of the enemy. | 是 | 继承自 TH10 |
| -9992.0f | REL_Y | float | 只读 | local/敌机局部 | Relative Y position of the enemy. | 是 | 继承自 TH10 |
| -9991.0f | PLAYER_X | float | 只读 | global/全局 | Player's X position. | 是 | 继承自 TH10 |
| -9990.0f | PLAYER_Y | float | 只读 | global/全局 | Player's Y position. | 是 | 继承自 TH10 |
| -9989.0f | ANGLE_PLAYER | float | 只读 | local/敌机局部 | Angle from the enemy to the player. | 是 | 继承自 TH10 |
| -9988 | TIME | int | 只读 | local/敌机局部 | Time elapsed since the enemy spawned, in frames. | 是 | 继承自 TH10 |
| -9987.0f | RANDF2 | float | 只读 | global/全局 | Random float from -1.0f to 1.0f. | 是 | 继承自 TH10 |
| -9986 | TIMEOUT | int | 只读 | global/全局 | Set to 1 by the engine when a timeout occurs. | 是 | 继承自 TH10 |
| -9985 | I0 | int | 读写 | local/敌机局部 | Local integer variable, inherited by spawned enemies. | 是 | 继承自 TH10 |
| -9984 | I1 | int | 读写 | local/敌机局部 | Local integer variable, inherited by spawned enemies. | 是 | 继承自 TH10 |
| -9983 | I2 | int | 读写 | local/敌机局部 | Local integer variable, inherited by spawned enemies. | 是 | 继承自 TH10 |
| -9982 | I3 | int | 读写 | local/敌机局部 | Local integer variable, inherited by spawned enemies. | 是 | 继承自 TH10 |
| -9981.0f | F0 | float | 读写 | local/敌机局部 | Local float variable, inherited by spawned enemies. | 是 | 继承自 TH10 |
| -9980.0f | F1 | float | 读写 | local/敌机局部 | Local float variable, inherited by spawned enemies. | 是 | 继承自 TH10 |
| -9979.0f | F2 | float | 读写 | local/敌机局部 | Local float variable, inherited by spawned enemies. | 是 | 继承自 TH10 |
| -9978.0f | F3 | float | 读写 | local/敌机局部 | Local float variable, inherited by spawned enemies. | 是 | 继承自 TH10 |
| -9977.0f | FINAL_X2 | float | 只读 | local/敌机局部 | Same as var_-9997. | 是 | 继承自 TH10 |
| -9976.0f | FINAL_Y2 | float | 只读 | local/敌机局部 | Same as var_-9996. | 是 | 继承自 TH10 |
| -9975.0f | ABS_X2 | float | 只读 | local/敌机局部 | Same as var_-9995. | 是 | 继承自 TH10 |
| -9974.0f | ABS_Y2 | float | 只读 | local/敌机局部 | Same as var_-9994. | 是 | 继承自 TH10 |
| -9973.0f | REL_X2 | float | 只读 | local/敌机局部 | Same as var_-9993. | 是 | 继承自 TH10 |
| -9972.0f | REL_Y2 | float | 只读 | local/敌机局部 | Same as var_-9992. | 是 | 继承自 TH10 |
| -9971.0f | ABS_ANGLE | float | 只读 | local/敌机局部 | Angle of enemy's absolute movement. | 是 | 继承自 TH10 |
| -9970.0f | REL_ANGLE | float | 只读 | local/敌机局部 | Angle of enemy's relative movement. | 是 | 继承自 TH10 |
| -9969.0f | ABS_SPEED | float | 只读 | local/敌机局部 | Speed of enemy's absolute movement. | 是 | 继承自 TH10 |
| -9968.0f | REL_SPEED | float | 只读 | local/敌机局部 | Speed of enemy's relative movement. | 是 | 继承自 TH10 |
| -9967.0f | ABS_ORIGIN_DIST | float | 只读 | local/敌机局部 | Distance from the origin of enemy's absolute circular movement (radius of the circle). | 是 | 继承自 TH10 |
| -9966.0f | REL_ORIGIN_DIST | float | 只读 | local/敌机局部 | Distance from the origin of enemy's relative circular movement (radius of the circle). | 是 | 继承自 TH10 |
| -9965.0f | PLAYER_X2 | float | 只读 | global/全局 | Same as var_-9991. | 是 | 继承自 TH10 |
| -9964.0f | PLAYER_Y2 | float | 只读 | global/全局 | Same as var_-9990. | 是 | 继承自 TH10 |
| -9963.0f | BOSS_X | float | 只读 | global/全局 | Final X position of the boss. | 是 | 继承自 TH10 |
| -9962.0f | BOSS_Y | float | 只读 | global/全局 | Final Y position of the boss. | 是 | 继承自 TH10 |
| -9961 | UNKNOWN61 | int | 只读 | local/敌机局部 | Is the current script on anm slot 0 of the enemy. | 是 | 继承自 TH10 |
| -9960 | RANK | int | 只读 | global/全局 | Numeric value of rank, ranging from -1024 to 1024. Increases over time and decreases when player bombs/dies etc. | 是 | 继承自 TH10 |
| -9959 | DIFF | int | 只读 | global/全局 | Difficulty (E=0, N=1, H=2, L=3, EX=4) | 是 | 继承自 TH10 |
| -9958.0f | FINAL_ANGLE | float | 只读 | local/敌机局部 | Final angle of enemy's movement. | 是 | 继承自 TH10 |
| -9957 | TRUE | int | 只读 | global/全局 | Always returns 1. | 是 | 继承自 TH10 |
| -9956.0f | ABS_ANGLE_PLAYER | float | 只读 | local/敌机局部 | Angle to the player from enemy's absolute position. | 是 | 继承自 TH10 |
| -9955.0f | REL_ANGLE_PLAYER | float | 只读 | local/敌机局部 | Angle to the player from enemy's relative position. | 是 | 继承自 TH10 |
| -9954 | LIFE | int | 只读 | local/敌机局部 | Enemy's current HP. | 是 | 继承自 TH10 |
| -9953 | EASY | int | 只读 | global/全局 | Set to 1 if difficulty is easy, otherwise it's 0. | 是 | 继承自 TH10 |
| -9952 | NORMAL | int | 只读 | global/全局 | Set to 1 if difficulty is normal, otherwise it's 0. | 是 | 继承自 TH10 |
| -9951 | HARD | int | 只读 | global/全局 | Set to 1 if difficulty is hard, otherwise it's 0. | 是 | 继承自 TH10 |
| -9950 | LUNATIC | int | 只读 | global/全局 | Set to 1 if difficulty is lunatic, otherwise it's 0. | 是 | 继承自 TH10 |
| -9949 | MISS_COUNT | int | 读写 | global/全局 | Increased by 1 every time the player dies. | 是 | 本作 |
| -9948 | BOMB_COUNT | int | 读写 | global/全局 | Increased by 1 every time the player bombs. | 是 | 本作 |
| -9947 | CAPTURE | int | 读写 | global/全局 | Set to 0 when the player dies, bombs, or uses a game-specific mechanic that "fails" a spell. | 是 | 本作 |
| -9946 | ENM_CNT_REAL | int | 只读 | global/全局 | Amount of enemies alive (including main and MapleEnemy). | 是 | 本作 |
| -9945 | SHOTTYPE | int | 只读 | global/全局 | Numeric value that represents player's shottype, the first shottype is 0. | 是 | 本作 |
| -9944.0f | DIST_PLAYER | float | 只读 | local/敌机局部 | Distance from the enemy to the player. | 是 | 本作 |
| -9943 | BI0 | int | 读写 | local/敌机局部 | Is the same as the I0 variable of boss 0. | 是 | 本作 |
| -9942 | BI1 | int | 读写 | local/敌机局部 | Is the same as the I1 variable of boss 0. | 是 | 本作 |
| -9941 | BI2 | int | 读写 | local/敌机局部 | Is the same as the I2 variable of boss 0. | 是 | 本作 |
| -9940 | BI3 | int | 读写 | local/敌机局部 | Is the same as the I3 variable of boss 0. | 是 | 本作 |
| -9939.0f | BF0 | float | 读写 | local/敌机局部 | Is the same as the F0 variable of boss 0. | 是 | 本作 |
| -9938.0f | BF1 | float | 读写 | local/敌机局部 | Is the same as the F1 variable of boss 0. | 是 | 本作 |
| -9937.0f | BF2 | float | 读写 | local/敌机局部 | Is the same as the F2 variable of boss 0. | 是 | 本作 |
| -9936.0f | BF3 | float | 读写 | local/敌机局部 | Is the same as the F3 variable of boss 0. | 是 | 本作 |
| -9935.0f | F4 | float | 读写 | local/敌机局部 | Local float variable inherited by spawned enemies, just like F0-F3 and I0-I3. | 是 | 本作 |
| -9934.0f | F5 | float | 读写 | local/敌机局部 | Local float variable inherited by spawned enemies, just like F0-F3 and I0-I3. | 是 | 本作 |
| -9933.0f | F6 | float | 读写 | local/敌机局部 | Local float variable inherited by spawned enemies, just like F0-F3 and I0-I3. | 是 | 本作 |
| -9932.0f | F7 | float | 读写 | local/敌机局部 | Local float variable inherited by spawned enemies, just like F0-F3 and I0-I3. | 是 | 本作 |

## TH12 东方星莲船

- 体系：第三世代
- 指令：ecl-web.txt 未列出该作 Priw8 指令表；通常沿用相近世代/上一作格式，本文仅列变量。
- 变量：变量范围 -10000..-9930；本文列出有说明/命名记录的 71 条，未列空洞/未知项。

### TH12 变量

| ID | 名称 | 类型 | 访问 | 作用域 | 说明 | 文档化 | 来源 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| -10000 | RAND | int | 只读 | global/全局 | Random integer, very large range. | 是 | 继承自 TH10 |
| -9999.0f | RANDF | float | 只读 | global/全局 | Random float from 0.0f to 1.0f. | 是 | 继承自 TH10 |
| -9998.0f | RANDRAD | float | 只读 | global/全局 | Random float from -pi to pi. | 是 | 继承自 TH10 |
| -9997.0f | FINAL_X | float | 只读 | local/敌机局部 | Final X position of the enemy. | 是 | 继承自 TH10 |
| -9996.0f | FINAL_Y | float | 只读 | local/敌机局部 | Final Y position of the enemy. | 是 | 继承自 TH10 |
| -9995.0f | ABS_X | float | 只读 | local/敌机局部 | Absolute X position of the enemy. | 是 | 继承自 TH10 |
| -9994.0f | ABS_Y | float | 只读 | local/敌机局部 | Absolute Y position of the enemy. | 是 | 继承自 TH10 |
| -9993.0f | REL_X | float | 只读 | local/敌机局部 | Relative X position of the enemy. | 是 | 继承自 TH10 |
| -9992.0f | REL_Y | float | 只读 | local/敌机局部 | Relative Y position of the enemy. | 是 | 继承自 TH10 |
| -9991.0f | PLAYER_X | float | 只读 | global/全局 | Player's X position. | 是 | 继承自 TH10 |
| -9990.0f | PLAYER_Y | float | 只读 | global/全局 | Player's Y position. | 是 | 继承自 TH10 |
| -9989.0f | ANGLE_PLAYER | float | 只读 | local/敌机局部 | Angle from the enemy to the player. | 是 | 继承自 TH10 |
| -9988 | TIME | int | 只读 | local/敌机局部 | Time elapsed since the enemy spawned, in frames. | 是 | 继承自 TH10 |
| -9987.0f | RANDF2 | float | 只读 | global/全局 | Random float from -1.0f to 1.0f. | 是 | 继承自 TH10 |
| -9986 | TIMEOUT | int | 只读 | global/全局 | Set to 1 by the engine when a timeout occurs. | 是 | 继承自 TH10 |
| -9985 | I0 | int | 读写 | local/敌机局部 | Local integer variable, inherited by spawned enemies. | 是 | 继承自 TH10 |
| -9984 | I1 | int | 读写 | local/敌机局部 | Local integer variable, inherited by spawned enemies. | 是 | 继承自 TH10 |
| -9983 | I2 | int | 读写 | local/敌机局部 | Local integer variable, inherited by spawned enemies. | 是 | 继承自 TH10 |
| -9982 | I3 | int | 读写 | local/敌机局部 | Local integer variable, inherited by spawned enemies. | 是 | 继承自 TH10 |
| -9981.0f | F0 | float | 读写 | local/敌机局部 | Local float variable, inherited by spawned enemies. | 是 | 继承自 TH10 |
| -9980.0f | F1 | float | 读写 | local/敌机局部 | Local float variable, inherited by spawned enemies. | 是 | 继承自 TH10 |
| -9979.0f | F2 | float | 读写 | local/敌机局部 | Local float variable, inherited by spawned enemies. | 是 | 继承自 TH10 |
| -9978.0f | F3 | float | 读写 | local/敌机局部 | Local float variable, inherited by spawned enemies. | 是 | 继承自 TH10 |
| -9977.0f | FINAL_X2 | float | 只读 | local/敌机局部 | Same as var_-9997. | 是 | 继承自 TH10 |
| -9976.0f | FINAL_Y2 | float | 只读 | local/敌机局部 | Same as var_-9996. | 是 | 继承自 TH10 |
| -9975.0f | ABS_X2 | float | 只读 | local/敌机局部 | Same as var_-9995. | 是 | 继承自 TH10 |
| -9974.0f | ABS_Y2 | float | 只读 | local/敌机局部 | Same as var_-9994. | 是 | 继承自 TH10 |
| -9973.0f | REL_X2 | float | 只读 | local/敌机局部 | Same as var_-9993. | 是 | 继承自 TH10 |
| -9972.0f | REL_Y2 | float | 只读 | local/敌机局部 | Same as var_-9992. | 是 | 继承自 TH10 |
| -9971.0f | ABS_ANGLE | float | 只读 | local/敌机局部 | Angle of enemy's absolute movement. | 是 | 继承自 TH10 |
| -9970.0f | REL_ANGLE | float | 只读 | local/敌机局部 | Angle of enemy's relative movement. | 是 | 继承自 TH10 |
| -9969.0f | ABS_SPEED | float | 只读 | local/敌机局部 | Speed of enemy's absolute movement. | 是 | 继承自 TH10 |
| -9968.0f | REL_SPEED | float | 只读 | local/敌机局部 | Speed of enemy's relative movement. | 是 | 继承自 TH10 |
| -9967.0f | ABS_ORIGIN_DIST | float | 只读 | local/敌机局部 | Distance from the origin of enemy's absolute circular movement (radius of the circle). | 是 | 继承自 TH10 |
| -9966.0f | REL_ORIGIN_DIST | float | 只读 | local/敌机局部 | Distance from the origin of enemy's relative circular movement (radius of the circle). | 是 | 继承自 TH10 |
| -9965.0f | PLAYER_X2 | float | 只读 | global/全局 | Same as var_-9991. | 是 | 继承自 TH10 |
| -9964.0f | PLAYER_Y2 | float | 只读 | global/全局 | Same as var_-9990. | 是 | 继承自 TH10 |
| -9963.0f | BOSS_X | float | 只读 | global/全局 | Final X position of the boss. | 是 | 继承自 TH10 |
| -9962.0f | BOSS_Y | float | 只读 | global/全局 | Final Y position of the boss. | 是 | 继承自 TH10 |
| -9961 | UNKNOWN61 | int | 只读 | local/敌机局部 | Is the current script on anm slot 0 of the enemy. | 是 | 继承自 TH10 |
| -9960 | RANK | int | 只读 | global/全局 | Numeric value of rank, ranging from -1024 to 1024. Increases over time and decreases when player bombs/dies etc. | 是 | 继承自 TH10 |
| -9959 | DIFF | int | 只读 | global/全局 | Difficulty (E=0, N=1, H=2, L=3, EX=4) | 是 | 继承自 TH10 |
| -9958.0f | FINAL_ANGLE | float | 只读 | local/敌机局部 | Final angle of enemy's movement. | 是 | 继承自 TH10 |
| -9957 | TRUE | int | 只读 | global/全局 | Always returns 1. | 是 | 继承自 TH10 |
| -9956.0f | ABS_ANGLE_PLAYER | float | 只读 | local/敌机局部 | Angle to the player from enemy's absolute position. | 是 | 继承自 TH10 |
| -9955.0f | REL_ANGLE_PLAYER | float | 只读 | local/敌机局部 | Angle to the player from enemy's relative position. | 是 | 继承自 TH10 |
| -9954 | LIFE | int | 只读 | local/敌机局部 | Enemy's current HP. | 是 | 继承自 TH10 |
| -9953 | EASY | int | 只读 | global/全局 | Set to 1 if difficulty is easy, otherwise it's 0. | 是 | 继承自 TH10 |
| -9952 | NORMAL | int | 只读 | global/全局 | Set to 1 if difficulty is normal, otherwise it's 0. | 是 | 继承自 TH10 |
| -9951 | HARD | int | 只读 | global/全局 | Set to 1 if difficulty is hard, otherwise it's 0. | 是 | 继承自 TH10 |
| -9950 | LUNATIC | int | 只读 | global/全局 | Set to 1 if difficulty is lunatic, otherwise it's 0. | 是 | 继承自 TH10 |
| -9949 | MISS_COUNT | int | 读写 | global/全局 | Increased by 1 every time the player dies. | 是 | 继承自 TH11 |
| -9948 | BOMB_COUNT | int | 读写 | global/全局 | Increased by 1 every time the player bombs. | 是 | 继承自 TH11 |
| -9947 | CAPTURE | int | 读写 | global/全局 | Set to 0 when the player dies, bombs, or uses a game-specific mechanic that "fails" a spell. | 是 | 继承自 TH11 |
| -9946 | ENM_CNT_REAL | int | 只读 | global/全局 | Amount of enemies alive (including main and MapleEnemy). | 是 | 继承自 TH11 |
| -9945 | SHOTTYPE | int | 只读 | global/全局 | Numeric value that represents player's shottype, the first shottype is 0. | 是 | 继承自 TH11 |
| -9944.0f | DIST_PLAYER | float | 只读 | local/敌机局部 | Distance from the enemy to the player. | 是 | 继承自 TH11 |
| -9943 | BI0 | int | 读写 | local/敌机局部 | Is the same as the I0 variable of boss 0. | 是 | 继承自 TH11 |
| -9942 | BI1 | int | 读写 | local/敌机局部 | Is the same as the I1 variable of boss 0. | 是 | 继承自 TH11 |
| -9941 | BI2 | int | 读写 | local/敌机局部 | Is the same as the I2 variable of boss 0. | 是 | 继承自 TH11 |
| -9940 | BI3 | int | 读写 | local/敌机局部 | Is the same as the I3 variable of boss 0. | 是 | 继承自 TH11 |
| -9939.0f | BF0 | float | 读写 | local/敌机局部 | Is the same as the F0 variable of boss 0. | 是 | 继承自 TH11 |
| -9938.0f | BF1 | float | 读写 | local/敌机局部 | Is the same as the F1 variable of boss 0. | 是 | 继承自 TH11 |
| -9937.0f | BF2 | float | 读写 | local/敌机局部 | Is the same as the F2 variable of boss 0. | 是 | 继承自 TH11 |
| -9936.0f | BF3 | float | 读写 | local/敌机局部 | Is the same as the F3 variable of boss 0. | 是 | 继承自 TH11 |
| -9935.0f | F4 | float | 读写 | local/敌机局部 | Local float variable inherited by spawned enemies, just like F0-F3 and I0-I3. | 是 | 继承自 TH11 |
| -9934.0f | F5 | float | 读写 | local/敌机局部 | Local float variable inherited by spawned enemies, just like F0-F3 and I0-I3. | 是 | 继承自 TH11 |
| -9933.0f | F6 | float | 读写 | local/敌机局部 | Local float variable inherited by spawned enemies, just like F0-F3 and I0-I3. | 是 | 继承自 TH11 |
| -9932.0f | F7 | float | 读写 | local/敌机局部 | Local float variable inherited by spawned enemies, just like F0-F3 and I0-I3. | 是 | 继承自 TH11 |
| -9931 | LAST_ENM_ID | int | 只读 | global/全局 | ID of the last spawned enemy. | 是 | 本作 |
| -9930 | POWER | int | 只读 | global/全局 | Player's power (4.00 => 400) | 是 | 本作 |

## TH12.5 Double Spoiler

- 体系：第三世代
- 指令：ecl-web.txt 未列出该作 Priw8 指令表；通常沿用相近世代/上一作格式，本文仅列变量。
- 变量：变量范围 -10000..-9910；本文列出有说明/命名记录的 91 条，未列空洞/未知项。

### TH12.5 变量

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
| -9929 | [-9929] | int | 只读 | global/全局 | Used in Double Spoiler, unknown. | 否/待确认 | 本作 |
| -9928 | [-9928] | int | 只读 | global/全局 | Used in Double Spoiler, unknown. | 否/待确认 | 本作 |
| -9927 | [-9927] | int | 只读 | global/全局 | Used in Double Spoiler, unknown. | 否/待确认 | 本作 |
| -9926 | [-9926] | int | 读写 | global/全局 | Global integer variable. | 是 | 本作 |
| -9925 | [-9925] | int | 读写 | global/全局 | Global integer variable. | 是 | 本作 |
| -9924 | [-9924] | int | 读写 | global/全局 | Global integer variable. | 是 | 本作 |
| -9923 | [-9923] | int | 读写 | global/全局 | Global integer variable. | 是 | 本作 |
| -9922.0f | [-9922] | float | 读写 | global/全局 | Global float variable. | 是 | 本作 |
| -9921.0f | [-9921] | float | 读写 | global/全局 | Global float variable. | 是 | 本作 |
| -9920.0f | [-9920] | float | 读写 | global/全局 | Global float variable. | 是 | 本作 |
| -9919.0f | [-9919] | float | 读写 | global/全局 | Global float variable. | 是 | 本作 |
| -9918.0f | [-9918] | float | 读写 | global/全局 | Global float variable. | 是 | 本作 |
| -9917.0f | [-9917] | float | 读写 | global/全局 | Global float variable. | 是 | 本作 |
| -9916.0f | [-9916] | float | 读写 | global/全局 | Global float variable. | 是 | 本作 |
| -9915.0f | [-9915] | float | 读写 | global/全局 | Global float variable. | 是 | 本作 |
| -9914 | [-9914] | int | 只读 | local/敌机局部 | ID of the enemy. | 是 | 本作 |
| -9913 | [-9913] | int | 只读 | global/全局 | Used in Double Spoiler, amount of photos taken. | 是 | 本作 |
| -9912 | [-9912] | int | 只读 | global/全局 | Used in Double Spoiler, unknown. | 否/待确认 | 本作 |
| -9911.0f | [-9911] | float | 只读 | global/全局 | Angle at which the boss moves. | 是 | 本作 |
| -9910.0f | [-9910] | float | 只读 | global/全局 | Speed at which the boss moves. | 是 | 本作 |

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

## TH13 东方神灵庙

- 体系：第四世代
- 指令：普通指令 297 条；已说明 242/297。主要分组：系统/流程/栈/算术 / System；敌机创建与 ANM 管理 / Enemy creation and ANM script management；移动管理 / Movement management；敌机属性与杂项 / Enemy property management and other miscellaneous things；子弹创建与删除 / Bullet creation and deletion；激光创建 / Laser creation；敌机交互 / Enemy interaction；调试 / Debug；游戏特有 / Game specific。
- 变量：变量范围 -10000..-9907；本文列出有说明/命名记录的 94 条，未列空洞/未知项。

### TH13 指令：系统/流程/栈/算术 / System

| ID | 助记名 | 参数 | 说明 | 文档化 | 来源 |
| --- | --- | --- | --- | --- | --- |
| 0 | nop | — | Empty instruction, doesn't do anything. | 是 | 本作 |
| 1 | delete | — | Returns to the top of current call stack. | 是 | 本作 |
| 2 | ins_2 | — |  | 否/待确认 | 继承自 TH-1 |
| 3 | ins_3 | — |  | 否/待确认 | 继承自 TH-1 |
| 4 | ins_4 | — |  | 否/待确认 | 继承自 TH-1 |
| 5 | ins_5 | — |  | 否/待确认 | 继承自 TH-1 |
| 6 | ins_6 | — |  | 否/待确认 | 继承自 TH-1 |
| 7 | ins_7 | — |  | 否/待确认 | 继承自 TH-1 |
| 8 | ins_8 | — |  | 否/待确认 | 继承自 TH-1 |
| 9 | ins_9 | — |  | 否/待确认 | 继承自 TH-1 |
| 10 | ret | — | Returns from the current sub. | 是 | 本作 |
| 11 | call | m (sub) | Calls a given sub. Can take additional parameters to pass as arguments to the sub. [c=orange]Direct Usage obsolete. Use `@subName()` syntax instead. | 是 | 本作 |
| 12 | jmp | o (target) | Unconditionally jumps to the label %1. [c=orange]Direct usage obsolete. Use `goto label` syntax instead. | 是 | 本作 |
| 13 | jmpEq | o (target) | Pops a number from the stack and if it evaluates to false (in this context, 0), jumps to label %1. [c=orange]Direct usage obsolete. Use if/unless statement instead. | 是 | 本作 |
| 14 | jmpNeq | o (target) | Pops a number from the stack and if it evaluates to true (in this context, anything non-0), jumps to label %1. [c=orange]Direct usage obsolete. Use if/unless statement instead. | 是 | 本作 |
| 15 | callAsync | m (sub) | Asynchronously calls a given sub. Can take additional parameters to pass as arguments to the sub. [c=orange]Direct usage obsolete. Use `@subName() async` syntax instead. | 是 | 本作 |
| 16 | callAsyncId | mS (sub, id) | Asynchronously calls a given sub and assigns it ID %2. Can take additional parameters to pass as arguments to the sub. [c=orange]Direct usage obsolete, use, `@subName() async id` syntax instead. | 是 | 本作 |
| 17 | killAsync | S (id) | Ends most recently called sub that has ID %1 (same ID as in ins_16). If no sub with the given ID is found, nothing happens. Using ID -1 can lead to various unexpected results, ranging from deleting the enemy to freezing the game. | 是 | 本作 |
| 18 | ins_18 | S (id) | Let `vm` be the most recent async sub running with ID %1: this ins sets `vm[0x000011E4]` to 1. | 否/待确认 | 本作 |
| 19 | ins_19 | S (id) | Let `vm` be the most recent async sub running with ID %1: this ins sets `vm[0x000011E4]` to 0. | 否/待确认 | 本作 |
| 20 | ins_20 | SS (id, b) | Let `vm` be the most recent async sub running with ID %1: this ins sets `vm[0x0000101C]` to %2. | 否/待确认 | 本作 |
| 21 | killAllAsync | — | Ends all running async subs. Calling this in an async sub can lead to unexpected results, such as crashing the game. | 是 | 本作 |
| 22 | debug22 | Sm (a, b) | Debug instruction, code does not exist in the release builds of the game. Most likely used to call sub %2 if some variable set in a debug menu is equal to %1. | 是 | 本作 |
| 23 | wait | S (time) | Stops sub execution for %1 frames. | 是 | 本作 |
| 24 | waitf | f (time) | ins_23, but time is given as a float instead of an int. Subframes do actually exist and affect ins_547. | 是 | 本作 |
| 25 | ins_25 | — |  | 否/待确认 | 继承自 TH-1 |
| 26 | ins_26 | — |  | 否/待确认 | 继承自 TH-1 |
| 27 | unknown27 | — |  | 否/待确认 | 继承自 TH-1 |
| 28 | ins_28 | — |  | 否/待确认 | 继承自 TH-1 |
| 29 | ins_29 | — |  | 否/待确认 | 继承自 TH-1 |
| 30 | unknown30 | m (formatString) | Some sort of `printf` debug instruction, which can take additional float/int arguments after %1. Its code does not exist in the release builds. | 是 | 本作 |
| 31 | unknown31 | — |  | 否/待确认 | 继承自 TH-1 |
| 32 | ins_32 | — |  | 否/待确认 | 继承自 TH-1 |
| 33 | ins_33 | — |  | 否/待确认 | 继承自 TH-1 |
| 34 | ins_34 | — |  | 否/待确认 | 继承自 TH-1 |
| 35 | ins_35 | — |  | 否/待确认 | 继承自 TH-1 |
| 36 | ins_36 | — |  | 否/待确认 | 继承自 TH-1 |
| 37 | ins_37 | — |  | 否/待确认 | 继承自 TH-1 |
| 38 | ins_38 | — |  | 否/待确认 | 继承自 TH-1 |
| 39 | ins_39 | — |  | 否/待确认 | 继承自 TH-1 |
| 40 | stackAlloc | S (size) | Increases the ECL stack pointer by %1 bytes (probably), to make space for sub variables. [c=orange]Obsolete, thecl generates this instruction automatically. | 是 | 本作 |
| 41 | ins_41 | — |  | 否/待确认 | 继承自 TH-1 |
| 42 | pushi | S (num) | Pushes an integer to the ECL stack. [c=orange]Obsolete, push values to stack by writing unassigned expressions instead. | 是 | 本作 |
| 43 | seti | S (var) | Pops an integer from the stack into variable %1. [c=orange]Obsolete, use assignment syntax instead. | 是 | 本作 |
| 44 | pushf | f (num) | Pushes a float to the ECL stack. [c=orange]Obsolete, push values to stack by writing unassigned expressions instead. | 是 | 本作 |
| 45 | setf | f (var) | Pops a float from the stack into variable %1. [c=orange]Obsolete, use assignment syntax instead. | 是 | 本作 |
| 46 | ins_46 | — |  | 否/待确认 | 继承自 TH-1 |
| 47 | ins_47 | — |  | 否/待确认 | 继承自 TH-1 |
| 48 | ins_48 | — |  | 否/待确认 | 继承自 TH-1 |
| 49 | ins_49 | — |  | 否/待确认 | 继承自 TH-1 |
| 50 | addi | — | Sums integers on the stack. [c=orange]Obsolete, use expressions instead. | 是 | 本作 |
| 51 | addf | — | Sums floats on the stack. [c=orange]Obsolete, use expressions instead. | 是 | 本作 |
| 52 | subi | — | Subtracts integers on the stack. [c=orange]Obsolete, use expressions instead. | 是 | 本作 |
| 53 | subf | — | Subtracts floats on the stack. [c=orange]Obsolete, use expressions instead. | 是 | 本作 |
| 54 | muli | — | Multiplies integers on the stack. [c=orange]Obsolete, use expressions instead. | 是 | 本作 |
| 55 | mulf | — | Multiplies floats on the stack. [c=orange]Obsolete, use expressions instead. | 是 | 本作 |
| 56 | divi | — | Divides integers on the stack. [c=orange]Obsolete, use expressions instead. | 是 | 本作 |
| 57 | divf | — | Divides floats on the stack. [c=orange]Obsolete, use expressions instead. | 是 | 本作 |
| 58 | modi | — | Modulo operation on integers on the stack. [c=orange]Obsolete, use expressions instead. | 是 | 本作 |
| 59 | eqi | — | Stack integer `==` comparison. [c=orange]Obsolete, use expressions instead. | 是 | 本作 |
| 60 | eqf | — | Stack float `==` comparison. [c=orange]Obsolete, use expressions instead. | 是 | 本作 |
| 61 | neqi | — | Stack integer `!=` comparison. [c=orange]Obsolete, use expressions instead. | 是 | 本作 |
| 62 | neqf | — | Stack float `!=` comparison. [c=orange]Obsolete, use expressions instead. | 是 | 本作 |
| 63 | lessi | — | Stack integer `<` comparison. [c=orange]Obsolete, use expressions instead. | 是 | 本作 |
| 64 | lessf | — | Stack float `<` comparison. [c=orange]Obsolete, use expressions instead. | 是 | 本作 |
| 65 | leqi | — | Stack integer `<=` comparison. [c=orange]Obsolete, use expressions instead. | 是 | 本作 |
| 66 | leqf | — | Stack float `<=` comparison. [c=orange]Obsolete, use expressions instead. | 是 | 本作 |
| 67 | greateri | — | Stack integer `>` comparison. [c=orange]Obsolete, use expressions instead. | 是 | 本作 |
| 68 | greaterf | — | Stack float `>` comparison. [c=orange]Obsolete, use expressions instead. | 是 | 本作 |
| 69 | geqi | — | Stack integer `>=` comparison. [c=orange]Obsolete, use expressions instead. | 是 | 本作 |
| 70 | geqf | — | Stack float `>=` comparison. [c=orange]Obsolete, use expressions instead. | 是 | 本作 |
| 71 | noti | — | Stack integer NOT operation (e.g. !1). [c=orange]Obsolete, use expressions instead. | 是 | 本作 |
| 72 | notf | — | Stack float NOT operation (e.g. !1.0f). [c=orange]Obsolete, use expressions instead. | 是 | 本作 |
| 73 | or | — | Logical OR operation on the stack. [c=orange]Obsolete, use expressions instead. | 是 | 本作 |
| 74 | and | — | Logical AND operation on the stack. [c=orange]Obsolete, use expressions instead. | 是 | 本作 |
| 75 | xor | — | Bitwise XOR operation on integers on the stack. [c=orange]Obsolete, use expressions instead. | 是 | 本作 |
| 76 | bit_or | — | Bitwise OR operation on integers on the stack. [c=orange]Obsolete, use expressions instead. | 是 | 本作 |
| 77 | bit_and | — | Bitwise AND operation on integers on the stack. [c=orange]Obsolete, use expressions instead. | 是 | 本作 |
| 78 | deci | S (var) | Pushes variable %1 to the stack and then decrements it. [c=orange]Obsolete, use expressions instead. | 是 | 本作 |
| 79 | stackSin | — | sin operation on a float on the stack. [c=orange]Obsolete, use `sin(floatVal)` instead. | 是 | 本作 |
| 80 | stackCos | — | cos operation on a float on the stack. [c=orange]Obsolete, use `cos(floatVal)` instead. | 是 | 本作 |
| 81 | circlePos | ffff (varX, varY, ang, radius) | Performs following operation: [code]%1 = cos(%3)*%4;<br>%2 = sin(%3)*%4;[/code] | 是 | 本作 |
| 82 | validRad | f (var) | Normalizes angle in %1. | 是 | 本作 |
| 83 | negi | — | Negates an integer on the stack. [c=orange]Obsolete, use expressions instead. | 是 | 本作 |
| 84 | negf | — | Negates a float on the stack. [c=orange]Obsolete, use expressions instead. | 是 | 本作 |
| 85 | squareSum | fff (var, x, y) | Performs following operation: [code]%1 = %2*%2 + %3*%3;[/code] | 是 | 本作 |
| 86 | squareSumRoot | fff (var, x, y) | Performs following operation: [code]%1 = sqrt(%2*%2 + %3*%3);[/code] | 是 | 本作 |
| 87 | getAngle | fffff (var, x1, y1, x2, y2) | Calculates angle from (%2,%3) to (%4,%5) and stores it in %1. | 是 | 本作 |
| 88 | stackSqrt | — | square root operation on a float on the stack. [c=orange]Obsolete, use `sqrt(floatVal)` instead. | 是 | 本作 |
| 89 | linearFunc | fff (var, a, x) | Performs following operation: [code]%1 = %2*%3;[/code]<br>(what's the point of making this an instruction, ZUN?) | 是 | 本作 |
| 90 | pointRotate | fffff (varX, varY, x, y, rad) | Rotates point (%3,%4) by angle %5 and stores the resulting coordinates in %1 and %2. | 是 | 本作 |
| 91 | floatTime | SfSSff (slot, var, time, mode, init, final) | In %3 frames using mode %4, variable %2 changes from %5 to %6. %1 is used to set the slot to be used by this ins, every enemy has 8 slots (0 to 7). | 是 | 本作 |
| 92 | math92 | SfSSffff (slot, var, time, mode, init, final, m, n) | Same as ins_91, but takes 2 extra arguments of unknown meaning. Needs investigation. | 否/待确认 | 本作 |
| 93 | math93 | ffff (varX, varY, r1, r2) | Gets a random point based on %3 and %4 and stores it on (%1,%2). Needs investigation. | 否/待确认 | 本作 |

### TH13 指令：敌机创建与 ANM 管理 / Enemy creation and ANM script management

| ID | 助记名 | 参数 | 说明 | 文档化 | 来源 |
| --- | --- | --- | --- | --- | --- |
| 300 | enmCreate | mffSSS (sub, x, y, hp, score, item) | Creates an enemy using subroutine %1 at coordinates %2, %3 (relative to position of enemy that called it), health of created enemy is %4, score bonus is %5 and item drop is %6. | 是 | 本作 |
| 301 | enmCreateA | mffSSS (sub, x, y, hp, score, item) | Creates an enemy using subroutine %1 at coordinates %2, %3 (absolute position), health of created enemy is %4, score bonus is %5 and item drop is %6. | 是 | 本作 |
| 302 | anmSelect | S (anmIndex) | Selects ANM file to be used by other instructions based on %1. | 是 | 本作 |
| 303 | anmSetSprite | SS (slot, script) | Loads script %2 from ANM selected with ins_302 on slot %1. | 是 | 本作 |
| 304 | enmCreateM | mffSSS (sub, x, y, hp, score, item) | Creates a mirrored enemy using subroutine %1 at coordinates %2, %3 (relative to caller's position), health of created enemy is %4, score bonus is %5 and item drop is %6. | 是 | 本作 |
| 305 | enmCreateAM | mffSSS (sub, x, y, hp, score, item) | Creates an mirrored enemy using subroutine %1 at coordinates %2, %3 (absolute position), health of created enemy is %4, score bonus is %5 and item drop is %6. | 是 | 本作 |
| 306 | anmSetMain | SS (slot, script) | Loads script %2 from ANM selected with ins_302 on slot %1. However, the script number provided will only be used when the enemy is not moving. When moving left %2+1 will be used, right %2+2, diagonal left %2+3, diagonal right %2+4. Might not work properly if %1 is not 0 according to THBWiki. | 是 | 本作 |
| 307 | anmPlay | SS (anmIndex, script) | From ANM file selected based on %1, play script %2 at caller's current coordinates. The spawned script is completely independent, and will continue existing even if caller is deleted. | 是 | 本作 |
| 308 | anmPlayAbs | SS (anmIndex, script) | From ANM file selected based on %1, play script %2 at coordinates (0, 0). The spawned script is completely independent, and will continue existing even if caller is deleted. | 是 | 本作 |
| 309 | enmCreateF | mffSSS (sub, x, y, hp, score, item) | Creates a filler enemy using subroutine %1 at coordinates %2, %3 (relative to caller's position), health of created enemy is %4, score bonus is %5 and item drop is %6. | 是 | 本作 |
| 310 | enmCreateAF | mffSSS (sub, x, y, hp, score, item) | Creates a filler enemy using subroutine %1 at coordinates %2, %3 (absolute position), health of created enemy is %4, score bonus is %5 and item drop is %6. | 是 | 本作 |
| 311 | enmCreateMF | mffSSS (sub, x, y, hp, score, item) | Creates a mirrored filler enemy using subroutine %1 at coordinates %2, %3 (relative to caller's position), health of created enemy is %4, score bonus is %5 and item drop is %6. | 是 | 本作 |
| 312 | enmCreateAMF | mffSSS (sub, x, y, hp, score, item) | Creates a mirrored filler enemy using subroutine %1 at coordinates %2, %3 (absolute position), health of created enemy is %4, score bonus is %5 and item drop is %6. | 是 | 本作 |
| 313 | anmSelectedPlay | S (script) | Same as ins_307, except it uses the ANM file selected by ins_302. | 是 | 本作 |
| 314 | anmPlayHigh | SS (anmIndex, script) | Same as ins_307, except it spawns the ANM with a higher layer? Needs further investigation. | 否/待确认 | 本作 |
| 315 | anmPlayRotate | SSf (anmIndex, script, angle) | Same as ins_307, except it sets rotation of spawned ANM to %3. | 是 | 本作 |
| 316 | anm316 | SS (a, b) | Unknown. | 否/待确认 | 本作 |
| 317 | anmSwitch | SS (slot, switch) | Sets the execution pointer of ANM script on slot %1 to where ANM `ins_5(a)` with `a` == `switch` is (the time is also changed to match time of `ins_5`). Doesn't work if the value is 0 apparently? | 是 | 本作 |
| 318 | anmReset | — | Resets some ANM-related parameters of the caller (TODO: what exactly?) | 是 | 本作 |
| 319 | anmRotate | Sf (slot, r) | Set rotation of an ANM script on slot %1 to %2. | 是 | 本作 |
| 320 | anmMove | Sff (slot, x, y) | Set position of an ANM script on slot %1 to (%2,%3). This does not detach the script from the caller, so the actual position of the script will be position of the caller + position set here. | 是 | 本作 |
| 321 | enmMapleEnemy | mffSSS (sub, x, y, hp, score, item) | ins_300, but used by 'MapleEnemy' (TODO: what's the difference from ins_300?) | 是 | 本作 |
| 322 | enm322 | SS (a, b) | Unknown. | 否/待确认 | 本作 |
| 323 | deathAnm | SS (anmIndex, script) | Set the animation that will play when the enemy dies to script %2 from ANM file specified by %1. | 是 | 本作 |
| 324 | enm324 | — | Unknown. | 否/待确认 | 本作 |
| 325 | anmColor | SSSS (slot, R, G, B) | Modify color of ANM script on slot %1, %2, %3, [c=lightblue]%4 correspond to individual colors and have to be from 0 to 255. | 是 | 本作 |
| 326 | anmColorTime | SSSSSS (slot, time, mode, R, G, B) | Same as ins_325, but the change is applied in %2 frames using mode %3. | 是 | 本作 |
| 327 | anmAlpha | SS (slot, alpha) | Sets alpha of ANM script on slot %1 to %2 (must be a value between 0-255) | 是 | 本作 |
| 328 | anmAlphaTime | SSSS (slot, time, mode, alpha) | Same as ins_327, but the change is applied in %2 frames using mode %3. | 是 | 本作 |
| 329 | anmScale | Sff (slot, w, h) | Sets horizontal and vertical scaling of ANM script on slot %1 to %2 and %3 respectively. Overwrites scaling properties set by the ANM script. | 是 | 本作 |
| 330 | anmScaleTime | SSSff (slot, time, mode, w, h) | Same as ins_329, but the change is applied in %2 frames using mode %3. | 是 | 本作 |
| 331 | anmAlpha2 | SS (slot, alpha) | Sets alpha2 (opacity of the gradient) of ANM script on slot %1 to %2. | 是 | 本作 |
| 332 | anmAlpha2Time | SSSS (slot, time, mode, alpha) | Same as ins_331, but the change is applied in %2 frames using mode %3. | 是 | 本作 |
| 333 | anm333 | SSSff (a, b, c, r, s) | Unknown. Might be doing something to ANM script on slot %1. | 否/待确认 | 本作 |
| 334 | anm334 | S (a) | Hard to tell? THBWiki Google translate gives this: 'The animation effect of the playing unit (enemy), the lightning effect near the evil spirit ball of the god temple', which might be referring to lightning around Nue in TD extra stage. | 否/待确认 | 本作 |
| 335 | anmScale2 | Sff (slot, w, h) | Same as ins_329, except it doesn't overwrite the scaling set by the ANM script - instead, it multiplies it. | 是 | 本作 |

### TH13 指令：移动管理 / Movement management

| ID | 助记名 | 参数 | 说明 | 文档化 | 来源 |
| --- | --- | --- | --- | --- | --- |
| 400 | movePos | ff (x, y) | Sets caller's absolute position to %1, %2. | 是 | 本作 |
| 401 | movePosTime | SSff (time, mode, x, y) | Same as ins_400, but the change is applied in %1 frames using mode %2. | 是 | 本作 |
| 402 | movePosRel | ff (x, y) | Sets caller's relative position to %1, %2. | 是 | 本作 |
| 403 | movePosRelTime | SSff (time, mode, x, y) | Same as ins_402, but the change is applied in %1 frames using mode %2. | 是 | 本作 |
| 404 | moveVel | ff (r, spd) | Sets caller's absolute movement angle to %1 and speed to %2. | 是 | 本作 |
| 405 | moveVelTime | SSff (time, mode, r, spd) | Same as ins_404, but the change is applied in %1 frames using mode %2. | 是 | 本作 |
| 406 | moveVelRel | ff (r, spd) | Sets caller's relative movement angle to %1 and speed to %2. | 是 | 本作 |
| 407 | moveVelRelTime | SSff (time, mode, r, spd) | Same as ins_406, but the change is applied in %1 frames using mode %2. | 是 | 本作 |
| 408 | moveCircle | ffff (θ, spd, rad, radInc) | Sets caller's absolute circle movement: %1 is the angle indicating initial position on the circle, %2 is the angular velocity, %3 is circle radius and %4 is by how much the radius increases each frame. | 是 | 本作 |
| 409 | moveCircleTime | SSfff (time, mode, spd, rad, radInc) | Same as ins_408, but the change is applied in %1 frames using mode %2. There is also no initial angle parameter here for obvious reason. | 是 | 本作 |
| 410 | moveCircleRel | ffff (θ, spd, rad, radInc) | Sets caller's relative circle movement: %1 is the angle indicating initial position on the circle, %2 is the angular velocity, %3 is circle radius and %4 is by how much the radius increases each frame. | 是 | 本作 |
| 411 | moveCircleRelTime | SSfff (time, mode, spd, rad, radInc) | Same as ins_410, but the change is applied in %1 frames using mode %2. There is also no initial angle parameter here for obvious reason. | 是 | 本作 |
| 412 | moveRand | SSf (time, mode, spd) | Randomizes caller's absolute angle and sets absolute speed to %3. The speed changes back to 0 in %1 frames using mode %2. | 是 | 本作 |
| 413 | moveRandRel | SSf (time, mode, spd) | Randomizes caller's relative angle and sets relative speed to %3. The speed changes back to 0 in %1 frames using mode %2. | 是 | 本作 |
| 414 | moveBoss | — | Sets caller's absolute position to the absolute position of the boss. If called without a boss, [tip=Google translated from THBWiki, I find this sentence funny]it will cause serious mis-access and explode[/tip]. | 是 | 本作 |
| 415 | moveBossRel | — | Sets caller's relative position to the relative position of the boss. If called without a boss, [tip=Google translated from THBWiki, I find this sentence funny]it will cause serious mis-access and explode[/tip]. | 是 | 本作 |
| 416 | movePos3d | fff (x, y, z) | Same as ins_400, but takes a %3 parameter for the third dimension, which probably affects 3D ANM scripts used by the caller, or something. | 是 | 本作 |
| 417 | movePos3dRel | fff (x, y, z) | Same as ins_402, but takes a %3 parameter for the third dimension, which probably affects 3D ANM scripts used by the caller, or something. | 是 | 本作 |
| 418 | moveAdd | ff (x, y) | Increases caller's absolute position by %1 and %2. | 是 | 本作 |
| 419 | move419 | ff (x, y) | While the code of this ins looks like it's supposed to be a relative version of ins_418, it doesn't seem to behave like that... | 否/待确认 | 本作 |
| 420 | moveEllipse | ffffff (θ, spd, rad, radInc, ellDir, ellRatio) | Sets caller's absolute ellipse movement: %1 is the angle indicating initial position on the ellipse, %2 is the angular velocity, %3 is the base circle radius and %4 is by how much the radius increases each frame. %6 is how much the base circle should be 'squished' to make it an ellipse, and %5 is the squishing angle (I don't know math terms in English, sorry) | 是 | 本作 |
| 421 | moveEllipseTime | SSfffff (time, mode, spd, rad, radInc, ellDir, ellRatio) | Same as ins_420, but the change is applied in %1 frames using mode %2. There is also no initial angle parameter here for obvious reason | 是 | 本作 |
| 422 | moveEllipseRel | ffffff (θ, spd, rad, radInc, ellDir, ellRatio) | Sets caller's relative ellipse movement: %1 is the angle indicating initial position on the ellipse, %2 is the angular velocity, %3 is the base circle radius and %4 is by how much the radius increases each frame. %6 is how much the base circle should be 'squished' to make it an ellipse, and %5 is the squishing angle (I don't know math terms in English, sorry) | 是 | 本作 |
| 423 | moveEllipseRelTime | SSfffff (time, mode, spd, rad, radInc, ellDir, ellRatio) | Same as ins_422, but the change is applied in %1 frames using mode %2. There is also no initial angle parameter here for obvious reason | 是 | 本作 |
| 424 | moveSetMirror | S (state) | Sets caller's mirror flag to %1. | 是 | 本作 |
| 425 | moveBezier | Sffffff (time, x1, y1, x2, y2, x3, y3) | In %1 frames, the enemy moves towards (%2,%3), then moves towards (%6,%7) for a while and finally moves to (%4,%5). Uses absolute position.<br>From THBWiki: <br>(assuming the current coordinates are (x0, y0)) the motion trajectory is actually a Bezier curve from (x0, y0) to (x2, y2);<br>The P1 coordinate of the curve is `((x1-x0)*1/3, (y1-y0)*1/3)`;<br>The P2 coordinate of the curve is `(-(x3-x2)*1/3+x2,-(y3-y2) *1/3+x2)` | 是 | 本作 |
| 426 | moveBezierRel | Sffffff (time, x1, y1, x2, y2, x3, y3) | Same as ins_425, but uses relative position. | 是 | 本作 |
| 427 | moveReset | — | Resets some movement-related parameters (TODO: what exactly?) | 否/待确认 | 本作 |
| 428 | moveVelNM | ff (r, spd) | Same as ins_404, but ignores the mirror flag. | 是 | 本作 |
| 429 | moveVelNMTime | SSff (time, mode, r, spd) | Same as ins_405, but ignores the mirror flag. | 是 | 本作 |
| 430 | moveVelNMRel | ff (r, spd) | Same as ins_406, but ignores the mirror flag. | 是 | 本作 |
| 431 | moveVelNMRelTime | SSff (time, mode, r, spd) | Same as ins_407, but ignores the mirror flag. | 是 | 本作 |
| 432 | moveEnm | S (id) | Sets caller's absolute position to absolute position of enemy with var_-9914 == %1. | 是 | 本作 |
| 433 | moveEnmRel | S (id) | Sets caller's relative position to relative position of enemy with var_-9914 == %1. | 是 | 本作 |
| 434 | moveCurve | SSSff (time, mode, c, x, y) | In %1 frames using mode %2, caller's absolute position is changed to (%4,%5). The movement trajectory is a curve based on %3, it is unknown how it works exactly. | 否/待确认 | 本作 |
| 435 | moveCurveRel | SSSff (time, mode, c, x, y) | In %1 frames using mode %2, caller's relative position is changed to (%4,%5). The movement trajectory is a curve based on %3, it is unknown how it works exactly. | 否/待确认 | 本作 |
| 436 | moveAddTime | SSff (time, mode, x, y) | Same as ins_418, but the change is applied in %1 frames using mode %2. | 是 | 本作 |
| 437 | moveAddRelTime | SSff (time, mode, x, y) | Same as ins_419, but the change is applied in %1 frames using mode %2 (it also behaves as expected, unlike ins_419). | 是 | 本作 |
| 438 | moveCurveAdd | SSSff (time, mode, c, x, y) | Same as ins_434, but instead caller's current absolute coordinates are added to %4 and %5. | 是 | 本作 |
| 439 | moveCurveAddRel | SSSff (time, mode, c, x, y) | Same as ins_435, but instead caller's current relative coordinates are added to %4 and %5. | 是 | 本作 |

### TH13 指令：敌机属性与杂项 / Enemy property management and other miscellaneous things

| ID | 助记名 | 参数 | 说明 | 文档化 | 来源 |
| --- | --- | --- | --- | --- | --- |
| 500 | setHurtbox | ff (w, h) | Sets caller's hurtbox width to %1 and height to %2. | 是 | 本作 |
| 501 | setHitbox | ff (w, h) | Sets caller's hitbox width to %1 and height to %2. | 是 | 本作 |
| 502 | flagSet | S (n) | Sets flag(s) according to %1. Refer to the [flag table](#s=modding/flags) for exact values. | 是 | 本作 |
| 503 | flagClear | S (n) | Clears flag(s) according to %1. Refer to the [flag table](#s=modding/flags) for exact values. | 是 | 本作 |
| 504 | moveLimit | ffff (x, y, w, h) | Sets caller's movement limit rectangle: (%1,%2) are the coordinates of the center of the rect, while %3, %4 are width and height of it. | 是 | 本作 |
| 505 | moveLimitReset | — | Removes caller's movement limit. | 是 | 本作 |
| 506 | dropClear | — | Clears caller's extra item drop. | 是 | 本作 |
| 507 | dropExtra | SS (type, amount) | Adds %2 items of type %1 to caller's extra drop. Item type table will be made in the future. | 是 | 本作 |
| 508 | dropArea | ff (w, h) | Sets caller's item drop area width to %1 and height to %2. | 是 | 本作 |
| 509 | dropItems | — | Drops all items the caller has. Has no effect in spell practice. | 是 | 本作 |
| 510 | dropMain | S (type) | Sets caller's main drop to %1. | 是 | 本作 |
| 511 | lifeSet | S (hp) | Sets caller's current HP and max HP to %1. | 是 | 本作 |
| 512 | setBoss | S (a) | If %1 is 0, activates boss mode and makes the caller the main boss. If %1 > 0, it makes the caller the secondary boss. If %1 is -1, ends boss mode. | 是 | 本作 |
| 513 | timerReset | — | Resets boss timer. | 是 | 本作 |
| 514 | setInterrupt | SSSm (slot, hp, time, sub) | Sets an interrupt on slot %1 (not sure how many slots there are) - once caller's hp reaches %2 or %3 frames have passed since this was called, caller will terminate all subs it's currently running and execute sub %4. | 是 | 本作 |
| 515 | setInvuln | S (time) | Makes the caller completely invulnerable for %1 frames. | 是 | 本作 |
| 516 | playSound | S (id) | Plays sound %1. Sound id table will be added in the future. | 是 | 本作 |
| 517 | setScreenShake | SSS (time, startIntensity, endIntensity) | Activates screen shake for %1 frames. %2 is the starting intensity and %3 is the ending intensity. The larger the intensity, the more the screen shakes. | 是 | 本作 |
| 518 | dialogRead | S (dialogueId) | Starts a dialogue, %1 is the ID of an entry in the .msg file. Apart from that, has the effect ins_525. | 是 | 本作 |
| 519 | dialogWait | — | Waits until there are no dialogues active, or the running .msg script calls a certain instruction (which one?) | 否/待确认 | 本作 |
| 520 | bossWait | — | Waits until there are no boss enemies. | 是 | 本作 |
| 521 | setTimeout | Sm (slot, sub) | Sets a timeout interrupt on slot %1 - when the timer reaches 0, caller will terminate all subs it's currently running and execute sub %2. | 是 | 本作 |
| 522 | spellEx | SSSm (id, time, unused, name) | Same as ins_537, but the difficulty number is NOT added to the id. | 是 | 本作 |
| 523 | spellEnd | — | Ends currently active spellcard. | 是 | 本作 |
| 524 | setChapter | S (a) | Some jank that's responsible for showing boss name and possibly other things. In LoLK, it also ends the current chapter and begins a new one. | 否/待确认 | 本作 |
| 525 | enmKillAll | — | Kills all other enemies (unless they have a flag that prevents that set). | 是 | 本作 |
| 526 | etProtectRange | f (r) | Makes bullets generated by the caller not spawn if they are in radius %1 around the player. | 是 | 本作 |
| 527 | lifeMarker | SfS (slot, hp, c) | Sets a new life marker on slot %1, %2 determines where the marker will appear on the health bar (if %2=1000.0f and the enemy has 2000 hp, the marker will split the hp bar in half). %3 is an RGB value of unknown use (possibly leftover from earlier ECL versions) | 是 | 本作 |
| 528 | spellUnused | SSSm (id, time, unused, name) | No difference from ins_522, unused. | 是 | 本作 |
| 529 | rankF3 | ffff (var, a, b, c) | Sets %1 to %2 if rank is low, %3 if rank is average or %4 if rank is high. | 是 | 本作 |
| 530 | rankF5 | ffffff (var, a, b, c, d, e) | Sets %1 to %2 if rank is very low, %3 if rank is low, %4 if rank is average, %5 if rank is high or %6 if rank is very high. | 是 | 本作 |
| 531 | rankF2 | fff (var, a, b) | Sets %1 to %2 if rank is low or %3 if rank is high. | 是 | 本作 |
| 532 | rankI3 | SSSS (var, a, b, c) | Sets %1 to %2 if rank is low, %3 if rank is average or %4 if rank is high. | 是 | 本作 |
| 533 | rankI5 | SSSSSS (var, a, b, c, d, e) | Sets %1 to %2 if rank is very low, %3 if rank is low, %4 if rank is average, %5 if rank is high or %6 if rank is very high. | 是 | 本作 |
| 534 | rankI2 | SSS (var, a, b) | Sets %1 to %2 if rank is low or %3 if rank is high. | 是 | 本作 |
| 535 | diffI | SSSSS (var, E, N, H, L) | Sets %1 to one of values provided based on difficulty. | 是 | 本作 |
| 536 | diffF | fffff (var, E, N, H, L) | Sets %1 to one of values provided based on difficulty. | 是 | 本作 |
| 537 | spell | SSSm (id, time, unused, name) | Declares a spellcard with id %1 and name %4. The actual ID passed to the spell-creating function is `id + difficulty`, with easy=0, normal=1, hard=2, lunatic=3, ex=4, overdrive=5. <br>%2 determines how much time the spell circle takes to shrink (in frames), as well as how fast the spell bonus decreases. The exact formula is as follows: <br>[code] int factor = maxSCB >> 2; // maxSCB is hardcoded<br> currSCB -= (maxSCB - factor) / (%2 - 300);<br> currSCB -= currSCB % 10; [/code] <br>As you can guess, setting %2 to 300 causes a division by 0 error and crashes the game, while setting it to a value smaller than 300 causes the SCB to increase over time, instead of decreasing. %3 is unused. | 是 | 本作 |
| 538 | spell2 | SSSm (id, time, unused, name) | Same as ins_537, except the ID used is `id - 1 + difficulty`. | 是 | 本作 |
| 539 | spell3 | SSSm (id, time, unused, name) | Same as ins_537, except the ID used is `id - 2 + difficulty`. | 是 | 本作 |
| 540 | stars | S (cnt) | Sets the amount of stars displayed in the top left corner. Stars might not appear at all if there is no boss active. | 是 | 本作 |
| 541 | noHitboxDur | S (time) | Disables the hitbox (but not the hurtbox) for the given amount of frames. | 是 | 本作 |
| 542 | spellTimeout | — | Makes the current spell a timeout spell (prevent spell bonus from decreasing, give capture bonus if timed out). | 是 | 本作 |
| 543 | unknown543 | — | Unknown. | 否/待确认 | 本作 |
| 544 | unknown544 | S (a) | Unknown, sets or clears some flag? | 否/待确认 | 本作 |
| 545 | laserCancel | — | Cancels all lasers. | 是 | 本作 |
| 546 | bombShield | SS (a, script) | Sets the bomb invulnerability flag (%1=1 set, %1=0 not set), the caller's ANM script will change to %2 when a bomb is active (how does it work with ANM slots exactly?) | 是 | 本作 |
| 547 | gameSpeed | f (s) | Sets game speed to %1 of the normal speed. In ISC, enemies with flag 13 (dec=8192) set will ignore effects of this opcode. | 是 | 本作 |
| 548 | diffWait | SSSS (e, n, h, l) | Same as ins_23, but the wait time is chosen from the given 4 based on the difficulty. | 是 | 本作 |
| 549 | unknown549 | S (a) | Unknown. | 否/待确认 | 本作 |
| 550 | unknown550 | S (a) | Unknown. | 否/待确认 | 本作 |
| 551 | unknown551 | S (a) | Unknown. | 否/待确认 | 本作 |
| 552 | zIndex | S (layers) | Increases layer of all ANM scripts used by the caller by %1. | 是 | 本作 |
| 553 | hitSound | S (id) | Makes the caller play sound %1 when hit. Sound id table will be added in the future. | 是 | 本作 |
| 554 | stageLogo | — | Shows the stage logo from an ANM of a hardcoded name. | 是 | 本作 |
| 555 | enmAlive | SS (var, id) | Checks if enemy of var_-9914 == %2 is still alive, and sets %1 to 1 if it is or 0 if it isn't. | 是 | 本作 |
| 556 | setDeath | m (sub) | Makes the caller execute sub %1 when the HP reaches 0. Keep in mind that the caller is already marked for deletion at the point when the sub actually executes, so if you put waiting there the sub will not execute fully (because the caller will be deleted) | 是 | 本作 |
| 557 | fogTime | SSSff (time, mode, color, start, end) | Same as STD ins_9, that is, fogTime. Refer to [the STD instruction table](#s=modding/std-ins) for details. | 是 | 本作 |
| 558 | flagMirror | S (state) | Literally the exact same instruction as ins_424. | 是 | 本作 |
| 559 | enmLimit | S (limit) | Set the maximum number of enemies that can be present. New enemies will fail to spawn if the cap is reached. Default is 99999. | 是 | 本作 |
| 560 | unknown560 | ff (r, s) | Unknown. | 否/待确认 | 本作 |
| 561 | die | — | Makes the caller execute the sub set with ins_556. If there is no such sub set, the caller dies instead (exactly the same as if the player shot down the caller, that is, items are dropped, death sound plays etc) | 是 | 本作 |
| 562 | dropItemsSp | — | Same as ins_509, but item spawning will not be blocked in spell practice. | 是 | 本作 |

### TH13 指令：子弹创建与删除 / Bullet creation and deletion

| ID | 助记名 | 参数 | 说明 | 文档化 | 来源 |
| --- | --- | --- | --- | --- | --- |
| 600 | etNew | S (etId) | Resets bullet manager %1 to default properties. | 是 | 本作 |
| 601 | etOn | S (etId) | Shoots bullet(s) using properties from bullet manager %1. | 是 | 本作 |
| 602 | etSprite | SSS (etId, type, color) | Sets bullet type and color of bullet manager %1. Pre-th15 bullet types are yet to be documented. | 是 | 本作 |
| 603 | etOffset | Sff (etId, x, y) | Sets the relative offset of bullets spawned by bullet manager %1 to (%2,%3). | 是 | 本作 |
| 604 | etAngle | Sff (etId, angle1, angle2) | Sets angle1 and angle2 of bullet manager %1. | 是 | 本作 |
| 605 | etSpeed | Sff (etId, speed1, speed2) | Sets speed1 and speed2 of bullet manager %1. | 是 | 本作 |
| 606 | etCount | SSS (etId, count1, count2) | Sets count1 and count2 of bullet manager %1. | 是 | 本作 |
| 607 | etAim | SS (etId, aim) | Sets aim mode of bullet manager %1. | 是 | 本作 |
| 608 | etSound | SSS (etId, sound1, sound2) | Sets sound1 and sound2 of bullet manager %1 (sound effect table is TODO). sound1 plays when the bullet manager fires a bullet, while sound2 plays when a bullet fired by the bullet manager does certain transformations. Set to -1 for no sound. | 是 | 本作 |
| 609 | etExSet | SSSSSSff (etId, index, async, type, a, b, r, s) | Sets bullet transformation of bullet manager %1, transformation explanation will be added in the future. | 是 | 本作 |
| 610 | etExSet2 | SSSSSSSSffff (etId, index, async, type, a, b, c, d, r, s, m, n) | Same as ins_609, but takes more arguments for certain transformation types. | 是 | 本作 |
| 611 | etEx | SSSSSff (etId, async, type, a, b, r, s) | Adds bullet transformation to bullet manager %1, transformation explanation will be added in the future. | 是 | 本作 |
| 612 | etEx2 | SSSSSSSffff (etId, async, type, a, b, c, d, r, s, m, n) | Same as ins_611, but takes more arguments for certain transformation types. | 是 | 本作 |
| 613 | etClearAll | — | Clears all bullets. | 是 | 本作 |
| 614 | etCopy | SS (etIdDest, etIdSrc) | Copies everything from bullet manager %2 into bullet manager %1. Warning: this instruction is partially broken and does NOT copy the index next ins_611/ins_612 transformations will be added at. | 是 | 本作 |
| 615 | etCancel | f (r) | Clears all bullets in a circle of radius %1 around the caller, and turns them into cancel items. | 是 | 本作 |
| 616 | etClear | f (r) | Clears all bullets in a circle of radius %1 around the caller without turning them into cancel items. | 是 | 本作 |
| 617 | etSpeedR3 | Sffffff (etId, spd1l, spd1m, spd1h, spd2l, spd2m, spd2h) | Sets speed1 and speed2 of bullet manager %1 to two of the values provided, based on ingame rank (l=low, m=medium, h=high) | 是 | 本作 |
| 618 | etSpeedR5 | Sffffffffff (etId, spd1l, spd1ml, spd1m, spd1mh, spd1h, spd2l, spd2ml, spd2m, spd2mh, spd2h) | Sets speed1 and speed2 of bullet manager %1 to two of the values provided, based on ingame rank (l=low, ml=medium-low, m=medium, mh=medium-high, h=high) | 是 | 本作 |
| 619 | etSpeedR2 | Sffff (etId, spd1l, spd1h, spd2l, spd2h) | Sets speed1 and speed2 of bullet manager %1 to two of the values provided, based on ingame rank (l=low, h=high) | 是 | 本作 |
| 620 | etCountR3 | SSSSSSS (etId, cnt1l, cnt1m, cnt1h, cnt2l, cnt2m, cnt2h) | Sets count1 and count2 of bullet manager %1 to two of the values provided, based on ingame rank (l=low, m=medium, h=high) | 是 | 本作 |
| 621 | etCountR5 | SSSSSSSSSSS (etId, cnt1l, cnt1ml, cnt1m, cnt1mh, cnt1h, cnt2l, cnt2ml, cnt2m, cnt2mh, cnt2h) | Sets count1 and count2 of bullet manager %1 to two of the values provided, based on ingame rank (l=low, ml=medium-low, m=medium, mh=medium-high, h=high) | 是 | 本作 |
| 622 | etCountR2 | SSSSS (etId, cnt1l, cnt1h, cnt2l, cnt2h) | Sets count1 and count2 of bullet manager %1 to two of the values provided, based on ingame rank (l=low, h=high) | 是 | 本作 |
| 623 | angleToPlayer | fff (var, x, y) | Gets angle to the player from coordinates (%2,%3) and stores it in %1. | 是 | 本作 |
| 624 | etSpeedD | Sffffffff (etId, spd1e, spd1n, spd1h, spd1l, spd2e, spd2n, spd2h, spd2l) | Sets speed1 and speed2 of bullet manager %1 to 2 of the values provided, based on the difficulty (e=easy, n=normal, h=hard, l=lunatic) | 是 | 本作 |
| 625 | etCountD | SSSSSSSSS (etId, cnt1e, cnt1n, cnt1h, cnt1l, cnt2e, cnt2n, cnt2h, cnt2l) | Sets count1 and count2 of bullet manager %1 to 2 of the values provided, based on the difficulty (e=easy, n=normal, h=hard, l=lunatic) | 是 | 本作 |
| 626 | etOffsetRad | Sff (etId, angle, radius) | Sets the relative offset of bullets spawned by bullet manager %1 to (cos(%2)\*%3,sin(%2)\*%3). Stacks with ins_603. | 是 | 本作 |
| 627 | etDist | Sf (etId, dist) | Sets distance of bullets spawned by bullet manager %1 to %2 (that is, when a bullet is spawned it moves by %2 using its current angle). | 是 | 本作 |
| 628 | etOffsetAbs | Sff (etId, x, y) | Sets the absolute offset of bullets spawned by bullet manager %1 to (%2,%3). | 是 | 本作 |
| 629 | fog | fS (r, color) | Sets caller's fog's radius to %1 and color to %2 (RGB value in reverse order). This resets the fog completely, that is, every time it's called the fog spawn animation plays. | 是 | 本作 |
| 630 | callSTD | S (switch) | Sets execution pointer of the STD script to where STD ins_16(%1) is (%1 must be the same), basically same concept as ins_317. | 是 | 本作 |
| 631 | lifeHide | S (time) | Hides boss lifebar for %1 frames. | 是 | 本作 |
| 632 | funcSet | S (id) | Sets a function that the game will execute every frame from a set of hardcoded functions that differs between games. | 是 | 本作 |
| 633 | flagExtDmg | S (state) | Sets the external damage flag to %1. Caller probably needs to be the main boss for this to work - with this flag set, the caller gets damaged by the value stored in var_-9940 every frame, and then resets the value. This allows other enemies to damage the boss by incrementing the aforementioned variable, used in LoLK by Sagume (and also happens to be the main cause of the Sagume skip glitch) | 是 | 本作 |
| 634 | setHitboxFunc | S (id) | Make the caller use a special function for determining collision with the player. TODO: create a list of functions and their IDs | 是 | 本作 |
| 635 | etCancel2 | f (r) | Same as ins_615, but doesn't clear bullets with bomb invulnerability. | 是 | 本作 |
| 636 | etClear2 | f (r) | Same as ins_616, but doesn't clear bullets with bomb invulnerability. | 是 | 本作 |
| 637 | funcCall | S (id) | Same as ins_632, except the function is called just once instead of every frame. | 是 | 本作 |
| 638 | scoreAdd | S (n) | Adds %1 to score (or subtracts if %1 is negative). There is no lower boundary check, so if this causes score to go below 0, an underflow happens. | 是 | 本作 |
| 639 | funcSet2 | S (id) | Same as ins_632, except it sets an unknown flag to 1 (ins_632 sets it to 0) | 是 | 本作 |
| 640 | etExSub | SSm (etId, index, s) | Sets the string parameter of transform on index %2 in bullet manager %1 to %3, transformations will be explained separately later. | 是 | 本作 |

### TH13 指令：激光创建 / Laser creation

| ID | 助记名 | 参数 | 说明 | 文档化 | 来源 |
| --- | --- | --- | --- | --- | --- |
| 700 | laserNew | Sffff (etId, init_length, final_length, unknown_arg_3, width) | Sets basic parameters of the laser. %4 has something to do with the length of straight line lasers (investigation needed), but doesn't do anything for other laser types. For curvy lasers, the only used argument is %5, and length is specified with ins_701 instead. | 是 | 本作 |
| 701 | laserTiming | SSSSSS (edId, startup_time, expand_time, duration, shrink_time, init_flags) | Sets timing for infinite lasers. %6 sets the initial flags for a laser, but these flags are unknown at the moment. For curvy lasers, the %2 argument instead specifies the length of the laser. | 是 | 本作 |
| 702 | laserOn | S (edId) | Shoots a straight line laser. | 是 | 本作 |
| 703 | laserStOn | SS (etId, laser_id) | Shoots an infinite laser. %2 is a number that's used to identify this particular laser instance, so that it can be referred to in other instructions. | 是 | 本作 |
| 704 | laserOffset | Sff (laser_id, x, y) | Sets the position of the infinite laser pointed to by %1. | 是 | 本作 |
| 705 | laserTrajectory | Sff (laser_id, x_speed, y_speed) | Sets the offset velocity of the infinite laser pointed to by %1. The laser's position will change by %2 and %3 every frame. | 是 | 本作 |
| 706 | laserStLength | Sf (laser_id, speed) | Sets the speed of the infinite laser pointed to by %1. | 是 | 本作 |
| 707 | laserStWidth | Sf (laser_id, width) | Sets the width of the infinite laser pointed to by %1. | 是 | 本作 |
| 708 | laserStAngle | Sf (laser_id, angle) | Sets the angle of the infinite laser pointed to by %1. | 是 | 本作 |
| 709 | laserStRotation | Sf (laser_id, angular_vel) | Sets the angular velocity of the infinite laser pointed to by %1. The laser's angle will change by %2 every frame. | 是 | 本作 |
| 710 | laserStEnd | S (laser_id) | Clears the laser pointed to by %1. | 是 | 本作 |
| 711 | laserCuOn | S (etId) | Shoots a curvy laser. | 是 | 本作 |
| 712 | etCancelRect | ff (w, h) | Cancels all bullets in rectangle of width %1 and height %2. | 是 | 本作 |
| 713 | unknown713 | SS (etId, laser_id) | Shoots a laser 'beam', a laser type used by marisa in GFW. Broken since this laser type does not exist outside of GFW. | 是 | 本作 |
| 714 | unknown714 | SS (laser_id, unknown) | Does something with a laser beam pointed to by %1. Broken since this laser type does not exist outside of GFW. | 是 | 本作 |

### TH13 指令：敌机交互 / Enemy interaction

| ID | 助记名 | 参数 | 说明 | 文档化 | 来源 |
| --- | --- | --- | --- | --- | --- |
| 800 | enmCall | Sm (id, sub) | Makes enemy with var_-9914 == %1 stop all subs it's running and execute sub %2 (works like an interrupt). This will NOT make the enemy execute the sub right as this instruction is called, the new sub will be executed when the game handles the given enemy, which might be later on the same frame or on the next frame. Using this to make the caller interrupt itself can make the game explode. | 是 | 本作 |
| 801 | enmPos | ffS (varX, varY, id) | Stores coordinates of enemy with var_-9914 == %3 in (%1,%2). | 是 | 本作 |
| 802 | broadcastInterrupt | S (slot) | For all existing bosses, trigger the interrupt set by ins_514 on slot %1. Does not change the HP to the one set in ins_514. | 是 | 本作 |

### TH13 指令：调试 / Debug

| ID | 助记名 | 参数 | 说明 | 文档化 | 来源 |
| --- | --- | --- | --- | --- | --- |
| 900 | debug900 | — | 未在 Priw8 表中记录/待确认 | 否/待确认 | — |

### TH13 指令：游戏特有 / Game specific

| ID | 助记名 | 参数 | 说明 | 文档化 | 来源 |
| --- | --- | --- | --- | --- | --- |
| 1000 | spec0 | — | 未在 Priw8 表中记录/待确认 | 否/待确认 | — |
| 1001 | spec1 | — | 未在 Priw8 表中记录/待确认 | 否/待确认 | — |
| 1002 | spec2 | — | 未在 Priw8 表中记录/待确认 | 否/待确认 | — |
| 1003 | spec3 | — | 未在 Priw8 表中记录/待确认 | 否/待确认 | — |

### TH13 变量

| ID | 名称 | 类型 | 访问 | 作用域 | 说明 | 文档化 | 来源 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| -10000 | RAND | int | 只读 | global/全局 | Random integer, very large range. | 是 | 继承自 TH10 |
| -9999.0f | RANDF | float | 只读 | global/全局 | Random float from 0.0f to 1.0f. | 是 | 继承自 TH10 |
| -9998.0f | RANDRAD | float | 只读 | global/全局 | Random float from -pi to pi. | 是 | 继承自 TH10 |
| -9997.0f | FINAL_X | float | 只读 | local/敌机局部 | Final X position of the enemy. | 是 | 继承自 TH10 |
| -9996.0f | FINAL_Y | float | 只读 | local/敌机局部 | Final Y position of the enemy. | 是 | 继承自 TH10 |
| -9995.0f | ABS_X | float | 只读 | local/敌机局部 | Absolute X position of the enemy. | 是 | 继承自 TH10 |
| -9994.0f | ABS_Y | float | 只读 | local/敌机局部 | Absolute Y position of the enemy. | 是 | 继承自 TH10 |
| -9993.0f | REL_X | float | 只读 | local/敌机局部 | Relative X position of the enemy. | 是 | 继承自 TH10 |
| -9992.0f | REL_Y | float | 只读 | local/敌机局部 | Relative Y position of the enemy. | 是 | 继承自 TH10 |
| -9991.0f | PLAYER_X | float | 只读 | global/全局 | Player's X position. | 是 | 继承自 TH10 |
| -9990.0f | PLAYER_Y | float | 只读 | global/全局 | Player's Y position. | 是 | 继承自 TH10 |
| -9989.0f | ANGLE_PLAYER | float | 只读 | local/敌机局部 | Angle from the enemy to the player. | 是 | 继承自 TH10 |
| -9988 | TIME | int | 只读 | local/敌机局部 | Time elapsed since the enemy spawned, in frames. | 是 | 继承自 TH10 |
| -9987.0f | RANDF2 | float | 只读 | global/全局 | Random float from -1.0f to 1.0f. | 是 | 继承自 TH10 |
| -9986 | TIMEOUT | int | 只读 | global/全局 | Set to 1 by the engine when a timeout occurs. | 是 | 继承自 TH10 |
| -9985 | I0 | int | 读写 | local/敌机局部 | Local integer variable, inherited by spawned enemies. | 是 | 继承自 TH10 |
| -9984 | I1 | int | 读写 | local/敌机局部 | Local integer variable, inherited by spawned enemies. | 是 | 继承自 TH10 |
| -9983 | I2 | int | 读写 | local/敌机局部 | Local integer variable, inherited by spawned enemies. | 是 | 继承自 TH10 |
| -9982 | I3 | int | 读写 | local/敌机局部 | Local integer variable, inherited by spawned enemies. | 是 | 继承自 TH10 |
| -9981.0f | F0 | float | 读写 | local/敌机局部 | Local float variable, inherited by spawned enemies. | 是 | 继承自 TH10 |
| -9980.0f | F1 | float | 读写 | local/敌机局部 | Local float variable, inherited by spawned enemies. | 是 | 继承自 TH10 |
| -9979.0f | F2 | float | 读写 | local/敌机局部 | Local float variable, inherited by spawned enemies. | 是 | 继承自 TH10 |
| -9978.0f | F3 | float | 读写 | local/敌机局部 | Local float variable, inherited by spawned enemies. | 是 | 继承自 TH10 |
| -9977.0f | FINAL_X2 | float | 只读 | local/敌机局部 | Same as var_-9997. | 是 | 继承自 TH10 |
| -9976.0f | FINAL_Y2 | float | 只读 | local/敌机局部 | Same as var_-9996. | 是 | 继承自 TH10 |
| -9975.0f | ABS_X2 | float | 只读 | local/敌机局部 | Same as var_-9995. | 是 | 继承自 TH10 |
| -9974.0f | ABS_Y2 | float | 只读 | local/敌机局部 | Same as var_-9994. | 是 | 继承自 TH10 |
| -9973.0f | REL_X2 | float | 只读 | local/敌机局部 | Same as var_-9993. | 是 | 继承自 TH10 |
| -9972.0f | REL_Y2 | float | 只读 | local/敌机局部 | Same as var_-9992. | 是 | 继承自 TH10 |
| -9971.0f | ABS_ANGLE | float | 只读 | local/敌机局部 | Angle of enemy's absolute movement. | 是 | 继承自 TH10 |
| -9970.0f | REL_ANGLE | float | 只读 | local/敌机局部 | Angle of enemy's relative movement. | 是 | 继承自 TH10 |
| -9969.0f | ABS_SPEED | float | 只读 | local/敌机局部 | Speed of enemy's absolute movement. | 是 | 继承自 TH10 |
| -9968.0f | REL_SPEED | float | 只读 | local/敌机局部 | Speed of enemy's relative movement. | 是 | 继承自 TH10 |
| -9967.0f | ABS_ORIGIN_DIST | float | 只读 | local/敌机局部 | Distance from the origin of enemy's absolute circular movement (radius of the circle). | 是 | 继承自 TH10 |
| -9966.0f | REL_ORIGIN_DIST | float | 只读 | local/敌机局部 | Distance from the origin of enemy's relative circular movement (radius of the circle). | 是 | 继承自 TH10 |
| -9965.0f | PLAYER_X2 | float | 只读 | global/全局 | Same as var_-9991. | 是 | 继承自 TH10 |
| -9964.0f | PLAYER_Y2 | float | 只读 | global/全局 | Same as var_-9990. | 是 | 继承自 TH10 |
| -9963.0f | BOSS_X | float | 只读 | global/全局 | Final X position of the boss. | 是 | 继承自 TH10 |
| -9962.0f | BOSS_Y | float | 只读 | global/全局 | Final Y position of the boss. | 是 | 继承自 TH10 |
| -9961 | ANM_ID | int | 只读 | local/敌机局部 | Is the current script on anm slot 0 of the enemy. | 是 | 继承自 TH10 |
| -9960 | RANK | int | 只读 | global/全局 | Numeric value of rank, ranging from -1024 to 1024. Increases over time and decreases when player bombs/dies etc. | 是 | 继承自 TH10 |
| -9959 | DIFF | int | 只读 | global/全局 | Difficulty (E=0, N=1, H=2, L=3, EX=4, O=5) | 是 | 继承自 TH10 |
| -9958.0f | FINAL_ANGLE | float | 只读 | local/敌机局部 | Final angle of enemy's movement. | 是 | 继承自 TH10 |
| -9957 | TRUE | int | 只读 | global/全局 | Always returns 1. | 是 | 继承自 TH10 |
| -9956.0f | ABS_ANGLE_PLAYER | float | 只读 | local/敌机局部 | Angle to the player from enemy's absolute position. | 是 | 继承自 TH10 |
| -9955.0f | REL_ANGLE_PLAYER | float | 只读 | local/敌机局部 | Angle to the player from enemy's relative position. | 是 | 继承自 TH10 |
| -9954 | LIFE | int | 只读 | local/敌机局部 | Enemy's current HP. | 是 | 继承自 TH10 |
| -9953 | EASY | int | 只读 | global/全局 | Set to 1 if difficulty is easy, otherwise it's 0. | 是 | 继承自 TH10 |
| -9952 | NORMAL | int | 只读 | global/全局 | Set to 1 if difficulty is normal, otherwise it's 0. | 是 | 继承自 TH10 |
| -9951 | HARD | int | 只读 | global/全局 | Set to 1 if difficulty is hard, otherwise it's 0. | 是 | 继承自 TH10 |
| -9950 | LUNATIC | int | 只读 | global/全局 | Set to 1 if difficulty is lunatic, otherwise it's 0. | 是 | 继承自 TH10 |
| -9949 | MISS_COUNT | int | 读写 | global/全局 | Increased by 1 every time the player dies. | 是 | 继承自 TH11 |
| -9948 | BOMB_COUNT | int | 读写 | global/全局 | Increased by 1 every time the player bombs. | 是 | 继承自 TH11 |
| -9947 | CAPTURE | int | 读写 | global/全局 | Set to 0 when the player dies, bombs, or uses a game-specific mechanic that "fails" a spell. | 是 | 继承自 TH11 |
| -9946 | ENM_CNT_REAL | int | 只读 | global/全局 | Amount of enemies alive (including main and MapleEnemy). | 是 | 继承自 TH11 |
| -9945 | SHOTTYPE | int | 只读 | global/全局 | Numeric value that represents player's shottype, the first shottype is 0. | 是 | 继承自 TH11 |
| -9944.0f | DIST_PLAYER | float | 只读 | local/敌机局部 | Distance from the enemy to the player. | 是 | 继承自 TH11 |
| -9943 | BI0 | int | 读写 | local/敌机局部 | Is the same as the I0 variable of boss 0. | 是 | 继承自 TH11 |
| -9942 | BI1 | int | 读写 | local/敌机局部 | Is the same as the I1 variable of boss 0. | 是 | 继承自 TH11 |
| -9941 | BI2 | int | 读写 | local/敌机局部 | Is the same as the I2 variable of boss 0. | 是 | 继承自 TH11 |
| -9940 | BI3 | int | 读写 | local/敌机局部 | Is the same as the I3 variable of boss 0. | 是 | 继承自 TH11 |
| -9939.0f | BF0 | float | 读写 | local/敌机局部 | Is the same as the F0 variable of boss 0. | 是 | 继承自 TH11 |
| -9938.0f | BF1 | float | 读写 | local/敌机局部 | Is the same as the F1 variable of boss 0. | 是 | 继承自 TH11 |
| -9937.0f | BF2 | float | 读写 | local/敌机局部 | Is the same as the F2 variable of boss 0. | 是 | 继承自 TH11 |
| -9936.0f | BF3 | float | 读写 | local/敌机局部 | Is the same as the F3 variable of boss 0. | 是 | 继承自 TH11 |
| -9935.0f | F4 | float | 读写 | local/敌机局部 | Local float variable inherited by spawned enemies, just like F0-F3 and I0-I3. | 是 | 继承自 TH11 |
| -9934.0f | F5 | float | 读写 | local/敌机局部 | Local float variable inherited by spawned enemies, just like F0-F3 and I0-I3. | 是 | 继承自 TH11 |
| -9933.0f | F6 | float | 读写 | local/敌机局部 | Local float variable inherited by spawned enemies, just like F0-F3 and I0-I3. | 是 | 继承自 TH11 |
| -9932.0f | F7 | float | 读写 | local/敌机局部 | Local float variable inherited by spawned enemies, just like F0-F3 and I0-I3. | 是 | 继承自 TH11 |
| -9931 | LAST_ENM_ID | int | 只读 | global/全局 | ID of the last spawned enemy. | 是 | 继承自 TH12 |
| -9930 | POWER | int | 只读 | global/全局 | Player's power (4.00 => 400) | 是 | 继承自 TH12 |
| -9929 | DS1 | int | 只读 | global/全局 | Used in Double Spoiler, unknown. | 否/待确认 | 继承自 TH12.5 |
| -9928 | DS2 | int | 只读 | global/全局 | Used in Double Spoiler, unknown. | 否/待确认 | 继承自 TH12.5 |
| -9927 | DS3 | int | 只读 | global/全局 | Used in Double Spoiler, unknown. | 否/待确认 | 继承自 TH12.5 |
| -9926 | GI0 | int | 读写 | global/全局 | Global integer variable. | 是 | 继承自 TH12.5 |
| -9925 | GI1 | int | 读写 | global/全局 | Global integer variable. | 是 | 继承自 TH12.5 |
| -9924 | GI2 | int | 读写 | global/全局 | Global integer variable. | 是 | 继承自 TH12.5 |
| -9923 | GI3 | int | 读写 | global/全局 | Global integer variable. | 是 | 继承自 TH12.5 |
| -9922.0f | GF0 | float | 读写 | global/全局 | Global float variable. | 是 | 继承自 TH12.5 |
| -9921.0f | GF1 | float | 读写 | global/全局 | Global float variable. | 是 | 继承自 TH12.5 |
| -9920.0f | GF2 | float | 读写 | global/全局 | Global float variable. | 是 | 继承自 TH12.5 |
| -9919.0f | GF3 | float | 读写 | global/全局 | Global float variable. | 是 | 继承自 TH12.5 |
| -9918.0f | GF4 | float | 读写 | global/全局 | Global float variable. | 是 | 继承自 TH12.5 |
| -9917.0f | GF5 | float | 读写 | global/全局 | Global float variable. | 是 | 继承自 TH12.5 |
| -9916.0f | GF6 | float | 读写 | global/全局 | Global float variable. | 是 | 继承自 TH12.5 |
| -9915.0f | GF7 | float | 读写 | global/全局 | Global float variable. | 是 | 继承自 TH12.5 |
| -9914 | ID | int | 只读 | local/敌机局部 | ID of the enemy. | 是 | 继承自 TH12.5 |
| -9913 | DS_PHOTOCOUNT | int | 只读 | global/全局 | Used in Double Spoiler, amount of photos taken. | 是 | 继承自 TH12.5 |
| -9912 | DS4 | int | 只读 | global/全局 | Used in Double Spoiler, unknown. | 否/待确认 | 继承自 TH12.5 |
| -9911.0f | ANGLE_BOSS | float | 只读 | global/全局 | Angle at which the boss moves. | 是 | 继承自 TH12.5 |
| -9910.0f | SPEED_BOSS | float | 只读 | global/全局 | Speed at which the boss moves. | 是 | 继承自 TH12.5 |
| -9909 | UNKNOWN9 | int | 只读 | local/敌机局部 | Enemy ID of the parent enemy. | 是 | 继承自 TH12.8 |
| -9908 | ENM_CNT | int | 只读 | global/全局 | Amount of killable enemies alive (that is, doesn't include hitboxless/intangible enemies etc). | 是 | 本作 |
| -9907 | SPELL_ID | int | 只读 | global/全局 | Spellcard ID, used by spell practice. Unknown meaning in LoLK. | 是 | 本作 |

## TH14 东方辉针城

- 体系：第四世代
- 指令：普通指令 316 条；已说明 257/316。主要分组：系统/流程/栈/算术 / System；敌机创建与 ANM 管理 / Enemy creation and ANM script management；移动管理 / Movement management；敌机属性与杂项 / Enemy property management and other miscellaneous things；子弹创建与删除 / Bullet creation and deletion；激光创建 / Laser creation；敌机交互 / Enemy interaction；调试 / Debug；游戏特有 / Game specific。
- 变量：变量范围 -10000..-9907；本文列出有说明/命名记录的 94 条，未列空洞/未知项。

### TH14 指令：系统/流程/栈/算术 / System

| ID | 助记名 | 参数 | 说明 | 文档化 | 来源 |
| --- | --- | --- | --- | --- | --- |
| 0 | nop | — | Empty instruction, doesn't do anything. | 是 | 继承自 TH13 |
| 1 | delete | — | Returns to the top of current call stack. | 是 | 继承自 TH13 |
| 2 | ins_2 | — |  | 否/待确认 | 继承自 TH-1 |
| 3 | ins_3 | — |  | 否/待确认 | 继承自 TH-1 |
| 4 | ins_4 | — |  | 否/待确认 | 继承自 TH-1 |
| 5 | ins_5 | — |  | 否/待确认 | 继承自 TH-1 |
| 6 | ins_6 | — |  | 否/待确认 | 继承自 TH-1 |
| 7 | ins_7 | — |  | 否/待确认 | 继承自 TH-1 |
| 8 | ins_8 | — |  | 否/待确认 | 继承自 TH-1 |
| 9 | ins_9 | — |  | 否/待确认 | 继承自 TH-1 |
| 10 | ret | — | Returns from the current sub. | 是 | 继承自 TH13 |
| 11 | call | m (sub) | Calls a given sub. Can take additional parameters to pass as arguments to the sub. [c=orange]Direct Usage obsolete. Use `@subName()` syntax instead. | 是 | 继承自 TH13 |
| 12 | jmp | o (target) | Unconditionally jumps to the label %1. [c=orange]Direct usage obsolete. Use `goto label` syntax instead. | 是 | 继承自 TH13 |
| 13 | jmpEq | o (target) | Pops a number from the stack and if it evaluates to false (in this context, 0), jumps to label %1. [c=orange]Direct usage obsolete. Use if/unless statement instead. | 是 | 继承自 TH13 |
| 14 | jmpNeq | o (target) | Pops a number from the stack and if it evaluates to true (in this context, anything non-0), jumps to label %1. [c=orange]Direct usage obsolete. Use if/unless statement instead. | 是 | 继承自 TH13 |
| 15 | callAsync | m (sub) | Asynchronously calls a given sub. Can take additional parameters to pass as arguments to the sub. [c=orange]Direct usage obsolete. Use `@subName() async` syntax instead. | 是 | 继承自 TH13 |
| 16 | callAsyncId | mS (sub, id) | Asynchronously calls a given sub and assigns it ID %2. Can take additional parameters to pass as arguments to the sub. [c=orange]Direct usage obsolete, use, `@subName() async id` syntax instead. | 是 | 继承自 TH13 |
| 17 | killAsync | S (id) | Ends most recently called sub that has ID %1 (same ID as in ins_16). If no sub with the given ID is found, nothing happens. Using ID -1 can lead to various unexpected results, ranging from deleting the enemy to freezing the game. | 是 | 继承自 TH13 |
| 18 | ins_18 | S (id) | Let `vm` be the most recent async sub running with ID %1: this ins sets `vm[0x000011E4]` to 1. | 否/待确认 | 继承自 TH13 |
| 19 | ins_19 | S (id) | Let `vm` be the most recent async sub running with ID %1: this ins sets `vm[0x000011E4]` to 0. | 否/待确认 | 继承自 TH13 |
| 20 | ins_20 | SS (id, b) | Let `vm` be the most recent async sub running with ID %1: this ins sets `vm[0x0000101C]` to %2. | 否/待确认 | 继承自 TH13 |
| 21 | killAllAsync | — | Ends all running async subs. Calling this in an async sub can lead to unexpected results, such as crashing the game. | 是 | 继承自 TH13 |
| 22 | debug22 | Sm (a, b) | Debug instruction, code does not exist in the release builds of the game. Most likely used to call sub %2 if some variable set in a debug menu is equal to %1. | 是 | 继承自 TH13 |
| 23 | wait | S (time) | Stops sub execution for %1 frames. | 是 | 继承自 TH13 |
| 24 | waitf | f (time) | ins_23, but time is given as a float instead of an int. Subframes do actually exist and affect ins_547. | 是 | 继承自 TH13 |
| 25 | ins_25 | — |  | 否/待确认 | 继承自 TH-1 |
| 26 | ins_26 | — |  | 否/待确认 | 继承自 TH-1 |
| 27 | unknown27 | — |  | 否/待确认 | 继承自 TH-1 |
| 28 | ins_28 | — |  | 否/待确认 | 继承自 TH-1 |
| 29 | ins_29 | — |  | 否/待确认 | 继承自 TH-1 |
| 30 | unknown30 | m (formatString) | Some sort of `printf` debug instruction, which can take additional float/int arguments after %1. Its code does not exist in the release builds. | 是 | 继承自 TH13 |
| 31 | unknown31 | — |  | 否/待确认 | 继承自 TH-1 |
| 32 | ins_32 | — |  | 否/待确认 | 继承自 TH-1 |
| 33 | ins_33 | — |  | 否/待确认 | 继承自 TH-1 |
| 34 | ins_34 | — |  | 否/待确认 | 继承自 TH-1 |
| 35 | ins_35 | — |  | 否/待确认 | 继承自 TH-1 |
| 36 | ins_36 | — |  | 否/待确认 | 继承自 TH-1 |
| 37 | ins_37 | — |  | 否/待确认 | 继承自 TH-1 |
| 38 | ins_38 | — |  | 否/待确认 | 继承自 TH-1 |
| 39 | ins_39 | — |  | 否/待确认 | 继承自 TH-1 |
| 40 | stackAlloc | S (size) | Increases the ECL stack pointer by %1 bytes (probably), to make space for sub variables. [c=orange]Obsolete, thecl generates this instruction automatically. | 是 | 继承自 TH13 |
| 41 | ins_41 | — |  | 否/待确认 | 继承自 TH-1 |
| 42 | pushi | S (num) | Pushes an integer to the ECL stack. [c=orange]Obsolete, push values to stack by writing unassigned expressions instead. | 是 | 继承自 TH13 |
| 43 | seti | S (var) | Pops an integer from the stack into variable %1. [c=orange]Obsolete, use assignment syntax instead. | 是 | 继承自 TH13 |
| 44 | pushf | f (num) | Pushes a float to the ECL stack. [c=orange]Obsolete, push values to stack by writing unassigned expressions instead. | 是 | 继承自 TH13 |
| 45 | setf | f (var) | Pops a float from the stack into variable %1. [c=orange]Obsolete, use assignment syntax instead. | 是 | 继承自 TH13 |
| 46 | ins_46 | — |  | 否/待确认 | 继承自 TH-1 |
| 47 | ins_47 | — |  | 否/待确认 | 继承自 TH-1 |
| 48 | ins_48 | — |  | 否/待确认 | 继承自 TH-1 |
| 49 | ins_49 | — |  | 否/待确认 | 继承自 TH-1 |
| 50 | addi | — | Sums integers on the stack. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 51 | addf | — | Sums floats on the stack. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 52 | subi | — | Subtracts integers on the stack. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 53 | subf | — | Subtracts floats on the stack. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 54 | muli | — | Multiplies integers on the stack. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 55 | mulf | — | Multiplies floats on the stack. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 56 | divi | — | Divides integers on the stack. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 57 | divf | — | Divides floats on the stack. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 58 | modi | — | Modulo operation on integers on the stack. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 59 | eqi | — | Stack integer `==` comparison. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 60 | eqf | — | Stack float `==` comparison. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 61 | neqi | — | Stack integer `!=` comparison. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 62 | neqf | — | Stack float `!=` comparison. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 63 | lessi | — | Stack integer `<` comparison. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 64 | lessf | — | Stack float `<` comparison. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 65 | leqi | — | Stack integer `<=` comparison. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 66 | leqf | — | Stack float `<=` comparison. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 67 | greateri | — | Stack integer `>` comparison. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 68 | greaterf | — | Stack float `>` comparison. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 69 | geqi | — | Stack integer `>=` comparison. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 70 | geqf | — | Stack float `>=` comparison. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 71 | noti | — | Stack integer NOT operation (e.g. !1). [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 72 | notf | — | Stack float NOT operation (e.g. !1.0f). [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 73 | or | — | Logical OR operation on the stack. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 74 | and | — | Logical AND operation on the stack. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 75 | xor | — | Bitwise XOR operation on integers on the stack. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 76 | bit_or | — | Bitwise OR operation on integers on the stack. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 77 | bit_and | — | Bitwise AND operation on integers on the stack. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 78 | deci | S (var) | Pushes variable %1 to the stack and then decrements it. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 79 | stackSin | — | sin operation on a float on the stack. [c=orange]Obsolete, use `sin(floatVal)` instead. | 是 | 继承自 TH13 |
| 80 | stackCos | — | cos operation on a float on the stack. [c=orange]Obsolete, use `cos(floatVal)` instead. | 是 | 继承自 TH13 |
| 81 | circlePos | ffff (varX, varY, ang, radius) | Performs following operation: [code]%1 = cos(%3)*%4;<br>%2 = sin(%3)*%4;[/code] | 是 | 继承自 TH13 |
| 82 | validRad | f (var) | Normalizes angle in %1. | 是 | 继承自 TH13 |
| 83 | negi | — | Negates an integer on the stack. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 84 | negf | — | Negates a float on the stack. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 85 | squareSum | fff (var, x, y) | Performs following operation: [code]%1 = %2*%2 + %3*%3;[/code] | 是 | 继承自 TH13 |
| 86 | squareSumRoot | fff (var, x, y) | Performs following operation: [code]%1 = sqrt(%2*%2 + %3*%3);[/code] | 是 | 继承自 TH13 |
| 87 | getAngle | fffff (var, x1, y1, x2, y2) | Calculates angle from (%2,%3) to (%4,%5) and stores it in %1. | 是 | 继承自 TH13 |
| 88 | stackSqrt | — | square root operation on a float on the stack. [c=orange]Obsolete, use `sqrt(floatVal)` instead. | 是 | 继承自 TH13 |
| 89 | linearFunc | fff (var, a, x) | Performs following operation: [code]%1 = %2*%3;[/code]<br>(what's the point of making this an instruction, ZUN?) | 是 | 继承自 TH13 |
| 90 | pointRotate | fffff (varX, varY, x, y, rad) | Rotates point (%3,%4) by angle %5 and stores the resulting coordinates in %1 and %2. | 是 | 继承自 TH13 |
| 91 | floatTime | SfSSff (slot, var, time, mode, init, final) | In %3 frames using mode %4, variable %2 changes from %5 to %6. %1 is used to set the slot to be used by this ins, every enemy has 8 slots (0 to 7). | 是 | 继承自 TH13 |
| 92 | math92 | SfSSffff (slot, var, time, mode, init, final, m, n) | Same as ins_91, but takes 2 extra arguments of unknown meaning. Needs investigation. | 否/待确认 | 继承自 TH13 |
| 93 | math93 | ffff (varX, varY, r1, r2) | Gets a random point based on %3 and %4 and stores it on (%1,%2). Needs investigation. | 否/待确认 | 继承自 TH13 |

### TH14 指令：敌机创建与 ANM 管理 / Enemy creation and ANM script management

| ID | 助记名 | 参数 | 说明 | 文档化 | 来源 |
| --- | --- | --- | --- | --- | --- |
| 300 | enmCreate | mffSSS (sub, x, y, hp, score, item) | Creates an enemy using subroutine %1 at coordinates %2, %3 (relative to position of enemy that called it), health of created enemy is %4, score bonus is %5 and item drop is %6. | 是 | 继承自 TH13 |
| 301 | enmCreateA | mffSSS (sub, x, y, hp, score, item) | Creates an enemy using subroutine %1 at coordinates %2, %3 (absolute position), health of created enemy is %4, score bonus is %5 and item drop is %6. | 是 | 继承自 TH13 |
| 302 | anmSelect | S (anmIndex) | Selects ANM file to be used by other instructions based on %1. | 是 | 继承自 TH13 |
| 303 | anmSetSprite | SS (slot, script) | Loads script %2 from ANM selected with ins_302 on slot %1. | 是 | 继承自 TH13 |
| 304 | enmCreateM | mffSSS (sub, x, y, hp, score, item) | Creates a mirrored enemy using subroutine %1 at coordinates %2, %3 (relative to caller's position), health of created enemy is %4, score bonus is %5 and item drop is %6. | 是 | 继承自 TH13 |
| 305 | enmCreateAM | mffSSS (sub, x, y, hp, score, item) | Creates an mirrored enemy using subroutine %1 at coordinates %2, %3 (absolute position), health of created enemy is %4, score bonus is %5 and item drop is %6. | 是 | 继承自 TH13 |
| 306 | anmSetMain | SS (slot, script) | Loads script %2 from ANM selected with ins_302 on slot %1. However, the script number provided will only be used when the enemy is not moving. When moving left %2+1 will be used, right %2+2, diagonal left %2+3, diagonal right %2+4. Might not work properly if %1 is not 0 according to THBWiki. | 是 | 继承自 TH13 |
| 307 | anmPlay | SS (anmIndex, script) | From ANM file selected based on %1, play script %2 at caller's current coordinates. The spawned script is completely independent, and will continue existing even if caller is deleted. | 是 | 继承自 TH13 |
| 308 | anmPlayAbs | SS (anmIndex, script) | From ANM file selected based on %1, play script %2 at coordinates (0, 0). The spawned script is completely independent, and will continue existing even if caller is deleted. | 是 | 继承自 TH13 |
| 309 | enmCreateF | mffSSS (sub, x, y, hp, score, item) | Creates a filler enemy using subroutine %1 at coordinates %2, %3 (relative to caller's position), health of created enemy is %4, score bonus is %5 and item drop is %6. | 是 | 继承自 TH13 |
| 310 | enmCreateAF | mffSSS (sub, x, y, hp, score, item) | Creates a filler enemy using subroutine %1 at coordinates %2, %3 (absolute position), health of created enemy is %4, score bonus is %5 and item drop is %6. | 是 | 继承自 TH13 |
| 311 | enmCreateMF | mffSSS (sub, x, y, hp, score, item) | Creates a mirrored filler enemy using subroutine %1 at coordinates %2, %3 (relative to caller's position), health of created enemy is %4, score bonus is %5 and item drop is %6. | 是 | 继承自 TH13 |
| 312 | enmCreateAMF | mffSSS (sub, x, y, hp, score, item) | Creates a mirrored filler enemy using subroutine %1 at coordinates %2, %3 (absolute position), health of created enemy is %4, score bonus is %5 and item drop is %6. | 是 | 继承自 TH13 |
| 313 | anmSelectedPlay | S (script) | Same as ins_307, except it uses the ANM file selected by ins_302. | 是 | 继承自 TH13 |
| 314 | anmPlayHigh | SS (anmIndex, script) | Same as ins_307, except it spawns the ANM with a higher layer? Needs further investigation. | 否/待确认 | 继承自 TH13 |
| 315 | anmPlayRotate | SSf (anmIndex, script, angle) | Same as ins_307, except it sets rotation of spawned ANM to %3. | 是 | 继承自 TH13 |
| 316 | anm316 | SS (a, b) | Unknown. | 否/待确认 | 继承自 TH13 |
| 317 | anmSwitch | SS (slot, switch) | Sets the execution pointer of ANM script on slot %1 to where ANM `ins_5(a)` with `a` == `switch` is (the time is also changed to match time of `ins_5`). Doesn't work if the value is 0 apparently? | 是 | 继承自 TH13 |
| 318 | anmReset | — | Resets some ANM-related parameters of the caller (TODO: what exactly?) | 是 | 继承自 TH13 |
| 319 | anmRotate | Sf (slot, r) | Set rotation of an ANM script on slot %1 to %2. | 是 | 继承自 TH13 |
| 320 | anmMove | Sff (slot, x, y) | Set position of an ANM script on slot %1 to (%2,%3). This does not detach the script from the caller, so the actual position of the script will be position of the caller + position set here. | 是 | 继承自 TH13 |
| 321 | enmMapleEnemy | mffSSS (sub, x, y, hp, score, item) | ins_300, but used by 'MapleEnemy' (TODO: what's the difference from ins_300?) | 是 | 继承自 TH13 |
| 322 | enm322 | SS (a, b) | Unknown. | 否/待确认 | 继承自 TH13 |
| 323 | deathAnm | SS (anmIndex, script) | Set the animation that will play when the enemy dies to script %2 from ANM file specified by %1. | 是 | 继承自 TH13 |
| 324 | enm324 | — | Unknown. | 否/待确认 | 继承自 TH13 |
| 325 | anmColor | SSSS (slot, R, G, B) | Modify color of ANM script on slot %1, %2, %3, [c=lightblue]%4 correspond to individual colors and have to be from 0 to 255. | 是 | 继承自 TH13 |
| 326 | anmColorTime | SSSSSS (slot, time, mode, R, G, B) | Same as ins_325, but the change is applied in %2 frames using mode %3. | 是 | 继承自 TH13 |
| 327 | anmAlpha | SS (slot, alpha) | Sets alpha of ANM script on slot %1 to %2 (must be a value between 0-255) | 是 | 继承自 TH13 |
| 328 | anmAlphaTime | SSSS (slot, time, mode, alpha) | Same as ins_327, but the change is applied in %2 frames using mode %3. | 是 | 继承自 TH13 |
| 329 | anmScale | Sff (slot, w, h) | Sets horizontal and vertical scaling of ANM script on slot %1 to %2 and %3 respectively. Overwrites scaling properties set by the ANM script. | 是 | 继承自 TH13 |
| 330 | anmScaleTime | SSSff (slot, time, mode, w, h) | Same as ins_329, but the change is applied in %2 frames using mode %3. | 是 | 继承自 TH13 |
| 331 | anmAlpha2 | SS (slot, alpha) | Sets alpha2 (opacity of the gradient) of ANM script on slot %1 to %2. | 是 | 继承自 TH13 |
| 332 | anmAlpha2Time | SSSS (slot, time, mode, alpha) | Same as ins_331, but the change is applied in %2 frames using mode %3. | 是 | 继承自 TH13 |
| 333 | anm333 | SSSff (a, b, c, r, s) | Unknown. Might be doing something to ANM script on slot %1. | 否/待确认 | 继承自 TH13 |
| 334 | anm334 | S (a) | Hard to tell? THBWiki Google translate gives this: 'The animation effect of the playing unit (enemy), the lightning effect near the evil spirit ball of the god temple', which might be referring to lightning around Nue in TD extra stage. | 否/待确认 | 继承自 TH13 |
| 335 | anmScale2 | Sff (slot, w, h) | Same as ins_329, except it doesn't overwrite the scaling set by the ANM script - instead, it multiplies it. | 是 | 继承自 TH13 |
| 336 | anmLayer | SS (slot, layer) | Set layer of ANM script on slot %1 to %2. | 是 | 本作 |
| 337 | anmPlayPos | SSfff (anmIndex, script, x, y, z) | Same as ins_307, but the spawned script is offset by (%3,%4). For 3D objects, %5 is used too (TODO: verify that). | 是 | 本作 |

### TH14 指令：移动管理 / Movement management

| ID | 助记名 | 参数 | 说明 | 文档化 | 来源 |
| --- | --- | --- | --- | --- | --- |
| 400 | movePos | ff (x, y) | Sets caller's absolute position to %1, %2. | 是 | 继承自 TH13 |
| 401 | movePosTime | SSff (time, mode, x, y) | Same as ins_400, but the change is applied in %1 frames using mode %2. | 是 | 继承自 TH13 |
| 402 | movePosRel | ff (x, y) | Sets caller's relative position to %1, %2. | 是 | 继承自 TH13 |
| 403 | movePosRelTime | SSff (time, mode, x, y) | Same as ins_402, but the change is applied in %1 frames using mode %2. | 是 | 继承自 TH13 |
| 404 | moveVel | ff (r, spd) | Sets caller's absolute movement angle to %1 and speed to %2. | 是 | 继承自 TH13 |
| 405 | moveVelTime | SSff (time, mode, r, spd) | Same as ins_404, but the change is applied in %1 frames using mode %2. | 是 | 继承自 TH13 |
| 406 | moveVelRel | ff (r, spd) | Sets caller's relative movement angle to %1 and speed to %2. | 是 | 继承自 TH13 |
| 407 | moveVelRelTime | SSff (time, mode, r, spd) | Same as ins_406, but the change is applied in %1 frames using mode %2. | 是 | 继承自 TH13 |
| 408 | moveCircle | ffff (θ, spd, rad, radInc) | Sets caller's absolute circle movement: %1 is the angle indicating initial position on the circle, %2 is the angular velocity, %3 is circle radius and %4 is by how much the radius increases each frame. | 是 | 继承自 TH13 |
| 409 | moveCircleTime | SSfff (time, mode, spd, rad, radInc) | Same as ins_408, but the change is applied in %1 frames using mode %2. There is also no initial angle parameter here for obvious reason. | 是 | 继承自 TH13 |
| 410 | moveCircleRel | ffff (θ, spd, rad, radInc) | Sets caller's relative circle movement: %1 is the angle indicating initial position on the circle, %2 is the angular velocity, %3 is circle radius and %4 is by how much the radius increases each frame. | 是 | 继承自 TH13 |
| 411 | moveCircleRelTime | SSfff (time, mode, spd, rad, radInc) | Same as ins_410, but the change is applied in %1 frames using mode %2. There is also no initial angle parameter here for obvious reason. | 是 | 继承自 TH13 |
| 412 | moveRand | SSf (time, mode, spd) | Randomizes caller's absolute angle and sets absolute speed to %3. The speed changes back to 0 in %1 frames using mode %2. | 是 | 继承自 TH13 |
| 413 | moveRandRel | SSf (time, mode, spd) | Randomizes caller's relative angle and sets relative speed to %3. The speed changes back to 0 in %1 frames using mode %2. | 是 | 继承自 TH13 |
| 414 | moveBoss | — | Sets caller's absolute position to the absolute position of the boss. If called without a boss, [tip=Google translated from THBWiki, I find this sentence funny]it will cause serious mis-access and explode[/tip]. | 是 | 继承自 TH13 |
| 415 | moveBossRel | — | Sets caller's relative position to the relative position of the boss. If called without a boss, [tip=Google translated from THBWiki, I find this sentence funny]it will cause serious mis-access and explode[/tip]. | 是 | 继承自 TH13 |
| 416 | movePos3d | fff (x, y, z) | Same as ins_400, but takes a %3 parameter for the third dimension, which probably affects 3D ANM scripts used by the caller, or something. | 是 | 继承自 TH13 |
| 417 | movePos3dRel | fff (x, y, z) | Same as ins_402, but takes a %3 parameter for the third dimension, which probably affects 3D ANM scripts used by the caller, or something. | 是 | 继承自 TH13 |
| 418 | moveAdd | ff (x, y) | Increases caller's absolute position by %1 and %2. | 是 | 继承自 TH13 |
| 419 | move419 | ff (x, y) | While the code of this ins looks like it's supposed to be a relative version of ins_418, it doesn't seem to behave like that... | 否/待确认 | 继承自 TH13 |
| 420 | moveEllipse | ffffff (θ, spd, rad, radInc, ellDir, ellRatio) | Sets caller's absolute ellipse movement: %1 is the angle indicating initial position on the ellipse, %2 is the angular velocity, %3 is the base circle radius and %4 is by how much the radius increases each frame. %6 is how much the base circle should be 'squished' to make it an ellipse, and %5 is the squishing angle (I don't know math terms in English, sorry) | 是 | 继承自 TH13 |
| 421 | moveEllipseTime | SSfffff (time, mode, spd, rad, radInc, ellDir, ellRatio) | Same as ins_420, but the change is applied in %1 frames using mode %2. There is also no initial angle parameter here for obvious reason | 是 | 继承自 TH13 |
| 422 | moveEllipseRel | ffffff (θ, spd, rad, radInc, ellDir, ellRatio) | Sets caller's relative ellipse movement: %1 is the angle indicating initial position on the ellipse, %2 is the angular velocity, %3 is the base circle radius and %4 is by how much the radius increases each frame. %6 is how much the base circle should be 'squished' to make it an ellipse, and %5 is the squishing angle (I don't know math terms in English, sorry) | 是 | 继承自 TH13 |
| 423 | moveEllipseRelTime | SSfffff (time, mode, spd, rad, radInc, ellDir, ellRatio) | Same as ins_422, but the change is applied in %1 frames using mode %2. There is also no initial angle parameter here for obvious reason | 是 | 继承自 TH13 |
| 424 | moveSetMirror | S (state) | Sets caller's mirror flag to %1. | 是 | 继承自 TH13 |
| 425 | moveBezier | Sffffff (time, x1, y1, x2, y2, x3, y3) | In %1 frames, the enemy moves towards (%2,%3), then moves towards (%6,%7) for a while and finally moves to (%4,%5). Uses absolute position.<br>From THBWiki: <br>(assuming the current coordinates are (x0, y0)) the motion trajectory is actually a Bezier curve from (x0, y0) to (x2, y2);<br>The P1 coordinate of the curve is `((x1-x0)*1/3, (y1-y0)*1/3)`;<br>The P2 coordinate of the curve is `(-(x3-x2)*1/3+x2,-(y3-y2) *1/3+x2)` | 是 | 继承自 TH13 |
| 426 | moveBezierRel | Sffffff (time, x1, y1, x2, y2, x3, y3) | Same as ins_425, but uses relative position. | 是 | 继承自 TH13 |
| 427 | moveReset | — | Resets some movement-related parameters (TODO: what exactly?) | 否/待确认 | 继承自 TH13 |
| 428 | moveVelNM | ff (r, spd) | Same as ins_404, but ignores the mirror flag. | 是 | 继承自 TH13 |
| 429 | moveVelNMTime | SSff (time, mode, r, spd) | Same as ins_405, but ignores the mirror flag. | 是 | 继承自 TH13 |
| 430 | moveVelNMRel | ff (r, spd) | Same as ins_406, but ignores the mirror flag. | 是 | 继承自 TH13 |
| 431 | moveVelNMRelTime | SSff (time, mode, r, spd) | Same as ins_407, but ignores the mirror flag. | 是 | 继承自 TH13 |
| 432 | moveEnm | S (id) | Sets caller's absolute position to absolute position of enemy with var_-9914 == %1. | 是 | 继承自 TH13 |
| 433 | moveEnmRel | S (id) | Sets caller's relative position to relative position of enemy with var_-9914 == %1. | 是 | 继承自 TH13 |
| 434 | moveCurve | SSSff (time, mode, c, x, y) | In %1 frames using mode %2, caller's absolute position is changed to (%4,%5). The movement trajectory is a curve based on %3, it is unknown how it works exactly. | 否/待确认 | 继承自 TH13 |
| 435 | moveCurveRel | SSSff (time, mode, c, x, y) | In %1 frames using mode %2, caller's relative position is changed to (%4,%5). The movement trajectory is a curve based on %3, it is unknown how it works exactly. | 否/待确认 | 继承自 TH13 |
| 436 | moveAddTime | SSff (time, mode, x, y) | Same as ins_418, but the change is applied in %1 frames using mode %2. | 是 | 继承自 TH13 |
| 437 | moveAddRelTime | SSff (time, mode, x, y) | Same as ins_419, but the change is applied in %1 frames using mode %2 (it also behaves as expected, unlike ins_419). | 是 | 继承自 TH13 |
| 438 | moveCurveAdd | SSSff (time, mode, c, x, y) | Same as ins_434, but instead caller's current absolute coordinates are added to %4 and %5. | 是 | 继承自 TH13 |
| 439 | moveCurveAddRel | SSSff (time, mode, c, x, y) | Same as ins_435, but instead caller's current relative coordinates are added to %4 and %5. | 是 | 继承自 TH13 |
| 440 | moveAngle | f (r) | Sets caller's absolute movement angle to %1. | 是 | 本作 |
| 441 | moveAngleTime | SSf (time, mode, r) | Same as ins_440, but the change is applied in %1 frames using mode %2. | 是 | 本作 |
| 442 | moveAngleRel | f (r) | Sets caller's relative movement angle to %1. | 是 | 本作 |
| 443 | moveAngleRelTime | SSf (time, mode, r) | Same as ins_442, but the change is applied in %1 frames using mode %2. | 是 | 本作 |
| 444 | moveSpeed | f (spd) | Sets caller's absolute movement speed to %1. | 是 | 本作 |
| 445 | moveSpeedTime | SSf (time, mode, spd) | Same as ins_444, but the change is applied in %1 frames using mode %2. | 是 | 本作 |
| 446 | moveSpeedRel | f (spd) | Sets caller's relative movement speed to %1. | 是 | 本作 |
| 447 | moveSpeedRelTime | SSf (time, mode, spd) | Same as ins_446, but the change is applied in %1 frames using mode %2. | 是 | 本作 |

### TH14 指令：敌机属性与杂项 / Enemy property management and other miscellaneous things

| ID | 助记名 | 参数 | 说明 | 文档化 | 来源 |
| --- | --- | --- | --- | --- | --- |
| 500 | setHurtbox | ff (w, h) | Sets caller's hurtbox width to %1 and height to %2. | 是 | 继承自 TH13 |
| 501 | setHitbox | ff (w, h) | Sets caller's hitbox width to %1 and height to %2. | 是 | 继承自 TH13 |
| 502 | flagSet | S (n) | Sets flag(s) according to %1. Refer to the [flag table](#s=modding/flags) for exact values. | 是 | 继承自 TH13 |
| 503 | flagClear | S (n) | Clears flag(s) according to %1. Refer to the [flag table](#s=modding/flags) for exact values. | 是 | 继承自 TH13 |
| 504 | moveLimit | ffff (x, y, w, h) | Sets caller's movement limit rectangle: (%1,%2) are the coordinates of the center of the rect, while %3, %4 are width and height of it. | 是 | 继承自 TH13 |
| 505 | moveLimitReset | — | Removes caller's movement limit. | 是 | 继承自 TH13 |
| 506 | dropClear | — | Clears caller's extra item drop. | 是 | 继承自 TH13 |
| 507 | dropExtra | SS (type, amount) | Adds %2 items of type %1 to caller's extra drop. Item type table will be made in the future. | 是 | 继承自 TH13 |
| 508 | dropArea | ff (w, h) | Sets caller's item drop area width to %1 and height to %2. | 是 | 继承自 TH13 |
| 509 | dropItems | — | Drops all items the caller has. Has no effect in spell practice. | 是 | 继承自 TH13 |
| 510 | dropMain | S (type) | Sets caller's main drop to %1. | 是 | 继承自 TH13 |
| 511 | lifeSet | S (hp) | Sets caller's current HP and max HP to %1. | 是 | 继承自 TH13 |
| 512 | setBoss | S (a) | If %1 is 0, activates boss mode and makes the caller the main boss. If %1 > 0, it makes the caller the secondary boss. If %1 is -1, ends boss mode. | 是 | 继承自 TH13 |
| 513 | timerReset | — | Resets boss timer. | 是 | 继承自 TH13 |
| 514 | setInterrupt | SSSm (slot, hp, time, sub) | Sets an interrupt on slot %1 (not sure how many slots there are) - once caller's hp reaches %2 or %3 frames have passed since this was called, caller will terminate all subs it's currently running and execute sub %4. | 是 | 继承自 TH13 |
| 515 | setInvuln | S (time) | Makes the caller completely invulnerable for %1 frames. | 是 | 继承自 TH13 |
| 516 | playSound | S (id) | Plays sound %1. Sound id table will be added in the future. | 是 | 继承自 TH13 |
| 517 | setScreenShake | SSS (time, startIntensity, endIntensity) | Activates screen shake for %1 frames. %2 is the starting intensity and %3 is the ending intensity. The larger the intensity, the more the screen shakes. | 是 | 继承自 TH13 |
| 518 | dialogRead | S (dialogueId) | Starts a dialogue, %1 is the ID of an entry in the .msg file. Apart from that, has the effect ins_525. | 是 | 继承自 TH13 |
| 519 | dialogWait | — | Waits until there are no dialogues active, or the running .msg script calls a certain instruction (which one?) | 否/待确认 | 继承自 TH13 |
| 520 | bossWait | — | Waits until there are no boss enemies. | 是 | 继承自 TH13 |
| 521 | setTimeout | Sm (slot, sub) | Sets a timeout interrupt on slot %1 - when the timer reaches 0, caller will terminate all subs it's currently running and execute sub %2. | 是 | 继承自 TH13 |
| 522 | spellEx | SSSm (id, time, unused, name) | Same as ins_537, but the difficulty number is NOT added to the id. | 是 | 继承自 TH13 |
| 523 | spellEnd | — | Ends currently active spellcard. | 是 | 继承自 TH13 |
| 524 | setChapter | S (a) | Some jank that's responsible for showing boss name and possibly other things. In LoLK, it also ends the current chapter and begins a new one. | 否/待确认 | 继承自 TH13 |
| 525 | enmKillAll | — | Kills all other enemies (unless they have a flag that prevents that set). | 是 | 继承自 TH13 |
| 526 | etProtectRange | f (r) | Makes bullets generated by the caller not spawn if they are in radius %1 around the player. | 是 | 继承自 TH13 |
| 527 | lifeMarker | SfS (slot, hp, c) | Sets a new life marker on slot %1, %2 determines where the marker will appear on the health bar (if %2=1000.0f and the enemy has 2000 hp, the marker will split the hp bar in half). %3 is an RGB value of unknown use (possibly leftover from earlier ECL versions) | 是 | 继承自 TH13 |
| 528 | spellUnused | SSSm (id, time, unused, name) | No difference from ins_522, unused. | 是 | 继承自 TH13 |
| 529 | rankF3 | ffff (var, a, b, c) | Sets %1 to %2 if rank is low, %3 if rank is average or %4 if rank is high. | 是 | 继承自 TH13 |
| 530 | rankF5 | ffffff (var, a, b, c, d, e) | Sets %1 to %2 if rank is very low, %3 if rank is low, %4 if rank is average, %5 if rank is high or %6 if rank is very high. | 是 | 继承自 TH13 |
| 531 | rankF2 | fff (var, a, b) | Sets %1 to %2 if rank is low or %3 if rank is high. | 是 | 继承自 TH13 |
| 532 | rankI3 | SSSS (var, a, b, c) | Sets %1 to %2 if rank is low, %3 if rank is average or %4 if rank is high. | 是 | 继承自 TH13 |
| 533 | rankI5 | SSSSSS (var, a, b, c, d, e) | Sets %1 to %2 if rank is very low, %3 if rank is low, %4 if rank is average, %5 if rank is high or %6 if rank is very high. | 是 | 继承自 TH13 |
| 534 | rankI2 | SSS (var, a, b) | Sets %1 to %2 if rank is low or %3 if rank is high. | 是 | 继承自 TH13 |
| 535 | diffI | SSSSS (var, E, N, H, L) | Sets %1 to one of values provided based on difficulty. | 是 | 继承自 TH13 |
| 536 | diffF | fffff (var, E, N, H, L) | Sets %1 to one of values provided based on difficulty. | 是 | 继承自 TH13 |
| 537 | spell | SSSm (id, time, unused, name) | Declares a spellcard with id %1 and name %4. The actual ID passed to the spell-creating function is `id + difficulty`, with easy=0, normal=1, hard=2, lunatic=3, ex=4, overdrive=5. <br>%2 determines how much time the spell circle takes to shrink (in frames), as well as how fast the spell bonus decreases. The exact formula is as follows: <br>[code] int factor = maxSCB >> 2; // maxSCB is hardcoded<br> currSCB -= (maxSCB - factor) / (%2 - 300);<br> currSCB -= currSCB % 10; [/code] <br>As you can guess, setting %2 to 300 causes a division by 0 error and crashes the game, while setting it to a value smaller than 300 causes the SCB to increase over time, instead of decreasing. %3 is unused. | 是 | 继承自 TH13 |
| 538 | spell2 | SSSm (id, time, unused, name) | Same as ins_537, except the ID used is `id - 1 + difficulty`. | 是 | 继承自 TH13 |
| 539 | spell3 | SSSm (id, time, unused, name) | Same as ins_537, except the ID used is `id - 2 + difficulty`. | 是 | 继承自 TH13 |
| 540 | stars | S (cnt) | Sets the amount of stars displayed in the top left corner. Stars might not appear at all if there is no boss active. | 是 | 继承自 TH13 |
| 541 | noHitboxDur | S (time) | Disables the hitbox (but not the hurtbox) for the given amount of frames. | 是 | 继承自 TH13 |
| 542 | spellTimeout | — | Makes the current spell a timeout spell (prevent spell bonus from decreasing, give capture bonus if timed out). | 是 | 继承自 TH13 |
| 543 | unknown543 | — | Unknown. | 否/待确认 | 继承自 TH13 |
| 544 | unknown544 | S (a) | Unknown, sets or clears some flag? | 否/待确认 | 继承自 TH13 |
| 545 | laserCancel | — | Cancels all lasers. | 是 | 继承自 TH13 |
| 546 | bombShield | SS (a, script) | Sets the bomb invulnerability flag (%1=1 set, %1=0 not set), the caller's ANM script will change to %2 when a bomb is active (how does it work with ANM slots exactly?) | 是 | 继承自 TH13 |
| 547 | gameSpeed | f (s) | Sets game speed to %1 of the normal speed. In ISC, enemies with flag 13 (dec=8192) set will ignore effects of this opcode. | 是 | 继承自 TH13 |
| 548 | diffWait | SSSS (e, n, h, l) | Same as ins_23, but the wait time is chosen from the given 4 based on the difficulty. | 是 | 继承自 TH13 |
| 549 | unknown549 | S (a) | Unknown. | 否/待确认 | 继承自 TH13 |
| 550 | unknown550 | S (a) | Unknown. | 否/待确认 | 继承自 TH13 |
| 551 | unknown551 | S (a) | Unknown. | 否/待确认 | 继承自 TH13 |
| 552 | zIndex | S (layers) | Increases layer of all ANM scripts used by the caller by %1. | 是 | 继承自 TH13 |
| 553 | hitSound | S (id) | Makes the caller play sound %1 when hit. Sound id table will be added in the future. | 是 | 继承自 TH13 |
| 554 | stageLogo | — | Shows the stage logo from an ANM of a hardcoded name. | 是 | 继承自 TH13 |
| 555 | enmAlive | SS (var, id) | Checks if enemy of var_-9914 == %2 is still alive, and sets %1 to 1 if it is or 0 if it isn't. | 是 | 继承自 TH13 |
| 556 | setDeath | m (sub) | Makes the caller execute sub %1 when the HP reaches 0. Keep in mind that the caller is already marked for deletion at the point when the sub actually executes, so if you put waiting there the sub will not execute fully (because the caller will be deleted) | 是 | 继承自 TH13 |
| 557 | fogTime | SSSff (time, mode, color, start, end) | Same as STD ins_9, that is, fogTime. Refer to [the STD instruction table](#s=modding/std-ins) for details. | 是 | 继承自 TH13 |
| 558 | flagMirror | S (state) | Literally the exact same instruction as ins_424. | 是 | 继承自 TH13 |
| 559 | enmLimit | S (limit) | Set the maximum number of enemies that can be present. New enemies will fail to spawn if the cap is reached. Default is 99999. | 是 | 继承自 TH13 |
| 560 | unknown560 | ff (r, s) | Unknown. | 否/待确认 | 继承自 TH13 |
| 561 | die | — | Makes the caller execute the sub set with ins_556. If there is no such sub set, the caller dies instead (exactly the same as if the player shot down the caller, that is, items are dropped, death sound plays etc) | 是 | 继承自 TH13 |
| 562 | dropItemsSp | — | Same as ins_509, but item spawning will not be blocked in spell practice. | 是 | 继承自 TH13 |
| 563 | unknown563 | S (flagState) | Sets [flag 12](#s=modding/flags) (decimal 4096), which controls whether the hitbox and hurtbox is a rectangle. If %1 is 1, collision is a rectangle. If %1 is 0, collision is elliptical. | 是 | 本作 |
| 564 | hitboxRotate | f (angle) | Rotates the hitbox and hurtbox of the enemy (note: the hitbox rotation is really janky, but hurtbox rotates fine). Has no effect unless the enemy uses rectangular collision. | 是 | 本作 |
| 565 | bombInvuln | f (red) | Sets caller's damage reduction when a bomb is active, 0.0f means no damage at all, 1.0f is full damage, negative values will make the enemy heal when you bomb. | 是 | 本作 |
| 566 | unknown566 | () | Unknown (does it even exist?) | 否/待确认 | 本作 |
| 567 | unknown567 | S (a) | Unknown. | 否/待确认 | 本作 |
| 568 | spellMode | S (state) | Enables/disables spell card damage reduction, if %1 is 1 it's enabled, if it's 0 it's disabled. Can be used outside of spell cards. | 是 | 本作 |

### TH14 指令：子弹创建与删除 / Bullet creation and deletion

| ID | 助记名 | 参数 | 说明 | 文档化 | 来源 |
| --- | --- | --- | --- | --- | --- |
| 600 | etNew | S (etId) | Resets bullet manager %1 to default properties. | 是 | 继承自 TH13 |
| 601 | etOn | S (etId) | Shoots bullet(s) using properties from bullet manager %1. | 是 | 继承自 TH13 |
| 602 | etSprite | SSS (etId, type, color) | Sets bullet type and color of bullet manager %1. Pre-th15 bullet types are yet to be documented. | 是 | 继承自 TH13 |
| 603 | etOffset | Sff (etId, x, y) | Sets the relative offset of bullets spawned by bullet manager %1 to (%2,%3). | 是 | 继承自 TH13 |
| 604 | etAngle | Sff (etId, angle1, angle2) | Sets angle1 and angle2 of bullet manager %1. | 是 | 继承自 TH13 |
| 605 | etSpeed | Sff (etId, speed1, speed2) | Sets speed1 and speed2 of bullet manager %1. | 是 | 继承自 TH13 |
| 606 | etCount | SSS (etId, count1, count2) | Sets count1 and count2 of bullet manager %1. | 是 | 继承自 TH13 |
| 607 | etAim | SS (etId, aim) | Sets aim mode of bullet manager %1. | 是 | 继承自 TH13 |
| 608 | etSound | SSS (etId, sound1, sound2) | Sets sound1 and sound2 of bullet manager %1 (sound effect table is TODO). sound1 plays when the bullet manager fires a bullet, while sound2 plays when a bullet fired by the bullet manager does certain transformations. Set to -1 for no sound. | 是 | 继承自 TH13 |
| 609 | etExSet | SSSSSSff (etId, index, async, type, a, b, r, s) | Sets bullet transformation of bullet manager %1, transformation explanation will be added in the future. | 是 | 继承自 TH13 |
| 610 | etExSet2 | SSSSSSSSffff (etId, index, async, type, a, b, c, d, r, s, m, n) | Same as ins_609, but takes more arguments for certain transformation types. | 是 | 继承自 TH13 |
| 611 | etEx | SSSSSff (etId, async, type, a, b, r, s) | Adds bullet transformation to bullet manager %1, transformation explanation will be added in the future. | 是 | 继承自 TH13 |
| 612 | etEx2 | SSSSSSSffff (etId, async, type, a, b, c, d, r, s, m, n) | Same as ins_611, but takes more arguments for certain transformation types. | 是 | 继承自 TH13 |
| 613 | etClearAll | — | Clears all bullets. | 是 | 继承自 TH13 |
| 614 | etCopy | SS (etIdDest, etIdSrc) | Copies everything from bullet manager %2 into bullet manager %1. Warning: this instruction is partially broken and does NOT copy the index next ins_611/ins_612 transformations will be added at. | 是 | 继承自 TH13 |
| 615 | etCancel | f (r) | Clears all bullets in a circle of radius %1 around the caller, and turns them into cancel items. | 是 | 继承自 TH13 |
| 616 | etClear | f (r) | Clears all bullets in a circle of radius %1 around the caller without turning them into cancel items. | 是 | 继承自 TH13 |
| 617 | etSpeedR3 | Sffffff (etId, spd1l, spd1m, spd1h, spd2l, spd2m, spd2h) | Sets speed1 and speed2 of bullet manager %1 to two of the values provided, based on ingame rank (l=low, m=medium, h=high) | 是 | 继承自 TH13 |
| 618 | etSpeedR5 | Sffffffffff (etId, spd1l, spd1ml, spd1m, spd1mh, spd1h, spd2l, spd2ml, spd2m, spd2mh, spd2h) | Sets speed1 and speed2 of bullet manager %1 to two of the values provided, based on ingame rank (l=low, ml=medium-low, m=medium, mh=medium-high, h=high) | 是 | 继承自 TH13 |
| 619 | etSpeedR2 | Sffff (etId, spd1l, spd1h, spd2l, spd2h) | Sets speed1 and speed2 of bullet manager %1 to two of the values provided, based on ingame rank (l=low, h=high) | 是 | 继承自 TH13 |
| 620 | etCountR3 | SSSSSSS (etId, cnt1l, cnt1m, cnt1h, cnt2l, cnt2m, cnt2h) | Sets count1 and count2 of bullet manager %1 to two of the values provided, based on ingame rank (l=low, m=medium, h=high) | 是 | 继承自 TH13 |
| 621 | etCountR5 | SSSSSSSSSSS (etId, cnt1l, cnt1ml, cnt1m, cnt1mh, cnt1h, cnt2l, cnt2ml, cnt2m, cnt2mh, cnt2h) | Sets count1 and count2 of bullet manager %1 to two of the values provided, based on ingame rank (l=low, ml=medium-low, m=medium, mh=medium-high, h=high) | 是 | 继承自 TH13 |
| 622 | etCountR2 | SSSSS (etId, cnt1l, cnt1h, cnt2l, cnt2h) | Sets count1 and count2 of bullet manager %1 to two of the values provided, based on ingame rank (l=low, h=high) | 是 | 继承自 TH13 |
| 623 | angleToPlayer | fff (var, x, y) | Gets angle to the player from coordinates (%2,%3) and stores it in %1. | 是 | 继承自 TH13 |
| 624 | etSpeedD | Sffffffff (etId, spd1e, spd1n, spd1h, spd1l, spd2e, spd2n, spd2h, spd2l) | Sets speed1 and speed2 of bullet manager %1 to 2 of the values provided, based on the difficulty (e=easy, n=normal, h=hard, l=lunatic) | 是 | 继承自 TH13 |
| 625 | etCountD | SSSSSSSSS (etId, cnt1e, cnt1n, cnt1h, cnt1l, cnt2e, cnt2n, cnt2h, cnt2l) | Sets count1 and count2 of bullet manager %1 to 2 of the values provided, based on the difficulty (e=easy, n=normal, h=hard, l=lunatic) | 是 | 继承自 TH13 |
| 626 | etOffsetRad | Sff (etId, angle, radius) | Sets the relative offset of bullets spawned by bullet manager %1 to (cos(%2)\*%3,sin(%2)\*%3). Stacks with ins_603. | 是 | 继承自 TH13 |
| 627 | etDist | Sf (etId, dist) | Sets distance of bullets spawned by bullet manager %1 to %2 (that is, when a bullet is spawned it moves by %2 using its current angle). | 是 | 继承自 TH13 |
| 628 | etOffsetAbs | Sff (etId, x, y) | Sets the absolute offset of bullets spawned by bullet manager %1 to (%2,%3). | 是 | 继承自 TH13 |
| 629 | fog | fS (r, color) | Sets caller's fog's radius to %1 and color to %2 (RGB value in reverse order). This resets the fog completely, that is, every time it's called the fog spawn animation plays. | 是 | 继承自 TH13 |
| 630 | callSTD | S (switch) | Sets execution pointer of the STD script to where STD ins_16(%1) is (%1 must be the same), basically same concept as ins_317. | 是 | 继承自 TH13 |
| 631 | lifeHide | S (time) | Hides boss lifebar for %1 frames. | 是 | 继承自 TH13 |
| 632 | funcSet | S (id) | Sets a function that the game will execute every frame from a set of hardcoded functions that differs between games. | 是 | 继承自 TH13 |
| 633 | flagExtDmg | S (state) | Sets the external damage flag to %1. Caller probably needs to be the main boss for this to work - with this flag set, the caller gets damaged by the value stored in var_-9940 every frame, and then resets the value. This allows other enemies to damage the boss by incrementing the aforementioned variable, used in LoLK by Sagume (and also happens to be the main cause of the Sagume skip glitch) | 是 | 继承自 TH13 |
| 634 | setHitboxFunc | S (id) | Make the caller use a special function for determining collision with the player. TODO: create a list of functions and their IDs | 是 | 继承自 TH13 |
| 635 | etCancel2 | f (r) | Same as ins_615, but doesn't clear bullets with bomb invulnerability. | 是 | 继承自 TH13 |
| 636 | etClear2 | f (r) | Same as ins_616, but doesn't clear bullets with bomb invulnerability. | 是 | 继承自 TH13 |
| 637 | funcCall | S (id) | Same as ins_632, except the function is called just once instead of every frame. | 是 | 继承自 TH13 |
| 638 | scoreAdd | S (n) | Adds %1 to score (or subtracts if %1 is negative). There is no lower boundary check, so if this causes score to go below 0, an underflow happens. | 是 | 继承自 TH13 |
| 639 | funcSet2 | S (id) | Same as ins_632, except it sets an unknown flag to 1 (ins_632 sets it to 0) | 是 | 继承自 TH13 |
| 640 | etExSub | SSm (etId, index, s) | Sets the string parameter of transform on index %2 in bullet manager %1 to %3, transformations will be explained separately later. | 是 | 继承自 TH13 |
| 641 | etExSubtract | S (etId) | Subtracts 1 from the index used by ins_611 and ins_612, unless it's already 0. This basically changes where the next transformation will be appended. | 是 | 本作 |

### TH14 指令：激光创建 / Laser creation

| ID | 助记名 | 参数 | 说明 | 文档化 | 来源 |
| --- | --- | --- | --- | --- | --- |
| 700 | laserNew | Sffff (etId, init_length, final_length, unknown_arg_3, width) | Sets basic parameters of the laser. %4 has something to do with the length of straight line lasers (investigation needed), but doesn't do anything for other laser types. For curvy lasers, the only used argument is %5, and length is specified with ins_701 instead. | 是 | 继承自 TH13 |
| 701 | laserTiming | SSSSSS (edId, startup_time, expand_time, duration, shrink_time, init_flags) | Sets timing for infinite lasers. %6 sets the initial flags for a laser, but these flags are unknown at the moment. For curvy lasers, the %2 argument instead specifies the length of the laser. | 是 | 继承自 TH13 |
| 702 | laserOn | S (edId) | Shoots a straight line laser. | 是 | 继承自 TH13 |
| 703 | laserStOn | SS (etId, laser_id) | Shoots an infinite laser. %2 is a number that's used to identify this particular laser instance, so that it can be referred to in other instructions. | 是 | 继承自 TH13 |
| 704 | laserOffset | Sff (laser_id, x, y) | Sets the position of the infinite laser pointed to by %1. | 是 | 继承自 TH13 |
| 705 | laserTrajectory | Sff (laser_id, x_speed, y_speed) | Sets the offset velocity of the infinite laser pointed to by %1. The laser's position will change by %2 and %3 every frame. | 是 | 继承自 TH13 |
| 706 | laserStLength | Sf (laser_id, speed) | Sets the speed of the infinite laser pointed to by %1. | 是 | 继承自 TH13 |
| 707 | laserStWidth | Sf (laser_id, width) | Sets the width of the infinite laser pointed to by %1. | 是 | 继承自 TH13 |
| 708 | laserStAngle | Sf (laser_id, angle) | Sets the angle of the infinite laser pointed to by %1. | 是 | 继承自 TH13 |
| 709 | laserStRotation | Sf (laser_id, angular_vel) | Sets the angular velocity of the infinite laser pointed to by %1. The laser's angle will change by %2 every frame. | 是 | 继承自 TH13 |
| 710 | laserStEnd | S (laser_id) | Clears the laser pointed to by %1. | 是 | 继承自 TH13 |
| 711 | laserCuOn | S (etId) | Shoots a curvy laser. | 是 | 继承自 TH13 |
| 712 | etCancelRect | ff (w, h) | Cancels all bullets in rectangle of width %1 and height %2. The area is affected by rotation set by ins_564. | 是 | 本作 |
| 713 | unknown713 | SS (etId, laser_id) | Shoots a laser 'beam', a laser type used by marisa in GFW. Broken since this laser type does not exist outside of GFW. | 是 | 继承自 TH13 |
| 714 | unknown714 | SS (laser_id, unknown) | Does something with a laser beam pointed to by %1. Broken since this laser type does not exist outside of GFW. | 是 | 继承自 TH13 |

### TH14 指令：敌机交互 / Enemy interaction

| ID | 助记名 | 参数 | 说明 | 文档化 | 来源 |
| --- | --- | --- | --- | --- | --- |
| 800 | enmCall | Sm (id, sub) | Makes enemy with var_-9914 == %1 stop all subs it's running and execute sub %2 (works like an interrupt). This will NOT make the enemy execute the sub right as this instruction is called, the new sub will be executed when the game handles the given enemy, which might be later on the same frame or on the next frame. Using this to make the caller interrupt itself can make the game explode. | 是 | 继承自 TH13 |
| 801 | enmPos | ffS (varX, varY, id) | Stores coordinates of enemy with var_-9914 == %3 in (%1,%2). | 是 | 继承自 TH13 |
| 802 | broadcastInterrupt | S (slot) | For all existing bosses, trigger the interrupt set by ins_514 on slot %1. Does not change the HP to the one set in ins_514. | 是 | 继承自 TH13 |

### TH14 指令：调试 / Debug

| ID | 助记名 | 参数 | 说明 | 文档化 | 来源 |
| --- | --- | --- | --- | --- | --- |
| 900 | debug900 | — | 未在 Priw8 表中记录/待确认 | 否/待确认 | — |
| 901 | debug901 | — | 未在 Priw8 表中记录/待确认 | 否/待确认 | — |
| 902 | debug902 | — | 未在 Priw8 表中记录/待确认 | 否/待确认 | — |

### TH14 指令：游戏特有 / Game specific

| ID | 助记名 | 参数 | 说明 | 文档化 | 来源 |
| --- | --- | --- | --- | --- | --- |
| 1000 | spec0 | — | 未在 Priw8 表中记录/待确认 | 否/待确认 | — |
| 1001 | spec1 | — | 未在 Priw8 表中记录/待确认 | 否/待确认 | — |
| 1002 | spec2 | — | 未在 Priw8 表中记录/待确认 | 否/待确认 | — |
| 1003 | spec3 | — | 未在 Priw8 表中记录/待确认 | 否/待确认 | — |

### TH14 变量

| ID | 名称 | 类型 | 访问 | 作用域 | 说明 | 文档化 | 来源 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| -10000 | RAND | int | 只读 | global/全局 | Random integer, very large range. | 是 | 继承自 TH10 |
| -9999.0f | RANDF | float | 只读 | global/全局 | Random float from 0.0f to 1.0f. | 是 | 继承自 TH10 |
| -9998.0f | RANDRAD | float | 只读 | global/全局 | Random float from -pi to pi. | 是 | 继承自 TH10 |
| -9997.0f | FINAL_X | float | 只读 | local/敌机局部 | Final X position of the enemy. | 是 | 继承自 TH10 |
| -9996.0f | FINAL_Y | float | 只读 | local/敌机局部 | Final Y position of the enemy. | 是 | 继承自 TH10 |
| -9995.0f | ABS_X | float | 只读 | local/敌机局部 | Absolute X position of the enemy. | 是 | 继承自 TH10 |
| -9994.0f | ABS_Y | float | 只读 | local/敌机局部 | Absolute Y position of the enemy. | 是 | 继承自 TH10 |
| -9993.0f | REL_X | float | 只读 | local/敌机局部 | Relative X position of the enemy. | 是 | 继承自 TH10 |
| -9992.0f | REL_Y | float | 只读 | local/敌机局部 | Relative Y position of the enemy. | 是 | 继承自 TH10 |
| -9991.0f | PLAYER_X | float | 只读 | global/全局 | Player's X position. | 是 | 继承自 TH10 |
| -9990.0f | PLAYER_Y | float | 只读 | global/全局 | Player's Y position. | 是 | 继承自 TH10 |
| -9989.0f | ANGLE_PLAYER | float | 只读 | local/敌机局部 | Angle from the enemy to the player. | 是 | 继承自 TH10 |
| -9988 | TIME | int | 只读 | local/敌机局部 | Time elapsed since the enemy spawned, in frames. | 是 | 继承自 TH10 |
| -9987.0f | RANDF2 | float | 只读 | global/全局 | Random float from -1.0f to 1.0f. | 是 | 继承自 TH10 |
| -9986 | TIMEOUT | int | 只读 | global/全局 | Set to 1 by the engine when a timeout occurs. | 是 | 继承自 TH10 |
| -9985 | I0 | int | 读写 | local/敌机局部 | Local integer variable, inherited by spawned enemies. | 是 | 继承自 TH10 |
| -9984 | I1 | int | 读写 | local/敌机局部 | Local integer variable, inherited by spawned enemies. | 是 | 继承自 TH10 |
| -9983 | I2 | int | 读写 | local/敌机局部 | Local integer variable, inherited by spawned enemies. | 是 | 继承自 TH10 |
| -9982 | I3 | int | 读写 | local/敌机局部 | Local integer variable, inherited by spawned enemies. | 是 | 继承自 TH10 |
| -9981.0f | F0 | float | 读写 | local/敌机局部 | Local float variable, inherited by spawned enemies. | 是 | 继承自 TH10 |
| -9980.0f | F1 | float | 读写 | local/敌机局部 | Local float variable, inherited by spawned enemies. | 是 | 继承自 TH10 |
| -9979.0f | F2 | float | 读写 | local/敌机局部 | Local float variable, inherited by spawned enemies. | 是 | 继承自 TH10 |
| -9978.0f | F3 | float | 读写 | local/敌机局部 | Local float variable, inherited by spawned enemies. | 是 | 继承自 TH10 |
| -9977.0f | FINAL_X2 | float | 只读 | local/敌机局部 | Same as var_-9997. | 是 | 继承自 TH10 |
| -9976.0f | FINAL_Y2 | float | 只读 | local/敌机局部 | Same as var_-9996. | 是 | 继承自 TH10 |
| -9975.0f | ABS_X2 | float | 只读 | local/敌机局部 | Same as var_-9995. | 是 | 继承自 TH10 |
| -9974.0f | ABS_Y2 | float | 只读 | local/敌机局部 | Same as var_-9994. | 是 | 继承自 TH10 |
| -9973.0f | REL_X2 | float | 只读 | local/敌机局部 | Same as var_-9993. | 是 | 继承自 TH10 |
| -9972.0f | REL_Y2 | float | 只读 | local/敌机局部 | Same as var_-9992. | 是 | 继承自 TH10 |
| -9971.0f | ABS_ANGLE | float | 只读 | local/敌机局部 | Angle of enemy's absolute movement. | 是 | 继承自 TH10 |
| -9970.0f | REL_ANGLE | float | 只读 | local/敌机局部 | Angle of enemy's relative movement. | 是 | 继承自 TH10 |
| -9969.0f | ABS_SPEED | float | 只读 | local/敌机局部 | Speed of enemy's absolute movement. | 是 | 继承自 TH10 |
| -9968.0f | REL_SPEED | float | 只读 | local/敌机局部 | Speed of enemy's relative movement. | 是 | 继承自 TH10 |
| -9967.0f | ABS_ORIGIN_DIST | float | 只读 | local/敌机局部 | Distance from the origin of enemy's absolute circular movement (radius of the circle). | 是 | 继承自 TH10 |
| -9966.0f | REL_ORIGIN_DIST | float | 只读 | local/敌机局部 | Distance from the origin of enemy's relative circular movement (radius of the circle). | 是 | 继承自 TH10 |
| -9965.0f | PLAYER_X2 | float | 只读 | global/全局 | Same as var_-9991. | 是 | 继承自 TH10 |
| -9964.0f | PLAYER_Y2 | float | 只读 | global/全局 | Same as var_-9990. | 是 | 继承自 TH10 |
| -9963.0f | BOSS_X | float | 只读 | global/全局 | Final X position of the boss. | 是 | 继承自 TH10 |
| -9962.0f | BOSS_Y | float | 只读 | global/全局 | Final Y position of the boss. | 是 | 继承自 TH10 |
| -9961 | ANM_ID | int | 只读 | local/敌机局部 | Is the current script on anm slot 0 of the enemy. | 是 | 继承自 TH10 |
| -9960 | RANK | int | 只读 | global/全局 | Numeric value of rank, ranging from -1024 to 1024. Increases over time and decreases when player bombs/dies etc. | 是 | 继承自 TH10 |
| -9959 | DIFF | int | 只读 | global/全局 | Difficulty (E=0, N=1, H=2, L=3, EX=4, O=5) | 是 | 继承自 TH10 |
| -9958.0f | FINAL_ANGLE | float | 只读 | local/敌机局部 | Final angle of enemy's movement. | 是 | 继承自 TH10 |
| -9957 | TRUE | int | 只读 | global/全局 | Always returns 1. | 是 | 继承自 TH10 |
| -9956.0f | ABS_ANGLE_PLAYER | float | 只读 | local/敌机局部 | Angle to the player from enemy's absolute position. | 是 | 继承自 TH10 |
| -9955.0f | REL_ANGLE_PLAYER | float | 只读 | local/敌机局部 | Angle to the player from enemy's relative position. | 是 | 继承自 TH10 |
| -9954 | LIFE | int | 只读 | local/敌机局部 | Enemy's current HP. | 是 | 继承自 TH10 |
| -9953 | EASY | int | 只读 | global/全局 | Set to 1 if difficulty is easy, otherwise it's 0. | 是 | 继承自 TH10 |
| -9952 | NORMAL | int | 只读 | global/全局 | Set to 1 if difficulty is normal, otherwise it's 0. | 是 | 继承自 TH10 |
| -9951 | HARD | int | 只读 | global/全局 | Set to 1 if difficulty is hard, otherwise it's 0. | 是 | 继承自 TH10 |
| -9950 | LUNATIC | int | 只读 | global/全局 | Set to 1 if difficulty is lunatic, otherwise it's 0. | 是 | 继承自 TH10 |
| -9949 | MISS_COUNT | int | 读写 | global/全局 | Increased by 1 every time the player dies. | 是 | 继承自 TH11 |
| -9948 | BOMB_COUNT | int | 读写 | global/全局 | Increased by 1 every time the player bombs. | 是 | 继承自 TH11 |
| -9947 | CAPTURE | int | 读写 | global/全局 | Set to 0 when the player dies, bombs, or uses a game-specific mechanic that "fails" a spell. | 是 | 继承自 TH11 |
| -9946 | ENM_CNT_REAL | int | 只读 | global/全局 | Amount of enemies alive (including main and MapleEnemy). | 是 | 继承自 TH11 |
| -9945 | SHOTTYPE | int | 只读 | global/全局 | Numeric value that represents player's shottype, the first shottype is 0. | 是 | 继承自 TH11 |
| -9944.0f | DIST_PLAYER | float | 只读 | local/敌机局部 | Distance from the enemy to the player. | 是 | 继承自 TH11 |
| -9943 | BI0 | int | 读写 | local/敌机局部 | Is the same as the I0 variable of boss 0. | 是 | 继承自 TH11 |
| -9942 | BI1 | int | 读写 | local/敌机局部 | Is the same as the I1 variable of boss 0. | 是 | 继承自 TH11 |
| -9941 | BI2 | int | 读写 | local/敌机局部 | Is the same as the I2 variable of boss 0. | 是 | 继承自 TH11 |
| -9940 | BI3 | int | 读写 | local/敌机局部 | Is the same as the I3 variable of boss 0. | 是 | 继承自 TH11 |
| -9939.0f | BF0 | float | 读写 | local/敌机局部 | Is the same as the F0 variable of boss 0. | 是 | 继承自 TH11 |
| -9938.0f | BF1 | float | 读写 | local/敌机局部 | Is the same as the F1 variable of boss 0. | 是 | 继承自 TH11 |
| -9937.0f | BF2 | float | 读写 | local/敌机局部 | Is the same as the F2 variable of boss 0. | 是 | 继承自 TH11 |
| -9936.0f | BF3 | float | 读写 | local/敌机局部 | Is the same as the F3 variable of boss 0. | 是 | 继承自 TH11 |
| -9935.0f | F4 | float | 读写 | local/敌机局部 | Local float variable inherited by spawned enemies, just like F0-F3 and I0-I3. | 是 | 继承自 TH11 |
| -9934.0f | F5 | float | 读写 | local/敌机局部 | Local float variable inherited by spawned enemies, just like F0-F3 and I0-I3. | 是 | 继承自 TH11 |
| -9933.0f | F6 | float | 读写 | local/敌机局部 | Local float variable inherited by spawned enemies, just like F0-F3 and I0-I3. | 是 | 继承自 TH11 |
| -9932.0f | F7 | float | 读写 | local/敌机局部 | Local float variable inherited by spawned enemies, just like F0-F3 and I0-I3. | 是 | 继承自 TH11 |
| -9931 | LAST_ENM_ID | int | 只读 | global/全局 | ID of the last spawned enemy. | 是 | 继承自 TH12 |
| -9930 | POWER | int | 只读 | global/全局 | Player's power (4.00 => 400) | 是 | 继承自 TH12 |
| -9929 | DS1 | int | 只读 | global/全局 | Used in Double Spoiler, unknown. | 否/待确认 | 继承自 TH12.5 |
| -9928 | DS2 | int | 只读 | global/全局 | Used in Double Spoiler, unknown. | 否/待确认 | 继承自 TH12.5 |
| -9927 | DS3 | int | 只读 | global/全局 | Used in Double Spoiler, unknown. | 否/待确认 | 继承自 TH12.5 |
| -9926 | GI0 | int | 读写 | global/全局 | Global integer variable. | 是 | 继承自 TH12.5 |
| -9925 | GI1 | int | 读写 | global/全局 | Global integer variable. | 是 | 继承自 TH12.5 |
| -9924 | GI2 | int | 读写 | global/全局 | Global integer variable. | 是 | 继承自 TH12.5 |
| -9923 | GI3 | int | 读写 | global/全局 | Global integer variable. | 是 | 继承自 TH12.5 |
| -9922.0f | GF0 | float | 读写 | global/全局 | Global float variable. | 是 | 继承自 TH12.5 |
| -9921.0f | GF1 | float | 读写 | global/全局 | Global float variable. | 是 | 继承自 TH12.5 |
| -9920.0f | GF2 | float | 读写 | global/全局 | Global float variable. | 是 | 继承自 TH12.5 |
| -9919.0f | GF3 | float | 读写 | global/全局 | Global float variable. | 是 | 继承自 TH12.5 |
| -9918.0f | GF4 | float | 读写 | global/全局 | Global float variable. | 是 | 继承自 TH12.5 |
| -9917.0f | GF5 | float | 读写 | global/全局 | Global float variable. | 是 | 继承自 TH12.5 |
| -9916.0f | GF6 | float | 读写 | global/全局 | Global float variable. | 是 | 继承自 TH12.5 |
| -9915.0f | GF7 | float | 读写 | global/全局 | Global float variable. | 是 | 继承自 TH12.5 |
| -9914 | ID | int | 只读 | local/敌机局部 | ID of the enemy. | 是 | 继承自 TH12.5 |
| -9913 | DS_PHOTOCOUNT | int | 只读 | global/全局 | Used in Double Spoiler, amount of photos taken. | 是 | 继承自 TH12.5 |
| -9912 | DS4 | int | 只读 | global/全局 | Used in Double Spoiler, unknown. | 否/待确认 | 继承自 TH12.5 |
| -9911.0f | ANGLE_BOSS | float | 只读 | global/全局 | Angle at which the boss moves. | 是 | 继承自 TH12.5 |
| -9910.0f | SPEED_BOSS | float | 只读 | global/全局 | Speed at which the boss moves. | 是 | 继承自 TH12.5 |
| -9909 | UNKNOWN9 | int | 只读 | local/敌机局部 | Enemy ID of the parent enemy. | 是 | 继承自 TH12.8 |
| -9908 | ENM_CNT | int | 只读 | global/全局 | Amount of killable enemies alive (that is, doesn't include hitboxless/intangible enemies etc). | 是 | 继承自 TH13 |
| -9907 | SPELL_ID | int | 只读 | global/全局 | Spellcard ID, used by spell practice. Unknown meaning in LoLK. | 是 | 继承自 TH13 |

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

## TH15 东方绀珠传

- 体系：第四世代
- 指令：普通指令 319 条；已说明 257/319。主要分组：系统/流程/栈/算术 / System；敌机创建与 ANM 管理 / Enemy creation and ANM script management；移动管理 / Movement management；敌机属性与杂项 / Enemy property management and other miscellaneous things；子弹创建与删除 / Bullet creation and deletion；激光创建 / Laser creation；敌机交互 / Enemy interaction；调试 / Debug；游戏特有 / Game specific。
- 变量：变量范围 -10000..-9904；本文列出有说明/命名记录的 97 条，未列空洞/未知项。

### TH15 指令：系统/流程/栈/算术 / System

| ID | 助记名 | 参数 | 说明 | 文档化 | 来源 |
| --- | --- | --- | --- | --- | --- |
| 0 | nop | — | Empty instruction, doesn't do anything. | 是 | 继承自 TH13 |
| 1 | delete | — | Returns to the top of current call stack. | 是 | 继承自 TH13 |
| 2 | ins_2 | — |  | 否/待确认 | 继承自 TH-1 |
| 3 | ins_3 | — |  | 否/待确认 | 继承自 TH-1 |
| 4 | ins_4 | — |  | 否/待确认 | 继承自 TH-1 |
| 5 | ins_5 | — |  | 否/待确认 | 继承自 TH-1 |
| 6 | ins_6 | — |  | 否/待确认 | 继承自 TH-1 |
| 7 | ins_7 | — |  | 否/待确认 | 继承自 TH-1 |
| 8 | ins_8 | — |  | 否/待确认 | 继承自 TH-1 |
| 9 | ins_9 | — |  | 否/待确认 | 继承自 TH-1 |
| 10 | ret | — | Returns from the current sub. | 是 | 继承自 TH13 |
| 11 | call | m (sub) | Calls a given sub. Can take additional parameters to pass as arguments to the sub. [c=orange]Direct Usage obsolete. Use `@subName()` syntax instead. | 是 | 继承自 TH13 |
| 12 | jmp | o (target) | Unconditionally jumps to the label %1. [c=orange]Direct usage obsolete. Use `goto label` syntax instead. | 是 | 继承自 TH13 |
| 13 | jmpEq | o (target) | Pops a number from the stack and if it evaluates to false (in this context, 0), jumps to label %1. [c=orange]Direct usage obsolete. Use if/unless statement instead. | 是 | 继承自 TH13 |
| 14 | jmpNeq | o (target) | Pops a number from the stack and if it evaluates to true (in this context, anything non-0), jumps to label %1. [c=orange]Direct usage obsolete. Use if/unless statement instead. | 是 | 继承自 TH13 |
| 15 | callAsync | m (sub) | Asynchronously calls a given sub. Can take additional parameters to pass as arguments to the sub. [c=orange]Direct usage obsolete. Use `@subName() async` syntax instead. | 是 | 继承自 TH13 |
| 16 | callAsyncId | mS (sub, id) | Asynchronously calls a given sub and assigns it ID %2. Can take additional parameters to pass as arguments to the sub. [c=orange]Direct usage obsolete, use, `@subName() async id` syntax instead. | 是 | 继承自 TH13 |
| 17 | killAsync | S (id) | Ends most recently called sub that has ID %1 (same ID as in ins_16). If no sub with the given ID is found, nothing happens. Using ID -1 can lead to various unexpected results, ranging from deleting the enemy to freezing the game. | 是 | 继承自 TH13 |
| 18 | ins_18 | S (id) | Let `vm` be the most recent async sub running with ID %1: this ins sets `vm[0x000011E4]` to 1. | 否/待确认 | 继承自 TH13 |
| 19 | ins_19 | S (id) | Let `vm` be the most recent async sub running with ID %1: this ins sets `vm[0x000011E4]` to 0. | 否/待确认 | 继承自 TH13 |
| 20 | ins_20 | SS (id, b) | Let `vm` be the most recent async sub running with ID %1: this ins sets `vm[0x0000101C]` to %2. | 否/待确认 | 继承自 TH13 |
| 21 | killAllAsync | — | Ends all running async subs. Calling this in an async sub can lead to unexpected results, such as crashing the game. | 是 | 继承自 TH13 |
| 22 | debug22 | Sm (a, b) | Debug instruction, code does not exist in the release builds of the game. Most likely used to call sub %2 if some variable set in a debug menu is equal to %1. | 是 | 继承自 TH13 |
| 23 | wait | S (time) | Stops sub execution for %1 frames. | 是 | 继承自 TH13 |
| 24 | waitf | f (time) | ins_23, but time is given as a float instead of an int. Subframes do actually exist and affect ins_547. | 是 | 继承自 TH13 |
| 25 | ins_25 | — |  | 否/待确认 | 继承自 TH-1 |
| 26 | ins_26 | — |  | 否/待确认 | 继承自 TH-1 |
| 27 | unknown27 | — |  | 否/待确认 | 继承自 TH-1 |
| 28 | ins_28 | — |  | 否/待确认 | 继承自 TH-1 |
| 29 | ins_29 | — |  | 否/待确认 | 继承自 TH-1 |
| 30 | unknown30 | m (formatString) | Some sort of `printf` debug instruction, which can take additional float/int arguments after %1. Its code does not exist in the release builds. | 是 | 继承自 TH13 |
| 31 | unknown31 | — |  | 否/待确认 | 继承自 TH-1 |
| 32 | ins_32 | — |  | 否/待确认 | 继承自 TH-1 |
| 33 | ins_33 | — |  | 否/待确认 | 继承自 TH-1 |
| 34 | ins_34 | — |  | 否/待确认 | 继承自 TH-1 |
| 35 | ins_35 | — |  | 否/待确认 | 继承自 TH-1 |
| 36 | ins_36 | — |  | 否/待确认 | 继承自 TH-1 |
| 37 | ins_37 | — |  | 否/待确认 | 继承自 TH-1 |
| 38 | ins_38 | — |  | 否/待确认 | 继承自 TH-1 |
| 39 | ins_39 | — |  | 否/待确认 | 继承自 TH-1 |
| 40 | stackAlloc | S (size) | Increases the ECL stack pointer by %1 bytes (probably), to make space for sub variables. [c=orange]Obsolete, thecl generates this instruction automatically. | 是 | 继承自 TH13 |
| 41 | ins_41 | — |  | 否/待确认 | 继承自 TH-1 |
| 42 | pushi | S (num) | Pushes an integer to the ECL stack. [c=orange]Obsolete, push values to stack by writing unassigned expressions instead. | 是 | 继承自 TH13 |
| 43 | seti | S (var) | Pops an integer from the stack into variable %1. [c=orange]Obsolete, use assignment syntax instead. | 是 | 继承自 TH13 |
| 44 | pushf | f (num) | Pushes a float to the ECL stack. [c=orange]Obsolete, push values to stack by writing unassigned expressions instead. | 是 | 继承自 TH13 |
| 45 | setf | f (var) | Pops a float from the stack into variable %1. [c=orange]Obsolete, use assignment syntax instead. | 是 | 继承自 TH13 |
| 46 | ins_46 | — |  | 否/待确认 | 继承自 TH-1 |
| 47 | ins_47 | — |  | 否/待确认 | 继承自 TH-1 |
| 48 | ins_48 | — |  | 否/待确认 | 继承自 TH-1 |
| 49 | ins_49 | — |  | 否/待确认 | 继承自 TH-1 |
| 50 | addi | — | Sums integers on the stack. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 51 | addf | — | Sums floats on the stack. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 52 | subi | — | Subtracts integers on the stack. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 53 | subf | — | Subtracts floats on the stack. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 54 | muli | — | Multiplies integers on the stack. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 55 | mulf | — | Multiplies floats on the stack. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 56 | divi | — | Divides integers on the stack. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 57 | divf | — | Divides floats on the stack. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 58 | modi | — | Modulo operation on integers on the stack. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 59 | eqi | — | Stack integer `==` comparison. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 60 | eqf | — | Stack float `==` comparison. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 61 | neqi | — | Stack integer `!=` comparison. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 62 | neqf | — | Stack float `!=` comparison. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 63 | lessi | — | Stack integer `<` comparison. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 64 | lessf | — | Stack float `<` comparison. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 65 | leqi | — | Stack integer `<=` comparison. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 66 | leqf | — | Stack float `<=` comparison. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 67 | greateri | — | Stack integer `>` comparison. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 68 | greaterf | — | Stack float `>` comparison. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 69 | geqi | — | Stack integer `>=` comparison. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 70 | geqf | — | Stack float `>=` comparison. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 71 | noti | — | Stack integer NOT operation (e.g. !1). [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 72 | notf | — | Stack float NOT operation (e.g. !1.0f). [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 73 | or | — | Logical OR operation on the stack. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 74 | and | — | Logical AND operation on the stack. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 75 | xor | — | Bitwise XOR operation on integers on the stack. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 76 | bit_or | — | Bitwise OR operation on integers on the stack. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 77 | bit_and | — | Bitwise AND operation on integers on the stack. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 78 | deci | S (var) | Pushes variable %1 to the stack and then decrements it. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 79 | stackSin | — | sin operation on a float on the stack. [c=orange]Obsolete, use `sin(floatVal)` instead. | 是 | 继承自 TH13 |
| 80 | stackCos | — | cos operation on a float on the stack. [c=orange]Obsolete, use `cos(floatVal)` instead. | 是 | 继承自 TH13 |
| 81 | circlePos | ffff (varX, varY, ang, radius) | Performs following operation: [code]%1 = cos(%3)*%4;<br>%2 = sin(%3)*%4;[/code] | 是 | 继承自 TH13 |
| 82 | validRad | f (var) | Normalizes angle in %1. | 是 | 继承自 TH13 |
| 83 | negi | — | Negates an integer on the stack. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 84 | negf | — | Negates a float on the stack. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 85 | squareSum | fff (var, x, y) | Performs following operation: [code]%1 = %2*%2 + %3*%3;[/code] | 是 | 继承自 TH13 |
| 86 | squareSumRoot | fff (var, x, y) | Performs following operation: [code]%1 = sqrt(%2*%2 + %3*%3);[/code] | 是 | 继承自 TH13 |
| 87 | getAngle | fffff (var, x1, y1, x2, y2) | Calculates angle from (%2,%3) to (%4,%5) and stores it in %1. | 是 | 继承自 TH13 |
| 88 | stackSqrt | — | square root operation on a float on the stack. [c=orange]Obsolete, use `sqrt(floatVal)` instead. | 是 | 继承自 TH13 |
| 89 | linearFunc | fff (var, a, x) | Performs following operation: [code]%1 = %2*%3;[/code]<br>(what's the point of making this an instruction, ZUN?) | 是 | 继承自 TH13 |
| 90 | pointRotate | fffff (varX, varY, x, y, rad) | Rotates point (%3,%4) by angle %5 and stores the resulting coordinates in %1 and %2. | 是 | 继承自 TH13 |
| 91 | floatTime | SfSSff (slot, var, time, mode, init, final) | In %3 frames using mode %4, variable %2 changes from %5 to %6. %1 is used to set the slot to be used by this ins, every enemy has 8 slots (0 to 7). | 是 | 继承自 TH13 |
| 92 | math92 | SfSSffff (slot, var, time, mode, init, final, m, n) | Same as ins_91, but takes 2 extra arguments of unknown meaning. Needs investigation. | 否/待确认 | 继承自 TH13 |
| 93 | math93 | ffff (varX, varY, r1, r2) | Gets a random point based on %3 and %4 and stores it on (%1,%2). Needs investigation. | 否/待确认 | 继承自 TH13 |

### TH15 指令：敌机创建与 ANM 管理 / Enemy creation and ANM script management

| ID | 助记名 | 参数 | 说明 | 文档化 | 来源 |
| --- | --- | --- | --- | --- | --- |
| 300 | enmCreate | mffSSS (sub, x, y, hp, score, item) | Creates an enemy using subroutine %1 at coordinates %2, %3 (relative to position of enemy that called it), health of created enemy is %4, score bonus is %5 and item drop is %6. | 是 | 继承自 TH13 |
| 301 | enmCreateA | mffSSS (sub, x, y, hp, score, item) | Creates an enemy using subroutine %1 at coordinates %2, %3 (absolute position), health of created enemy is %4, score bonus is %5 and item drop is %6. | 是 | 继承自 TH13 |
| 302 | anmSelect | S (anmIndex) | Selects ANM file to be used by other instructions based on %1. | 是 | 继承自 TH13 |
| 303 | anmSetSprite | SS (slot, script) | Loads script %2 from ANM selected with ins_302 on slot %1. | 是 | 继承自 TH13 |
| 304 | enmCreateM | mffSSS (sub, x, y, hp, score, item) | Creates a mirrored enemy using subroutine %1 at coordinates %2, %3 (relative to caller's position), health of created enemy is %4, score bonus is %5 and item drop is %6. | 是 | 继承自 TH13 |
| 305 | enmCreateAM | mffSSS (sub, x, y, hp, score, item) | Creates an mirrored enemy using subroutine %1 at coordinates %2, %3 (absolute position), health of created enemy is %4, score bonus is %5 and item drop is %6. | 是 | 继承自 TH13 |
| 306 | anmSetMain | SS (slot, script) | Loads script %2 from ANM selected with ins_302 on slot %1. However, the script number provided will only be used when the enemy is not moving. When moving left %2+1 will be used, right %2+2, diagonal left %2+3, diagonal right %2+4. Might not work properly if %1 is not 0 according to THBWiki. | 是 | 继承自 TH13 |
| 307 | anmPlay | SS (anmIndex, script) | From ANM file selected based on %1, play script %2 at caller's current coordinates. The spawned script is completely independent, and will continue existing even if caller is deleted. | 是 | 继承自 TH13 |
| 308 | anmPlayAbs | SS (anmIndex, script) | From ANM file selected based on %1, play script %2 at coordinates (0, 0). The spawned script is completely independent, and will continue existing even if caller is deleted. | 是 | 继承自 TH13 |
| 309 | enmCreateF | mffSSS (sub, x, y, hp, score, item) | Creates a filler enemy using subroutine %1 at coordinates %2, %3 (relative to caller's position), health of created enemy is %4, score bonus is %5 and item drop is %6. | 是 | 继承自 TH13 |
| 310 | enmCreateAF | mffSSS (sub, x, y, hp, score, item) | Creates a filler enemy using subroutine %1 at coordinates %2, %3 (absolute position), health of created enemy is %4, score bonus is %5 and item drop is %6. | 是 | 继承自 TH13 |
| 311 | enmCreateMF | mffSSS (sub, x, y, hp, score, item) | Creates a mirrored filler enemy using subroutine %1 at coordinates %2, %3 (relative to caller's position), health of created enemy is %4, score bonus is %5 and item drop is %6. | 是 | 继承自 TH13 |
| 312 | enmCreateAMF | mffSSS (sub, x, y, hp, score, item) | Creates a mirrored filler enemy using subroutine %1 at coordinates %2, %3 (absolute position), health of created enemy is %4, score bonus is %5 and item drop is %6. | 是 | 继承自 TH13 |
| 313 | anmSelectedPlay | S (script) | Same as ins_307, except it uses the ANM file selected by ins_302. | 是 | 继承自 TH13 |
| 314 | anmPlayHigh | SS (anmIndex, script) | Same as ins_307, except it spawns the ANM with a higher layer? Needs further investigation. | 否/待确认 | 继承自 TH13 |
| 315 | anmPlayRotate | SSf (anmIndex, script, angle) | Same as ins_307, except it sets rotation of spawned ANM to %3. | 是 | 继承自 TH13 |
| 316 | anm316 | SS (a, b) | Unknown. | 否/待确认 | 继承自 TH13 |
| 317 | anmSwitch | SS (slot, switch) | Sets the execution pointer of ANM script on slot %1 to where ANM `ins_5(a)` with `a` == `switch` is (the time is also changed to match time of `ins_5`). Doesn't work if the value is 0 apparently? | 是 | 继承自 TH13 |
| 318 | anmReset | — | Resets some ANM-related parameters of the caller (TODO: what exactly?) | 是 | 继承自 TH13 |
| 319 | anmRotate | Sf (slot, r) | Set rotation of an ANM script on slot %1 to %2. | 是 | 继承自 TH13 |
| 320 | anmMove | Sff (slot, x, y) | Set position of an ANM script on slot %1 to (%2,%3). This does not detach the script from the caller, so the actual position of the script will be position of the caller + position set here. | 是 | 继承自 TH13 |
| 321 | enmMapleEnemy | mffSSS (sub, x, y, hp, score, item) | ins_300, but used by 'MapleEnemy' (TODO: what's the difference from ins_300?) | 是 | 继承自 TH13 |
| 322 | enm322 | SS (a, b) | Unknown. | 否/待确认 | 继承自 TH13 |
| 323 | deathAnm | SS (anmIndex, script) | Set the animation that will play when the enemy dies to script %2 from ANM file specified by %1. | 是 | 继承自 TH13 |
| 324 | enm324 | — | Unknown. | 否/待确认 | 继承自 TH13 |
| 325 | anmColor | SSSS (slot, R, G, B) | Modify color of ANM script on slot %1, %2, %3, [c=lightblue]%4 correspond to individual colors and have to be from 0 to 255. | 是 | 继承自 TH13 |
| 326 | anmColorTime | SSSSSS (slot, time, mode, R, G, B) | Same as ins_325, but the change is applied in %2 frames using mode %3. | 是 | 继承自 TH13 |
| 327 | anmAlpha | SS (slot, alpha) | Sets alpha of ANM script on slot %1 to %2 (must be a value between 0-255) | 是 | 继承自 TH13 |
| 328 | anmAlphaTime | SSSS (slot, time, mode, alpha) | Same as ins_327, but the change is applied in %2 frames using mode %3. | 是 | 继承自 TH13 |
| 329 | anmScale | Sff (slot, w, h) | Sets horizontal and vertical scaling of ANM script on slot %1 to %2 and %3 respectively. Overwrites scaling properties set by the ANM script. | 是 | 继承自 TH13 |
| 330 | anmScaleTime | SSSff (slot, time, mode, w, h) | Same as ins_329, but the change is applied in %2 frames using mode %3. | 是 | 继承自 TH13 |
| 331 | anmAlpha2 | SS (slot, alpha) | Sets alpha2 (opacity of the gradient) of ANM script on slot %1 to %2. | 是 | 继承自 TH13 |
| 332 | anmAlpha2Time | SSSS (slot, time, mode, alpha) | Same as ins_331, but the change is applied in %2 frames using mode %3. | 是 | 继承自 TH13 |
| 333 | anm333 | SSSff (a, b, c, r, s) | Unknown. Might be doing something to ANM script on slot %1. | 否/待确认 | 继承自 TH13 |
| 334 | anm334 | S (a) | Hard to tell? THBWiki Google translate gives this: 'The animation effect of the playing unit (enemy), the lightning effect near the evil spirit ball of the god temple', which might be referring to lightning around Nue in TD extra stage. | 否/待确认 | 继承自 TH13 |
| 335 | anmScale2 | Sff (slot, w, h) | Same as ins_329, except it doesn't overwrite the scaling set by the ANM script - instead, it multiplies it. | 是 | 继承自 TH13 |
| 336 | anmLayer | SS (slot, layer) | Set layer of ANM script on slot %1 to %2. | 是 | 继承自 TH14 |
| 337 | anmPlayPos | SSfff (anmIndex, script, x, y, z) | Same as ins_307, but the spawned script is offset by (%3,%4). For 3D objects, %5 is used too (TODO: verify that). | 是 | 继承自 TH14 |

### TH15 指令：移动管理 / Movement management

| ID | 助记名 | 参数 | 说明 | 文档化 | 来源 |
| --- | --- | --- | --- | --- | --- |
| 400 | movePos | ff (x, y) | Sets caller's absolute position to %1, %2. | 是 | 继承自 TH13 |
| 401 | movePosTime | SSff (time, mode, x, y) | Same as ins_400, but the change is applied in %1 frames using mode %2. | 是 | 继承自 TH13 |
| 402 | movePosRel | ff (x, y) | Sets caller's relative position to %1, %2. | 是 | 继承自 TH13 |
| 403 | movePosRelTime | SSff (time, mode, x, y) | Same as ins_402, but the change is applied in %1 frames using mode %2. | 是 | 继承自 TH13 |
| 404 | moveVel | ff (r, spd) | Sets caller's absolute movement angle to %1 and speed to %2. | 是 | 继承自 TH13 |
| 405 | moveVelTime | SSff (time, mode, r, spd) | Same as ins_404, but the change is applied in %1 frames using mode %2. | 是 | 继承自 TH13 |
| 406 | moveVelRel | ff (r, spd) | Sets caller's relative movement angle to %1 and speed to %2. | 是 | 继承自 TH13 |
| 407 | moveVelRelTime | SSff (time, mode, r, spd) | Same as ins_406, but the change is applied in %1 frames using mode %2. | 是 | 继承自 TH13 |
| 408 | moveCircle | ffff (θ, spd, rad, radInc) | Sets caller's absolute circle movement: %1 is the angle indicating initial position on the circle, %2 is the angular velocity, %3 is circle radius and %4 is by how much the radius increases each frame. | 是 | 继承自 TH13 |
| 409 | moveCircleTime | SSfff (time, mode, spd, rad, radInc) | Same as ins_408, but the change is applied in %1 frames using mode %2. There is also no initial angle parameter here for obvious reason. | 是 | 继承自 TH13 |
| 410 | moveCircleRel | ffff (θ, spd, rad, radInc) | Sets caller's relative circle movement: %1 is the angle indicating initial position on the circle, %2 is the angular velocity, %3 is circle radius and %4 is by how much the radius increases each frame. | 是 | 继承自 TH13 |
| 411 | moveCircleRelTime | SSfff (time, mode, spd, rad, radInc) | Same as ins_410, but the change is applied in %1 frames using mode %2. There is also no initial angle parameter here for obvious reason. | 是 | 继承自 TH13 |
| 412 | moveRand | SSf (time, mode, spd) | Randomizes caller's absolute angle and sets absolute speed to %3. The speed changes back to 0 in %1 frames using mode %2. | 是 | 继承自 TH13 |
| 413 | moveRandRel | SSf (time, mode, spd) | Randomizes caller's relative angle and sets relative speed to %3. The speed changes back to 0 in %1 frames using mode %2. | 是 | 继承自 TH13 |
| 414 | moveBoss | — | Sets caller's absolute position to the absolute position of the boss. If called without a boss, [tip=Google translated from THBWiki, I find this sentence funny]it will cause serious mis-access and explode[/tip]. | 是 | 继承自 TH13 |
| 415 | moveBossRel | — | Sets caller's relative position to the relative position of the boss. If called without a boss, [tip=Google translated from THBWiki, I find this sentence funny]it will cause serious mis-access and explode[/tip]. | 是 | 继承自 TH13 |
| 416 | movePos3d | fff (x, y, z) | Same as ins_400, but takes a %3 parameter for the third dimension, which probably affects 3D ANM scripts used by the caller, or something. | 是 | 继承自 TH13 |
| 417 | movePos3dRel | fff (x, y, z) | Same as ins_402, but takes a %3 parameter for the third dimension, which probably affects 3D ANM scripts used by the caller, or something. | 是 | 继承自 TH13 |
| 418 | moveAdd | ff (x, y) | Increases caller's absolute position by %1 and %2. | 是 | 继承自 TH13 |
| 419 | move419 | ff (x, y) | While the code of this ins looks like it's supposed to be a relative version of ins_418, it doesn't seem to behave like that... | 否/待确认 | 继承自 TH13 |
| 420 | moveEllipse | ffffff (θ, spd, rad, radInc, ellDir, ellRatio) | Sets caller's absolute ellipse movement: %1 is the angle indicating initial position on the ellipse, %2 is the angular velocity, %3 is the base circle radius and %4 is by how much the radius increases each frame. %6 is how much the base circle should be 'squished' to make it an ellipse, and %5 is the squishing angle (I don't know math terms in English, sorry) | 是 | 继承自 TH13 |
| 421 | moveEllipseTime | SSfffff (time, mode, spd, rad, radInc, ellDir, ellRatio) | Same as ins_420, but the change is applied in %1 frames using mode %2. There is also no initial angle parameter here for obvious reason | 是 | 继承自 TH13 |
| 422 | moveEllipseRel | ffffff (θ, spd, rad, radInc, ellDir, ellRatio) | Sets caller's relative ellipse movement: %1 is the angle indicating initial position on the ellipse, %2 is the angular velocity, %3 is the base circle radius and %4 is by how much the radius increases each frame. %6 is how much the base circle should be 'squished' to make it an ellipse, and %5 is the squishing angle (I don't know math terms in English, sorry) | 是 | 继承自 TH13 |
| 423 | moveEllipseRelTime | SSfffff (time, mode, spd, rad, radInc, ellDir, ellRatio) | Same as ins_422, but the change is applied in %1 frames using mode %2. There is also no initial angle parameter here for obvious reason | 是 | 继承自 TH13 |
| 424 | moveSetMirror | S (state) | Sets caller's mirror flag to %1. | 是 | 继承自 TH13 |
| 425 | moveBezier | Sffffff (time, x1, y1, x2, y2, x3, y3) | In %1 frames, the enemy moves towards (%2,%3), then moves towards (%6,%7) for a while and finally moves to (%4,%5). Uses absolute position.<br>From THBWiki: <br>(assuming the current coordinates are (x0, y0)) the motion trajectory is actually a Bezier curve from (x0, y0) to (x2, y2);<br>The P1 coordinate of the curve is `((x1-x0)*1/3, (y1-y0)*1/3)`;<br>The P2 coordinate of the curve is `(-(x3-x2)*1/3+x2,-(y3-y2) *1/3+x2)` | 是 | 继承自 TH13 |
| 426 | moveBezierRel | Sffffff (time, x1, y1, x2, y2, x3, y3) | Same as ins_425, but uses relative position. | 是 | 继承自 TH13 |
| 427 | moveReset | — | Resets some movement-related parameters (TODO: what exactly?) | 否/待确认 | 继承自 TH13 |
| 428 | moveVelNM | ff (r, spd) | Same as ins_404, but ignores the mirror flag. | 是 | 继承自 TH13 |
| 429 | moveVelNMTime | SSff (time, mode, r, spd) | Same as ins_405, but ignores the mirror flag. | 是 | 继承自 TH13 |
| 430 | moveVelNMRel | ff (r, spd) | Same as ins_406, but ignores the mirror flag. | 是 | 继承自 TH13 |
| 431 | moveVelNMRelTime | SSff (time, mode, r, spd) | Same as ins_407, but ignores the mirror flag. | 是 | 继承自 TH13 |
| 432 | moveEnm | S (id) | Sets caller's absolute position to absolute position of enemy with var_-9914 == %1. | 是 | 继承自 TH13 |
| 433 | moveEnmRel | S (id) | Sets caller's relative position to relative position of enemy with var_-9914 == %1. | 是 | 继承自 TH13 |
| 434 | moveCurve | SSSff (time, mode, c, x, y) | In %1 frames using mode %2, caller's absolute position is changed to (%4,%5). The movement trajectory is a curve based on %3, it is unknown how it works exactly. | 否/待确认 | 继承自 TH13 |
| 435 | moveCurveRel | SSSff (time, mode, c, x, y) | In %1 frames using mode %2, caller's relative position is changed to (%4,%5). The movement trajectory is a curve based on %3, it is unknown how it works exactly. | 否/待确认 | 继承自 TH13 |
| 436 | moveAddTime | SSff (time, mode, x, y) | Same as ins_418, but the change is applied in %1 frames using mode %2. | 是 | 继承自 TH13 |
| 437 | moveAddRelTime | SSff (time, mode, x, y) | Same as ins_419, but the change is applied in %1 frames using mode %2 (it also behaves as expected, unlike ins_419). | 是 | 继承自 TH13 |
| 438 | moveCurveAdd | SSSff (time, mode, c, x, y) | Same as ins_434, but instead caller's current absolute coordinates are added to %4 and %5. | 是 | 继承自 TH13 |
| 439 | moveCurveAddRel | SSSff (time, mode, c, x, y) | Same as ins_435, but instead caller's current relative coordinates are added to %4 and %5. | 是 | 继承自 TH13 |
| 440 | moveAngle | f (r) | Sets caller's absolute movement angle to %1. | 是 | 继承自 TH14 |
| 441 | moveAngleTime | SSf (time, mode, r) | Same as ins_440, but the change is applied in %1 frames using mode %2. | 是 | 继承自 TH14 |
| 442 | moveAngleRel | f (r) | Sets caller's relative movement angle to %1. | 是 | 继承自 TH14 |
| 443 | moveAngleRelTime | SSf (time, mode, r) | Same as ins_442, but the change is applied in %1 frames using mode %2. | 是 | 继承自 TH14 |
| 444 | moveSpeed | f (spd) | Sets caller's absolute movement speed to %1. | 是 | 继承自 TH14 |
| 445 | moveSpeedTime | SSf (time, mode, spd) | Same as ins_444, but the change is applied in %1 frames using mode %2. | 是 | 继承自 TH14 |
| 446 | moveSpeedRel | f (spd) | Sets caller's relative movement speed to %1. | 是 | 继承自 TH14 |
| 447 | moveSpeedRelTime | SSf (time, mode, spd) | Same as ins_446, but the change is applied in %1 frames using mode %2. | 是 | 继承自 TH14 |

### TH15 指令：敌机属性与杂项 / Enemy property management and other miscellaneous things

| ID | 助记名 | 参数 | 说明 | 文档化 | 来源 |
| --- | --- | --- | --- | --- | --- |
| 500 | setHurtbox | ff (w, h) | Sets caller's hurtbox width to %1 and height to %2. | 是 | 继承自 TH13 |
| 501 | setHitbox | ff (w, h) | Sets caller's hitbox width to %1 and height to %2. | 是 | 继承自 TH13 |
| 502 | flagSet | S (n) | Sets flag(s) according to %1. Refer to the [flag table](#s=modding/flags) for exact values. | 是 | 继承自 TH13 |
| 503 | flagClear | S (n) | Clears flag(s) according to %1. Refer to the [flag table](#s=modding/flags) for exact values. | 是 | 继承自 TH13 |
| 504 | moveLimit | ffff (x, y, w, h) | Sets caller's movement limit rectangle: (%1,%2) are the coordinates of the center of the rect, while %3, %4 are width and height of it. | 是 | 继承自 TH13 |
| 505 | moveLimitReset | — | Removes caller's movement limit. | 是 | 继承自 TH13 |
| 506 | dropClear | — | Clears caller's extra item drop. | 是 | 继承自 TH13 |
| 507 | dropExtra | SS (type, amount) | Adds %2 items of type %1 to caller's extra drop. Item type table will be made in the future. | 是 | 继承自 TH13 |
| 508 | dropArea | ff (w, h) | Sets caller's item drop area width to %1 and height to %2. | 是 | 继承自 TH13 |
| 509 | dropItems | — | Drops all items the caller has. Has no effect in spell practice. | 是 | 继承自 TH13 |
| 510 | dropMain | S (type) | Sets caller's main drop to %1. | 是 | 继承自 TH13 |
| 511 | lifeSet | S (hp) | Sets caller's current HP and max HP to %1. | 是 | 继承自 TH13 |
| 512 | setBoss | S (a) | If %1 is 0, activates boss mode and makes the caller the main boss. If %1 > 0, it makes the caller the secondary boss. If %1 is -1, ends boss mode. | 是 | 继承自 TH13 |
| 513 | timerReset | — | Resets boss timer. | 是 | 继承自 TH13 |
| 514 | setInterrupt | SSSm (slot, hp, time, sub) | Sets an interrupt on slot %1 (not sure how many slots there are) - once caller's hp reaches %2 or %3 frames have passed since this was called, caller will terminate all subs it's currently running and execute sub %4. | 是 | 继承自 TH13 |
| 515 | setInvuln | S (time) | Makes the caller completely invulnerable for %1 frames. | 是 | 继承自 TH13 |
| 516 | playSound | S (id) | Plays sound %1. Sound id table will be added in the future. | 是 | 继承自 TH13 |
| 517 | setScreenShake | SSS (time, startIntensity, endIntensity) | Activates screen shake for %1 frames. %2 is the starting intensity and %3 is the ending intensity. The larger the intensity, the more the screen shakes. | 是 | 继承自 TH13 |
| 518 | dialogRead | S (dialogueId) | Starts a dialogue, %1 is the ID of an entry in the .msg file. Apart from that, has the effect ins_525. | 是 | 继承自 TH13 |
| 519 | dialogWait | — | Waits until there are no dialogues active, or the running .msg script calls a certain instruction (which one?) | 否/待确认 | 继承自 TH13 |
| 520 | bossWait | — | Waits until there are no boss enemies. | 是 | 继承自 TH13 |
| 521 | setTimeout | Sm (slot, sub) | Sets a timeout interrupt on slot %1 - when the timer reaches 0, caller will terminate all subs it's currently running and execute sub %2. | 是 | 继承自 TH13 |
| 522 | spellEx | SSSm (id, time, unused, name) | Same as ins_537, but the difficulty number is NOT added to the id. | 是 | 继承自 TH13 |
| 523 | spellEnd | — | Ends currently active spellcard. | 是 | 继承自 TH13 |
| 524 | setChapter | S (a) | Some jank that's responsible for showing boss name and possibly other things. In LoLK, it also ends the current chapter and begins a new one. | 否/待确认 | 继承自 TH13 |
| 525 | enmKillAll | — | Kills all other enemies (unless they have a flag that prevents that set). | 是 | 继承自 TH13 |
| 526 | etProtectRange | f (r) | Makes bullets generated by the caller not spawn if they are in radius %1 around the player. | 是 | 继承自 TH13 |
| 527 | lifeMarker | SfS (slot, hp, c) | Sets a new life marker on slot %1, %2 determines where the marker will appear on the health bar (if %2=1000.0f and the enemy has 2000 hp, the marker will split the hp bar in half). %3 is an RGB value of unknown use (possibly leftover from earlier ECL versions) | 是 | 继承自 TH13 |
| 528 | spellUnused | SSSm (id, time, unused, name) | No difference from ins_522, unused. | 是 | 继承自 TH13 |
| 529 | rankF3 | ffff (var, a, b, c) | Sets %1 to %2 if rank is low, %3 if rank is average or %4 if rank is high. | 是 | 继承自 TH13 |
| 530 | rankF5 | ffffff (var, a, b, c, d, e) | Sets %1 to %2 if rank is very low, %3 if rank is low, %4 if rank is average, %5 if rank is high or %6 if rank is very high. | 是 | 继承自 TH13 |
| 531 | rankF2 | fff (var, a, b) | Sets %1 to %2 if rank is low or %3 if rank is high. | 是 | 继承自 TH13 |
| 532 | rankI3 | SSSS (var, a, b, c) | Sets %1 to %2 if rank is low, %3 if rank is average or %4 if rank is high. | 是 | 继承自 TH13 |
| 533 | rankI5 | SSSSSS (var, a, b, c, d, e) | Sets %1 to %2 if rank is very low, %3 if rank is low, %4 if rank is average, %5 if rank is high or %6 if rank is very high. | 是 | 继承自 TH13 |
| 534 | rankI2 | SSS (var, a, b) | Sets %1 to %2 if rank is low or %3 if rank is high. | 是 | 继承自 TH13 |
| 535 | diffI | SSSSS (var, E, N, H, L) | Sets %1 to one of values provided based on difficulty. | 是 | 继承自 TH13 |
| 536 | diffF | fffff (var, E, N, H, L) | Sets %1 to one of values provided based on difficulty. | 是 | 继承自 TH13 |
| 537 | spell | SSSm (id, time, unused, name) | Declares a spellcard with id %1 and name %4. The actual ID passed to the spell-creating function is `id + difficulty`, with easy=0, normal=1, hard=2, lunatic=3, ex=4, overdrive=5. <br>%2 determines how much time the spell circle takes to shrink (in frames), as well as how fast the spell bonus decreases. The exact formula is as follows: <br>[code] int factor = maxSCB >> 2; // maxSCB is hardcoded<br> currSCB -= (maxSCB - factor) / (%2 - 300);<br> currSCB -= currSCB % 10; [/code] <br>As you can guess, setting %2 to 300 causes a division by 0 error and crashes the game, while setting it to a value smaller than 300 causes the SCB to increase over time, instead of decreasing. %3 is unused. | 是 | 继承自 TH13 |
| 538 | spell2 | SSSm (id, time, unused, name) | Same as ins_537, except the ID used is `id - 1 + difficulty`. | 是 | 继承自 TH13 |
| 539 | spell3 | SSSm (id, time, unused, name) | Same as ins_537, except the ID used is `id - 2 + difficulty`. | 是 | 继承自 TH13 |
| 540 | stars | S (cnt) | Sets the amount of stars displayed in the top left corner. Stars might not appear at all if there is no boss active. | 是 | 继承自 TH13 |
| 541 | noHitboxDur | S (time) | Disables the hitbox (but not the hurtbox) for the given amount of frames. | 是 | 继承自 TH13 |
| 542 | spellTimeout | — | Makes the current spell a timeout spell (prevent spell bonus from decreasing, give capture bonus if timed out). | 是 | 继承自 TH13 |
| 543 | unknown543 | — | Unknown. | 否/待确认 | 继承自 TH13 |
| 544 | unknown544 | S (a) | Unknown, sets or clears some flag? | 否/待确认 | 继承自 TH13 |
| 545 | laserCancel | — | Cancels all lasers. | 是 | 继承自 TH13 |
| 546 | bombShield | SS (a, script) | Sets the bomb invulnerability flag (%1=1 set, %1=0 not set), the caller's ANM script will change to %2 when a bomb is active (how does it work with ANM slots exactly?) | 是 | 继承自 TH13 |
| 547 | gameSpeed | f (s) | Sets game speed to %1 of the normal speed. In ISC, enemies with flag 13 (dec=8192) set will ignore effects of this opcode. | 是 | 继承自 TH13 |
| 548 | diffWait | SSSS (e, n, h, l) | Same as ins_23, but the wait time is chosen from the given 4 based on the difficulty. | 是 | 继承自 TH13 |
| 549 | unknown549 | S (a) | Unknown. | 否/待确认 | 继承自 TH13 |
| 550 | unknown550 | S (a) | Unknown. | 否/待确认 | 继承自 TH13 |
| 551 | unknown551 | S (a) | Unknown. | 否/待确认 | 继承自 TH13 |
| 552 | zIndex | S (layers) | Increases layer of all ANM scripts used by the caller by %1. | 是 | 继承自 TH13 |
| 553 | hitSound | S (id) | Makes the caller play sound %1 when hit. Sound id table will be added in the future. | 是 | 继承自 TH13 |
| 554 | stageLogo | — | Shows the stage logo from an ANM of a hardcoded name. | 是 | 继承自 TH13 |
| 555 | enmAlive | SS (var, id) | Checks if enemy of var_-9914 == %2 is still alive, and sets %1 to 1 if it is or 0 if it isn't. | 是 | 继承自 TH13 |
| 556 | setDeath | m (sub) | Makes the caller execute sub %1 when the HP reaches 0. Keep in mind that the caller is already marked for deletion at the point when the sub actually executes, so if you put waiting there the sub will not execute fully (because the caller will be deleted) | 是 | 继承自 TH13 |
| 557 | fogTime | SSSff (time, mode, color, start, end) | Same as STD ins_9, that is, fogTime. Refer to [the STD instruction table](#s=modding/std-ins) for details. | 是 | 继承自 TH13 |
| 558 | flagMirror | S (state) | Literally the exact same instruction as ins_424. | 是 | 继承自 TH13 |
| 559 | enmLimit | S (limit) | Set the maximum number of enemies that can be present. New enemies will fail to spawn if the cap is reached. Default is 99999. | 是 | 继承自 TH13 |
| 560 | unknown560 | ff (r, s) | Unknown. | 否/待确认 | 继承自 TH13 |
| 561 | die | — | Makes the caller execute the sub set with ins_556. If there is no such sub set, the caller dies instead (exactly the same as if the player shot down the caller, that is, items are dropped, death sound plays etc) | 是 | 继承自 TH13 |
| 562 | dropItemsSp | — | Same as ins_509, but item spawning will not be blocked in spell practice. | 是 | 继承自 TH13 |
| 563 | unknown563 | S (flagState) | Sets [flag 12](#s=modding/flags) (decimal 4096), which controls whether the hitbox and hurtbox is a rectangle. If %1 is 1, collision is a rectangle. If %1 is 0, collision is elliptical. | 是 | 继承自 TH14 |
| 564 | hitboxRotate | f (angle) | Rotates the hitbox and hurtbox of the enemy (note: the hitbox rotation is really janky, but hurtbox rotates fine). Has no effect unless the enemy uses rectangular collision. | 是 | 继承自 TH14 |
| 565 | bombInvuln | f (red) | Sets caller's damage reduction when a bomb is active, 0.0f means no damage at all, 1.0f is full damage, negative values will make the enemy heal when you bomb. | 是 | 继承自 TH14 |
| 566 | unknown566 | () | Unknown (does it even exist?) | 否/待确认 | 继承自 TH14 |
| 567 | unknown567 | S (a) | Unknown. | 否/待确认 | 继承自 TH14 |
| 568 | spellMode | S (state) | Enables/disables spell card damage reduction, if %1 is 1 it's enabled, if it's 0 it's disabled. Can be used outside of spell cards. | 是 | 继承自 TH14 |
| 569 | unknown569 | S (a) | Unknown. | 否/待确认 | 本作 |
| 570 | unknown570 | — | Unknown. | 否/待确认 | 本作 |
| 571 | unknown571 | — | Unknown. | 否/待确认 | 本作 |

### TH15 指令：子弹创建与删除 / Bullet creation and deletion

| ID | 助记名 | 参数 | 说明 | 文档化 | 来源 |
| --- | --- | --- | --- | --- | --- |
| 600 | etNew | S (etId) | Resets bullet manager %1 to default properties. | 是 | 继承自 TH13 |
| 601 | etOn | S (etId) | Shoots bullet(s) using properties from bullet manager %1. | 是 | 继承自 TH13 |
| 602 | etSprite | SSS (etId, type, color) | Sets bullet type and color of bullet manager %1. Refer to [this image](https://cdn.discordapp.com/attachments/395767870119870466/570658618316161041/BULLET_IDS.png) made by Dai. Remarks:<br>- bullet types 35 and 36 spin<br>- type 30 pulses<br>- the difference between 16/37 is the spin direction (same case for 23 and 24) | 是 | 本作 |
| 603 | etOffset | Sff (etId, x, y) | Sets the relative offset of bullets spawned by bullet manager %1 to (%2,%3). | 是 | 继承自 TH13 |
| 604 | etAngle | Sff (etId, angle1, angle2) | Sets angle1 and angle2 of bullet manager %1. | 是 | 继承自 TH13 |
| 605 | etSpeed | Sff (etId, speed1, speed2) | Sets speed1 and speed2 of bullet manager %1. | 是 | 继承自 TH13 |
| 606 | etCount | SSS (etId, count1, count2) | Sets count1 and count2 of bullet manager %1. | 是 | 继承自 TH13 |
| 607 | etAim | SS (etId, aim) | Sets aim mode of bullet manager %1. | 是 | 继承自 TH13 |
| 608 | etSound | SSS (etId, sound1, sound2) | Sets sound1 and sound2 of bullet manager %1 (sound effect table is TODO). sound1 plays when the bullet manager fires a bullet, while sound2 plays when a bullet fired by the bullet manager does certain transformations. Set to -1 for no sound. | 是 | 继承自 TH13 |
| 609 | etExSet | SSSSSSff (etId, index, async, type, a, b, r, s) | Sets bullet transformation of bullet manager %1, transformation explanation will be added in the future. | 是 | 继承自 TH13 |
| 610 | etExSet2 | SSSSSSSSffff (etId, index, async, type, a, b, c, d, r, s, m, n) | Same as ins_609, but takes more arguments for certain transformation types. | 是 | 继承自 TH13 |
| 611 | etEx | SSSSSff (etId, async, type, a, b, r, s) | Adds bullet transformation to bullet manager %1, transformation explanation will be added in the future. | 是 | 继承自 TH13 |
| 612 | etEx2 | SSSSSSSffff (etId, async, type, a, b, c, d, r, s, m, n) | Same as ins_611, but takes more arguments for certain transformation types. | 是 | 继承自 TH13 |
| 613 | etClearAll | — | Clears all bullets. | 是 | 继承自 TH13 |
| 614 | etCopy | SS (etIdDest, etIdSrc) | Copies everything from bullet manager %2 into bullet manager %1. Warning: this instruction is partially broken and does NOT copy the index next ins_611/ins_612 transformations will be added at. | 是 | 继承自 TH13 |
| 615 | etCancel | f (r) | Clears all bullets in a circle of radius %1 around the caller, and turns them into cancel items. | 是 | 继承自 TH13 |
| 616 | etClear | f (r) | Clears all bullets in a circle of radius %1 around the caller without turning them into cancel items. | 是 | 继承自 TH13 |
| 617 | etSpeedR3 | Sffffff (etId, spd1l, spd1m, spd1h, spd2l, spd2m, spd2h) | Sets speed1 and speed2 of bullet manager %1 to two of the values provided, based on ingame rank (l=low, m=medium, h=high) | 是 | 继承自 TH13 |
| 618 | etSpeedR5 | Sffffffffff (etId, spd1l, spd1ml, spd1m, spd1mh, spd1h, spd2l, spd2ml, spd2m, spd2mh, spd2h) | Sets speed1 and speed2 of bullet manager %1 to two of the values provided, based on ingame rank (l=low, ml=medium-low, m=medium, mh=medium-high, h=high) | 是 | 继承自 TH13 |
| 619 | etSpeedR2 | Sffff (etId, spd1l, spd1h, spd2l, spd2h) | Sets speed1 and speed2 of bullet manager %1 to two of the values provided, based on ingame rank (l=low, h=high) | 是 | 继承自 TH13 |
| 620 | etCountR3 | SSSSSSS (etId, cnt1l, cnt1m, cnt1h, cnt2l, cnt2m, cnt2h) | Sets count1 and count2 of bullet manager %1 to two of the values provided, based on ingame rank (l=low, m=medium, h=high) | 是 | 继承自 TH13 |
| 621 | etCountR5 | SSSSSSSSSSS (etId, cnt1l, cnt1ml, cnt1m, cnt1mh, cnt1h, cnt2l, cnt2ml, cnt2m, cnt2mh, cnt2h) | Sets count1 and count2 of bullet manager %1 to two of the values provided, based on ingame rank (l=low, ml=medium-low, m=medium, mh=medium-high, h=high) | 是 | 继承自 TH13 |
| 622 | etCountR2 | SSSSS (etId, cnt1l, cnt1h, cnt2l, cnt2h) | Sets count1 and count2 of bullet manager %1 to two of the values provided, based on ingame rank (l=low, h=high) | 是 | 继承自 TH13 |
| 623 | angleToPlayer | fff (var, x, y) | Gets angle to the player from coordinates (%2,%3) and stores it in %1. | 是 | 继承自 TH13 |
| 624 | etSpeedD | Sffffffff (etId, spd1e, spd1n, spd1h, spd1l, spd2e, spd2n, spd2h, spd2l) | Sets speed1 and speed2 of bullet manager %1 to 2 of the values provided, based on the difficulty (e=easy, n=normal, h=hard, l=lunatic) | 是 | 继承自 TH13 |
| 625 | etCountD | SSSSSSSSS (etId, cnt1e, cnt1n, cnt1h, cnt1l, cnt2e, cnt2n, cnt2h, cnt2l) | Sets count1 and count2 of bullet manager %1 to 2 of the values provided, based on the difficulty (e=easy, n=normal, h=hard, l=lunatic) | 是 | 继承自 TH13 |
| 626 | etOffsetRad | Sff (etId, angle, radius) | Sets the relative offset of bullets spawned by bullet manager %1 to (cos(%2)\*%3,sin(%2)\*%3). Stacks with ins_603. | 是 | 继承自 TH13 |
| 627 | etDist | Sf (etId, dist) | Sets distance of bullets spawned by bullet manager %1 to %2 (that is, when a bullet is spawned it moves by %2 using its current angle). | 是 | 继承自 TH13 |
| 628 | etOffsetAbs | Sff (etId, x, y) | Sets the absolute offset of bullets spawned by bullet manager %1 to (%2,%3). | 是 | 继承自 TH13 |
| 629 | fog | fS (r, color) | Sets caller's fog's radius to %1 and color to %2 (RGB value in reverse order). This resets the fog completely, that is, every time it's called the fog spawn animation plays. | 是 | 继承自 TH13 |
| 630 | callSTD | S (switch) | Sets execution pointer of the STD script to where STD ins_16(%1) is (%1 must be the same), basically same concept as ins_317. | 是 | 继承自 TH13 |
| 631 | lifeHide | S (time) | Hides boss lifebar for %1 frames. | 是 | 继承自 TH13 |
| 632 | funcSet | S (id) | Sets a function that the game will execute every frame from a set of hardcoded functions that differs between games. | 是 | 继承自 TH13 |
| 633 | flagExtDmg | S (state) | Sets the external damage flag to %1. Caller probably needs to be the main boss for this to work - with this flag set, the caller gets damaged by the value stored in var_-9940 every frame, and then resets the value. This allows other enemies to damage the boss by incrementing the aforementioned variable, used in LoLK by Sagume (and also happens to be the main cause of the Sagume skip glitch) | 是 | 继承自 TH13 |
| 634 | setHitboxFunc | S (id) | Make the caller use a special function for determining collision with the player. TODO: create a list of functions and their IDs | 是 | 继承自 TH13 |
| 635 | etCancel2 | f (r) | Same as ins_615, but doesn't clear bullets with bomb invulnerability. | 是 | 继承自 TH13 |
| 636 | etClear2 | f (r) | Same as ins_616, but doesn't clear bullets with bomb invulnerability. | 是 | 继承自 TH13 |
| 637 | funcCall | S (id) | Same as ins_632, except the function is called just once instead of every frame. | 是 | 继承自 TH13 |
| 638 | scoreAdd | S (n) | Adds %1 to score (or subtracts if %1 is negative). There is no lower boundary check, so if this causes score to go below 0, an underflow happens. | 是 | 继承自 TH13 |
| 639 | funcSet2 | S (id) | Same as ins_632, except it sets an unknown flag to 1 (ins_632 sets it to 0) | 是 | 继承自 TH13 |
| 640 | etExSub | SSm (etId, index, s) | Sets the string parameter of transform on index %2 in bullet manager %1 to %3, transformations will be explained separately later. | 是 | 继承自 TH13 |
| 641 | etExSubtract | S (etId) | Subtracts 1 from the index used by ins_611 and ins_612, unless it's already 0. This basically changes where the next transformation will be appended. | 是 | 继承自 TH14 |

### TH15 指令：激光创建 / Laser creation

| ID | 助记名 | 参数 | 说明 | 文档化 | 来源 |
| --- | --- | --- | --- | --- | --- |
| 700 | laserNew | Sffff (etId, init_length, final_length, unknown_arg_3, width) | Sets basic parameters of the laser. %4 has something to do with the length of straight line lasers (investigation needed), but doesn't do anything for other laser types. For curvy lasers, the only used argument is %5, and length is specified with ins_701 instead. | 是 | 继承自 TH13 |
| 701 | laserTiming | SSSSSS (edId, startup_time, expand_time, duration, shrink_time, init_flags) | Sets timing for infinite lasers. %6 sets the initial flags for a laser, but these flags are unknown at the moment. For curvy lasers, the %2 argument instead specifies the length of the laser. | 是 | 继承自 TH13 |
| 702 | laserOn | S (edId) | Shoots a straight line laser. | 是 | 继承自 TH13 |
| 703 | laserStOn | SS (etId, laser_id) | Shoots an infinite laser. %2 is a number that's used to identify this particular laser instance, so that it can be referred to in other instructions. | 是 | 继承自 TH13 |
| 704 | laserOffset | Sff (laser_id, x, y) | Sets the position of the infinite laser pointed to by %1. | 是 | 继承自 TH13 |
| 705 | laserTrajectory | Sff (laser_id, x_speed, y_speed) | Sets the offset velocity of the infinite laser pointed to by %1. The laser's position will change by %2 and %3 every frame. | 是 | 继承自 TH13 |
| 706 | laserStLength | Sf (laser_id, speed) | Sets the speed of the infinite laser pointed to by %1. | 是 | 继承自 TH13 |
| 707 | laserStWidth | Sf (laser_id, width) | Sets the width of the infinite laser pointed to by %1. | 是 | 继承自 TH13 |
| 708 | laserStAngle | Sf (laser_id, angle) | Sets the angle of the infinite laser pointed to by %1. | 是 | 继承自 TH13 |
| 709 | laserStRotation | Sf (laser_id, angular_vel) | Sets the angular velocity of the infinite laser pointed to by %1. The laser's angle will change by %2 every frame. | 是 | 继承自 TH13 |
| 710 | laserStEnd | S (laser_id) | Clears the laser pointed to by %1. | 是 | 继承自 TH13 |
| 711 | laserCuOn | S (etId) | Shoots a curvy laser. | 是 | 继承自 TH13 |
| 712 | etCancelRect | ff (w, h) | Cancels all bullets in rectangle of width %1 and height %2. The area is affected by rotation set by ins_564. | 是 | 继承自 TH14 |
| 713 | unknown713 | SS (etId, laser_id) | Shoots a laser 'beam', a laser type used by marisa in GFW. Broken since this laser type does not exist outside of GFW. | 是 | 继承自 TH13 |
| 714 | unknown714 | SS (laser_id, unknown) | Does something with a laser beam pointed to by %1. Broken since this laser type does not exist outside of GFW. | 是 | 继承自 TH13 |

### TH15 指令：敌机交互 / Enemy interaction

| ID | 助记名 | 参数 | 说明 | 文档化 | 来源 |
| --- | --- | --- | --- | --- | --- |
| 800 | enmCall | Sm (id, sub) | Makes enemy with var_-9914 == %1 stop all subs it's running and execute sub %2 (works like an interrupt). This will NOT make the enemy execute the sub right as this instruction is called, the new sub will be executed when the game handles the given enemy, which might be later on the same frame or on the next frame. Using this to make the caller interrupt itself can make the game explode. | 是 | 继承自 TH13 |
| 801 | enmPos | ffS (varX, varY, id) | Stores coordinates of enemy with var_-9914 == %3 in (%1,%2). | 是 | 继承自 TH13 |
| 802 | broadcastInterrupt | S (slot) | For all existing bosses, trigger the interrupt set by ins_514 on slot %1. Does not change the HP to the one set in ins_514. | 是 | 继承自 TH13 |

### TH15 指令：调试 / Debug

| ID | 助记名 | 参数 | 说明 | 文档化 | 来源 |
| --- | --- | --- | --- | --- | --- |
| 900 | debug900 | — | 未在 Priw8 表中记录/待确认 | 否/待确认 | — |
| 901 | debug901 | — | 未在 Priw8 表中记录/待确认 | 否/待确认 | — |
| 902 | debug902 | — | 未在 Priw8 表中记录/待确认 | 否/待确认 | — |

### TH15 指令：游戏特有 / Game specific

| ID | 助记名 | 参数 | 说明 | 文档化 | 来源 |
| --- | --- | --- | --- | --- | --- |
| 1000 | spec0 | — | 未在 Priw8 表中记录/待确认 | 否/待确认 | — |
| 1001 | spec1 | — | 未在 Priw8 表中记录/待确认 | 否/待确认 | — |
| 1002 | spec2 | — | 未在 Priw8 表中记录/待确认 | 否/待确认 | — |
| 1003 | spec3 | — | 未在 Priw8 表中记录/待确认 | 否/待确认 | — |

### TH15 变量

| ID | 名称 | 类型 | 访问 | 作用域 | 说明 | 文档化 | 来源 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| -10000 | RAND | int | 只读 | global/全局 | Random integer, very large range. | 是 | 继承自 TH10 |
| -9999.0f | RANDF | float | 只读 | global/全局 | Random float from 0.0f to 1.0f. | 是 | 继承自 TH10 |
| -9998.0f | RANDRAD | float | 只读 | global/全局 | Random float from -pi to pi. | 是 | 继承自 TH10 |
| -9997.0f | FINAL_X | float | 只读 | local/敌机局部 | Final X position of the enemy. | 是 | 继承自 TH10 |
| -9996.0f | FINAL_Y | float | 只读 | local/敌机局部 | Final Y position of the enemy. | 是 | 继承自 TH10 |
| -9995.0f | ABS_X | float | 只读 | local/敌机局部 | Absolute X position of the enemy. | 是 | 继承自 TH10 |
| -9994.0f | ABS_Y | float | 只读 | local/敌机局部 | Absolute Y position of the enemy. | 是 | 继承自 TH10 |
| -9993.0f | REL_X | float | 只读 | local/敌机局部 | Relative X position of the enemy. | 是 | 继承自 TH10 |
| -9992.0f | REL_Y | float | 只读 | local/敌机局部 | Relative Y position of the enemy. | 是 | 继承自 TH10 |
| -9991.0f | PLAYER_X | float | 只读 | global/全局 | Player's X position. | 是 | 继承自 TH10 |
| -9990.0f | PLAYER_Y | float | 只读 | global/全局 | Player's Y position. | 是 | 继承自 TH10 |
| -9989.0f | ANGLE_PLAYER | float | 只读 | local/敌机局部 | Angle from the enemy to the player. | 是 | 继承自 TH10 |
| -9988 | TIME | int | 只读 | local/敌机局部 | Time elapsed since the enemy spawned, in frames. | 是 | 继承自 TH10 |
| -9987.0f | RANDF2 | float | 只读 | global/全局 | Random float from -1.0f to 1.0f. | 是 | 继承自 TH10 |
| -9986 | TIMEOUT | int | 只读 | global/全局 | Set to 1 by the engine when a timeout occurs. | 是 | 继承自 TH10 |
| -9985 | I0 | int | 读写 | local/敌机局部 | Local integer variable, inherited by spawned enemies. | 是 | 继承自 TH10 |
| -9984 | I1 | int | 读写 | local/敌机局部 | Local integer variable, inherited by spawned enemies. | 是 | 继承自 TH10 |
| -9983 | I2 | int | 读写 | local/敌机局部 | Local integer variable, inherited by spawned enemies. | 是 | 继承自 TH10 |
| -9982 | I3 | int | 读写 | local/敌机局部 | Local integer variable, inherited by spawned enemies. | 是 | 继承自 TH10 |
| -9981.0f | F0 | float | 读写 | local/敌机局部 | Local float variable, inherited by spawned enemies. | 是 | 继承自 TH10 |
| -9980.0f | F1 | float | 读写 | local/敌机局部 | Local float variable, inherited by spawned enemies. | 是 | 继承自 TH10 |
| -9979.0f | F2 | float | 读写 | local/敌机局部 | Local float variable, inherited by spawned enemies. | 是 | 继承自 TH10 |
| -9978.0f | F3 | float | 读写 | local/敌机局部 | Local float variable, inherited by spawned enemies. | 是 | 继承自 TH10 |
| -9977.0f | FINAL_X2 | float | 只读 | local/敌机局部 | Same as var_-9997. | 是 | 继承自 TH10 |
| -9976.0f | FINAL_Y2 | float | 只读 | local/敌机局部 | Same as var_-9996. | 是 | 继承自 TH10 |
| -9975.0f | ABS_X2 | float | 只读 | local/敌机局部 | Same as var_-9995. | 是 | 继承自 TH10 |
| -9974.0f | ABS_Y2 | float | 只读 | local/敌机局部 | Same as var_-9994. | 是 | 继承自 TH10 |
| -9973.0f | REL_X2 | float | 只读 | local/敌机局部 | Same as var_-9993. | 是 | 继承自 TH10 |
| -9972.0f | REL_Y2 | float | 只读 | local/敌机局部 | Same as var_-9992. | 是 | 继承自 TH10 |
| -9971.0f | ABS_ANGLE | float | 只读 | local/敌机局部 | Angle of enemy's absolute movement. | 是 | 继承自 TH10 |
| -9970.0f | REL_ANGLE | float | 只读 | local/敌机局部 | Angle of enemy's relative movement. | 是 | 继承自 TH10 |
| -9969.0f | ABS_SPEED | float | 只读 | local/敌机局部 | Speed of enemy's absolute movement. | 是 | 继承自 TH10 |
| -9968.0f | REL_SPEED | float | 只读 | local/敌机局部 | Speed of enemy's relative movement. | 是 | 继承自 TH10 |
| -9967.0f | ABS_ORIGIN_DIST | float | 只读 | local/敌机局部 | Distance from the origin of enemy's absolute circular movement (radius of the circle). | 是 | 继承自 TH10 |
| -9966.0f | REL_ORIGIN_DIST | float | 只读 | local/敌机局部 | Distance from the origin of enemy's relative circular movement (radius of the circle). | 是 | 继承自 TH10 |
| -9965.0f | PLAYER_X2 | float | 只读 | global/全局 | Same as var_-9991. | 是 | 继承自 TH10 |
| -9964.0f | PLAYER_Y2 | float | 只读 | global/全局 | Same as var_-9990. | 是 | 继承自 TH10 |
| -9963.0f | BOSS_X | float | 只读 | global/全局 | Final X position of the boss. | 是 | 继承自 TH10 |
| -9962.0f | BOSS_Y | float | 只读 | global/全局 | Final Y position of the boss. | 是 | 继承自 TH10 |
| -9961 | ANM_ID | int | 只读 | local/敌机局部 | Is the current script on anm slot 0 of the enemy. | 是 | 继承自 TH10 |
| -9960 | RANK | int | 只读 | global/全局 | Numeric value of rank, ranging from -1024 to 1024. Increases over time and decreases when player bombs/dies etc. | 是 | 继承自 TH10 |
| -9959 | DIFF | int | 只读 | global/全局 | Difficulty (E=0, N=1, H=2, L=3, EX=4, O=5) | 是 | 继承自 TH10 |
| -9958.0f | FINAL_ANGLE | float | 只读 | local/敌机局部 | Final angle of enemy's movement. | 是 | 继承自 TH10 |
| -9957 | TRUE | int | 只读 | global/全局 | Always returns 1. | 是 | 继承自 TH10 |
| -9956.0f | ABS_ANGLE_PLAYER | float | 只读 | local/敌机局部 | Angle to the player from enemy's absolute position. | 是 | 继承自 TH10 |
| -9955.0f | REL_ANGLE_PLAYER | float | 只读 | local/敌机局部 | Angle to the player from enemy's relative position. | 是 | 继承自 TH10 |
| -9954 | LIFE | int | 只读 | local/敌机局部 | Enemy's current HP. | 是 | 继承自 TH10 |
| -9953 | EASY | int | 只读 | global/全局 | Set to 1 if difficulty is easy, otherwise it's 0. | 是 | 继承自 TH10 |
| -9952 | NORMAL | int | 只读 | global/全局 | Set to 1 if difficulty is normal, otherwise it's 0. | 是 | 继承自 TH10 |
| -9951 | HARD | int | 只读 | global/全局 | Set to 1 if difficulty is hard, otherwise it's 0. | 是 | 继承自 TH10 |
| -9950 | LUNATIC | int | 只读 | global/全局 | Set to 1 if difficulty is lunatic, otherwise it's 0. | 是 | 继承自 TH10 |
| -9949 | MISS_COUNT | int | 读写 | global/全局 | Increased by 1 every time the player dies. | 是 | 继承自 TH11 |
| -9948 | BOMB_COUNT | int | 读写 | global/全局 | Increased by 1 every time the player bombs. | 是 | 继承自 TH11 |
| -9947 | CAPTURE | int | 读写 | global/全局 | Set to 0 when the player dies, bombs, or uses a game-specific mechanic that "fails" a spell. | 是 | 继承自 TH11 |
| -9946 | ENM_CNT_REAL | int | 只读 | global/全局 | Amount of enemies alive (including main and MapleEnemy). | 是 | 继承自 TH11 |
| -9945 | SHOTTYPE | int | 只读 | global/全局 | Numeric value that represents player's shottype, the first shottype is 0. | 是 | 继承自 TH11 |
| -9944.0f | DIST_PLAYER | float | 只读 | local/敌机局部 | Distance from the enemy to the player. | 是 | 继承自 TH11 |
| -9943 | BI0 | int | 读写 | local/敌机局部 | Is the same as the I0 variable of boss 0. | 是 | 继承自 TH11 |
| -9942 | BI1 | int | 读写 | local/敌机局部 | Is the same as the I1 variable of boss 0. | 是 | 继承自 TH11 |
| -9941 | BI2 | int | 读写 | local/敌机局部 | Is the same as the I2 variable of boss 0. | 是 | 继承自 TH11 |
| -9940 | BI3 | int | 读写 | local/敌机局部 | Is the same as the I3 variable of boss 0. | 是 | 继承自 TH11 |
| -9939.0f | BF0 | float | 读写 | local/敌机局部 | Is the same as the F0 variable of boss 0. | 是 | 继承自 TH11 |
| -9938.0f | BF1 | float | 读写 | local/敌机局部 | Is the same as the F1 variable of boss 0. | 是 | 继承自 TH11 |
| -9937.0f | BF2 | float | 读写 | local/敌机局部 | Is the same as the F2 variable of boss 0. | 是 | 继承自 TH11 |
| -9936.0f | BF3 | float | 读写 | local/敌机局部 | Is the same as the F3 variable of boss 0. | 是 | 继承自 TH11 |
| -9935.0f | F4 | float | 读写 | local/敌机局部 | Local float variable inherited by spawned enemies, just like F0-F3 and I0-I3. | 是 | 继承自 TH11 |
| -9934.0f | F5 | float | 读写 | local/敌机局部 | Local float variable inherited by spawned enemies, just like F0-F3 and I0-I3. | 是 | 继承自 TH11 |
| -9933.0f | F6 | float | 读写 | local/敌机局部 | Local float variable inherited by spawned enemies, just like F0-F3 and I0-I3. | 是 | 继承自 TH11 |
| -9932.0f | F7 | float | 读写 | local/敌机局部 | Local float variable inherited by spawned enemies, just like F0-F3 and I0-I3. | 是 | 继承自 TH11 |
| -9931 | LAST_ENM_ID | int | 只读 | global/全局 | ID of the last spawned enemy. | 是 | 继承自 TH12 |
| -9930 | POWER | int | 只读 | global/全局 | Player's power (4.00 => 400) | 是 | 继承自 TH12 |
| -9929 | DS1 | int | 只读 | global/全局 | Used in Double Spoiler, unknown. | 否/待确认 | 继承自 TH12.5 |
| -9928 | DS2 | int | 只读 | global/全局 | Used in Double Spoiler, unknown. | 否/待确认 | 继承自 TH12.5 |
| -9927 | DS3 | int | 只读 | global/全局 | Used in Double Spoiler, unknown. | 否/待确认 | 继承自 TH12.5 |
| -9926 | GI0 | int | 读写 | global/全局 | Global integer variable. | 是 | 继承自 TH12.5 |
| -9925 | GI1 | int | 读写 | global/全局 | Global integer variable. | 是 | 继承自 TH12.5 |
| -9924 | GI2 | int | 读写 | global/全局 | Global integer variable. | 是 | 继承自 TH12.5 |
| -9923 | GI3 | int | 读写 | global/全局 | Global integer variable. | 是 | 继承自 TH12.5 |
| -9922.0f | GF0 | float | 读写 | global/全局 | Global float variable. | 是 | 继承自 TH12.5 |
| -9921.0f | GF1 | float | 读写 | global/全局 | Global float variable. | 是 | 继承自 TH12.5 |
| -9920.0f | GF2 | float | 读写 | global/全局 | Global float variable. | 是 | 继承自 TH12.5 |
| -9919.0f | GF3 | float | 读写 | global/全局 | Global float variable. | 是 | 继承自 TH12.5 |
| -9918.0f | GF4 | float | 读写 | global/全局 | Global float variable. | 是 | 继承自 TH12.5 |
| -9917.0f | GF5 | float | 读写 | global/全局 | Global float variable. | 是 | 继承自 TH12.5 |
| -9916.0f | GF6 | float | 读写 | global/全局 | Global float variable. | 是 | 继承自 TH12.5 |
| -9915.0f | GF7 | float | 读写 | global/全局 | Global float variable. | 是 | 继承自 TH12.5 |
| -9914 | ID | int | 只读 | local/敌机局部 | ID of the enemy. | 是 | 继承自 TH12.5 |
| -9913 | DS_PHOTOCOUNT | int | 只读 | global/全局 | Used in Double Spoiler, amount of photos taken. | 是 | 继承自 TH12.5 |
| -9912 | DS4 | int | 只读 | global/全局 | Used in Double Spoiler, unknown. | 否/待确认 | 继承自 TH12.5 |
| -9911.0f | ANGLE_BOSS | float | 只读 | global/全局 | Angle at which the boss moves. | 是 | 继承自 TH12.5 |
| -9910.0f | SPEED_BOSS | float | 只读 | global/全局 | Speed at which the boss moves. | 是 | 继承自 TH12.5 |
| -9909 | UNKNOWN9 | int | 只读 | local/敌机局部 | Enemy ID of the parent enemy. | 是 | 继承自 TH12.8 |
| -9908 | ENM_CNT | int | 只读 | global/全局 | Amount of killable enemies alive (that is, doesn't include hitboxless/intangible enemies etc). | 是 | 继承自 TH13 |
| -9907 | SPELL_ID | int | 只读 | global/全局 | Spellcard ID, used by spell practice. Unknown meaning in LoLK. | 是 | 继承自 TH13 |
| -9906 | MIRROR | int | 只读 | local/敌机局部 | Mirror flag state, either 0 or 1. TODO: verify game version | 否/待确认 | 本作 |
| -9905 | [-9905] | int | 只读 | global/全局 | Value set by ins_524. | 是 | 本作 |
| -9904 | MISS_COUNT_GLOBAL | int | 只读 | global/全局 | Amount of misses throughout the entire game. | 是 | 本作 |

## TH16 东方天空璋

- 体系：第四世代
- 指令：普通指令 321 条；已说明 262/321。主要分组：系统/流程/栈/算术 / System；敌机创建与 ANM 管理 / Enemy creation and ANM script management；移动管理 / Movement management；敌机属性与杂项 / Enemy property management and other miscellaneous things；子弹创建与删除 / Bullet creation and deletion；激光创建 / Laser creation；敌机交互 / Enemy interaction；调试 / Debug；游戏特有 / Game specific。
- 变量：变量范围 -10000..-9903；本文列出有说明/命名记录的 98 条，未列空洞/未知项。

### TH16 指令：系统/流程/栈/算术 / System

| ID | 助记名 | 参数 | 说明 | 文档化 | 来源 |
| --- | --- | --- | --- | --- | --- |
| 0 | nop | — | Empty instruction, doesn't do anything. | 是 | 继承自 TH13 |
| 1 | delete | — | Returns to the top of current call stack. | 是 | 继承自 TH13 |
| 2 | ins_2 | — |  | 否/待确认 | 继承自 TH-1 |
| 3 | ins_3 | — |  | 否/待确认 | 继承自 TH-1 |
| 4 | ins_4 | — |  | 否/待确认 | 继承自 TH-1 |
| 5 | ins_5 | — |  | 否/待确认 | 继承自 TH-1 |
| 6 | ins_6 | — |  | 否/待确认 | 继承自 TH-1 |
| 7 | ins_7 | — |  | 否/待确认 | 继承自 TH-1 |
| 8 | ins_8 | — |  | 否/待确认 | 继承自 TH-1 |
| 9 | ins_9 | — |  | 否/待确认 | 继承自 TH-1 |
| 10 | ret | — | Returns from the current sub. | 是 | 继承自 TH13 |
| 11 | call | m (sub) | Calls a given sub. Can take additional parameters to pass as arguments to the sub. [c=orange]Direct Usage obsolete. Use `@subName()` syntax instead. | 是 | 继承自 TH13 |
| 12 | jmp | o (target) | Unconditionally jumps to the label %1. [c=orange]Direct usage obsolete. Use `goto label` syntax instead. | 是 | 继承自 TH13 |
| 13 | jmpEq | o (target) | Pops a number from the stack and if it evaluates to false (in this context, 0), jumps to label %1. [c=orange]Direct usage obsolete. Use if/unless statement instead. | 是 | 继承自 TH13 |
| 14 | jmpNeq | o (target) | Pops a number from the stack and if it evaluates to true (in this context, anything non-0), jumps to label %1. [c=orange]Direct usage obsolete. Use if/unless statement instead. | 是 | 继承自 TH13 |
| 15 | callAsync | m (sub) | Asynchronously calls a given sub. Can take additional parameters to pass as arguments to the sub. [c=orange]Direct usage obsolete. Use `@subName() async` syntax instead. | 是 | 继承自 TH13 |
| 16 | callAsyncId | mS (sub, id) | Asynchronously calls a given sub and assigns it ID %2. Can take additional parameters to pass as arguments to the sub. [c=orange]Direct usage obsolete, use, `@subName() async id` syntax instead. | 是 | 继承自 TH13 |
| 17 | killAsync | S (id) | Ends most recently called sub that has ID %1 (same ID as in ins_16). If no sub with the given ID is found, nothing happens. Using ID -1 can lead to various unexpected results, ranging from deleting the enemy to freezing the game. | 是 | 继承自 TH13 |
| 18 | ins_18 | S (id) | Let `vm` be the most recent async sub running with ID %1: this ins sets `vm[0x000011E4]` to 1. | 否/待确认 | 继承自 TH13 |
| 19 | ins_19 | S (id) | Let `vm` be the most recent async sub running with ID %1: this ins sets `vm[0x000011E4]` to 0. | 否/待确认 | 继承自 TH13 |
| 20 | ins_20 | SS (id, b) | Let `vm` be the most recent async sub running with ID %1: this ins sets `vm[0x0000101C]` to %2. | 否/待确认 | 继承自 TH13 |
| 21 | killAllAsync | — | Ends all running async subs. Calling this in an async sub can lead to unexpected results, such as crashing the game. | 是 | 继承自 TH13 |
| 22 | debug22 | Sm (a, b) | Debug instruction, code does not exist in the release builds of the game. Most likely used to call sub %2 if some variable set in a debug menu is equal to %1. | 是 | 继承自 TH13 |
| 23 | wait | S (time) | Stops sub execution for %1 frames. | 是 | 继承自 TH13 |
| 24 | waitf | f (time) | ins_23, but time is given as a float instead of an int. Subframes do actually exist and affect ins_547. | 是 | 继承自 TH13 |
| 25 | ins_25 | — |  | 否/待确认 | 继承自 TH-1 |
| 26 | ins_26 | — |  | 否/待确认 | 继承自 TH-1 |
| 27 | unknown27 | — |  | 否/待确认 | 继承自 TH-1 |
| 28 | ins_28 | — |  | 否/待确认 | 继承自 TH-1 |
| 29 | ins_29 | — |  | 否/待确认 | 继承自 TH-1 |
| 30 | unknown30 | m (formatString) | Some sort of `printf` debug instruction, which can take additional float/int arguments after %1. Its code does not exist in the release builds. | 是 | 继承自 TH13 |
| 31 | unknown31 | — |  | 否/待确认 | 继承自 TH-1 |
| 32 | ins_32 | — |  | 否/待确认 | 继承自 TH-1 |
| 33 | ins_33 | — |  | 否/待确认 | 继承自 TH-1 |
| 34 | ins_34 | — |  | 否/待确认 | 继承自 TH-1 |
| 35 | ins_35 | — |  | 否/待确认 | 继承自 TH-1 |
| 36 | ins_36 | — |  | 否/待确认 | 继承自 TH-1 |
| 37 | ins_37 | — |  | 否/待确认 | 继承自 TH-1 |
| 38 | ins_38 | — |  | 否/待确认 | 继承自 TH-1 |
| 39 | ins_39 | — |  | 否/待确认 | 继承自 TH-1 |
| 40 | stackAlloc | S (size) | Increases the ECL stack pointer by %1 bytes (probably), to make space for sub variables. [c=orange]Obsolete, thecl generates this instruction automatically. | 是 | 继承自 TH13 |
| 41 | ins_41 | — |  | 否/待确认 | 继承自 TH-1 |
| 42 | pushi | S (num) | Pushes an integer to the ECL stack. [c=orange]Obsolete, push values to stack by writing unassigned expressions instead. | 是 | 继承自 TH13 |
| 43 | seti | S (var) | Pops an integer from the stack into variable %1. [c=orange]Obsolete, use assignment syntax instead. | 是 | 继承自 TH13 |
| 44 | pushf | f (num) | Pushes a float to the ECL stack. [c=orange]Obsolete, push values to stack by writing unassigned expressions instead. | 是 | 继承自 TH13 |
| 45 | setf | f (var) | Pops a float from the stack into variable %1. [c=orange]Obsolete, use assignment syntax instead. | 是 | 继承自 TH13 |
| 46 | ins_46 | — |  | 否/待确认 | 继承自 TH-1 |
| 47 | ins_47 | — |  | 否/待确认 | 继承自 TH-1 |
| 48 | ins_48 | — |  | 否/待确认 | 继承自 TH-1 |
| 49 | ins_49 | — |  | 否/待确认 | 继承自 TH-1 |
| 50 | addi | — | Sums integers on the stack. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 51 | addf | — | Sums floats on the stack. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 52 | subi | — | Subtracts integers on the stack. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 53 | subf | — | Subtracts floats on the stack. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 54 | muli | — | Multiplies integers on the stack. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 55 | mulf | — | Multiplies floats on the stack. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 56 | divi | — | Divides integers on the stack. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 57 | divf | — | Divides floats on the stack. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 58 | modi | — | Modulo operation on integers on the stack. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 59 | eqi | — | Stack integer `==` comparison. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 60 | eqf | — | Stack float `==` comparison. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 61 | neqi | — | Stack integer `!=` comparison. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 62 | neqf | — | Stack float `!=` comparison. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 63 | lessi | — | Stack integer `<` comparison. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 64 | lessf | — | Stack float `<` comparison. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 65 | leqi | — | Stack integer `<=` comparison. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 66 | leqf | — | Stack float `<=` comparison. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 67 | greateri | — | Stack integer `>` comparison. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 68 | greaterf | — | Stack float `>` comparison. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 69 | geqi | — | Stack integer `>=` comparison. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 70 | geqf | — | Stack float `>=` comparison. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 71 | noti | — | Stack integer NOT operation (e.g. !1). [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 72 | notf | — | Stack float NOT operation (e.g. !1.0f). [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 73 | or | — | Logical OR operation on the stack. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 74 | and | — | Logical AND operation on the stack. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 75 | xor | — | Bitwise XOR operation on integers on the stack. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 76 | bit_or | — | Bitwise OR operation on integers on the stack. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 77 | bit_and | — | Bitwise AND operation on integers on the stack. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 78 | deci | S (var) | Pushes variable %1 to the stack and then decrements it. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 79 | stackSin | — | sin operation on a float on the stack. [c=orange]Obsolete, use `sin(floatVal)` instead. | 是 | 继承自 TH13 |
| 80 | stackCos | — | cos operation on a float on the stack. [c=orange]Obsolete, use `cos(floatVal)` instead. | 是 | 继承自 TH13 |
| 81 | circlePos | ffff (varX, varY, ang, radius) | Performs following operation: [code]%1 = cos(%3)*%4;<br>%2 = sin(%3)*%4;[/code] | 是 | 继承自 TH13 |
| 82 | validRad | f (var) | Normalizes angle in %1. | 是 | 继承自 TH13 |
| 83 | negi | — | Negates an integer on the stack. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 84 | negf | — | Negates a float on the stack. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 85 | squareSum | fff (var, x, y) | Performs following operation: [code]%1 = %2*%2 + %3*%3;[/code] | 是 | 继承自 TH13 |
| 86 | squareSumRoot | fff (var, x, y) | Performs following operation: [code]%1 = sqrt(%2*%2 + %3*%3);[/code] | 是 | 继承自 TH13 |
| 87 | getAngle | fffff (var, x1, y1, x2, y2) | Calculates angle from (%2,%3) to (%4,%5) and stores it in %1. | 是 | 继承自 TH13 |
| 88 | stackSqrt | — | square root operation on a float on the stack. [c=orange]Obsolete, use `sqrt(floatVal)` instead. | 是 | 继承自 TH13 |
| 89 | linearFunc | fff (var, a, x) | Performs following operation: [code]%1 = %2*%3;[/code]<br>(what's the point of making this an instruction, ZUN?) | 是 | 继承自 TH13 |
| 90 | pointRotate | fffff (varX, varY, x, y, rad) | Rotates point (%3,%4) by angle %5 and stores the resulting coordinates in %1 and %2. | 是 | 继承自 TH13 |
| 91 | floatTime | SfSSff (slot, var, time, mode, init, final) | In %3 frames using mode %4, variable %2 changes from %5 to %6. %1 is used to set the slot to be used by this ins, every enemy has 8 slots (0 to 7). | 是 | 继承自 TH13 |
| 92 | math92 | SfSSffff (slot, var, time, mode, init, final, m, n) | Same as ins_91, but takes 2 extra arguments of unknown meaning. Needs investigation. | 否/待确认 | 继承自 TH13 |
| 93 | math93 | ffff (varX, varY, r1, r2) | Gets a random point based on %3 and %4 and stores it on (%1,%2). Needs investigation. | 否/待确认 | 继承自 TH13 |

### TH16 指令：敌机创建与 ANM 管理 / Enemy creation and ANM script management

| ID | 助记名 | 参数 | 说明 | 文档化 | 来源 |
| --- | --- | --- | --- | --- | --- |
| 300 | enmCreate | mffSSS (sub, x, y, hp, score, item) | Creates an enemy using subroutine %1 at coordinates %2, %3 (relative to position of enemy that called it), health of created enemy is %4, score bonus is %5 and item drop is %6. | 是 | 继承自 TH13 |
| 301 | enmCreateA | mffSSS (sub, x, y, hp, score, item) | Creates an enemy using subroutine %1 at coordinates %2, %3 (absolute position), health of created enemy is %4, score bonus is %5 and item drop is %6. | 是 | 继承自 TH13 |
| 302 | anmSelect | S (anmIndex) | Selects ANM file to be used by other instructions based on %1. | 是 | 继承自 TH13 |
| 303 | anmSetSprite | SS (slot, script) | Loads script %2 from ANM selected with ins_302 on slot %1. | 是 | 继承自 TH13 |
| 304 | enmCreateM | mffSSS (sub, x, y, hp, score, item) | Creates a mirrored enemy using subroutine %1 at coordinates %2, %3 (relative to caller's position), health of created enemy is %4, score bonus is %5 and item drop is %6. | 是 | 继承自 TH13 |
| 305 | enmCreateAM | mffSSS (sub, x, y, hp, score, item) | Creates an mirrored enemy using subroutine %1 at coordinates %2, %3 (absolute position), health of created enemy is %4, score bonus is %5 and item drop is %6. | 是 | 继承自 TH13 |
| 306 | anmSetMain | SS (slot, script) | Loads script %2 from ANM selected with ins_302 on slot %1. However, the script number provided will only be used when the enemy is not moving. When moving left %2+1 will be used, right %2+2, diagonal left %2+3, diagonal right %2+4. Might not work properly if %1 is not 0 according to THBWiki. | 是 | 继承自 TH13 |
| 307 | anmPlay | SS (anmIndex, script) | From ANM file selected based on %1, play script %2 at caller's current coordinates. The spawned script is completely independent, and will continue existing even if caller is deleted. | 是 | 继承自 TH13 |
| 308 | anmPlayAbs | SS (anmIndex, script) | From ANM file selected based on %1, play script %2 at coordinates (0, 0). The spawned script is completely independent, and will continue existing even if caller is deleted. | 是 | 继承自 TH13 |
| 309 | enmCreateF | mffSSS (sub, x, y, hp, score, item) | Creates a filler enemy using subroutine %1 at coordinates %2, %3 (relative to caller's position), health of created enemy is %4, score bonus is %5 and item drop is %6. | 是 | 继承自 TH13 |
| 310 | enmCreateAF | mffSSS (sub, x, y, hp, score, item) | Creates a filler enemy using subroutine %1 at coordinates %2, %3 (absolute position), health of created enemy is %4, score bonus is %5 and item drop is %6. | 是 | 继承自 TH13 |
| 311 | enmCreateMF | mffSSS (sub, x, y, hp, score, item) | Creates a mirrored filler enemy using subroutine %1 at coordinates %2, %3 (relative to caller's position), health of created enemy is %4, score bonus is %5 and item drop is %6. | 是 | 继承自 TH13 |
| 312 | enmCreateAMF | mffSSS (sub, x, y, hp, score, item) | Creates a mirrored filler enemy using subroutine %1 at coordinates %2, %3 (absolute position), health of created enemy is %4, score bonus is %5 and item drop is %6. | 是 | 继承自 TH13 |
| 313 | anmSelectedPlay | S (script) | Same as ins_307, except it uses the ANM file selected by ins_302. | 是 | 继承自 TH13 |
| 314 | anmPlayHigh | SS (anmIndex, script) | Same as ins_307, except it spawns the ANM with a higher layer? Needs further investigation. | 否/待确认 | 继承自 TH13 |
| 315 | anmPlayRotate | SSf (anmIndex, script, angle) | Same as ins_307, except it sets rotation of spawned ANM to %3. | 是 | 继承自 TH13 |
| 316 | anm316 | SS (a, b) | Unknown. | 否/待确认 | 继承自 TH13 |
| 317 | anmSwitch | SS (slot, switch) | Sets the execution pointer of ANM script on slot %1 to where ANM `ins_5(a)` with `a` == `switch` is (the time is also changed to match time of `ins_5`). Doesn't work if the value is 0 apparently? | 是 | 继承自 TH13 |
| 318 | anmReset | — | Resets some ANM-related parameters of the caller (TODO: what exactly?) | 是 | 继承自 TH13 |
| 319 | anmRotate | Sf (slot, r) | Set rotation of an ANM script on slot %1 to %2. | 是 | 继承自 TH13 |
| 320 | anmMove | Sff (slot, x, y) | Set position of an ANM script on slot %1 to (%2,%3). This does not detach the script from the caller, so the actual position of the script will be position of the caller + position set here. | 是 | 继承自 TH13 |
| 321 | enmMapleEnemy | mffSSS (sub, x, y, hp, score, item) | ins_300, but used by 'MapleEnemy' (TODO: what's the difference from ins_300?) | 是 | 继承自 TH13 |
| 322 | enm322 | SS (a, b) | Unknown. | 否/待确认 | 继承自 TH13 |
| 323 | deathAnm | SS (anmIndex, script) | Set the animation that will play when the enemy dies to script %2 from ANM file specified by %1. | 是 | 继承自 TH13 |
| 324 | enm324 | — | Unknown. | 否/待确认 | 继承自 TH13 |
| 325 | anmColor | SSSS (slot, R, G, B) | Modify color of ANM script on slot %1, %2, %3, [c=lightblue]%4 correspond to individual colors and have to be from 0 to 255. | 是 | 继承自 TH13 |
| 326 | anmColorTime | SSSSSS (slot, time, mode, R, G, B) | Same as ins_325, but the change is applied in %2 frames using mode %3. | 是 | 继承自 TH13 |
| 327 | anmAlpha | SS (slot, alpha) | Sets alpha of ANM script on slot %1 to %2 (must be a value between 0-255) | 是 | 继承自 TH13 |
| 328 | anmAlphaTime | SSSS (slot, time, mode, alpha) | Same as ins_327, but the change is applied in %2 frames using mode %3. | 是 | 继承自 TH13 |
| 329 | anmScale | Sff (slot, w, h) | Sets horizontal and vertical scaling of ANM script on slot %1 to %2 and %3 respectively. Overwrites scaling properties set by the ANM script. | 是 | 继承自 TH13 |
| 330 | anmScaleTime | SSSff (slot, time, mode, w, h) | Same as ins_329, but the change is applied in %2 frames using mode %3. | 是 | 继承自 TH13 |
| 331 | anmAlpha2 | SS (slot, alpha) | Sets alpha2 (opacity of the gradient) of ANM script on slot %1 to %2. | 是 | 继承自 TH13 |
| 332 | anmAlpha2Time | SSSS (slot, time, mode, alpha) | Same as ins_331, but the change is applied in %2 frames using mode %3. | 是 | 继承自 TH13 |
| 333 | anm333 | SSSff (a, b, c, r, s) | Unknown. Might be doing something to ANM script on slot %1. | 否/待确认 | 继承自 TH13 |
| 334 | anm334 | S (a) | Hard to tell? THBWiki Google translate gives this: 'The animation effect of the playing unit (enemy), the lightning effect near the evil spirit ball of the god temple', which might be referring to lightning around Nue in TD extra stage. | 否/待确认 | 继承自 TH13 |
| 335 | anmScale2 | Sff (slot, w, h) | Same as ins_329, except it doesn't overwrite the scaling set by the ANM script - instead, it multiplies it. | 是 | 继承自 TH13 |
| 336 | anmLayer | SS (slot, layer) | Set layer of ANM script on slot %1 to %2. | 是 | 继承自 TH14 |
| 337 | anmBlendMode | SS (slot, b) | Set blend mode of ANM script on slot %1 to %2 (TODO: make a list of blend modes). | 是 | 本作 |
| 338 | anmPlayPos | SSfff (anmIndex, script, x, y, z) | Same as ins_307, but the spawned script is offset by (%3,%4). For 3D objects, %5 is used too (TODO: verify that). | 是 | 本作 |
| 339 | anm339 | SSS (a, b, c) | Unknown. Might be doing something to ANM script on slot %1. | 否/待确认 | 本作 |
| 340 | enmDelete | S (id) | Delete enemy with the given ID. | 是 | 本作 |

### TH16 指令：移动管理 / Movement management

| ID | 助记名 | 参数 | 说明 | 文档化 | 来源 |
| --- | --- | --- | --- | --- | --- |
| 400 | movePos | ff (x, y) | Sets caller's absolute position to %1, %2. | 是 | 继承自 TH13 |
| 401 | movePosTime | SSff (time, mode, x, y) | Same as ins_400, but the change is applied in %1 frames using mode %2. | 是 | 继承自 TH13 |
| 402 | movePosRel | ff (x, y) | Sets caller's relative position to %1, %2. | 是 | 继承自 TH13 |
| 403 | movePosRelTime | SSff (time, mode, x, y) | Same as ins_402, but the change is applied in %1 frames using mode %2. | 是 | 继承自 TH13 |
| 404 | moveVel | ff (r, spd) | Sets caller's absolute movement angle to %1 and speed to %2. | 是 | 继承自 TH13 |
| 405 | moveVelTime | SSff (time, mode, r, spd) | Same as ins_404, but the change is applied in %1 frames using mode %2. | 是 | 继承自 TH13 |
| 406 | moveVelRel | ff (r, spd) | Sets caller's relative movement angle to %1 and speed to %2. | 是 | 继承自 TH13 |
| 407 | moveVelRelTime | SSff (time, mode, r, spd) | Same as ins_406, but the change is applied in %1 frames using mode %2. | 是 | 继承自 TH13 |
| 408 | moveCircle | ffff (θ, spd, rad, radInc) | Sets caller's absolute circle movement: %1 is the angle indicating initial position on the circle, %2 is the angular velocity, %3 is circle radius and %4 is by how much the radius increases each frame. | 是 | 继承自 TH13 |
| 409 | moveCircleTime | SSfff (time, mode, spd, rad, radInc) | Same as ins_408, but the change is applied in %1 frames using mode %2. There is also no initial angle parameter here for obvious reason. | 是 | 继承自 TH13 |
| 410 | moveCircleRel | ffff (θ, spd, rad, radInc) | Sets caller's relative circle movement: %1 is the angle indicating initial position on the circle, %2 is the angular velocity, %3 is circle radius and %4 is by how much the radius increases each frame. | 是 | 继承自 TH13 |
| 411 | moveCircleRelTime | SSfff (time, mode, spd, rad, radInc) | Same as ins_410, but the change is applied in %1 frames using mode %2. There is also no initial angle parameter here for obvious reason. | 是 | 继承自 TH13 |
| 412 | moveRand | SSf (time, mode, spd) | Randomizes caller's absolute angle and sets absolute speed to %3. The speed changes back to 0 in %1 frames using mode %2. | 是 | 继承自 TH13 |
| 413 | moveRandRel | SSf (time, mode, spd) | Randomizes caller's relative angle and sets relative speed to %3. The speed changes back to 0 in %1 frames using mode %2. | 是 | 继承自 TH13 |
| 414 | moveBoss | — | Sets caller's absolute position to the absolute position of the boss. If called without a boss, [tip=Google translated from THBWiki, I find this sentence funny]it will cause serious mis-access and explode[/tip]. | 是 | 继承自 TH13 |
| 415 | moveBossRel | — | Sets caller's relative position to the relative position of the boss. If called without a boss, [tip=Google translated from THBWiki, I find this sentence funny]it will cause serious mis-access and explode[/tip]. | 是 | 继承自 TH13 |
| 416 | movePos3d | fff (x, y, z) | Same as ins_400, but takes a %3 parameter for the third dimension, which probably affects 3D ANM scripts used by the caller, or something. | 是 | 继承自 TH13 |
| 417 | movePos3dRel | fff (x, y, z) | Same as ins_402, but takes a %3 parameter for the third dimension, which probably affects 3D ANM scripts used by the caller, or something. | 是 | 继承自 TH13 |
| 418 | moveAdd | ff (x, y) | Increases caller's absolute position by %1 and %2. | 是 | 继承自 TH13 |
| 419 | move419 | ff (x, y) | While the code of this ins looks like it's supposed to be a relative version of ins_418, it doesn't seem to behave like that... | 否/待确认 | 继承自 TH13 |
| 420 | moveEllipse | ffffff (θ, spd, rad, radInc, ellDir, ellRatio) | Sets caller's absolute ellipse movement: %1 is the angle indicating initial position on the ellipse, %2 is the angular velocity, %3 is the base circle radius and %4 is by how much the radius increases each frame. %6 is how much the base circle should be 'squished' to make it an ellipse, and %5 is the squishing angle (I don't know math terms in English, sorry) | 是 | 继承自 TH13 |
| 421 | moveEllipseTime | SSfffff (time, mode, spd, rad, radInc, ellDir, ellRatio) | Same as ins_420, but the change is applied in %1 frames using mode %2. There is also no initial angle parameter here for obvious reason | 是 | 继承自 TH13 |
| 422 | moveEllipseRel | ffffff (θ, spd, rad, radInc, ellDir, ellRatio) | Sets caller's relative ellipse movement: %1 is the angle indicating initial position on the ellipse, %2 is the angular velocity, %3 is the base circle radius and %4 is by how much the radius increases each frame. %6 is how much the base circle should be 'squished' to make it an ellipse, and %5 is the squishing angle (I don't know math terms in English, sorry) | 是 | 继承自 TH13 |
| 423 | moveEllipseRelTime | SSfffff (time, mode, spd, rad, radInc, ellDir, ellRatio) | Same as ins_422, but the change is applied in %1 frames using mode %2. There is also no initial angle parameter here for obvious reason | 是 | 继承自 TH13 |
| 424 | moveSetMirror | S (state) | Sets caller's mirror flag to %1. | 是 | 继承自 TH13 |
| 425 | moveBezier | Sffffff (time, x1, y1, x2, y2, x3, y3) | In %1 frames, the enemy moves towards (%2,%3), then moves towards (%6,%7) for a while and finally moves to (%4,%5). Uses absolute position.<br>From THBWiki: <br>(assuming the current coordinates are (x0, y0)) the motion trajectory is actually a Bezier curve from (x0, y0) to (x2, y2);<br>The P1 coordinate of the curve is `((x1-x0)*1/3, (y1-y0)*1/3)`;<br>The P2 coordinate of the curve is `(-(x3-x2)*1/3+x2,-(y3-y2) *1/3+x2)` | 是 | 继承自 TH13 |
| 426 | moveBezierRel | Sffffff (time, x1, y1, x2, y2, x3, y3) | Same as ins_425, but uses relative position. | 是 | 继承自 TH13 |
| 427 | moveReset | — | Resets some movement-related parameters (TODO: what exactly?) | 否/待确认 | 继承自 TH13 |
| 428 | moveVelNM | ff (r, spd) | Same as ins_404, but ignores the mirror flag. | 是 | 继承自 TH13 |
| 429 | moveVelNMTime | SSff (time, mode, r, spd) | Same as ins_405, but ignores the mirror flag. | 是 | 继承自 TH13 |
| 430 | moveVelNMRel | ff (r, spd) | Same as ins_406, but ignores the mirror flag. | 是 | 继承自 TH13 |
| 431 | moveVelNMRelTime | SSff (time, mode, r, spd) | Same as ins_407, but ignores the mirror flag. | 是 | 继承自 TH13 |
| 432 | moveEnm | S (id) | Sets caller's absolute position to absolute position of enemy with var_-9914 == %1. | 是 | 继承自 TH13 |
| 433 | moveEnmRel | S (id) | Sets caller's relative position to relative position of enemy with var_-9914 == %1. | 是 | 继承自 TH13 |
| 434 | moveCurve | SSSff (time, mode, c, x, y) | In %1 frames using mode %2, caller's absolute position is changed to (%4,%5). The movement trajectory is a curve based on %3, it is unknown how it works exactly. | 否/待确认 | 继承自 TH13 |
| 435 | moveCurveRel | SSSff (time, mode, c, x, y) | In %1 frames using mode %2, caller's relative position is changed to (%4,%5). The movement trajectory is a curve based on %3, it is unknown how it works exactly. | 否/待确认 | 继承自 TH13 |
| 436 | moveAddTime | SSff (time, mode, x, y) | Same as ins_418, but the change is applied in %1 frames using mode %2. | 是 | 继承自 TH13 |
| 437 | moveAddRelTime | SSff (time, mode, x, y) | Same as ins_419, but the change is applied in %1 frames using mode %2 (it also behaves as expected, unlike ins_419). | 是 | 继承自 TH13 |
| 438 | moveCurveAdd | SSSff (time, mode, c, x, y) | Same as ins_434, but instead caller's current absolute coordinates are added to %4 and %5. | 是 | 继承自 TH13 |
| 439 | moveCurveAddRel | SSSff (time, mode, c, x, y) | Same as ins_435, but instead caller's current relative coordinates are added to %4 and %5. | 是 | 继承自 TH13 |
| 440 | moveAngle | f (r) | Sets caller's absolute movement angle to %1. | 是 | 继承自 TH14 |
| 441 | moveAngleTime | SSf (time, mode, r) | Same as ins_440, but the change is applied in %1 frames using mode %2. | 是 | 继承自 TH14 |
| 442 | moveAngleRel | f (r) | Sets caller's relative movement angle to %1. | 是 | 继承自 TH14 |
| 443 | moveAngleRelTime | SSf (time, mode, r) | Same as ins_442, but the change is applied in %1 frames using mode %2. | 是 | 继承自 TH14 |
| 444 | moveSpeed | f (spd) | Sets caller's absolute movement speed to %1. | 是 | 继承自 TH14 |
| 445 | moveSpeedTime | SSf (time, mode, spd) | Same as ins_444, but the change is applied in %1 frames using mode %2. | 是 | 继承自 TH14 |
| 446 | moveSpeedRel | f (spd) | Sets caller's relative movement speed to %1. | 是 | 继承自 TH14 |
| 447 | moveSpeedRelTime | SSf (time, mode, spd) | Same as ins_446, but the change is applied in %1 frames using mode %2. | 是 | 继承自 TH14 |

### TH16 指令：敌机属性与杂项 / Enemy property management and other miscellaneous things

| ID | 助记名 | 参数 | 说明 | 文档化 | 来源 |
| --- | --- | --- | --- | --- | --- |
| 500 | setHurtbox | ff (w, h) | Sets caller's hurtbox width to %1 and height to %2. | 是 | 继承自 TH13 |
| 501 | setHitbox | ff (w, h) | Sets caller's hitbox width to %1 and height to %2. | 是 | 继承自 TH13 |
| 502 | flagSet | S (n) | Sets flag(s) according to %1. Refer to the [flag table](#s=modding/flags) for exact values. | 是 | 继承自 TH13 |
| 503 | flagClear | S (n) | Clears flag(s) according to %1. Refer to the [flag table](#s=modding/flags) for exact values. | 是 | 继承自 TH13 |
| 504 | moveLimit | ffff (x, y, w, h) | Sets caller's movement limit rectangle: (%1,%2) are the coordinates of the center of the rect, while %3, %4 are width and height of it. | 是 | 继承自 TH13 |
| 505 | moveLimitReset | — | Removes caller's movement limit. | 是 | 继承自 TH13 |
| 506 | dropClear | — | Clears caller's extra item drop. | 是 | 继承自 TH13 |
| 507 | dropExtra | SS (type, amount) | Adds %2 items of type %1 to caller's extra drop. Item type table will be made in the future. | 是 | 继承自 TH13 |
| 508 | dropArea | ff (w, h) | Sets caller's item drop area width to %1 and height to %2. | 是 | 继承自 TH13 |
| 509 | dropItems | — | Drops all items the caller has. Has no effect in spell practice. | 是 | 继承自 TH13 |
| 510 | dropMain | S (type) | Sets caller's main drop to %1. | 是 | 继承自 TH13 |
| 511 | lifeSet | S (hp) | Sets caller's current HP and max HP to %1. | 是 | 继承自 TH13 |
| 512 | setBoss | S (a) | If %1 is 0, activates boss mode and makes the caller the main boss. If %1 > 0, it makes the caller the secondary boss. If %1 is -1, ends boss mode. | 是 | 继承自 TH13 |
| 513 | timerReset | — | Resets boss timer. | 是 | 继承自 TH13 |
| 514 | setInterrupt | SSSm (slot, hp, time, sub) | Sets an interrupt on slot %1 (not sure how many slots there are) - once caller's hp reaches %2 or %3 frames have passed since this was called, caller will terminate all subs it's currently running and execute sub %4. | 是 | 继承自 TH13 |
| 515 | setInvuln | S (time) | Makes the caller completely invulnerable for %1 frames. | 是 | 继承自 TH13 |
| 516 | playSound | S (id) | Plays sound %1. Sound id table will be added in the future. | 是 | 继承自 TH13 |
| 517 | setScreenShake | SSS (time, startIntensity, endIntensity) | Activates screen shake for %1 frames. %2 is the starting intensity and %3 is the ending intensity. The larger the intensity, the more the screen shakes. | 是 | 继承自 TH13 |
| 518 | dialogRead | S (dialogueId) | Starts a dialogue, %1 is the ID of an entry in the .msg file. Apart from that, has the effect ins_525. | 是 | 继承自 TH13 |
| 519 | dialogWait | — | Waits until there are no dialogues active, or the running .msg script calls a certain instruction (which one?) | 否/待确认 | 继承自 TH13 |
| 520 | bossWait | — | Waits until there are no boss enemies. | 是 | 继承自 TH13 |
| 521 | setTimeout | Sm (slot, sub) | Sets a timeout interrupt on slot %1 - when the timer reaches 0, caller will terminate all subs it's currently running and execute sub %2. | 是 | 继承自 TH13 |
| 522 | spellEx | SSSm (id, time, type, name) | Same as ins_537, but the difficulty number is NOT added to the id. | 是 | 本作 |
| 523 | spellEnd | — | Ends currently active spellcard. | 是 | 继承自 TH13 |
| 524 | setChapter | S (a) | Some jank that's responsible for showing boss name and possibly other things. In LoLK, it also ends the current chapter and begins a new one. | 否/待确认 | 继承自 TH13 |
| 525 | enmKillAll | — | Kills all other enemies (unless they have a flag that prevents that set). | 是 | 继承自 TH13 |
| 526 | etProtectRange | f (r) | Makes bullets generated by the caller not spawn if they are in radius %1 around the player. | 是 | 继承自 TH13 |
| 527 | lifeMarker | SfS (slot, hp, c) | Sets a new life marker on slot %1, %2 determines where the marker will appear on the health bar (if %2=1000.0f and the enemy has 2000 hp, the marker will split the hp bar in half). %3 is an RGB value of unknown use (possibly leftover from earlier ECL versions) | 是 | 继承自 TH13 |
| 528 | spellUnused | SSSm (id, time, type, name) | No difference from ins_522, unused. | 是 | 本作 |
| 529 | rankF3 | ffff (var, a, b, c) | Sets %1 to %2 if rank is low, %3 if rank is average or %4 if rank is high. | 是 | 继承自 TH13 |
| 530 | rankF5 | ffffff (var, a, b, c, d, e) | Sets %1 to %2 if rank is very low, %3 if rank is low, %4 if rank is average, %5 if rank is high or %6 if rank is very high. | 是 | 继承自 TH13 |
| 531 | rankF2 | fff (var, a, b) | Sets %1 to %2 if rank is low or %3 if rank is high. | 是 | 继承自 TH13 |
| 532 | rankI3 | SSSS (var, a, b, c) | Sets %1 to %2 if rank is low, %3 if rank is average or %4 if rank is high. | 是 | 继承自 TH13 |
| 533 | rankI5 | SSSSSS (var, a, b, c, d, e) | Sets %1 to %2 if rank is very low, %3 if rank is low, %4 if rank is average, %5 if rank is high or %6 if rank is very high. | 是 | 继承自 TH13 |
| 534 | rankI2 | SSS (var, a, b) | Sets %1 to %2 if rank is low or %3 if rank is high. | 是 | 继承自 TH13 |
| 535 | diffI | SSSSS (var, E, N, H, L) | Sets %1 to one of values provided based on difficulty. | 是 | 继承自 TH13 |
| 536 | diffF | fffff (var, E, N, H, L) | Sets %1 to one of values provided based on difficulty. | 是 | 继承自 TH13 |
| 537 | spell | SSSm (id, time, mode, name) | Declares a spellcard with id %1 and name %4. The actual ID passed to the spell-creating function is `id + difficulty`, with easy=0, normal=1, hard=2, lunatic=3, ex=4, overdrive=5. <br>%2 determines how much time the spell circle takes to shrink (in frames), as well as how fast the spell bonus decreases. The exact formula is as follows: <br>[code] int factor = maxSCB >> 2; // maxSCB is hardcoded<br> currSCB -= (maxSCB - factor) / (%2 - 300);<br> currSCB -= currSCB % 10; [/code] <br>As you can guess, setting %2 to 300 causes a division by 0 error and crashes the game, while setting it to a value smaller than 300 causes the SCB to increase over time, instead of decreasing. %3 TBD, it's not unused. | 是 | 本作 |
| 538 | spell2 | SSSm (id, time, mode, name) | Same as ins_537, except the ID used it `id - 1 + difficulty`. | 是 | 本作 |
| 539 | spell3 | SSSm (id, time, mode, name) | Same as ins_537, except the ID used it `id - 2 + difficulty`. | 是 | 本作 |
| 540 | stars | S (cnt) | Sets the amount of stars displayed in the top left corner. Stars might not appear at all if there is no boss active. | 是 | 继承自 TH13 |
| 541 | noHitboxDur | S (time) | Disables the hitbox (but not the hurtbox) for the given amount of frames. | 是 | 继承自 TH13 |
| 542 | spellTimeout | — | Makes the current spell a timeout spell (prevent spell bonus from decreasing, give capture bonus if timed out). | 是 | 继承自 TH13 |
| 543 | unknown543 | — | Unknown. | 否/待确认 | 继承自 TH13 |
| 544 | unknown544 | S (a) | Unknown, sets or clears some flag? | 否/待确认 | 继承自 TH13 |
| 545 | laserCancel | — | Cancels all lasers. | 是 | 继承自 TH13 |
| 546 | bombShield | SS (a, script) | Sets the bomb invulnerability flag (%1=1 set, %1=0 not set), the caller's ANM script will change to %2 when a bomb is active (how does it work with ANM slots exactly?) | 是 | 继承自 TH13 |
| 547 | gameSpeed | f (s) | Sets game speed to %1 of the normal speed. In ISC, enemies with flag 13 (dec=8192) set will ignore effects of this opcode. | 是 | 继承自 TH13 |
| 548 | diffWait | SSSS (e, n, h, l) | Same as ins_23, but the wait time is chosen from the given 4 based on the difficulty. | 是 | 继承自 TH13 |
| 549 | unknown549 | S (a) | Unknown. | 否/待确认 | 继承自 TH13 |
| 550 | unknown550 | S (a) | Unknown. | 否/待确认 | 继承自 TH13 |
| 551 | unknown551 | S (a) | Unknown. | 否/待确认 | 继承自 TH13 |
| 552 | zIndex | S (layers) | Increases layer of all ANM scripts used by the caller by %1. | 是 | 继承自 TH13 |
| 553 | hitSound | S (id) | Makes the caller play sound %1 when hit. Sound id table will be added in the future. | 是 | 继承自 TH13 |
| 554 | stageLogo | — | Shows the stage logo from an ANM of a hardcoded name. | 是 | 继承自 TH13 |
| 555 | enmAlive | SS (var, id) | Checks if enemy of var_-9914 == %2 is still alive, and sets %1 to 1 if it is or 0 if it isn't. | 是 | 继承自 TH13 |
| 556 | setDeath | m (sub) | Makes the caller execute sub %1 when the HP reaches 0. Keep in mind that the caller is already marked for deletion at the point when the sub actually executes, so if you put waiting there the sub will not execute fully (because the caller will be deleted) | 是 | 继承自 TH13 |
| 557 | fogTime | SSSff (time, mode, color, start, end) | Same as STD ins_9, that is, fogTime. Refer to [the STD instruction table](#s=modding/std-ins) for details. | 是 | 继承自 TH13 |
| 558 | flagMirror | S (state) | Literally the exact same instruction as ins_424. | 是 | 继承自 TH13 |
| 559 | enmLimit | S (limit) | Set the maximum number of enemies that can be present. New enemies will fail to spawn if the cap is reached. Default is 99999. | 是 | 继承自 TH13 |
| 560 | unknown560 | ff (r, s) | Unknown. | 否/待确认 | 继承自 TH13 |
| 561 | die | — | Makes the caller execute the sub set with ins_556. If there is no such sub set, the caller dies instead (exactly the same as if the player shot down the caller, that is, items are dropped, death sound plays etc) | 是 | 继承自 TH13 |
| 562 | dropItemsSp | — | Same as ins_509, but item spawning will not be blocked in spell practice. | 是 | 继承自 TH13 |
| 563 | unknown563 | S (flagState) | Sets [flag 12](#s=modding/flags) (decimal 4096), which controls whether the hitbox and hurtbox is a rectangle. If %1 is 1, collision is a rectangle. If %1 is 0, collision is elliptical. | 是 | 继承自 TH14 |
| 564 | hitboxRotate | f (angle) | Rotates the hitbox and hurtbox of the enemy (note: the hitbox rotation is really janky, but hurtbox rotates fine). Has no effect unless the enemy uses rectangular collision. | 是 | 继承自 TH14 |
| 565 | bombInvuln | f (red) | Sets caller's damage reduction when a bomb is active, 0.0f means no damage at all, 1.0f is full damage, negative values will make the enemy heal when you bomb. | 是 | 继承自 TH14 |
| 566 | unknown566 | () | Unknown (does it even exist?) | 否/待确认 | 继承自 TH14 |
| 567 | unknown567 | S (a) | Unknown. | 否/待确认 | 继承自 TH14 |
| 568 | spellMode | S (state) | Enables/disables spell card damage reduction, if %1 is 1 it's enabled, if it's 0 it's disabled. Can be used outside of spell cards. | 是 | 继承自 TH14 |
| 569 | unknown569 | S (a) | Unknown. | 否/待确认 | 继承自 TH15 |
| 570 | unknown570 | — | Unknown. | 否/待确认 | 继承自 TH15 |
| 571 | unknown571 | — | Unknown. | 否/待确认 | 继承自 TH15 |
| 572 | lifeNow | S (hp) | Sets caller's current HP to %1, without changing max HP. | 是 | 本作 |

### TH16 指令：子弹创建与删除 / Bullet creation and deletion

| ID | 助记名 | 参数 | 说明 | 文档化 | 来源 |
| --- | --- | --- | --- | --- | --- |
| 600 | etNew | S (etId) | Resets bullet manager %1 to default properties. | 是 | 继承自 TH13 |
| 601 | etOn | S (etId) | Shoots bullet(s) using properties from bullet manager %1. | 是 | 继承自 TH13 |
| 602 | etSprite | SSS (etId, type, color) | Sets bullet type and color of bullet manager %1. Refer to [this image](https://cdn.discordapp.com/attachments/395767870119870466/570658618316161041/BULLET_IDS.png) made by Dai. Remarks:<br>- bullet types 35 and 36 spin<br>- type 30 pulses<br>- the difference between 16/37 is the spin direction (same case for 23 and 24) | 是 | 继承自 TH15 |
| 603 | etOffset | Sff (etId, x, y) | Sets the relative offset of bullets spawned by bullet manager %1 to (%2,%3). | 是 | 继承自 TH13 |
| 604 | etAngle | Sff (etId, angle1, angle2) | Sets angle1 and angle2 of bullet manager %1. | 是 | 继承自 TH13 |
| 605 | etSpeed | Sff (etId, speed1, speed2) | Sets speed1 and speed2 of bullet manager %1. | 是 | 继承自 TH13 |
| 606 | etCount | SSS (etId, count1, count2) | Sets count1 and count2 of bullet manager %1. | 是 | 继承自 TH13 |
| 607 | etAim | SS (etId, aim) | Sets aim mode of bullet manager %1. | 是 | 继承自 TH13 |
| 608 | etSound | SSS (etId, sound1, sound2) | Sets sound1 and sound2 of bullet manager %1 (sound effect table is TODO). sound1 plays when the bullet manager fires a bullet, while sound2 plays when a bullet fired by the bullet manager does certain transformations. Set to -1 for no sound. | 是 | 继承自 TH13 |
| 609 | etExSet | SSSSSSff (etId, index, async, type, a, b, r, s) | Sets bullet transformation of bullet manager %1, transformation explanation will be added in the future. | 是 | 继承自 TH13 |
| 610 | etExSet2 | SSSSSSSSffff (etId, index, async, type, a, b, c, d, r, s, m, n) | Same as ins_609, but takes more arguments for certain transformation types. | 是 | 继承自 TH13 |
| 611 | etEx | SSSSSff (etId, async, type, a, b, r, s) | Adds bullet transformation to bullet manager %1, transformation explanation will be added in the future. | 是 | 继承自 TH13 |
| 612 | etEx2 | SSSSSSSffff (etId, async, type, a, b, c, d, r, s, m, n) | Same as ins_611, but takes more arguments for certain transformation types. | 是 | 继承自 TH13 |
| 613 | etClearAll | — | Clears all bullets. | 是 | 继承自 TH13 |
| 614 | etCopy | SS (etIdDest, etIdSrc) | Copies everything from bullet manager %2 into bullet manager %1. Warning: this instruction is partially broken and does NOT copy the index next ins_611/ins_612 transformations will be added at. | 是 | 继承自 TH13 |
| 615 | etCancel | f (r) | Clears all bullets in a circle of radius %1 around the caller, and turns them into cancel items. | 是 | 继承自 TH13 |
| 616 | etClear | f (r) | Clears all bullets in a circle of radius %1 around the caller without turning them into cancel items. | 是 | 继承自 TH13 |
| 617 | etSpeedR3 | Sffffff (etId, spd1l, spd1m, spd1h, spd2l, spd2m, spd2h) | Sets speed1 and speed2 of bullet manager %1 to two of the values provided, based on ingame rank (l=low, m=medium, h=high) | 是 | 继承自 TH13 |
| 618 | etSpeedR5 | Sffffffffff (etId, spd1l, spd1ml, spd1m, spd1mh, spd1h, spd2l, spd2ml, spd2m, spd2mh, spd2h) | Sets speed1 and speed2 of bullet manager %1 to two of the values provided, based on ingame rank (l=low, ml=medium-low, m=medium, mh=medium-high, h=high) | 是 | 继承自 TH13 |
| 619 | etSpeedR2 | Sffff (etId, spd1l, spd1h, spd2l, spd2h) | Sets speed1 and speed2 of bullet manager %1 to two of the values provided, based on ingame rank (l=low, h=high) | 是 | 继承自 TH13 |
| 620 | etCountR3 | SSSSSSS (etId, cnt1l, cnt1m, cnt1h, cnt2l, cnt2m, cnt2h) | Sets count1 and count2 of bullet manager %1 to two of the values provided, based on ingame rank (l=low, m=medium, h=high) | 是 | 继承自 TH13 |
| 621 | etCountR5 | SSSSSSSSSSS (etId, cnt1l, cnt1ml, cnt1m, cnt1mh, cnt1h, cnt2l, cnt2ml, cnt2m, cnt2mh, cnt2h) | Sets count1 and count2 of bullet manager %1 to two of the values provided, based on ingame rank (l=low, ml=medium-low, m=medium, mh=medium-high, h=high) | 是 | 继承自 TH13 |
| 622 | etCountR2 | SSSSS (etId, cnt1l, cnt1h, cnt2l, cnt2h) | Sets count1 and count2 of bullet manager %1 to two of the values provided, based on ingame rank (l=low, h=high) | 是 | 继承自 TH13 |
| 623 | angleToPlayer | fff (var, x, y) | Gets angle to the player from coordinates (%2,%3) and stores it in %1. | 是 | 继承自 TH13 |
| 624 | etSpeedD | Sffffffff (etId, spd1e, spd1n, spd1h, spd1l, spd2e, spd2n, spd2h, spd2l) | Sets speed1 and speed2 of bullet manager %1 to 2 of the values provided, based on the difficulty (e=easy, n=normal, h=hard, l=lunatic) | 是 | 继承自 TH13 |
| 625 | etCountD | SSSSSSSSS (etId, cnt1e, cnt1n, cnt1h, cnt1l, cnt2e, cnt2n, cnt2h, cnt2l) | Sets count1 and count2 of bullet manager %1 to 2 of the values provided, based on the difficulty (e=easy, n=normal, h=hard, l=lunatic) | 是 | 继承自 TH13 |
| 626 | etOffsetRad | Sff (etId, angle, radius) | Sets the relative offset of bullets spawned by bullet manager %1 to (cos(%2)\*%3,sin(%2)\*%3). Stacks with ins_603. | 是 | 继承自 TH13 |
| 627 | etDist | Sf (etId, dist) | Sets distance of bullets spawned by bullet manager %1 to %2 (that is, when a bullet is spawned it moves by %2 using its current angle). | 是 | 继承自 TH13 |
| 628 | etOffsetAbs | Sff (etId, x, y) | Sets the absolute offset of bullets spawned by bullet manager %1 to (%2,%3). | 是 | 继承自 TH13 |
| 629 | fog | fS (r, color) | Sets caller's fog's radius to %1 and color to %2 (RGB value in reverse order). This resets the fog completely, that is, every time it's called the fog spawn animation plays. | 是 | 继承自 TH13 |
| 630 | callSTD | S (switch) | Sets execution pointer of the STD script to where STD ins_16(%1) is (%1 must be the same), basically same concept as ins_317. | 是 | 继承自 TH13 |
| 631 | lifeHide | S (time) | Hides boss lifebar for %1 frames. | 是 | 继承自 TH13 |
| 632 | funcSet | S (id) | Sets a function that the game will execute every frame from a set of hardcoded functions that differs between games. | 是 | 继承自 TH13 |
| 633 | flagExtDmg | S (state) | Sets the external damage flag to %1. Caller probably needs to be the main boss for this to work - with this flag set, the caller gets damaged by the value stored in var_-9940 every frame, and then resets the value. This allows other enemies to damage the boss by incrementing the aforementioned variable, used in LoLK by Sagume (and also happens to be the main cause of the Sagume skip glitch) | 是 | 继承自 TH13 |
| 634 | setHitboxFunc | S (id) | Make the caller use a special function for determining collision with the player. TODO: create a list of functions and their IDs | 是 | 继承自 TH13 |
| 635 | etCancel2 | f (r) | Same as ins_615, but doesn't clear bullets with bomb invulnerability. | 是 | 继承自 TH13 |
| 636 | etClear2 | f (r) | Same as ins_616, but doesn't clear bullets with bomb invulnerability. | 是 | 继承自 TH13 |
| 637 | funcCall | S (id) | Same as ins_632, except the function is called just once instead of every frame. | 是 | 继承自 TH13 |
| 638 | scoreAdd | S (n) | Adds %1 to score (or subtracts if %1 is negative). There is no lower boundary check, so if this causes score to go below 0, an underflow happens. | 是 | 继承自 TH13 |
| 639 | funcSet2 | S (id) | Same as ins_632, except it sets an unknown flag to 1 (ins_632 sets it to 0) | 是 | 继承自 TH13 |
| 640 | etExSub | SSm (etId, index, s) | Sets the string parameter of transform on index %2 in bullet manager %1 to %3, transformations will be explained separately later. | 是 | 继承自 TH13 |
| 641 | etExSubtract | S (etId) | Subtracts 1 from the index used by ins_611 and ins_612, unless it's already 0. This basically changes where the next transformation will be appended. | 是 | 继承自 TH14 |

### TH16 指令：激光创建 / Laser creation

| ID | 助记名 | 参数 | 说明 | 文档化 | 来源 |
| --- | --- | --- | --- | --- | --- |
| 700 | laserNew | Sffff (etId, init_length, final_length, unknown_arg_3, width) | Sets basic parameters of the laser. %4 has something to do with the length of straight line lasers (investigation needed), but doesn't do anything for other laser types. For curvy lasers, the only used argument is %5, and length is specified with ins_701 instead. | 是 | 继承自 TH13 |
| 701 | laserTiming | SSSSSS (edId, startup_time, expand_time, duration, shrink_time, init_flags) | Sets timing for infinite lasers. %6 sets the initial flags for a laser, but these flags are unknown at the moment. For curvy lasers, the %2 argument instead specifies the length of the laser. | 是 | 继承自 TH13 |
| 702 | laserOn | S (edId) | Shoots a straight line laser. | 是 | 继承自 TH13 |
| 703 | laserStOn | SS (etId, laser_id) | Shoots an infinite laser. %2 is a number that's used to identify this particular laser instance, so that it can be referred to in other instructions. | 是 | 继承自 TH13 |
| 704 | laserOffset | Sff (laser_id, x, y) | Sets the position of the infinite laser pointed to by %1. | 是 | 继承自 TH13 |
| 705 | laserTrajectory | Sff (laser_id, x_speed, y_speed) | Sets the offset velocity of the infinite laser pointed to by %1. The laser's position will change by %2 and %3 every frame. | 是 | 继承自 TH13 |
| 706 | laserStLength | Sf (laser_id, speed) | Sets the speed of the infinite laser pointed to by %1. | 是 | 继承自 TH13 |
| 707 | laserStWidth | Sf (laser_id, width) | Sets the width of the infinite laser pointed to by %1. | 是 | 继承自 TH13 |
| 708 | laserStAngle | Sf (laser_id, angle) | Sets the angle of the infinite laser pointed to by %1. | 是 | 继承自 TH13 |
| 709 | laserStRotation | Sf (laser_id, angular_vel) | Sets the angular velocity of the infinite laser pointed to by %1. The laser's angle will change by %2 every frame. | 是 | 继承自 TH13 |
| 710 | laserStEnd | S (laser_id) | Clears the laser pointed to by %1. | 是 | 继承自 TH13 |
| 711 | laserCuOn | S (etId) | Shoots a curvy laser. | 是 | 继承自 TH13 |
| 712 | etCancelRect | ff (w, h) | Cancels all bullets in rectangle of width %1 and height %2. The area is affected by rotation set by ins_564. | 是 | 继承自 TH14 |
| 713 | unknown713 | SS (etId, laser_id) | Shoots a laser 'beam', a laser type used by marisa in GFW. Broken since this laser type does not exist outside of GFW. | 是 | 继承自 TH13 |
| 714 | unknown714 | SS (laser_id, unknown) | Does something with a laser beam pointed to by %1. Broken since this laser type does not exist outside of GFW. | 是 | 继承自 TH13 |

### TH16 指令：敌机交互 / Enemy interaction

| ID | 助记名 | 参数 | 说明 | 文档化 | 来源 |
| --- | --- | --- | --- | --- | --- |
| 800 | enmCall | Sm (id, sub) | Makes enemy with var_-9914 == %1 stop all subs it's running and execute sub %2 (works like an interrupt). This will NOT make the enemy execute the sub right as this instruction is called, the new sub will be executed when the game handles the given enemy, which might be later on the same frame or on the next frame. Using this to make the caller interrupt itself can make the game explode. | 是 | 继承自 TH13 |
| 801 | enmPos | ffS (varX, varY, id) | Stores coordinates of enemy with var_-9914 == %3 in (%1,%2). | 是 | 继承自 TH13 |
| 802 | broadcastInterrupt | S (slot) | For all existing bosses, trigger the interrupt set by ins_514 on slot %1. Does not change the HP to the one set in ins_514. | 是 | 继承自 TH13 |

### TH16 指令：调试 / Debug

| ID | 助记名 | 参数 | 说明 | 文档化 | 来源 |
| --- | --- | --- | --- | --- | --- |
| 900 | debug900 | — | 未在 Priw8 表中记录/待确认 | 否/待确认 | — |
| 901 | debug901 | — | 未在 Priw8 表中记录/待确认 | 否/待确认 | — |
| 902 | debug902 | — | 未在 Priw8 表中记录/待确认 | 否/待确认 | — |

### TH16 指令：游戏特有 / Game specific

| ID | 助记名 | 参数 | 说明 | 文档化 | 来源 |
| --- | --- | --- | --- | --- | --- |
| 1000 | dropSeason | SSS (time, max, min) | Set the number of season items dropped by the enemy. At the time this instruction is called, the bonus for killing the enemy will be %2 season items, and will decrease linearly to %3 over the next %1 frames. | 是 | 本作 |
| 1001 | seasonItemDamage | S (damage) | The enemy will spawn a season item for every %1 points of damage it receives. Used by bosses. | 是 | 本作 |

### TH16 变量

| ID | 名称 | 类型 | 访问 | 作用域 | 说明 | 文档化 | 来源 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| -10000 | RAND | int | 只读 | global/全局 | Random integer, very large range. | 是 | 继承自 TH10 |
| -9999.0f | RANDF | float | 只读 | global/全局 | Random float from 0.0f to 1.0f. | 是 | 继承自 TH10 |
| -9998.0f | RANDRAD | float | 只读 | global/全局 | Random float from -pi to pi. | 是 | 继承自 TH10 |
| -9997.0f | FINAL_X | float | 只读 | local/敌机局部 | Final X position of the enemy. | 是 | 继承自 TH10 |
| -9996.0f | FINAL_Y | float | 只读 | local/敌机局部 | Final Y position of the enemy. | 是 | 继承自 TH10 |
| -9995.0f | ABS_X | float | 只读 | local/敌机局部 | Absolute X position of the enemy. | 是 | 继承自 TH10 |
| -9994.0f | ABS_Y | float | 只读 | local/敌机局部 | Absolute Y position of the enemy. | 是 | 继承自 TH10 |
| -9993.0f | REL_X | float | 只读 | local/敌机局部 | Relative X position of the enemy. | 是 | 继承自 TH10 |
| -9992.0f | REL_Y | float | 只读 | local/敌机局部 | Relative Y position of the enemy. | 是 | 继承自 TH10 |
| -9991.0f | PLAYER_X | float | 只读 | global/全局 | Player's X position. | 是 | 继承自 TH10 |
| -9990.0f | PLAYER_Y | float | 只读 | global/全局 | Player's Y position. | 是 | 继承自 TH10 |
| -9989.0f | ANGLE_PLAYER | float | 只读 | local/敌机局部 | Angle from the enemy to the player. | 是 | 继承自 TH10 |
| -9988 | TIME | int | 只读 | local/敌机局部 | Time elapsed since the enemy spawned, in frames. | 是 | 继承自 TH10 |
| -9987.0f | RANDF2 | float | 只读 | global/全局 | Random float from -1.0f to 1.0f. | 是 | 继承自 TH10 |
| -9986 | TIMEOUT | int | 只读 | global/全局 | Set to 1 by the engine when a timeout occurs. | 是 | 继承自 TH10 |
| -9985 | I0 | int | 读写 | local/敌机局部 | Local integer variable, inherited by spawned enemies. | 是 | 继承自 TH10 |
| -9984 | I1 | int | 读写 | local/敌机局部 | Local integer variable, inherited by spawned enemies. | 是 | 继承自 TH10 |
| -9983 | I2 | int | 读写 | local/敌机局部 | Local integer variable, inherited by spawned enemies. | 是 | 继承自 TH10 |
| -9982 | I3 | int | 读写 | local/敌机局部 | Local integer variable, inherited by spawned enemies. | 是 | 继承自 TH10 |
| -9981.0f | F0 | float | 读写 | local/敌机局部 | Local float variable, inherited by spawned enemies. | 是 | 继承自 TH10 |
| -9980.0f | F1 | float | 读写 | local/敌机局部 | Local float variable, inherited by spawned enemies. | 是 | 继承自 TH10 |
| -9979.0f | F2 | float | 读写 | local/敌机局部 | Local float variable, inherited by spawned enemies. | 是 | 继承自 TH10 |
| -9978.0f | F3 | float | 读写 | local/敌机局部 | Local float variable, inherited by spawned enemies. | 是 | 继承自 TH10 |
| -9977.0f | FINAL_X2 | float | 只读 | local/敌机局部 | Same as var_-9997. | 是 | 继承自 TH10 |
| -9976.0f | FINAL_Y2 | float | 只读 | local/敌机局部 | Same as var_-9996. | 是 | 继承自 TH10 |
| -9975.0f | ABS_X2 | float | 只读 | local/敌机局部 | Same as var_-9995. | 是 | 继承自 TH10 |
| -9974.0f | ABS_Y2 | float | 只读 | local/敌机局部 | Same as var_-9994. | 是 | 继承自 TH10 |
| -9973.0f | REL_X2 | float | 只读 | local/敌机局部 | Same as var_-9993. | 是 | 继承自 TH10 |
| -9972.0f | REL_Y2 | float | 只读 | local/敌机局部 | Same as var_-9992. | 是 | 继承自 TH10 |
| -9971.0f | ABS_ANGLE | float | 只读 | local/敌机局部 | Angle of enemy's absolute movement. | 是 | 继承自 TH10 |
| -9970.0f | REL_ANGLE | float | 只读 | local/敌机局部 | Angle of enemy's relative movement. | 是 | 继承自 TH10 |
| -9969.0f | ABS_SPEED | float | 只读 | local/敌机局部 | Speed of enemy's absolute movement. | 是 | 继承自 TH10 |
| -9968.0f | REL_SPEED | float | 只读 | local/敌机局部 | Speed of enemy's relative movement. | 是 | 继承自 TH10 |
| -9967.0f | ABS_ORIGIN_DIST | float | 只读 | local/敌机局部 | Distance from the origin of enemy's absolute circular movement (radius of the circle). | 是 | 继承自 TH10 |
| -9966.0f | REL_ORIGIN_DIST | float | 只读 | local/敌机局部 | Distance from the origin of enemy's relative circular movement (radius of the circle). | 是 | 继承自 TH10 |
| -9965.0f | PLAYER_X2 | float | 只读 | global/全局 | Same as var_-9991. | 是 | 继承自 TH10 |
| -9964.0f | PLAYER_Y2 | float | 只读 | global/全局 | Same as var_-9990. | 是 | 继承自 TH10 |
| -9963.0f | BOSS_X | float | 只读 | global/全局 | Final X position of the boss. | 是 | 继承自 TH10 |
| -9962.0f | BOSS_Y | float | 只读 | global/全局 | Final Y position of the boss. | 是 | 继承自 TH10 |
| -9961 | ANM_ID | int | 只读 | local/敌机局部 | Is the current script on anm slot 0 of the enemy. | 是 | 继承自 TH10 |
| -9960 | RANK | int | 只读 | global/全局 | Numeric value of rank, ranging from -1024 to 1024. Increases over time and decreases when player bombs/dies etc. | 是 | 继承自 TH10 |
| -9959 | DIFF | int | 只读 | global/全局 | Difficulty (E=0, N=1, H=2, L=3, EX=4, O=5) | 是 | 继承自 TH10 |
| -9958.0f | FINAL_ANGLE | float | 只读 | local/敌机局部 | Final angle of enemy's movement. | 是 | 继承自 TH10 |
| -9957 | TRUE | int | 只读 | global/全局 | Always returns 1. | 是 | 继承自 TH10 |
| -9956.0f | ABS_ANGLE_PLAYER | float | 只读 | local/敌机局部 | Angle to the player from enemy's absolute position. | 是 | 继承自 TH10 |
| -9955.0f | REL_ANGLE_PLAYER | float | 只读 | local/敌机局部 | Angle to the player from enemy's relative position. | 是 | 继承自 TH10 |
| -9954 | LIFE | int | 只读 | local/敌机局部 | Enemy's current HP. | 是 | 继承自 TH10 |
| -9953 | EASY | int | 只读 | global/全局 | Set to 1 if difficulty is easy, otherwise it's 0. | 是 | 继承自 TH10 |
| -9952 | NORMAL | int | 只读 | global/全局 | Set to 1 if difficulty is normal, otherwise it's 0. | 是 | 继承自 TH10 |
| -9951 | HARD | int | 只读 | global/全局 | Set to 1 if difficulty is hard, otherwise it's 0. | 是 | 继承自 TH10 |
| -9950 | LUNATIC | int | 只读 | global/全局 | Set to 1 if difficulty is lunatic, otherwise it's 0. | 是 | 继承自 TH10 |
| -9949 | MISS_COUNT | int | 读写 | global/全局 | Increased by 1 every time the player dies. | 是 | 继承自 TH11 |
| -9948 | BOMB_COUNT | int | 读写 | global/全局 | Increased by 1 every time the player bombs. | 是 | 继承自 TH11 |
| -9947 | CAPTURE | int | 读写 | global/全局 | Set to 0 when the player dies, bombs, or uses a game-specific mechanic that "fails" a spell. | 是 | 继承自 TH11 |
| -9946 | ENM_CNT_REAL | int | 只读 | global/全局 | Amount of enemies alive (including main and MapleEnemy). | 是 | 继承自 TH11 |
| -9945 | SHOTTYPE | int | 只读 | global/全局 | Numeric value that represents player's shottype, the first shottype is 0. | 是 | 继承自 TH11 |
| -9944.0f | DIST_PLAYER | float | 只读 | local/敌机局部 | Distance from the enemy to the player. | 是 | 继承自 TH11 |
| -9943 | BI0 | int | 读写 | local/敌机局部 | Is the same as the I0 variable of boss 0. | 是 | 继承自 TH11 |
| -9942 | BI1 | int | 读写 | local/敌机局部 | Is the same as the I1 variable of boss 0. | 是 | 继承自 TH11 |
| -9941 | BI2 | int | 读写 | local/敌机局部 | Is the same as the I2 variable of boss 0. | 是 | 继承自 TH11 |
| -9940 | BI3 | int | 读写 | local/敌机局部 | Is the same as the I3 variable of boss 0. | 是 | 继承自 TH11 |
| -9939.0f | BF0 | float | 读写 | local/敌机局部 | Is the same as the F0 variable of boss 0. | 是 | 继承自 TH11 |
| -9938.0f | BF1 | float | 读写 | local/敌机局部 | Is the same as the F1 variable of boss 0. | 是 | 继承自 TH11 |
| -9937.0f | BF2 | float | 读写 | local/敌机局部 | Is the same as the F2 variable of boss 0. | 是 | 继承自 TH11 |
| -9936.0f | BF3 | float | 读写 | local/敌机局部 | Is the same as the F3 variable of boss 0. | 是 | 继承自 TH11 |
| -9935.0f | F4 | float | 读写 | local/敌机局部 | Local float variable inherited by spawned enemies, just like F0-F3 and I0-I3. | 是 | 继承自 TH11 |
| -9934.0f | F5 | float | 读写 | local/敌机局部 | Local float variable inherited by spawned enemies, just like F0-F3 and I0-I3. | 是 | 继承自 TH11 |
| -9933.0f | F6 | float | 读写 | local/敌机局部 | Local float variable inherited by spawned enemies, just like F0-F3 and I0-I3. | 是 | 继承自 TH11 |
| -9932.0f | F7 | float | 读写 | local/敌机局部 | Local float variable inherited by spawned enemies, just like F0-F3 and I0-I3. | 是 | 继承自 TH11 |
| -9931 | LAST_ENM_ID | int | 只读 | global/全局 | ID of the last spawned enemy. | 是 | 继承自 TH12 |
| -9930 | POWER | int | 只读 | global/全局 | Player's power (4.00 => 400) | 是 | 继承自 TH12 |
| -9929 | DS1 | int | 只读 | global/全局 | Used in Double Spoiler, unknown. | 否/待确认 | 继承自 TH12.5 |
| -9928 | DS2 | int | 只读 | global/全局 | Used in Double Spoiler, unknown. | 否/待确认 | 继承自 TH12.5 |
| -9927 | DS3 | int | 只读 | global/全局 | Used in Double Spoiler, unknown. | 否/待确认 | 继承自 TH12.5 |
| -9926 | GI0 | int | 读写 | global/全局 | Global integer variable. | 是 | 继承自 TH12.5 |
| -9925 | GI1 | int | 读写 | global/全局 | Global integer variable. | 是 | 继承自 TH12.5 |
| -9924 | GI2 | int | 读写 | global/全局 | Global integer variable. | 是 | 继承自 TH12.5 |
| -9923 | GI3 | int | 读写 | global/全局 | Global integer variable. | 是 | 继承自 TH12.5 |
| -9922.0f | GF0 | float | 读写 | global/全局 | Global float variable. | 是 | 继承自 TH12.5 |
| -9921.0f | GF1 | float | 读写 | global/全局 | Global float variable. | 是 | 继承自 TH12.5 |
| -9920.0f | GF2 | float | 读写 | global/全局 | Global float variable. | 是 | 继承自 TH12.5 |
| -9919.0f | GF3 | float | 读写 | global/全局 | Global float variable. | 是 | 继承自 TH12.5 |
| -9918.0f | GF4 | float | 读写 | global/全局 | Global float variable. | 是 | 继承自 TH12.5 |
| -9917.0f | GF5 | float | 读写 | global/全局 | Global float variable. | 是 | 继承自 TH12.5 |
| -9916.0f | GF6 | float | 读写 | global/全局 | Global float variable. | 是 | 继承自 TH12.5 |
| -9915.0f | GF7 | float | 读写 | global/全局 | Global float variable. | 是 | 继承自 TH12.5 |
| -9914 | ID | int | 只读 | local/敌机局部 | ID of the enemy. | 是 | 继承自 TH12.5 |
| -9913 | DS_PHOTOCOUNT | int | 只读 | global/全局 | Used in Double Spoiler, amount of photos taken. | 是 | 继承自 TH12.5 |
| -9912 | DS4 | int | 只读 | global/全局 | Used in Double Spoiler, unknown. | 否/待确认 | 继承自 TH12.5 |
| -9911.0f | ANGLE_BOSS | float | 只读 | global/全局 | Angle at which the boss moves. | 是 | 继承自 TH12.5 |
| -9910.0f | SPEED_BOSS | float | 只读 | global/全局 | Speed at which the boss moves. | 是 | 继承自 TH12.5 |
| -9909 | UNKNOWN9 | int | 只读 | local/敌机局部 | Enemy ID of the parent enemy. | 是 | 继承自 TH12.8 |
| -9908 | ENM_CNT | int | 只读 | global/全局 | Amount of killable enemies alive (that is, doesn't include hitboxless/intangible enemies etc). | 是 | 继承自 TH13 |
| -9907 | SPELL_ID | int | 只读 | global/全局 | Spellcard ID, used by spell practice. Unknown meaning in LoLK. | 是 | 继承自 TH13 |
| -9906 | MIRROR | int | 只读 | local/敌机局部 | Mirror flag state, either 0 or 1. TODO: verify game version | 否/待确认 | 继承自 TH15 |
| -9905 | [-9905] | int | 只读 | global/全局 | Value set by ins_524. | 是 | 继承自 TH15 |
| -9904 | MISS_COUNT_GLOBAL | int | 只读 | global/全局 | Amount of misses throughout the entire game. | 是 | 继承自 TH15 |
| -9903 | SUBSEASON | int | 只读 | global/全局 | Selected subseason. Spring = 0, summer = 1, autumn = 2, winter = 3, extra subseason = 4. | 是 | 本作 |

## TH16.5 秘封噩梦日记

- 体系：第四世代
- 指令：普通指令 334 条；已说明 271/334。主要分组：系统/流程/栈/算术 / System；敌机创建与 ANM 管理 / Enemy creation and ANM script management；移动管理 / Movement management；敌机属性与杂项 / Enemy property management and other miscellaneous things；子弹创建与删除 / Bullet creation and deletion；激光创建 / Laser creation；敌机交互 / Enemy interaction；调试 / Debug；游戏特有 / Game specific。
- 变量：变量范围 -10000..-9903；本文列出有说明/命名记录的 98 条，未列空洞/未知项。

### TH16.5 指令：系统/流程/栈/算术 / System

| ID | 助记名 | 参数 | 说明 | 文档化 | 来源 |
| --- | --- | --- | --- | --- | --- |
| 0 | nop | — | Empty instruction, doesn't do anything. | 是 | 继承自 TH13 |
| 1 | delete | — | Returns to the top of current call stack. | 是 | 继承自 TH13 |
| 2 | ins_2 | — |  | 否/待确认 | 继承自 TH-1 |
| 3 | ins_3 | — |  | 否/待确认 | 继承自 TH-1 |
| 4 | ins_4 | — |  | 否/待确认 | 继承自 TH-1 |
| 5 | ins_5 | — |  | 否/待确认 | 继承自 TH-1 |
| 6 | ins_6 | — |  | 否/待确认 | 继承自 TH-1 |
| 7 | ins_7 | — |  | 否/待确认 | 继承自 TH-1 |
| 8 | ins_8 | — |  | 否/待确认 | 继承自 TH-1 |
| 9 | ins_9 | — |  | 否/待确认 | 继承自 TH-1 |
| 10 | ret | — | Returns from the current sub. | 是 | 继承自 TH13 |
| 11 | call | m (sub) | Calls a given sub. Can take additional parameters to pass as arguments to the sub. [c=orange]Direct Usage obsolete. Use `@subName()` syntax instead. | 是 | 继承自 TH13 |
| 12 | jmp | o (target) | Unconditionally jumps to the label %1. [c=orange]Direct usage obsolete. Use `goto label` syntax instead. | 是 | 继承自 TH13 |
| 13 | jmpEq | o (target) | Pops a number from the stack and if it evaluates to false (in this context, 0), jumps to label %1. [c=orange]Direct usage obsolete. Use if/unless statement instead. | 是 | 继承自 TH13 |
| 14 | jmpNeq | o (target) | Pops a number from the stack and if it evaluates to true (in this context, anything non-0), jumps to label %1. [c=orange]Direct usage obsolete. Use if/unless statement instead. | 是 | 继承自 TH13 |
| 15 | callAsync | m (sub) | Asynchronously calls a given sub. Can take additional parameters to pass as arguments to the sub. [c=orange]Direct usage obsolete. Use `@subName() async` syntax instead. | 是 | 继承自 TH13 |
| 16 | callAsyncId | mS (sub, id) | Asynchronously calls a given sub and assigns it ID %2. Can take additional parameters to pass as arguments to the sub. [c=orange]Direct usage obsolete, use, `@subName() async id` syntax instead. | 是 | 继承自 TH13 |
| 17 | killAsync | S (id) | Ends most recently called sub that has ID %1 (same ID as in ins_16). If no sub with the given ID is found, nothing happens. Using ID -1 can lead to various unexpected results, ranging from deleting the enemy to freezing the game. | 是 | 继承自 TH13 |
| 18 | ins_18 | S (id) | Let `vm` be the most recent async sub running with ID %1: this ins sets `vm[0x000011E4]` to 1. | 否/待确认 | 继承自 TH13 |
| 19 | ins_19 | S (id) | Let `vm` be the most recent async sub running with ID %1: this ins sets `vm[0x000011E4]` to 0. | 否/待确认 | 继承自 TH13 |
| 20 | ins_20 | SS (id, b) | Let `vm` be the most recent async sub running with ID %1: this ins sets `vm[0x0000101C]` to %2. | 否/待确认 | 继承自 TH13 |
| 21 | killAllAsync | — | Ends all running async subs. Calling this in an async sub can lead to unexpected results, such as crashing the game. | 是 | 继承自 TH13 |
| 22 | debug22 | Sm (a, b) | Debug instruction, code does not exist in the release builds of the game. Most likely used to call sub %2 if some variable set in a debug menu is equal to %1. | 是 | 继承自 TH13 |
| 23 | wait | S (time) | Stops sub execution for %1 frames. | 是 | 继承自 TH13 |
| 24 | waitf | f (time) | ins_23, but time is given as a float instead of an int. Subframes do actually exist and affect ins_547. | 是 | 继承自 TH13 |
| 25 | ins_25 | — |  | 否/待确认 | 继承自 TH-1 |
| 26 | ins_26 | — |  | 否/待确认 | 继承自 TH-1 |
| 27 | unknown27 | — |  | 否/待确认 | 继承自 TH-1 |
| 28 | ins_28 | — |  | 否/待确认 | 继承自 TH-1 |
| 29 | ins_29 | — |  | 否/待确认 | 继承自 TH-1 |
| 30 | unknown30 | m (formatString) | Some sort of `printf` debug instruction, which can take additional float/int arguments after %1. Its code does not exist in the release builds. | 是 | 继承自 TH13 |
| 31 | unknown31 | — |  | 否/待确认 | 继承自 TH-1 |
| 32 | ins_32 | — |  | 否/待确认 | 继承自 TH-1 |
| 33 | ins_33 | — |  | 否/待确认 | 继承自 TH-1 |
| 34 | ins_34 | — |  | 否/待确认 | 继承自 TH-1 |
| 35 | ins_35 | — |  | 否/待确认 | 继承自 TH-1 |
| 36 | ins_36 | — |  | 否/待确认 | 继承自 TH-1 |
| 37 | ins_37 | — |  | 否/待确认 | 继承自 TH-1 |
| 38 | ins_38 | — |  | 否/待确认 | 继承自 TH-1 |
| 39 | ins_39 | — |  | 否/待确认 | 继承自 TH-1 |
| 40 | stackAlloc | S (size) | Increases the ECL stack pointer by %1 bytes (probably), to make space for sub variables. [c=orange]Obsolete, thecl generates this instruction automatically. | 是 | 继承自 TH13 |
| 41 | ins_41 | — |  | 否/待确认 | 继承自 TH-1 |
| 42 | pushi | S (num) | Pushes an integer to the ECL stack. [c=orange]Obsolete, push values to stack by writing unassigned expressions instead. | 是 | 继承自 TH13 |
| 43 | seti | S (var) | Pops an integer from the stack into variable %1. [c=orange]Obsolete, use assignment syntax instead. | 是 | 继承自 TH13 |
| 44 | pushf | f (num) | Pushes a float to the ECL stack. [c=orange]Obsolete, push values to stack by writing unassigned expressions instead. | 是 | 继承自 TH13 |
| 45 | setf | f (var) | Pops a float from the stack into variable %1. [c=orange]Obsolete, use assignment syntax instead. | 是 | 继承自 TH13 |
| 46 | ins_46 | — |  | 否/待确认 | 继承自 TH-1 |
| 47 | ins_47 | — |  | 否/待确认 | 继承自 TH-1 |
| 48 | ins_48 | — |  | 否/待确认 | 继承自 TH-1 |
| 49 | ins_49 | — |  | 否/待确认 | 继承自 TH-1 |
| 50 | addi | — | Sums integers on the stack. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 51 | addf | — | Sums floats on the stack. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 52 | subi | — | Subtracts integers on the stack. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 53 | subf | — | Subtracts floats on the stack. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 54 | muli | — | Multiplies integers on the stack. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 55 | mulf | — | Multiplies floats on the stack. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 56 | divi | — | Divides integers on the stack. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 57 | divf | — | Divides floats on the stack. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 58 | modi | — | Modulo operation on integers on the stack. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 59 | eqi | — | Stack integer `==` comparison. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 60 | eqf | — | Stack float `==` comparison. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 61 | neqi | — | Stack integer `!=` comparison. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 62 | neqf | — | Stack float `!=` comparison. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 63 | lessi | — | Stack integer `<` comparison. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 64 | lessf | — | Stack float `<` comparison. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 65 | leqi | — | Stack integer `<=` comparison. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 66 | leqf | — | Stack float `<=` comparison. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 67 | greateri | — | Stack integer `>` comparison. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 68 | greaterf | — | Stack float `>` comparison. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 69 | geqi | — | Stack integer `>=` comparison. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 70 | geqf | — | Stack float `>=` comparison. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 71 | noti | — | Stack integer NOT operation (e.g. !1). [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 72 | notf | — | Stack float NOT operation (e.g. !1.0f). [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 73 | or | — | Logical OR operation on the stack. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 74 | and | — | Logical AND operation on the stack. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 75 | xor | — | Bitwise XOR operation on integers on the stack. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 76 | bit_or | — | Bitwise OR operation on integers on the stack. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 77 | bit_and | — | Bitwise AND operation on integers on the stack. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 78 | deci | S (var) | Pushes variable %1 to the stack and then decrements it. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 79 | stackSin | — | sin operation on a float on the stack. [c=orange]Obsolete, use `sin(floatVal)` instead. | 是 | 继承自 TH13 |
| 80 | stackCos | — | cos operation on a float on the stack. [c=orange]Obsolete, use `cos(floatVal)` instead. | 是 | 继承自 TH13 |
| 81 | mathCirclePos | ffff (varX, varY, ang, radius) | Performs following operation: [code]%1 = cos(%3)*%4;<br>%2 = sin(%3)*%4;[/code] | 是 | 继承自 TH13 |
| 82 | validRad | f (var) | Normalizes angle in %1. | 是 | 继承自 TH13 |
| 83 | negi | — | Negates an integer on the stack. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 84 | negf | — | Negates a float on the stack. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 85 | squareSum | fff (var, x, y) | Performs following operation: [code]%1 = %2*%2 + %3*%3;[/code] | 是 | 继承自 TH13 |
| 86 | squareSumRoot | fff (var, x, y) | Performs following operation: [code]%1 = sqrt(%2*%2 + %3*%3);[/code] | 是 | 继承自 TH13 |
| 87 | mathAngle | fffff (var, x1, y1, x2, y2) | Calculates angle from (%2,%3) to (%4,%5) and stores it in %1. | 是 | 继承自 TH13 |
| 88 | stackSqrt | — | square root operation on a float on the stack. [c=orange]Obsolete, use `sqrt(floatVal)` instead. | 是 | 继承自 TH13 |
| 89 | linearFunc | fff (var, a, x) | Performs following operation: [code]%1 = %2*%3;[/code]<br>(what's the point of making this an instruction, ZUN?) | 是 | 继承自 TH13 |
| 90 | pointRotate | fffff (varX, varY, x, y, rad) | Rotates point (%3,%4) by angle %5 and stores the resulting coordinates in %1 and %2. | 是 | 继承自 TH13 |
| 91 | floatTime | SfSSff (slot, var, time, mode, init, final) | In %3 frames using mode %4, variable %2 changes from %5 to %6. %1 is used to set the slot to be used by this ins, every enemy has 8 slots (0 to 7). | 是 | 继承自 TH13 |
| 92 | math92 | SfSSffff (slot, var, time, mode, init, final, m, n) | Same as ins_91, but takes 2 extra arguments of unknown meaning. Needs investigation. | 否/待确认 | 继承自 TH13 |
| 93 | math93 | ffff (varX, varY, r1, r2) | Gets a random point based on %3 and %4 and stores it on (%1,%2). Needs investigation. | 否/待确认 | 继承自 TH13 |

### TH16.5 指令：敌机创建与 ANM 管理 / Enemy creation and ANM script management

| ID | 助记名 | 参数 | 说明 | 文档化 | 来源 |
| --- | --- | --- | --- | --- | --- |
| 300 | enmCreate | mffSSS (sub, x, y, hp, score, item) | Creates an enemy using subroutine %1 at coordinates %2, %3 (relative to position of enemy that called it), health of created enemy is %4, score bonus is %5 and item drop is %6. | 是 | 继承自 TH13 |
| 301 | enmCreateA | mffSSS (sub, x, y, hp, score, item) | Creates an enemy using subroutine %1 at coordinates %2, %3 (absolute position), health of created enemy is %4, score bonus is %5 and item drop is %6. | 是 | 继承自 TH13 |
| 302 | anmSelect | S (anmIndex) | Selects ANM file to be used by other instructions based on %1. | 是 | 继承自 TH13 |
| 303 | anmSetSprite | SS (slot, script) | Loads script %2 from ANM selected with ins_302 on slot %1. | 是 | 继承自 TH13 |
| 304 | enmCreateM | mffSSS (sub, x, y, hp, score, item) | Creates a mirrored enemy using subroutine %1 at coordinates %2, %3 (relative to caller's position), health of created enemy is %4, score bonus is %5 and item drop is %6. | 是 | 继承自 TH13 |
| 305 | enmCreateAM | mffSSS (sub, x, y, hp, score, item) | Creates an mirrored enemy using subroutine %1 at coordinates %2, %3 (absolute position), health of created enemy is %4, score bonus is %5 and item drop is %6. | 是 | 继承自 TH13 |
| 306 | anmSetMain | SS (slot, script) | Loads script %2 from ANM selected with ins_302 on slot %1. However, the script number provided will only be used when the enemy is not moving. When moving left %2+1 will be used, right %2+2, diagonal left %2+3, diagonal right %2+4. Might not work properly if %1 is not 0 according to THBWiki. | 是 | 继承自 TH13 |
| 307 | anmPlay | SS (anmIndex, script) | From ANM file selected based on %1, play script %2 at caller's current coordinates. The spawned script is completely independent, and will continue existing even if caller is deleted. | 是 | 继承自 TH13 |
| 308 | anmPlayAbs | SS (anmIndex, script) | From ANM file selected based on %1, play script %2 at coordinates (0, 0). The spawned script is completely independent, and will continue existing even if caller is deleted. | 是 | 继承自 TH13 |
| 309 | enmCreateF | mffSSS (sub, x, y, hp, score, item) | Creates a filler enemy using subroutine %1 at coordinates %2, %3 (relative to caller's position), health of created enemy is %4, score bonus is %5 and item drop is %6. | 是 | 继承自 TH13 |
| 310 | enmCreateAF | mffSSS (sub, x, y, hp, score, item) | Creates a filler enemy using subroutine %1 at coordinates %2, %3 (absolute position), health of created enemy is %4, score bonus is %5 and item drop is %6. | 是 | 继承自 TH13 |
| 311 | enmCreateMF | mffSSS (sub, x, y, hp, score, item) | Creates a mirrored filler enemy using subroutine %1 at coordinates %2, %3 (relative to caller's position), health of created enemy is %4, score bonus is %5 and item drop is %6. | 是 | 继承自 TH13 |
| 312 | enmCreateAMF | mffSSS (sub, x, y, hp, score, item) | Creates a mirrored filler enemy using subroutine %1 at coordinates %2, %3 (absolute position), health of created enemy is %4, score bonus is %5 and item drop is %6. | 是 | 继承自 TH13 |
| 313 | anmSelectedPlay | S (script) | Same as ins_307, except it uses the ANM file selected by ins_302. | 是 | 继承自 TH13 |
| 314 | anmPlayHigh | SS (anmIndex, script) | Same as ins_307, except it spawns the ANM with a higher layer? Needs further investigation. | 否/待确认 | 继承自 TH13 |
| 315 | anmPlayRotate | SSf (anmIndex, script, angle) | Same as ins_307, except it sets rotation of spawned ANM to %3. | 是 | 继承自 TH13 |
| 316 | anm316 | SS (a, b) | Unknown. | 否/待确认 | 继承自 TH13 |
| 317 | anmSwitch | SS (slot, switch) | Sets the execution pointer of ANM script on slot %1 to where ANM `ins_5(a)` with `a` == `switch` is (the time is also changed to match time of `ins_5`). Doesn't work if the value is 0 apparently? | 是 | 继承自 TH13 |
| 318 | anmReset | — | Resets some ANM-related parameters of the caller (TODO: what exactly?) | 是 | 继承自 TH13 |
| 319 | anmRotate | Sf (slot, r) | Set rotation of an ANM script on slot %1 to %2. | 是 | 继承自 TH13 |
| 320 | anmMove | Sff (slot, x, y) | Set position of an ANM script on slot %1 to (%2,%3). This does not detach the script from the caller, so the actual position of the script will be position of the caller + position set here. | 是 | 继承自 TH13 |
| 321 | enmMapleEnemy | mffSSS (sub, x, y, hp, score, item) | ins_300, but used by 'MapleEnemy' (TODO: what's the difference from ins_300?) | 是 | 继承自 TH13 |
| 322 | enm322 | SS (a, b) | Unknown. | 否/待确认 | 继承自 TH13 |
| 323 | deathAnm | SS (anmIndex, script) | Set the animation that will play when the enemy dies to script %2 from ANM file specified by %1. | 是 | 继承自 TH13 |
| 324 | enm324 | — | Unknown. | 否/待确认 | 继承自 TH13 |
| 325 | anmColor | SSSS (slot, R, G, B) | Modify color of ANM script on slot %1, %2, %3, [c=lightblue]%4 correspond to individual colors and have to be from 0 to 255. | 是 | 继承自 TH13 |
| 326 | anmColorTime | SSSSSS (slot, time, mode, R, G, B) | Same as ins_325, but the change is applied in %2 frames using mode %3. | 是 | 继承自 TH13 |
| 327 | anmAlpha | SS (slot, alpha) | Sets alpha of ANM script on slot %1 to %2 (must be a value between 0-255) | 是 | 继承自 TH13 |
| 328 | anmAlphaTime | SSSS (slot, time, mode, alpha) | Same as ins_327, but the change is applied in %2 frames using mode %3. | 是 | 继承自 TH13 |
| 329 | anmScale | Sff (slot, w, h) | Sets horizontal and vertical scaling of ANM script on slot %1 to %2 and %3 respectively. Overwrites scaling properties set by the ANM script. | 是 | 继承自 TH13 |
| 330 | anmScaleTime | SSSff (slot, time, mode, w, h) | Same as ins_329, but the change is applied in %2 frames using mode %3. | 是 | 继承自 TH13 |
| 331 | anmAlpha2 | SS (slot, alpha) | Sets alpha2 (opacity of the gradient) of ANM script on slot %1 to %2. | 是 | 继承自 TH13 |
| 332 | anmAlpha2Time | SSSS (slot, time, mode, alpha) | Same as ins_331, but the change is applied in %2 frames using mode %3. | 是 | 继承自 TH13 |
| 333 | anm333 | SSSff (a, b, c, r, s) | Unknown. Might be doing something to ANM script on slot %1. | 否/待确认 | 继承自 TH13 |
| 334 | anm334 | S (a) | Hard to tell? THBWiki Google translate gives this: 'The animation effect of the playing unit (enemy), the lightning effect near the evil spirit ball of the god temple', which might be referring to lightning around Nue in TD extra stage. | 否/待确认 | 继承自 TH13 |
| 335 | anmScale2 | Sff (slot, w, h) | Same as ins_329, except it doesn't overwrite the scaling set by the ANM script - instead, it multiplies it. | 是 | 继承自 TH13 |
| 336 | anmLayer | SS (slot, layer) | Set layer of ANM script on slot %1 to %2. | 是 | 继承自 TH14 |
| 337 | anmBlendMode | SS (slot, b) | Set blend mode of ANM script on slot %1 to %2 (TODO: make a list of blend modes). | 是 | 继承自 TH16 |
| 338 | anmPlayPos | SSfff (anmIndex, script, x, y, z) | Same as ins_307, but the spawned script is offset by (%3,%4). For 3D objects, %5 is used too (TODO: verify that). | 是 | 继承自 TH16 |
| 339 | anm339 | SSS (a, b, c) | Unknown. Might be doing something to ANM script on slot %1. | 否/待确认 | 继承自 TH16 |
| 340 | enmDelete | S (id) | Delete enemy with the given ID. | 是 | 继承自 TH16 |

### TH16.5 指令：移动管理 / Movement management

| ID | 助记名 | 参数 | 说明 | 文档化 | 来源 |
| --- | --- | --- | --- | --- | --- |
| 400 | movePos | ff (x, y) | Sets caller's absolute position to %1, %2. | 是 | 继承自 TH13 |
| 401 | movePosTime | SSff (time, mode, x, y) | Same as ins_400, but the change is applied in %1 frames using mode %2. | 是 | 继承自 TH13 |
| 402 | movePosRel | ff (x, y) | Sets caller's relative position to %1, %2. | 是 | 继承自 TH13 |
| 403 | movePosRelTime | SSff (time, mode, x, y) | Same as ins_402, but the change is applied in %1 frames using mode %2. | 是 | 继承自 TH13 |
| 404 | moveVel | ff (r, spd) | Sets caller's absolute movement angle to %1 and speed to %2. | 是 | 继承自 TH13 |
| 405 | moveVelTime | SSff (time, mode, r, spd) | Same as ins_404, but the change is applied in %1 frames using mode %2. | 是 | 继承自 TH13 |
| 406 | moveVelRel | ff (r, spd) | Sets caller's relative movement angle to %1 and speed to %2. | 是 | 继承自 TH13 |
| 407 | moveVelRelTime | SSff (time, mode, r, spd) | Same as ins_406, but the change is applied in %1 frames using mode %2. | 是 | 继承自 TH13 |
| 408 | moveCircle | ffff (θ, spd, rad, radInc) | Sets caller's absolute circle movement: %1 is the angle indicating initial position on the circle, %2 is the angular velocity, %3 is circle radius and %4 is by how much the radius increases each frame. | 是 | 继承自 TH13 |
| 409 | moveCircleTime | SSfff (time, mode, spd, rad, radInc) | Same as ins_408, but the change is applied in %1 frames using mode %2. There is also no initial angle parameter here for obvious reason. | 是 | 继承自 TH13 |
| 410 | moveCircleRel | ffff (θ, spd, rad, radInc) | Sets caller's relative circle movement: %1 is the angle indicating initial position on the circle, %2 is the angular velocity, %3 is circle radius and %4 is by how much the radius increases each frame. | 是 | 继承自 TH13 |
| 411 | moveCircleRelTime | SSfff (time, mode, spd, rad, radInc) | Same as ins_410, but the change is applied in %1 frames using mode %2. There is also no initial angle parameter here for obvious reason. | 是 | 继承自 TH13 |
| 412 | moveRand | SSf (time, mode, spd) | Randomizes caller's absolute angle and sets absolute speed to %3. The speed changes back to 0 in %1 frames using mode %2. | 是 | 继承自 TH13 |
| 413 | moveRandRel | SSf (time, mode, spd) | Randomizes caller's relative angle and sets relative speed to %3. The speed changes back to 0 in %1 frames using mode %2. | 是 | 继承自 TH13 |
| 414 | moveBoss | — | Sets caller's absolute position to the absolute position of the boss. If called without a boss, [tip=Google translated from THBWiki, I find this sentence funny]it will cause serious mis-access and explode[/tip]. | 是 | 继承自 TH13 |
| 415 | moveBossRel | — | Sets caller's relative position to the relative position of the boss. If called without a boss, [tip=Google translated from THBWiki, I find this sentence funny]it will cause serious mis-access and explode[/tip]. | 是 | 继承自 TH13 |
| 416 | movePos3d | fff (x, y, z) | Same as ins_400, but takes a %3 parameter for the third dimension, which probably affects 3D ANM scripts used by the caller, or something. | 是 | 继承自 TH13 |
| 417 | movePos3dRel | fff (x, y, z) | Same as ins_402, but takes a %3 parameter for the third dimension, which probably affects 3D ANM scripts used by the caller, or something. | 是 | 继承自 TH13 |
| 418 | moveAdd | ff (x, y) | Increases caller's absolute position by %1 and %2. | 是 | 继承自 TH13 |
| 419 | move419 | ff (x, y) | While the code of this ins looks like it's supposed to be a relative version of ins_418, it doesn't seem to behave like that... | 否/待确认 | 继承自 TH13 |
| 420 | moveEllipse | ffffff (θ, spd, rad, radInc, ellDir, ellRatio) | Sets caller's absolute ellipse movement: %1 is the angle indicating initial position on the ellipse, %2 is the angular velocity, %3 is the base circle radius and %4 is by how much the radius increases each frame. %6 is how much the base circle should be 'squished' to make it an ellipse, and %5 is the squishing angle (I don't know math terms in English, sorry) | 是 | 继承自 TH13 |
| 421 | moveEllipseTime | SSfffff (time, mode, spd, rad, radInc, ellDir, ellRatio) | Same as ins_420, but the change is applied in %1 frames using mode %2. There is also no initial angle parameter here for obvious reason | 是 | 继承自 TH13 |
| 422 | moveEllipseRel | ffffff (θ, spd, rad, radInc, ellDir, ellRatio) | Sets caller's relative ellipse movement: %1 is the angle indicating initial position on the ellipse, %2 is the angular velocity, %3 is the base circle radius and %4 is by how much the radius increases each frame. %6 is how much the base circle should be 'squished' to make it an ellipse, and %5 is the squishing angle (I don't know math terms in English, sorry) | 是 | 继承自 TH13 |
| 423 | moveEllipseRelTime | SSfffff (time, mode, spd, rad, radInc, ellDir, ellRatio) | Same as ins_422, but the change is applied in %1 frames using mode %2. There is also no initial angle parameter here for obvious reason | 是 | 继承自 TH13 |
| 424 | moveSetMirror | S (state) | Sets caller's mirror flag to %1. | 是 | 继承自 TH13 |
| 425 | moveBezier | Sffffff (time, x1, y1, x2, y2, x3, y3) | In %1 frames, the enemy moves towards (%2,%3), then moves towards (%6,%7) for a while and finally moves to (%4,%5). Uses absolute position.<br>From THBWiki: <br>(assuming the current coordinates are (x0, y0)) the motion trajectory is actually a Bezier curve from (x0, y0) to (x2, y2);<br>The P1 coordinate of the curve is `((x1-x0)*1/3, (y1-y0)*1/3)`;<br>The P2 coordinate of the curve is `(-(x3-x2)*1/3+x2,-(y3-y2) *1/3+x2)` | 是 | 继承自 TH13 |
| 426 | moveBezierRel | Sffffff (time, x1, y1, x2, y2, x3, y3) | Same as ins_425, but uses relative position. | 是 | 继承自 TH13 |
| 427 | moveReset | — | Resets some movement-related parameters (TODO: what exactly?) | 否/待确认 | 继承自 TH13 |
| 428 | moveVelNM | ff (r, spd) | Same as ins_404, but ignores the mirror flag. | 是 | 继承自 TH13 |
| 429 | moveVelNMTime | SSff (time, mode, r, spd) | Same as ins_405, but ignores the mirror flag. | 是 | 继承自 TH13 |
| 430 | moveVelNMRel | ff (r, spd) | Same as ins_406, but ignores the mirror flag. | 是 | 继承自 TH13 |
| 431 | moveVelNMRelTime | SSff (time, mode, r, spd) | Same as ins_407, but ignores the mirror flag. | 是 | 继承自 TH13 |
| 432 | moveEnm | S (id) | Sets caller's absolute position to absolute position of enemy with var_-9914 == %1. | 是 | 继承自 TH13 |
| 433 | moveEnmRel | S (id) | Sets caller's relative position to relative position of enemy with var_-9914 == %1. | 是 | 继承自 TH13 |
| 434 | moveCurve | SSSff (time, mode, c, x, y) | In %1 frames using mode %2, caller's absolute position is changed to (%4,%5). The movement trajectory is a curve based on %3, it is unknown how it works exactly. | 否/待确认 | 继承自 TH13 |
| 435 | moveCurveRel | SSSff (time, mode, c, x, y) | In %1 frames using mode %2, caller's relative position is changed to (%4,%5). The movement trajectory is a curve based on %3, it is unknown how it works exactly. | 否/待确认 | 继承自 TH13 |
| 436 | moveAddTime | SSff (time, mode, x, y) | Same as ins_418, but the change is applied in %1 frames using mode %2. | 是 | 继承自 TH13 |
| 437 | moveAddRelTime | SSff (time, mode, x, y) | Same as ins_419, but the change is applied in %1 frames using mode %2 (it also behaves as expected, unlike ins_419). | 是 | 继承自 TH13 |
| 438 | moveCurveAdd | SSSff (time, mode, c, x, y) | Same as ins_434, but instead caller's current absolute coordinates are added to %4 and %5. | 是 | 继承自 TH13 |
| 439 | moveCurveAddRel | SSSff (time, mode, c, x, y) | Same as ins_435, but instead caller's current relative coordinates are added to %4 and %5. | 是 | 继承自 TH13 |
| 440 | moveAngle | f (r) | Sets caller's absolute movement angle to %1. | 是 | 继承自 TH14 |
| 441 | moveAngleTime | SSf (time, mode, r) | Same as ins_440, but the change is applied in %1 frames using mode %2. | 是 | 继承自 TH14 |
| 442 | moveAngleRel | f (r) | Sets caller's relative movement angle to %1. | 是 | 继承自 TH14 |
| 443 | moveAngleRelTime | SSf (time, mode, r) | Same as ins_442, but the change is applied in %1 frames using mode %2. | 是 | 继承自 TH14 |
| 444 | moveSpeed | f (spd) | Sets caller's absolute movement speed to %1. | 是 | 继承自 TH14 |
| 445 | moveSpeedTime | SSf (time, mode, spd) | Same as ins_444, but the change is applied in %1 frames using mode %2. | 是 | 继承自 TH14 |
| 446 | moveSpeedRel | f (spd) | Sets caller's relative movement speed to %1. | 是 | 继承自 TH14 |
| 447 | moveSpeedRelTime | SSf (time, mode, spd) | Same as ins_446, but the change is applied in %1 frames using mode %2. | 是 | 继承自 TH14 |

### TH16.5 指令：敌机属性与杂项 / Enemy property management and other miscellaneous things

| ID | 助记名 | 参数 | 说明 | 文档化 | 来源 |
| --- | --- | --- | --- | --- | --- |
| 500 | setHurtbox | ff (w, h) | Sets caller's hurtbox width to %1 and height to %2. | 是 | 继承自 TH13 |
| 501 | setHitbox | ff (w, h) | Sets caller's hitbox width to %1 and height to %2. | 是 | 继承自 TH13 |
| 502 | flagSet | S (n) | Sets flag(s) according to %1. Refer to the [flag table](#s=modding/flags) for exact values. | 是 | 继承自 TH13 |
| 503 | flagClear | S (n) | Clears flag(s) according to %1. Refer to the [flag table](#s=modding/flags) for exact values. | 是 | 继承自 TH13 |
| 504 | moveLimit | ffff (x, y, w, h) | Sets caller's movement limit rectangle: (%1,%2) are the coordinates of the center of the rect, while %3, %4 are width and height of it. | 是 | 继承自 TH13 |
| 505 | moveLimitReset | — | Removes caller's movement limit. | 是 | 继承自 TH13 |
| 506 | dropClear | — | Clears caller's extra item drop. | 是 | 继承自 TH13 |
| 507 | dropExtra | SS (type, amount) | Adds %2 items of type %1 to caller's extra drop. Item type table will be made in the future. | 是 | 继承自 TH13 |
| 508 | dropArea | ff (w, h) | Sets caller's item drop area width to %1 and height to %2. | 是 | 继承自 TH13 |
| 509 | dropItems | — | Drops all items the caller has. Has no effect in spell practice. | 是 | 继承自 TH13 |
| 510 | dropMain | S (type) | Sets caller's main drop to %1. | 是 | 继承自 TH13 |
| 511 | lifeSet | S (hp) | Sets caller's current HP and max HP to %1. | 是 | 继承自 TH13 |
| 512 | setBoss | S (a) | If %1 is 0, activates boss mode and makes the caller the main boss. If %1 > 0, it makes the caller the secondary boss. If %1 is -1, ends boss mode. | 是 | 继承自 TH13 |
| 513 | timerReset | — | Resets boss timer. | 是 | 继承自 TH13 |
| 514 | setInterrupt | SSSm (slot, hp, time, sub) | Sets an interrupt on slot %1 (not sure how many slots there are) - once caller's hp reaches %2 or %3 frames have passed since this was called, caller will terminate all subs it's currently running and execute sub %4. | 是 | 继承自 TH13 |
| 515 | setInvuln | S (time) | Makes the caller completely invulnerable for %1 frames. | 是 | 继承自 TH13 |
| 516 | playSound | S (id) | Plays sound %1. Sound id table will be added in the future. | 是 | 继承自 TH13 |
| 517 | setScreenShake | SSS (time, startIntensity, endIntensity) | Activates screen shake for %1 frames. %2 is the starting intensity and %3 is the ending intensity. The larger the intensity, the more the screen shakes. | 是 | 继承自 TH13 |
| 518 | dialogRead | S (dialogueId) | Starts a dialogue, %1 is the ID of an entry in the .msg file. Apart from that, has the effect ins_525. | 是 | 继承自 TH13 |
| 519 | dialogWait | — | Waits until there are no dialogues active, or the running .msg script calls a certain instruction (which one?) | 否/待确认 | 继承自 TH13 |
| 520 | unknown520 | — | Waits until there are no boss enemies. | 是 | 继承自 TH13 |
| 521 | setTimeout | Sm (slot, sub) | Sets a timeout interrupt on slot %1 - when the timer reaches 0, caller will terminate all subs it's currently running and execute sub %2. | 是 | 继承自 TH13 |
| 522 | spellEx | SSSm (id, time, type, name) | Same as ins_537, but the difficulty number is NOT added to the id. | 是 | 继承自 TH16 |
| 523 | spellEnd | — | Ends currently active spellcard. | 是 | 继承自 TH13 |
| 524 | setChapter | S (a) | Some jank that's responsible for showing boss name and possibly other things. In LoLK, it also ends the current chapter and begins a new one. | 否/待确认 | 继承自 TH13 |
| 525 | enmKillAll | — | Kills all other enemies (unless they have a flag that prevents that set). | 是 | 继承自 TH13 |
| 526 | etProtectRange | f (r) | Makes bullets generated by the caller not spawn if they are in radius %1 around the player. | 是 | 继承自 TH13 |
| 527 | lifeMarker | SfS (slot, hp, c) | Sets a new life marker on slot %1, %2 determines where the marker will appear on the health bar (if %2=1000.0f and the enemy has 2000 hp, the marker will split the hp bar in half). %3 is an RGB value of unknown use (possibly leftover from earlier ECL versions) | 是 | 继承自 TH13 |
| 528 | spellUnused | SSSm (id, time, type, name) | No difference from ins_522, unused. | 是 | 继承自 TH16 |
| 529 | rankF3 | ffff (var, a, b, c) | Sets %1 to %2 if rank is low, %3 if rank is average or %4 if rank is high. | 是 | 继承自 TH13 |
| 530 | rankF5 | ffffff (var, a, b, c, d, e) | Sets %1 to %2 if rank is very low, %3 if rank is low, %4 if rank is average, %5 if rank is high or %6 if rank is very high. | 是 | 继承自 TH13 |
| 531 | rankF2 | fff (var, a, b) | Sets %1 to %2 if rank is low or %3 if rank is high. | 是 | 继承自 TH13 |
| 532 | rankI3 | SSSS (var, a, b, c) | Sets %1 to %2 if rank is low, %3 if rank is average or %4 if rank is high. | 是 | 继承自 TH13 |
| 533 | rankI5 | SSSSSS (var, a, b, c, d, e) | Sets %1 to %2 if rank is very low, %3 if rank is low, %4 if rank is average, %5 if rank is high or %6 if rank is very high. | 是 | 继承自 TH13 |
| 534 | rankI2 | SSS (var, a, b) | Sets %1 to %2 if rank is low or %3 if rank is high. | 是 | 继承自 TH13 |
| 535 | diffI | SSSSS (var, E, N, H, L) | Sets %1 to one of values provided based on difficulty. | 是 | 继承自 TH13 |
| 536 | diffF | fffff (var, E, N, H, L) | Sets %1 to one of values provided based on difficulty. | 是 | 继承自 TH13 |
| 537 | spell | SSSm (id, time, mode, name) | Declares a spellcard with id %1 and name %4. The actual ID passed to the spell-creating function is `id + difficulty`, with easy=0, normal=1, hard=2, lunatic=3, ex=4, overdrive=5. <br>%2 determines how much time the spell circle takes to shrink (in frames), as well as how fast the spell bonus decreases. The exact formula is as follows: <br>[code] int factor = maxSCB >> 2; // maxSCB is hardcoded<br> currSCB -= (maxSCB - factor) / (%2 - 300);<br> currSCB -= currSCB % 10; [/code] <br>As you can guess, setting %2 to 300 causes a division by 0 error and crashes the game, while setting it to a value smaller than 300 causes the SCB to increase over time, instead of decreasing. %3 TBD, it's not unused. | 是 | 继承自 TH16 |
| 538 | spell2 | SSSm (id, time, mode, name) | Same as ins_537, except the ID used it `id - 1 + difficulty`. | 是 | 继承自 TH16 |
| 539 | spell3 | SSSm (id, time, mode, name) | Same as ins_537, except the ID used it `id - 2 + difficulty`. | 是 | 继承自 TH16 |
| 540 | stars | S (cnt) | Sets the amount of stars displayed in the top left corner. Stars might not appear at all if there is no boss active. | 是 | 继承自 TH13 |
| 541 | noHitboxDur | S (time) | Disables the hitbox (but not the hurtbox) for the given amount of frames. | 是 | 继承自 TH13 |
| 542 | spellTimeout | — | Makes the current spell a timeout spell (prevent spell bonus from decreasing, give capture bonus if timed out). | 是 | 继承自 TH13 |
| 543 | unknown543 | — | Unknown. | 否/待确认 | 继承自 TH13 |
| 544 | unknown544 | S (a) | Unknown, sets or clears some flag? | 否/待确认 | 继承自 TH13 |
| 545 | laserCancel | — | Cancels all lasers. | 是 | 继承自 TH13 |
| 546 | bombShield | SS (a, script) | Sets the bomb invulnerability flag (%1=1 set, %1=0 not set), the caller's ANM script will change to %2 when a bomb is active (how does it work with ANM slots exactly?) | 是 | 继承自 TH13 |
| 547 | gameSpeed | f (s) | Sets game speed to %1 of the normal speed. In ISC, enemies with flag 13 (dec=8192) set will ignore effects of this opcode. | 是 | 继承自 TH13 |
| 548 | diffWait | SSSS (e, n, h, l) | Same as ins_23, but the wait time is chosen from the given 4 based on the difficulty. | 是 | 继承自 TH13 |
| 549 | unknown549 | S (a) | Unknown. | 否/待确认 | 继承自 TH13 |
| 550 | unknown550 | S (a) | Unknown. | 否/待确认 | 继承自 TH13 |
| 551 | unknown551 | S (a) | Unknown. | 否/待确认 | 继承自 TH13 |
| 552 | zIndex | S (layers) | Increases layer of all ANM scripts used by the caller by %1. | 是 | 继承自 TH13 |
| 553 | hitSound | S (id) | Makes the caller play sound %1 when hit. Sound id table will be added in the future. | 是 | 继承自 TH13 |
| 554 | stageLogo | — | Shows the stage logo from an ANM of a hardcoded name. | 是 | 继承自 TH13 |
| 555 | enmAlive | SS (var, id) | Checks if enemy of var_-9914 == %2 is still alive, and sets %1 to 1 if it is or 0 if it isn't. | 是 | 继承自 TH13 |
| 556 | setDeath | m (sub) | Makes the caller execute sub %1 when the HP reaches 0. Keep in mind that the caller is already marked for deletion at the point when the sub actually executes, so if you put waiting there the sub will not execute fully (because the caller will be deleted) | 是 | 继承自 TH13 |
| 557 | fogTime | SSSff (time, mode, color, start, end) | Same as STD ins_9, that is, fogTime. Refer to [the STD instruction table](#s=modding/std-ins) for details. | 是 | 继承自 TH13 |
| 558 | flagMirror | S (state) | Literally the exact same instruction as ins_424. | 是 | 继承自 TH13 |
| 559 | enmLimit | S (limit) | Set the maximum number of enemies that can be present. New enemies will fail to spawn if the cap is reached. Default is 99999. | 是 | 继承自 TH13 |
| 560 | unknown560 | ff (r, s) | Unknown. | 否/待确认 | 继承自 TH13 |
| 561 | die | — | Makes the caller execute the sub set with ins_556. If there is no such sub set, the caller dies instead (exactly the same as if the player shot down the caller, that is, items are dropped, death sound plays etc) | 是 | 继承自 TH13 |
| 562 | dropItemsSp | — | Same as ins_509, but item spawning will not be blocked in spell practice. | 是 | 继承自 TH13 |
| 563 | unknown563 | S (flagState) | Sets [flag 12](#s=modding/flags) (decimal 4096), which controls whether the hitbox and hurtbox is a rectangle. If %1 is 1, collision is a rectangle. If %1 is 0, collision is elliptical. | 是 | 继承自 TH14 |
| 564 | hitboxRotate | f (angle) | Rotates the hitbox and hurtbox of the enemy (note: the hitbox rotation is really janky, but hurtbox rotates fine). Has no effect unless the enemy uses rectangular collision. | 是 | 继承自 TH14 |
| 565 | bombInvuln | f (red) | Sets caller's damage reduction when a bomb is active, 0.0f means no damage at all, 1.0f is full damage, negative values will make the enemy heal when you bomb. | 是 | 继承自 TH14 |
| 566 | unknown566 | () | Unknown (does it even exist?) | 否/待确认 | 继承自 TH14 |
| 567 | unknown567 | S (a) | Unknown. | 否/待确认 | 继承自 TH14 |
| 568 | spellMode | S (state) | Enables/disables spell card damage reduction, if %1 is 1 it's enabled, if it's 0 it's disabled. Can be used outside of spell cards. | 是 | 继承自 TH14 |
| 569 | unknown569 | S (a) | Unknown. | 否/待确认 | 继承自 TH15 |
| 570 | unknown570 | — | Unknown. | 否/待确认 | 继承自 TH15 |
| 571 | unknown571 | — | Unknown. | 否/待确认 | 继承自 TH15 |
| 572 | lifeNow | S (hp) | Sets caller's current HP to %1, without changing max HP. | 是 | 继承自 TH16 |

### TH16.5 指令：子弹创建与删除 / Bullet creation and deletion

| ID | 助记名 | 参数 | 说明 | 文档化 | 来源 |
| --- | --- | --- | --- | --- | --- |
| 600 | etNew | S (etId) | Resets bullet manager %1 to default properties. | 是 | 继承自 TH13 |
| 601 | etOn | S (etId) | Shoots bullet(s) using properties from bullet manager %1. | 是 | 继承自 TH13 |
| 602 | etSprite | SSS (etId, type, color) | Sets bullet type and color of bullet manager %1. Refer to [this image](https://cdn.discordapp.com/attachments/395767870119870466/570658618316161041/BULLET_IDS.png) made by Dai. Remarks:<br>- bullet types 35 and 36 spin<br>- type 30 pulses<br>- the difference between 16/37 is the spin direction (same case for 23 and 24) | 是 | 继承自 TH15 |
| 603 | etOffset | Sff (etId, x, y) | Sets the relative offset of bullets spawned by bullet manager %1 to (%2,%3). | 是 | 继承自 TH13 |
| 604 | etAngle | Sff (etId, angle1, angle2) | Sets angle1 and angle2 of bullet manager %1. | 是 | 继承自 TH13 |
| 605 | etSpeed | Sff (etId, speed1, speed2) | Sets speed1 and speed2 of bullet manager %1. | 是 | 继承自 TH13 |
| 606 | etCount | SSS (etId, count1, count2) | Sets count1 and count2 of bullet manager %1. | 是 | 继承自 TH13 |
| 607 | etAim | SS (etId, aim) | Sets aim mode of bullet manager %1. | 是 | 继承自 TH13 |
| 608 | etSound | SSS (etId, sound1, sound2) | Sets sound1 and sound2 of bullet manager %1 (sound effect table is TODO). sound1 plays when the bullet manager fires a bullet, while sound2 plays when a bullet fired by the bullet manager does certain transformations. Set to -1 for no sound. | 是 | 继承自 TH13 |
| 609 | etExSet | SSSSSSff (etId, index, async, type, a, b, r, s) | Sets bullet transformation of bullet manager %1, transformation explanation will be added in the future. | 是 | 继承自 TH13 |
| 610 | etExSet2 | SSSSSSSSffff (etId, index, async, type, a, b, c, d, r, s, m, n) | Same as ins_609, but takes more arguments for certain transformation types. | 是 | 继承自 TH13 |
| 611 | etEx | SSSSSff (etId, async, type, a, b, r, s) | Adds bullet transformation to bullet manager %1, transformation explanation will be added in the future. | 是 | 继承自 TH13 |
| 612 | etEx2 | SSSSSSSffff (etId, async, type, a, b, c, d, r, s, m, n) | Same as ins_611, but takes more arguments for certain transformation types. | 是 | 继承自 TH13 |
| 613 | etClearAll | — | Clears all bullets. | 是 | 继承自 TH13 |
| 614 | etCopy | SS (etIdDest, etIdSrc) | Copies everything from bullet manager %2 into bullet manager %1. Warning: this instruction is partially broken and does NOT copy the index next ins_611/ins_612 transformations will be added at. | 是 | 继承自 TH13 |
| 615 | etCancel | f (r) | Clears all bullets in a circle of radius %1 around the caller, and turns them into cancel items. | 是 | 继承自 TH13 |
| 616 | etClear | f (r) | Clears all bullets in a circle of radius %1 around the caller without turning them into cancel items. | 是 | 继承自 TH13 |
| 617 | etSpeedR3 | Sffffff (etId, spd1l, spd1m, spd1h, spd2l, spd2m, spd2h) | Sets speed1 and speed2 of bullet manager %1 to two of the values provided, based on ingame rank (l=low, m=medium, h=high) | 是 | 继承自 TH13 |
| 618 | etSpeedR5 | Sffffffffff (etId, spd1l, spd1ml, spd1m, spd1mh, spd1h, spd2l, spd2ml, spd2m, spd2mh, spd2h) | Sets speed1 and speed2 of bullet manager %1 to two of the values provided, based on ingame rank (l=low, ml=medium-low, m=medium, mh=medium-high, h=high) | 是 | 继承自 TH13 |
| 619 | etSpeedR2 | Sffff (etId, spd1l, spd1h, spd2l, spd2h) | Sets speed1 and speed2 of bullet manager %1 to two of the values provided, based on ingame rank (l=low, h=high) | 是 | 继承自 TH13 |
| 620 | etCountR3 | SSSSSSS (etId, cnt1l, cnt1m, cnt1h, cnt2l, cnt2m, cnt2h) | Sets count1 and count2 of bullet manager %1 to two of the values provided, based on ingame rank (l=low, m=medium, h=high) | 是 | 继承自 TH13 |
| 621 | etCountR5 | SSSSSSSSSSS (etId, cnt1l, cnt1ml, cnt1m, cnt1mh, cnt1h, cnt2l, cnt2ml, cnt2m, cnt2mh, cnt2h) | Sets count1 and count2 of bullet manager %1 to two of the values provided, based on ingame rank (l=low, ml=medium-low, m=medium, mh=medium-high, h=high) | 是 | 继承自 TH13 |
| 622 | etCountR2 | SSSSS (etId, cnt1l, cnt1h, cnt2l, cnt2h) | Sets count1 and count2 of bullet manager %1 to two of the values provided, based on ingame rank (l=low, h=high) | 是 | 继承自 TH13 |
| 623 | angleToPlayer | fff (var, x, y) | Gets angle to the player from coordinates (%2,%3) and stores it in %1. | 是 | 继承自 TH13 |
| 624 | etSpeedD | Sffffffff (etId, spd1e, spd1n, spd1h, spd1l, spd2e, spd2n, spd2h, spd2l) | Sets speed1 and speed2 of bullet manager %1 to 2 of the values provided, based on the difficulty (e=easy, n=normal, h=hard, l=lunatic) | 是 | 继承自 TH13 |
| 625 | etCountD | SSSSSSSSS (etId, cnt1e, cnt1n, cnt1h, cnt1l, cnt2e, cnt2n, cnt2h, cnt2l) | Sets count1 and count2 of bullet manager %1 to 2 of the values provided, based on the difficulty (e=easy, n=normal, h=hard, l=lunatic) | 是 | 继承自 TH13 |
| 626 | etOffsetRad | Sff (etId, angle, radius) | Sets the relative offset of bullets spawned by bullet manager %1 to (cos(%2)\*%3,sin(%2)\*%3). Stacks with ins_603. | 是 | 继承自 TH13 |
| 627 | etDist | Sf (etId, dist) | Sets distance of bullets spawned by bullet manager %1 to %2 (that is, when a bullet is spawned it moves by %2 using its current angle). | 是 | 继承自 TH13 |
| 628 | etOffsetAbs | Sff (etId, x, y) | Sets the absolute offset of bullets spawned by bullet manager %1 to (%2,%3). | 是 | 继承自 TH13 |
| 629 | fog | fS (r, color) | Sets caller's fog's radius to %1 and color to %2 (RGB value in reverse order). This resets the fog completely, that is, every time it's called the fog spawn animation plays. | 是 | 继承自 TH13 |
| 630 | callSTD | S (switch) | Sets execution pointer of the STD script to where STD ins_16(%1) is (%1 must be the same), basically same concept as ins_317. | 是 | 继承自 TH13 |
| 631 | lifeHide | S (time) | Hides boss lifebar for %1 frames. | 是 | 继承自 TH13 |
| 632 | funcSet | S (id) | Sets a function that the game will execute every frame from a set of hardcoded functions that differs between games. | 是 | 继承自 TH13 |
| 633 | flagExtDmg | S (state) | Sets the external damage flag to %1. Caller probably needs to be the main boss for this to work - with this flag set, the caller gets damaged by the value stored in var_-9940 every frame, and then resets the value. This allows other enemies to damage the boss by incrementing the aforementioned variable, used in LoLK by Sagume (and also happens to be the main cause of the Sagume skip glitch) | 是 | 继承自 TH13 |
| 634 | setHitboxFunc | S (id) | Make the caller use a special function for determining collision with the player. TODO: create a list of functions and their IDs | 是 | 继承自 TH13 |
| 635 | etCancel2 | f (r) | Same as ins_615, but doesn't clear bullets with bomb invulnerability. | 是 | 继承自 TH13 |
| 636 | etClear2 | f (r) | Same as ins_616, but doesn't clear bullets with bomb invulnerability. | 是 | 继承自 TH13 |
| 637 | funcCall | S (id) | Same as ins_632, except the function is called just once instead of every frame. | 是 | 继承自 TH13 |
| 638 | scoreAdd | S (n) | Adds %1 to score (or subtracts if %1 is negative). There is no lower boundary check, so if this causes score to go below 0, an underflow happens. | 是 | 继承自 TH13 |
| 639 | funcSet2 | S (id) | Same as ins_632, except it sets an unknown flag to 1 (ins_632 sets it to 0) | 是 | 继承自 TH13 |
| 640 | etExSub | SSm (etId, index, s) | Sets the string parameter of transform on index %2 in bullet manager %1 to %3, transformations will be explained separately later. | 是 | 继承自 TH13 |
| 641 | etExSubtract | S (etId) | Subtracts 1 from the index used by ins_611 and ins_612, unless it's already 0. This basically changes where the next transformation will be appended. | 是 | 继承自 TH14 |

### TH16.5 指令：激光创建 / Laser creation

| ID | 助记名 | 参数 | 说明 | 文档化 | 来源 |
| --- | --- | --- | --- | --- | --- |
| 700 | laserNew | Sffff (etId, init_length, final_length, unknown_arg_3, width) | Sets basic parameters of the laser. %4 has something to do with the length of straight line lasers (investigation needed), but doesn't do anything for other laser types. For curvy lasers, the only used argument is %5, and length is specified with ins_701 instead. | 是 | 继承自 TH13 |
| 701 | laserTiming | SSSSSS (edId, startup_time, expand_time, duration, shrink_time, init_flags) | Sets timing for infinite lasers. %6 sets the initial flags for a laser, but these flags are unknown at the moment. For curvy lasers, the %2 argument instead specifies the length of the laser. | 是 | 继承自 TH13 |
| 702 | laserOn | S (edId) | Shoots a straight line laser. | 是 | 继承自 TH13 |
| 703 | laserStOn | SS (etId, laser_id) | Shoots an infinite laser. %2 is a number that's used to identify this particular laser instance, so that it can be referred to in other instructions. | 是 | 继承自 TH13 |
| 704 | laserOffset | Sff (laser_id, x, y) | Sets the position of the infinite laser pointed to by %1. | 是 | 继承自 TH13 |
| 705 | laserTrajectory | Sff (laser_id, x_speed, y_speed) | Sets the offset velocity of the infinite laser pointed to by %1. The laser's position will change by %2 and %3 every frame. | 是 | 继承自 TH13 |
| 706 | laserStLength | Sf (laser_id, speed) | Sets the speed of the infinite laser pointed to by %1. | 是 | 继承自 TH13 |
| 707 | laserStWidth | Sf (laser_id, width) | Sets the width of the infinite laser pointed to by %1. | 是 | 继承自 TH13 |
| 708 | laserStAngle | Sf (laser_id, angle) | Sets the angle of the infinite laser pointed to by %1. | 是 | 继承自 TH13 |
| 709 | laserStRotation | Sf (laser_id, angular_vel) | Sets the angular velocity of the infinite laser pointed to by %1. The laser's angle will change by %2 every frame. | 是 | 继承自 TH13 |
| 710 | laserStEnd | S (laser_id) | Clears the laser pointed to by %1. | 是 | 继承自 TH13 |
| 711 | laserCuOn | S (etId) | Shoots a curvy laser. | 是 | 继承自 TH13 |
| 712 | etCancelRect | ff (w, h) | Cancels all bullets in rectangle of width %1 and height %2. The area is affected by rotation set by ins_564. | 是 | 继承自 TH14 |
| 713 | unknown713 | SS (etId, laser_id) | Shoots a laser 'beam', a laser type used by marisa in GFW. Broken since this laser type does not exist outside of GFW. | 是 | 继承自 TH13 |
| 714 | unknown714 | SS (laser_id, unknown) | Does something with a laser beam pointed to by %1. Broken since this laser type does not exist outside of GFW. | 是 | 继承自 TH13 |

### TH16.5 指令：敌机交互 / Enemy interaction

| ID | 助记名 | 参数 | 说明 | 文档化 | 来源 |
| --- | --- | --- | --- | --- | --- |
| 800 | enmCall | Sm (id, sub) | Makes enemy with var_-9914 == %1 stop all subs it's running and execute sub %2 (works like an interrupt). This will NOT make the enemy execute the sub right as this instruction is called, the new sub will be executed when the game handles the given enemy, which might be later on the same frame or on the next frame. Using this to make the caller interrupt itself can make the game explode. | 是 | 继承自 TH13 |
| 801 | enmPos | ffS (varX, varY, id) | Stores coordinates of enemy with var_-9914 == %3 in (%1,%2). | 是 | 继承自 TH13 |
| 802 | broadcastInterrupt | S (slot) | For all existing bosses, trigger the interrupt set by ins_514 on slot %1. Does not change the HP to the one set in ins_514. | 是 | 继承自 TH13 |

### TH16.5 指令：调试 / Debug

| ID | 助记名 | 参数 | 说明 | 文档化 | 来源 |
| --- | --- | --- | --- | --- | --- |
| 900 | debug900 | — | 未在 Priw8 表中记录/待确认 | 否/待确认 | — |
| 901 | debug901 | — | 未在 Priw8 表中记录/待确认 | 否/待确认 | — |
| 902 | debug902 | — | 未在 Priw8 表中记录/待确认 | 否/待确认 | — |

### TH16.5 指令：游戏特有 / Game specific

| ID | 助记名 | 参数 | 说明 | 文档化 | 来源 |
| --- | --- | --- | --- | --- | --- |
| 1000 | sceneClear | — | Ends the scene as a victory. | 是 | 本作 |
| 1001 | sceneFail | — | Ends the scene as a game over. | 是 | 本作 |
| 1002 | photoBonusMultiplier | f (mult) | Set value used to determine "photo views", "like" and "faved" values when a photo is taken, something gets multiplied by it (exact formula unknown, 1.0f by default) | 是 | 本作 |
| 1003 | ins_1003 | S (state) | `th165.exe+1F5A6`: sets or clears flag 0x8 in flags_high; this bitflag is checked when a photo of the enemy is taken to determine... uh... something! it's an if-else, checked at `th165.exe+4B4CA` | 否/待确认 | 本作 |
| 1004 | ins_1004 | — | `th165.exe+1F54F`: calls a pretty involved method on `photoManager`. | 否/待确认 | 本作 |
| 1005 | effFadeout | S (duration) | Makes the entire screen fade to black in the given amount of frames. | 是 | 本作 |
| 1006 | ins_1006 | f (a) | `th165.exe+1F60A`: calls some method on the `supervisor`. | 否/待确认 | 本作 |
| 1007 | effFadeoutStg | S (duration) | Makes the inner area of the STG frame fade to black in the given amount of frames. | 是 | 本作 |
| 1008 | playerAllowCamera | S (state) | Determines whether camera can be used; Setting %1 to `1` allows using camera, `0` completely removes it | 是 | 本作 |
| 1009 | ins_1009 | S (a) | `th165.exe+1F64B`: sets some value in player struct, this value is used multiple times when a photo is taken. | 否/待确认 | 本作 |
| 1010 | cameraItemMult | f (mult) | Sets how much a single cancel item adds to the camera charge (a multiplier). | 是 | 本作 |
| 1011 | selfPhotoValue | S (val) | Sets a value that determines the bonus for getting the enemy in the photo (every enemy has its own specific one), default is 10, exact formula unknown. | 是 | 本作 |
| 1012 | selfPhotoBonus | S (bonus) | Sets the additional bonus for taking picture of the enemy (in form of a #hashtag).<br> With English patch, they are as follows:<br> - 0 - nothing<br>- 1 - #GiantBulletslel<br>- 2 - #SuperMoon!<br>- 3 - #DanmakuDestroyingRod?<br>- 4 - #StoneDanmakuROFL<br>- 5 - #FluffyFluff<br>- 6 - #DoggiePhoto<br>- 7 - #AnimalPhoto<br>- 8 - #BanginDrum<br>- 9 - #BodyOfMist?!<br>- 10 - #TheyrePissed...<br>- 11 - #ImTheRealSumirekoUsami!<br><br>~~Using other values will corrupt the stack~~ | 是 | 本作 |
| 1013 | takeSelfie | — | Makes the enemy take a photo of itself. | 是 | 本作 |
| 1014 | playerDisableShoot | S (duration) | Disables player shooting for a given amount of frames. | 是 | 本作 |

### TH16.5 变量

| ID | 名称 | 类型 | 访问 | 作用域 | 说明 | 文档化 | 来源 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| -10000 | RAND | int | 只读 | global/全局 | Random integer, very large range. | 是 | 继承自 TH10 |
| -9999.0f | RANDF | float | 只读 | global/全局 | Random float from 0.0f to 1.0f. | 是 | 继承自 TH10 |
| -9998.0f | RANDRAD | float | 只读 | global/全局 | Random float from -pi to pi. | 是 | 继承自 TH10 |
| -9997.0f | FINAL_X | float | 只读 | local/敌机局部 | Final X position of the enemy. | 是 | 继承自 TH10 |
| -9996.0f | FINAL_Y | float | 只读 | local/敌机局部 | Final Y position of the enemy. | 是 | 继承自 TH10 |
| -9995.0f | ABS_X | float | 只读 | local/敌机局部 | Absolute X position of the enemy. | 是 | 继承自 TH10 |
| -9994.0f | ABS_Y | float | 只读 | local/敌机局部 | Absolute Y position of the enemy. | 是 | 继承自 TH10 |
| -9993.0f | REL_X | float | 只读 | local/敌机局部 | Relative X position of the enemy. | 是 | 继承自 TH10 |
| -9992.0f | REL_Y | float | 只读 | local/敌机局部 | Relative Y position of the enemy. | 是 | 继承自 TH10 |
| -9991.0f | PLAYER_X | float | 只读 | global/全局 | Player's X position. | 是 | 继承自 TH10 |
| -9990.0f | PLAYER_Y | float | 只读 | global/全局 | Player's Y position. | 是 | 继承自 TH10 |
| -9989.0f | ANGLE_PLAYER | float | 只读 | local/敌机局部 | Angle from the enemy to the player. | 是 | 继承自 TH10 |
| -9988 | TIME | int | 只读 | local/敌机局部 | Time elapsed since the enemy spawned, in frames. | 是 | 继承自 TH10 |
| -9987.0f | RANDF2 | float | 只读 | global/全局 | Random float from -1.0f to 1.0f. | 是 | 继承自 TH10 |
| -9986 | TIMEOUT | int | 只读 | global/全局 | Set to 1 by the engine when a timeout occurs. | 是 | 继承自 TH10 |
| -9985 | I0 | int | 读写 | local/敌机局部 | Local integer variable, inherited by spawned enemies. | 是 | 继承自 TH10 |
| -9984 | I1 | int | 读写 | local/敌机局部 | Local integer variable, inherited by spawned enemies. | 是 | 继承自 TH10 |
| -9983 | I2 | int | 读写 | local/敌机局部 | Local integer variable, inherited by spawned enemies. | 是 | 继承自 TH10 |
| -9982 | I3 | int | 读写 | local/敌机局部 | Local integer variable, inherited by spawned enemies. | 是 | 继承自 TH10 |
| -9981.0f | F0 | float | 读写 | local/敌机局部 | Local float variable, inherited by spawned enemies. | 是 | 继承自 TH10 |
| -9980.0f | F1 | float | 读写 | local/敌机局部 | Local float variable, inherited by spawned enemies. | 是 | 继承自 TH10 |
| -9979.0f | F2 | float | 读写 | local/敌机局部 | Local float variable, inherited by spawned enemies. | 是 | 继承自 TH10 |
| -9978.0f | F3 | float | 读写 | local/敌机局部 | Local float variable, inherited by spawned enemies. | 是 | 继承自 TH10 |
| -9977.0f | FINAL_X2 | float | 只读 | local/敌机局部 | Same as var_-9997. | 是 | 继承自 TH10 |
| -9976.0f | FINAL_Y2 | float | 只读 | local/敌机局部 | Same as var_-9996. | 是 | 继承自 TH10 |
| -9975.0f | ABS_X2 | float | 只读 | local/敌机局部 | Same as var_-9995. | 是 | 继承自 TH10 |
| -9974.0f | ABS_Y2 | float | 只读 | local/敌机局部 | Same as var_-9994. | 是 | 继承自 TH10 |
| -9973.0f | REL_X2 | float | 只读 | local/敌机局部 | Same as var_-9993. | 是 | 继承自 TH10 |
| -9972.0f | REL_Y2 | float | 只读 | local/敌机局部 | Same as var_-9992. | 是 | 继承自 TH10 |
| -9971.0f | ABS_ANGLE | float | 只读 | local/敌机局部 | Angle of enemy's absolute movement. | 是 | 继承自 TH10 |
| -9970.0f | REL_ANGLE | float | 只读 | local/敌机局部 | Angle of enemy's relative movement. | 是 | 继承自 TH10 |
| -9969.0f | ABS_SPEED | float | 只读 | local/敌机局部 | Speed of enemy's absolute movement. | 是 | 继承自 TH10 |
| -9968.0f | REL_SPEED | float | 只读 | local/敌机局部 | Speed of enemy's relative movement. | 是 | 继承自 TH10 |
| -9967.0f | ABS_ORIGIN_DIST | float | 只读 | local/敌机局部 | Distance from the origin of enemy's absolute circular movement (radius of the circle). | 是 | 继承自 TH10 |
| -9966.0f | REL_ORIGIN_DIST | float | 只读 | local/敌机局部 | Distance from the origin of enemy's relative circular movement (radius of the circle). | 是 | 继承自 TH10 |
| -9965.0f | PLAYER_X2 | float | 只读 | global/全局 | Same as var_-9991. | 是 | 继承自 TH10 |
| -9964.0f | PLAYER_Y2 | float | 只读 | global/全局 | Same as var_-9990. | 是 | 继承自 TH10 |
| -9963.0f | BOSS_X | float | 只读 | global/全局 | Final X position of the boss. | 是 | 继承自 TH10 |
| -9962.0f | BOSS_Y | float | 只读 | global/全局 | Final Y position of the boss. | 是 | 继承自 TH10 |
| -9961 | ANM_ID | int | 只读 | local/敌机局部 | Is the current script on anm slot 0 of the enemy. | 是 | 继承自 TH10 |
| -9960 | RANK | int | 只读 | global/全局 | Numeric value of rank, ranging from -1024 to 1024. Increases over time and decreases when player bombs/dies etc. | 是 | 继承自 TH10 |
| -9959 | DIFF | int | 只读 | global/全局 | Difficulty (E=0, N=1, H=2, L=3, EX=4, O=5) | 是 | 继承自 TH10 |
| -9958.0f | FINAL_ANGLE | float | 只读 | local/敌机局部 | Final angle of enemy's movement. | 是 | 继承自 TH10 |
| -9957 | TRUE | int | 只读 | global/全局 | Always returns 1. | 是 | 继承自 TH10 |
| -9956.0f | ABS_ANGLE_PLAYER | float | 只读 | local/敌机局部 | Angle to the player from enemy's absolute position. | 是 | 继承自 TH10 |
| -9955.0f | REL_ANGLE_PLAYER | float | 只读 | local/敌机局部 | Angle to the player from enemy's relative position. | 是 | 继承自 TH10 |
| -9954 | LIFE | int | 只读 | local/敌机局部 | Enemy's current HP. | 是 | 继承自 TH10 |
| -9953 | EASY | int | 只读 | global/全局 | Set to 1 if difficulty is easy, otherwise it's 0. | 是 | 继承自 TH10 |
| -9952 | NORMAL | int | 只读 | global/全局 | Set to 1 if difficulty is normal, otherwise it's 0. | 是 | 继承自 TH10 |
| -9951 | HARD | int | 只读 | global/全局 | Set to 1 if difficulty is hard, otherwise it's 0. | 是 | 继承自 TH10 |
| -9950 | LUNATIC | int | 只读 | global/全局 | Set to 1 if difficulty is lunatic, otherwise it's 0. | 是 | 继承自 TH10 |
| -9949 | MISS_COUNT | int | 读写 | global/全局 | Increased by 1 every time the player dies. | 是 | 继承自 TH11 |
| -9948 | BOMB_COUNT | int | 读写 | global/全局 | Increased by 1 every time the player bombs. | 是 | 继承自 TH11 |
| -9947 | CAPTURE | int | 读写 | global/全局 | Set to 0 when the player dies, bombs, or uses a game-specific mechanic that "fails" a spell. | 是 | 继承自 TH11 |
| -9946 | ENM_CNT_REAL | int | 只读 | global/全局 | Amount of enemies alive (including main and MapleEnemy). | 是 | 继承自 TH11 |
| -9945 | SHOTTYPE | int | 只读 | global/全局 | Numeric value that represents player's shottype, the first shottype is 0. | 是 | 继承自 TH11 |
| -9944.0f | DIST_PLAYER | float | 只读 | local/敌机局部 | Distance from the enemy to the player. | 是 | 继承自 TH11 |
| -9943 | BI0 | int | 读写 | local/敌机局部 | Is the same as the I0 variable of boss 0. | 是 | 继承自 TH11 |
| -9942 | BI1 | int | 读写 | local/敌机局部 | Is the same as the I1 variable of boss 0. | 是 | 继承自 TH11 |
| -9941 | BI2 | int | 读写 | local/敌机局部 | Is the same as the I2 variable of boss 0. | 是 | 继承自 TH11 |
| -9940 | BI3 | int | 读写 | local/敌机局部 | Is the same as the I3 variable of boss 0. | 是 | 继承自 TH11 |
| -9939.0f | BF0 | float | 读写 | local/敌机局部 | Is the same as the F0 variable of boss 0. | 是 | 继承自 TH11 |
| -9938.0f | BF1 | float | 读写 | local/敌机局部 | Is the same as the F1 variable of boss 0. | 是 | 继承自 TH11 |
| -9937.0f | BF2 | float | 读写 | local/敌机局部 | Is the same as the F2 variable of boss 0. | 是 | 继承自 TH11 |
| -9936.0f | BF3 | float | 读写 | local/敌机局部 | Is the same as the F3 variable of boss 0. | 是 | 继承自 TH11 |
| -9935.0f | F4 | float | 读写 | local/敌机局部 | Local float variable inherited by spawned enemies, just like F0-F3 and I0-I3. | 是 | 继承自 TH11 |
| -9934.0f | F5 | float | 读写 | local/敌机局部 | Local float variable inherited by spawned enemies, just like F0-F3 and I0-I3. | 是 | 继承自 TH11 |
| -9933.0f | F6 | float | 读写 | local/敌机局部 | Local float variable inherited by spawned enemies, just like F0-F3 and I0-I3. | 是 | 继承自 TH11 |
| -9932.0f | F7 | float | 读写 | local/敌机局部 | Local float variable inherited by spawned enemies, just like F0-F3 and I0-I3. | 是 | 继承自 TH11 |
| -9931 | LAST_ENM_ID | int | 只读 | global/全局 | ID of the last spawned enemy. | 是 | 继承自 TH12 |
| -9930 | POWER | int | 只读 | global/全局 | Player's power (4.00 => 400) | 是 | 继承自 TH12 |
| -9929 | DS1 | int | 只读 | global/全局 | Used in Double Spoiler, unknown. | 否/待确认 | 继承自 TH12.5 |
| -9928 | DS2 | int | 只读 | global/全局 | Used in Double Spoiler, unknown. | 否/待确认 | 继承自 TH12.5 |
| -9927 | DS3 | int | 只读 | global/全局 | Used in Double Spoiler, unknown. | 否/待确认 | 继承自 TH12.5 |
| -9926 | GI0 | int | 读写 | global/全局 | Global integer variable. | 是 | 继承自 TH12.5 |
| -9925 | GI1 | int | 读写 | global/全局 | Global integer variable. | 是 | 继承自 TH12.5 |
| -9924 | GI2 | int | 读写 | global/全局 | Global integer variable. | 是 | 继承自 TH12.5 |
| -9923 | GI3 | int | 读写 | global/全局 | Global integer variable. | 是 | 继承自 TH12.5 |
| -9922.0f | GF0 | float | 读写 | global/全局 | Global float variable. | 是 | 继承自 TH12.5 |
| -9921.0f | GF1 | float | 读写 | global/全局 | Global float variable. | 是 | 继承自 TH12.5 |
| -9920.0f | GF2 | float | 读写 | global/全局 | Global float variable. | 是 | 继承自 TH12.5 |
| -9919.0f | GF3 | float | 读写 | global/全局 | Global float variable. | 是 | 继承自 TH12.5 |
| -9918.0f | GF4 | float | 读写 | global/全局 | Global float variable. | 是 | 继承自 TH12.5 |
| -9917.0f | GF5 | float | 读写 | global/全局 | Global float variable. | 是 | 继承自 TH12.5 |
| -9916.0f | GF6 | float | 读写 | global/全局 | Global float variable. | 是 | 继承自 TH12.5 |
| -9915.0f | GF7 | float | 读写 | global/全局 | Global float variable. | 是 | 继承自 TH12.5 |
| -9914 | ID | int | 只读 | local/敌机局部 | ID of the enemy. | 是 | 继承自 TH12.5 |
| -9913 | DS_PHOTOCOUNT | int | 只读 | global/全局 | Used in Double Spoiler, amount of photos taken. | 是 | 继承自 TH12.5 |
| -9912 | DS4 | int | 只读 | global/全局 | Used in Double Spoiler, unknown. | 否/待确认 | 继承自 TH12.5 |
| -9911.0f | ANGLE_BOSS | float | 只读 | global/全局 | Angle at which the boss moves. | 是 | 继承自 TH12.5 |
| -9910.0f | SPEED_BOSS | float | 只读 | global/全局 | Speed at which the boss moves. | 是 | 继承自 TH12.5 |
| -9909 | UNKNOWN9 | int | 只读 | local/敌机局部 | Enemy ID of the parent enemy. | 是 | 继承自 TH12.8 |
| -9908 | ENM_CNT | int | 只读 | global/全局 | Amount of killable enemies alive (that is, doesn't include hitboxless/intangible enemies etc). | 是 | 继承自 TH13 |
| -9907 | SPELL_ID | int | 只读 | global/全局 | Spellcard ID, used by spell practice. Unknown meaning in LoLK. | 是 | 继承自 TH13 |
| -9906 | MIRROR | int | 只读 | local/敌机局部 | Mirror flag state, either 0 or 1. TODO: verify game version | 否/待确认 | 继承自 TH15 |
| -9905 | [-9905] | int | 只读 | global/全局 | Value set by ins_524. | 是 | 继承自 TH15 |
| -9904 | MISS_COUNT_GLOBAL | int | 只读 | global/全局 | Amount of misses throughout the entire game. | 是 | 继承自 TH15 |
| -9903 | SUBSEASON | int | 只读 | global/全局 | Selected subseason. Spring = 0, summer = 1, autumn = 2, winter = 3, extra subseason = 4. | 是 | 继承自 TH16 |

## TH17 东方鬼形兽

- 体系：第四世代
- 指令：普通指令 347 条；已说明 260/347。主要分组：系统/流程/栈/算术 / System；敌机创建与 ANM 管理 / Enemy creation and ANM script management；移动管理 / Movement management；敌机属性与杂项 / Enemy property management and other miscellaneous things；子弹创建与删除 / Bullet creation and deletion；激光创建 / Laser creation；敌机交互 / Enemy interaction；调试 / Debug；游戏特有 / Game specific。
- 变量：变量范围 -10000..-9899；本文列出有说明/命名记录的 102 条，未列空洞/未知项。

### TH17 指令：系统/流程/栈/算术 / System

| ID | 助记名 | 参数 | 说明 | 文档化 | 来源 |
| --- | --- | --- | --- | --- | --- |
| 0 | nop | — | Empty instruction, doesn't do anything. | 是 | 继承自 TH13 |
| 1 | delete | — | Returns to the top of current call stack. | 是 | 继承自 TH13 |
| 2 | ins_2 | — |  | 否/待确认 | 继承自 TH-1 |
| 3 | ins_3 | — |  | 否/待确认 | 继承自 TH-1 |
| 4 | ins_4 | — |  | 否/待确认 | 继承自 TH-1 |
| 5 | ins_5 | — |  | 否/待确认 | 继承自 TH-1 |
| 6 | ins_6 | — |  | 否/待确认 | 继承自 TH-1 |
| 7 | ins_7 | — |  | 否/待确认 | 继承自 TH-1 |
| 8 | ins_8 | — |  | 否/待确认 | 继承自 TH-1 |
| 9 | ins_9 | — |  | 否/待确认 | 继承自 TH-1 |
| 10 | ret | — | Returns from the current sub. | 是 | 继承自 TH13 |
| 11 | call | m (sub) | Calls a given sub. Can take additional parameters to pass as arguments to the sub. [c=orange]Direct Usage obsolete. Use `@subName()` syntax instead. | 是 | 继承自 TH13 |
| 12 | jmp | o (target) | Unconditionally jumps to the label %1. [c=orange]Direct usage obsolete. Use `goto label` syntax instead. | 是 | 继承自 TH13 |
| 13 | jmpEq | o (target) | Pops a number from the stack and if it evaluates to false (in this context, 0), jumps to label %1. [c=orange]Direct usage obsolete. Use if/unless statement instead. | 是 | 继承自 TH13 |
| 14 | jmpNeq | o (target) | Pops a number from the stack and if it evaluates to true (in this context, anything non-0), jumps to label %1. [c=orange]Direct usage obsolete. Use if/unless statement instead. | 是 | 继承自 TH13 |
| 15 | callAsync | m (sub) | Asynchronously calls a given sub. Can take additional parameters to pass as arguments to the sub. [c=orange]Direct usage obsolete. Use `@subName() async` syntax instead. | 是 | 继承自 TH13 |
| 16 | callAsyncId | mS (sub, id) | Asynchronously calls a given sub and assigns it ID %2. Can take additional parameters to pass as arguments to the sub. [c=orange]Direct usage obsolete, use, `@subName() async id` syntax instead. | 是 | 继承自 TH13 |
| 17 | killAsync | S (id) | Ends most recently called sub that has ID %1 (same ID as in ins_16). If no sub with the given ID is found, nothing happens. Using ID -1 can lead to various unexpected results, ranging from deleting the enemy to freezing the game. | 是 | 继承自 TH13 |
| 18 | ins_18 | S (id) | Let `vm` be the most recent async sub running with ID %1: this ins sets `vm[0x000011E4]` to 1. | 否/待确认 | 继承自 TH13 |
| 19 | ins_19 | S (id) | Let `vm` be the most recent async sub running with ID %1: this ins sets `vm[0x000011E4]` to 0. | 否/待确认 | 继承自 TH13 |
| 20 | ins_20 | SS (id, b) | Let `vm` be the most recent async sub running with ID %1: this ins sets `vm[0x0000101C]` to %2. | 否/待确认 | 继承自 TH13 |
| 21 | killAllAsync | — | Ends all running async subs. Calling this in an async sub can lead to unexpected results, such as crashing the game. | 是 | 继承自 TH13 |
| 22 | debug22 | Sm (a, b) | Debug instruction, code does not exist in the release builds of the game. Most likely used to call sub %2 if some variable set in a debug menu is equal to %1. | 是 | 继承自 TH13 |
| 23 | wait | S (time) | Stops sub execution for %1 frames. | 是 | 继承自 TH13 |
| 24 | waitf | f (time) | ins_23, but time is given as a float instead of an int. Subframes do actually exist and affect ins_547. | 是 | 继承自 TH13 |
| 25 | ins_25 | — |  | 否/待确认 | 继承自 TH-1 |
| 26 | ins_26 | — |  | 否/待确认 | 继承自 TH-1 |
| 27 | unknown27 | — |  | 否/待确认 | 继承自 TH-1 |
| 28 | ins_28 | — |  | 否/待确认 | 继承自 TH-1 |
| 29 | ins_29 | — |  | 否/待确认 | 继承自 TH-1 |
| 30 | unknown30 | m (formatString) | Some sort of `printf` debug instruction, which can take additional float/int arguments after %1. Its code does not exist in the release builds. | 是 | 继承自 TH13 |
| 31 | unknown31 | — |  | 否/待确认 | 继承自 TH-1 |
| 32 | ins_32 | — |  | 否/待确认 | 继承自 TH-1 |
| 33 | ins_33 | — |  | 否/待确认 | 继承自 TH-1 |
| 34 | ins_34 | — |  | 否/待确认 | 继承自 TH-1 |
| 35 | ins_35 | — |  | 否/待确认 | 继承自 TH-1 |
| 36 | ins_36 | — |  | 否/待确认 | 继承自 TH-1 |
| 37 | ins_37 | — |  | 否/待确认 | 继承自 TH-1 |
| 38 | ins_38 | — |  | 否/待确认 | 继承自 TH-1 |
| 39 | ins_39 | — |  | 否/待确认 | 继承自 TH-1 |
| 40 | stackAlloc | S (size) | Increases the ECL stack pointer by %1 bytes (probably), to make space for sub variables. [c=orange]Obsolete, thecl generates this instruction automatically. | 是 | 继承自 TH13 |
| 41 | ins_41 | — |  | 否/待确认 | 继承自 TH-1 |
| 42 | pushi | S (num) | Pushes an integer to the ECL stack. [c=orange]Obsolete, push values to stack by writing unassigned expressions instead. | 是 | 继承自 TH13 |
| 43 | seti | S (var) | Pops an integer from the stack into variable %1. [c=orange]Obsolete, use assignment syntax instead. | 是 | 继承自 TH13 |
| 44 | pushf | f (num) | Pushes a float to the ECL stack. [c=orange]Obsolete, push values to stack by writing unassigned expressions instead. | 是 | 继承自 TH13 |
| 45 | setf | f (var) | Pops a float from the stack into variable %1. [c=orange]Obsolete, use assignment syntax instead. | 是 | 继承自 TH13 |
| 46 | ins_46 | — |  | 否/待确认 | 继承自 TH-1 |
| 47 | ins_47 | — |  | 否/待确认 | 继承自 TH-1 |
| 48 | ins_48 | — |  | 否/待确认 | 继承自 TH-1 |
| 49 | ins_49 | — |  | 否/待确认 | 继承自 TH-1 |
| 50 | addi | — | Sums integers on the stack. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 51 | addf | — | Sums floats on the stack. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 52 | subi | — | Subtracts integers on the stack. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 53 | subf | — | Subtracts floats on the stack. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 54 | muli | — | Multiplies integers on the stack. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 55 | mulf | — | Multiplies floats on the stack. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 56 | divi | — | Divides integers on the stack. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 57 | divf | — | Divides floats on the stack. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 58 | modi | — | Modulo operation on integers on the stack. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 59 | eqi | — | Stack integer `==` comparison. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 60 | eqf | — | Stack float `==` comparison. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 61 | neqi | — | Stack integer `!=` comparison. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 62 | neqf | — | Stack float `!=` comparison. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 63 | lessi | — | Stack integer `<` comparison. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 64 | lessf | — | Stack float `<` comparison. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 65 | leqi | — | Stack integer `<=` comparison. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 66 | leqf | — | Stack float `<=` comparison. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 67 | greateri | — | Stack integer `>` comparison. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 68 | greaterf | — | Stack float `>` comparison. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 69 | geqi | — | Stack integer `>=` comparison. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 70 | geqf | — | Stack float `>=` comparison. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 71 | noti | — | Stack integer NOT operation (e.g. !1). [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 72 | notf | — | Stack float NOT operation (e.g. !1.0f). [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 73 | or | — | Logical OR operation on the stack. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 74 | and | — | Logical AND operation on the stack. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 75 | xor | — | Bitwise XOR operation on integers on the stack. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 76 | bit_or | — | Bitwise OR operation on integers on the stack. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 77 | bit_and | — | Bitwise AND operation on integers on the stack. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 78 | deci | S (var) | Pushes variable %1 to the stack and then decrements it. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 79 | stackSin | — | sin operation on a float on the stack. [c=orange]Obsolete, use `sin(floatVal)` instead. | 是 | 继承自 TH13 |
| 80 | stackCos | — | cos operation on a float on the stack. [c=orange]Obsolete, use `cos(floatVal)` instead. | 是 | 继承自 TH13 |
| 81 | circlePos | ffff (varX, varY, ang, radius) | Performs following operation: [code]%1 = cos(%3)*%4;<br>%2 = sin(%3)*%4;[/code] | 是 | 继承自 TH13 |
| 82 | validRad | f (var) | Normalizes angle in %1. | 是 | 继承自 TH13 |
| 83 | negi | — | Negates an integer on the stack. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 84 | negf | — | Negates a float on the stack. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 85 | squareSum | fff (var, x, y) | Performs following operation: [code]%1 = %2*%2 + %3*%3;[/code] | 是 | 继承自 TH13 |
| 86 | squareSumRoot | fff (var, x, y) | Performs following operation: [code]%1 = sqrt(%2*%2 + %3*%3);[/code] | 是 | 继承自 TH13 |
| 87 | getAngle | fffff (var, x1, y1, x2, y2) | Calculates angle from (%2,%3) to (%4,%5) and stores it in %1. | 是 | 继承自 TH13 |
| 88 | stackSqrt | — | square root operation on a float on the stack. [c=orange]Obsolete, use `sqrt(floatVal)` instead. | 是 | 继承自 TH13 |
| 89 | linearFunc | fff (var, a, x) | Performs following operation: [code]%1 = %2*%3;[/code]<br>(what's the point of making this an instruction, ZUN?) | 是 | 继承自 TH13 |
| 90 | pointRotate | fffff (varX, varY, x, y, rad) | Rotates point (%3,%4) by angle %5 and stores the resulting coordinates in %1 and %2. | 是 | 继承自 TH13 |
| 91 | floatTime | SfSSff (slot, var, time, mode, init, final) | In %3 frames using mode %4, variable %2 changes from %5 to %6. %1 is used to set the slot to be used by this ins, every enemy has 8 slots (0 to 7). | 是 | 继承自 TH13 |
| 92 | math92 | SfSSffff (slot, var, time, mode, init, final, m, n) | Same as ins_91, but takes 2 extra arguments of unknown meaning. Needs investigation. | 否/待确认 | 继承自 TH13 |
| 93 | math93 | ffff (varX, varY, r1, r2) | Gets a random point based on %3 and %4 and stores it on (%1,%2). Needs investigation. | 否/待确认 | 继承自 TH13 |

### TH17 指令：敌机创建与 ANM 管理 / Enemy creation and ANM script management

| ID | 助记名 | 参数 | 说明 | 文档化 | 来源 |
| --- | --- | --- | --- | --- | --- |
| 300 | enmCreate | mffSSS (sub, x, y, hp, score, item) | Creates an enemy using subroutine %1 at coordinates %2, %3 (relative to position of enemy that called it), health of created enemy is %4, score bonus is %5 and item drop is %6. | 是 | 继承自 TH13 |
| 301 | enmCreateA | mffSSS (sub, x, y, hp, score, item) | Creates an enemy using subroutine %1 at coordinates %2, %3 (absolute position), health of created enemy is %4, score bonus is %5 and item drop is %6. | 是 | 继承自 TH13 |
| 302 | anmSelect | S (anmIndex) | Selects ANM file to be used by other instructions based on %1. | 是 | 继承自 TH13 |
| 303 | anmSetSprite | SS (slot, script) | Loads script %2 from ANM selected with ins_302 on slot %1. | 是 | 继承自 TH13 |
| 304 | enmCreateM | mffSSS (sub, x, y, hp, score, item) | Creates a mirrored enemy using subroutine %1 at coordinates %2, %3 (relative to caller's position), health of created enemy is %4, score bonus is %5 and item drop is %6. | 是 | 继承自 TH13 |
| 305 | enmCreateAM | mffSSS (sub, x, y, hp, score, item) | Creates an mirrored enemy using subroutine %1 at coordinates %2, %3 (absolute position), health of created enemy is %4, score bonus is %5 and item drop is %6. | 是 | 继承自 TH13 |
| 306 | anmSetMain | SS (slot, script) | Loads script %2 from ANM selected with ins_302 on slot %1. However, the script number provided will only be used when the enemy is not moving. When moving left %2+1 will be used, right %2+2, diagonal left %2+3, diagonal right %2+4. Might not work properly if %1 is not 0 according to THBWiki. | 是 | 继承自 TH13 |
| 307 | anmPlay | SS (anmIndex, script) | From ANM file selected based on %1, play script %2 at caller's current coordinates. The spawned script is completely independent, and will continue existing even if caller is deleted. | 是 | 继承自 TH13 |
| 308 | anmPlayAbs | SS (anmIndex, script) | From ANM file selected based on %1, play script %2 at coordinates (0, 0). The spawned script is completely independent, and will continue existing even if caller is deleted. | 是 | 继承自 TH13 |
| 309 | enmCreateF | mffSSS (sub, x, y, hp, score, item) | Creates a filler enemy using subroutine %1 at coordinates %2, %3 (relative to caller's position), health of created enemy is %4, score bonus is %5 and item drop is %6. | 是 | 继承自 TH13 |
| 310 | enmCreateAF | mffSSS (sub, x, y, hp, score, item) | Creates a filler enemy using subroutine %1 at coordinates %2, %3 (absolute position), health of created enemy is %4, score bonus is %5 and item drop is %6. | 是 | 继承自 TH13 |
| 311 | enmCreateMF | mffSSS (sub, x, y, hp, score, item) | Creates a mirrored filler enemy using subroutine %1 at coordinates %2, %3 (relative to caller's position), health of created enemy is %4, score bonus is %5 and item drop is %6. | 是 | 继承自 TH13 |
| 312 | enmCreateAMF | mffSSS (sub, x, y, hp, score, item) | Creates a mirrored filler enemy using subroutine %1 at coordinates %2, %3 (absolute position), health of created enemy is %4, score bonus is %5 and item drop is %6. | 是 | 继承自 TH13 |
| 313 | anmSelectedPlay | S (script) | Same as ins_307, except it uses the ANM file selected by ins_302. | 是 | 继承自 TH13 |
| 314 | anmPlayHigh | SS (anmIndex, script) | Same as ins_307, except it spawns the ANM with a higher layer? Needs further investigation. | 否/待确认 | 继承自 TH13 |
| 315 | anmPlayRotate | SSf (anmIndex, script, angle) | Same as ins_307, except it sets rotation of spawned ANM to %3. | 是 | 继承自 TH13 |
| 316 | anm316 | SS (a, b) | Unknown. | 否/待确认 | 继承自 TH13 |
| 317 | anmSwitch | SS (slot, switch) | Sets the execution pointer of ANM script on slot %1 to where ANM `ins_5(a)` with `a` == `switch` is (the time is also changed to match time of `ins_5`). Doesn't work if the value is 0 apparently? | 是 | 继承自 TH13 |
| 318 | anmReset | — | Resets some ANM-related parameters of the caller (TODO: what exactly?) | 是 | 继承自 TH13 |
| 319 | anmRotate | Sf (slot, r) | Set rotation of an ANM script on slot %1 to %2. | 是 | 继承自 TH13 |
| 320 | anmMove | Sff (slot, x, y) | Set position of an ANM script on slot %1 to (%2,%3). This does not detach the script from the caller, so the actual position of the script will be position of the caller + position set here. | 是 | 继承自 TH13 |
| 321 | enmMapleEnemy | mffSSS (sub, x, y, hp, score, item) | ins_300, but used by 'MapleEnemy' (TODO: what's the difference from ins_300?) | 是 | 继承自 TH13 |
| 322 | enm322 | SS (a, b) | Unknown. | 否/待确认 | 继承自 TH13 |
| 323 | deathAnm | SS (anmIndex, script) | Set the animation that will play when the enemy dies to script %2 from ANM file specified by %1. | 是 | 继承自 TH13 |
| 324 | enmPos2 | — | Unknown. | 否/待确认 | 继承自 TH13 |
| 325 | anmColor | SSSS (slot, R, G, B) | Modify color of ANM script on slot %1, %2, %3, [c=lightblue]%4 correspond to individual colors and have to be from 0 to 255. | 是 | 继承自 TH13 |
| 326 | anmColorTime | SSSSSS (slot, time, mode, R, G, B) | Same as ins_325, but the change is applied in %2 frames using mode %3. | 是 | 继承自 TH13 |
| 327 | anmAlpha | SS (slot, alpha) | Sets alpha of ANM script on slot %1 to %2 (must be a value between 0-255) | 是 | 继承自 TH13 |
| 328 | anmAlphaTime | SSSS (slot, time, mode, alpha) | Same as ins_327, but the change is applied in %2 frames using mode %3. | 是 | 继承自 TH13 |
| 329 | anmScale | Sff (slot, w, h) | Sets horizontal and vertical scaling of ANM script on slot %1 to %2 and %3 respectively. Overwrites scaling properties set by the ANM script. | 是 | 继承自 TH13 |
| 330 | anmScaleTime | SSSff (slot, time, mode, w, h) | Same as ins_329, but the change is applied in %2 frames using mode %3. | 是 | 继承自 TH13 |
| 331 | anmAlpha2 | SS (slot, alpha) | Sets alpha2 (opacity of the gradient) of ANM script on slot %1 to %2. | 是 | 继承自 TH13 |
| 332 | anmAlpha2Time | SSSS (slot, time, mode, alpha) | Same as ins_331, but the change is applied in %2 frames using mode %3. | 是 | 继承自 TH13 |
| 333 | anm333 | SSSff (a, b, c, r, s) | Unknown. Might be doing something to ANM script on slot %1. | 否/待确认 | 继承自 TH13 |
| 334 | anm334 | S (a) | Hard to tell? THBWiki Google translate gives this: 'The animation effect of the playing unit (enemy), the lightning effect near the evil spirit ball of the god temple', which might be referring to lightning around Nue in TD extra stage. | 否/待确认 | 继承自 TH13 |
| 335 | anmScale2 | Sff (slot, w, h) | Same as ins_329, except it doesn't overwrite the scaling set by the ANM script - instead, it multiplies it. | 是 | 继承自 TH13 |
| 336 | anmLayer | SS (slot, layer) | Set layer of ANM script on slot %1 to %2. | 是 | 继承自 TH14 |
| 337 | anmBlendMode | SS (slot, b) | Set blend mode of ANM script on slot %1 to %2 (TODO: make a list of blend modes). | 是 | 继承自 TH16 |
| 338 | anmPlayPos | SSfff (anmIndex, script, x, y, z) | Same as ins_307, but the spawned script is offset by (%3,%4). For 3D objects, %5 is used too (TODO: verify that). | 是 | 继承自 TH16 |
| 339 | anm339 | SSS (a, b, c) | Unknown. Might be doing something to ANM script on slot %1. | 否/待确认 | 继承自 TH16 |
| 340 | enmDelete | S (id) | Delete enemy with the given ID. | 是 | 继承自 TH16 |

### TH17 指令：移动管理 / Movement management

| ID | 助记名 | 参数 | 说明 | 文档化 | 来源 |
| --- | --- | --- | --- | --- | --- |
| 400 | movePos | ff (x, y) | Sets caller's absolute position to %1, %2. | 是 | 继承自 TH13 |
| 401 | movePosTime | SSff (time, mode, x, y) | Same as ins_400, but the change is applied in %1 frames using mode %2. | 是 | 继承自 TH13 |
| 402 | movePosRel | ff (x, y) | Sets caller's relative position to %1, %2. | 是 | 继承自 TH13 |
| 403 | movePosRelTime | SSff (time, mode, x, y) | Same as ins_402, but the change is applied in %1 frames using mode %2. | 是 | 继承自 TH13 |
| 404 | moveVel | ff (r, spd) | Sets caller's absolute movement angle to %1 and speed to %2. | 是 | 继承自 TH13 |
| 405 | moveVelTime | SSff (time, mode, r, spd) | Same as ins_404, but the change is applied in %1 frames using mode %2. | 是 | 继承自 TH13 |
| 406 | moveVelRel | ff (r, spd) | Sets caller's relative movement angle to %1 and speed to %2. | 是 | 继承自 TH13 |
| 407 | moveVelRelTime | SSff (time, mode, r, spd) | Same as ins_406, but the change is applied in %1 frames using mode %2. | 是 | 继承自 TH13 |
| 408 | moveCircle | ffff (θ, spd, rad, radInc) | Sets caller's absolute circle movement: %1 is the angle indicating initial position on the circle, %2 is the angular velocity, %3 is circle radius and %4 is by how much the radius increases each frame. | 是 | 继承自 TH13 |
| 409 | moveCircleTime | SSfff (time, mode, spd, rad, radInc) | Same as ins_408, but the change is applied in %1 frames using mode %2. There is also no initial angle parameter here for obvious reason. | 是 | 继承自 TH13 |
| 410 | moveCircleRel | ffff (θ, spd, rad, radInc) | Sets caller's relative circle movement: %1 is the angle indicating initial position on the circle, %2 is the angular velocity, %3 is circle radius and %4 is by how much the radius increases each frame. | 是 | 继承自 TH13 |
| 411 | moveCircleRelTime | SSfff (time, mode, spd, rad, radInc) | Same as ins_410, but the change is applied in %1 frames using mode %2. There is also no initial angle parameter here for obvious reason. | 是 | 继承自 TH13 |
| 412 | moveRand | SSf (time, mode, spd) | Randomizes caller's absolute angle and sets absolute speed to %3. The speed changes back to 0 in %1 frames using mode %2. | 是 | 继承自 TH13 |
| 413 | moveRandRel | SSf (time, mode, spd) | Randomizes caller's relative angle and sets relative speed to %3. The speed changes back to 0 in %1 frames using mode %2. | 是 | 继承自 TH13 |
| 414 | moveBoss | — | Sets caller's absolute position to the absolute position of the boss. If called without a boss, [tip=Google translated from THBWiki, I find this sentence funny]it will cause serious mis-access and explode[/tip]. | 是 | 继承自 TH13 |
| 415 | moveBossRel | — | Sets caller's relative position to the relative position of the boss. If called without a boss, [tip=Google translated from THBWiki, I find this sentence funny]it will cause serious mis-access and explode[/tip]. | 是 | 继承自 TH13 |
| 416 | movePos3d | fff (x, y, z) | Same as ins_400, but takes a %3 parameter for the third dimension, which probably affects 3D ANM scripts used by the caller, or something. | 是 | 继承自 TH13 |
| 417 | movePos3dRel | fff (x, y, z) | Same as ins_402, but takes a %3 parameter for the third dimension, which probably affects 3D ANM scripts used by the caller, or something. | 是 | 继承自 TH13 |
| 418 | moveAdd | ff (x, y) | Increases caller's absolute position by %1 and %2. | 是 | 继承自 TH13 |
| 419 | move419 | ff (x, y) | While the code of this ins looks like it's supposed to be a relative version of ins_418, it doesn't seem to behave like that... | 否/待确认 | 继承自 TH13 |
| 420 | moveEllipse | ffffff (θ, spd, rad, radInc, ellDir, ellRatio) | Sets caller's absolute ellipse movement: %1 is the angle indicating initial position on the ellipse, %2 is the angular velocity, %3 is the base circle radius and %4 is by how much the radius increases each frame. %6 is how much the base circle should be 'squished' to make it an ellipse, and %5 is the squishing angle (I don't know math terms in English, sorry) | 是 | 继承自 TH13 |
| 421 | moveEllipseTime | SSfffff (time, mode, spd, rad, radInc, ellDir, ellRatio) | Same as ins_420, but the change is applied in %1 frames using mode %2. There is also no initial angle parameter here for obvious reason | 是 | 继承自 TH13 |
| 422 | moveEllipseRel | ffffff (θ, spd, rad, radInc, ellDir, ellRatio) | Sets caller's relative ellipse movement: %1 is the angle indicating initial position on the ellipse, %2 is the angular velocity, %3 is the base circle radius and %4 is by how much the radius increases each frame. %6 is how much the base circle should be 'squished' to make it an ellipse, and %5 is the squishing angle (I don't know math terms in English, sorry) | 是 | 继承自 TH13 |
| 423 | moveEllipseRelTime | SSfffff (time, mode, spd, rad, radInc, ellDir, ellRatio) | Same as ins_422, but the change is applied in %1 frames using mode %2. There is also no initial angle parameter here for obvious reason | 是 | 继承自 TH13 |
| 424 | moveSetMirror | S (state) | Sets caller's mirror flag to %1. | 是 | 继承自 TH13 |
| 425 | moveBezier | Sffffff (time, x1, y1, x2, y2, x3, y3) | In %1 frames, the enemy moves towards (%2,%3), then moves towards (%6,%7) for a while and finally moves to (%4,%5). Uses absolute position.<br>From THBWiki: <br>(assuming the current coordinates are (x0, y0)) the motion trajectory is actually a Bezier curve from (x0, y0) to (x2, y2);<br>The P1 coordinate of the curve is `((x1-x0)*1/3, (y1-y0)*1/3)`;<br>The P2 coordinate of the curve is `(-(x3-x2)*1/3+x2,-(y3-y2) *1/3+x2)` | 是 | 继承自 TH13 |
| 426 | moveBezierRel | Sffffff (time, x1, y1, x2, y2, x3, y3) | Same as ins_425, but uses relative position. | 是 | 继承自 TH13 |
| 427 | moveReset | — | Resets some movement-related parameters (TODO: what exactly?) | 否/待确认 | 继承自 TH13 |
| 428 | moveVelNM | ff (r, spd) | Same as ins_404, but ignores the mirror flag. | 是 | 继承自 TH13 |
| 429 | moveVelNMTime | SSff (time, mode, r, spd) | Same as ins_405, but ignores the mirror flag. | 是 | 继承自 TH13 |
| 430 | moveVelNMRel | ff (r, spd) | Same as ins_406, but ignores the mirror flag. | 是 | 继承自 TH13 |
| 431 | moveVelNMRelTime | SSff (time, mode, r, spd) | Same as ins_407, but ignores the mirror flag. | 是 | 继承自 TH13 |
| 432 | moveEnm | S (id) | Sets caller's absolute position to absolute position of enemy with var_-9914 == %1. | 是 | 继承自 TH13 |
| 433 | moveEnmRel | S (id) | Sets caller's relative position to relative position of enemy with var_-9914 == %1. | 是 | 继承自 TH13 |
| 434 | moveCurve | SSSff (time, mode, c, x, y) | In %1 frames using mode %2, caller's absolute position is changed to (%4,%5). The movement trajectory is a curve based on %3, it is unknown how it works exactly. | 否/待确认 | 继承自 TH13 |
| 435 | moveCurveRel | SSSff (time, mode, c, x, y) | In %1 frames using mode %2, caller's relative position is changed to (%4,%5). The movement trajectory is a curve based on %3, it is unknown how it works exactly. | 否/待确认 | 继承自 TH13 |
| 436 | moveAddTime | SSff (time, mode, x, y) | Same as ins_418, but the change is applied in %1 frames using mode %2. | 是 | 继承自 TH13 |
| 437 | moveAddRelTime | SSff (time, mode, x, y) | Same as ins_419, but the change is applied in %1 frames using mode %2 (it also behaves as expected, unlike ins_419). | 是 | 继承自 TH13 |
| 438 | moveCurveAdd | SSSff (time, mode, c, x, y) | Same as ins_434, but instead caller's current absolute coordinates are added to %4 and %5. | 是 | 继承自 TH13 |
| 439 | moveCurveAddRel | SSSff (time, mode, c, x, y) | Same as ins_435, but instead caller's current relative coordinates are added to %4 and %5. | 是 | 继承自 TH13 |
| 440 | moveAngle | f (r) | Sets caller's absolute movement angle to %1. | 是 | 继承自 TH14 |
| 441 | moveAngleTime | SSf (time, mode, r) | Same as ins_440, but the change is applied in %1 frames using mode %2. | 是 | 继承自 TH14 |
| 442 | moveAngleRel | f (r) | Sets caller's relative movement angle to %1. | 是 | 继承自 TH14 |
| 443 | moveAngleRelTime | SSf (time, mode, r) | Same as ins_442, but the change is applied in %1 frames using mode %2. | 是 | 继承自 TH14 |
| 444 | moveSpeed | f (spd) | Sets caller's absolute movement speed to %1. | 是 | 继承自 TH14 |
| 445 | moveSpeedTime | SSf (time, mode, spd) | Same as ins_444, but the change is applied in %1 frames using mode %2. | 是 | 继承自 TH14 |
| 446 | moveSpeedRel | f (spd) | Sets caller's relative movement speed to %1. | 是 | 继承自 TH14 |
| 447 | moveSpeedRelTime | SSf (time, mode, spd) | Same as ins_446, but the change is applied in %1 frames using mode %2. | 是 | 继承自 TH14 |

### TH17 指令：敌机属性与杂项 / Enemy property management and other miscellaneous things

| ID | 助记名 | 参数 | 说明 | 文档化 | 来源 |
| --- | --- | --- | --- | --- | --- |
| 500 | setHurtbox | ff (w, h) | Sets caller's hurtbox width to %1 and height to %2. | 是 | 继承自 TH13 |
| 501 | setHitbox | ff (w, h) | Sets caller's hitbox width to %1 and height to %2. | 是 | 继承自 TH13 |
| 502 | flagSet | S (n) | Sets flag(s) according to %1. Refer to the [flag table](#s=modding/flags) for exact values. | 是 | 继承自 TH13 |
| 503 | flagClear | S (n) | Clears flag(s) according to %1. Refer to the [flag table](#s=modding/flags) for exact values. | 是 | 继承自 TH13 |
| 504 | moveLimit | ffff (x, y, w, h) | Sets caller's movement limit rectangle: (%1,%2) are the coordinates of the center of the rect, while %3, %4 are width and height of it. | 是 | 继承自 TH13 |
| 505 | moveLimitReset | — | Removes caller's movement limit. | 是 | 继承自 TH13 |
| 506 | dropClear | — | Clears caller's extra item drop. | 是 | 继承自 TH13 |
| 507 | dropExtra | SS (type, amount) | Adds %2 items of type %1 to caller's extra drop. Item type table will be made in the future. | 是 | 继承自 TH13 |
| 508 | dropArea | ff (w, h) | Sets caller's item drop area width to %1 and height to %2. | 是 | 继承自 TH13 |
| 509 | dropItems | — | Drops all items the caller has. Has no effect in spell practice. | 是 | 继承自 TH13 |
| 510 | dropMain | S (type) | Sets caller's main drop to %1. | 是 | 继承自 TH13 |
| 511 | lifeSet | S (hp) | Sets caller's current HP and max HP to %1. | 是 | 继承自 TH13 |
| 512 | setBoss | S (a) | If %1 is 0, activates boss mode and makes the caller the main boss. If %1 > 0, it makes the caller the secondary boss. If %1 is -1, ends boss mode. | 是 | 继承自 TH13 |
| 513 | timerReset | — | Resets boss timer. | 是 | 继承自 TH13 |
| 514 | setInterrupt | SSSm (slot, hp, time, sub) | Sets an interrupt on slot %1 (not sure how many slots there are) - once caller's hp reaches %2 or %3 frames have passed since this was called, caller will terminate all subs it's currently running and execute sub %4. | 是 | 继承自 TH13 |
| 515 | setInvuln | S (time) | Makes the caller completely invulnerable for %1 frames. | 是 | 继承自 TH13 |
| 516 | playSound | S (id) | Plays sound %1. Sound id table will be added in the future. | 是 | 继承自 TH13 |
| 517 | setScreenShake | SSS (time, startIntensity, endIntensity) | Activates screen shake for %1 frames. %2 is the starting intensity and %3 is the ending intensity. The larger the intensity, the more the screen shakes. | 是 | 继承自 TH13 |
| 518 | dialogRead | S (dialogueId) | Starts a dialogue, %1 is the ID of an entry in the .msg file. Apart from that, has the effect ins_525. | 是 | 继承自 TH13 |
| 519 | dialogWait | — | Waits until there are no dialogues active, or the running .msg script calls a certain instruction (which one?) | 否/待确认 | 继承自 TH13 |
| 520 | bossWait | — | Waits until there are no boss enemies. | 是 | 继承自 TH13 |
| 521 | setTimeout | Sm (slot, sub) | Sets a timeout interrupt on slot %1 - when the timer reaches 0, caller will terminate all subs it's currently running and execute sub %2. | 是 | 继承自 TH13 |
| 522 | spellEx | SSSm (id, time, type, name) | Same as ins_537, but the difficulty number is NOT added to the id. | 是 | 继承自 TH16 |
| 523 | spellEnd | — | Ends currently active spellcard. | 是 | 继承自 TH13 |
| 524 | setChapter | S (a) | Some jank that's responsible for showing boss name and possibly other things. In LoLK, it also ends the current chapter and begins a new one. | 否/待确认 | 继承自 TH13 |
| 525 | enmKillAll | — | Kills all other enemies (unless they have a flag that prevents that set). | 是 | 继承自 TH13 |
| 526 | etProtectRange | f (r) | Makes bullets generated by the caller not spawn if they are in radius %1 around the player. | 是 | 继承自 TH13 |
| 527 | lifeMarker | SfS (slot, hp, c) | Sets a new life marker on slot %1, %2 determines where the marker will appear on the health bar (if %2=1000.0f and the enemy has 2000 hp, the marker will split the hp bar in half). %3 is an RGB value of unknown use (possibly leftover from earlier ECL versions) | 是 | 继承自 TH13 |
| 528 | spellUnused | SSSm (id, time, type, name) | No difference from ins_522, unused. | 是 | 继承自 TH16 |
| 529 | rankF3 | ffff (var, a, b, c) | Sets %1 to %2 if rank is low, %3 if rank is average or %4 if rank is high. | 是 | 继承自 TH13 |
| 530 | rankF5 | ffffff (var, a, b, c, d, e) | Sets %1 to %2 if rank is very low, %3 if rank is low, %4 if rank is average, %5 if rank is high or %6 if rank is very high. | 是 | 继承自 TH13 |
| 531 | rankF2 | fff (var, a, b) | Sets %1 to %2 if rank is low or %3 if rank is high. | 是 | 继承自 TH13 |
| 532 | rankI3 | SSSS (var, a, b, c) | Sets %1 to %2 if rank is low, %3 if rank is average or %4 if rank is high. | 是 | 继承自 TH13 |
| 533 | rankI5 | SSSSSS (var, a, b, c, d, e) | Sets %1 to %2 if rank is very low, %3 if rank is low, %4 if rank is average, %5 if rank is high or %6 if rank is very high. | 是 | 继承自 TH13 |
| 534 | rankI2 | SSS (var, a, b) | Sets %1 to %2 if rank is low or %3 if rank is high. | 是 | 继承自 TH13 |
| 535 | diffI | SSSSS (var, E, N, H, L) | Sets %1 to one of values provided based on difficulty. | 是 | 继承自 TH13 |
| 536 | diffF | fffff (var, E, N, H, L) | Sets %1 to one of values provided based on difficulty. | 是 | 继承自 TH13 |
| 537 | spell | SSSm (id, time, mode, name) | Declares a spellcard with id %1 and name %4. The actual ID passed to the spell-creating function is `id + difficulty`, with easy=0, normal=1, hard=2, lunatic=3, ex=4, overdrive=5. <br>%2 determines how much time the spell circle takes to shrink (in frames), as well as how fast the spell bonus decreases. The exact formula is as follows: <br>[code] int factor = maxSCB >> 2; // maxSCB is hardcoded<br> currSCB -= (maxSCB - factor) / (%2 - 300);<br> currSCB -= currSCB % 10; [/code] <br>As you can guess, setting %2 to 300 causes a division by 0 error and crashes the game, while setting it to a value smaller than 300 causes the SCB to increase over time, instead of decreasing. %3 TBD, it's not unused. | 是 | 继承自 TH16 |
| 538 | spell2 | SSSm (id, time, mode, name) | Same as ins_537, except the ID used it `id - 1 + difficulty`. | 是 | 继承自 TH16 |
| 539 | spell3 | SSSm (id, time, mode, name) | Same as ins_537, except the ID used it `id - 2 + difficulty`. | 是 | 继承自 TH16 |
| 540 | stars | S (cnt) | Sets the amount of stars displayed in the top left corner. Stars might not appear at all if there is no boss active. | 是 | 继承自 TH13 |
| 541 | noHitboxDur | S (time) | Disables the hitbox (but not the hurtbox) for the given amount of frames. | 是 | 继承自 TH13 |
| 542 | spellTimeout | — | Makes the current spell a timeout spell (prevent spell bonus from decreasing, give capture bonus if timed out). | 是 | 继承自 TH13 |
| 543 | unknown543 | — | Unknown. | 否/待确认 | 继承自 TH13 |
| 544 | unknown544 | S (a) | Unknown, sets or clears some flag? | 否/待确认 | 继承自 TH13 |
| 545 | laserCancel | — | Cancels all lasers. | 是 | 继承自 TH13 |
| 546 | bombShield | SS (a, script) | Sets the bomb invulnerability flag (%1=1 set, %1=0 not set), the caller's ANM script will change to %2 when a bomb is active (how does it work with ANM slots exactly?) | 是 | 继承自 TH13 |
| 547 | gameSpeed | f (s) | Sets game speed to %1 of the normal speed. In ISC, enemies with flag 13 (dec=8192) set will ignore effects of this opcode. | 是 | 继承自 TH13 |
| 548 | diffWait | SSSS (e, n, h, l) | Same as ins_23, but the wait time is chosen from the given 4 based on the difficulty. | 是 | 继承自 TH13 |
| 549 | unknown549 | S (a) | Unknown. | 否/待确认 | 继承自 TH13 |
| 550 | unknown550 | S (a) | Unknown. | 否/待确认 | 继承自 TH13 |
| 551 | unknown551 | S (a) | Unknown. | 否/待确认 | 继承自 TH13 |
| 552 | zIndex | S (layers) | Increases layer of all ANM scripts used by the caller by %1. | 是 | 继承自 TH13 |
| 553 | hitSound | S (id) | Makes the caller play sound %1 when hit. Sound id table will be added in the future. | 是 | 继承自 TH13 |
| 554 | stageLogo | — | Shows the stage logo from an ANM of a hardcoded name. | 是 | 继承自 TH13 |
| 555 | enmAlive | SS (var, id) | Checks if enemy of var_-9914 == %2 is still alive, and sets %1 to 1 if it is or 0 if it isn't. | 是 | 继承自 TH13 |
| 556 | setDeath | m (sub) | Makes the caller execute sub %1 when the HP reaches 0. Keep in mind that the caller is already marked for deletion at the point when the sub actually executes, so if you put waiting there the sub will not execute fully (because the caller will be deleted) | 是 | 继承自 TH13 |
| 557 | fogTime | SSSff (time, mode, color, start, end) | Same as STD ins_9, that is, fogTime. Refer to [the STD instruction table](#s=modding/std-ins) for details. | 是 | 继承自 TH13 |
| 558 | flagMirror | S (state) | Literally the exact same instruction as ins_424. | 是 | 继承自 TH13 |
| 559 | enmLimit | S (limit) | Set the maximum number of enemies that can be present. New enemies will fail to spawn if the cap is reached. Default is 99999. | 是 | 继承自 TH13 |
| 560 | unknown560 | ff (r, s) | Unknown. | 否/待确认 | 继承自 TH13 |
| 561 | die | — | Makes the caller execute the sub set with ins_556. If there is no such sub set, the caller dies instead (exactly the same as if the player shot down the caller, that is, items are dropped, death sound plays etc) | 是 | 继承自 TH13 |
| 562 | dropItemsSp | — | Same as ins_509, but item spawning will not be blocked in spell practice. | 是 | 继承自 TH13 |
| 563 | unknown563 | S (flagState) | Sets [flag 12](#s=modding/flags) (decimal 4096), which controls whether the hitbox and hurtbox is a rectangle. If %1 is 1, collision is a rectangle. If %1 is 0, collision is elliptical. | 是 | 继承自 TH14 |
| 564 | hitboxRotate | f (angle) | Rotates the hitbox and hurtbox of the enemy (note: the hitbox rotation is really janky, but hurtbox rotates fine). Has no effect unless the enemy uses rectangular collision. | 是 | 继承自 TH14 |
| 565 | bombInvuln | f (red) | Sets caller's damage reduction when a bomb is active, 0.0f means no damage at all, 1.0f is full damage, negative values will make the enemy heal when you bomb. | 是 | 继承自 TH14 |
| 566 | unknown566 | () | Unknown (does it even exist?) | 否/待确认 | 继承自 TH14 |
| 567 | unknown567 | S (a) | Unknown. | 否/待确认 | 继承自 TH14 |
| 568 | spellMode | S (state) | Enables/disables spell card damage reduction, if %1 is 1 it's enabled, if it's 0 it's disabled. Can be used outside of spell cards. | 是 | 继承自 TH14 |
| 569 | unknown569 | S (a) | Unknown. | 否/待确认 | 继承自 TH15 |
| 570 | unknown570 | — | Unknown. | 否/待确认 | 继承自 TH15 |
| 571 | unknown571 | — | Unknown. | 否/待确认 | 继承自 TH15 |
| 572 | lifeNow | S (hp) | Sets caller's current HP to %1, without changing max HP. | 是 | 继承自 TH16 |

### TH17 指令：子弹创建与删除 / Bullet creation and deletion

| ID | 助记名 | 参数 | 说明 | 文档化 | 来源 |
| --- | --- | --- | --- | --- | --- |
| 600 | etNew | S (etId) | Resets bullet manager %1 to default properties. | 是 | 继承自 TH13 |
| 601 | etOn | S (etId) | Shoots bullet(s) using properties from bullet manager %1. | 是 | 继承自 TH13 |
| 602 | etSprite | SSS (etId, type, color) | Sets bullet type and color of bullet manager %1. Refer to [this image](https://cdn.discordapp.com/attachments/395767870119870466/570658618316161041/BULLET_IDS.png) made by Dai. Remarks:<br>- bullet types 35 and 36 spin<br>- type 30 pulses<br>- the difference between 16/37 is the spin direction (same case for 23 and 24) | 是 | 继承自 TH15 |
| 603 | etOffset | Sff (etId, x, y) | Sets the relative offset of bullets spawned by bullet manager %1 to (%2,%3). | 是 | 继承自 TH13 |
| 604 | etAngle | Sff (etId, angle1, angle2) | Sets angle1 and angle2 of bullet manager %1. | 是 | 继承自 TH13 |
| 605 | etSpeed | Sff (etId, speed1, speed2) | Sets speed1 and speed2 of bullet manager %1. | 是 | 继承自 TH13 |
| 606 | etCount | SSS (etId, count1, count2) | Sets count1 and count2 of bullet manager %1. | 是 | 继承自 TH13 |
| 607 | etAim | SS (etId, aim) | Sets aim mode of bullet manager %1. | 是 | 继承自 TH13 |
| 608 | etSound | SSS (etId, sound1, sound2) | Sets sound1 and sound2 of bullet manager %1 (sound effect table is TODO). sound1 plays when the bullet manager fires a bullet, while sound2 plays when a bullet fired by the bullet manager does certain transformations. Set to -1 for no sound. | 是 | 继承自 TH13 |
| 609 | etExSet | SSSSSSff (etId, index, async, type, a, b, r, s) | Sets bullet transformation of bullet manager %1, transformation explanation will be added in the future. | 是 | 继承自 TH13 |
| 610 | etExSet2 | SSSSSSSSffff (etId, index, async, type, a, b, c, d, r, s, m, n) | Same as ins_609, but takes more arguments for certain transformation types. | 是 | 继承自 TH13 |
| 611 | etEx | SSSSSff (etId, async, type, a, b, r, s) | Adds bullet transformation to bullet manager %1, transformation explanation will be added in the future. | 是 | 继承自 TH13 |
| 612 | etEx2 | SSSSSSSffff (etId, async, type, a, b, c, d, r, s, m, n) | Same as ins_611, but takes more arguments for certain transformation types. | 是 | 继承自 TH13 |
| 613 | etClearAll | — | Clears all bullets. | 是 | 继承自 TH13 |
| 614 | etCopy | SS (etIdDest, etIdSrc) | Copies everything from bullet manager %2 into bullet manager %1. Warning: this instruction is partially broken and does NOT copy the index next ins_611/ins_612 transformations will be added at. | 是 | 继承自 TH13 |
| 615 | etCancel | f (r) | Clears all bullets in a circle of radius %1 around the caller, and turns them into cancel items. | 是 | 继承自 TH13 |
| 616 | etClear | f (r) | Clears all bullets in a circle of radius %1 around the caller without turning them into cancel items. | 是 | 继承自 TH13 |
| 617 | etSpeedR3 | Sffffff (etId, spd1l, spd1m, spd1h, spd2l, spd2m, spd2h) | Sets speed1 and speed2 of bullet manager %1 to two of the values provided, based on ingame rank (l=low, m=medium, h=high) | 是 | 继承自 TH13 |
| 618 | etSpeedR5 | Sffffffffff (etId, spd1l, spd1ml, spd1m, spd1mh, spd1h, spd2l, spd2ml, spd2m, spd2mh, spd2h) | Sets speed1 and speed2 of bullet manager %1 to two of the values provided, based on ingame rank (l=low, ml=medium-low, m=medium, mh=medium-high, h=high) | 是 | 继承自 TH13 |
| 619 | etSpeedR2 | Sffff (etId, spd1l, spd1h, spd2l, spd2h) | Sets speed1 and speed2 of bullet manager %1 to two of the values provided, based on ingame rank (l=low, h=high) | 是 | 继承自 TH13 |
| 620 | etCountR3 | SSSSSSS (etId, cnt1l, cnt1m, cnt1h, cnt2l, cnt2m, cnt2h) | Sets count1 and count2 of bullet manager %1 to two of the values provided, based on ingame rank (l=low, m=medium, h=high) | 是 | 继承自 TH13 |
| 621 | etCountR5 | SSSSSSSSSSS (etId, cnt1l, cnt1ml, cnt1m, cnt1mh, cnt1h, cnt2l, cnt2ml, cnt2m, cnt2mh, cnt2h) | Sets count1 and count2 of bullet manager %1 to two of the values provided, based on ingame rank (l=low, ml=medium-low, m=medium, mh=medium-high, h=high) | 是 | 继承自 TH13 |
| 622 | etCountR2 | SSSSS (etId, cnt1l, cnt1h, cnt2l, cnt2h) | Sets count1 and count2 of bullet manager %1 to two of the values provided, based on ingame rank (l=low, h=high) | 是 | 继承自 TH13 |
| 623 | angleToPlayer | fff (var, x, y) | Gets angle to the player from coordinates (%2,%3) and stores it in %1. | 是 | 继承自 TH13 |
| 624 | etSpeedD | Sffffffff (etId, spd1e, spd1n, spd1h, spd1l, spd2e, spd2n, spd2h, spd2l) | Sets speed1 and speed2 of bullet manager %1 to 2 of the values provided, based on the difficulty (e=easy, n=normal, h=hard, l=lunatic) | 是 | 继承自 TH13 |
| 625 | etCountD | SSSSSSSSS (etId, cnt1e, cnt1n, cnt1h, cnt1l, cnt2e, cnt2n, cnt2h, cnt2l) | Sets count1 and count2 of bullet manager %1 to 2 of the values provided, based on the difficulty (e=easy, n=normal, h=hard, l=lunatic) | 是 | 继承自 TH13 |
| 626 | etOffsetRad | Sff (etId, angle, radius) | Sets the relative offset of bullets spawned by bullet manager %1 to (cos(%2)\*%3,sin(%2)\*%3). Stacks with ins_603. | 是 | 继承自 TH13 |
| 627 | etDist | Sf (etId, dist) | Sets distance of bullets spawned by bullet manager %1 to %2 (that is, when a bullet is spawned it moves by %2 using its current angle). | 是 | 继承自 TH13 |
| 628 | etOffsetAbs | Sff (etId, x, y) | Sets the absolute offset of bullets spawned by bullet manager %1 to (%2,%3). | 是 | 继承自 TH13 |
| 629 | fog | fS (r, color) | Sets caller's fog's radius to %1 and color to %2 (RGB value in reverse order). This resets the fog completely, that is, every time it's called the fog spawn animation plays. | 是 | 继承自 TH13 |
| 630 | callSTD | S (switch) | Sets execution pointer of the STD script to where STD ins_16(%1) is (%1 must be the same), basically same concept as ins_317. | 是 | 继承自 TH13 |
| 631 | lifeHide | S (time) | Hides boss lifebar for %1 frames. | 是 | 继承自 TH13 |
| 632 | funcSet | S (id) | Sets a function that the game will execute every frame from a set of hardcoded functions that differs between games. | 是 | 继承自 TH13 |
| 633 | flagExtDmg | S (state) | Sets the external damage flag to %1. Caller probably needs to be the main boss for this to work - with this flag set, the caller gets damaged by the value stored in var_-9940 every frame, and then resets the value. This allows other enemies to damage the boss by incrementing the aforementioned variable, used in LoLK by Sagume (and also happens to be the main cause of the Sagume skip glitch) | 是 | 继承自 TH13 |
| 634 | setHitboxFunc | S (id) | Make the caller use a special function for determining collision with the player. TODO: create a list of functions and their IDs | 是 | 继承自 TH13 |
| 635 | etCancel2 | f (r) | Same as ins_615, but doesn't clear bullets with bomb invulnerability. | 是 | 继承自 TH13 |
| 636 | etClear2 | f (r) | Same as ins_616, but doesn't clear bullets with bomb invulnerability. | 是 | 继承自 TH13 |
| 637 | funcCall | S (id) | Same as ins_632, except the function is called just once instead of every frame. | 是 | 继承自 TH13 |
| 638 | scoreAdd | S (n) | Adds %1 to score (or subtracts if %1 is negative). There is no lower boundary check, so if this causes score to go below 0, an underflow happens. | 是 | 继承自 TH13 |
| 639 | funcSet2 | S (id) | Same as ins_632, except it sets an unknown flag to 1 (ins_632 sets it to 0) | 是 | 继承自 TH13 |
| 640 | etExSub | SSm (etId, index, s) | Sets the string parameter of transform on index %2 in bullet manager %1 to %3, transformations will be explained separately later. | 是 | 继承自 TH13 |
| 641 | etExSubtract | S (etId) | Subtracts 1 from the index used by ins_611 and ins_612, unless it's already 0. This basically changes where the next transformation will be appended. | 是 | 继承自 TH14 |

### TH17 指令：激光创建 / Laser creation

| ID | 助记名 | 参数 | 说明 | 文档化 | 来源 |
| --- | --- | --- | --- | --- | --- |
| 700 | laserNew | Sffff (etId, init_length, final_length, unknown_arg_3, width) | Sets basic parameters of the laser. %4 has something to do with the length of straight line lasers (investigation needed), but doesn't do anything for other laser types. For curvy lasers, the only used argument is %5, and length is specified with ins_701 instead. | 是 | 继承自 TH13 |
| 701 | laserTiming | SSSSSS (edId, startup_time, expand_time, duration, shrink_time, init_flags) | Sets timing for infinite lasers. %6 sets the initial flags for a laser, but these flags are unknown at the moment. For curvy lasers, the %2 argument instead specifies the length of the laser. | 是 | 继承自 TH13 |
| 702 | laserOn | S (edId) | Shoots a straight line laser. | 是 | 继承自 TH13 |
| 703 | laserStOn | SS (etId, laser_id) | Shoots an infinite laser. %2 is a number that's used to identify this particular laser instance, so that it can be referred to in other instructions. | 是 | 继承自 TH13 |
| 704 | laserOffset | Sff (laser_id, x, y) | Sets the position of the infinite laser pointed to by %1. | 是 | 继承自 TH13 |
| 705 | laserTrajectory | Sff (laser_id, x_speed, y_speed) | Sets the offset velocity of the infinite laser pointed to by %1. The laser's position will change by %2 and %3 every frame. | 是 | 继承自 TH13 |
| 706 | laserStLength | Sf (laser_id, speed) | Sets the speed of the infinite laser pointed to by %1. | 是 | 继承自 TH13 |
| 707 | laserStWidth | Sf (laser_id, width) | Sets the width of the infinite laser pointed to by %1. | 是 | 继承自 TH13 |
| 708 | laserStAngle | Sf (laser_id, angle) | Sets the angle of the infinite laser pointed to by %1. | 是 | 继承自 TH13 |
| 709 | laserStRotation | Sf (laser_id, angular_vel) | Sets the angular velocity of the infinite laser pointed to by %1. The laser's angle will change by %2 every frame. | 是 | 继承自 TH13 |
| 710 | laserStEnd | S (laser_id) | Clears the laser pointed to by %1. | 是 | 继承自 TH13 |
| 711 | laserCuOn | S (etId) | Shoots a curvy laser. | 是 | 继承自 TH13 |
| 712 | etCancelRect | ff (w, h) | Cancels all bullets in rectangle of width %1 and height %2. The area is affected by rotation set by ins_564. | 是 | 继承自 TH14 |
| 713 | unknown713 | SS (etId, laser_id) | Shoots a laser 'beam', a laser type used by marisa in GFW. Broken since this laser type does not exist outside of GFW. | 是 | 继承自 TH13 |
| 714 | unknown714 | SS (laser_id, unknown) | Does something with a laser beam pointed to by %1. Broken since this laser type does not exist outside of GFW. | 是 | 继承自 TH13 |

### TH17 指令：敌机交互 / Enemy interaction

| ID | 助记名 | 参数 | 说明 | 文档化 | 来源 |
| --- | --- | --- | --- | --- | --- |
| 800 | enmCall | Sm (id, sub) | Makes enemy with var_-9914 == %1 stop all subs it's running and execute sub %2 (works like an interrupt). This will NOT make the enemy execute the sub right as this instruction is called, the new sub will be executed when the game handles the given enemy, which might be later on the same frame or on the next frame. Using this to make the caller interrupt itself can make the game explode. | 是 | 继承自 TH13 |
| 801 | enmPos | ffS (varX, varY, id) | Stores coordinates of enemy with var_-9914 == %3 in (%1,%2). | 是 | 继承自 TH13 |
| 802 | broadcastInterrupt | S (slot) | For all existing bosses, trigger the interrupt set by ins_514 on slot %1. Does not change the HP to the one set in ins_514. | 是 | 继承自 TH13 |

### TH17 指令：调试 / Debug

| ID | 助记名 | 参数 | 说明 | 文档化 | 来源 |
| --- | --- | --- | --- | --- | --- |
| 900 | debug900 | — | 未在 Priw8 表中记录/待确认 | 否/待确认 | — |
| 901 | debug901 | — | 未在 Priw8 表中记录/待确认 | 否/待确认 | — |
| 902 | debug902 | — | 未在 Priw8 表中记录/待确认 | 否/待确认 | — |
| 903 | debug903 | — | 未在 Priw8 表中记录/待确认 | 否/待确认 | — |
| 904 | debug904 | — | 未在 Priw8 表中记录/待确认 | 否/待确认 | — |

### TH17 指令：游戏特有 / Game specific

| ID | 助记名 | 参数 | 说明 | 文档化 | 来源 |
| --- | --- | --- | --- | --- | --- |
| 1000 | spec0 | — | 未在 Priw8 表中记录/待确认 | 否/待确认 | — |
| 1001 | spec1 | — | 未在 Priw8 表中记录/待确认 | 否/待确认 | — |
| 1002 | spec2 | — | 未在 Priw8 表中记录/待确认 | 否/待确认 | — |
| 1003 | spec3 | — | 未在 Priw8 表中记录/待确认 | 否/待确认 | — |
| 1004 | spec4 | — | 未在 Priw8 表中记录/待确认 | 否/待确认 | — |
| 1005 | spec5 | — | 未在 Priw8 表中记录/待确认 | 否/待确认 | — |
| 1006 | spec6 | — | 未在 Priw8 表中记录/待确认 | 否/待确认 | — |
| 1007 | spec7 | — | 未在 Priw8 表中记录/待确认 | 否/待确认 | — |
| 1008 | spec8 | — | 未在 Priw8 表中记录/待确认 | 否/待确认 | — |
| 1009 | spec9 | — | 未在 Priw8 表中记录/待确认 | 否/待确认 | — |
| 1010 | spec10 | — | 未在 Priw8 表中记录/待确认 | 否/待确认 | — |
| 1011 | spec11 | — | 未在 Priw8 表中记录/待确认 | 否/待确认 | — |
| 1012 | spec12 | — | 未在 Priw8 表中记录/待确认 | 否/待确认 | — |
| 1013 | spec13 | — | 未在 Priw8 表中记录/待确认 | 否/待确认 | — |
| 1014 | spec14 | — | 未在 Priw8 表中记录/待确认 | 否/待确认 | — |
| 1015 | spec15 | — | 未在 Priw8 表中记录/待确认 | 否/待确认 | — |
| 1016 | spec16 | — | 未在 Priw8 表中记录/待确认 | 否/待确认 | — |
| 1017 | spec17 | — | 未在 Priw8 表中记录/待确认 | 否/待确认 | — |
| 1018 | spec18 | — | 未在 Priw8 表中记录/待确认 | 否/待确认 | — |
| 1019 | spec19 | — | 未在 Priw8 表中记录/待确认 | 否/待确认 | — |
| 1020 | spec20 | — | 未在 Priw8 表中记录/待确认 | 否/待确认 | — |
| 1021 | ins_1021 | — | 未在 Priw8 表中记录/待确认 | 否/待确认 | — |
| 1022 | ins_1022 | — | 未在 Priw8 表中记录/待确认 | 否/待确认 | — |
| 1023 | ins_1023 | — | 未在 Priw8 表中记录/待确认 | 否/待确认 | — |
| 1024 | ins_1024 | — | 未在 Priw8 表中记录/待确认 | 否/待确认 | — |
| 1025 | ins_1025 | — | 未在 Priw8 表中记录/待确认 | 否/待确认 | — |

### TH17 变量

| ID | 名称 | 类型 | 访问 | 作用域 | 说明 | 文档化 | 来源 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| -10000 | RAND | int | 只读 | global/全局 | Random integer, very large range. | 是 | 继承自 TH10 |
| -9999.0f | RANDF | float | 只读 | global/全局 | Random float from 0.0f to 1.0f. | 是 | 继承自 TH10 |
| -9998.0f | RANDRAD | float | 只读 | global/全局 | Random float from -pi to pi. | 是 | 继承自 TH10 |
| -9997.0f | FINAL_X | float | 只读 | local/敌机局部 | Final X position of the enemy. | 是 | 继承自 TH10 |
| -9996.0f | FINAL_Y | float | 只读 | local/敌机局部 | Final Y position of the enemy. | 是 | 继承自 TH10 |
| -9995.0f | ABS_X | float | 只读 | local/敌机局部 | Absolute X position of the enemy. | 是 | 继承自 TH10 |
| -9994.0f | ABS_Y | float | 只读 | local/敌机局部 | Absolute Y position of the enemy. | 是 | 继承自 TH10 |
| -9993.0f | REL_X | float | 只读 | local/敌机局部 | Relative X position of the enemy. | 是 | 继承自 TH10 |
| -9992.0f | REL_Y | float | 只读 | local/敌机局部 | Relative Y position of the enemy. | 是 | 继承自 TH10 |
| -9991.0f | PLAYER_X | float | 只读 | global/全局 | Player's X position. | 是 | 继承自 TH10 |
| -9990.0f | PLAYER_Y | float | 只读 | global/全局 | Player's Y position. | 是 | 继承自 TH10 |
| -9989.0f | ANGLE_PLAYER | float | 只读 | local/敌机局部 | Angle from the enemy to the player. | 是 | 继承自 TH10 |
| -9988 | TIME | int | 只读 | local/敌机局部 | Time elapsed since the enemy spawned, in frames. | 是 | 继承自 TH10 |
| -9987.0f | RANDF2 | float | 只读 | global/全局 | Random float from -1.0f to 1.0f. | 是 | 继承自 TH10 |
| -9986 | TIMEOUT | int | 只读 | global/全局 | Set to 1 by the engine when a timeout occurs. | 是 | 继承自 TH10 |
| -9985 | I0 | int | 读写 | local/敌机局部 | Local integer variable, inherited by spawned enemies. | 是 | 继承自 TH10 |
| -9984 | I1 | int | 读写 | local/敌机局部 | Local integer variable, inherited by spawned enemies. | 是 | 继承自 TH10 |
| -9983 | I2 | int | 读写 | local/敌机局部 | Local integer variable, inherited by spawned enemies. | 是 | 继承自 TH10 |
| -9982 | I3 | int | 读写 | local/敌机局部 | Local integer variable, inherited by spawned enemies. | 是 | 继承自 TH10 |
| -9981.0f | F0 | float | 读写 | local/敌机局部 | Local float variable, inherited by spawned enemies. | 是 | 继承自 TH10 |
| -9980.0f | F1 | float | 读写 | local/敌机局部 | Local float variable, inherited by spawned enemies. | 是 | 继承自 TH10 |
| -9979.0f | F2 | float | 读写 | local/敌机局部 | Local float variable, inherited by spawned enemies. | 是 | 继承自 TH10 |
| -9978.0f | F3 | float | 读写 | local/敌机局部 | Local float variable, inherited by spawned enemies. | 是 | 继承自 TH10 |
| -9977.0f | FINAL_X2 | float | 只读 | local/敌机局部 | Same as var_-9997. | 是 | 继承自 TH10 |
| -9976.0f | FINAL_Y2 | float | 只读 | local/敌机局部 | Same as var_-9996. | 是 | 继承自 TH10 |
| -9975.0f | ABS_X2 | float | 只读 | local/敌机局部 | Same as var_-9995. | 是 | 继承自 TH10 |
| -9974.0f | ABS_Y2 | float | 只读 | local/敌机局部 | Same as var_-9994. | 是 | 继承自 TH10 |
| -9973.0f | REL_X2 | float | 只读 | local/敌机局部 | Same as var_-9993. | 是 | 继承自 TH10 |
| -9972.0f | REL_Y2 | float | 只读 | local/敌机局部 | Same as var_-9992. | 是 | 继承自 TH10 |
| -9971.0f | ABS_ANGLE | float | 只读 | local/敌机局部 | Angle of enemy's absolute movement. | 是 | 继承自 TH10 |
| -9970.0f | REL_ANGLE | float | 只读 | local/敌机局部 | Angle of enemy's relative movement. | 是 | 继承自 TH10 |
| -9969.0f | ABS_SPEED | float | 只读 | local/敌机局部 | Speed of enemy's absolute movement. | 是 | 继承自 TH10 |
| -9968.0f | REL_SPEED | float | 只读 | local/敌机局部 | Speed of enemy's relative movement. | 是 | 继承自 TH10 |
| -9967.0f | ABS_ORIGIN_DIST | float | 只读 | local/敌机局部 | Distance from the origin of enemy's absolute circular movement (radius of the circle). | 是 | 继承自 TH10 |
| -9966.0f | REL_ORIGIN_DIST | float | 只读 | local/敌机局部 | Distance from the origin of enemy's relative circular movement (radius of the circle). | 是 | 继承自 TH10 |
| -9965.0f | PLAYER_X2 | float | 只读 | global/全局 | Same as var_-9991. | 是 | 继承自 TH10 |
| -9964.0f | PLAYER_Y2 | float | 只读 | global/全局 | Same as var_-9990. | 是 | 继承自 TH10 |
| -9963.0f | BOSS_X | float | 只读 | global/全局 | Final X position of the boss. | 是 | 继承自 TH10 |
| -9962.0f | BOSS_Y | float | 只读 | global/全局 | Final Y position of the boss. | 是 | 继承自 TH10 |
| -9961 | ANM_ID | int | 只读 | local/敌机局部 | Is the current script on anm slot 0 of the enemy. | 是 | 继承自 TH10 |
| -9960 | RANK | int | 只读 | global/全局 | Numeric value of rank, ranging from -1024 to 1024. Increases over time and decreases when player bombs/dies etc. | 是 | 继承自 TH10 |
| -9959 | DIFF | int | 只读 | global/全局 | Difficulty (E=0, N=1, H=2, L=3, EX=4, O=5) | 是 | 继承自 TH10 |
| -9958.0f | FINAL_ANGLE | float | 只读 | local/敌机局部 | Final angle of enemy's movement. | 是 | 继承自 TH10 |
| -9957 | TRUE | int | 只读 | global/全局 | Always returns 1. | 是 | 继承自 TH10 |
| -9956.0f | ABS_ANGLE_PLAYER | float | 只读 | local/敌机局部 | Angle to the player from enemy's absolute position. | 是 | 继承自 TH10 |
| -9955.0f | REL_ANGLE_PLAYER | float | 只读 | local/敌机局部 | Angle to the player from enemy's relative position. | 是 | 继承自 TH10 |
| -9954 | LIFE | int | 只读 | local/敌机局部 | Enemy's current HP. | 是 | 继承自 TH10 |
| -9953 | EASY | int | 只读 | global/全局 | Set to 1 if difficulty is easy, otherwise it's 0. | 是 | 继承自 TH10 |
| -9952 | NORMAL | int | 只读 | global/全局 | Set to 1 if difficulty is normal, otherwise it's 0. | 是 | 继承自 TH10 |
| -9951 | HARD | int | 只读 | global/全局 | Set to 1 if difficulty is hard, otherwise it's 0. | 是 | 继承自 TH10 |
| -9950 | LUNATIC | int | 只读 | global/全局 | Set to 1 if difficulty is lunatic, otherwise it's 0. | 是 | 继承自 TH10 |
| -9949 | MISS_COUNT | int | 读写 | global/全局 | Increased by 1 every time the player dies. | 是 | 继承自 TH11 |
| -9948 | BOMB_COUNT | int | 读写 | global/全局 | Increased by 1 every time the player bombs. | 是 | 继承自 TH11 |
| -9947 | CAPTURE | int | 读写 | global/全局 | Set to 0 when the player dies, bombs, or uses a game-specific mechanic that "fails" a spell. | 是 | 继承自 TH11 |
| -9946 | ENM_CNT_REAL | int | 只读 | global/全局 | Amount of enemies alive (including main and MapleEnemy). | 是 | 继承自 TH11 |
| -9945 | SHOTTYPE | int | 只读 | global/全局 | Numeric value that represents player's shottype, the first shottype is 0. | 是 | 继承自 TH11 |
| -9944.0f | DIST_PLAYER | float | 只读 | local/敌机局部 | Distance from the enemy to the player. | 是 | 继承自 TH11 |
| -9943 | BI0 | int | 读写 | local/敌机局部 | Is the same as the I0 variable of boss 0. | 是 | 继承自 TH11 |
| -9942 | BI1 | int | 读写 | local/敌机局部 | Is the same as the I1 variable of boss 0. | 是 | 继承自 TH11 |
| -9941 | BI2 | int | 读写 | local/敌机局部 | Is the same as the I2 variable of boss 0. | 是 | 继承自 TH11 |
| -9940 | BI3 | int | 读写 | local/敌机局部 | Is the same as the I3 variable of boss 0. | 是 | 继承自 TH11 |
| -9939.0f | BF0 | float | 读写 | local/敌机局部 | Is the same as the F0 variable of boss 0. | 是 | 继承自 TH11 |
| -9938.0f | BF1 | float | 读写 | local/敌机局部 | Is the same as the F1 variable of boss 0. | 是 | 继承自 TH11 |
| -9937.0f | BF2 | float | 读写 | local/敌机局部 | Is the same as the F2 variable of boss 0. | 是 | 继承自 TH11 |
| -9936.0f | BF3 | float | 读写 | local/敌机局部 | Is the same as the F3 variable of boss 0. | 是 | 继承自 TH11 |
| -9935.0f | F4 | float | 读写 | local/敌机局部 | Local float variable inherited by spawned enemies, just like F0-F3 and I0-I3. | 是 | 继承自 TH11 |
| -9934.0f | F5 | float | 读写 | local/敌机局部 | Local float variable inherited by spawned enemies, just like F0-F3 and I0-I3. | 是 | 继承自 TH11 |
| -9933.0f | F6 | float | 读写 | local/敌机局部 | Local float variable inherited by spawned enemies, just like F0-F3 and I0-I3. | 是 | 继承自 TH11 |
| -9932.0f | F7 | float | 读写 | local/敌机局部 | Local float variable inherited by spawned enemies, just like F0-F3 and I0-I3. | 是 | 继承自 TH11 |
| -9931 | LAST_ENM_ID | int | 只读 | global/全局 | ID of the last spawned enemy. | 是 | 继承自 TH12 |
| -9930 | POWER | int | 只读 | global/全局 | Player's power (4.00 => 400) | 是 | 继承自 TH12 |
| -9929 | DS1 | int | 只读 | global/全局 | Used in Double Spoiler, unknown. | 否/待确认 | 继承自 TH12.5 |
| -9928 | DS2 | int | 只读 | global/全局 | Used in Double Spoiler, unknown. | 否/待确认 | 继承自 TH12.5 |
| -9927 | DS3 | int | 只读 | global/全局 | Used in Double Spoiler, unknown. | 否/待确认 | 继承自 TH12.5 |
| -9926 | GI0 | int | 读写 | global/全局 | Global integer variable. | 是 | 继承自 TH12.5 |
| -9925 | GI1 | int | 读写 | global/全局 | Global integer variable. | 是 | 继承自 TH12.5 |
| -9924 | GI2 | int | 读写 | global/全局 | Global integer variable. | 是 | 继承自 TH12.5 |
| -9923 | GI3 | int | 读写 | global/全局 | Global integer variable. | 是 | 继承自 TH12.5 |
| -9922.0f | GF0 | float | 读写 | global/全局 | Global float variable. | 是 | 继承自 TH12.5 |
| -9921.0f | GF1 | float | 读写 | global/全局 | Global float variable. | 是 | 继承自 TH12.5 |
| -9920.0f | GF2 | float | 读写 | global/全局 | Global float variable. | 是 | 继承自 TH12.5 |
| -9919.0f | GF3 | float | 读写 | global/全局 | Global float variable. | 是 | 继承自 TH12.5 |
| -9918.0f | GF4 | float | 读写 | global/全局 | Global float variable. | 是 | 继承自 TH12.5 |
| -9917.0f | GF5 | float | 读写 | global/全局 | Global float variable. | 是 | 继承自 TH12.5 |
| -9916.0f | GF6 | float | 读写 | global/全局 | Global float variable. | 是 | 继承自 TH12.5 |
| -9915.0f | GF7 | float | 读写 | global/全局 | Global float variable. | 是 | 继承自 TH12.5 |
| -9914 | ID | int | 只读 | local/敌机局部 | ID of the enemy. | 是 | 继承自 TH12.5 |
| -9913 | DS_PHOTOCOUNT | int | 只读 | global/全局 | Used in Double Spoiler, amount of photos taken. | 是 | 继承自 TH12.5 |
| -9912 | DS4 | int | 只读 | global/全局 | Used in Double Spoiler, unknown. | 否/待确认 | 继承自 TH12.5 |
| -9911.0f | ANGLE_BOSS | float | 只读 | global/全局 | Angle at which the boss moves. | 是 | 继承自 TH12.5 |
| -9910.0f | SPEED_BOSS | float | 只读 | global/全局 | Speed at which the boss moves. | 是 | 继承自 TH12.5 |
| -9909 | UNKNOWN9 | int | 只读 | local/敌机局部 | Enemy ID of the parent enemy. | 是 | 继承自 TH12.8 |
| -9908 | ENM_CNT | int | 只读 | global/全局 | Amount of killable enemies alive (that is, doesn't include hitboxless/intangible enemies etc). | 是 | 继承自 TH13 |
| -9907 | SPELL_ID | int | 只读 | global/全局 | Spellcard ID, used by spell practice. Unknown meaning in LoLK. | 是 | 继承自 TH13 |
| -9906 | MIRROR | int | 只读 | local/敌机局部 | Mirror flag state, either 0 or 1. TODO: verify game version | 否/待确认 | 继承自 TH15 |
| -9905 | [-9905] | int | 只读 | global/全局 | Value set by ins_524. | 是 | 继承自 TH15 |
| -9904 | MISS_COUNT_GLOBAL | int | 只读 | global/全局 | Amount of misses throughout the entire game. | 是 | 继承自 TH15 |
| -9903 | HYPER | int | 只读 | global/全局 | Currently active hyper. No hyper = 0, wolf = 1, otter = 2, eagle = 3, neutral hyper = 4. | 是 | 本作 |
| -9902 | GRAZE_RECENT | int | 只读 | global/全局 | Increases whenever you graze something, but also decreases very quickly. Used by st4 midboss. | 是 | 本作 |
| -9901 | GOASTS | int | 只读 | global/全局 | Amount of tokens currently flying around the screen. Used by st5 midboss. | 是 | 本作 |
| -9900 | HYPERDYING | int | 只读 | global/全局 | Set to 1 when player is in the state of hyperdying, that is, right after breaking a hyper. Used by st6 midboss. | 是 | 本作 |
| -9899 | ACHIEVEMENT_MODE | int | 只读 | global/全局 | Set to 1 when the stage was loaded through the achievement menu, otherwise -1. | 是 | 本作 |

## TH18 东方虹龙洞

- 体系：第四世代
- 指令：普通指令 325 条；已说明 260/325。主要分组：系统/流程/栈/算术 / System；敌机创建与 ANM 管理 / Enemy creation and ANM script management；移动管理 / Movement management；敌机属性与杂项 / Enemy property management and other miscellaneous things；子弹创建与删除 / Bullet creation and deletion；激光创建 / Laser creation；敌机交互 / Enemy interaction；调试 / Debug；游戏特有 / Game specific。
- 变量：ecl-web.txt 未列出该作变量表。

### TH18 指令：系统/流程/栈/算术 / System

| ID | 助记名 | 参数 | 说明 | 文档化 | 来源 |
| --- | --- | --- | --- | --- | --- |
| 0 | nop | — | Empty instruction, doesn't do anything. | 是 | 继承自 TH13 |
| 1 | delete | — | Returns to the top of current call stack. | 是 | 继承自 TH13 |
| 2 | ins_2 | — |  | 否/待确认 | 继承自 TH-1 |
| 3 | ins_3 | — |  | 否/待确认 | 继承自 TH-1 |
| 4 | ins_4 | — |  | 否/待确认 | 继承自 TH-1 |
| 5 | ins_5 | — |  | 否/待确认 | 继承自 TH-1 |
| 6 | ins_6 | — |  | 否/待确认 | 继承自 TH-1 |
| 7 | ins_7 | — |  | 否/待确认 | 继承自 TH-1 |
| 8 | ins_8 | — |  | 否/待确认 | 继承自 TH-1 |
| 9 | ins_9 | — |  | 否/待确认 | 继承自 TH-1 |
| 10 | ret | — | Returns from the current sub. | 是 | 继承自 TH13 |
| 11 | call | m (sub) | Calls a given sub. Can take additional parameters to pass as arguments to the sub. [c=orange]Direct Usage obsolete. Use `@subName()` syntax instead. | 是 | 继承自 TH13 |
| 12 | jmp | o (target) | Unconditionally jumps to the label %1. [c=orange]Direct usage obsolete. Use `goto label` syntax instead. | 是 | 继承自 TH13 |
| 13 | jmpEq | o (target) | Pops a number from the stack and if it evaluates to false (in this context, 0), jumps to label %1. [c=orange]Direct usage obsolete. Use if/unless statement instead. | 是 | 继承自 TH13 |
| 14 | jmpNeq | o (target) | Pops a number from the stack and if it evaluates to true (in this context, anything non-0), jumps to label %1. [c=orange]Direct usage obsolete. Use if/unless statement instead. | 是 | 继承自 TH13 |
| 15 | callAsync | m (sub) | Asynchronously calls a given sub. Can take additional parameters to pass as arguments to the sub. [c=orange]Direct usage obsolete. Use `@subName() async` syntax instead. | 是 | 继承自 TH13 |
| 16 | callAsyncId | mS (sub, id) | Asynchronously calls a given sub and assigns it ID %2. Can take additional parameters to pass as arguments to the sub. [c=orange]Direct usage obsolete, use, `@subName() async id` syntax instead. | 是 | 继承自 TH13 |
| 17 | killAsync | S (id) | Ends most recently called sub that has ID %1 (same ID as in ins_16). If no sub with the given ID is found, nothing happens. Using ID -1 can lead to various unexpected results, ranging from deleting the enemy to freezing the game. | 是 | 继承自 TH13 |
| 18 | ins_18 | S (id) | Let `vm` be the most recent async sub running with ID %1: this ins sets `vm[0x000011E4]` to 1. | 否/待确认 | 继承自 TH13 |
| 19 | ins_19 | S (id) | Let `vm` be the most recent async sub running with ID %1: this ins sets `vm[0x000011E4]` to 0. | 否/待确认 | 继承自 TH13 |
| 20 | ins_20 | SS (id, b) | Let `vm` be the most recent async sub running with ID %1: this ins sets `vm[0x0000101C]` to %2. | 否/待确认 | 继承自 TH13 |
| 21 | killAllAsync | — | Ends all running async subs. Calling this in an async sub can lead to unexpected results, such as crashing the game. | 是 | 继承自 TH13 |
| 22 | debug22 | Sm (a, b) | Debug instruction, code does not exist in the release builds of the game. Most likely used to call sub %2 if some variable set in a debug menu is equal to %1. | 是 | 继承自 TH13 |
| 23 | wait | S (time) | Stops sub execution for %1 frames. | 是 | 继承自 TH13 |
| 24 | waitf | f (time) | ins_23, but time is given as a float instead of an int. Subframes do actually exist and affect ins_547. | 是 | 继承自 TH13 |
| 25 | ins_25 | — |  | 否/待确认 | 继承自 TH-1 |
| 26 | ins_26 | — |  | 否/待确认 | 继承自 TH-1 |
| 27 | unknown27 | — |  | 否/待确认 | 继承自 TH-1 |
| 28 | ins_28 | — |  | 否/待确认 | 继承自 TH-1 |
| 29 | ins_29 | — |  | 否/待确认 | 继承自 TH-1 |
| 30 | unknown30 | m (formatString) | Some sort of `printf` debug instruction, which can take additional float/int arguments after %1. Its code does not exist in the release builds. | 是 | 继承自 TH13 |
| 31 | unknown31 | — |  | 否/待确认 | 继承自 TH-1 |
| 32 | ins_32 | — |  | 否/待确认 | 继承自 TH-1 |
| 33 | ins_33 | — |  | 否/待确认 | 继承自 TH-1 |
| 34 | ins_34 | — |  | 否/待确认 | 继承自 TH-1 |
| 35 | ins_35 | — |  | 否/待确认 | 继承自 TH-1 |
| 36 | ins_36 | — |  | 否/待确认 | 继承自 TH-1 |
| 37 | ins_37 | — |  | 否/待确认 | 继承自 TH-1 |
| 38 | ins_38 | — |  | 否/待确认 | 继承自 TH-1 |
| 39 | ins_39 | — |  | 否/待确认 | 继承自 TH-1 |
| 40 | stackAlloc | S (size) | Increases the ECL stack pointer by %1 bytes (probably), to make space for sub variables. [c=orange]Obsolete, thecl generates this instruction automatically. | 是 | 继承自 TH13 |
| 41 | ins_41 | — |  | 否/待确认 | 继承自 TH-1 |
| 42 | pushi | S (num) | Pushes an integer to the ECL stack. [c=orange]Obsolete, push values to stack by writing unassigned expressions instead. | 是 | 继承自 TH13 |
| 43 | seti | S (var) | Pops an integer from the stack into variable %1. [c=orange]Obsolete, use assignment syntax instead. | 是 | 继承自 TH13 |
| 44 | pushf | f (num) | Pushes a float to the ECL stack. [c=orange]Obsolete, push values to stack by writing unassigned expressions instead. | 是 | 继承自 TH13 |
| 45 | setf | f (var) | Pops a float from the stack into variable %1. [c=orange]Obsolete, use assignment syntax instead. | 是 | 继承自 TH13 |
| 46 | ins_46 | — |  | 否/待确认 | 继承自 TH-1 |
| 47 | ins_47 | — |  | 否/待确认 | 继承自 TH-1 |
| 48 | ins_48 | — |  | 否/待确认 | 继承自 TH-1 |
| 49 | ins_49 | — |  | 否/待确认 | 继承自 TH-1 |
| 50 | addi | — | Sums integers on the stack. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 51 | addf | — | Sums floats on the stack. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 52 | subi | — | Subtracts integers on the stack. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 53 | subf | — | Subtracts floats on the stack. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 54 | muli | — | Multiplies integers on the stack. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 55 | mulf | — | Multiplies floats on the stack. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 56 | divi | — | Divides integers on the stack. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 57 | divf | — | Divides floats on the stack. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 58 | modi | — | Modulo operation on integers on the stack. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 59 | eqi | — | Stack integer `==` comparison. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 60 | eqf | — | Stack float `==` comparison. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 61 | neqi | — | Stack integer `!=` comparison. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 62 | neqf | — | Stack float `!=` comparison. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 63 | lessi | — | Stack integer `<` comparison. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 64 | lessf | — | Stack float `<` comparison. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 65 | leqi | — | Stack integer `<=` comparison. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 66 | leqf | — | Stack float `<=` comparison. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 67 | greateri | — | Stack integer `>` comparison. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 68 | greaterf | — | Stack float `>` comparison. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 69 | geqi | — | Stack integer `>=` comparison. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 70 | geqf | — | Stack float `>=` comparison. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 71 | noti | — | Stack integer NOT operation (e.g. !1). [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 72 | notf | — | Stack float NOT operation (e.g. !1.0f). [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 73 | or | — | Logical OR operation on the stack. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 74 | and | — | Logical AND operation on the stack. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 75 | xor | — | Bitwise XOR operation on integers on the stack. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 76 | bit_or | — | Bitwise OR operation on integers on the stack. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 77 | bit_and | — | Bitwise AND operation on integers on the stack. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 78 | deci | S (var) | Pushes variable %1 to the stack and then decrements it. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 79 | stackSin | — | sin operation on a float on the stack. [c=orange]Obsolete, use `sin(floatVal)` instead. | 是 | 继承自 TH13 |
| 80 | stackCos | — | cos operation on a float on the stack. [c=orange]Obsolete, use `cos(floatVal)` instead. | 是 | 继承自 TH13 |
| 81 | circlePos | ffff (varX, varY, ang, radius) | Performs following operation: [code]%1 = cos(%3)*%4;<br>%2 = sin(%3)*%4;[/code] | 是 | 继承自 TH13 |
| 82 | validRad | f (var) | Normalizes angle in %1. | 是 | 继承自 TH13 |
| 83 | negi | — | Negates an integer on the stack. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 84 | negf | — | Negates a float on the stack. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 85 | squareSum | fff (var, x, y) | Performs following operation: [code]%1 = %2*%2 + %3*%3;[/code] | 是 | 继承自 TH13 |
| 86 | squareSumRoot | fff (var, x, y) | Performs following operation: [code]%1 = sqrt(%2*%2 + %3*%3);[/code] | 是 | 继承自 TH13 |
| 87 | getAngle | fffff (var, x1, y1, x2, y2) | Calculates angle from (%2,%3) to (%4,%5) and stores it in %1. | 是 | 继承自 TH13 |
| 88 | stackSqrt | — | square root operation on a float on the stack. [c=orange]Obsolete, use `sqrt(floatVal)` instead. | 是 | 继承自 TH13 |
| 89 | linearFunc | fff (var, a, x) | Performs following operation: [code]%1 = %2*%3;[/code]<br>(what's the point of making this an instruction, ZUN?) | 是 | 继承自 TH13 |
| 90 | pointRotate | fffff (varX, varY, x, y, rad) | Rotates point (%3,%4) by angle %5 and stores the resulting coordinates in %1 and %2. | 是 | 继承自 TH13 |
| 91 | floatTime | SfSSff (slot, var, time, mode, init, final) | In %3 frames using mode %4, variable %2 changes from %5 to %6. %1 is used to set the slot to be used by this ins, every enemy has 8 slots (0 to 7). | 是 | 继承自 TH13 |
| 92 | math92 | SfSSffff (slot, var, time, mode, init, final, m, n) | Same as ins_91, but takes 2 extra arguments of unknown meaning. Needs investigation. | 否/待确认 | 继承自 TH13 |
| 93 | math93 | ffff (varX, varY, r1, r2) | Gets a random point based on %3 and %4 and stores it on (%1,%2). Needs investigation. | 否/待确认 | 继承自 TH13 |

### TH18 指令：敌机创建与 ANM 管理 / Enemy creation and ANM script management

| ID | 助记名 | 参数 | 说明 | 文档化 | 来源 |
| --- | --- | --- | --- | --- | --- |
| 300 | enmCreate | mffSSS (sub, x, y, hp, score, item) | Creates an enemy using subroutine %1 at coordinates %2, %3 (relative to position of enemy that called it), health of created enemy is %4, score bonus is %5 and item drop is %6. | 是 | 继承自 TH13 |
| 301 | enmCreateA | mffSSS (sub, x, y, hp, score, item) | Creates an enemy using subroutine %1 at coordinates %2, %3 (absolute position), health of created enemy is %4, score bonus is %5 and item drop is %6. | 是 | 继承自 TH13 |
| 302 | anmSelect | S (anmIndex) | Selects ANM file to be used by other instructions based on %1. | 是 | 继承自 TH13 |
| 303 | anmSetSprite | SS (slot, script) | Loads script %2 from ANM selected with ins_302 on slot %1. | 是 | 继承自 TH13 |
| 304 | enmCreateM | mffSSS (sub, x, y, hp, score, item) | Creates a mirrored enemy using subroutine %1 at coordinates %2, %3 (relative to caller's position), health of created enemy is %4, score bonus is %5 and item drop is %6. | 是 | 继承自 TH13 |
| 305 | enmCreateAM | mffSSS (sub, x, y, hp, score, item) | Creates an mirrored enemy using subroutine %1 at coordinates %2, %3 (absolute position), health of created enemy is %4, score bonus is %5 and item drop is %6. | 是 | 继承自 TH13 |
| 306 | anmSetMain | SS (slot, script) | Loads script %2 from ANM selected with ins_302 on slot %1. However, the script number provided will only be used when the enemy is not moving. When moving left %2+1 will be used, right %2+2, diagonal left %2+3, diagonal right %2+4. Might not work properly if %1 is not 0 according to THBWiki. | 是 | 继承自 TH13 |
| 307 | anmPlay | SS (anmIndex, script) | From ANM file selected based on %1, play script %2 at caller's current coordinates. The spawned script is completely independent, and will continue existing even if caller is deleted. | 是 | 继承自 TH13 |
| 308 | anmPlayAbs | SS (anmIndex, script) | From ANM file selected based on %1, play script %2 at coordinates (0, 0). The spawned script is completely independent, and will continue existing even if caller is deleted. | 是 | 继承自 TH13 |
| 309 | enmCreateF | mffSSS (sub, x, y, hp, score, item) | Creates a filler enemy using subroutine %1 at coordinates %2, %3 (relative to caller's position), health of created enemy is %4, score bonus is %5 and item drop is %6. | 是 | 继承自 TH13 |
| 310 | enmCreateAF | mffSSS (sub, x, y, hp, score, item) | Creates a filler enemy using subroutine %1 at coordinates %2, %3 (absolute position), health of created enemy is %4, score bonus is %5 and item drop is %6. | 是 | 继承自 TH13 |
| 311 | enmCreateMF | mffSSS (sub, x, y, hp, score, item) | Creates a mirrored filler enemy using subroutine %1 at coordinates %2, %3 (relative to caller's position), health of created enemy is %4, score bonus is %5 and item drop is %6. | 是 | 继承自 TH13 |
| 312 | enmCreateAMF | mffSSS (sub, x, y, hp, score, item) | Creates a mirrored filler enemy using subroutine %1 at coordinates %2, %3 (absolute position), health of created enemy is %4, score bonus is %5 and item drop is %6. | 是 | 继承自 TH13 |
| 313 | anmSelectedPlay | S (script) | Same as ins_307, except it uses the ANM file selected by ins_302. | 是 | 继承自 TH13 |
| 314 | anmPlayHigh | SS (anmIndex, script) | Same as ins_307, except it spawns the ANM with a higher layer? Needs further investigation. | 否/待确认 | 继承自 TH13 |
| 315 | anmPlayRotate | SSf (anmIndex, script, angle) | Same as ins_307, except it sets rotation of spawned ANM to %3. | 是 | 继承自 TH13 |
| 316 | anm316 | SS (a, b) | Unknown. | 否/待确认 | 继承自 TH13 |
| 317 | anmSwitch | SS (slot, switch) | Sets the execution pointer of ANM script on slot %1 to where ANM `ins_5(a)` with `a` == `switch` is (the time is also changed to match time of `ins_5`). Doesn't work if the value is 0 apparently? | 是 | 继承自 TH13 |
| 318 | anmReset | — | Resets some ANM-related parameters of the caller (TODO: what exactly?) | 是 | 继承自 TH13 |
| 319 | anmRotate | Sf (slot, r) | Set rotation of an ANM script on slot %1 to %2. | 是 | 继承自 TH13 |
| 320 | anmMove | Sff (slot, x, y) | Set position of an ANM script on slot %1 to (%2,%3). This does not detach the script from the caller, so the actual position of the script will be position of the caller + position set here. | 是 | 继承自 TH13 |
| 321 | enmMapleEnemy | mffSSS (sub, x, y, hp, score, item) | ins_300, but used by 'MapleEnemy' (TODO: what's the difference from ins_300?) | 是 | 继承自 TH13 |
| 322 | enm322 | SS (a, b) | Unknown. | 否/待确认 | 继承自 TH13 |
| 323 | deathAnm | SS (anmIndex, script) | Set the animation that will play when the enemy dies to script %2 from ANM file specified by %1. | 是 | 继承自 TH13 |
| 324 | enmPos2 | — | Unknown. | 否/待确认 | 继承自 TH13 |
| 325 | anmColor | SSSS (slot, R, G, B) | Modify color of ANM script on slot %1, %2, %3, [c=lightblue]%4 correspond to individual colors and have to be from 0 to 255. | 是 | 继承自 TH13 |
| 326 | anmColorTime | SSSSSS (slot, time, mode, R, G, B) | Same as ins_325, but the change is applied in %2 frames using mode %3. | 是 | 继承自 TH13 |
| 327 | anmAlpha | SS (slot, alpha) | Sets alpha of ANM script on slot %1 to %2 (must be a value between 0-255) | 是 | 继承自 TH13 |
| 328 | anmAlphaTime | SSSS (slot, time, mode, alpha) | Same as ins_327, but the change is applied in %2 frames using mode %3. | 是 | 继承自 TH13 |
| 329 | anmScale | Sff (slot, w, h) | Sets horizontal and vertical scaling of ANM script on slot %1 to %2 and %3 respectively. Overwrites scaling properties set by the ANM script. | 是 | 继承自 TH13 |
| 330 | anmScaleTime | SSSff (slot, time, mode, w, h) | Same as ins_329, but the change is applied in %2 frames using mode %3. | 是 | 继承自 TH13 |
| 331 | anmAlpha2 | SS (slot, alpha) | Sets alpha2 (opacity of the gradient) of ANM script on slot %1 to %2. | 是 | 继承自 TH13 |
| 332 | anmAlpha2Time | SSSS (slot, time, mode, alpha) | Same as ins_331, but the change is applied in %2 frames using mode %3. | 是 | 继承自 TH13 |
| 333 | anm333 | SSSff (a, b, c, r, s) | Unknown. Might be doing something to ANM script on slot %1. | 否/待确认 | 继承自 TH13 |
| 334 | anm334 | S (a) | Hard to tell? THBWiki Google translate gives this: 'The animation effect of the playing unit (enemy), the lightning effect near the evil spirit ball of the god temple', which might be referring to lightning around Nue in TD extra stage. | 否/待确认 | 继承自 TH13 |
| 335 | anmScale2 | Sff (slot, w, h) | Same as ins_329, except it doesn't overwrite the scaling set by the ANM script - instead, it multiplies it. | 是 | 继承自 TH13 |
| 336 | anmLayer | SS (slot, layer) | Set layer of ANM script on slot %1 to %2. | 是 | 继承自 TH14 |
| 337 | anmBlendMode | SS (slot, b) | Set blend mode of ANM script on slot %1 to %2 (TODO: make a list of blend modes). | 是 | 继承自 TH16 |
| 338 | anmPlayPos | SSfff (anmIndex, script, x, y, z) | Same as ins_307, but the spawned script is offset by (%3,%4). For 3D objects, %5 is used too (TODO: verify that). | 是 | 继承自 TH16 |
| 339 | anm339 | SSS (a, b, c) | Unknown. Might be doing something to ANM script on slot %1. | 否/待确认 | 继承自 TH16 |
| 340 | enmDelete | S (id) | Delete enemy with the given ID. | 是 | 继承自 TH16 |

### TH18 指令：移动管理 / Movement management

| ID | 助记名 | 参数 | 说明 | 文档化 | 来源 |
| --- | --- | --- | --- | --- | --- |
| 400 | movePos | ff (x, y) | Sets caller's absolute position to %1, %2. | 是 | 继承自 TH13 |
| 401 | movePosTime | SSff (time, mode, x, y) | Same as ins_400, but the change is applied in %1 frames using mode %2. | 是 | 继承自 TH13 |
| 402 | movePosRel | ff (x, y) | Sets caller's relative position to %1, %2. | 是 | 继承自 TH13 |
| 403 | movePosRelTime | SSff (time, mode, x, y) | Same as ins_402, but the change is applied in %1 frames using mode %2. | 是 | 继承自 TH13 |
| 404 | moveVel | ff (r, spd) | Sets caller's absolute movement angle to %1 and speed to %2. | 是 | 继承自 TH13 |
| 405 | moveVelTime | SSff (time, mode, r, spd) | Same as ins_404, but the change is applied in %1 frames using mode %2. | 是 | 继承自 TH13 |
| 406 | moveVelRel | ff (r, spd) | Sets caller's relative movement angle to %1 and speed to %2. | 是 | 继承自 TH13 |
| 407 | moveVelRelTime | SSff (time, mode, r, spd) | Same as ins_406, but the change is applied in %1 frames using mode %2. | 是 | 继承自 TH13 |
| 408 | moveCircle | ffff (θ, spd, rad, radInc) | Sets caller's absolute circle movement: %1 is the angle indicating initial position on the circle, %2 is the angular velocity, %3 is circle radius and %4 is by how much the radius increases each frame. | 是 | 继承自 TH13 |
| 409 | moveCircleTime | SSfff (time, mode, spd, rad, radInc) | Same as ins_408, but the change is applied in %1 frames using mode %2. There is also no initial angle parameter here for obvious reason. | 是 | 继承自 TH13 |
| 410 | moveCircleRel | ffff (θ, spd, rad, radInc) | Sets caller's relative circle movement: %1 is the angle indicating initial position on the circle, %2 is the angular velocity, %3 is circle radius and %4 is by how much the radius increases each frame. | 是 | 继承自 TH13 |
| 411 | moveCircleRelTime | SSfff (time, mode, spd, rad, radInc) | Same as ins_410, but the change is applied in %1 frames using mode %2. There is also no initial angle parameter here for obvious reason. | 是 | 继承自 TH13 |
| 412 | moveRand | SSf (time, mode, spd) | Randomizes caller's absolute angle and sets absolute speed to %3. The speed changes back to 0 in %1 frames using mode %2. | 是 | 继承自 TH13 |
| 413 | moveRandRel | SSf (time, mode, spd) | Randomizes caller's relative angle and sets relative speed to %3. The speed changes back to 0 in %1 frames using mode %2. | 是 | 继承自 TH13 |
| 414 | moveBoss | — | Sets caller's absolute position to the absolute position of the boss. If called without a boss, [tip=Google translated from THBWiki, I find this sentence funny]it will cause serious mis-access and explode[/tip]. | 是 | 继承自 TH13 |
| 415 | moveBossRel | — | Sets caller's relative position to the relative position of the boss. If called without a boss, [tip=Google translated from THBWiki, I find this sentence funny]it will cause serious mis-access and explode[/tip]. | 是 | 继承自 TH13 |
| 416 | movePos3d | fff (x, y, z) | Same as ins_400, but takes a %3 parameter for the third dimension, which probably affects 3D ANM scripts used by the caller, or something. | 是 | 继承自 TH13 |
| 417 | movePos3dRel | fff (x, y, z) | Same as ins_402, but takes a %3 parameter for the third dimension, which probably affects 3D ANM scripts used by the caller, or something. | 是 | 继承自 TH13 |
| 418 | moveAdd | ff (x, y) | Increases caller's absolute position by %1 and %2. | 是 | 继承自 TH13 |
| 419 | move419 | ff (x, y) | While the code of this ins looks like it's supposed to be a relative version of ins_418, it doesn't seem to behave like that... | 否/待确认 | 继承自 TH13 |
| 420 | moveEllipse | ffffff (θ, spd, rad, radInc, ellDir, ellRatio) | Sets caller's absolute ellipse movement: %1 is the angle indicating initial position on the ellipse, %2 is the angular velocity, %3 is the base circle radius and %4 is by how much the radius increases each frame. %6 is how much the base circle should be 'squished' to make it an ellipse, and %5 is the squishing angle (I don't know math terms in English, sorry) | 是 | 继承自 TH13 |
| 421 | moveEllipseTime | SSfffff (time, mode, spd, rad, radInc, ellDir, ellRatio) | Same as ins_420, but the change is applied in %1 frames using mode %2. There is also no initial angle parameter here for obvious reason | 是 | 继承自 TH13 |
| 422 | moveEllipseRel | ffffff (θ, spd, rad, radInc, ellDir, ellRatio) | Sets caller's relative ellipse movement: %1 is the angle indicating initial position on the ellipse, %2 is the angular velocity, %3 is the base circle radius and %4 is by how much the radius increases each frame. %6 is how much the base circle should be 'squished' to make it an ellipse, and %5 is the squishing angle (I don't know math terms in English, sorry) | 是 | 继承自 TH13 |
| 423 | moveEllipseRelTime | SSfffff (time, mode, spd, rad, radInc, ellDir, ellRatio) | Same as ins_422, but the change is applied in %1 frames using mode %2. There is also no initial angle parameter here for obvious reason | 是 | 继承自 TH13 |
| 424 | moveSetMirror | S (state) | Sets caller's mirror flag to %1. | 是 | 继承自 TH13 |
| 425 | moveBezier | Sffffff (time, x1, y1, x2, y2, x3, y3) | In %1 frames, the enemy moves towards (%2,%3), then moves towards (%6,%7) for a while and finally moves to (%4,%5). Uses absolute position.<br>From THBWiki: <br>(assuming the current coordinates are (x0, y0)) the motion trajectory is actually a Bezier curve from (x0, y0) to (x2, y2);<br>The P1 coordinate of the curve is `((x1-x0)*1/3, (y1-y0)*1/3)`;<br>The P2 coordinate of the curve is `(-(x3-x2)*1/3+x2,-(y3-y2) *1/3+x2)` | 是 | 继承自 TH13 |
| 426 | moveBezierRel | Sffffff (time, x1, y1, x2, y2, x3, y3) | Same as ins_425, but uses relative position. | 是 | 继承自 TH13 |
| 427 | moveReset | — | Resets some movement-related parameters (TODO: what exactly?) | 否/待确认 | 继承自 TH13 |
| 428 | moveVelNM | ff (r, spd) | Same as ins_404, but ignores the mirror flag. | 是 | 继承自 TH13 |
| 429 | moveVelNMTime | SSff (time, mode, r, spd) | Same as ins_405, but ignores the mirror flag. | 是 | 继承自 TH13 |
| 430 | moveVelNMRel | ff (r, spd) | Same as ins_406, but ignores the mirror flag. | 是 | 继承自 TH13 |
| 431 | moveVelNMRelTime | SSff (time, mode, r, spd) | Same as ins_407, but ignores the mirror flag. | 是 | 继承自 TH13 |
| 432 | moveEnm | S (id) | Sets caller's absolute position to absolute position of enemy with var_-9914 == %1. | 是 | 继承自 TH13 |
| 433 | moveEnmRel | S (id) | Sets caller's relative position to relative position of enemy with var_-9914 == %1. | 是 | 继承自 TH13 |
| 434 | moveCurve | SSSff (time, mode, c, x, y) | In %1 frames using mode %2, caller's absolute position is changed to (%4,%5). The movement trajectory is a curve based on %3, it is unknown how it works exactly. | 否/待确认 | 继承自 TH13 |
| 435 | moveCurveRel | SSSff (time, mode, c, x, y) | In %1 frames using mode %2, caller's relative position is changed to (%4,%5). The movement trajectory is a curve based on %3, it is unknown how it works exactly. | 否/待确认 | 继承自 TH13 |
| 436 | moveAddTime | SSff (time, mode, x, y) | Same as ins_418, but the change is applied in %1 frames using mode %2. | 是 | 继承自 TH13 |
| 437 | moveAddRelTime | SSff (time, mode, x, y) | Same as ins_419, but the change is applied in %1 frames using mode %2 (it also behaves as expected, unlike ins_419). | 是 | 继承自 TH13 |
| 438 | moveCurveAdd | SSSff (time, mode, c, x, y) | Same as ins_434, but instead caller's current absolute coordinates are added to %4 and %5. | 是 | 继承自 TH13 |
| 439 | moveCurveAddRel | SSSff (time, mode, c, x, y) | Same as ins_435, but instead caller's current relative coordinates are added to %4 and %5. | 是 | 继承自 TH13 |
| 440 | moveAngle | f (r) | Sets caller's absolute movement angle to %1. | 是 | 继承自 TH14 |
| 441 | moveAngleTime | SSf (time, mode, r) | Same as ins_440, but the change is applied in %1 frames using mode %2. | 是 | 继承自 TH14 |
| 442 | moveAngleRel | f (r) | Sets caller's relative movement angle to %1. | 是 | 继承自 TH14 |
| 443 | moveAngleRelTime | SSf (time, mode, r) | Same as ins_442, but the change is applied in %1 frames using mode %2. | 是 | 继承自 TH14 |
| 444 | moveSpeed | f (spd) | Sets caller's absolute movement speed to %1. | 是 | 继承自 TH14 |
| 445 | moveSpeedTime | SSf (time, mode, spd) | Same as ins_444, but the change is applied in %1 frames using mode %2. | 是 | 继承自 TH14 |
| 446 | moveSpeedRel | f (spd) | Sets caller's relative movement speed to %1. | 是 | 继承自 TH14 |
| 447 | moveSpeedRelTime | SSf (time, mode, spd) | Same as ins_446, but the change is applied in %1 frames using mode %2. | 是 | 继承自 TH14 |

### TH18 指令：敌机属性与杂项 / Enemy property management and other miscellaneous things

| ID | 助记名 | 参数 | 说明 | 文档化 | 来源 |
| --- | --- | --- | --- | --- | --- |
| 500 | setHurtbox | ff (w, h) | Sets caller's hurtbox width to %1 and height to %2. | 是 | 继承自 TH13 |
| 501 | setHitbox | ff (w, h) | Sets caller's hitbox width to %1 and height to %2. | 是 | 继承自 TH13 |
| 502 | flagSet | S (n) | Sets flag(s) according to %1. Refer to the [flag table](#s=modding/flags) for exact values. | 是 | 继承自 TH13 |
| 503 | flagClear | S (n) | Clears flag(s) according to %1. Refer to the [flag table](#s=modding/flags) for exact values. | 是 | 继承自 TH13 |
| 504 | moveLimit | ffff (x, y, w, h) | Sets caller's movement limit rectangle: (%1,%2) are the coordinates of the center of the rect, while %3, %4 are width and height of it. | 是 | 继承自 TH13 |
| 505 | moveLimitReset | — | Removes caller's movement limit. | 是 | 继承自 TH13 |
| 506 | dropClear | — | Clears caller's extra item drop. | 是 | 继承自 TH13 |
| 507 | dropExtra | SS (type, amount) | Adds %2 items of type %1 to caller's extra drop. Item type table will be made in the future. | 是 | 继承自 TH13 |
| 508 | dropArea | ff (w, h) | Sets caller's item drop area width to %1 and height to %2. | 是 | 继承自 TH13 |
| 509 | dropItems | — | Drops all items the caller has. Has no effect in spell practice. | 是 | 继承自 TH13 |
| 510 | dropMain | S (type) | Sets caller's main drop to %1. | 是 | 继承自 TH13 |
| 511 | lifeSet | S (hp) | Sets caller's current HP and max HP to %1. | 是 | 继承自 TH13 |
| 512 | setBoss | S (a) | If %1 is 0, activates boss mode and makes the caller the main boss. If %1 > 0, it makes the caller the secondary boss. If %1 is -1, ends boss mode. | 是 | 继承自 TH13 |
| 513 | timerReset | — | Resets boss timer. | 是 | 继承自 TH13 |
| 514 | setInterrupt | SSSm (slot, hp, time, sub) | Sets an interrupt on slot %1 (not sure how many slots there are) - once caller's hp reaches %2 or %3 frames have passed since this was called, caller will terminate all subs it's currently running and execute sub %4. | 是 | 继承自 TH13 |
| 515 | setInvuln | S (time) | Makes the caller completely invulnerable for %1 frames. | 是 | 继承自 TH13 |
| 516 | playSound | S (id) | Plays sound %1. Sound id table will be added in the future. | 是 | 继承自 TH13 |
| 517 | setScreenShake | SSS (time, startIntensity, endIntensity) | Activates screen shake for %1 frames. %2 is the starting intensity and %3 is the ending intensity. The larger the intensity, the more the screen shakes. | 是 | 继承自 TH13 |
| 518 | dialogRead | S (dialogueId) | Starts a dialogue, %1 is the ID of an entry in the .msg file. Apart from that, has the effect ins_525. | 是 | 继承自 TH13 |
| 519 | dialogWait | — | Waits until there are no dialogues active, or the running .msg script calls a certain instruction (which one?) | 否/待确认 | 继承自 TH13 |
| 520 | bossWait | — | Waits until there are no boss enemies. | 是 | 继承自 TH13 |
| 521 | setTimeout | Sm (slot, sub) | Sets a timeout interrupt on slot %1 - when the timer reaches 0, caller will terminate all subs it's currently running and execute sub %2. | 是 | 继承自 TH13 |
| 522 | spellEx | SSSm (id, time, type, name) | Same as ins_537, but the difficulty number is NOT added to the id. | 是 | 继承自 TH16 |
| 523 | spellEnd | — | Ends currently active spellcard. | 是 | 继承自 TH13 |
| 524 | setChapter | S (a) | Some jank that's responsible for showing boss name and possibly other things. In LoLK, it also ends the current chapter and begins a new one. | 否/待确认 | 继承自 TH13 |
| 525 | enmKillAll | — | Kills all other enemies (unless they have a flag that prevents that set). | 是 | 继承自 TH13 |
| 526 | etProtectRange | f (r) | Makes bullets generated by the caller not spawn if they are in radius %1 around the player. | 是 | 继承自 TH13 |
| 527 | lifeMarker | SfS (slot, hp, c) | Sets a new life marker on slot %1, %2 determines where the marker will appear on the health bar (if %2=1000.0f and the enemy has 2000 hp, the marker will split the hp bar in half). %3 is an RGB value of unknown use (possibly leftover from earlier ECL versions) | 是 | 继承自 TH13 |
| 528 | spellUnused | SSSm (id, time, type, name) | No difference from ins_522, unused. | 是 | 继承自 TH16 |
| 529 | rankF3 | ffff (var, a, b, c) | Sets %1 to %2 if rank is low, %3 if rank is average or %4 if rank is high. | 是 | 继承自 TH13 |
| 530 | rankF5 | ffffff (var, a, b, c, d, e) | Sets %1 to %2 if rank is very low, %3 if rank is low, %4 if rank is average, %5 if rank is high or %6 if rank is very high. | 是 | 继承自 TH13 |
| 531 | rankF2 | fff (var, a, b) | Sets %1 to %2 if rank is low or %3 if rank is high. | 是 | 继承自 TH13 |
| 532 | rankI3 | SSSS (var, a, b, c) | Sets %1 to %2 if rank is low, %3 if rank is average or %4 if rank is high. | 是 | 继承自 TH13 |
| 533 | rankI5 | SSSSSS (var, a, b, c, d, e) | Sets %1 to %2 if rank is very low, %3 if rank is low, %4 if rank is average, %5 if rank is high or %6 if rank is very high. | 是 | 继承自 TH13 |
| 534 | rankI2 | SSS (var, a, b) | Sets %1 to %2 if rank is low or %3 if rank is high. | 是 | 继承自 TH13 |
| 535 | diffI | SSSSS (var, E, N, H, L) | Sets %1 to one of values provided based on difficulty. | 是 | 继承自 TH13 |
| 536 | diffF | fffff (var, E, N, H, L) | Sets %1 to one of values provided based on difficulty. | 是 | 继承自 TH13 |
| 537 | spell | SSSm (id, time, mode, name) | Declares a spellcard with id %1 and name %4. The actual ID passed to the spell-creating function is `id + difficulty`, with easy=0, normal=1, hard=2, lunatic=3, ex=4, overdrive=5. <br>%2 determines how much time the spell circle takes to shrink (in frames), as well as how fast the spell bonus decreases. The exact formula is as follows: <br>[code] int factor = maxSCB >> 2; // maxSCB is hardcoded<br> currSCB -= (maxSCB - factor) / (%2 - 300);<br> currSCB -= currSCB % 10; [/code] <br>As you can guess, setting %2 to 300 causes a division by 0 error and crashes the game, while setting it to a value smaller than 300 causes the SCB to increase over time, instead of decreasing. %3 TBD, it's not unused. | 是 | 继承自 TH16 |
| 538 | spell2 | SSSm (id, time, mode, name) | Same as ins_537, except the ID used it `id - 1 + difficulty`. | 是 | 继承自 TH16 |
| 539 | spell3 | SSSm (id, time, mode, name) | Same as ins_537, except the ID used it `id - 2 + difficulty`. | 是 | 继承自 TH16 |
| 540 | stars | S (cnt) | Sets the amount of stars displayed in the top left corner. Stars might not appear at all if there is no boss active. | 是 | 继承自 TH13 |
| 541 | noHitboxDur | S (time) | Disables the hitbox (but not the hurtbox) for the given amount of frames. | 是 | 继承自 TH13 |
| 542 | spellTimeout | — | Makes the current spell a timeout spell (prevent spell bonus from decreasing, give capture bonus if timed out). | 是 | 继承自 TH13 |
| 543 | unknown543 | — | Unknown. | 否/待确认 | 继承自 TH13 |
| 544 | unknown544 | S (a) | Unknown, sets or clears some flag? | 否/待确认 | 继承自 TH13 |
| 545 | laserCancel | — | Cancels all lasers. | 是 | 继承自 TH13 |
| 546 | bombShield | SS (a, script) | Sets the bomb invulnerability flag (%1=1 set, %1=0 not set), the caller's ANM script will change to %2 when a bomb is active (how does it work with ANM slots exactly?) | 是 | 继承自 TH13 |
| 547 | gameSpeed | f (s) | Sets game speed to %1 of the normal speed. In ISC, enemies with flag 13 (dec=8192) set will ignore effects of this opcode. | 是 | 继承自 TH13 |
| 548 | diffWait | SSSS (e, n, h, l) | Same as ins_23, but the wait time is chosen from the given 4 based on the difficulty. | 是 | 继承自 TH13 |
| 549 | unknown549 | S (a) | Unknown. | 否/待确认 | 继承自 TH13 |
| 550 | unknown550 | S (a) | Unknown. | 否/待确认 | 继承自 TH13 |
| 551 | unknown551 | S (a) | Unknown. | 否/待确认 | 继承自 TH13 |
| 552 | zIndex | S (layers) | Increases layer of all ANM scripts used by the caller by %1. | 是 | 继承自 TH13 |
| 553 | hitSound | S (id) | Makes the caller play sound %1 when hit. Sound id table will be added in the future. | 是 | 继承自 TH13 |
| 554 | stageLogo | — | Shows the stage logo from an ANM of a hardcoded name. | 是 | 继承自 TH13 |
| 555 | enmAlive | SS (var, id) | Checks if enemy of var_-9914 == %2 is still alive, and sets %1 to 1 if it is or 0 if it isn't. | 是 | 继承自 TH13 |
| 556 | setDeath | m (sub) | Makes the caller execute sub %1 when the HP reaches 0. Keep in mind that the caller is already marked for deletion at the point when the sub actually executes, so if you put waiting there the sub will not execute fully (because the caller will be deleted) | 是 | 继承自 TH13 |
| 557 | fogTime | SSSff (time, mode, color, start, end) | Same as STD ins_9, that is, fogTime. Refer to [the STD instruction table](#s=modding/std-ins) for details. | 是 | 继承自 TH13 |
| 558 | flagMirror | S (state) | Literally the exact same instruction as ins_424. | 是 | 继承自 TH13 |
| 559 | enmLimit | S (limit) | Set the maximum number of enemies that can be present. New enemies will fail to spawn if the cap is reached. Default is 99999. | 是 | 继承自 TH13 |
| 560 | unknown560 | ff (r, s) | Unknown. | 否/待确认 | 继承自 TH13 |
| 561 | die | — | Makes the caller execute the sub set with ins_556. If there is no such sub set, the caller dies instead (exactly the same as if the player shot down the caller, that is, items are dropped, death sound plays etc) | 是 | 继承自 TH13 |
| 562 | dropItemsSp | — | Same as ins_509, but item spawning will not be blocked in spell practice. | 是 | 继承自 TH13 |
| 563 | unknown563 | S (flagState) | Sets [flag 12](#s=modding/flags) (decimal 4096), which controls whether the hitbox and hurtbox is a rectangle. If %1 is 1, collision is a rectangle. If %1 is 0, collision is elliptical. | 是 | 继承自 TH14 |
| 564 | hitboxRotate | f (angle) | Rotates the hitbox and hurtbox of the enemy (note: the hitbox rotation is really janky, but hurtbox rotates fine). Has no effect unless the enemy uses rectangular collision. | 是 | 继承自 TH14 |
| 565 | bombInvuln | f (red) | Sets caller's damage reduction when a bomb is active, 0.0f means no damage at all, 1.0f is full damage, negative values will make the enemy heal when you bomb. | 是 | 继承自 TH14 |
| 566 | unknown566 | () | Unknown (does it even exist?) | 否/待确认 | 继承自 TH14 |
| 567 | unknown567 | S (a) | Unknown. | 否/待确认 | 继承自 TH14 |
| 568 | spellMode | S (state) | Enables/disables spell card damage reduction, if %1 is 1 it's enabled, if it's 0 it's disabled. Can be used outside of spell cards. | 是 | 继承自 TH14 |
| 569 | unknown569 | S (a) | Unknown. | 否/待确认 | 继承自 TH15 |
| 570 | unknown570 | — | Unknown. | 否/待确认 | 继承自 TH15 |
| 571 | unknown571 | — | Unknown. | 否/待确认 | 继承自 TH15 |
| 572 | lifeNow | S (hp) | Sets caller's current HP to %1, without changing max HP. | 是 | 继承自 TH16 |

### TH18 指令：子弹创建与删除 / Bullet creation and deletion

| ID | 助记名 | 参数 | 说明 | 文档化 | 来源 |
| --- | --- | --- | --- | --- | --- |
| 600 | etNew | S (etId) | Resets bullet manager %1 to default properties. | 是 | 继承自 TH13 |
| 601 | etOn | S (etId) | Shoots bullet(s) using properties from bullet manager %1. | 是 | 继承自 TH13 |
| 602 | etSprite | SSS (etId, type, color) | Sets bullet type and color of bullet manager %1. Refer to [this image](https://cdn.discordapp.com/attachments/395767870119870466/570658618316161041/BULLET_IDS.png) made by Dai. Remarks:<br>- bullet types 35 and 36 spin<br>- type 30 pulses<br>- the difference between 16/37 is the spin direction (same case for 23 and 24) | 是 | 继承自 TH15 |
| 603 | etOffset | Sff (etId, x, y) | Sets the relative offset of bullets spawned by bullet manager %1 to (%2,%3). | 是 | 继承自 TH13 |
| 604 | etAngle | Sff (etId, angle1, angle2) | Sets angle1 and angle2 of bullet manager %1. | 是 | 继承自 TH13 |
| 605 | etSpeed | Sff (etId, speed1, speed2) | Sets speed1 and speed2 of bullet manager %1. | 是 | 继承自 TH13 |
| 606 | etCount | SSS (etId, count1, count2) | Sets count1 and count2 of bullet manager %1. | 是 | 继承自 TH13 |
| 607 | etAim | SS (etId, aim) | Sets aim mode of bullet manager %1. | 是 | 继承自 TH13 |
| 608 | etSound | SSS (etId, sound1, sound2) | Sets sound1 and sound2 of bullet manager %1 (sound effect table is TODO). sound1 plays when the bullet manager fires a bullet, while sound2 plays when a bullet fired by the bullet manager does certain transformations. Set to -1 for no sound. | 是 | 继承自 TH13 |
| 609 | etExSet | SSSSSSff (etId, index, async, type, a, b, r, s) | Sets bullet transformation of bullet manager %1, transformation explanation will be added in the future. | 是 | 继承自 TH13 |
| 610 | etExSet2 | SSSSSSSSffff (etId, index, async, type, a, b, c, d, r, s, m, n) | Same as ins_609, but takes more arguments for certain transformation types. | 是 | 继承自 TH13 |
| 611 | etEx | SSSSSff (etId, async, type, a, b, r, s) | Adds bullet transformation to bullet manager %1, transformation explanation will be added in the future. | 是 | 继承自 TH13 |
| 612 | etEx2 | SSSSSSSffff (etId, async, type, a, b, c, d, r, s, m, n) | Same as ins_611, but takes more arguments for certain transformation types. | 是 | 继承自 TH13 |
| 613 | etClearAll | — | Clears all bullets. | 是 | 继承自 TH13 |
| 614 | etCopy | SS (etIdDest, etIdSrc) | Copies everything from bullet manager %2 into bullet manager %1. Warning: this instruction is partially broken and does NOT copy the index next ins_611/ins_612 transformations will be added at. | 是 | 继承自 TH13 |
| 615 | etCancel | f (r) | Clears all bullets in a circle of radius %1 around the caller, and turns them into cancel items. | 是 | 继承自 TH13 |
| 616 | etClear | f (r) | Clears all bullets in a circle of radius %1 around the caller without turning them into cancel items. | 是 | 继承自 TH13 |
| 617 | etSpeedR3 | Sffffff (etId, spd1l, spd1m, spd1h, spd2l, spd2m, spd2h) | Sets speed1 and speed2 of bullet manager %1 to two of the values provided, based on ingame rank (l=low, m=medium, h=high) | 是 | 继承自 TH13 |
| 618 | etSpeedR5 | Sffffffffff (etId, spd1l, spd1ml, spd1m, spd1mh, spd1h, spd2l, spd2ml, spd2m, spd2mh, spd2h) | Sets speed1 and speed2 of bullet manager %1 to two of the values provided, based on ingame rank (l=low, ml=medium-low, m=medium, mh=medium-high, h=high) | 是 | 继承自 TH13 |
| 619 | etSpeedR2 | Sffff (etId, spd1l, spd1h, spd2l, spd2h) | Sets speed1 and speed2 of bullet manager %1 to two of the values provided, based on ingame rank (l=low, h=high) | 是 | 继承自 TH13 |
| 620 | etCountR3 | SSSSSSS (etId, cnt1l, cnt1m, cnt1h, cnt2l, cnt2m, cnt2h) | Sets count1 and count2 of bullet manager %1 to two of the values provided, based on ingame rank (l=low, m=medium, h=high) | 是 | 继承自 TH13 |
| 621 | etCountR5 | SSSSSSSSSSS (etId, cnt1l, cnt1ml, cnt1m, cnt1mh, cnt1h, cnt2l, cnt2ml, cnt2m, cnt2mh, cnt2h) | Sets count1 and count2 of bullet manager %1 to two of the values provided, based on ingame rank (l=low, ml=medium-low, m=medium, mh=medium-high, h=high) | 是 | 继承自 TH13 |
| 622 | etCountR2 | SSSSS (etId, cnt1l, cnt1h, cnt2l, cnt2h) | Sets count1 and count2 of bullet manager %1 to two of the values provided, based on ingame rank (l=low, h=high) | 是 | 继承自 TH13 |
| 623 | angleToPlayer | fff (var, x, y) | Gets angle to the player from coordinates (%2,%3) and stores it in %1. | 是 | 继承自 TH13 |
| 624 | etSpeedD | Sffffffff (etId, spd1e, spd1n, spd1h, spd1l, spd2e, spd2n, spd2h, spd2l) | Sets speed1 and speed2 of bullet manager %1 to 2 of the values provided, based on the difficulty (e=easy, n=normal, h=hard, l=lunatic) | 是 | 继承自 TH13 |
| 625 | etCountD | SSSSSSSSS (etId, cnt1e, cnt1n, cnt1h, cnt1l, cnt2e, cnt2n, cnt2h, cnt2l) | Sets count1 and count2 of bullet manager %1 to 2 of the values provided, based on the difficulty (e=easy, n=normal, h=hard, l=lunatic) | 是 | 继承自 TH13 |
| 626 | etOffsetRad | Sff (etId, angle, radius) | Sets the relative offset of bullets spawned by bullet manager %1 to (cos(%2)\*%3,sin(%2)\*%3). Stacks with ins_603. | 是 | 继承自 TH13 |
| 627 | etDist | Sf (etId, dist) | Sets distance of bullets spawned by bullet manager %1 to %2 (that is, when a bullet is spawned it moves by %2 using its current angle). | 是 | 继承自 TH13 |
| 628 | etOffsetAbs | Sff (etId, x, y) | Sets the absolute offset of bullets spawned by bullet manager %1 to (%2,%3). | 是 | 继承自 TH13 |
| 629 | fog | fS (r, color) | Sets caller's fog's radius to %1 and color to %2 (RGB value in reverse order). This resets the fog completely, that is, every time it's called the fog spawn animation plays. | 是 | 继承自 TH13 |
| 630 | callSTD | S (switch) | Sets execution pointer of the STD script to where STD ins_16(%1) is (%1 must be the same), basically same concept as ins_317. | 是 | 继承自 TH13 |
| 631 | lifeHide | S (time) | Hides boss lifebar for %1 frames. | 是 | 继承自 TH13 |
| 632 | funcSet | S (id) | Sets a function that the game will execute every frame from a set of hardcoded functions that differs between games. | 是 | 继承自 TH13 |
| 633 | flagExtDmg | S (state) | Sets the external damage flag to %1. Caller probably needs to be the main boss for this to work - with this flag set, the caller gets damaged by the value stored in var_-9940 every frame, and then resets the value. This allows other enemies to damage the boss by incrementing the aforementioned variable, used in LoLK by Sagume (and also happens to be the main cause of the Sagume skip glitch) | 是 | 继承自 TH13 |
| 634 | setHitboxFunc | S (id) | Make the caller use a special function for determining collision with the player. TODO: create a list of functions and their IDs | 是 | 继承自 TH13 |
| 635 | etCancel2 | f (r) | Same as ins_615, but doesn't clear bullets with bomb invulnerability. | 是 | 继承自 TH13 |
| 636 | etClear2 | f (r) | Same as ins_616, but doesn't clear bullets with bomb invulnerability. | 是 | 继承自 TH13 |
| 637 | funcCall | S (id) | Same as ins_632, except the function is called just once instead of every frame. | 是 | 继承自 TH13 |
| 638 | scoreAdd | S (n) | Adds %1 to score (or subtracts if %1 is negative). There is no lower boundary check, so if this causes score to go below 0, an underflow happens. | 是 | 继承自 TH13 |
| 639 | funcSet2 | S (id) | Same as ins_632, except it sets an unknown flag to 1 (ins_632 sets it to 0) | 是 | 继承自 TH13 |
| 640 | etExSub | SSm (etId, index, s) | Sets the string parameter of transform on index %2 in bullet manager %1 to %3, transformations will be explained separately later. | 是 | 继承自 TH13 |
| 641 | etExSubtract | S (etId) | Subtracts 1 from the index used by ins_611 and ins_612, unless it's already 0. This basically changes where the next transformation will be appended. | 是 | 继承自 TH14 |

### TH18 指令：激光创建 / Laser creation

| ID | 助记名 | 参数 | 说明 | 文档化 | 来源 |
| --- | --- | --- | --- | --- | --- |
| 700 | laserNew | Sffff (etId, init_length, final_length, unknown_arg_3, width) | Sets basic parameters of the laser. %4 has something to do with the length of straight line lasers (investigation needed), but doesn't do anything for other laser types. For curvy lasers, the only used argument is %5, and length is specified with ins_701 instead. | 是 | 继承自 TH13 |
| 701 | laserTiming | SSSSSS (edId, startup_time, expand_time, duration, shrink_time, init_flags) | Sets timing for infinite lasers. %6 sets the initial flags for a laser, but these flags are unknown at the moment. For curvy lasers, the %2 argument instead specifies the length of the laser. | 是 | 继承自 TH13 |
| 702 | laserOn | S (edId) | Shoots a straight line laser. | 是 | 继承自 TH13 |
| 703 | laserStOn | SS (etId, laser_id) | Shoots an infinite laser. %2 is a number that's used to identify this particular laser instance, so that it can be referred to in other instructions. | 是 | 继承自 TH13 |
| 704 | laserOffset | Sff (laser_id, x, y) | Sets the position of the infinite laser pointed to by %1. | 是 | 继承自 TH13 |
| 705 | laserTrajectory | Sff (laser_id, x_speed, y_speed) | Sets the offset velocity of the infinite laser pointed to by %1. The laser's position will change by %2 and %3 every frame. | 是 | 继承自 TH13 |
| 706 | laserStLength | Sf (laser_id, speed) | Sets the speed of the infinite laser pointed to by %1. | 是 | 继承自 TH13 |
| 707 | laserStWidth | Sf (laser_id, width) | Sets the width of the infinite laser pointed to by %1. | 是 | 继承自 TH13 |
| 708 | laserStAngle | Sf (laser_id, angle) | Sets the angle of the infinite laser pointed to by %1. | 是 | 继承自 TH13 |
| 709 | laserStRotation | Sf (laser_id, angular_vel) | Sets the angular velocity of the infinite laser pointed to by %1. The laser's angle will change by %2 every frame. | 是 | 继承自 TH13 |
| 710 | laserStEnd | S (laser_id) | Clears the laser pointed to by %1. | 是 | 继承自 TH13 |
| 711 | laserCuOn | S (etId) | Shoots a curvy laser. | 是 | 继承自 TH13 |
| 712 | etCancelRect | ff (w, h) | Cancels all bullets in rectangle of width %1 and height %2. The area is affected by rotation set by ins_564. | 是 | 继承自 TH14 |
| 713 | unknown713 | SS (etId, laser_id) | Shoots a laser 'beam', a laser type used by marisa in GFW. Broken since this laser type does not exist outside of GFW. | 是 | 继承自 TH13 |
| 714 | unknown714 | SS (laser_id, unknown) | Does something with a laser beam pointed to by %1. Broken since this laser type does not exist outside of GFW. | 是 | 继承自 TH13 |

### TH18 指令：敌机交互 / Enemy interaction

| ID | 助记名 | 参数 | 说明 | 文档化 | 来源 |
| --- | --- | --- | --- | --- | --- |
| 800 | enmCall | Sm (id, sub) | Makes enemy with var_-9914 == %1 stop all subs it's running and execute sub %2 (works like an interrupt). This will NOT make the enemy execute the sub right as this instruction is called, the new sub will be executed when the game handles the given enemy, which might be later on the same frame or on the next frame. Using this to make the caller interrupt itself can make the game explode. | 是 | 继承自 TH13 |
| 801 | enmPos | ffS (varX, varY, id) | Stores coordinates of enemy with var_-9914 == %3 in (%1,%2). | 是 | 继承自 TH13 |
| 802 | broadcastInterrupt | S (slot) | For all existing bosses, trigger the interrupt set by ins_514 on slot %1. Does not change the HP to the one set in ins_514. | 是 | 继承自 TH13 |

### TH18 指令：调试 / Debug

| ID | 助记名 | 参数 | 说明 | 文档化 | 来源 |
| --- | --- | --- | --- | --- | --- |
| 900 | debug900 | — | 未在 Priw8 表中记录/待确认 | 否/待确认 | — |
| 901 | debug901 | — | 未在 Priw8 表中记录/待确认 | 否/待确认 | — |
| 902 | debug902 | — | 未在 Priw8 表中记录/待确认 | 否/待确认 | — |
| 903 | debug903 | — | 未在 Priw8 表中记录/待确认 | 否/待确认 | — |
| 904 | debug904 | — | 未在 Priw8 表中记录/待确认 | 否/待确认 | — |

### TH18 指令：游戏特有 / Game specific

| ID | 助记名 | 参数 | 说明 | 文档化 | 来源 |
| --- | --- | --- | --- | --- | --- |
| 1000 | spec0 | — | 未在 Priw8 表中记录/待确认 | 否/待确认 | — |
| 1001 | spec1 | — | 未在 Priw8 表中记录/待确认 | 否/待确认 | — |
| 1002 | spec2 | — | 未在 Priw8 表中记录/待确认 | 否/待确认 | — |
| 1003 | spec3 | — | 未在 Priw8 表中记录/待确认 | 否/待确认 | — |

## TH18.5 弹幕狂们的黑市

- 体系：第四世代
- 指令：普通指令 347 条；已说明 271/347。主要分组：系统/流程/栈/算术 / System；敌机创建与 ANM 管理 / Enemy creation and ANM script management；移动管理 / Movement management；敌机属性与杂项 / Enemy property management and other miscellaneous things；子弹创建与删除 / Bullet creation and deletion；激光创建 / Laser creation；敌机交互 / Enemy interaction；调试 / Debug；游戏特有 / Game specific。
- 变量：ecl-web.txt 未列出该作变量表。

### TH18.5 指令：系统/流程/栈/算术 / System

| ID | 助记名 | 参数 | 说明 | 文档化 | 来源 |
| --- | --- | --- | --- | --- | --- |
| 0 | nop | — | Empty instruction, doesn't do anything. | 是 | 继承自 TH13 |
| 1 | delete | — | Returns to the top of current call stack. | 是 | 继承自 TH13 |
| 2 | ins_2 | — |  | 否/待确认 | 继承自 TH-1 |
| 3 | ins_3 | — |  | 否/待确认 | 继承自 TH-1 |
| 4 | ins_4 | — |  | 否/待确认 | 继承自 TH-1 |
| 5 | ins_5 | — |  | 否/待确认 | 继承自 TH-1 |
| 6 | ins_6 | — |  | 否/待确认 | 继承自 TH-1 |
| 7 | ins_7 | — |  | 否/待确认 | 继承自 TH-1 |
| 8 | ins_8 | — |  | 否/待确认 | 继承自 TH-1 |
| 9 | ins_9 | — |  | 否/待确认 | 继承自 TH-1 |
| 10 | ret | — | Returns from the current sub. | 是 | 继承自 TH13 |
| 11 | call | m (sub) | Calls a given sub. Can take additional parameters to pass as arguments to the sub. [c=orange]Direct Usage obsolete. Use `@subName()` syntax instead. | 是 | 继承自 TH13 |
| 12 | jmp | o (target) | Unconditionally jumps to the label %1. [c=orange]Direct usage obsolete. Use `goto label` syntax instead. | 是 | 继承自 TH13 |
| 13 | jmpEq | o (target) | Pops a number from the stack and if it evaluates to false (in this context, 0), jumps to label %1. [c=orange]Direct usage obsolete. Use if/unless statement instead. | 是 | 继承自 TH13 |
| 14 | jmpNeq | o (target) | Pops a number from the stack and if it evaluates to true (in this context, anything non-0), jumps to label %1. [c=orange]Direct usage obsolete. Use if/unless statement instead. | 是 | 继承自 TH13 |
| 15 | callAsync | m (sub) | Asynchronously calls a given sub. Can take additional parameters to pass as arguments to the sub. [c=orange]Direct usage obsolete. Use `@subName() async` syntax instead. | 是 | 继承自 TH13 |
| 16 | callAsyncId | mS (sub, id) | Asynchronously calls a given sub and assigns it ID %2. Can take additional parameters to pass as arguments to the sub. [c=orange]Direct usage obsolete, use, `@subName() async id` syntax instead. | 是 | 继承自 TH13 |
| 17 | killAsync | S (id) | Ends most recently called sub that has ID %1 (same ID as in ins_16). If no sub with the given ID is found, nothing happens. Using ID -1 can lead to various unexpected results, ranging from deleting the enemy to freezing the game. | 是 | 继承自 TH13 |
| 18 | ins_18 | S (id) | Let `vm` be the most recent async sub running with ID %1: this ins sets `vm[0x000011E4]` to 1. | 否/待确认 | 继承自 TH13 |
| 19 | ins_19 | S (id) | Let `vm` be the most recent async sub running with ID %1: this ins sets `vm[0x000011E4]` to 0. | 否/待确认 | 继承自 TH13 |
| 20 | ins_20 | SS (id, b) | Let `vm` be the most recent async sub running with ID %1: this ins sets `vm[0x0000101C]` to %2. | 否/待确认 | 继承自 TH13 |
| 21 | killAllAsync | — | Ends all running async subs. Calling this in an async sub can lead to unexpected results, such as crashing the game. | 是 | 继承自 TH13 |
| 22 | debug22 | Sm (a, b) | Debug instruction, code does not exist in the release builds of the game. Most likely used to call sub %2 if some variable set in a debug menu is equal to %1. | 是 | 继承自 TH13 |
| 23 | wait | S (time) | Stops sub execution for %1 frames. | 是 | 继承自 TH13 |
| 24 | waitf | f (time) | ins_23, but time is given as a float instead of an int. Subframes do actually exist and affect ins_547. | 是 | 继承自 TH13 |
| 25 | ins_25 | — |  | 否/待确认 | 继承自 TH-1 |
| 26 | ins_26 | — |  | 否/待确认 | 继承自 TH-1 |
| 27 | unknown27 | — |  | 否/待确认 | 继承自 TH-1 |
| 28 | ins_28 | — |  | 否/待确认 | 继承自 TH-1 |
| 29 | ins_29 | — |  | 否/待确认 | 继承自 TH-1 |
| 30 | unknown30 | m (formatString) | Some sort of `printf` debug instruction, which can take additional float/int arguments after %1. Its code does not exist in the release builds. | 是 | 继承自 TH13 |
| 31 | unknown31 | — |  | 否/待确认 | 继承自 TH-1 |
| 32 | ins_32 | — |  | 否/待确认 | 继承自 TH-1 |
| 33 | ins_33 | — |  | 否/待确认 | 继承自 TH-1 |
| 34 | ins_34 | — |  | 否/待确认 | 继承自 TH-1 |
| 35 | ins_35 | — |  | 否/待确认 | 继承自 TH-1 |
| 36 | ins_36 | — |  | 否/待确认 | 继承自 TH-1 |
| 37 | ins_37 | — |  | 否/待确认 | 继承自 TH-1 |
| 38 | ins_38 | — |  | 否/待确认 | 继承自 TH-1 |
| 39 | ins_39 | — |  | 否/待确认 | 继承自 TH-1 |
| 40 | stackAlloc | S (size) | Increases the ECL stack pointer by %1 bytes (probably), to make space for sub variables. [c=orange]Obsolete, thecl generates this instruction automatically. | 是 | 继承自 TH13 |
| 41 | ins_41 | — |  | 否/待确认 | 继承自 TH-1 |
| 42 | pushi | S (num) | Pushes an integer to the ECL stack. [c=orange]Obsolete, push values to stack by writing unassigned expressions instead. | 是 | 继承自 TH13 |
| 43 | seti | S (var) | Pops an integer from the stack into variable %1. [c=orange]Obsolete, use assignment syntax instead. | 是 | 继承自 TH13 |
| 44 | pushf | f (num) | Pushes a float to the ECL stack. [c=orange]Obsolete, push values to stack by writing unassigned expressions instead. | 是 | 继承自 TH13 |
| 45 | setf | f (var) | Pops a float from the stack into variable %1. [c=orange]Obsolete, use assignment syntax instead. | 是 | 继承自 TH13 |
| 46 | ins_46 | — |  | 否/待确认 | 继承自 TH-1 |
| 47 | ins_47 | — |  | 否/待确认 | 继承自 TH-1 |
| 48 | ins_48 | — |  | 否/待确认 | 继承自 TH-1 |
| 49 | ins_49 | — |  | 否/待确认 | 继承自 TH-1 |
| 50 | addi | — | Sums integers on the stack. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 51 | addf | — | Sums floats on the stack. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 52 | subi | — | Subtracts integers on the stack. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 53 | subf | — | Subtracts floats on the stack. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 54 | muli | — | Multiplies integers on the stack. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 55 | mulf | — | Multiplies floats on the stack. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 56 | divi | — | Divides integers on the stack. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 57 | divf | — | Divides floats on the stack. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 58 | modi | — | Modulo operation on integers on the stack. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 59 | eqi | — | Stack integer `==` comparison. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 60 | eqf | — | Stack float `==` comparison. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 61 | neqi | — | Stack integer `!=` comparison. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 62 | neqf | — | Stack float `!=` comparison. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 63 | lessi | — | Stack integer `<` comparison. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 64 | lessf | — | Stack float `<` comparison. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 65 | leqi | — | Stack integer `<=` comparison. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 66 | leqf | — | Stack float `<=` comparison. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 67 | greateri | — | Stack integer `>` comparison. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 68 | greaterf | — | Stack float `>` comparison. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 69 | geqi | — | Stack integer `>=` comparison. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 70 | geqf | — | Stack float `>=` comparison. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 71 | noti | — | Stack integer NOT operation (e.g. !1). [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 72 | notf | — | Stack float NOT operation (e.g. !1.0f). [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 73 | or | — | Logical OR operation on the stack. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 74 | and | — | Logical AND operation on the stack. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 75 | xor | — | Bitwise XOR operation on integers on the stack. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 76 | bit_or | — | Bitwise OR operation on integers on the stack. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 77 | bit_and | — | Bitwise AND operation on integers on the stack. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 78 | deci | S (var) | Pushes variable %1 to the stack and then decrements it. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 79 | stackSin | — | sin operation on a float on the stack. [c=orange]Obsolete, use `sin(floatVal)` instead. | 是 | 继承自 TH13 |
| 80 | stackCos | — | cos operation on a float on the stack. [c=orange]Obsolete, use `cos(floatVal)` instead. | 是 | 继承自 TH13 |
| 81 | circlePos | ffff (varX, varY, ang, radius) | Performs following operation: [code]%1 = cos(%3)*%4;<br>%2 = sin(%3)*%4;[/code] | 是 | 继承自 TH13 |
| 82 | validRad | f (var) | Normalizes angle in %1. | 是 | 继承自 TH13 |
| 83 | negi | — | Negates an integer on the stack. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 84 | negf | — | Negates a float on the stack. [c=orange]Obsolete, use expressions instead. | 是 | 继承自 TH13 |
| 85 | squareSum | fff (var, x, y) | Performs following operation: [code]%1 = %2*%2 + %3*%3;[/code] | 是 | 继承自 TH13 |
| 86 | squareSumRoot | fff (var, x, y) | Performs following operation: [code]%1 = sqrt(%2*%2 + %3*%3);[/code] | 是 | 继承自 TH13 |
| 87 | getAngle | fffff (var, x1, y1, x2, y2) | Calculates angle from (%2,%3) to (%4,%5) and stores it in %1. | 是 | 继承自 TH13 |
| 88 | stackSqrt | — | square root operation on a float on the stack. [c=orange]Obsolete, use `sqrt(floatVal)` instead. | 是 | 继承自 TH13 |
| 89 | linearFunc | fff (var, a, x) | Performs following operation: [code]%1 = %2*%3;[/code]<br>(what's the point of making this an instruction, ZUN?) | 是 | 继承自 TH13 |
| 90 | pointRotate | fffff (varX, varY, x, y, rad) | Rotates point (%3,%4) by angle %5 and stores the resulting coordinates in %1 and %2. | 是 | 继承自 TH13 |
| 91 | floatTime | SfSSff (slot, var, time, mode, init, final) | In %3 frames using mode %4, variable %2 changes from %5 to %6. %1 is used to set the slot to be used by this ins, every enemy has 8 slots (0 to 7). | 是 | 继承自 TH13 |
| 92 | math92 | SfSSffff (slot, var, time, mode, init, final, m, n) | Same as ins_91, but takes 2 extra arguments of unknown meaning. Needs investigation. | 否/待确认 | 继承自 TH13 |
| 93 | math93 | ffff (varX, varY, r1, r2) | Gets a random point based on %3 and %4 and stores it on (%1,%2). Needs investigation. | 否/待确认 | 继承自 TH13 |

### TH18.5 指令：敌机创建与 ANM 管理 / Enemy creation and ANM script management

| ID | 助记名 | 参数 | 说明 | 文档化 | 来源 |
| --- | --- | --- | --- | --- | --- |
| 300 | enmCreate | mffSSS (sub, x, y, hp, score, item) | Creates an enemy using subroutine %1 at coordinates %2, %3 (relative to position of enemy that called it), health of created enemy is %4, score bonus is %5 and item drop is %6. | 是 | 继承自 TH13 |
| 301 | enmCreateA | mffSSS (sub, x, y, hp, score, item) | Creates an enemy using subroutine %1 at coordinates %2, %3 (absolute position), health of created enemy is %4, score bonus is %5 and item drop is %6. | 是 | 继承自 TH13 |
| 302 | anmSelect | S (anmIndex) | Selects ANM file to be used by other instructions based on %1. | 是 | 继承自 TH13 |
| 303 | anmSetSprite | SS (slot, script) | Loads script %2 from ANM selected with ins_302 on slot %1. | 是 | 继承自 TH13 |
| 304 | enmCreateM | mffSSS (sub, x, y, hp, score, item) | Creates a mirrored enemy using subroutine %1 at coordinates %2, %3 (relative to caller's position), health of created enemy is %4, score bonus is %5 and item drop is %6. | 是 | 继承自 TH13 |
| 305 | enmCreateAM | mffSSS (sub, x, y, hp, score, item) | Creates an mirrored enemy using subroutine %1 at coordinates %2, %3 (absolute position), health of created enemy is %4, score bonus is %5 and item drop is %6. | 是 | 继承自 TH13 |
| 306 | anmSetMain | SS (slot, script) | Loads script %2 from ANM selected with ins_302 on slot %1. However, the script number provided will only be used when the enemy is not moving. When moving left %2+1 will be used, right %2+2, diagonal left %2+3, diagonal right %2+4. Might not work properly if %1 is not 0 according to THBWiki. | 是 | 继承自 TH13 |
| 307 | anmPlay | SS (anmIndex, script) | From ANM file selected based on %1, play script %2 at caller's current coordinates. The spawned script is completely independent, and will continue existing even if caller is deleted. | 是 | 继承自 TH13 |
| 308 | anmPlayAbs | SS (anmIndex, script) | From ANM file selected based on %1, play script %2 at coordinates (0, 0). The spawned script is completely independent, and will continue existing even if caller is deleted. | 是 | 继承自 TH13 |
| 309 | enmCreateF | mffSSS (sub, x, y, hp, score, item) | Creates a filler enemy using subroutine %1 at coordinates %2, %3 (relative to caller's position), health of created enemy is %4, score bonus is %5 and item drop is %6. | 是 | 继承自 TH13 |
| 310 | enmCreateAF | mffSSS (sub, x, y, hp, score, item) | Creates a filler enemy using subroutine %1 at coordinates %2, %3 (absolute position), health of created enemy is %4, score bonus is %5 and item drop is %6. | 是 | 继承自 TH13 |
| 311 | enmCreateMF | mffSSS (sub, x, y, hp, score, item) | Creates a mirrored filler enemy using subroutine %1 at coordinates %2, %3 (relative to caller's position), health of created enemy is %4, score bonus is %5 and item drop is %6. | 是 | 继承自 TH13 |
| 312 | enmCreateAMF | mffSSS (sub, x, y, hp, score, item) | Creates a mirrored filler enemy using subroutine %1 at coordinates %2, %3 (absolute position), health of created enemy is %4, score bonus is %5 and item drop is %6. | 是 | 继承自 TH13 |
| 313 | anmSelectedPlay | S (script) | Same as ins_307, except it uses the ANM file selected by ins_302. | 是 | 继承自 TH13 |
| 314 | anmPlayHigh | SS (anmIndex, script) | Same as ins_307, except it spawns the ANM with a higher layer? Needs further investigation. | 否/待确认 | 继承自 TH13 |
| 315 | anmPlayRotate | SSf (anmIndex, script, angle) | Same as ins_307, except it sets rotation of spawned ANM to %3. | 是 | 继承自 TH13 |
| 316 | anm316 | SS (a, b) | Unknown. | 否/待确认 | 继承自 TH13 |
| 317 | anmSwitch | SS (slot, switch) | Sets the execution pointer of ANM script on slot %1 to where ANM `ins_5(a)` with `a` == `switch` is (the time is also changed to match time of `ins_5`). Doesn't work if the value is 0 apparently? | 是 | 继承自 TH13 |
| 318 | anmReset | — | Resets some ANM-related parameters of the caller (TODO: what exactly?) | 是 | 继承自 TH13 |
| 319 | anmRotate | Sf (slot, r) | Set rotation of an ANM script on slot %1 to %2. | 是 | 继承自 TH13 |
| 320 | anmMove | Sff (slot, x, y) | Set position of an ANM script on slot %1 to (%2,%3). This does not detach the script from the caller, so the actual position of the script will be position of the caller + position set here. | 是 | 继承自 TH13 |
| 321 | enmMapleEnemy | mffSSS (sub, x, y, hp, score, item) | ins_300, but used by 'MapleEnemy' (TODO: what's the difference from ins_300?) | 是 | 继承自 TH13 |
| 322 | enm322 | SS (a, b) | Unknown. | 否/待确认 | 继承自 TH13 |
| 323 | deathAnm | SS (anmIndex, script) | Set the animation that will play when the enemy dies to script %2 from ANM file specified by %1. | 是 | 继承自 TH13 |
| 324 | enmPos2 | — | Unknown. | 否/待确认 | 继承自 TH13 |
| 325 | anmColor | SSSS (slot, R, G, B) | Modify color of ANM script on slot %1, %2, %3, [c=lightblue]%4 correspond to individual colors and have to be from 0 to 255. | 是 | 继承自 TH13 |
| 326 | anmColorTime | SSSSSS (slot, time, mode, R, G, B) | Same as ins_325, but the change is applied in %2 frames using mode %3. | 是 | 继承自 TH13 |
| 327 | anmAlpha | SS (slot, alpha) | Sets alpha of ANM script on slot %1 to %2 (must be a value between 0-255) | 是 | 继承自 TH13 |
| 328 | anmAlphaTime | SSSS (slot, time, mode, alpha) | Same as ins_327, but the change is applied in %2 frames using mode %3. | 是 | 继承自 TH13 |
| 329 | anmScale | Sff (slot, w, h) | Sets horizontal and vertical scaling of ANM script on slot %1 to %2 and %3 respectively. Overwrites scaling properties set by the ANM script. | 是 | 继承自 TH13 |
| 330 | anmScaleTime | SSSff (slot, time, mode, w, h) | Same as ins_329, but the change is applied in %2 frames using mode %3. | 是 | 继承自 TH13 |
| 331 | anmAlpha2 | SS (slot, alpha) | Sets alpha2 (opacity of the gradient) of ANM script on slot %1 to %2. | 是 | 继承自 TH13 |
| 332 | anmAlpha2Time | SSSS (slot, time, mode, alpha) | Same as ins_331, but the change is applied in %2 frames using mode %3. | 是 | 继承自 TH13 |
| 333 | anm333 | SSSff (a, b, c, r, s) | Unknown. Might be doing something to ANM script on slot %1. | 否/待确认 | 继承自 TH13 |
| 334 | anm334 | S (a) | Hard to tell? THBWiki Google translate gives this: 'The animation effect of the playing unit (enemy), the lightning effect near the evil spirit ball of the god temple', which might be referring to lightning around Nue in TD extra stage. | 否/待确认 | 继承自 TH13 |
| 335 | anmScale2 | Sff (slot, w, h) | Same as ins_329, except it doesn't overwrite the scaling set by the ANM script - instead, it multiplies it. | 是 | 继承自 TH13 |
| 336 | anmLayer | SS (slot, layer) | Set layer of ANM script on slot %1 to %2. | 是 | 继承自 TH14 |
| 337 | anmBlendMode | SS (slot, b) | Set blend mode of ANM script on slot %1 to %2 (TODO: make a list of blend modes). | 是 | 继承自 TH16 |
| 338 | anmPlayPos | SSfff (anmIndex, script, x, y, z) | Same as ins_307, but the spawned script is offset by (%3,%4). For 3D objects, %5 is used too (TODO: verify that). | 是 | 继承自 TH16 |
| 339 | anm339 | SSS (a, b, c) | Unknown. Might be doing something to ANM script on slot %1. | 否/待确认 | 继承自 TH16 |
| 340 | enmDelete | S (id) | Delete enemy with the given ID. | 是 | 继承自 TH16 |

### TH18.5 指令：移动管理 / Movement management

| ID | 助记名 | 参数 | 说明 | 文档化 | 来源 |
| --- | --- | --- | --- | --- | --- |
| 400 | movePos | ff (x, y) | Sets caller's absolute position to %1, %2. | 是 | 继承自 TH13 |
| 401 | movePosTime | SSff (time, mode, x, y) | Same as ins_400, but the change is applied in %1 frames using mode %2. | 是 | 继承自 TH13 |
| 402 | movePosRel | ff (x, y) | Sets caller's relative position to %1, %2. | 是 | 继承自 TH13 |
| 403 | movePosRelTime | SSff (time, mode, x, y) | Same as ins_402, but the change is applied in %1 frames using mode %2. | 是 | 继承自 TH13 |
| 404 | moveVel | ff (r, spd) | Sets caller's absolute movement angle to %1 and speed to %2. | 是 | 继承自 TH13 |
| 405 | moveVelTime | SSff (time, mode, r, spd) | Same as ins_404, but the change is applied in %1 frames using mode %2. | 是 | 继承自 TH13 |
| 406 | moveVelRel | ff (r, spd) | Sets caller's relative movement angle to %1 and speed to %2. | 是 | 继承自 TH13 |
| 407 | moveVelRelTime | SSff (time, mode, r, spd) | Same as ins_406, but the change is applied in %1 frames using mode %2. | 是 | 继承自 TH13 |
| 408 | moveCircle | ffff (θ, spd, rad, radInc) | Sets caller's absolute circle movement: %1 is the angle indicating initial position on the circle, %2 is the angular velocity, %3 is circle radius and %4 is by how much the radius increases each frame. | 是 | 继承自 TH13 |
| 409 | moveCircleTime | SSfff (time, mode, spd, rad, radInc) | Same as ins_408, but the change is applied in %1 frames using mode %2. There is also no initial angle parameter here for obvious reason. | 是 | 继承自 TH13 |
| 410 | moveCircleRel | ffff (θ, spd, rad, radInc) | Sets caller's relative circle movement: %1 is the angle indicating initial position on the circle, %2 is the angular velocity, %3 is circle radius and %4 is by how much the radius increases each frame. | 是 | 继承自 TH13 |
| 411 | moveCircleRelTime | SSfff (time, mode, spd, rad, radInc) | Same as ins_410, but the change is applied in %1 frames using mode %2. There is also no initial angle parameter here for obvious reason. | 是 | 继承自 TH13 |
| 412 | moveRand | SSf (time, mode, spd) | Randomizes caller's absolute angle and sets absolute speed to %3. The speed changes back to 0 in %1 frames using mode %2. | 是 | 继承自 TH13 |
| 413 | moveRandRel | SSf (time, mode, spd) | Randomizes caller's relative angle and sets relative speed to %3. The speed changes back to 0 in %1 frames using mode %2. | 是 | 继承自 TH13 |
| 414 | moveBoss | — | Sets caller's absolute position to the absolute position of the boss. If called without a boss, [tip=Google translated from THBWiki, I find this sentence funny]it will cause serious mis-access and explode[/tip]. | 是 | 继承自 TH13 |
| 415 | moveBossRel | — | Sets caller's relative position to the relative position of the boss. If called without a boss, [tip=Google translated from THBWiki, I find this sentence funny]it will cause serious mis-access and explode[/tip]. | 是 | 继承自 TH13 |
| 416 | movePos3d | fff (x, y, z) | Same as ins_400, but takes a %3 parameter for the third dimension, which probably affects 3D ANM scripts used by the caller, or something. | 是 | 继承自 TH13 |
| 417 | movePos3dRel | fff (x, y, z) | Same as ins_402, but takes a %3 parameter for the third dimension, which probably affects 3D ANM scripts used by the caller, or something. | 是 | 继承自 TH13 |
| 418 | moveAdd | ff (x, y) | Increases caller's absolute position by %1 and %2. | 是 | 继承自 TH13 |
| 419 | move419 | ff (x, y) | While the code of this ins looks like it's supposed to be a relative version of ins_418, it doesn't seem to behave like that... | 否/待确认 | 继承自 TH13 |
| 420 | moveEllipse | ffffff (θ, spd, rad, radInc, ellDir, ellRatio) | Sets caller's absolute ellipse movement: %1 is the angle indicating initial position on the ellipse, %2 is the angular velocity, %3 is the base circle radius and %4 is by how much the radius increases each frame. %6 is how much the base circle should be 'squished' to make it an ellipse, and %5 is the squishing angle (I don't know math terms in English, sorry) | 是 | 继承自 TH13 |
| 421 | moveEllipseTime | SSfffff (time, mode, spd, rad, radInc, ellDir, ellRatio) | Same as ins_420, but the change is applied in %1 frames using mode %2. There is also no initial angle parameter here for obvious reason | 是 | 继承自 TH13 |
| 422 | moveEllipseRel | ffffff (θ, spd, rad, radInc, ellDir, ellRatio) | Sets caller's relative ellipse movement: %1 is the angle indicating initial position on the ellipse, %2 is the angular velocity, %3 is the base circle radius and %4 is by how much the radius increases each frame. %6 is how much the base circle should be 'squished' to make it an ellipse, and %5 is the squishing angle (I don't know math terms in English, sorry) | 是 | 继承自 TH13 |
| 423 | moveEllipseRelTime | SSfffff (time, mode, spd, rad, radInc, ellDir, ellRatio) | Same as ins_422, but the change is applied in %1 frames using mode %2. There is also no initial angle parameter here for obvious reason | 是 | 继承自 TH13 |
| 424 | moveSetMirror | S (state) | Sets caller's mirror flag to %1. | 是 | 继承自 TH13 |
| 425 | moveBezier | Sffffff (time, x1, y1, x2, y2, x3, y3) | In %1 frames, the enemy moves towards (%2,%3), then moves towards (%6,%7) for a while and finally moves to (%4,%5). Uses absolute position.<br>From THBWiki: <br>(assuming the current coordinates are (x0, y0)) the motion trajectory is actually a Bezier curve from (x0, y0) to (x2, y2);<br>The P1 coordinate of the curve is `((x1-x0)*1/3, (y1-y0)*1/3)`;<br>The P2 coordinate of the curve is `(-(x3-x2)*1/3+x2,-(y3-y2) *1/3+x2)` | 是 | 继承自 TH13 |
| 426 | moveBezierRel | Sffffff (time, x1, y1, x2, y2, x3, y3) | Same as ins_425, but uses relative position. | 是 | 继承自 TH13 |
| 427 | moveReset | — | Resets some movement-related parameters (TODO: what exactly?) | 否/待确认 | 继承自 TH13 |
| 428 | moveVelNM | ff (r, spd) | Same as ins_404, but ignores the mirror flag. | 是 | 继承自 TH13 |
| 429 | moveVelNMTime | SSff (time, mode, r, spd) | Same as ins_405, but ignores the mirror flag. | 是 | 继承自 TH13 |
| 430 | moveVelNMRel | ff (r, spd) | Same as ins_406, but ignores the mirror flag. | 是 | 继承自 TH13 |
| 431 | moveVelNMRelTime | SSff (time, mode, r, spd) | Same as ins_407, but ignores the mirror flag. | 是 | 继承自 TH13 |
| 432 | moveEnm | S (id) | Sets caller's absolute position to absolute position of enemy with var_-9914 == %1. | 是 | 继承自 TH13 |
| 433 | moveEnmRel | S (id) | Sets caller's relative position to relative position of enemy with var_-9914 == %1. | 是 | 继承自 TH13 |
| 434 | moveCurve | SSSff (time, mode, c, x, y) | In %1 frames using mode %2, caller's absolute position is changed to (%4,%5). The movement trajectory is a curve based on %3, it is unknown how it works exactly. | 否/待确认 | 继承自 TH13 |
| 435 | moveCurveRel | SSSff (time, mode, c, x, y) | In %1 frames using mode %2, caller's relative position is changed to (%4,%5). The movement trajectory is a curve based on %3, it is unknown how it works exactly. | 否/待确认 | 继承自 TH13 |
| 436 | moveAddTime | SSff (time, mode, x, y) | Same as ins_418, but the change is applied in %1 frames using mode %2. | 是 | 继承自 TH13 |
| 437 | moveAddRelTime | SSff (time, mode, x, y) | Same as ins_419, but the change is applied in %1 frames using mode %2 (it also behaves as expected, unlike ins_419). | 是 | 继承自 TH13 |
| 438 | moveCurveAdd | SSSff (time, mode, c, x, y) | Same as ins_434, but instead caller's current absolute coordinates are added to %4 and %5. | 是 | 继承自 TH13 |
| 439 | moveCurveAddRel | SSSff (time, mode, c, x, y) | Same as ins_435, but instead caller's current relative coordinates are added to %4 and %5. | 是 | 继承自 TH13 |
| 440 | moveAngle | f (r) | Sets caller's absolute movement angle to %1. | 是 | 继承自 TH14 |
| 441 | moveAngleTime | SSf (time, mode, r) | Same as ins_440, but the change is applied in %1 frames using mode %2. | 是 | 继承自 TH14 |
| 442 | moveAngleRel | f (r) | Sets caller's relative movement angle to %1. | 是 | 继承自 TH14 |
| 443 | moveAngleRelTime | SSf (time, mode, r) | Same as ins_442, but the change is applied in %1 frames using mode %2. | 是 | 继承自 TH14 |
| 444 | moveSpeed | f (spd) | Sets caller's absolute movement speed to %1. | 是 | 继承自 TH14 |
| 445 | moveSpeedTime | SSf (time, mode, spd) | Same as ins_444, but the change is applied in %1 frames using mode %2. | 是 | 继承自 TH14 |
| 446 | moveSpeedRel | f (spd) | Sets caller's relative movement speed to %1. | 是 | 继承自 TH14 |
| 447 | moveSpeedRelTime | SSf (time, mode, spd) | Same as ins_446, but the change is applied in %1 frames using mode %2. | 是 | 继承自 TH14 |

### TH18.5 指令：敌机属性与杂项 / Enemy property management and other miscellaneous things

| ID | 助记名 | 参数 | 说明 | 文档化 | 来源 |
| --- | --- | --- | --- | --- | --- |
| 500 | setHurtbox | ff (w, h) | Sets caller's hurtbox width to %1 and height to %2. | 是 | 继承自 TH13 |
| 501 | setHitbox | ff (w, h) | Sets caller's hitbox width to %1 and height to %2. | 是 | 继承自 TH13 |
| 502 | flagSet | S (n) | Sets flag(s) according to %1. Refer to the [flag table](#s=modding/flags) for exact values. | 是 | 继承自 TH13 |
| 503 | flagClear | S (n) | Clears flag(s) according to %1. Refer to the [flag table](#s=modding/flags) for exact values. | 是 | 继承自 TH13 |
| 504 | moveLimit | ffff (x, y, w, h) | Sets caller's movement limit rectangle: (%1,%2) are the coordinates of the center of the rect, while %3, %4 are width and height of it. | 是 | 继承自 TH13 |
| 505 | moveLimitReset | — | Removes caller's movement limit. | 是 | 继承自 TH13 |
| 506 | dropClear | — | Clears caller's extra item drop. | 是 | 继承自 TH13 |
| 507 | dropExtra | SS (type, amount) | Adds %2 items of type %1 to caller's extra drop. Item type table will be made in the future. | 是 | 继承自 TH13 |
| 508 | dropArea | ff (w, h) | Sets caller's item drop area width to %1 and height to %2. | 是 | 继承自 TH13 |
| 509 | dropItems | — | Drops all items the caller has. Has no effect in spell practice. | 是 | 继承自 TH13 |
| 510 | dropMain | S (type) | Sets caller's main drop to %1. | 是 | 继承自 TH13 |
| 511 | lifeSet | S (hp) | Sets caller's current HP and max HP to %1. | 是 | 继承自 TH13 |
| 512 | setBoss | S (a) | If %1 is 0, activates boss mode and makes the caller the main boss. If %1 > 0, it makes the caller the secondary boss. If %1 is -1, ends boss mode. | 是 | 继承自 TH13 |
| 513 | timerReset | — | Resets boss timer. | 是 | 继承自 TH13 |
| 514 | setInterrupt | SSSm (slot, hp, time, sub) | Sets an interrupt on slot %1 (not sure how many slots there are) - once caller's hp reaches %2 or %3 frames have passed since this was called, caller will terminate all subs it's currently running and execute sub %4. | 是 | 继承自 TH13 |
| 515 | setInvuln | S (time) | Makes the caller completely invulnerable for %1 frames. | 是 | 继承自 TH13 |
| 516 | playSound | S (id) | Plays sound %1. Sound id table will be added in the future. | 是 | 继承自 TH13 |
| 517 | setScreenShake | SSS (time, startIntensity, endIntensity) | Activates screen shake for %1 frames. %2 is the starting intensity and %3 is the ending intensity. The larger the intensity, the more the screen shakes. | 是 | 继承自 TH13 |
| 518 | dialogRead | S (dialogueId) | Starts a dialogue, %1 is the ID of an entry in the .msg file. Apart from that, has the effect ins_525. | 是 | 继承自 TH13 |
| 519 | dialogWait | — | Waits until there are no dialogues active, or the running .msg script calls a certain instruction (which one?) | 否/待确认 | 继承自 TH13 |
| 520 | bossWait | — | Waits until there are no boss enemies. | 是 | 继承自 TH13 |
| 521 | setTimeout | Sm (slot, sub) | Sets a timeout interrupt on slot %1 - when the timer reaches 0, caller will terminate all subs it's currently running and execute sub %2. | 是 | 继承自 TH13 |
| 522 | spellEx | SSSm (id, time, type, name) | Same as ins_537, but the difficulty number is NOT added to the id. | 是 | 继承自 TH16 |
| 523 | spellEnd | — | Ends currently active spellcard. | 是 | 继承自 TH13 |
| 524 | setChapter | S (a) | Some jank that's responsible for showing boss name and possibly other things. In LoLK, it also ends the current chapter and begins a new one. | 否/待确认 | 继承自 TH13 |
| 525 | enmKillAll | — | Kills all other enemies (unless they have a flag that prevents that set). | 是 | 继承自 TH13 |
| 526 | etProtectRange | f (r) | Makes bullets generated by the caller not spawn if they are in radius %1 around the player. | 是 | 继承自 TH13 |
| 527 | lifeMarker | SfS (slot, hp, c) | Sets a new life marker on slot %1, %2 determines where the marker will appear on the health bar (if %2=1000.0f and the enemy has 2000 hp, the marker will split the hp bar in half). %3 is an RGB value of unknown use (possibly leftover from earlier ECL versions) | 是 | 继承自 TH13 |
| 528 | spellUnused | SSSm (id, time, type, name) | No difference from ins_522, unused. | 是 | 继承自 TH16 |
| 529 | rankF3 | ffff (var, a, b, c) | Sets %1 to %2 if rank is low, %3 if rank is average or %4 if rank is high. | 是 | 继承自 TH13 |
| 530 | rankF5 | ffffff (var, a, b, c, d, e) | Sets %1 to %2 if rank is very low, %3 if rank is low, %4 if rank is average, %5 if rank is high or %6 if rank is very high. | 是 | 继承自 TH13 |
| 531 | rankF2 | fff (var, a, b) | Sets %1 to %2 if rank is low or %3 if rank is high. | 是 | 继承自 TH13 |
| 532 | rankI3 | SSSS (var, a, b, c) | Sets %1 to %2 if rank is low, %3 if rank is average or %4 if rank is high. | 是 | 继承自 TH13 |
| 533 | rankI5 | SSSSSS (var, a, b, c, d, e) | Sets %1 to %2 if rank is very low, %3 if rank is low, %4 if rank is average, %5 if rank is high or %6 if rank is very high. | 是 | 继承自 TH13 |
| 534 | rankI2 | SSS (var, a, b) | Sets %1 to %2 if rank is low or %3 if rank is high. | 是 | 继承自 TH13 |
| 535 | diffI | SSSSS (var, E, N, H, L) | Sets %1 to one of values provided based on difficulty. | 是 | 继承自 TH13 |
| 536 | diffF | fffff (var, E, N, H, L) | Sets %1 to one of values provided based on difficulty. | 是 | 继承自 TH13 |
| 537 | spell | SSSm (id, time, mode, name) | Declares a spellcard with id %1 and name %4. The actual ID passed to the spell-creating function is `id + difficulty`, with easy=0, normal=1, hard=2, lunatic=3, ex=4, overdrive=5. <br>%2 determines how much time the spell circle takes to shrink (in frames), as well as how fast the spell bonus decreases. The exact formula is as follows: <br>[code] int factor = maxSCB >> 2; // maxSCB is hardcoded<br> currSCB -= (maxSCB - factor) / (%2 - 300);<br> currSCB -= currSCB % 10; [/code] <br>As you can guess, setting %2 to 300 causes a division by 0 error and crashes the game, while setting it to a value smaller than 300 causes the SCB to increase over time, instead of decreasing. %3 TBD, it's not unused. | 是 | 继承自 TH16 |
| 538 | spell2 | SSSm (id, time, mode, name) | Same as ins_537, except the ID used it `id - 1 + difficulty`. | 是 | 继承自 TH16 |
| 539 | spell3 | SSSm (id, time, mode, name) | Same as ins_537, except the ID used it `id - 2 + difficulty`. | 是 | 继承自 TH16 |
| 540 | stars | S (cnt) | Sets the amount of stars displayed in the top left corner. Stars might not appear at all if there is no boss active. | 是 | 继承自 TH13 |
| 541 | noHitboxDur | S (time) | Disables the hitbox (but not the hurtbox) for the given amount of frames. | 是 | 继承自 TH13 |
| 542 | spellTimeout | — | Makes the current spell a timeout spell (prevent spell bonus from decreasing, give capture bonus if timed out). | 是 | 继承自 TH13 |
| 543 | unknown543 | — | Unknown. | 否/待确认 | 继承自 TH13 |
| 544 | unknown544 | S (a) | Unknown, sets or clears some flag? | 否/待确认 | 继承自 TH13 |
| 545 | laserCancel | — | Cancels all lasers. | 是 | 继承自 TH13 |
| 546 | bombShield | SS (a, script) | Sets the bomb invulnerability flag (%1=1 set, %1=0 not set), the caller's ANM script will change to %2 when a bomb is active (how does it work with ANM slots exactly?) | 是 | 继承自 TH13 |
| 547 | gameSpeed | f (s) | Sets game speed to %1 of the normal speed. In ISC, enemies with flag 13 (dec=8192) set will ignore effects of this opcode. | 是 | 继承自 TH13 |
| 548 | diffWait | SSSS (e, n, h, l) | Same as ins_23, but the wait time is chosen from the given 4 based on the difficulty. | 是 | 继承自 TH13 |
| 549 | unknown549 | S (a) | Unknown. | 否/待确认 | 继承自 TH13 |
| 550 | unknown550 | S (a) | Unknown. | 否/待确认 | 继承自 TH13 |
| 551 | unknown551 | S (a) | Unknown. | 否/待确认 | 继承自 TH13 |
| 552 | zIndex | S (layers) | Increases layer of all ANM scripts used by the caller by %1. | 是 | 继承自 TH13 |
| 553 | hitSound | S (id) | Makes the caller play sound %1 when hit. Sound id table will be added in the future. | 是 | 继承自 TH13 |
| 554 | stageLogo | — | Shows the stage logo from an ANM of a hardcoded name. | 是 | 继承自 TH13 |
| 555 | enmAlive | SS (var, id) | Checks if enemy of var_-9914 == %2 is still alive, and sets %1 to 1 if it is or 0 if it isn't. | 是 | 继承自 TH13 |
| 556 | setDeath | m (sub) | Makes the caller execute sub %1 when the HP reaches 0. Keep in mind that the caller is already marked for deletion at the point when the sub actually executes, so if you put waiting there the sub will not execute fully (because the caller will be deleted) | 是 | 继承自 TH13 |
| 557 | fogTime | SSSff (time, mode, color, start, end) | Same as STD ins_9, that is, fogTime. Refer to [the STD instruction table](#s=modding/std-ins) for details. | 是 | 继承自 TH13 |
| 558 | flagMirror | S (state) | Literally the exact same instruction as ins_424. | 是 | 继承自 TH13 |
| 559 | enmLimit | S (limit) | Set the maximum number of enemies that can be present. New enemies will fail to spawn if the cap is reached. Default is 99999. | 是 | 继承自 TH13 |
| 560 | unknown560 | ff (r, s) | Unknown. | 否/待确认 | 继承自 TH13 |
| 561 | die | — | Makes the caller execute the sub set with ins_556. If there is no such sub set, the caller dies instead (exactly the same as if the player shot down the caller, that is, items are dropped, death sound plays etc) | 是 | 继承自 TH13 |
| 562 | dropItemsSp | — | Same as ins_509, but item spawning will not be blocked in spell practice. | 是 | 继承自 TH13 |
| 563 | unknown563 | S (flagState) | Sets [flag 12](#s=modding/flags) (decimal 4096), which controls whether the hitbox and hurtbox is a rectangle. If %1 is 1, collision is a rectangle. If %1 is 0, collision is elliptical. | 是 | 继承自 TH14 |
| 564 | hitboxRotate | f (angle) | Rotates the hitbox and hurtbox of the enemy (note: the hitbox rotation is really janky, but hurtbox rotates fine). Has no effect unless the enemy uses rectangular collision. | 是 | 继承自 TH14 |
| 565 | bombInvuln | f (red) | Sets caller's damage reduction when a bomb is active, 0.0f means no damage at all, 1.0f is full damage, negative values will make the enemy heal when you bomb. | 是 | 继承自 TH14 |
| 566 | unknown566 | () | Unknown (does it even exist?) | 否/待确认 | 继承自 TH14 |
| 567 | unknown567 | S (a) | Unknown. | 否/待确认 | 继承自 TH14 |
| 568 | spellMode | S (state) | Enables/disables spell card damage reduction, if %1 is 1 it's enabled, if it's 0 it's disabled. Can be used outside of spell cards. | 是 | 继承自 TH14 |
| 569 | unknown569 | S (a) | Unknown. | 否/待确认 | 继承自 TH15 |
| 570 | unknown570 | — | Unknown. | 否/待确认 | 继承自 TH15 |
| 571 | unknown571 | — | Unknown. | 否/待确认 | 继承自 TH15 |
| 572 | lifeNow | S (hp) | Sets caller's current HP to %1, without changing max HP. | 是 | 继承自 TH16 |

### TH18.5 指令：子弹创建与删除 / Bullet creation and deletion

| ID | 助记名 | 参数 | 说明 | 文档化 | 来源 |
| --- | --- | --- | --- | --- | --- |
| 600 | etNew | S (etId) | Resets bullet manager %1 to default properties. | 是 | 继承自 TH13 |
| 601 | etOn | S (etId) | Shoots bullet(s) using properties from bullet manager %1. | 是 | 继承自 TH13 |
| 602 | etSprite | SSS (etId, type, color) | Sets bullet type and color of bullet manager %1. Refer to [this image](https://cdn.discordapp.com/attachments/395767870119870466/570658618316161041/BULLET_IDS.png) made by Dai. Remarks:<br>- bullet types 35 and 36 spin<br>- type 30 pulses<br>- the difference between 16/37 is the spin direction (same case for 23 and 24) | 是 | 继承自 TH15 |
| 603 | etOffset | Sff (etId, x, y) | Sets the relative offset of bullets spawned by bullet manager %1 to (%2,%3). | 是 | 继承自 TH13 |
| 604 | etAngle | Sff (etId, angle1, angle2) | Sets angle1 and angle2 of bullet manager %1. | 是 | 继承自 TH13 |
| 605 | etSpeed | Sff (etId, speed1, speed2) | Sets speed1 and speed2 of bullet manager %1. | 是 | 继承自 TH13 |
| 606 | etCount | SSS (etId, count1, count2) | Sets count1 and count2 of bullet manager %1. | 是 | 继承自 TH13 |
| 607 | etAim | SS (etId, aim) | Sets aim mode of bullet manager %1. | 是 | 继承自 TH13 |
| 608 | etSound | SSS (etId, sound1, sound2) | Sets sound1 and sound2 of bullet manager %1 (sound effect table is TODO). sound1 plays when the bullet manager fires a bullet, while sound2 plays when a bullet fired by the bullet manager does certain transformations. Set to -1 for no sound. | 是 | 继承自 TH13 |
| 609 | etExSet | SSSSSSff (etId, index, async, type, a, b, r, s) | Sets bullet transformation of bullet manager %1, transformation explanation will be added in the future. | 是 | 继承自 TH13 |
| 610 | etExSet2 | SSSSSSSSffff (etId, index, async, type, a, b, c, d, r, s, m, n) | Same as ins_609, but takes more arguments for certain transformation types. | 是 | 继承自 TH13 |
| 611 | etEx | SSSSSff (etId, async, type, a, b, r, s) | Adds bullet transformation to bullet manager %1, transformation explanation will be added in the future. | 是 | 继承自 TH13 |
| 612 | etEx2 | SSSSSSSffff (etId, async, type, a, b, c, d, r, s, m, n) | Same as ins_611, but takes more arguments for certain transformation types. | 是 | 继承自 TH13 |
| 613 | etClearAll | — | Clears all bullets. | 是 | 继承自 TH13 |
| 614 | etCopy | SS (etIdDest, etIdSrc) | Copies everything from bullet manager %2 into bullet manager %1. Warning: this instruction is partially broken and does NOT copy the index next ins_611/ins_612 transformations will be added at. | 是 | 继承自 TH13 |
| 615 | etCancel | f (r) | Clears all bullets in a circle of radius %1 around the caller, and turns them into cancel items. | 是 | 继承自 TH13 |
| 616 | etClear | f (r) | Clears all bullets in a circle of radius %1 around the caller without turning them into cancel items. | 是 | 继承自 TH13 |
| 617 | etSpeedR3 | Sffffff (etId, spd1l, spd1m, spd1h, spd2l, spd2m, spd2h) | Sets speed1 and speed2 of bullet manager %1 to two of the values provided, based on ingame rank (l=low, m=medium, h=high) | 是 | 继承自 TH13 |
| 618 | etSpeedR5 | Sffffffffff (etId, spd1l, spd1ml, spd1m, spd1mh, spd1h, spd2l, spd2ml, spd2m, spd2mh, spd2h) | Sets speed1 and speed2 of bullet manager %1 to two of the values provided, based on ingame rank (l=low, ml=medium-low, m=medium, mh=medium-high, h=high) | 是 | 继承自 TH13 |
| 619 | etSpeedR2 | Sffff (etId, spd1l, spd1h, spd2l, spd2h) | Sets speed1 and speed2 of bullet manager %1 to two of the values provided, based on ingame rank (l=low, h=high) | 是 | 继承自 TH13 |
| 620 | etCountR3 | SSSSSSS (etId, cnt1l, cnt1m, cnt1h, cnt2l, cnt2m, cnt2h) | Sets count1 and count2 of bullet manager %1 to two of the values provided, based on ingame rank (l=low, m=medium, h=high) | 是 | 继承自 TH13 |
| 621 | etCountR5 | SSSSSSSSSSS (etId, cnt1l, cnt1ml, cnt1m, cnt1mh, cnt1h, cnt2l, cnt2ml, cnt2m, cnt2mh, cnt2h) | Sets count1 and count2 of bullet manager %1 to two of the values provided, based on ingame rank (l=low, ml=medium-low, m=medium, mh=medium-high, h=high) | 是 | 继承自 TH13 |
| 622 | etCountR2 | SSSSS (etId, cnt1l, cnt1h, cnt2l, cnt2h) | Sets count1 and count2 of bullet manager %1 to two of the values provided, based on ingame rank (l=low, h=high) | 是 | 继承自 TH13 |
| 623 | angleToPlayer | fff (var, x, y) | Gets angle to the player from coordinates (%2,%3) and stores it in %1. | 是 | 继承自 TH13 |
| 624 | etSpeedD | Sffffffff (etId, spd1e, spd1n, spd1h, spd1l, spd2e, spd2n, spd2h, spd2l) | Sets speed1 and speed2 of bullet manager %1 to 2 of the values provided, based on the difficulty (e=easy, n=normal, h=hard, l=lunatic) | 是 | 继承自 TH13 |
| 625 | etCountD | SSSSSSSSS (etId, cnt1e, cnt1n, cnt1h, cnt1l, cnt2e, cnt2n, cnt2h, cnt2l) | Sets count1 and count2 of bullet manager %1 to 2 of the values provided, based on the difficulty (e=easy, n=normal, h=hard, l=lunatic) | 是 | 继承自 TH13 |
| 626 | etOffsetRad | Sff (etId, angle, radius) | Sets the relative offset of bullets spawned by bullet manager %1 to (cos(%2)\*%3,sin(%2)\*%3). Stacks with ins_603. | 是 | 继承自 TH13 |
| 627 | etDist | Sf (etId, dist) | Sets distance of bullets spawned by bullet manager %1 to %2 (that is, when a bullet is spawned it moves by %2 using its current angle). | 是 | 继承自 TH13 |
| 628 | etOffsetAbs | Sff (etId, x, y) | Sets the absolute offset of bullets spawned by bullet manager %1 to (%2,%3). | 是 | 继承自 TH13 |
| 629 | fog | fS (r, color) | Sets caller's fog's radius to %1 and color to %2 (RGB value in reverse order). This resets the fog completely, that is, every time it's called the fog spawn animation plays. | 是 | 继承自 TH13 |
| 630 | callSTD | S (switch) | Sets execution pointer of the STD script to where STD ins_16(%1) is (%1 must be the same), basically same concept as ins_317. | 是 | 继承自 TH13 |
| 631 | lifeHide | S (time) | Hides boss lifebar for %1 frames. | 是 | 继承自 TH13 |
| 632 | funcSet | S (id) | Sets a function that the game will execute every frame from a set of hardcoded functions that differs between games. | 是 | 继承自 TH13 |
| 633 | flagExtDmg | S (state) | Sets the external damage flag to %1. Caller probably needs to be the main boss for this to work - with this flag set, the caller gets damaged by the value stored in var_-9940 every frame, and then resets the value. This allows other enemies to damage the boss by incrementing the aforementioned variable, used in LoLK by Sagume (and also happens to be the main cause of the Sagume skip glitch) | 是 | 继承自 TH13 |
| 634 | setHitboxFunc | S (id) | Make the caller use a special function for determining collision with the player. TODO: create a list of functions and their IDs | 是 | 继承自 TH13 |
| 635 | etCancel2 | f (r) | Same as ins_615, but doesn't clear bullets with bomb invulnerability. | 是 | 继承自 TH13 |
| 636 | etClear2 | f (r) | Same as ins_616, but doesn't clear bullets with bomb invulnerability. | 是 | 继承自 TH13 |
| 637 | funcCall | S (id) | Same as ins_632, except the function is called just once instead of every frame. | 是 | 继承自 TH13 |
| 638 | scoreAdd | S (n) | Adds %1 to score (or subtracts if %1 is negative). There is no lower boundary check, so if this causes score to go below 0, an underflow happens. | 是 | 继承自 TH13 |
| 639 | funcSet2 | S (id) | Same as ins_632, except it sets an unknown flag to 1 (ins_632 sets it to 0) | 是 | 继承自 TH13 |
| 640 | etExSub | SSm (etId, index, s) | Sets the string parameter of transform on index %2 in bullet manager %1 to %3, transformations will be explained separately later. | 是 | 继承自 TH13 |
| 641 | etExSubtract | S (etId) | Subtracts 1 from the index used by ins_611 and ins_612, unless it's already 0. This basically changes where the next transformation will be appended. | 是 | 继承自 TH14 |

### TH18.5 指令：激光创建 / Laser creation

| ID | 助记名 | 参数 | 说明 | 文档化 | 来源 |
| --- | --- | --- | --- | --- | --- |
| 700 | laserNew | Sffff (etId, init_length, final_length, unknown_arg_3, width) | Sets basic parameters of the laser. %4 has something to do with the length of straight line lasers (investigation needed), but doesn't do anything for other laser types. For curvy lasers, the only used argument is %5, and length is specified with ins_701 instead. | 是 | 继承自 TH13 |
| 701 | laserTiming | SSSSSS (edId, startup_time, expand_time, duration, shrink_time, init_flags) | Sets timing for infinite lasers. %6 sets the initial flags for a laser, but these flags are unknown at the moment. For curvy lasers, the %2 argument instead specifies the length of the laser. | 是 | 继承自 TH13 |
| 702 | laserOn | S (edId) | Shoots a straight line laser. | 是 | 继承自 TH13 |
| 703 | laserStOn | SS (etId, laser_id) | Shoots an infinite laser. %2 is a number that's used to identify this particular laser instance, so that it can be referred to in other instructions. | 是 | 继承自 TH13 |
| 704 | laserOffset | Sff (laser_id, x, y) | Sets the position of the infinite laser pointed to by %1. | 是 | 继承自 TH13 |
| 705 | laserTrajectory | Sff (laser_id, x_speed, y_speed) | Sets the offset velocity of the infinite laser pointed to by %1. The laser's position will change by %2 and %3 every frame. | 是 | 继承自 TH13 |
| 706 | laserStLength | Sf (laser_id, speed) | Sets the speed of the infinite laser pointed to by %1. | 是 | 继承自 TH13 |
| 707 | laserStWidth | Sf (laser_id, width) | Sets the width of the infinite laser pointed to by %1. | 是 | 继承自 TH13 |
| 708 | laserStAngle | Sf (laser_id, angle) | Sets the angle of the infinite laser pointed to by %1. | 是 | 继承自 TH13 |
| 709 | laserStRotation | Sf (laser_id, angular_vel) | Sets the angular velocity of the infinite laser pointed to by %1. The laser's angle will change by %2 every frame. | 是 | 继承自 TH13 |
| 710 | laserStEnd | S (laser_id) | Clears the laser pointed to by %1. | 是 | 继承自 TH13 |
| 711 | laserCuOn | S (etId) | Shoots a curvy laser. | 是 | 继承自 TH13 |
| 712 | etCancelRect | ff (w, h) | Cancels all bullets in rectangle of width %1 and height %2. The area is affected by rotation set by ins_564. | 是 | 继承自 TH14 |
| 713 | unknown713 | SS (etId, laser_id) | Shoots a laser 'beam', a laser type used by marisa in GFW. Broken since this laser type does not exist outside of GFW. | 是 | 继承自 TH13 |
| 714 | unknown714 | SS (laser_id, unknown) | Does something with a laser beam pointed to by %1. Broken since this laser type does not exist outside of GFW. | 是 | 继承自 TH13 |

### TH18.5 指令：敌机交互 / Enemy interaction

| ID | 助记名 | 参数 | 说明 | 文档化 | 来源 |
| --- | --- | --- | --- | --- | --- |
| 800 | enmCall | Sm (id, sub) | Makes enemy with var_-9914 == %1 stop all subs it's running and execute sub %2 (works like an interrupt). This will NOT make the enemy execute the sub right as this instruction is called, the new sub will be executed when the game handles the given enemy, which might be later on the same frame or on the next frame. Using this to make the caller interrupt itself can make the game explode. | 是 | 继承自 TH13 |
| 801 | enmPos | ffS (varX, varY, id) | Stores coordinates of enemy with var_-9914 == %3 in (%1,%2). | 是 | 继承自 TH13 |
| 802 | broadcastInterrupt | S (slot) | For all existing bosses, trigger the interrupt set by ins_514 on slot %1. Does not change the HP to the one set in ins_514. | 是 | 继承自 TH13 |

### TH18.5 指令：调试 / Debug

| ID | 助记名 | 参数 | 说明 | 文档化 | 来源 |
| --- | --- | --- | --- | --- | --- |
| 900 | debug900 | — | 未在 Priw8 表中记录/待确认 | 否/待确认 | — |
| 901 | debug901 | — | 未在 Priw8 表中记录/待确认 | 否/待确认 | — |
| 902 | debug902 | — | 未在 Priw8 表中记录/待确认 | 否/待确认 | — |
| 903 | debug903 | — | 未在 Priw8 表中记录/待确认 | 否/待确认 | — |
| 904 | debug904 | — | 未在 Priw8 表中记录/待确认 | 否/待确认 | — |

### TH18.5 指令：游戏特有 / Game specific

| ID | 助记名 | 参数 | 说明 | 文档化 | 来源 |
| --- | --- | --- | --- | --- | --- |
| 1000 | spec0 | — | 未在 Priw8 表中记录/待确认 | 否/待确认 | — |
| 1001 | spec1 | — | 未在 Priw8 表中记录/待确认 | 否/待确认 | — |
| 1002 | spec2 | — | Opens the shop. | 是 | 本作 |
| 1003 | spec3 | — | 未在 Priw8 表中记录/待确认 | 否/待确认 | — |
| 1004 | spec4 | S (wave) | Sets the current wave number to %1. | 是 | 本作 |
| 1005 | spec5 | — | Increments the current wave number by 1. | 是 | 本作 |
| 1006 | spec6 | m (name) | Sets the current wave name to %1. Expected to be used by enemies spawned by ins_1012. | 是 | 本作 |
| 1007 | spec7 | — | 未在 Priw8 表中记录/待确认 | 否/待确认 | — |
| 1008 | spec8 | — | Increments the difficulty number by 1 if it's less than 7. | 是 | 本作 |
| 1009 | spec9 | — | 未在 Priw8 表中记录/待确认 | 否/待确认 | — |
| 1010 | spec10 | — | Clears weighted picker data. | 是 | 本作 |
| 1011 | spec11 | SS (subID, weight) | Adds the given subID with weight %2 to the weighted picker data. %1 refers to a hardcoded sub name. | 是 | 本作 |
| 1012 | spec12 | S (flags) | Invokes the weighted picker using values set by ins_1011. Based on the chosen subID, the game picks a sub name from a hardcoded list and spawns an enemy using that sub. Also makes the wave intro text show up. Effect of %1 is unknown. | 否/待确认 | 本作 |
| 1013 | spec13 | SSSSSSSSS (slot, d0, d1, d2, d3, d4, d5, d6, d7) | Writes a bunch of numbers (%2-%9) to storage slot specified by %1. | 是 | 本作 |
| 1014 | spec14 | — | 未在 Priw8 表中记录/待确认 | 否/待确认 | — |
| 1015 | spec15 | SS (&var, slot) | Retrieve one of the numbers stored by ins_1013 in the given slot based on the current difficulty number into %1. | 是 | 本作 |
| 1016 | spec16 | — | 未在 Priw8 表中记录/待确认 | 否/待确认 | — |
| 1017 | spec17 | — | Finishes the stage and shows a selection of cards you can choose from to unlock one. | 是 | 本作 |
| 1018 | spec18 | — | 未在 Priw8 表中记录/待确认 | 否/待确认 | — |
| 1019 | spec19 | — | Finishes the stage as "failed", not letting you choose anything. | 是 | 本作 |
| 1020 | spec20 | — | 未在 Priw8 表中记录/待确认 | 否/待确认 | — |
| 1021 | ins_1021 | — | 未在 Priw8 表中记录/待确认 | 否/待确认 | — |
| 1022 | ins_1022 | — | 未在 Priw8 表中记录/待确认 | 否/待确认 | — |
| 1023 | ins_1023 | — | 未在 Priw8 表中记录/待确认 | 否/待确认 | — |
| 1024 | ins_1024 | — | 未在 Priw8 表中记录/待确认 | 否/待确认 | — |
| 1025 | ins_1025 | — | 未在 Priw8 表中记录/待确认 | 否/待确认 | — |

