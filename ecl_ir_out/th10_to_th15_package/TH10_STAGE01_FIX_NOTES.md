# TH10 stage01 -> TH15 st01 first-waves fix notes

## Symptom

The converted `st01.decl` could crash when the first enemy of the third early wave appears. In the source this is the first `ins_261("RGirl00", 144.0f, -64.0f, 20, 1000, 1)` at TH10 `stage01.decl` line 1823.

## Cause

The source IR already lifted TH10 enemy creation correctly:

- `257` -> `enemy.create_abs`, absolute-position create.
- `261` -> `enemy.create_abs_mirror`, absolute-position mirrored create.
- `create.position_mode` was `absolute`, and `create.mirror` was preserved.

The backend then overwrote stage enemy create semantics using only the mirror flag:

- non-mirror absolute creates became TH15 `ins_300` instead of `ins_301`.
- mirror absolute creates became TH15 `ins_304` instead of `ins_305`.

That means x/y from TH10 absolute spawns were interpreted as relative offsets in TH15. The third wave starts with mirrored spawns on the right side, so the wrong relative/mirror create was a strong crash trigger.

A second lossy mapping collapsed TH10 create item policy `2`/`3` into TH15 `1`. This is not the same namespace as explicit drop-type opcodes and changes spawn/drop presets used by the early waves.

## Fix

- `backend.enemy_create_op_key_for_target()` now chooses among all four semantic axes: relative/absolute and normal/mirror (`create`, `create_abs`, `create_mirror`, `create_abs_mirror`).
- `semantics.remap_create_item_policy()` now preserves raw TH10 create item policy values when targeting TH13+ instead of collapsing every nonzero value to `1`.

## Verified early-wave mapping

The fixed `st01.decl` now maps the early waves as follows:

- First loop wave: TH10 `257` -> TH15 `301`, preserving `item=2/1/3` and 20-frame loop interval.
- Second five enemies: TH10 `257/261` -> TH15 `301/305`, preserving absolute coordinates, mirror behavior, and item values.
- Third five enemies: TH10 `261/257` -> TH15 `305/301`, preserving absolute coordinates, mirror behavior, and item values.

`wine thtkGUI-th20tr/thtk/thtk12/thecl.exe -c 15 st01.decl st01.ecl` succeeds for the regenerated package file.

## Follow-up: `async 0` calls and variable suspicion

A second audit checked whether `%A`/`$A`-style variables were simply missing from function declarations. A function scan found no undeclared `%/$` local names in the regenerated file.

However, the parser previously failed to recognize calls of the form `@Girl01_at() async 0;` and treated them as raw comments. In TH10 stage01 these calls are used by `Girl01` and `Girl02`; `Girl01` appears immediately before the third early wave. Dropping the async slot call removes the enemy's bullet child task and can leave behavior/state diverging right before the reported crash point.

The parser now accepts `async <slot>` and the emitter preserves it. The regenerated file contains:

- `@Girl01_at() async 0;`
- `@Girl02_at() async 0;`

The package `st01.ecl` was recompiled successfully after this fix.

## 2026-06-15 variable/dynamic-emitter-order fix

Crash around the first enemy of the third early wave was not caused by missing declarations for `%A/%B` or `$A/$B`; a scan of `st01.decl` reports zero undeclared `%/$` local uses.

Root cause found in `Girl01_at`: TH10 source has a dynamic bullet count update inside the loop:

```decl
$A = 1;
...
Girl01_at_484:
    ins_406(0, $A, 1);
    ins_401(0);
    ins_83($C);
    $A = $A + 1;
```

The previous lifter merged the later `ins_406(0, $A, 1)` into the BulletEmitter definition, so TH15 emitted `ins_606(0, $A, 1)` before `$A = 1`. This could read an uninitialized local and also changed the flower/fan expansion sequence.

Fixes:
- `th062/ecl_ir/lifter.py`: `definition_state` now uses only the contiguous emitter setup prefix; TH10/11 emitters now get this prefix snapshot too.
- `th062/ecl_ir/semantics.py`: TH10/11 slot BulletEmitter coverage policy is now `contiguous_setup_prefix`, so dynamic config instructions after labels/gaps are preserved in timeline order.
- Regenerated `th062/ecl_ir_out/th10_to_th15_package/st01.decl`; `Girl01_at` now emits definition `ins_606(0, 1, 1)` first, then loop-local `ins_606(0, $A, 1)` immediately before `ins_601(0)`.
- Recompiled with `wine thtkGUI-th20tr/thtk/thtk12/thecl.exe -c 15`; output `st01.ecl` was produced successfully.

## 2026-06-15 stage enemy ANM slot fix

Runtime still crashed and the 4th/5th enemies in the early five-enemy wave were invisible. Those enemies are `BGirl00` and `GGirl00` wrappers.

