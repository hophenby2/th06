# TH12 stage06 Boss ECL → LuaSTG/THlib 公共库版本

## 目标

这个版本不依赖 `liu_10_mc` 私有库，只依赖 LuaSTG/THlib 公共环境：

- `task.New`、`task._Wait`、`task.MoveTo`
- `New`、`SetV2`、`Angle`、`cos`、`sin`
- THlib editor 的 `_straight` bullet class
- 常规 `player`、`ran`、`lstg.var` 全局

生成命令：

```sh
python3 -m th062.ecl_ir.cli luastg th062/th12/stage06.decl \
  --runtime thlib \
  --output th062/ecl_ir_out/luastg_stage06_boss_thlib/ecl_stage06_boss_thlib.lua \
  --module-name ecl_stage06_boss_thlib
```

## 与 liu_10_mc 版本的区别

- liu_10_mc 版本直接调用 `liu_10_mc.bullet.ShotBulletMode(...)`。
- THlib 版本在生成脚本内注入 `ecl_shot(...)`，用 `New(_straight, ...)` 展开 fan/ring/layer。
- 不生成 `_editor_class[Bullet_*]`，而是直接把 ECL 的 `style/color` 传给 `_straight`。
- `ins_312` 随机移动不再调用 `_editor_tasks["liu_10_mc_moveRand"]`，而是本地 `ecl_move_rand(...)` 近似实现。

## 当前 THlib 运行时 helper

`ecl_shot(mode,num,style,color,x,y,dx,dy,dis,o,r,way,layer,spd1,spd2,ang1,ang2,param)` 封装了一个跨 LuaSTG 后端的语义发弹对象：

- `mode=0`：自机狙 fan。
- `mode=1`：固定角 fan。
- `mode=2`：自机狙 ring。
- `mode=3`：固定角 ring。
- `way/layer`：对应 ECL `ins_506/522`。
- `spd1/spd2`：对应 ECL `ins_505/521`，按 layer 插值。
- `ang1/ang2`：ECL 弧度经 `ecl_rad` 转成 LuaSTG 角度。
- `style/color`：直接喂给 `_straight` 的 `imgclass/index`。

## 验证

已通过：

```sh
python3 -m py_compile th062/ecl_ir/cli.py th062/ecl_ir/luastg_backend.py th062/ecl_ir/luastg_lifter.py
lua -e 'assert(loadfile("th062/ecl_ir_out/luastg_stage06_boss_thlib/ecl_stage06_boss_thlib.lua"))'
python3 -m th062.ecl_ir.cli luastg-lift th062/ecl_ir_out/luastg_stage06_boss_thlib/ecl_stage06_boss_thlib.lua --output /tmp/luastg_lift.json
```

`luastg-lift` 在该生成脚本上识别出：

- `BulletEmitter`：71 个
- `Movement`：47 个
- `Wait`：89 个

## 局限

- `_straight` 只能覆盖直线子弹，`ins_509` 的复杂变换目前只保存在 `param`，未完全执行。
- 激光还未映射到 THlib `laser`/`laser_bent`，需要下一步 `LaserEmitter` helper。
- THlib `_straight` 的 `style/color` 是否与 ECL `style/color` 完全一致取决于资源表，当前是近似直传。
