# ECL semantic op_key alignment

IR 不以 source→target 一对一 opcode 为核心；每行是一个语义 op_key，在各游戏里选择可用的 opcode 与参数格式。参数签名不同的 op 由 `th062/ecl_ir/arg_adapter.py` 的字段语义 layout 负责重排/补默认/判定不可安全转换。

| op_key | domain | th08 | th10 | th11 | th12 | th13 | th14 | th15 | th16 | th17 | th18 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| anm.alpha | anm |  |  |  |  | ins_327 `SS` | ins_327 `SS` | ins_327 `SS` | ins_327 `SS` | ins_327 `SS` | ins_327 `SS` |
| anm.alpha2 | anm |  |  |  |  | ins_331 `SS` | ins_331 `SS` | ins_331 `SS` | ins_331 `SS` | ins_331 `SS` | ins_331 `SS` |
| anm.alpha2_time | anm |  |  |  |  | ins_332 `SSSS` | ins_332 `SSSS` | ins_332 `SSSS` | ins_332 `SSSS` | ins_332 `SSSS` | ins_332 `SSSS` |
| anm.alpha_time | anm |  |  |  |  | ins_328 `SSSS` | ins_328 `SSSS` | ins_328 `SSSS` | ins_328 `SSSS` | ins_328 `SSSS` | ins_328 `SSSS` |
| anm.anm316 | anm |  |  |  |  | ins_316 `SS` | ins_316 `SS` | ins_316 `SS` | ins_316 `SS` | ins_316 `SS` | ins_316 `SS` |
| anm.anm333 | anm |  |  |  |  | ins_333 `SSSff` | ins_333 `SSSff` | ins_333 `SSSff` | ins_333 `SSSff` | ins_333 `SSSff` | ins_333 `SSSff` |
| anm.anm334 | anm |  |  |  |  | ins_334 `S` | ins_334 `S` | ins_334 `S` | ins_334 `S` | ins_334 `S` | ins_334 `S` |
| anm.anm339 | anm |  |  |  |  |  |  |  | ins_339 `SSS` | ins_339 `SSS` | ins_339 `SSS` |
| anm.blend_mode | anm |  |  |  |  |  |  |  | ins_337 `SS` | ins_337 `SS` | ins_337 `SS` |
| anm.color | anm |  |  |  |  | ins_325 `SSSS` | ins_325 `SSSS` | ins_325 `SSSS` | ins_325 `SSSS` | ins_325 `SSSS` | ins_325 `SSSS` |
| anm.color_time | anm |  |  |  |  | ins_326 `SSSSSS` | ins_326 `SSSSSS` | ins_326 `SSSSSS` | ins_326 `SSSSSS` | ins_326 `SSSSSS` | ins_326 `SSSSSS` |
| anm.familiar | anm | ins_174 `S` |  |  |  |  |  |  |  |  |  |
| anm.follow_main | anm | ins_182 `S` |  |  |  |  |  |  |  |  |  |
| anm.layer | anm |  |  |  |  |  | ins_336 `SS` | ins_336 `SS` | ins_336 `SS` | ins_336 `SS` | ins_336 `SS` |
| anm.move | anm |  |  |  | ins_279 `Sff` | ins_320 `Sff` | ins_320 `Sff` | ins_320 `Sff` | ins_320 `Sff` | ins_320 `Sff` | ins_320 `Sff` |
| anm.on_et | anm |  |  | ins_274 `SS` | ins_274 `SS` |  |  |  |  |  |  |
| anm.on_photo | anm |  |  |  | ins_282 `ff` |  |  |  |  |  |  |
| anm.play | anm |  |  | ins_263 `SS` | ins_263 `SS` | ins_307 `SS` | ins_307 `SS` | ins_307 `SS` | ins_307 `SS` | ins_307 `SS` | ins_307 `SS` |
| anm.play_abs | anm |  |  | ins_264 `SS` | ins_264 `SS` | ins_308 `SS` | ins_308 `SS` | ins_308 `SS` | ins_308 `SS` | ins_308 `SS` | ins_308 `SS` |
| anm.play_attack | anm | ins_62 `` |  |  |  |  |  |  |  |  |  |
| anm.play_high | anm |  |  | ins_272 `SS` | ins_272 `SS` | ins_314 `SS` | ins_314 `SS` | ins_314 `SS` | ins_314 `SS` | ins_314 `SS` | ins_314 `SS` |
| anm.play_pos | anm |  |  |  |  |  | ins_337 `SSfff` | ins_337 `SSfff` | ins_338 `SSfff` | ins_338 `SSfff` | ins_338 `SSfff` |
| anm.play_rotate | anm |  |  | ins_273 `SSf` | ins_273 `SSf` | ins_315 `SSf` | ins_315 `SSf` | ins_315 `SSf` | ins_315 `SSf` | ins_315 `SSf` | ins_315 `SSf` |
| anm.reset | anm |  |  | ins_276 `` | ins_276 `` | ins_318 `` | ins_318 `` | ins_318 `` | ins_318 `` | ins_318 `` | ins_318 `` |
| anm.rot_set | anm | ins_145 `S` |  |  |  |  |  |  |  |  |  |
| anm.rotate | anm | ins_165 `f` |  |  | ins_277 `Sf` | ins_319 `Sf` | ins_319 `Sf` | ins_319 `Sf` | ins_319 `Sf` | ins_319 `Sf` | ins_319 `Sf` |
| anm.scale | anm |  |  |  | ins_278 `Sff` | ins_329 `Sff` | ins_329 `Sff` | ins_329 `Sff` | ins_329 `Sff` | ins_329 `Sff` | ins_329 `Sff` |
| anm.scale2 | anm |  |  |  |  | ins_335 `Sff` | ins_335 `Sff` | ins_335 `Sff` | ins_335 `Sff` | ins_335 `Sff` | ins_335 `Sff` |
| anm.scale_time | anm |  |  |  |  | ins_330 `SSSff` | ins_330 `SSSff` | ins_330 `SSSff` | ins_330 `SSSff` | ins_330 `SSSff` | ins_330 `SSSff` |
| anm.select | anm |  |  | ins_258 `S` | ins_258 `S` | ins_302 `S` | ins_302 `S` | ins_302 `S` | ins_302 `S` | ins_302 `S` | ins_302 `S` |
| anm.selected_play | anm |  |  | ins_269 `S` | ins_269 `S` | ins_313 `S` | ins_313 `S` | ins_313 `S` | ins_313 `S` | ins_313 `S` | ins_313 `S` |
| anm.set | anm | ins_54 `S` |  |  |  |  |  |  |  |  |  |
| anm.set_boss | anm | ins_58 `S` |  |  |  |  |  |  |  |  |  |
| anm.set_boss_ex | anm | ins_59 `S` |  |  |  |  |  |  |  |  |  |
| anm.set_boss_ex2 | anm | ins_60 `SSSSSS` |  |  |  |  |  |  |  |  |  |
| anm.set_boss_slot | anm | ins_61 `SS` |  |  |  |  |  |  |  |  |  |
| anm.set_ex | anm | ins_55 `S` |  |  |  |  |  |  |  |  |  |
| anm.set_ex2 | anm | ins_56 `SSSSSS` |  |  |  |  |  |  |  |  |  |
| anm.set_main | anm |  |  | ins_262 `SS` | ins_262 `SS` | ins_306 `SS` | ins_306 `SS` | ins_306 `SS` | ins_306 `SS` | ins_306 `SS` | ins_306 `SS` |
| anm.set_slot | anm | ins_57 `SS` |  |  |  |  |  |  |  |  |  |
| anm.set_sprite | anm |  |  | ins_259 `SS` | ins_259 `SS` | ins_303 `SS` | ins_303 `SS` | ins_303 `SS` | ins_303 `SS` | ins_303 `SS` | ins_303 `SS` |
| anm.switch | anm |  |  | ins_275 `SS` | ins_275 `SS` | ins_317 `SS` | ins_317 `SS` | ins_317 `SS` | ins_317 `SS` | ins_317 `SS` | ins_317 `SS` |
| boss.life_set | boss | ins_131 `S` |  | ins_331 `S` | ins_411 `S` | ins_511 `S` | ins_511 `S` | ins_511 `S` | ins_511 `S` | ins_511 `S` | ins_511 `S` |
| boss.set_boss | boss | ins_127 `S` |  | ins_332 `S` | ins_412 `S` | ins_512 `S` | ins_512 `S` | ins_512 `S` | ins_512 `S` | ins_512 `S` | ins_512 `S` |
| boss.set_chapter | boss |  |  | ins_344 `S` | ins_424 `S` | ins_524 `S` | ins_524 `S` | ins_524 `S` | ins_524 `S` | ins_524 `S` | ins_524 `S` |
| boss.set_interrupt | boss | ins_130 `S` |  | ins_334 `SSSm` | ins_414 `SSSm` | ins_514 `SSSm` | ins_514 `SSSm` | ins_514 `SSSm` | ins_514 `SSSm` | ins_514 `SSSm` | ins_514 `SSSm` |
| boss.set_timeout | boss |  |  | ins_341 `Sm` | ins_421 `Sm` | ins_521 `Sm` | ins_521 `Sm` | ins_521 `Sm` | ins_521 `Sm` | ins_521 `Sm` | ins_521 `Sm` |
| boss.spell | boss | ins_122 `SSS` |  | ins_357 `SSSx` | ins_437 `SSSx` | ins_537 `SSSm` | ins_537 `SSSm` | ins_537 `SSSm` | ins_537 `SSSm` | ins_537 `SSSm` | ins_537 `SSSm` |
| boss.spell2 | boss |  |  | ins_358 `SSSx` | ins_438 `SSSx` | ins_538 `SSSm` | ins_538 `SSSm` | ins_538 `SSSm` | ins_538 `SSSm` | ins_538 `SSSm` | ins_538 `SSSm` |
| boss.spell3 | boss |  |  | ins_359 `SSSx` | ins_439 `SSSx` | ins_539 `SSSm` | ins_539 `SSSm` | ins_539 `SSSm` | ins_539 `SSSm` | ins_539 `SSSm` | ins_539 `SSSm` |
| boss.spell_end | boss | ins_123 `` |  | ins_343 `` | ins_423 `` | ins_523 `` | ins_523 `` | ins_523 `` | ins_523 `` | ins_523 `` | ins_523 `` |
| boss.timer_reset | boss |  |  | ins_333 `` | ins_413 `` | ins_513 `` | ins_513 `` | ins_513 `` | ins_513 `` | ins_513 `` | ins_513 `` |
| bullet.aim | bullet |  |  | ins_407 `SS` | ins_507 `SS` | ins_607 `SS` | ins_607 `SS` | ins_607 `SS` | ins_607 `SS` | ins_607 `SS` | ins_607 `SS` |
| bullet.angle | bullet |  |  | ins_404 `Sff` | ins_504 `Sff` | ins_604 `Sff` | ins_604 `Sff` | ins_604 `Sff` | ins_604 `Sff` | ins_604 `Sff` | ins_604 `Sff` |
| bullet.angle_to_player | bullet |  |  |  | ins_520 `fff` | ins_623 `fff` | ins_623 `fff` | ins_623 `fff` | ins_623 `fff` | ins_623 `fff` | ins_623 `fff` |
| bullet.call_std | bullet |  |  |  |  | ins_630 `S` | ins_630 `S` | ins_630 `S` | ins_630 `S` | ins_630 `S` | ins_630 `S` |
| bullet.cancel_radius | bullet | ins_112 `` |  | ins_420 `f` | ins_512 `f` | ins_615 `f` | ins_615 `f` | ins_615 `f` | ins_615 `f` | ins_615 `f` | ins_615 `f` |
| bullet.clear_all | bullet |  |  | ins_410 `` | ins_510 `` | ins_613 `` | ins_613 `` | ins_613 `` | ins_613 `` | ins_613 `` | ins_613 `` |
| bullet.clear_radius | bullet | ins_162 `` |  | ins_421 `f` | ins_513 `f` | ins_616 `f` | ins_616 `f` | ins_616 `f` | ins_616 `f` | ins_616 `f` | ins_616 `f` |
| bullet.copy | bullet |  |  | ins_411 `SS` | ins_511 `SS` | ins_614 `SS` | ins_614 `SS` | ins_614 `SS` | ins_614 `SS` | ins_614 `SS` | ins_614 `SS` |
| bullet.count | bullet |  |  | ins_406 `SSS` | ins_506 `SSS` | ins_606 `SSS` | ins_606 `SSS` | ins_606 `SSS` | ins_606 `SSS` | ins_606 `SSS` | ins_606 `SSS` |
| bullet.count_by_difficulty | bullet |  |  | ins_436 `SSSSSSSSS` | ins_522 `SSSSSSSSS` | ins_625 `SSSSSSSSS` | ins_625 `SSSSSSSSS` | ins_625 `SSSSSSSSS` | ins_625 `SSSSSSSSS` | ins_625 `SSSSSSSSS` | ins_625 `SSSSSSSSS` |
| bullet.et_cancel2 | bullet |  |  |  |  | ins_635 `f` | ins_635 `f` | ins_635 `f` | ins_635 `f` | ins_635 `f` | ins_635 `f` |
| bullet.et_clear2 | bullet |  |  |  |  | ins_636 `f` | ins_636 `f` | ins_636 `f` | ins_636 `f` | ins_636 `f` | ins_636 `f` |
| bullet.et_count_r2 | bullet |  |  | ins_427 `SSSSS` | ins_519 `SSSSS` | ins_622 `SSSSS` | ins_622 `SSSSS` | ins_622 `SSSSS` | ins_622 `SSSSS` | ins_622 `SSSSS` | ins_622 `SSSSS` |
| bullet.et_count_r3 | bullet |  |  | ins_425 `SSSSSSS` | ins_517 `SSSSSSS` | ins_620 `SSSSSSS` | ins_620 `SSSSSSS` | ins_620 `SSSSSSS` | ins_620 `SSSSSSS` | ins_620 `SSSSSSS` | ins_620 `SSSSSSS` |
| bullet.et_count_r5 | bullet |  |  | ins_426 `SSSSSSSSSSS` |  | ins_621 `SSSSSSSSSSS` | ins_621 `SSSSSSSSSSS` | ins_621 `SSSSSSSSSSS` | ins_621 `SSSSSSSSSSS` | ins_621 `SSSSSSSSSSS` | ins_621 `SSSSSSSSSSS` |
| bullet.et_dist | bullet |  |  | ins_438 `Sf` | ins_524 `Sf` | ins_627 `Sf` | ins_627 `Sf` | ins_627 `Sf` | ins_627 `Sf` | ins_627 `Sf` | ins_627 `Sf` |
| bullet.et_ex_sub | bullet |  |  |  |  | ins_640 `SSm` | ins_640 `SSm` | ins_640 `SSm` | ins_640 `SSm` | ins_640 `SSm` | ins_640 `SSm` |
| bullet.et_ex_subtract | bullet |  |  |  |  |  | ins_641 `S` | ins_641 `S` | ins_641 `S` | ins_641 `S` | ins_641 `S` |
| bullet.et_new | bullet |  |  | ins_400 `S` | ins_500 `S` | ins_600 `S` | ins_600 `S` | ins_600 `S` | ins_600 `S` | ins_600 `S` | ins_600 `S` |
| bullet.et_offset_abs | bullet |  |  | ins_439 `Sff` | ins_525 `Sff` | ins_628 `Sff` | ins_628 `Sff` | ins_628 `Sff` | ins_628 `Sff` | ins_628 `Sff` | ins_628 `Sff` |
| bullet.et_offset_rad | bullet |  |  | ins_437 `Sff` | ins_523 `Sff` | ins_626 `Sff` | ins_626 `Sff` | ins_626 `Sff` | ins_626 `Sff` | ins_626 `Sff` | ins_626 `Sff` |
| bullet.et_speed_r2 | bullet |  |  | ins_424 `Sffff` | ins_516 `Sffff` | ins_619 `Sffff` | ins_619 `Sffff` | ins_619 `Sffff` | ins_619 `Sffff` | ins_619 `Sffff` | ins_619 `Sffff` |
| bullet.et_speed_r3 | bullet |  |  | ins_422 `Sffffff` | ins_514 `Sffffff` | ins_617 `Sffffff` | ins_617 `Sffffff` | ins_617 `Sffffff` | ins_617 `Sffffff` | ins_617 `Sffffff` | ins_617 `Sffffff` |
| bullet.et_speed_r5 | bullet |  |  | ins_423 `Sffffffffff` | ins_515 `Sffffffffff` | ins_618 `Sffffffffff` | ins_618 `Sffffffffff` | ins_618 `Sffffffffff` | ins_618 `Sffffffffff` | ins_618 `Sffffffffff` | ins_618 `Sffffffffff` |
| bullet.fire | bullet | ins_108 `` |  | ins_401 `S` | ins_501 `S` | ins_601 `S` | ins_601 `S` | ins_601 `S` | ins_601 `S` | ins_601 `S` | ins_601 `S` |
| bullet.flag_ext_dmg | bullet |  |  |  |  | ins_633 `S` | ins_633 `S` | ins_633 `S` | ins_633 `S` | ins_633 `S` | ins_633 `S` |
| bullet.fog | bullet |  |  |  |  | ins_629 `fS` | ins_629 `fS` | ins_629 `fS` | ins_629 `fS` | ins_629 `fS` | ins_629 `fS` |
| bullet.func_call | bullet |  |  |  |  | ins_637 `S` | ins_637 `S` | ins_637 `S` | ins_637 `S` | ins_637 `S` | ins_637 `S` |
| bullet.func_set | bullet |  |  |  |  | ins_632 `S` | ins_632 `S` | ins_632 `S` | ins_632 `S` | ins_632 `S` | ins_632 `S` |
| bullet.func_set2 | bullet |  |  |  |  | ins_639 `S` | ins_639 `S` | ins_639 `S` | ins_639 `S` | ins_639 `S` | ins_639 `S` |
| bullet.hitbox_rect | bullet |  |  |  | ins_612 `ff` |  |  |  |  |  |  |
| bullet.life_hide | bullet |  |  |  |  | ins_631 `S` | ins_631 `S` | ins_631 `S` | ins_631 `S` | ins_631 `S` | ins_631 `S` |
| bullet.offset | bullet | ins_110 `ff` |  | ins_403 `Sff` | ins_503 `Sff` | ins_603 `Sff` | ins_603 `Sff` | ins_603 `Sff` | ins_603 `Sff` | ins_603 `Sff` | ins_603 `Sff` |
| bullet.score_add | bullet |  |  |  |  | ins_638 `S` | ins_638 `S` | ins_638 `S` | ins_638 `S` | ins_638 `S` | ins_638 `S` |
| bullet.set_hitbox_func | bullet |  |  |  |  | ins_634 `S` | ins_634 `S` | ins_634 `S` | ins_634 `S` | ins_634 `S` | ins_634 `S` |
| bullet.sound | bullet | ins_113 `SS` |  | ins_408 `SSS` | ins_508 `SSS` | ins_608 `SSS` | ins_608 `SSS` | ins_608 `SSS` | ins_608 `SSS` | ins_608 `SSS` | ins_608 `SSS` |
| bullet.speed | bullet |  |  | ins_405 `Sff` | ins_505 `Sff` | ins_605 `Sff` | ins_605 `Sff` | ins_605 `Sff` | ins_605 `Sff` | ins_605 `Sff` | ins_605 `Sff` |
| bullet.speed_by_difficulty | bullet |  |  | ins_435 `Sffffffff` | ins_521 `Sffffffff` | ins_624 `Sffffffff` | ins_624 `Sffffffff` | ins_624 `Sffffffff` | ins_624 `Sffffffff` | ins_624 `Sffffffff` | ins_624 `Sffffffff` |
| bullet.sprite | bullet |  |  | ins_402 `SSS` | ins_502 `SSS` | ins_602 `SSS` | ins_602 `SSS` | ins_602 `SSS` | ins_602 `SSS` | ins_602 `SSS` | ins_602 `SSS` |
| bullet.transform | bullet | ins_111 `SSSSSff` |  | ins_409 `SSSSSSff` | ins_509 `SSSSSSff` | ins_611 `SSSSSff` | ins_611 `SSSSSff` | ins_611 `SSSSSff` | ins_611 `SSSSSff` | ins_611 `SSSSSff` | ins_611 `SSSSSff` |
| bullet.transform2 | bullet |  |  |  |  | ins_612 `SSSSSSSffff` | ins_612 `SSSSSSSffff` | ins_612 `SSSSSSSffff` | ins_612 `SSSSSSSffff` | ins_612 `SSSSSSSffff` | ins_612 `SSSSSSSffff` |
| bullet.transform_set | bullet |  |  |  |  | ins_609 `SSSSSSff` | ins_609 `SSSSSSff` | ins_609 `SSSSSSff` | ins_609 `SSSSSSff` | ins_609 `SSSSSSff` | ins_609 `SSSSSSff` |
| bullet.transform_set2 | bullet |  |  |  |  | ins_610 `SSSSSSSSffff` | ins_610 `SSSSSSSSffff` | ins_610 `SSSSSSSSffff` | ins_610 `SSSSSSSSffff` | ins_610 `SSSSSSSSffff` | ins_610 `SSSSSSSSffff` |
| bullet.unknown613 | bullet |  |  |  | ins_613 `SS` |  |  |  |  |  |  |
| bullet.unknown614 | bullet |  |  |  | ins_614 `SS` |  |  |  |  |  |  |
| bullet.unknown615 | bullet |  |  |  | ins_615 `SS` |  |  |  |  |  |  |
| enemy.bomb_shield | enemy |  |  | ins_366 `SS` |  |  |  |  |  |  |  |
| enemy.byakuren_butterfly | enemy |  |  |  | ins_281 `SS` |  |  |  |  |  |  |
| enemy.create | enemy | ins_94 `SfffSSS` |  | ins_256 `mffSSS` | ins_256 `mffSSS` | ins_300 `mffSSS` | ins_300 `mffSSS` | ins_300 `mffSSS` | ins_300 `mffSSS` | ins_300 `mffSSS` | ins_300 `mffSSS` |
| enemy.create_abs | enemy | ins_93 `SfffSSS` |  | ins_257 `mffSSS` | ins_257 `mffSSS` | ins_301 `mffSSS` | ins_301 `mffSSS` | ins_301 `mffSSS` | ins_301 `mffSSS` | ins_301 `mffSSS` | ins_301 `mffSSS` |
| enemy.create_abs_func | enemy |  |  | ins_266 `mffSSS` | ins_266 `mffSSS` | ins_310 `mffSSS` | ins_310 `mffSSS` | ins_310 `mffSSS` | ins_310 `mffSSS` | ins_310 `mffSSS` | ins_310 `mffSSS` |
| enemy.create_abs_mirror | enemy |  |  | ins_261 `mffSSS` | ins_261 `mffSSS` | ins_305 `mffSSS` | ins_305 `mffSSS` | ins_305 `mffSSS` | ins_305 `mffSSS` | ins_305 `mffSSS` | ins_305 `mffSSS` |
| enemy.create_abs_mirror_func | enemy |  |  | ins_268 `mffSSS` | ins_268 `mffSSS` | ins_312 `mffSSS` | ins_312 `mffSSS` | ins_312 `mffSSS` | ins_312 `mffSSS` | ins_312 `mffSSS` | ins_312 `mffSSS` |
| enemy.create_func | enemy |  |  | ins_265 `mffSSS` | ins_265 `mffSSS` | ins_309 `mffSSS` | ins_309 `mffSSS` | ins_309 `mffSSS` | ins_309 `mffSSS` | ins_309 `mffSSS` | ins_309 `mffSSS` |
| enemy.create_mirror | enemy |  |  | ins_260 `mffSSS` | ins_260 `mffSSS` | ins_304 `mffSSS` | ins_304 `mffSSS` | ins_304 `mffSSS` | ins_304 `mffSSS` | ins_304 `mffSSS` | ins_304 `mffSSS` |
| enemy.create_mirror_func | enemy |  |  | ins_267 `mffSSS` | ins_267 `mffSSS` | ins_311 `mffSSS` | ins_311 `mffSSS` | ins_311 `mffSSS` | ins_311 `mffSSS` | ins_311 `mffSSS` | ins_311 `mffSSS` |
| enemy.death_anm | enemy |  |  |  |  | ins_323 `SS` | ins_323 `SS` | ins_323 `SS` | ins_323 `SS` | ins_323 `SS` | ins_323 `SS` |
| enemy.death_wait | enemy |  |  | ins_340 `` |  |  |  |  |  |  |  |
| enemy.dialog_read | enemy |  |  | ins_338 `S` |  |  |  |  |  |  |  |
| enemy.dialog_wait | enemy |  |  | ins_339 `` |  |  |  |  |  |  |  |
| enemy.diff_f | enemy |  |  | ins_356 `fffff` |  |  |  |  |  |  |  |
| enemy.diff_i | enemy |  |  | ins_355 `SSSSS` |  |  |  |  |  |  |  |
| enemy.diff_wait | enemy |  |  | ins_368 `SSSS` |  |  |  |  |  |  |  |
| enemy.drop_area | enemy |  |  | ins_328 `ff` |  |  |  |  |  |  |  |
| enemy.drop_clear | enemy |  |  | ins_326 `` |  |  |  |  |  |  |  |
| enemy.drop_extra | enemy |  |  | ins_327 `SS` |  |  |  |  |  |  |  |
| enemy.drop_items | enemy |  |  | ins_329 `` |  |  |  |  |  |  |  |
| enemy.drop_main | enemy |  |  | ins_330 `S` |  |  |  |  |  |  |  |
| enemy.enm322 | enemy |  |  |  |  | ins_322 `SS` | ins_322 `SS` | ins_322 `SS` | ins_322 `SS` | ins_322 `SS` | ins_322 `SS` |
| enemy.enm324 | enemy |  |  |  |  | ins_324 `S` | ins_324 `S` | ins_324 `S` | ins_324 `S` |  |  |
| enemy.enm_alive | enemy |  |  |  | ins_455 `SS` | ins_555 `SS` | ins_555 `SS` | ins_555 `SS` | ins_555 `SS` | ins_555 `SS` | ins_555 `SS` |
| enemy.enm_call | enemy |  |  |  |  | ins_800 `Sm` | ins_800 `Sm` | ins_800 `Sm` | ins_800 `Sm` | ins_800 `Sm` | ins_800 `Sm` |
| enemy.enm_create270 | enemy |  |  | ins_270 `mffSSSS` | ins_270 `mffSSSS` |  |  |  |  |  |  |
| enemy.enm_create271 | enemy |  |  | ins_271 `mffSSSS` | ins_271 `mffSSSS` |  |  |  |  |  |  |
| enemy.enm_delete | enemy |  |  |  |  |  |  |  | ins_340 `S` | ins_340 `S` | ins_340 `S` |
| enemy.enm_kill_all | enemy | ins_95 `` |  | ins_345 `` | ins_425 `` | ins_525 `` | ins_525 `` | ins_525 `` | ins_525 `` | ins_525 `` | ins_525 `` |
| enemy.enm_limit | enemy |  |  |  |  | ins_559 `S` | ins_559 `S` | ins_559 `S` | ins_559 `S` | ins_559 `S` | ins_559 `S` |
| enemy.enm_maple_enemy | enemy |  |  |  | ins_280 `mSSSSS` | ins_321 `mffSSS` | ins_321 `mffSSS` | ins_321 `mffSSS` | ins_321 `mffSSS` | ins_321 `mffSSS` | ins_321 `mffSSS` |
| enemy.enm_pos | enemy |  |  |  |  | ins_801 `ffS` | ins_801 `ffS` | ins_801 `ffS` | ins_801 `ffS` | ins_801 `ffS` | ins_801 `ffS` |
| enemy.enm_pos2 | enemy |  |  |  |  |  |  |  |  | ins_324 `S` | ins_324 `S` |
| enemy.enm_spawn_prevent | enemy | ins_175 `S` |  |  |  |  |  |  |  |  |  |
| enemy.et_protect_range | enemy |  |  | ins_346 `f` |  |  |  |  |  |  |  |
| enemy.flag_clear | enemy |  |  | ins_323 `S` |  |  |  |  |  |  |  |
| enemy.flag_set | enemy |  |  | ins_322 `S` |  |  |  |  |  |  |  |
| enemy.game_speed | enemy |  |  | ins_367 `f` |  |  |  |  |  |  |  |
| enemy.laser_cancel | enemy |  |  | ins_365 `` |  |  |  |  |  |  |  |
| enemy.life_marker | enemy |  |  | ins_347 `SfS` |  |  |  |  |  |  |  |
| enemy.play_sound | enemy |  |  | ins_336 `S` |  |  |  |  |  |  |  |
| enemy.rank_f2 | enemy |  |  | ins_351 `fff` |  |  |  |  |  |  |  |
| enemy.rank_f3 | enemy |  |  | ins_349 `ffff` |  |  |  |  |  |  |  |
| enemy.rank_f5 | enemy |  |  | ins_350 `ffffff` |  |  |  |  |  |  |  |
| enemy.rank_i2 | enemy |  |  | ins_354 `SSS` |  |  |  |  |  |  |  |
| enemy.rank_i3 | enemy |  |  | ins_352 `SSSS` |  |  |  |  |  |  |  |
| enemy.rank_i5 | enemy |  |  | ins_353 `SSSSSS` |  |  |  |  |  |  |  |
| enemy.set_hitbox | enemy |  |  | ins_321 `ff` |  |  |  |  |  |  |  |
| enemy.set_hurtbox | enemy |  |  | ins_320 `ff` |  |  |  |  |  |  |  |
| enemy.set_invuln | enemy |  |  | ins_335 `S` |  |  |  |  |  |  |  |
| enemy.set_screen_shake | enemy |  |  | ins_337 `SSS` |  |  |  |  |  |  |  |
| enemy.spell_ex | enemy |  |  | ins_342 `SSSx` |  |  |  |  |  |  |  |
| enemy.spell_timeout | enemy |  |  | ins_362 `` |  |  |  |  |  |  |  |
| enemy.spell_unused | enemy |  |  | ins_348 `SSSx` |  |  |  |  |  |  |  |
| enemy.stars | enemy |  |  | ins_360 `S` |  |  |  |  |  |  |  |
| enemy.unknown283 | enemy |  |  |  | ins_283 `SSfS` |  |  |  |  |  |  |
| enemy.unknown361 | enemy |  |  | ins_361 `S` |  |  |  |  |  |  |  |
| enemy.unknown363 | enemy |  |  | ins_363 `` |  |  |  |  |  |  |  |
| enemy.unknown364 | enemy |  |  | ins_364 `S` |  |  |  |  |  |  |  |
| enemy.unknown369 | enemy |  |  | ins_369 `S` |  |  |  |  |  |  |  |
| enemy.unknown370 | enemy |  |  | ins_370 `S` |  |  |  |  |  |  |  |
| flow.addf | flow |  |  | ins_51 `` | ins_51 `` | ins_51 `` | ins_51 `` | ins_51 `` | ins_51 `` | ins_51 `` | ins_51 `` |
| flow.addi | flow |  |  | ins_50 `` | ins_50 `` | ins_50 `` | ins_50 `` | ins_50 `` | ins_50 `` | ins_50 `` | ins_50 `` |
| flow.and | flow |  |  | ins_74 `` | ins_74 `` | ins_74 `` | ins_74 `` | ins_74 `` | ins_74 `` | ins_74 `` | ins_74 `` |
| flow.bit_and | flow |  |  | ins_77 `` | ins_77 `` | ins_77 `` | ins_77 `` | ins_77 `` | ins_77 `` | ins_77 `` | ins_77 `` |
| flow.bit_or | flow |  |  | ins_76 `` | ins_76 `` | ins_76 `` | ins_76 `` | ins_76 `` | ins_76 `` | ins_76 `` | ins_76 `` |
| flow.boss_call | flow | ins_88 `SS` |  |  |  |  |  |  |  |  |  |
| flow.call | flow | ins_52 `S` |  | ins_11 `m*D` | ins_11 `m*D` | ins_11 `m` | ins_11 `m` | ins_11 `m` | ins_11 `m` | ins_11 `m` | ins_11 `m` |
| flow.call_async | flow |  |  | ins_15 `m*D` | ins_15 `m*D` | ins_15 `m` | ins_15 `m` | ins_15 `m` | ins_15 `m` | ins_15 `m` | ins_15 `m` |
| flow.call_async_id | flow |  |  | ins_16 `mS*D` | ins_16 `mS*D` | ins_16 `mS` | ins_16 `mS` | ins_16 `mS` | ins_16 `mS` | ins_16 `mS` | ins_16 `mS` |
| flow.circle_pos | flow |  |  | ins_81 `ffff` | ins_81 `ffff` | ins_81 `ffff` | ins_81 `ffff` | ins_81 `ffff` | ins_81 `ffff` | ins_81 `ffff` | ins_81 `ffff` |
| flow.debug22 | flow |  |  | ins_22 `` | ins_22 `` | ins_22 `Sm` | ins_22 `Sm` | ins_22 `Sm` | ins_22 `Sm` | ins_22 `Sm` | ins_22 `Sm` |
| flow.dec | flow | ins_31 `S` |  |  |  |  |  |  |  |  |  |
| flow.deci | flow |  |  | ins_78 `S` | ins_78 `S` | ins_78 `S` | ins_78 `S` | ins_78 `S` | ins_78 `S` | ins_78 `S` | ins_78 `S` |
| flow.delete | flow | ins_1 `S` |  | ins_1 `` | ins_1 `` | ins_1 `` | ins_1 `` | ins_1 `` | ins_1 `` | ins_1 `` | ins_1 `` |
| flow.divf | flow |  |  | ins_57 `` | ins_57 `` | ins_57 `` | ins_57 `` | ins_57 `` | ins_57 `` | ins_57 `` | ins_57 `` |
| flow.divi | flow |  |  | ins_56 `` | ins_56 `` | ins_56 `` | ins_56 `` | ins_56 `` | ins_56 `` | ins_56 `` | ins_56 `` |
| flow.eqf | flow |  |  | ins_60 `` | ins_60 `` | ins_60 `` | ins_60 `` | ins_60 `` | ins_60 `` | ins_60 `` | ins_60 `` |
| flow.eqi | flow |  |  | ins_59 `` | ins_59 `` | ins_59 `` | ins_59 `` | ins_59 `` | ins_59 `` | ins_59 `` | ins_59 `` |
| flow.et_fan | flow | ins_97 `SSSSffffS` |  |  |  |  |  |  |  |  |  |
| flow.et_fan_aimed | flow | ins_96 `SSSSffffS` |  |  |  |  |  |  |  |  |  |
| flow.et_protect_range | flow | ins_82 `f` |  |  |  |  |  |  |  |  |  |
| flow.et_ring | flow | ins_99 `SSSSffffS` |  |  |  |  |  |  |  |  |  |
| flow.et_ring_aimed | flow | ins_98 `SSSSffffS` |  |  |  |  |  |  |  |  |  |
| flow.fadd | flow | ins_15 `ff` |  |  |  |  |  |  |  |  |  |
| flow.familiar_create | flow | ins_91 `SffSSS` |  |  |  |  |  |  |  |  |  |
| flow.familiar_create_a | flow | ins_90 `SffSSS` |  |  |  |  |  |  |  |  |  |
| flow.familiar_create_f | flow | ins_92 `SffSSS` |  |  |  |  |  |  |  |  |  |
| flow.fdiv | flow | ins_18 `ff` |  |  |  |  |  |  |  |  |  |
| flow.flag_clear | flow | ins_81 `S` |  |  |  |  |  |  |  |  |  |
| flow.flag_set | flow | ins_80 `S` |  |  |  |  |  |  |  |  |  |
| flow.float_time | flow | ins_36 `fSSSffff` |  | ins_91 `` | ins_91 `` | ins_91 `SfSSff` | ins_91 `SfSSff` | ins_91 `SfSSff` | ins_91 `SfSSff` | ins_91 `SfSSff` | ins_91 `SfSSff` |
| flow.fmod | flow | ins_19 `ff` |  |  |  |  |  |  |  |  |  |
| flow.fmul | flow | ins_17 `ff` |  |  |  |  |  |  |  |  |  |
| flow.fset | flow | ins_7 `ff` |  |  |  |  |  |  |  |  |  |
| flow.fset_add | flow | ins_25 `fff` |  |  |  |  |  |  |  |  |  |
| flow.fset_bossvar | flow | ins_87 `ffS` |  |  |  |  |  |  |  |  |  |
| flow.fset_cos | flow | ins_33 `ff` |  |  |  |  |  |  |  |  |  |
| flow.fset_div | flow | ins_28 `fff` |  |  |  |  |  |  |  |  |  |
| flow.fset_mod | flow | ins_29 `fff` |  |  |  |  |  |  |  |  |  |
| flow.fset_mul | flow | ins_27 `fff` |  |  |  |  |  |  |  |  |  |
| flow.fset_rand_sign | flow | ins_9 `ff` |  |  |  |  |  |  |  |  |  |
| flow.fset_sin | flow | ins_32 `ff` |  |  |  |  |  |  |  |  |  |
| flow.fset_sub | flow | ins_26 `fff` |  |  |  |  |  |  |  |  |  |
| flow.fsub | flow | ins_16 `ff` |  |  |  |  |  |  |  |  |  |
| flow.geqf | flow |  |  | ins_70 `` | ins_70 `` | ins_70 `` | ins_70 `` | ins_70 `` | ins_70 `` | ins_70 `` | ins_70 `` |
| flow.geqi | flow |  |  | ins_69 `` | ins_69 `` | ins_69 `` | ins_69 `` | ins_69 `` | ins_69 `` | ins_69 `` | ins_69 `` |
| flow.get_angle | flow |  |  | ins_87 `fffff` | ins_87 `fffff` | ins_87 `fffff` | ins_87 `fffff` | ins_87 `fffff` | ins_87 `fffff` | ins_87 `fffff` | ins_87 `fffff` |
| flow.greaterf | flow |  |  | ins_68 `` | ins_68 `` | ins_68 `` | ins_68 `` | ins_68 `` | ins_68 `` | ins_68 `` | ins_68 `` |
| flow.greateri | flow |  |  | ins_67 `` | ins_67 `` | ins_67 `` | ins_67 `` | ins_67 `` | ins_67 `` | ins_67 `` | ins_67 `` |
| flow.hitbox_set | flow | ins_77 `ff` |  |  |  |  |  |  |  |  |  |
| flow.hurtbox_set | flow | ins_78 `ff` |  |  |  |  |  |  |  |  |  |
| flow.iadd | flow | ins_10 `SS` |  |  |  |  |  |  |  |  |  |
| flow.idiv | flow | ins_13 `SS` |  |  |  |  |  |  |  |  |  |
| flow.imod | flow | ins_14 `SS` |  |  |  |  |  |  |  |  |  |
| flow.imul | flow | ins_12 `SS` |  |  |  |  |  |  |  |  |  |
| flow.inc | flow | ins_30 `S` |  |  |  |  |  |  |  |  |  |
| flow.ins_18 | flow |  |  |  |  | ins_18 `S` | ins_18 `S` | ins_18 `S` | ins_18 `S` | ins_18 `S` | ins_18 `S` |
| flow.ins_19 | flow |  |  |  |  | ins_19 `S` | ins_19 `S` | ins_19 `S` | ins_19 `S` | ins_19 `S` | ins_19 `S` |
| flow.ins_2 | flow |  |  |  |  | ins_2 `` | ins_2 `` | ins_2 `` | ins_2 `` | ins_2 `` | ins_2 `` |
| flow.ins_20 | flow |  |  |  |  | ins_20 `SS` | ins_20 `SS` | ins_20 `SS` | ins_20 `SS` | ins_20 `SS` | ins_20 `SS` |
| flow.ins_25 | flow |  |  |  |  | ins_25 `` | ins_25 `` | ins_25 `` | ins_25 `` | ins_25 `` | ins_25 `` |
| flow.ins_26 | flow |  |  |  |  | ins_26 `` | ins_26 `` | ins_26 `` | ins_26 `` | ins_26 `` | ins_26 `` |
| flow.ins_28 | flow |  |  |  |  | ins_28 `` | ins_28 `` | ins_28 `` | ins_28 `` | ins_28 `` | ins_28 `` |
| flow.ins_29 | flow |  |  |  |  | ins_29 `` | ins_29 `` | ins_29 `` | ins_29 `` | ins_29 `` | ins_29 `` |
| flow.ins_3 | flow |  |  |  |  | ins_3 `` | ins_3 `` | ins_3 `` | ins_3 `` | ins_3 `` | ins_3 `` |
| flow.ins_32 | flow |  |  |  |  | ins_32 `` | ins_32 `` | ins_32 `` | ins_32 `` | ins_32 `` | ins_32 `` |
| flow.ins_33 | flow |  |  |  |  | ins_33 `` | ins_33 `` | ins_33 `` | ins_33 `` | ins_33 `` | ins_33 `` |
| flow.ins_34 | flow |  |  |  |  | ins_34 `` | ins_34 `` | ins_34 `` | ins_34 `` | ins_34 `` | ins_34 `` |
| flow.ins_35 | flow | ins_35 `` |  |  |  | ins_35 `` | ins_35 `` | ins_35 `` | ins_35 `` | ins_35 `` | ins_35 `` |
| flow.ins_36 | flow |  |  |  |  | ins_36 `` | ins_36 `` | ins_36 `` | ins_36 `` | ins_36 `` | ins_36 `` |
| flow.ins_37 | flow |  |  |  |  | ins_37 `` | ins_37 `` | ins_37 `` | ins_37 `` | ins_37 `` | ins_37 `` |
| flow.ins_38 | flow |  |  |  |  | ins_38 `` | ins_38 `` | ins_38 `` | ins_38 `` | ins_38 `` | ins_38 `` |
| flow.ins_39 | flow |  |  |  |  | ins_39 `` | ins_39 `` | ins_39 `` | ins_39 `` | ins_39 `` | ins_39 `` |
| flow.ins_4 | flow |  |  |  |  | ins_4 `` | ins_4 `` | ins_4 `` | ins_4 `` | ins_4 `` | ins_4 `` |
| flow.ins_41 | flow |  |  |  |  | ins_41 `` | ins_41 `` | ins_41 `` | ins_41 `` | ins_41 `` | ins_41 `` |
| flow.ins_46 | flow |  |  |  |  | ins_46 `` | ins_46 `` | ins_46 `` | ins_46 `` | ins_46 `` | ins_46 `` |
| flow.ins_47 | flow |  |  |  |  | ins_47 `` | ins_47 `` | ins_47 `` | ins_47 `` | ins_47 `` | ins_47 `` |
| flow.ins_48 | flow |  |  |  |  | ins_48 `` | ins_48 `` | ins_48 `` | ins_48 `` | ins_48 `` | ins_48 `` |
| flow.ins_49 | flow |  |  |  |  | ins_49 `` | ins_49 `` | ins_49 `` | ins_49 `` | ins_49 `` | ins_49 `` |
| flow.ins_5 | flow |  |  |  |  | ins_5 `` | ins_5 `` | ins_5 `` | ins_5 `` | ins_5 `` | ins_5 `` |
| flow.ins_6 | flow |  |  |  |  | ins_6 `` | ins_6 `` | ins_6 `` | ins_6 `` | ins_6 `` | ins_6 `` |
| flow.ins_68 | flow | ins_68 `` |  |  |  |  |  |  |  |  |  |
| flow.ins_69 | flow | ins_69 `` |  |  |  |  |  |  |  |  |  |
| flow.ins_7 | flow |  |  |  |  | ins_7 `` | ins_7 `` | ins_7 `` | ins_7 `` | ins_7 `` | ins_7 `` |
| flow.ins_79 | flow | ins_79 `S` |  |  |  |  |  |  |  |  |  |
| flow.ins_8 | flow |  |  |  |  | ins_8 `` | ins_8 `` | ins_8 `` | ins_8 `` | ins_8 `` | ins_8 `` |
| flow.ins_89 | flow | ins_89 `` |  |  |  |  |  |  |  |  |  |
| flow.ins_9 | flow |  |  |  |  | ins_9 `` | ins_9 `` | ins_9 `` | ins_9 `` | ins_9 `` | ins_9 `` |
| flow.iset | flow | ins_6 `SS` |  |  |  |  |  |  |  |  |  |
| flow.iset_add | flow | ins_20 `SSS` |  |  |  |  |  |  |  |  |  |
| flow.iset_bossvar | flow | ins_86 `SSS` |  |  |  |  |  |  |  |  |  |
| flow.iset_div | flow | ins_23 `SSS` |  |  |  |  |  |  |  |  |  |
| flow.iset_mod | flow | ins_24 `SSS` |  |  |  |  |  |  |  |  |  |
| flow.iset_mul | flow | ins_22 `SSS` |  |  |  |  |  |  |  |  |  |
| flow.iset_rand_sign | flow | ins_8 `SS` |  |  |  |  |  |  |  |  |  |
| flow.iset_sub | flow | ins_21 `SSS` |  |  |  |  |  |  |  |  |  |
| flow.isub | flow | ins_11 `SS` |  |  |  |  |  |  |  |  |  |
| flow.jmp | flow | ins_4 `So` |  | ins_12 `ot` | ins_12 `ot` | ins_12 `o` | ins_12 `o` | ins_12 `o` | ins_12 `o` | ins_12 `o` | ins_12 `o` |
| flow.jmp_eq | flow |  |  | ins_13 `ot` | ins_13 `ot` | ins_13 `o` | ins_13 `o` | ins_13 `o` | ins_13 `o` | ins_13 `o` | ins_13 `o` |
| flow.jmp_equ | flow | ins_40 `SSSo` |  |  |  |  |  |  |  |  |  |
| flow.jmp_equ_f | flow | ins_41 `ffSo` |  |  |  |  |  |  |  |  |  |
| flow.jmp_geq | flow | ins_50 `SSSo` |  |  |  |  |  |  |  |  |  |
| flow.jmp_geq_f | flow | ins_51 `ffSo` |  |  |  |  |  |  |  |  |  |
| flow.jmp_gre | flow | ins_48 `SSSo` |  |  |  |  |  |  |  |  |  |
| flow.jmp_gre_f | flow | ins_49 `ffSo` |  |  |  |  |  |  |  |  |  |
| flow.jmp_leq | flow | ins_46 `SSSo` |  |  |  |  |  |  |  |  |  |
| flow.jmp_leq_f | flow | ins_47 `ffSo` |  |  |  |  |  |  |  |  |  |
| flow.jmp_lss | flow | ins_44 `SSSo` |  |  |  |  |  |  |  |  |  |
| flow.jmp_lss_f | flow | ins_45 `ffSo` |  |  |  |  |  |  |  |  |  |
| flow.jmp_neq | flow | ins_42 `SSSo` |  | ins_14 `ot` | ins_14 `ot` | ins_14 `o` | ins_14 `o` | ins_14 `o` | ins_14 `o` | ins_14 `o` | ins_14 `o` |
| flow.jmp_neq_f | flow | ins_43 `ffSo` |  |  |  |  |  |  |  |  |  |
| flow.kill_all_async | flow |  |  | ins_21 `` | ins_21 `` | ins_21 `` | ins_21 `` | ins_21 `` | ins_21 `` | ins_21 `` | ins_21 `` |
| flow.kill_async | flow |  |  | ins_17 `S` | ins_17 `S` | ins_17 `S` | ins_17 `S` | ins_17 `S` | ins_17 `S` | ins_17 `S` | ins_17 `S` |
| flow.leqf | flow |  |  | ins_66 `` | ins_66 `` | ins_66 `` | ins_66 `` | ins_66 `` | ins_66 `` | ins_66 `` | ins_66 `` |
| flow.leqi | flow |  |  | ins_65 `` | ins_65 `` | ins_65 `` | ins_65 `` | ins_65 `` | ins_65 `` | ins_65 `` | ins_65 `` |
| flow.lessf | flow |  |  | ins_64 `` | ins_64 `` | ins_64 `` | ins_64 `` | ins_64 `` | ins_64 `` | ins_64 `` | ins_64 `` |
| flow.lessi | flow |  |  | ins_63 `` | ins_63 `` | ins_63 `` | ins_63 `` | ins_63 `` | ins_63 `` | ins_63 `` | ins_63 `` |
| flow.linear_func | flow |  |  | ins_89 `SSS` | ins_89 `fff` | ins_89 `fff` | ins_89 `fff` | ins_89 `fff` | ins_89 `fff` | ins_89 `fff` | ins_89 `fff` |
| flow.loop | flow | ins_5 `SoS` |  |  |  |  |  |  |  |  |  |
| flow.math92 | flow |  |  | ins_92 `` | ins_92 `` | ins_92 `SfSSffff` | ins_92 `SfSSffff` | ins_92 `SfSSffff` | ins_92 `SfSSffff` | ins_92 `SfSSffff` | ins_92 `SfSSffff` |
| flow.math93 | flow |  |  | ins_93 `` | ins_93 `` | ins_93 `ffff` | ins_93 `ffff` | ins_93 `ffff` | ins_93 `ffff` | ins_93 `ffff` | ins_93 `ffff` |
| flow.math_angle | flow | ins_34 `fffff` |  |  |  |  |  |  |  |  |  |
| flow.math_circle_pos | flow | ins_38 `ffff` |  |  |  |  |  |  |  |  |  |
| flow.math_distance | flow | ins_39 `fffff` |  |  |  |  |  |  |  |  |  |
| flow.modi | flow |  |  | ins_58 `` | ins_58 `` | ins_58 `` | ins_58 `` | ins_58 `` | ins_58 `` | ins_58 `` | ins_58 `` |
| flow.mulf | flow |  |  | ins_55 `` | ins_55 `` | ins_55 `` | ins_55 `` | ins_55 `` | ins_55 `` | ins_55 `` | ins_55 `` |
| flow.muli | flow |  |  | ins_54 `` | ins_54 `` | ins_54 `` | ins_54 `` | ins_54 `` | ins_54 `` | ins_54 `` | ins_54 `` |
| flow.negf | flow |  |  | ins_85 `` | ins_85 `` | ins_84 `` | ins_84 `` | ins_84 `` | ins_84 `` | ins_84 `` | ins_84 `` |
| flow.negi | flow |  |  | ins_84 `` | ins_84 `` | ins_83 `` | ins_83 `` | ins_83 `` | ins_83 `` | ins_83 `` | ins_83 `` |
| flow.neqf | flow |  |  | ins_62 `` | ins_62 `` | ins_62 `` | ins_62 `` | ins_62 `` | ins_62 `` | ins_62 `` | ins_62 `` |
| flow.neqi | flow |  |  | ins_61 `` | ins_61 `` | ins_61 `` | ins_61 `` | ins_61 `` | ins_61 `` | ins_61 `` | ins_61 `` |
| flow.nop | flow | ins_0 `S` |  | ins_0 `` | ins_0 `` | ins_0 `` | ins_0 `` | ins_0 `` | ins_0 `` | ins_0 `` | ins_0 `` |
| flow.nop3 | flow | ins_3 `S` |  |  |  |  |  |  |  |  |  |
| flow.nop84 | flow | ins_84 `` |  |  |  |  |  |  |  |  |  |
| flow.nop85 | flow | ins_85 `` |  |  |  |  |  |  |  |  |  |
| flow.norm_rad | flow | ins_37 `f` |  |  |  |  |  |  |  |  |  |
| flow.notf | flow |  |  | ins_72 `` | ins_72 `` | ins_72 `` | ins_72 `` | ins_72 `` | ins_72 `` | ins_72 `` | ins_72 `` |
| flow.noti | flow |  |  | ins_71 `` | ins_71 `` | ins_71 `` | ins_71 `` | ins_71 `` | ins_71 `` | ins_71 `` | ins_71 `` |
| flow.or | flow |  |  | ins_73 `` | ins_73 `` | ins_73 `` | ins_73 `` | ins_73 `` | ins_73 `` | ins_73 `` | ins_73 `` |
| flow.point_rotate | flow |  |  | ins_90 `` | ins_90 `` | ins_90 `fffff` | ins_90 `fffff` | ins_90 `fffff` | ins_90 `fffff` | ins_90 `fffff` | ins_90 `fffff` |
| flow.pushf | flow |  |  | ins_44 `f` | ins_44 `f` | ins_44 `f` | ins_44 `f` | ins_44 `f` | ins_44 `f` | ins_44 `f` | ins_44 `f` |
| flow.pushi | flow |  |  | ins_42 `S` | ins_42 `S` | ins_42 `S` | ins_42 `S` | ins_42 `S` | ins_42 `S` | ins_42 `S` | ins_42 `S` |
| flow.ret | flow | ins_53 `` |  | ins_10 `` | ins_10 `` | ins_10 `` | ins_10 `` | ins_10 `` | ins_10 `` | ins_10 `` | ins_10 `` |
| flow.setf | flow |  |  | ins_45 `f` | ins_45 `f` | ins_45 `f` | ins_45 `f` | ins_45 `f` | ins_45 `f` | ins_45 `f` | ins_45 `f` |
| flow.seti | flow |  |  | ins_43 `S` | ins_43 `S` | ins_43 `S` | ins_43 `S` | ins_43 `S` | ins_43 `S` | ins_43 `S` | ins_43 `S` |
| flow.square_sum | flow |  |  | ins_86 `fff` | ins_86 `fff` | ins_85 `fff` | ins_85 `fff` | ins_85 `fff` | ins_85 `fff` | ins_85 `fff` | ins_85 `fff` |
| flow.square_sum_root | flow |  |  |  |  | ins_86 `fff` | ins_86 `fff` | ins_86 `fff` | ins_86 `fff` | ins_86 `fff` | ins_86 `fff` |
| flow.stack_alloc | flow |  |  | ins_40 `S` | ins_40 `S` | ins_40 `S` | ins_40 `S` | ins_40 `S` | ins_40 `S` | ins_40 `S` | ins_40 `S` |
| flow.stack_cos | flow |  |  | ins_80 `` | ins_80 `` | ins_80 `` | ins_80 `` | ins_80 `` | ins_80 `` | ins_80 `` | ins_80 `` |
| flow.stack_sin | flow |  |  | ins_79 `` | ins_79 `` | ins_79 `` | ins_79 `` | ins_79 `` | ins_79 `` | ins_79 `` | ins_79 `` |
| flow.stack_sqrt | flow |  |  | ins_88 `` | ins_88 `` | ins_88 `` | ins_88 `` | ins_88 `` | ins_88 `` | ins_88 `` | ins_88 `` |
| flow.subf | flow |  |  | ins_53 `` | ins_53 `` | ins_53 `` | ins_53 `` | ins_53 `` | ins_53 `` | ins_53 `` | ins_53 `` |
| flow.subi | flow |  |  | ins_52 `` | ins_52 `` | ins_52 `` | ins_52 `` | ins_52 `` | ins_52 `` | ins_52 `` | ins_52 `` |
| flow.trail_familiar_set | flow | ins_83 `S` |  |  |  |  |  |  |  |  |  |
| flow.unknown27 | flow |  |  | ins_27 `` | ins_27 `` | ins_27 `` | ins_27 `` | ins_27 `` | ins_27 `` | ins_27 `` | ins_27 `` |
| flow.unknown30 | flow |  |  | ins_30 `` | ins_30 `` | ins_30 `m` | ins_30 `m` | ins_30 `m` | ins_30 `m` | ins_30 `m` | ins_30 `m` |
| flow.unknown31 | flow |  |  | ins_31 `` | ins_31 `` | ins_31 `` | ins_31 `` | ins_31 `` | ins_31 `` | ins_31 `` | ins_31 `` |
| flow.valid_rad | flow |  |  | ins_82 `f` | ins_82 `f` | ins_82 `f` | ins_82 `f` | ins_82 `f` | ins_82 `f` | ins_82 `f` | ins_82 `f` |
| flow.wait | flow | ins_2 `S` |  | ins_83 `S` | ins_83 `S` | ins_23 `S` | ins_23 `S` | ins_23 `S` | ins_23 `S` | ins_23 `S` | ins_23 `S` |
| flow.waitf | flow |  |  |  |  | ins_24 `f` | ins_24 `f` | ins_24 `f` | ins_24 `f` | ins_24 `f` | ins_24 `f` |
| flow.xor | flow |  |  | ins_75 `` | ins_75 `` | ins_75 `` | ins_75 `` | ins_75 `` | ins_75 `` | ins_75 `` | ins_75 `` |
| laser.angle | laser |  |  |  | ins_608 `Sf` | ins_708 `Sf` | ins_708 `Sf` | ins_708 `Sf` | ins_708 `Sf` | ins_708 `Sf` | ins_708 `Sf` |
| laser.curve_on | laser |  |  |  | ins_611 `S` | ins_711 `S` | ins_711 `S` | ins_711 `S` | ins_711 `S` | ins_711 `S` | ins_711 `S` |
| laser.debug700 | laser |  |  |  | ins_700 `S` |  |  |  |  |  |  |
| laser.end | laser |  |  |  | ins_610 `S` | ins_710 `S` | ins_710 `S` | ins_710 `S` | ins_710 `S` | ins_710 `S` | ins_710 `S` |
| laser.et_cancel_rect | laser |  |  |  |  | ins_712 `ff` | ins_712 `ff` | ins_712 `ff` | ins_712 `ff` | ins_712 `ff` | ins_712 `ff` |
| laser.length | laser |  |  |  | ins_606 `Sf` | ins_706 `Sf` | ins_706 `Sf` | ins_706 `Sf` | ins_706 `Sf` | ins_706 `Sf` | ins_706 `Sf` |
| laser.new | laser |  |  |  | ins_600 `Sffff` | ins_700 `Sffff` | ins_700 `Sffff` | ins_700 `Sffff` | ins_700 `Sffff` | ins_700 `Sffff` | ins_700 `Sffff` |
| laser.offset | laser | ins_119 `Sfff` |  |  | ins_604 `Sff` | ins_704 `Sff` | ins_704 `Sff` | ins_704 `Sff` | ins_704 `Sff` | ins_704 `Sff` | ins_704 `Sff` |
| laser.on | laser | ins_114 `SSffffffSSSSSS` |  | ins_428 `SSffSfSf` | ins_602 `S` | ins_702 `S` | ins_702 `S` | ins_702 `S` | ins_702 `S` | ins_702 `S` | ins_702 `S` |
| laser.rotation | laser |  |  |  | ins_609 `Sf` | ins_709 `Sf` | ins_709 `Sf` | ins_709 `Sf` | ins_709 `Sf` | ins_709 `Sf` | ins_709 `Sf` |
| laser.straight_on | laser |  |  | ins_413 `SSSfffSSSSfS` | ins_603 `SS` | ins_703 `SS` | ins_703 `SS` | ins_703 `SS` | ins_703 `SS` | ins_703 `SS` | ins_703 `SS` |
| laser.timing | laser |  |  |  | ins_601 `SSSSSS` | ins_701 `SSSSSS` | ins_701 `SSSSSS` | ins_701 `SSSSSS` | ins_701 `SSSSSS` | ins_701 `SSSSSS` | ins_701 `SSSSSS` |
| laser.trajectory | laser |  |  |  | ins_605 `Sff` | ins_705 `Sff` | ins_705 `Sff` | ins_705 `Sff` | ins_705 `Sff` | ins_705 `Sff` | ins_705 `Sff` |
| laser.unknown713 | laser |  |  |  |  | ins_713 `SS` | ins_713 `SS` | ins_713 `SS` | ins_713 `SS` | ins_713 `SS` | ins_713 `SS` |
| laser.unknown714 | laser |  |  |  |  | ins_714 `SS` | ins_714 `SS` | ins_714 `SS` | ins_714 `SS` | ins_714 `SS` | ins_714 `SS` |
| laser.width | laser |  |  |  | ins_607 `Sf` | ins_707 `Sf` | ins_707 `Sf` | ins_707 `Sf` | ins_707 `Sf` | ins_707 `Sf` | ins_707 `Sf` |
| movement.bezier | movement |  |  | ins_305 `Sffffff` | ins_325 `Sffffff` | ins_425 `Sffffff` | ins_425 `Sffffff` | ins_425 `Sffffff` | ins_425 `Sffffff` | ins_425 `Sffffff` | ins_425 `Sffffff` |
| movement.bezier_rel | movement |  |  | ins_306 `Sffffff` | ins_326 `Sffffff` | ins_426 `Sffffff` | ins_426 `Sffffff` | ins_426 `Sffffff` | ins_426 `Sffffff` | ins_426 `Sffffff` | ins_426 `Sffffff` |
| movement.bomb_shield | movement |  |  |  | ins_446 `Sf` |  |  |  |  |  |  |
| movement.call_std | movement |  |  | ins_441 `S` |  |  |  |  |  |  |  |
| movement.circle.set | movement | ins_73 `Sfff` |  | ins_288 `ffff` | ins_308 `ffff` | ins_408 `ffff` | ins_408 `ffff` | ins_408 `ffff` | ins_408 `ffff` | ins_408 `ffff` | ins_408 `ffff` |
| movement.circle.tween | movement |  |  | ins_289 `SSfff` | ins_309 `SSfff` | ins_409 `SSfff` | ins_409 `SSfff` | ins_409 `SSfff` | ins_409 `SSfff` | ins_409 `SSfff` | ins_409 `SSfff` |
| movement.circle_rel.set | movement |  |  | ins_290 `ffff` | ins_310 `ffff` | ins_410 `ffff` | ins_410 `ffff` | ins_410 `ffff` | ins_410 `ffff` | ins_410 `ffff` | ins_410 `ffff` |
| movement.circle_rel.tween | movement |  |  | ins_291 `SSffS` | ins_311 `SSfff` | ins_411 `SSfff` | ins_411 `SSfff` | ins_411 `SSfff` | ins_411 `SSfff` | ins_411 `SSfff` | ins_411 `SSfff` |
| movement.death_wait | movement |  |  |  | ins_420 `` |  |  |  |  |  |  |
| movement.dialog_read | movement |  |  |  | ins_418 `S` |  |  |  |  |  |  |
| movement.dialog_wait | movement |  |  |  | ins_419 `` |  |  |  |  |  |  |
| movement.diff_f | movement |  |  |  | ins_436 `fffff` |  |  |  |  |  |  |
| movement.diff_i | movement |  |  |  | ins_435 `SSSSS` |  |  |  |  |  |  |
| movement.diff_wait | movement |  |  |  | ins_448 `SSSS` |  |  |  |  |  |  |
| movement.drop_area | movement |  |  |  | ins_408 `ff` |  |  |  |  |  |  |
| movement.drop_clear | movement |  |  |  | ins_406 `` |  |  |  |  |  |  |
| movement.drop_extra | movement |  |  |  | ins_407 `SS` |  |  |  |  |  |  |
| movement.drop_items | movement |  |  |  | ins_409 `` |  |  |  |  |  |  |
| movement.drop_main | movement |  |  |  | ins_410 `S` |  |  |  |  |  |  |
| movement.ds_nice | movement |  |  |  | ins_459 `S` |  |  |  |  |  |  |
| movement.ds_score_mult | movement |  |  |  | ins_460 `f` |  |  |  |  |  |  |
| movement.ds_timer | movement |  |  |  | ins_458 `S` |  |  |  |  |  |  |
| movement.ellipse.set | movement |  |  | ins_300 `ffffSff` | ins_320 `ffffff` | ins_420 `ffffff` | ins_420 `ffffff` | ins_420 `ffffff` | ins_420 `ffffff` | ins_420 `ffffff` | ins_420 `ffffff` |
| movement.ellipse.tween | movement |  |  | ins_301 `SSfffff` | ins_321 `SSfffff` | ins_421 `SSfffff` | ins_421 `SSfffff` | ins_421 `SSfffff` | ins_421 `SSfffff` | ins_421 `SSfffff` | ins_421 `SSfffff` |
| movement.ellipse_rel.set | movement |  |  | ins_302 `ffffSff` | ins_322 `ffffff` | ins_422 `ffffff` | ins_422 `ffffff` | ins_422 `ffffff` | ins_422 `ffffff` | ins_422 `ffffff` | ins_422 `ffffff` |
| movement.ellipse_rel.tween | movement |  |  | ins_303 `SSfffff` | ins_323 `SSfffff` | ins_423 `SSfffff` | ins_423 `SSfffff` | ins_423 `SSfffff` | ins_423 `SSfffff` | ins_423 `SSfffff` | ins_423 `SSfffff` |
| movement.et_cancel2 | movement |  |  | ins_446 `f` |  |  |  |  |  |  |  |
| movement.et_clear2 | movement |  |  | ins_447 `f` |  |  |  |  |  |  |  |
| movement.et_protect_range | movement |  |  |  | ins_426 `f` |  |  |  |  |  |  |
| movement.flag_clear | movement |  |  |  | ins_403 `S` |  |  |  |  |  |  |
| movement.flag_set | movement |  |  |  | ins_402 `S` |  |  |  |  |  |  |
| movement.fog | movement |  |  | ins_440 `fS` |  |  |  |  |  |  |  |
| movement.func_call | movement |  |  | ins_449 `S` |  |  |  |  |  |  |  |
| movement.func_set | movement |  |  | ins_443 `S` |  |  |  |  |  |  |  |
| movement.game_speed | movement |  |  |  | ins_447 `f` |  |  |  |  |  |  |
| movement.hit_sound | movement |  |  |  | ins_453 `S` |  |  |  |  |  |  |
| movement.laser_cancel | movement |  |  |  | ins_445 `` |  |  |  |  |  |  |
| movement.laser_on3 | movement |  |  | ins_433 `SSffSfff` |  |  |  |  |  |  |  |
| movement.laser_on_a | movement |  |  | ins_412 `SSffffSf` |  |  |  |  |  |  |  |
| movement.laser_on_a2 | movement |  |  | ins_431 `SSffSfff` |  |  |  |  |  |  |  |
| movement.laser_st_on2 | movement |  |  | ins_429 `SSSfffSSSSfS` |  |  |  |  |  |  |  |
| movement.laser_st_on3 | movement |  |  | ins_432 `SSSfffSSSSfS` |  |  |  |  |  |  |  |
| movement.laser_st_on4 | movement |  |  | ins_434 `SSSfffSSSSfS` |  |  |  |  |  |  |  |
| movement.laser_unknown414 | movement |  |  | ins_414 `Sff` |  |  |  |  |  |  |  |
| movement.laser_unknown415 | movement |  |  | ins_415 `Sff` |  |  |  |  |  |  |  |
| movement.laser_unknown416 | movement |  |  | ins_416 `Sf` |  |  |  |  |  |  |  |
| movement.laser_unknown417 | movement |  |  | ins_417 `Sf` |  |  |  |  |  |  |  |
| movement.laser_unknown418 | movement |  |  | ins_418 `Sf` |  |  |  |  |  |  |  |
| movement.laser_unknown419 | movement |  |  | ins_419 `Sf` |  |  |  |  |  |  |  |
| movement.laser_unknown430 | movement |  |  | ins_430 `Sff` |  |  |  |  |  |  |  |
| movement.life_hide | movement |  |  | ins_442 `S` |  |  |  |  |  |  |  |
| movement.life_marker | movement |  |  |  | ins_427 `SfS` |  |  |  |  |  |  |
| movement.move419 | movement |  |  |  |  | ins_419 `ff` | ins_419 `ff` | ins_419 `ff` | ins_419 `ff` | ins_419 `ff` | ins_419 `ff` |
| movement.move432 | movement |  |  |  | ins_332 `S` |  |  |  |  |  |  |
| movement.move433 | movement |  |  |  | ins_333 `` |  |  |  |  |  |  |
| movement.move_accel | movement | ins_71 `f` |  |  |  |  |  |  |  |  |  |
| movement.move_add | movement |  |  | ins_298 `ff` | ins_318 `ff` | ins_418 `ff` | ins_418 `ff` | ins_418 `ff` | ins_418 `ff` | ins_418 `ff` | ins_418 `ff` |
| movement.move_add_rel | movement |  |  | ins_299 `ff` | ins_319 `ff` |  |  |  |  |  |  |
| movement.move_add_rel_time | movement |  |  |  |  | ins_437 `SSff` | ins_437 `SSff` | ins_437 `SSff` | ins_437 `SSff` | ins_437 `SSff` | ins_437 `SSff` |
| movement.move_add_time | movement |  |  |  |  | ins_436 `SSff` | ins_436 `SSff` | ins_436 `SSff` | ins_436 `SSff` | ins_436 `SSff` | ins_436 `SSff` |
| movement.move_angle | movement |  |  |  |  |  | ins_440 `f` | ins_440 `f` | ins_440 `f` | ins_440 `f` | ins_440 `f` |
| movement.move_angle_rel | movement |  |  |  |  |  | ins_442 `f` | ins_442 `f` | ins_442 `f` | ins_442 `f` | ins_442 `f` |
| movement.move_angle_rel_time | movement |  |  |  |  |  | ins_443 `SSf` | ins_443 `SSf` | ins_443 `SSf` | ins_443 `SSf` | ins_443 `SSf` |
| movement.move_angle_time | movement |  |  |  |  |  | ins_441 `SSf` | ins_441 `SSf` | ins_441 `SSf` | ins_441 `SSf` | ins_441 `SSf` |
| movement.move_boss | movement |  |  | ins_294 `` | ins_314 `` | ins_414 `` | ins_414 `` | ins_414 `` | ins_414 `` | ins_414 `` | ins_414 `` |
| movement.move_boss_rel | movement |  |  | ins_295 `` | ins_315 `` | ins_415 `` | ins_415 `` | ins_415 `` | ins_415 `` | ins_415 `` | ins_415 `` |
| movement.move_circle_abs | movement | ins_72 `Sffffff` |  |  |  |  |  |  |  |  |  |
| movement.move_circle_change | movement | ins_74 `Sff` |  |  |  |  |  |  |  |  |  |
| movement.move_curve | movement | ins_70 `f` |  |  |  | ins_434 `SSSff` | ins_434 `SSSff` | ins_434 `SSSff` | ins_434 `SSSff` | ins_434 `SSSff` | ins_434 `SSSff` |
| movement.move_curve_add | movement |  |  |  |  | ins_438 `SSSff` | ins_438 `SSSff` | ins_438 `SSSff` | ins_438 `SSSff` | ins_438 `SSSff` | ins_438 `SSSff` |
| movement.move_curve_add_rel | movement |  |  |  |  | ins_439 `SSSff` | ins_439 `SSSff` | ins_439 `SSSff` | ins_439 `SSSff` | ins_439 `SSSff` | ins_439 `SSSff` |
| movement.move_curve_rel | movement |  |  |  |  | ins_435 `SSSff` | ins_435 `SSSff` | ins_435 `SSSff` | ins_435 `SSSff` | ins_435 `SSSff` | ins_435 `SSSff` |
| movement.move_dir | movement | ins_65 `ff` |  |  |  |  |  |  |  |  |  |
| movement.move_dir_time | movement | ins_66 `SSff` |  |  |  |  |  |  |  |  |  |
| movement.move_enm | movement |  |  |  |  | ins_432 `S` | ins_432 `S` | ins_432 `S` | ins_432 `S` | ins_432 `S` | ins_432 `S` |
| movement.move_enm_rel | movement |  |  |  |  | ins_433 `S` | ins_433 `S` | ins_433 `S` | ins_433 `S` | ins_433 `S` | ins_433 `S` |
| movement.move_limit | movement | ins_75 `ffff` |  | ins_324 `ffff` | ins_404 `ffff` | ins_504 `ffff` | ins_504 `ffff` | ins_504 `ffff` | ins_504 `ffff` | ins_504 `ffff` | ins_504 `ffff` |
| movement.move_limit_reset | movement | ins_76 `` |  | ins_325 `` | ins_405 `` | ins_505 `` | ins_505 `` | ins_505 `` | ins_505 `` | ins_505 `` | ins_505 `` |
| movement.move_pos3d | movement |  |  | ins_296 `SSf` | ins_316 `ff` | ins_416 `fff` | ins_416 `fff` | ins_416 `fff` | ins_416 `fff` | ins_416 `fff` | ins_416 `fff` |
| movement.move_pos3d_rel | movement |  |  | ins_297 `ff` | ins_317 `fff` | ins_417 `fff` | ins_417 `fff` | ins_417 `fff` | ins_417 `fff` | ins_417 `fff` | ins_417 `fff` |
| movement.move_rand | movement |  |  | ins_292 `SSf` | ins_312 `SSf` | ins_412 `SSf` | ins_412 `SSf` | ins_412 `SSf` | ins_412 `SSf` | ins_412 `SSf` | ins_412 `SSf` |
| movement.move_rand_rel | movement |  |  | ins_293 `SSf` | ins_313 `SSf` | ins_413 `SSf` | ins_413 `SSf` | ins_413 `SSf` | ins_413 `SSf` | ins_413 `SSf` | ins_413 `SSf` |
| movement.move_rand_time | movement | ins_67 `SSf` |  |  |  |  |  |  |  |  |  |
| movement.move_rand_time2 | movement | ins_178 `SSf` |  |  |  |  |  |  |  |  |  |
| movement.move_set_mirror | movement |  |  | ins_304 `S` | ins_324 `S` | ins_424 `S` | ins_424 `S` | ins_424 `S` | ins_424 `S` | ins_424 `S` | ins_424 `S` |
| movement.move_speed | movement |  |  |  |  |  | ins_444 `f` | ins_444 `f` | ins_444 `f` | ins_444 `f` | ins_444 `f` |
| movement.move_speed_rel | movement |  |  |  |  |  | ins_446 `f` | ins_446 `f` | ins_446 `f` | ins_446 `f` | ins_446 `f` |
| movement.move_speed_rel_time | movement |  |  |  |  |  | ins_447 `SSf` | ins_447 `SSf` | ins_447 `SSf` | ins_447 `SSf` | ins_447 `SSf` |
| movement.move_speed_time | movement |  |  |  |  |  | ins_445 `SSf` | ins_445 `SSf` | ins_445 `SSf` | ins_445 `SSf` | ins_445 `SSf` |
| movement.move_vel_nm | movement |  |  |  | ins_328 `ff` | ins_428 `ff` | ins_428 `ff` | ins_428 `ff` | ins_428 `ff` | ins_428 `ff` | ins_428 `ff` |
| movement.move_vel_nm_rel | movement |  |  |  | ins_330 `ff` | ins_430 `ff` | ins_430 `ff` | ins_430 `ff` | ins_430 `ff` | ins_430 `ff` | ins_430 `ff` |
| movement.move_vel_nm_rel_time | movement |  |  |  | ins_331 `SSff` | ins_431 `SSff` | ins_431 `SSff` | ins_431 `SSff` | ins_431 `SSff` | ins_431 `SSff` | ins_431 `SSff` |
| movement.move_vel_nm_time | movement |  |  |  | ins_329 `Sfff` | ins_429 `SSff` | ins_429 `SSff` | ins_429 `SSff` | ins_429 `SSff` | ins_429 `SSff` | ins_429 `SSff` |
| movement.play_sound | movement |  |  |  | ins_416 `S` |  |  |  |  |  |  |
| movement.position.set | movement | ins_63 `ff` |  | ins_280 `ff` | ins_300 `ff` | ins_400 `ff` | ins_400 `ff` | ins_400 `ff` | ins_400 `ff` | ins_400 `ff` | ins_400 `ff` |
| movement.position.tween | movement | ins_64 `SSff` |  | ins_281 `SSff` | ins_301 `SSff` | ins_401 `SSff` | ins_401 `SSff` | ins_401 `SSff` | ins_401 `SSff` | ins_401 `SSff` | ins_401 `SSff` |
| movement.position_rel.set | movement |  |  | ins_282 `ff` | ins_302 `ff` | ins_402 `ff` | ins_402 `ff` | ins_402 `ff` | ins_402 `ff` | ins_402 `ff` | ins_402 `ff` |
| movement.position_rel.tween | movement |  |  | ins_283 `SSfS` | ins_303 `SSff` | ins_403 `SSff` | ins_403 `SSff` | ins_403 `SSff` | ins_403 `SSff` | ins_403 `SSff` | ins_403 `SSff` |
| movement.rank_f2 | movement |  |  |  | ins_431 `fff` |  |  |  |  |  |  |
| movement.rank_f3 | movement |  |  |  | ins_429 `ffff` |  |  |  |  |  |  |
| movement.rank_f5 | movement |  |  |  | ins_430 `ffffff` |  |  |  |  |  |  |
| movement.rank_i2 | movement |  |  |  | ins_434 `SSS` |  |  |  |  |  |  |
| movement.rank_i3 | movement |  |  |  | ins_432 `SSSS` |  |  |  |  |  |  |
| movement.rank_i5 | movement |  |  |  | ins_433 `SSSSSS` |  |  |  |  |  |  |
| movement.reset | movement |  |  | ins_307 `` | ins_327 `` | ins_427 `` | ins_427 `` | ins_427 `` | ins_427 `` | ins_427 `` | ins_427 `` |
| movement.set_hitbox | movement |  |  |  | ins_401 `ff` |  |  |  |  |  |  |
| movement.set_hurtbox | movement |  |  |  | ins_400 `ff` |  |  |  |  |  |  |
| movement.set_invuln | movement |  |  |  | ins_415 `S` |  |  |  |  |  |  |
| movement.set_screen_shake | movement |  |  |  | ins_417 `SSS` |  |  |  |  |  |  |
| movement.spell_ex | movement |  |  |  | ins_422 `SSSx` |  |  |  |  |  |  |
| movement.spell_timeout | movement |  |  |  | ins_442 `` |  |  |  |  |  |  |
| movement.spell_unused | movement |  |  |  | ins_428 `SSSx` |  |  |  |  |  |  |
| movement.stage_logo | movement |  |  |  | ins_454 `` |  |  |  |  |  |  |
| movement.stars | movement |  |  |  | ins_440 `S` |  |  |  |  |  |  |
| movement.store_coords | movement |  |  |  | ins_456 `ffS` |  |  |  |  |  |  |
| movement.unknown441 | movement |  |  |  | ins_441 `S` |  |  |  |  |  |  |
| movement.unknown443 | movement |  |  |  | ins_443 `` |  |  |  |  |  |  |
| movement.unknown444 | movement |  |  | ins_444 `S` | ins_444 `S` |  |  |  |  |  |  |
| movement.unknown445 | movement |  |  | ins_445 `S` |  |  |  |  |  |  |  |
| movement.unknown448 | movement |  |  | ins_448 `S` |  |  |  |  |  |  |  |
| movement.unknown449 | movement |  |  |  | ins_449 `S` |  |  |  |  |  |  |
| movement.unknown450 | movement |  |  | ins_450 `S` | ins_450 `S` |  |  |  |  |  |  |
| movement.unknown451 | movement |  |  |  | ins_451 `S` |  |  |  |  |  |  |
| movement.unknown457 | movement |  |  |  | ins_457 `` |  |  |  |  |  |  |
| movement.unknown461 | movement |  |  |  | ins_461 `f` |  |  |  |  |  |  |
| movement.unknown462 | movement |  |  |  | ins_462 `S` |  |  |  |  |  |  |
| movement.unknown463 | movement |  |  |  | ins_463 `S` |  |  |  |  |  |  |
| movement.velocity.set | movement |  |  | ins_284 `ff` | ins_304 `ff` | ins_404 `ff` | ins_404 `ff` | ins_404 `ff` | ins_404 `ff` | ins_404 `ff` | ins_404 `ff` |
| movement.velocity.tween | movement |  |  | ins_285 `SSff` | ins_305 `SSff` | ins_405 `SSff` | ins_405 `SSff` | ins_405 `SSff` | ins_405 `SSff` | ins_405 `SSff` | ins_405 `SSff` |
| movement.velocity_rel.set | movement |  |  | ins_286 `ff` | ins_306 `ff` | ins_406 `ff` | ins_406 `ff` | ins_406 `ff` | ins_406 `ff` | ins_406 `ff` | ins_406 `ff` |
| movement.velocity_rel.tween | movement |  |  | ins_287 `SSff` | ins_307 `SSff` | ins_407 `SSff` | ins_407 `SSff` | ins_407 `SSff` | ins_407 `SSff` | ins_407 `SSff` | ins_407 `SSff` |
| movement.z_index | movement |  |  |  | ins_452 `f` |  |  |  |  |  |  |
| unit.bomb_invuln | unit |  |  |  |  |  | ins_565 `f` | ins_565 `f` | ins_565 `f` | ins_565 `f` | ins_565 `f` |
| unit.bomb_shield | unit |  |  |  |  | ins_546 `SS` | ins_546 `SS` | ins_546 `SS` | ins_546 `SS` | ins_546 `SS` | ins_546 `SS` |
| unit.boss_wait | unit |  |  |  |  | ins_520 `` | ins_520 `` | ins_520 `` | ins_520 `` | ins_520 `` | ins_520 `` |
| unit.call_std | unit |  |  |  | ins_527 `` |  |  |  |  |  |  |
| unit.dialog_read | unit |  |  |  |  | ins_518 `S` | ins_518 `S` | ins_518 `S` | ins_518 `S` | ins_518 `S` | ins_518 `S` |
| unit.dialog_wait | unit |  |  |  |  | ins_519 `` | ins_519 `` | ins_519 `` | ins_519 `` | ins_519 `` | ins_519 `` |
| unit.die | unit |  |  |  |  | ins_561 `` | ins_561 `` | ins_561 `` | ins_561 `` | ins_561 `` | ins_561 `` |
| unit.diff_f | unit |  |  |  |  | ins_536 `fffff` | ins_536 `fffff` | ins_536 `fffff` | ins_536 `fffff` | ins_536 `fffff` | ins_536 `fffff` |
| unit.diff_i | unit |  |  |  |  | ins_535 `SSSSS` | ins_535 `SSSSS` | ins_535 `SSSSS` | ins_535 `SSSSS` | ins_535 `SSSSS` | ins_535 `SSSSS` |
| unit.diff_wait | unit |  |  |  |  | ins_548 `SSSS` | ins_548 `SSSS` | ins_548 `SSSS` | ins_548 `SSSS` | ins_548 `SSSS` | ins_548 `SSSS` |
| unit.drop_area | unit |  |  |  |  | ins_508 `ff` | ins_508 `ff` | ins_508 `ff` | ins_508 `ff` | ins_508 `ff` | ins_508 `ff` |
| unit.drop_clear | unit |  |  |  |  | ins_506 `` | ins_506 `` | ins_506 `` | ins_506 `` | ins_506 `` | ins_506 `` |
| unit.drop_extra | unit |  |  |  |  | ins_507 `SS` | ins_507 `SS` | ins_507 `SS` | ins_507 `SS` | ins_507 `SS` | ins_507 `SS` |
| unit.drop_items | unit |  |  |  |  | ins_509 `` | ins_509 `` | ins_509 `` | ins_509 `` | ins_509 `` | ins_509 `` |
| unit.drop_items_sp | unit |  |  |  |  | ins_562 `S` | ins_562 `S` | ins_562 `S` | ins_562 `S` | ins_562 `S` | ins_562 `S` |
| unit.drop_main | unit |  |  |  |  | ins_510 `S` | ins_510 `S` | ins_510 `S` | ins_510 `S` | ins_510 `S` | ins_510 `S` |
| unit.et_cancel2 | unit |  |  |  | ins_532 `f` |  |  |  |  |  |  |
| unit.et_clear2 | unit |  |  |  | ins_533 `f` |  |  |  |  |  |  |
| unit.et_protect_range | unit |  |  |  |  | ins_526 `f` | ins_526 `f` | ins_526 `f` | ins_526 `f` | ins_526 `f` | ins_526 `f` |
| unit.flag_clear | unit |  |  |  |  | ins_503 `S` | ins_503 `S` | ins_503 `S` | ins_503 `S` | ins_503 `S` | ins_503 `S` |
| unit.flag_ext_dmg | unit |  |  |  | ins_530 `S` |  |  |  |  |  |  |
| unit.flag_mirror | unit |  |  |  |  | ins_558 `S` | ins_558 `S` | ins_558 `S` | ins_558 `S` | ins_558 `S` | ins_558 `S` |
| unit.flag_set | unit |  |  |  |  | ins_502 `S` | ins_502 `S` | ins_502 `S` | ins_502 `S` | ins_502 `S` | ins_502 `S` |
| unit.fog | unit |  |  |  | ins_526 `fS` |  |  |  |  |  |  |
| unit.fog_time | unit |  |  |  |  | ins_557 `SSSff` | ins_557 `SSSff` | ins_557 `SSSff` | ins_557 `SSSff` | ins_557 `SSSff` | ins_557 `SSSff` |
| unit.func_call | unit |  |  |  | ins_534 `S` |  |  |  |  |  |  |
| unit.func_set | unit |  |  |  | ins_529 `S` |  |  |  |  |  |  |
| unit.game_speed | unit |  |  |  |  | ins_547 `f` | ins_547 `f` | ins_547 `f` | ins_547 `f` | ins_547 `f` | ins_547 `f` |
| unit.hit_sound | unit |  |  |  |  | ins_553 `S` | ins_553 `S` | ins_553 `S` | ins_553 `S` | ins_553 `S` | ins_553 `S` |
| unit.hitbox_rotate | unit |  |  |  |  |  | ins_564 `f` | ins_564 `f` | ins_564 `f` | ins_564 `f` | ins_564 `f` |
| unit.laser_cancel | unit |  |  |  |  | ins_545 `` | ins_545 `` | ins_545 `` | ins_545 `` | ins_545 `` | ins_545 `` |
| unit.life_hide | unit |  |  |  | ins_528 `` |  |  |  |  |  |  |
| unit.life_marker | unit |  |  |  |  | ins_527 `SfS` | ins_527 `SfS` | ins_527 `SfS` | ins_527 `SfS` | ins_527 `SfS` | ins_527 `SfS` |
| unit.life_now | unit |  |  |  |  |  |  |  | ins_572 `S` | ins_572 `S` | ins_572 `S` |
| unit.no_hitbox_dur | unit |  |  |  |  | ins_541 `S` | ins_541 `S` | ins_541 `S` | ins_541 `S` | ins_541 `S` | ins_541 `S` |
| unit.play_sound | unit |  |  |  |  | ins_516 `S` | ins_516 `S` | ins_516 `S` | ins_516 `S` | ins_516 `S` | ins_516 `S` |
| unit.rank_f2 | unit |  |  |  |  | ins_531 `fff` | ins_531 `fff` | ins_531 `fff` | ins_531 `fff` | ins_531 `fff` | ins_531 `fff` |
| unit.rank_f3 | unit |  |  |  |  | ins_529 `ffff` | ins_529 `ffff` | ins_529 `ffff` | ins_529 `ffff` | ins_529 `ffff` | ins_529 `ffff` |
| unit.rank_f5 | unit |  |  |  |  | ins_530 `ffffff` | ins_530 `ffffff` | ins_530 `ffffff` | ins_530 `ffffff` | ins_530 `ffffff` | ins_530 `ffffff` |
| unit.rank_i2 | unit |  |  |  |  | ins_534 `SSS` | ins_534 `SSS` | ins_534 `SSS` | ins_534 `SSS` | ins_534 `SSS` | ins_534 `SSS` |
| unit.rank_i3 | unit |  |  |  |  | ins_532 `SSSS` | ins_532 `SSSS` | ins_532 `SSSS` | ins_532 `SSSS` | ins_532 `SSSS` | ins_532 `SSSS` |
| unit.rank_i5 | unit |  |  |  |  | ins_533 `SSSSSS` | ins_533 `SSSSSS` | ins_533 `SSSSSS` | ins_533 `SSSSSS` | ins_533 `SSSSSS` | ins_533 `SSSSSS` |
| unit.set_death | unit |  |  |  |  | ins_556 `m` | ins_556 `m` | ins_556 `m` | ins_556 `m` | ins_556 `m` | ins_556 `m` |
| unit.set_hitbox | unit |  |  |  |  | ins_501 `ff` | ins_501 `ff` | ins_501 `ff` | ins_501 `ff` | ins_501 `ff` | ins_501 `ff` |
| unit.set_hurtbox | unit |  |  |  |  | ins_500 `ff` | ins_500 `ff` | ins_500 `ff` | ins_500 `ff` | ins_500 `ff` | ins_500 `ff` |
| unit.set_invuln | unit |  |  |  |  | ins_515 `S` | ins_515 `S` | ins_515 `S` | ins_515 `S` | ins_515 `S` | ins_515 `S` |
| unit.set_screen_shake | unit |  |  |  |  | ins_517 `SSS` | ins_517 `SSS` | ins_517 `SSS` | ins_517 `SSS` | ins_517 `SSS` | ins_517 `SSS` |
| unit.spell_ex | unit |  |  |  |  | ins_522 `SSSm` | ins_522 `SSSm` | ins_522 `SSSm` | ins_522 `SSSm` | ins_522 `SSSm` | ins_522 `SSSm` |
| unit.spell_mode | unit |  |  |  |  |  | ins_568 `S` | ins_568 `S` | ins_568 `S` | ins_568 `S` | ins_568 `S` |
| unit.spell_timeout | unit |  |  |  |  | ins_542 `` | ins_542 `` | ins_542 `` | ins_542 `` | ins_542 `` | ins_542 `` |
| unit.spell_unused | unit |  |  |  |  | ins_528 `SSSm` | ins_528 `SSSm` | ins_528 `SSSm` | ins_528 `SSSm` | ins_528 `SSSm` | ins_528 `SSSm` |
| unit.stage_logo | unit |  |  |  |  | ins_554 `` | ins_554 `` | ins_554 `` | ins_554 `` | ins_554 `` | ins_554 `` |
| unit.stars | unit |  |  |  |  | ins_540 `S` | ins_540 `S` | ins_540 `S` | ins_540 `S` | ins_540 `S` | ins_540 `S` |
| unit.unknown531 | unit |  |  |  | ins_531 `S` |  |  |  |  |  |  |
| unit.unknown535 | unit |  |  |  | ins_535 `S` |  |  |  |  |  |  |
| unit.unknown536 | unit |  |  |  | ins_536 `S` |  |  |  |  |  |  |
| unit.unknown537 | unit |  |  |  | ins_537 `SSSSSSSSfSSS` |  |  |  |  |  |  |
| unit.unknown538 | unit |  |  |  | ins_538 `SS` |  |  |  |  |  |  |
| unit.unknown543 | unit |  |  |  |  | ins_543 `` | ins_543 `` | ins_543 `` | ins_543 `` | ins_543 `` | ins_543 `` |
| unit.unknown544 | unit |  |  |  |  | ins_544 `S` | ins_544 `S` | ins_544 `S` | ins_544 `S` | ins_544 `S` | ins_544 `S` |
| unit.unknown549 | unit |  |  |  |  | ins_549 `S` | ins_549 `S` | ins_549 `S` | ins_549 `S` | ins_549 `S` | ins_549 `S` |
| unit.unknown550 | unit |  |  |  |  | ins_550 `S` | ins_550 `S` | ins_550 `S` | ins_550 `S` | ins_550 `S` | ins_550 `S` |
| unit.unknown551 | unit |  |  |  |  | ins_551 `S` | ins_551 `S` | ins_551 `S` | ins_551 `S` | ins_551 `S` | ins_551 `S` |
| unit.unknown560 | unit |  |  |  |  | ins_560 `ff` | ins_560 `ff` | ins_560 `ff` | ins_560 `ff` | ins_560 `ff` | ins_560 `ff` |
| unit.unknown563 | unit |  |  |  |  |  | ins_563 `S` | ins_563 `S` | ins_563 `S` | ins_563 `S` | ins_563 `S` |
| unit.unknown566 | unit |  |  |  |  |  | ins_566 `S` | ins_566 `S` | ins_566 `S` | ins_566 `S` | ins_566 `S` |
| unit.unknown567 | unit |  |  |  |  |  | ins_567 `S` | ins_567 `S` | ins_567 `S` | ins_567 `S` | ins_567 `S` |
| unit.unknown569 | unit |  |  |  |  |  |  | ins_569 `S` | ins_569 `S` | ins_569 `S` | ins_569 `S` |
| unit.unknown570 | unit |  |  |  |  |  |  | ins_570 `` | ins_570 `` | ins_570 `` | ins_570 `` |
| unit.unknown571 | unit |  |  |  |  |  |  | ins_571 `` | ins_571 `` | ins_571 `` | ins_571 `` |
| unit.unknown573 | unit |  |  |  |  |  |  |  | ins_573 `SS` | ins_573 `SS` | ins_573 `SS` |
| unit.z_index | unit |  |  |  |  | ins_552 `S` | ins_552 `S` | ins_552 `S` | ins_552 `S` | ins_552 `S` | ins_552 `S` |
