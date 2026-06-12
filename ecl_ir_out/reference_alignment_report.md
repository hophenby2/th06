# ECL IR Reference Alignment Report

Generated from `ecl-by-game`, `ecl_sources/eclmap`, and thtk format tables.

## th15 -> th12
| source | name | sig | mapped | target name | target sig | status |
| --- | --- | --- | --- | --- | --- | --- |
| ins_300 | enmCreate | mffSSS | ins_256 | enmCreate | mffSSS | mapped |
| ins_301 | enmCreateA | mffSSS | ins_257 | enmCreateA | mffSSS | mapped |
| ins_302 | anmSelect | S | ins_258 | anmSelect | S | mapped |
| ins_303 | anmSetSprite | SS | ins_259 | anmSetSprite | SS | mapped |
| ins_304 | enmCreateM | mffSSS | ins_260 | enmCreateM | mffSSS | mapped |
| ins_305 | enmCreateAM | mffSSS | ins_261 | enmCreateAM | mffSSS | mapped |
| ins_306 | anmSetMain | SS | ins_262 | anmSetMain | SS | mapped |
| ins_307 | anmPlay | SS | ins_263 | anmPlay | SS | mapped |
| ins_308 | anmPlayAbs | SS | ins_264 | anmPlayAbs | SS | mapped |
| ins_309 | enmCreateF | mffSSS | ins_265 | enmCreateF | mffSSS | mapped |
| ins_310 | enmCreateAF | mffSSS | ins_266 | enmCreateAF | mffSSS | mapped |
| ins_311 | enmCreateMF | mffSSS | ins_267 | enmCreateMF | mffSSS | mapped |
| ins_312 | enmCreateAMF | mffSSS | ins_268 | enmCreateAMF | mffSSS | mapped |
| ins_313 | anmSelectedPlay | S | ins_269 | anmSelectedPlay | S | mapped |
| ins_314 | anmPlayHigh | SS | ins_272 | anmPlayHigh | SS | mapped |
| ins_315 | anmPlayRotate | SSf | ins_273 | anmPlayRotate | SSf | mapped |
| ins_316 | anm316 | SS |  |  |  | no-same-name |
| ins_317 | anmSwitch | SS | ins_275 | anmSwitch | SS | mapped |
| ins_318 | anmReset |  | ins_276 | anmReset |  | mapped |
| ins_319 | anmRotate | Sf | ins_277 | anmRotate | Sf | mapped |
| ins_320 | anmMove | Sff | ins_279 | anmMove | Sff | mapped |
| ins_321 | enmMapleEnemy | mffSSS | ins_280 | enmMapleEnemy | mSSSSS | same-name-unmapped |
| ins_322 | enm322 | SS |  |  |  | no-same-name |
| ins_323 | deathAnm | SS |  |  |  | no-same-name |
| ins_324 | enm324 |  |  |  |  | no-same-name |
| ins_325 | anmColor | SSSS |  |  |  | no-same-name |
| ins_326 | anmColorTime | SSSSSS |  |  |  | no-same-name |
| ins_327 | anmAlpha | SS |  |  |  | no-same-name |
| ins_328 | anmAlphaTime | SSSS |  |  |  | no-same-name |
| ins_329 | anmScale | Sff | ins_278 | anmScale | Sff | mapped |
| ins_330 | anmScaleTime | SSSff |  |  |  | no-same-name |
| ins_331 | anmAlpha2 | SS |  |  |  | no-same-name |
| ins_332 | anmAlpha2Time | SSSS |  |  |  | no-same-name |
| ins_333 | anm333 | SSSff |  |  |  | no-same-name |
| ins_334 | anm334 | S |  |  |  | no-same-name |
| ins_335 | anmScale2 | Sff |  |  |  | no-same-name |
| ins_336 | anmLayer | SS |  |  |  | no-same-name |
| ins_337 | anmPlayPos | SSfff |  |  |  | no-same-name |
| ins_400 | movePos | ff | ins_300 | movePos | ff | mapped |
| ins_401 | movePosTime | SSff | ins_301 | movePosTime | SSff | mapped |
| ins_402 | movePosRel | ff | ins_302 | movePosRel | ff | mapped |
| ins_403 | movePosRelTime | SSff | ins_303 | movePosRelTime | SSff | mapped |
| ins_404 | moveVel | ff | ins_304 | moveVel | ff | mapped |
| ins_405 | moveVelTime | SSff | ins_305 | moveVelTime | SSff | mapped |
| ins_406 | moveVelRel | ff | ins_306 | moveVelRel | ff | mapped |
| ins_407 | moveVelRelTime | SSff | ins_307 | moveVelRelTime | SSff | mapped |
| ins_408 | moveCircle | ffff | ins_308 | moveCircle | ffff | mapped |
| ins_409 | moveCircleTime | SSfff | ins_309 | moveCircleTime | SSfff | mapped |
| ins_410 | moveCircleRel | ffff | ins_310 | moveCircleRel | ffff | mapped |
| ins_411 | moveCircleRelTime | SSfff | ins_311 | moveCircleRelTime | SSfff | mapped |
| ins_412 | moveRand | SSf | ins_312 | moveRand | SSf | mapped |
| ins_413 | moveRandRel | SSf | ins_313 | moveRandRel | SSf | mapped |
| ins_414 | moveBoss |  | ins_314 | moveBoss |  | mapped |
| ins_415 | moveBossRel |  | ins_315 | moveBossRel |  | mapped |
| ins_416 | movePos3d | fff | ins_316 | movePos3d | ff | same-name-unmapped |
| ins_417 | movePos3dRel | fff | ins_317 | movePos3dRel | fff | mapped |
| ins_418 | moveAdd | ff | ins_318 | moveAdd | ff | mapped |
| ins_419 | move419 | ff |  |  |  | no-same-name |
| ins_420 | moveEllipse | ffffff | ins_320 | moveEllipse | ffffff | mapped |
| ins_421 | moveEllipseTime | SSfffff | ins_321 | moveEllipseTime | SSfffff | mapped |
| ins_422 | moveEllipseRel | ffffff | ins_322 | moveEllipseRel | ffffff | mapped |
| ins_423 | moveEllipseRelTime | SSfffff | ins_323 | moveEllipseRelTime | SSfffff | mapped |
| ins_424 | moveSetMirror | S | ins_324 | moveSetMirror | S | mapped |
| ins_425 | moveBezier | Sffffff | ins_325 | moveBezier | Sffffff | mapped |
| ins_426 | moveBezierRel | Sffffff | ins_326 | moveBezierRel | Sffffff | mapped |
| ins_427 | moveReset |  | ins_327 | moveReset |  | mapped |
| ins_428 | moveVelNM | ff | ins_328 | moveVelNM | ff | mapped |
| ins_429 | moveVelNMTime | SSff | ins_329 | moveVelNMTime | Sfff | same-name-unmapped |
| ins_430 | moveVelNMRel | ff | ins_330 | moveVelNMRel | ff | mapped |
| ins_431 | moveVelNMRelTime | SSff | ins_331 | moveVelNMRelTime | SSff | mapped |
| ins_432 | moveEnm | S |  |  |  | no-same-name |
| ins_433 | moveEnmRel | S |  |  |  | no-same-name |
| ins_434 | moveCurve | SSSff |  |  |  | no-same-name |
| ins_435 | moveCurveRel | SSSff |  |  |  | no-same-name |
| ins_436 | moveAddTime | SSff |  |  |  | no-same-name |
| ins_437 | moveAddRelTime | SSff |  |  |  | no-same-name |
| ins_438 | moveCurveAdd | SSSff |  |  |  | no-same-name |
| ins_439 | moveCurveAddRel | SSSff |  |  |  | no-same-name |
| ins_440 | moveAngle | f |  |  |  | no-same-name |
| ins_441 | moveAngleTime | SSf |  |  |  | no-same-name |
| ins_442 | moveAngleRel | f |  |  |  | no-same-name |
| ins_443 | moveAngleRelTime | SSf |  |  |  | no-same-name |
| ins_444 | moveSpeed | f |  |  |  | no-same-name |
| ins_445 | moveSpeedTime | SSf |  |  |  | no-same-name |
| ins_446 | moveSpeedRel | f |  |  |  | no-same-name |
| ins_447 | moveSpeedRelTime | SSf |  |  |  | no-same-name |
| ins_500 | setHurtbox | ff | ins_400 | setHurtbox | ff | mapped |
| ins_501 | setHitbox | ff | ins_401 | setHitbox | ff | mapped |
| ins_502 | flagSet | S | ins_402 | flagSet | S | mapped |
| ins_503 | flagClear | S | ins_403 | flagClear | S | mapped |
| ins_504 | moveLimit | ffff | ins_404 | moveLimit | ffff | mapped |
| ins_505 | moveLimitReset |  | ins_405 | moveLimitReset |  | mapped |
| ins_506 | dropClear |  | ins_406 | dropClear |  | mapped |
| ins_507 | dropExtra | SS | ins_407 | dropExtra | SS | mapped |
| ins_508 | dropArea | ff | ins_408 | dropArea | ff | mapped |
| ins_509 | dropItems |  | ins_409 | dropItems |  | mapped |
| ins_510 | dropMain | S | ins_410 | dropMain | S | mapped |
| ins_511 | lifeSet | S | ins_411 | lifeSet | S | mapped |
| ins_512 | setBoss | S | ins_412 | setBoss | S | mapped |
| ins_513 | timerReset |  | ins_413 | timerReset |  | mapped |
| ins_514 | setInterrupt | SSSm | ins_414 | setInterrupt | SSSm | mapped |
| ins_515 | setInvuln | S | ins_415 | setInvuln | S | mapped |
| ins_516 | playSound | S | ins_416 | playSound | S | mapped |
| ins_517 | setScreenShake | SSS | ins_417 | setScreenShake | SSS | mapped |
| ins_518 | dialogRead | S | ins_418 | dialogRead | S | mapped |
| ins_519 | dialogWait |  | ins_419 | dialogWait |  | mapped |
| ins_520 | bossWait |  | ins_420 | deathWait |  | mapped |
| ins_521 | setTimeout | Sm | ins_421 | setTimeout | Sm | mapped |
| ins_522 | spellEx | SSSm | ins_422 | spellEx | SSSx | mapped |
| ins_523 | spellEnd |  | ins_423 | spellEnd |  | mapped |
| ins_524 | setChapter | S | ins_424 | setChapter | S | mapped |
| ins_525 | enmKillAll |  | ins_425 | enmKillAll |  | mapped |
| ins_526 | etProtectRange | f | ins_426 | etProtectRange | f | mapped |
| ins_527 | lifeMarker | SfS | ins_427 | lifeMarker | SfS | mapped |
| ins_528 | spellUnused | SSSm | ins_428 | spellUnused | SSSx | mapped |
| ins_529 | rankF3 | ffff | ins_435 | diffI | SSSSS | mapped |
| ins_530 | rankF5 | ffffff | ins_436 | diffF | fffff | mapped |
| ins_531 | rankF2 | fff | ins_437 | spell | SSSx | mapped |
| ins_532 | rankI3 | SSSS | ins_438 | spell2 | SSSx | mapped |
| ins_533 | rankI5 | SSSSSS | ins_439 | spell3 | SSSx | mapped |
| ins_534 | rankI2 | SSS | ins_440 | stars | S | mapped |
| ins_535 | diffI | SSSSS | ins_435 | diffI | SSSSS | mapped |
| ins_536 | diffF | fffff | ins_436 | diffF | fffff | mapped |
| ins_537 | spell | SSSm | ins_437 | spell | SSSx | mapped |
| ins_538 | spell2 | SSSm | ins_438 | spell2 | SSSx | mapped |
| ins_539 | spell3 | SSSm | ins_439 | spell3 | SSSx | mapped |
| ins_540 | stars | S | ins_440 | stars | S | mapped |
| ins_541 | noHitboxDur | S |  |  |  | no-same-name |
| ins_542 | spellTimeout |  | ins_442 | spellTimeout |  | mapped |
| ins_545 | laserCancel |  | ins_445 | laserCancel |  | mapped |
| ins_546 | bombShield | SS | ins_446 | bombShield | Sf | mapped |
| ins_547 | gameSpeed | f | ins_447 | gameSpeed | f | mapped |
| ins_548 | diffWait | SSSS | ins_448 | diffWait | SSSS | mapped |
| ins_552 | zIndex | S | ins_452 | zIndex | f | same-name-unmapped |
| ins_553 | hitSound | S | ins_453 | hitSound | S | mapped |
| ins_554 | stageLogo |  | ins_454 | stageLogo |  | mapped |
| ins_555 | enmAlive | SS | ins_455 | enmAlive | SS | mapped |
| ins_556 | setDeath | m | ins_456 | storeCoords | ffS | mapped |
| ins_557 | fogTime | SSSff |  |  |  | no-same-name |
| ins_558 | flagMirror | S |  |  |  | no-same-name |
| ins_559 | enmLimit | S |  |  |  | no-same-name |
| ins_561 | die |  |  |  |  | no-same-name |
| ins_562 | dropItemsSp | S |  |  |  | no-same-name |
| ins_564 | hitboxRotate | f |  |  |  | no-same-name |
| ins_565 | bombInvuln | f |  |  |  | no-same-name |
| ins_568 | spellMode | S |  |  |  | no-same-name |
| ins_600 | etNew | S | ins_500 | etNew | S | mapped |
| ins_601 | etOn | S | ins_501 | etOn | S | mapped |
| ins_602 | etSprite | SSS | ins_502 | etSprite | SSS | mapped |
| ins_603 | etOffset | Sff | ins_503 | etOffset | Sff | mapped |
| ins_604 | etAngle | Sff | ins_504 | etAngle | Sff | mapped |
| ins_605 | etSpeed | Sff | ins_505 | etSpeed | Sff | mapped |
| ins_606 | etCount | SSS | ins_506 | etCount | SSS | mapped |
| ins_607 | etAim | SS | ins_507 | etAim | SS | mapped |
| ins_608 | etSound | SSS | ins_508 | etSound | SSS | mapped |
| ins_609 | etExSet | SSSSSSff | ins_509 | etEx | SSSSSSff | mapped |
| ins_610 | etExSet2 | SSSSSSSSffff |  |  |  | no-same-name |
| ins_611 | etEx | SSSSSff | ins_509 | etEx | SSSSSSff | same-name-unmapped |
| ins_612 | etEx2 | SSSSSSSffff |  |  |  | no-same-name |
| ins_613 | etClearAll |  | ins_510 | etClearAll |  | mapped |
| ins_614 | etCopy | SS | ins_511 | etCopy | SS | mapped |
| ins_615 | etCancel | f | ins_512 | etCancel | f | mapped |
| ins_616 | etClear | f | ins_513 | etClear | f | mapped |
| ins_617 | etSpeedR3 | Sffffff | ins_514 | etSpeedR3 | Sffffff | mapped |
| ins_618 | etSpeedR5 | Sffffffffff | ins_515 | etSpeedR5 | Sffffffffff | mapped |
| ins_619 | etSpeedR2 | Sffff | ins_516 | etSpeedR2 | Sffff | mapped |
| ins_620 | etCountR3 | SSSSSSS | ins_517 | etCountR3 | SSSSSSS | mapped |
| ins_621 | etCountR5 | SSSSSSSSSSS |  |  |  | no-same-name |
| ins_622 | etCountR2 | SSSSS | ins_519 | etCountR2 | SSSSS | mapped |
| ins_623 | angleToPlayer | fff | ins_520 | angleToPlayer | fff | mapped |
| ins_624 | etSpeedD | Sffffffff | ins_521 | etSpeedD | Sffffffff | mapped |
| ins_625 | etCountD | SSSSSSSSS | ins_522 | etCountD | SSSSSSSSS | mapped |
| ins_626 | etOffsetRad | Sff | ins_523 | etOffsetRad | Sff | mapped |
| ins_627 | etDist | Sf | ins_524 | etDist | Sf | mapped |
| ins_628 | etOffsetAbs | Sff | ins_525 | etOffsetAbs | Sff | mapped |
| ins_629 | fog | fS | ins_526 | fog | fS | mapped |
| ins_630 | callSTD | S | ins_527 | callSTD |  | same-name-unmapped |