Root cause: TH10/11 opcode `262` is `anmSetMain(slot, script)`, but the object lifter was incorrectly rewriting `anmSetMain` with non-zero slot to `anmSetSprite`. Thus TH10 stage enemy main scripts `45/46/47/48` were lowered as TH15 sprite script `93`, a boss/stage sprite overlay used differently by native TH15, instead of using the child `Girl00(arg)` main script path.

Fixes:
- `th062/ecl_ir/object_lifter.py`: no longer rewrites `anmSetMain(slot != 0)` into `anmSetSprite`.
- `th062/ecl_ir/backend.py`: for TH10/11 stage wrappers targeting TH13+, drops wrapper-only non-zero-slot main ANM setup; the called child sub (`Girl00(0/5/35/40)`) now sets the target slot-0 main script.
- Regenerated `st01.decl`: `BGirl00/GGirl00/RGirl00/YGirl00` wrappers no longer emit `ins_303(1, 93)` or `ins_306(..., -1)`; `Girl00(var A)` emits `ins_306(0, $A)`.
- Verified all numeric TH15 stage bank-2 `ins_303/ins_306` refs in the regenerated file exist in the ANM catalog; count of invalid refs is 0.
- Recompiled with `wine thtkGUI-th20tr/thtk/thtk12/thecl.exe -c 15`; output `st01.ecl` was produced successfully.

## 2026-06-15 native TH15 stage1 ANM combo fix

The previous stage enemy ANM fix still allowed catalog-valid combinations instead of strictly using combinations observed in native TH15 `st01.decl`. The mapping is now tightened to native TH15 stage1 combinations:

- TH10 blue wrapper script `45` -> TH15 native `ins_302(2); ins_306(0, 0);`
- TH10 red wrapper script `46` -> TH15 native `ins_302(2); ins_306(0, 5);`
- TH10 green wrapper script `47` -> TH15 native `ins_302(2); ins_306(0, 35); ins_303(1, 93);`
- TH10 yellow wrapper script `48` -> TH15 native `ins_302(2); ins_306(0, 40); ins_303(1, 93);`

These are all patterns used by TH15 original stage1 enemies (`GirlBlueA*`, `GirlRedA*`, `GirlC01/GirlB02`, `GirlD01/GirlD02`). The regenerated package no longer relies on merely catalog-valid but unobserved wrapper slot combinations.

Recompiled successfully with `wine thtkGUI-th20tr/thtk/thtk12/thecl.exe -c 15`.

## 2026-06-15 second-wave 1/2/3 vs 4/5 difference audit

For the five enemies at TH10 source lines 1823-1831 (converted lines around 3223-3239):

- #1-#3 call `RGirl00`, red visual wrapper, source create item policy `1`.
- #4 calls `BGirl00`, blue visual wrapper, source create item policy `2`.
- #5 calls `GGirl00`, green visual wrapper, source create item policy `3`.

After lowering to TH15 the visible/runtime-relevant differences were:

- Create final parameter differed: `RGirl00` kept `1`, while `BGirl00/GGirl00` kept `2/3`. Native TH15 stage1 enemy creates use final parameter `1`; explicit `ins_510` in the child/wrapper controls the drop type. This has now been normalized to `1` for TH10/11 -> TH13+ creates.
- Wrapper ANM differs by color. Current native TH15 combos are: red `306(0,5)`, blue `306(0,0)`, green `306(0,35)+303(1,93)`.
- DropMain differs by color: red `510(1)`, blue `510(2)`, green `510(3)`. This is preserved because it is explicit drop behavior, not create policy.

The regenerated file now has the five creates all ending in `..., 1);`, so #4/#5 no longer use target-side create presets `2/3`.

## 2026-06-15 corrected counting from enemy #11

Counting from the first enemy after the initial 10 visible enemies, the sequence in the regenerated TH15 file is:

- #1-#3: `RGirl00` (`ins_305(..., 1)`) at source lines 1823/1825/1827.
- #4: `BGirl00` (`ins_305(..., 1)`) at source line 1829.
- #5: `GGirl00` (`ins_305(..., 1)`) at source line 1831.
- #6: `RGirl00` (`ins_301(..., 1)`) at source line 1833.

Differences found after this recount:

- #1-#3 use red wrapper `RGirl00`; #4/#5 use blue/green wrappers `BGirl00/GGirl00`.
- Create final policy is now normalized to `1` for all of them, matching native TH15 stage enemy creates.
- `BGirl00/GGirl00` still differed in wrapper ordering: inherited TH10 order emitted `ins_510(2/3)` before ANM setup, while native TH15 wrappers set ANM first and then drop. A postprocess pass now moves `ins_510` in `BGirl00/GGirl00` wrapper families after the native TH15 ANM combo and before `@Girl00...`.

Current wrapper starts:

- `BGirl00`: `ins_302(2); ins_306(0, 0); ins_510(2); @Girl00(0);`
- `GGirl00`: `ins_302(2); ins_306(0, 35); ins_303(1, 93); ins_510(3); @Girl00(35);`

Recompiled successfully after regeneration.
