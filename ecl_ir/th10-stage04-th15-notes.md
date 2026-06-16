# TH10 Stage04 -> TH15 Fix Notes

## Problems

1. TH10 laser objects did not appear in TH15 output.
2. Stage 4 background/helper enemies, including the first spawned group, did not appear after conversion.

## Root Causes

- `lift_lasers()` only recognized TH12 and TH13+ laser opcode families. TH10/TH11 laser opcodes such as `412 laserOnA`, `413 laserStOn`, `428 laserOn`, and `429 laserStOn2` were never lifted as `LaserEmitter` objects.
- TH10 opcode `270 enmCreate270` was mapped to `enemy.create_legacy270`, but this op_key was listed in `SOURCE_SPECIFIC_DROP_OP_KEYS`, so the generated TH15 script emitted only comments and dropped every `DiveEnemy*` background/helper spawn.

## Fixes

- Added TH10/TH11 laser lifting for opcodes `412, 413, 414, 415, 416, 417, 418, 419, 428, 429`.
- Added a `legacy_laser_on_aimed` lowering policy for TH10/TH11 `laser.on_aimed`:
  - TH15 approximation: `ins_700`, `ins_701`, `ins_708`, `ins_702`.
  - TH12 approximation: `ins_600`, `ins_601`, `ins_608`, `ins_602`.
- Removed `enemy.create_legacy270` from source-specific drops.
- Lowered `enemy.create_legacy270` to target `enemy.create_func`, dropping the legacy-only fourth argument.

## Current Caveats

- TH10 `laserOnA` contains old-generation behavior not fully represented in TH15. The current lowering preserves angle, length, width, and lifetime, but it is still an approximation.
- TH10 `enmCreate270` has a legacy runtime flag argument; the current lowering drops it and uses target func-create so the background/helper enemy appears.

## Validation

- `th062/th10/stage04.decl` now lifts 2 `LaserEmitter` objects.
- `th062/ecl_ir_out/th10_to_th15_package/st04.decl` contains TH15 laser instructions for the two stage 4 boss lasers.
- `DiveEnemy*` background/helper spawns now lower to `ins_309(...)` instead of unsupported/drop comments.
- Direct transpile and `emit-ir + compile-ir` output are byte-identical for this file.
- `wine thtkGUI-th20tr/thtk/thtk12/thecl.exe -c 15 th062/ecl_ir_out/th10_to_th15_package/st04.decl /tmp/th10_stage04_to_th15_new.ecl` succeeds.