## th12 -> th15
| source | name | sig | mapped | target name | target sig | status |
| --- | --- | --- | --- | --- | --- | --- |
| ins_256 | enmCreate | mffSSS | ins_300 | enmCreate | mffSSS | mapped |
| ins_257 | enmCreateA | mffSSS | ins_301 | enmCreateA | mffSSS | mapped |
| ins_258 | anmSelect | S | ins_302 | anmSelect | S | mapped |
| ins_259 | anmSetSprite | SS | ins_303 | anmSetSprite | SS | mapped |
| ins_260 | enmCreateM | mffSSS | ins_304 | enmCreateM | mffSSS | mapped |
| ins_261 | enmCreateAM | mffSSS | ins_305 | enmCreateAM | mffSSS | mapped |
| ins_262 | anmSetMain | SS | ins_306 | anmSetMain | SS | mapped |
| ins_263 | anmPlay | SS | ins_307 | anmPlay | SS | mapped |
| ins_264 | anmPlayAbs | SS | ins_308 | anmPlayAbs | SS | mapped |
| ins_265 | enmCreateF | mffSSS | ins_309 | enmCreateF | mffSSS | mapped |
| ins_266 | enmCreateAF | mffSSS | ins_310 | enmCreateAF | mffSSS | mapped |
| ins_267 | enmCreateMF | mffSSS | ins_311 | enmCreateMF | mffSSS | mapped |
| ins_268 | enmCreateAMF | mffSSS | ins_312 | enmCreateAMF | mffSSS | mapped |
| ins_269 | anmSelectedPlay | S | ins_313 | anmSelectedPlay | S | mapped |
| ins_270 | enmCreate270 | mffSSSS |  |  |  | no-same-name |
| ins_271 | enmCreate271 | mffSSSS |  |  |  | no-same-name |
| ins_272 | anmPlayHigh | SS | ins_314 | anmPlayHigh | SS | mapped |
| ins_273 | anmPlayRotate | SSf | ins_315 | anmPlayRotate | SSf | mapped |
| ins_274 | anmOnEt | SS |  |  |  | no-same-name |
| ins_275 | anmSwitch | SS | ins_317 | anmSwitch | SS | mapped |
| ins_276 | anmReset |  | ins_318 | anmReset |  | mapped |
| ins_277 | anmRotate | Sf | ins_319 | anmRotate | Sf | mapped |
| ins_278 | anmScale | Sff | ins_329 | anmScale | Sff | mapped |
| ins_279 | anmMove | Sff | ins_320 | anmMove | Sff | mapped |
| ins_280 | enmMapleEnemy | mSSSSS | ins_321 | enmMapleEnemy | mffSSS | same-name-unmapped |
| ins_281 | byakurenButterfly | SS |  |  |  | no-same-name |
| ins_282 | anmOnPhoto | SS |  |  |  | no-same-name |
| ins_300 | movePos | ff | ins_400 | movePos | ff | mapped |
| ins_301 | movePosTime | SSff | ins_401 | movePosTime | SSff | mapped |
| ins_302 | movePosRel | ff | ins_402 | movePosRel | ff | mapped |
| ins_303 | movePosRelTime | SSff | ins_403 | movePosRelTime | SSff | mapped |
| ins_304 | moveVel | ff | ins_404 | moveVel | ff | mapped |
| ins_305 | moveVelTime | SSff | ins_405 | moveVelTime | SSff | mapped |
| ins_306 | moveVelRel | ff | ins_406 | moveVelRel | ff | mapped |
| ins_307 | moveVelRelTime | SSff | ins_407 | moveVelRelTime | SSff | mapped |
| ins_308 | moveCircle | ffff | ins_408 | moveCircle | ffff | mapped |
| ins_309 | moveCircleTime | SSfff | ins_409 | moveCircleTime | SSfff | mapped |
| ins_310 | moveCircleRel | ffff | ins_410 | moveCircleRel | ffff | mapped |
| ins_311 | moveCircleRelTime | SSfff | ins_411 | moveCircleRelTime | SSfff | mapped |
| ins_312 | moveRand | SSf | ins_412 | moveRand | SSf | mapped |
| ins_313 | moveRandRel | SSf | ins_413 | moveRandRel | SSf | mapped |
| ins_314 | moveBoss |  | ins_414 | moveBoss |  | mapped |
| ins_315 | moveBossRel |  | ins_415 | moveBossRel |  | mapped |
| ins_316 | movePos3d | ff | ins_416 | movePos3d | fff | same-name-unmapped |
| ins_317 | movePos3dRel | fff | ins_417 | movePos3dRel | fff | mapped |
| ins_318 | moveAdd | ff | ins_418 | moveAdd | ff | mapped |
| ins_319 | moveAddRel | ff |  |  |  | no-same-name |
| ins_320 | moveEllipse | ffffff | ins_420 | moveEllipse | ffffff | mapped |
| ins_321 | moveEllipseTime | SSfffff | ins_421 | moveEllipseTime | SSfffff | mapped |
| ins_322 | moveEllipseRel | ffffff | ins_422 | moveEllipseRel | ffffff | mapped |
| ins_323 | moveEllipseRelTime | SSfffff | ins_423 | moveEllipseRelTime | SSfffff | mapped |
| ins_324 | moveSetMirror | S | ins_424 | moveSetMirror | S | mapped |
| ins_325 | moveBezier | Sffffff | ins_425 | moveBezier | Sffffff | mapped |
| ins_326 | moveBezierRel | Sffffff | ins_426 | moveBezierRel | Sffffff | mapped |
| ins_327 | moveReset |  | ins_427 | moveReset |  | mapped |
| ins_328 | moveVelNM | ff | ins_428 | moveVelNM | ff | mapped |
| ins_329 | moveVelNMTime | Sfff | ins_429 | moveVelNMTime | SSff | same-name-unmapped |
| ins_330 | moveVelNMRel | ff | ins_430 | moveVelNMRel | ff | mapped |
| ins_331 | moveVelNMRelTime | SSff | ins_431 | moveVelNMRelTime | SSff | mapped |
| ins_332 | move432 | S |  |  |  | no-same-name |
| ins_333 | move433 | S |  |  |  | no-same-name |
| ins_400 | setHurtbox | ff | ins_500 | setHurtbox | ff | mapped |
| ins_401 | setHitbox | ff | ins_501 | setHitbox | ff | mapped |
| ins_402 | flagSet | S | ins_502 | flagSet | S | mapped |
| ins_403 | flagClear | S | ins_503 | flagClear | S | mapped |
| ins_404 | moveLimit | ffff | ins_504 | moveLimit | ffff | mapped |
| ins_405 | moveLimitReset |  | ins_505 | moveLimitReset |  | mapped |
| ins_406 | dropClear |  | ins_506 | dropClear |  | mapped |
| ins_407 | dropExtra | SS | ins_507 | dropExtra | SS | mapped |
| ins_408 | dropArea | ff | ins_508 | dropArea | ff | mapped |
| ins_409 | dropItems |  | ins_509 | dropItems |  | mapped |
| ins_410 | dropMain | S | ins_510 | dropMain | S | mapped |
| ins_411 | lifeSet | S | ins_511 | lifeSet | S | mapped |
| ins_412 | setBoss | S | ins_512 | setBoss | S | mapped |
| ins_413 | timerReset |  | ins_513 | timerReset |  | mapped |
| ins_414 | setInterrupt | SSSm | ins_514 | setInterrupt | SSSm | mapped |
| ins_415 | setInvuln | S | ins_515 | setInvuln | S | mapped |
| ins_416 | playSound | S | ins_516 | playSound | S | mapped |
| ins_417 | setScreenShake | SSS | ins_517 | setScreenShake | SSS | mapped |
| ins_418 | dialogRead | S | ins_518 | dialogRead | S | mapped |
| ins_419 | dialogWait |  | ins_519 | dialogWait |  | mapped |
| ins_420 | deathWait |  | ins_520 | bossWait |  | mapped |
| ins_421 | setTimeout | Sm | ins_521 | setTimeout | Sm | mapped |
| ins_422 | spellEx | SSSx | ins_522 | spellEx | SSSm | mapped |
| ins_423 | spellEnd |  | ins_523 | spellEnd |  | mapped |
| ins_424 | setChapter | S | ins_524 | setChapter | S | mapped |
| ins_425 | enmKillAll |  | ins_525 | enmKillAll |  | mapped |
| ins_426 | etProtectRange | f | ins_526 | etProtectRange | f | mapped |
| ins_427 | lifeMarker | SfS | ins_527 | lifeMarker | SfS | mapped |
| ins_428 | spellUnused | SSSx | ins_528 | spellUnused | SSSm | mapped |
| ins_429 | rankF3 | ffff | ins_529 | rankF3 | ffff | mapped |
| ins_430 | rankF5 | ffffff | ins_530 | rankF5 | ffffff | mapped |
| ins_431 | rankF2 | fff | ins_531 | rankF2 | fff | mapped |
| ins_432 | rankI3 | SSSS | ins_532 | rankI3 | SSSS | mapped |
| ins_433 | rankI5 | SSSSSS | ins_533 | rankI5 | SSSSSS | mapped |
| ins_434 | rankI2 | SSS | ins_534 | rankI2 | SSS | mapped |
| ins_435 | diffI | SSSSS | ins_535 | diffI | SSSSS | mapped |
| ins_436 | diffF | fffff | ins_536 | diffF | fffff | mapped |
| ins_437 | spell | SSSx | ins_537 | spell | SSSm | mapped |
| ins_438 | spell2 | SSSx | ins_538 | spell2 | SSSm | mapped |
| ins_439 | spell3 | SSSx | ins_539 | spell3 | SSSm | mapped |
| ins_440 | stars | S | ins_540 | stars | S | mapped |
| ins_442 | spellTimeout |  | ins_542 | spellTimeout |  | mapped |
| ins_445 | laserCancel |  | ins_545 | laserCancel |  | mapped |
| ins_446 | bombShield | Sf | ins_546 | bombShield | SS | mapped |
| ins_447 | gameSpeed | f | ins_547 | gameSpeed | f | mapped |
| ins_448 | diffWait | SSSS | ins_548 | diffWait | SSSS | mapped |
| ins_452 | zIndex | f | ins_552 | zIndex | S | same-name-unmapped |
| ins_453 | hitSound | S | ins_553 | hitSound | S | mapped |
| ins_454 | stageLogo |  | ins_554 | stageLogo |  | mapped |
| ins_455 | enmAlive | SS | ins_555 | enmAlive | SS | mapped |
| ins_456 | storeCoords | ffS | ins_556 | setDeath | m | mapped |
| ins_458 | DS_timer | S |  |  |  | no-same-name |
| ins_459 | DS_nice | S |  |  |  | no-same-name |
| ins_460 | DS_scoreMult | f |  |  |  | no-same-name |
| ins_500 | etNew | S | ins_600 | etNew | S | mapped |
| ins_501 | etOn | S | ins_601 | etOn | S | mapped |
| ins_502 | etSprite | SSS | ins_602 | etSprite | SSS | mapped |
| ins_503 | etOffset | Sff | ins_603 | etOffset | Sff | mapped |
| ins_504 | etAngle | Sff | ins_604 | etAngle | Sff | mapped |
| ins_505 | etSpeed | Sff | ins_605 | etSpeed | Sff | mapped |
| ins_506 | etCount | SSS | ins_606 | etCount | SSS | mapped |
| ins_507 | etAim | SS | ins_607 | etAim | SS | mapped |
| ins_508 | etSound | SSS | ins_608 | etSound | SSS | mapped |
| ins_509 | etEx | SSSSSSff | ins_609 | etExSet | SSSSSSff | mapped |
| ins_510 | etClearAll |  | ins_613 | etClearAll |  | mapped |
| ins_511 | etCopy | SS | ins_614 | etCopy | SS | mapped |
| ins_512 | etCancel | f | ins_615 | etCancel | f | mapped |
| ins_513 | etClear | f | ins_616 | etClear | f | mapped |
| ins_514 | etSpeedR3 | Sffffff | ins_617 | etSpeedR3 | Sffffff | mapped |
| ins_515 | etSpeedR5 | Sffffffffff | ins_618 | etSpeedR5 | Sffffffffff | mapped |
| ins_516 | etSpeedR2 | Sffff | ins_619 | etSpeedR2 | Sffff | mapped |
| ins_517 | etCountR3 | SSSSSSS | ins_620 | etCountR3 | SSSSSSS | mapped |
| ins_519 | etCountR2 | SSSSS | ins_622 | etCountR2 | SSSSS | mapped |
| ins_520 | angleToPlayer | fff | ins_623 | angleToPlayer | fff | mapped |
| ins_521 | etSpeedD | Sffffffff | ins_624 | etSpeedD | Sffffffff | mapped |
| ins_522 | etCountD | SSSSSSSSS | ins_625 | etCountD | SSSSSSSSS | mapped |
| ins_523 | etOffsetRad | Sff | ins_626 | etOffsetRad | Sff | mapped |
| ins_524 | etDist | Sf | ins_627 | etDist | Sf | mapped |
| ins_525 | etOffsetAbs | Sff | ins_628 | etOffsetAbs | Sff | mapped |
| ins_526 | fog | fS | ins_629 | fog | fS | mapped |
| ins_527 | callSTD |  | ins_630 | callSTD | S | same-name-unmapped |
| ins_528 | lifeHide |  | ins_631 | lifeHide | S | same-name-unmapped |
| ins_529 | funcSet | S | ins_632 | funcSet | S | mapped |
| ins_530 | flagExtDmg | S | ins_633 | flagExtDmg | S | mapped |
| ins_532 | etCancel2 | f | ins_635 | etCancel2 | f | mapped |
| ins_533 | etClear2 | f | ins_636 | etClear2 | f | mapped |
| ins_534 | funcCall | S | ins_637 | funcCall | S | mapped |
| ins_600 | laserNew | Sffff | ins_700 | laserNew | Sffff | mapped |
| ins_601 | laserTiming | SSSSSS | ins_701 | laserTiming | SSSSSS | mapped |
| ins_602 | laserOn | S | ins_702 | laserOn | S | mapped |
| ins_603 | laserStOn | SS | ins_703 | laserStOn | SS | mapped |
| ins_604 | laserOffset | Sff | ins_704 | laserOffset | Sff | mapped |
| ins_605 | laserTrajectory | Sff | ins_705 | laserTrajectory | Sff | mapped |
| ins_606 | laserStLength | Sf | ins_706 | laserStLength | Sf | mapped |
| ins_607 | laserStWidth | Sf | ins_707 | laserStWidth | Sf | mapped |
| ins_608 | laserStAngle | Sf | ins_708 | laserStAngle | Sf | mapped |
| ins_609 | laserStRotation | Sf | ins_709 | laserStRotation | Sf | mapped |
| ins_610 | laserStEnd | S | ins_710 | laserStEnd | S | mapped |
| ins_611 | laserCuOn | S | ins_711 | laserCuOn | S | mapped |
| ins_612 | hitboxRect | ff |  |  |  | no-same-name |

