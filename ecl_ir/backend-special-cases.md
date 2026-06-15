# Backend Special Case Migration Table

This table tracks backend source-semantics logic that should move into IR objects, op policies, or reference/tool ABI metadata. Status values:

- `todo`: identified but not migrated.
- `partial`: IR metadata exists, backend still contains semantic branching.
- `done`: backend only consumes generic IR/policy metadata.
- `keep-backend`: target ABI/codegen concern, not source semantic recognition.

| ID | Backend Location | Current Special Case | Target IR / Metadata Owner | Status | Notes |
|---|---|---|---|---|---|
| B01 | `normalize_target_args_for_op_key` | TH13+ movement float index normalization and TH12 tween-mode clamping | `arg_adapter` op layouts / target argument schema | todo | Backend should not know per-op argument semantic indices. |
| B02 | `UNSAFE_TARGET_OPCODES` | thecl/thtk format table hazards | `reference.py` or `tool_abi.py` | keep-backend | Tool ABI metadata, not IR semantic; can move out of backend later. |
| B03 | `compile_th08_vm_arithmetic` | TH06-08 expression ops lowered to stack VM instruction sequences | `op_ir.op_lowering_policy` / `LegacyVmOp` sequence templates | partial | Simple stack ops moved to policy; geometry helpers `circle_pos/math_angle/math_distance` remain. |
| B04 | `compile_th08_movement_alias` | TH06-08 `move_dir*` aliases to velocity ops | `op_ir.op_lowering_policy` alias templates | done | Function deleted; handled by IR op policy. |
| B05 | `compile_th08_conditional_jump` | TH06-08 comparison+jump/loop lowered to stack compare + jump | `op_ir.op_lowering_policy` control-flow templates | done | Function deleted; comparison and loop policies emit target compare/jump sequences. |
| B06 | `compile_th08_anm_alias` | TH06-08 `anm.set`/slot aliases | `op_ir.op_lowering_policy` sequence template | done | Function deleted; handled by IR op policy. |
| B07 | `compile_th10_stage_wrapper_anm` | Old TH10/11 stage enemy wrapper ANM special lowering | `AnimationOp.target_policy.stage_enemy_wrapper_anm` | done | Deleted from backend; handled by IR target policy. |
| B08 | `drop_th12_stage6_stage_mboss_boss_anm` | TH12 stage06 MBoss boss-bank ANM drop | `AnimationOp.target_policy.drop_for_target` | done | Deleted from backend; handled by IR target policy. |
| B09 | `compile_ir_op_event` pre-fallback checks | Disabled async, float-time, nop, transform unsafe handling | `op_ir.lowering_policy` / transform IR | partial | Disabled async and float-time are policies; nop and TH13+ transform-to-TH12 still backend checks. |
| B10 | `target_policy_applies` / `compile_target_policy` | Generic IR policy executor | backend executor | keep-backend | Correct place unless it starts identifying source semantics. |
| B11 | `enemy_create_op_key_for_target` | Enemy create op selection from role/absolute/mirror/func | `EnemyOp.fields.create.target_forms` | done | Function removed; backend consumes precomputed target forms. |
| B12 | `remap_named_args` ANM role/script remaps | ANM bank/script semantic remapping | `AnimationOp.target_policy` / ANM semantic object | partial | Some high-level policies exist, but generic named-op path still remaps. |
| B13 | `compile_boss_timer` | Legacy timer/life/bomb/HUD semantic branches | `BossTimer.lowering_plan` with target op and arg templates | done | Backend now consumes generic plan instructions/sequences. |
| B14 | `compile_motion_modifier` | Legacy random/circle/accel motion approximations | `MotionModifier.lowering_plan` with target op and arg templates | done | Backend now consumes generic plan instructions. |
| B15 | `compile_luastg_laser` and LuaSTG bullet path | LuaSTG-specific objects in backend | LuaSTG lifter emits standard `LaserEmitter`/`BulletEmitter` | todo | Backend should not test `game == luastg`. |
| B16 | `compile_laser` old target unsupported branch | Laser generation availability | target capability metadata | keep-backend | Target capability/codegen concern. |
| B17 | `compile_th13plus` / `compile_th12` / `compile_th10_slot` / `compile_th08_macro` | Target bullet emitter codegen | backend target lowerers consuming `BulletEmitter.lowering_plan` | keep-backend | These can stay; internal unsupported transform comments can move to transform IR. |
| B18 | `compile_th10_slot` start opcode from raw first opcode | TH10 slot start mode (`etNew` vs `etNew2`) | `BulletEmitter.semantics.start_mode` | todo | Easy follow-up after emitter lifter marks it. |
| B19 | `clamp_old_shape` | Old-target bullet shape bounds | target bullet-shape catalog metadata | todo | Should use semantic shape/color catalog, not hardcoded max. |
| B20 | `compile_lossy_semantic_fallback` | Missing policy fallback comment | backend diagnostics | keep-backend | Useful to reveal unmigrated semantics. |