## th12 -> th10
| source | name | sig | mapped | target name | target sig | status |
| --- | --- | --- | --- | --- | --- | --- |
| ins_256 | enmCreate | mffSSS | ins_256 |  | mffSSS | mapped |
| ins_257 | enmCreateA | mffSSS | ins_257 |  | mffSSS | mapped |
| ins_258 | anmSelect | S | ins_258 |  | S | mapped |
| ins_259 | anmSetSprite | SS | ins_259 |  | SS | mapped |
| ins_260 | enmCreateM | mffSSS | ins_260 |  | mffSSS | mapped |
| ins_261 | enmCreateAM | mffSSS | ins_261 |  | mffSSS | mapped |
| ins_262 | anmSetMain | SS | ins_262 |  | SS | mapped |
| ins_263 | anmPlay | SS | ins_263 |  | SS | mapped |
| ins_264 | anmPlayAbs | SS | ins_264 |  | SS | mapped |
| ins_265 | enmCreateF | mffSSS | ins_265 |  | mffSSS | mapped |
| ins_266 | enmCreateAF | mffSSS | ins_266 |  | mffSSS | mapped |
| ins_267 | enmCreateMF | mffSSS | ins_267 |  | mffSSS | mapped |
| ins_268 | enmCreateAMF | mffSSS | ins_268 |  | mffSSS | mapped |
| ins_269 | anmSelectedPlay | S |  |  |  | no-same-name |
| ins_270 | enmCreate270 | mffSSSS |  |  |  | no-same-name |
| ins_271 | enmCreate271 | mffSSSS |  |  |  | no-same-name |
| ins_272 | anmPlayHigh | SS |  |  |  | no-same-name |
| ins_273 | anmPlayRotate | SSf |  |  |  | no-same-name |
| ins_274 | anmOnEt | SS |  |  |  | no-same-name |
| ins_275 | anmSwitch | SS |  |  |  | no-same-name |
| ins_276 | anmReset |  |  |  |  | no-same-name |
| ins_277 | anmRotate | Sf |  |  |  | no-same-name |
| ins_278 | anmScale | Sff |  |  |  | no-same-name |
| ins_279 | anmMove | Sff |  |  |  | no-same-name |
| ins_280 | enmMapleEnemy | mSSSSS |  |  |  | no-same-name |
| ins_281 | byakurenButterfly | SS |  |  |  | no-same-name |
| ins_282 | anmOnPhoto | SS |  |  |  | no-same-name |
| ins_300 | movePos | ff |  |  |  | no-same-name |
| ins_301 | movePosTime | SSff |  |  |  | no-same-name |
| ins_302 | movePosRel | ff |  |  |  | no-same-name |
| ins_303 | movePosRelTime | SSff |  |  |  | no-same-name |
| ins_304 | moveVel | ff |  |  |  | no-same-name |
| ins_305 | moveVelTime | SSff |  |  |  | no-same-name |
| ins_306 | moveVelRel | ff |  |  |  | no-same-name |
| ins_307 | moveVelRelTime | SSff |  |  |  | no-same-name |
| ins_308 | moveCircle | ffff |  |  |  | no-same-name |
| ins_309 | moveCircleTime | SSfff |  |  |  | no-same-name |
| ins_310 | moveCircleRel | ffff |  |  |  | no-same-name |
| ins_311 | moveCircleRelTime | SSfff |  |  |  | no-same-name |
| ins_312 | moveRand | SSf |  |  |  | no-same-name |
| ins_313 | moveRandRel | SSf |  |  |  | no-same-name |
| ins_314 | moveBoss |  |  |  |  | no-same-name |
| ins_315 | moveBossRel |  |  |  |  | no-same-name |
| ins_316 | movePos3d | ff |  |  |  | no-same-name |
| ins_317 | movePos3dRel | fff |  |  |  | no-same-name |
| ins_318 | moveAdd | ff |  |  |  | no-same-name |
| ins_319 | moveAddRel | ff |  |  |  | no-same-name |
| ins_320 | moveEllipse | ffffff |  |  |  | no-same-name |
| ins_321 | moveEllipseTime | SSfffff |  |  |  | no-same-name |
| ins_322 | moveEllipseRel | ffffff |  |  |  | no-same-name |
| ins_323 | moveEllipseRelTime | SSfffff |  |  |  | no-same-name |
| ins_324 | moveSetMirror | S |  |  |  | no-same-name |
| ins_325 | moveBezier | Sffffff |  |  |  | no-same-name |
| ins_326 | moveBezierRel | Sffffff |  |  |  | no-same-name |
| ins_327 | moveReset |  |  |  |  | no-same-name |
| ins_328 | moveVelNM | ff |  |  |  | no-same-name |
| ins_329 | moveVelNMTime | Sfff |  |  |  | no-same-name |
| ins_330 | moveVelNMRel | ff |  |  |  | no-same-name |
| ins_331 | moveVelNMRelTime | SSff |  |  |  | no-same-name |
| ins_332 | move432 | S |  |  |  | no-same-name |
| ins_333 | move433 | S |  |  |  | no-same-name |
| ins_400 | setHurtbox | ff |  |  |  | no-same-name |
| ins_401 | setHitbox | ff |  |  |  | no-same-name |
| ins_402 | flagSet | S |  |  |  | no-same-name |
| ins_403 | flagClear | S |  |  |  | no-same-name |
| ins_404 | moveLimit | ffff |  |  |  | no-same-name |
| ins_405 | moveLimitReset |  |  |  |  | no-same-name |
| ins_406 | dropClear |  |  |  |  | no-same-name |
| ins_407 | dropExtra | SS |  |  |  | no-same-name |
| ins_408 | dropArea | ff |  |  |  | no-same-name |
| ins_409 | dropItems |  |  |  |  | no-same-name |
| ins_410 | dropMain | S |  |  |  | no-same-name |
| ins_411 | lifeSet | S |  |  |  | no-same-name |
| ins_412 | setBoss | S |  |  |  | no-same-name |
| ins_413 | timerReset |  |  |  |  | no-same-name |
| ins_414 | setInterrupt | SSSm |  |  |  | no-same-name |
| ins_415 | setInvuln | S |  |  |  | no-same-name |
| ins_416 | playSound | S |  |  |  | no-same-name |
| ins_417 | setScreenShake | SSS |  |  |  | no-same-name |
| ins_418 | dialogRead | S |  |  |  | no-same-name |
| ins_419 | dialogWait |  |  |  |  | no-same-name |
| ins_420 | deathWait |  |  |  |  | no-same-name |
| ins_421 | setTimeout | Sm |  |  |  | no-same-name |
| ins_422 | spellEx | SSSx |  |  |  | no-same-name |
| ins_423 | spellEnd |  |  |  |  | no-same-name |
| ins_424 | setChapter | S |  |  |  | no-same-name |
| ins_425 | enmKillAll |  |  |  |  | no-same-name |
| ins_426 | etProtectRange | f |  |  |  | no-same-name |
| ins_427 | lifeMarker | SfS |  |  |  | no-same-name |
| ins_428 | spellUnused | SSSx |  |  |  | no-same-name |
| ins_429 | rankF3 | ffff |  |  |  | no-same-name |
| ins_430 | rankF5 | ffffff |  |  |  | no-same-name |
| ins_431 | rankF2 | fff |  |  |  | no-same-name |
| ins_432 | rankI3 | SSSS |  |  |  | no-same-name |
| ins_433 | rankI5 | SSSSSS |  |  |  | no-same-name |
| ins_434 | rankI2 | SSS |  |  |  | no-same-name |
| ins_435 | diffI | SSSSS |  |  |  | no-same-name |
| ins_436 | diffF | fffff |  |  |  | no-same-name |
| ins_437 | spell | SSSx |  |  |  | no-same-name |
| ins_438 | spell2 | SSSx |  |  |  | no-same-name |
| ins_439 | spell3 | SSSx |  |  |  | no-same-name |
| ins_440 | stars | S |  |  |  | no-same-name |
| ins_442 | spellTimeout |  |  |  |  | no-same-name |
| ins_445 | laserCancel |  |  |  |  | no-same-name |
| ins_446 | bombShield | Sf |  |  |  | no-same-name |
| ins_447 | gameSpeed | f |  |  |  | no-same-name |
| ins_448 | diffWait | SSSS |  |  |  | no-same-name |
| ins_452 | zIndex | f |  |  |  | no-same-name |
| ins_453 | hitSound | S |  |  |  | no-same-name |
| ins_454 | stageLogo |  |  |  |  | no-same-name |
| ins_455 | enmAlive | SS |  |  |  | no-same-name |
| ins_456 | storeCoords | ffS |  |  |  | no-same-name |
| ins_458 | DS_timer | S |  |  |  | no-same-name |
| ins_459 | DS_nice | S |  |  |  | no-same-name |
| ins_460 | DS_scoreMult | f |  |  |  | no-same-name |
| ins_500 | etNew | S |  |  |  | no-same-name |
| ins_501 | etOn | S |  |  |  | no-same-name |
| ins_502 | etSprite | SSS |  |  |  | no-same-name |
| ins_503 | etOffset | Sff |  |  |  | no-same-name |
| ins_504 | etAngle | Sff |  |  |  | no-same-name |
| ins_505 | etSpeed | Sff |  |  |  | no-same-name |
| ins_506 | etCount | SSS |  |  |  | no-same-name |
| ins_507 | etAim | SS |  |  |  | no-same-name |
| ins_508 | etSound | SSS |  |  |  | no-same-name |
| ins_509 | etEx | SSSSSSff |  |  |  | no-same-name |
| ins_510 | etClearAll |  |  |  |  | no-same-name |
| ins_511 | etCopy | SS |  |  |  | no-same-name |
| ins_512 | etCancel | f |  |  |  | no-same-name |
| ins_513 | etClear | f |  |  |  | no-same-name |
| ins_514 | etSpeedR3 | Sffffff |  |  |  | no-same-name |
| ins_515 | etSpeedR5 | Sffffffffff |  |  |  | no-same-name |
| ins_516 | etSpeedR2 | Sffff |  |  |  | no-same-name |
| ins_517 | etCountR3 | SSSSSSS |  |  |  | no-same-name |
| ins_519 | etCountR2 | SSSSS |  |  |  | no-same-name |
| ins_520 | angleToPlayer | fff |  |  |  | no-same-name |
| ins_521 | etSpeedD | Sffffffff |  |  |  | no-same-name |
| ins_522 | etCountD | SSSSSSSSS |  |  |  | no-same-name |
| ins_523 | etOffsetRad | Sff |  |  |  | no-same-name |
| ins_524 | etDist | Sf |  |  |  | no-same-name |
| ins_525 | etOffsetAbs | Sff |  |  |  | no-same-name |
| ins_526 | fog | fS |  |  |  | no-same-name |
| ins_527 | callSTD |  |  |  |  | no-same-name |
| ins_528 | lifeHide |  |  |  |  | no-same-name |
| ins_529 | funcSet | S |  |  |  | no-same-name |
| ins_530 | flagExtDmg | S |  |  |  | no-same-name |
| ins_532 | etCancel2 | f |  |  |  | no-same-name |
| ins_533 | etClear2 | f |  |  |  | no-same-name |
| ins_534 | funcCall | S |  |  |  | no-same-name |
| ins_600 | laserNew | Sffff |  |  |  | no-same-name |
| ins_601 | laserTiming | SSSSSS |  |  |  | no-same-name |
| ins_602 | laserOn | S |  |  |  | no-same-name |
| ins_603 | laserStOn | SS |  |  |  | no-same-name |
| ins_604 | laserOffset | Sff |  |  |  | no-same-name |
| ins_605 | laserTrajectory | Sff |  |  |  | no-same-name |
| ins_606 | laserStLength | Sf |  |  |  | no-same-name |
| ins_607 | laserStWidth | Sf |  |  |  | no-same-name |
| ins_608 | laserStAngle | Sf |  |  |  | no-same-name |
| ins_609 | laserStRotation | Sf |  |  |  | no-same-name |
| ins_610 | laserStEnd | S |  |  |  | no-same-name |
| ins_611 | laserCuOn | S |  |  |  | no-same-name |
| ins_612 | hitboxRect | ff |  |  |  | no-same-name |

## th10 -> th12
| source | name | sig | mapped | target name | target sig | status |
| --- | --- | --- | --- | --- | --- | --- |

