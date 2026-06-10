# Experimental ECL IR Tool

This is an experimental cross-game Touhou ECL IR implementation. It parses `.decl` scripts, lifts common opcode clusters into higher-level objects, and lowers a conservative subset back into target-game opcode shapes.

## Implemented Object Lifting

- `BulletEmitter`
  - TH13+ style: `600/607/602/606/604/605/609-612/601`.
  - TH12 style: `500/507/502/506/504/505/509-512/501`.
  - TH10/TH11 slot style: partial `400/401/402/404/405/406/407/408/409`.
  - TH08 macro style: `96..104` plus pending `111` transforms.
- `LaserEmitter`
  - TH13+ `700..714` cluster.
  - TH12 `600..615` cluster.
- `Movement`
  - TH13+ common movement opcodes `400..407`, ellipse, bezier, curve/reset subset.
  - TH12 corresponding `300..327` subset.
  - TH10/TH11 partial movement subset.
- `Animation`
  - TH13+ `302/303/306/307/308/317/318`.
  - TH10-TH12 `258/259/262/263/264`.
- `Enemy`
  - TH13+ `300/301/304/305/309..312`.
  - TH10-TH12 `256/257/260/261/265..268`.
- `BossPattern`
  - TH13+ life/boss/timer/interrupt/spell/chapter subset.
  - TH12 corresponding subset.
- `Timeline`
  - Preserves function-level statements as structured events: labels, time labels, `goto`, conditional `goto`, calls, async calls, returns, variable declarations, assignments, raw lines, and wait instructions.
  - Detects simple backward-edge loops, including counter-like conditions such as `$A--`.

The parser also preserves resource headers (`anim` / `ecli`) and simple difficulty literal blocks such as `!E ... !LO ... !* ins_605(...[-1.0f]...)`.

## Implemented Lowering

- `BulletEmitter -> TH12` and `BulletEmitter -> TH13+`.
- `LaserEmitter -> TH12/TH13+` via opcode-family offset where safe enough to emit with verification comments.
- `Movement -> TH12/TH13+` for mapped semantic movement ops.
- `Animation -> TH12/TH13+` for mapped semantic animation ops.
- `Enemy -> TH12/TH13+` for mapped semantic enemy creation ops.
- `BossPattern -> TH12/TH13+` for mapped semantic boss ops.
- `Timeline -> TH12/TH13+` as a structure-preserving draft that keeps control flow and comments out instruction bodies that should be lowered by object-specific passes.

Every non-trivial lowering emits comments like `semantic verification required`; unsupported pieces are preserved as comments rather than silently dropped.

## Usage

```bash
python3 -m th062.ecl_ir.cli scan th062
python3 -m th062.ecl_ir.cli scan th062 --json
python3 -m th062.ecl_ir.cli lift th062/th15/st01.decl
python3 -m th062.ecl_ir.cli compile th062/th15/st01.decl --kind BulletEmitter --target th12 --index 0
python3 -m th062.ecl_ir.cli compile th062/th12/stage01.decl --kind BulletEmitter --target th13 --index 0
python3 -m th062.ecl_ir.cli compile th062/th15/st01.decl --kind Movement --target th12 --index 0
python3 -m th062.ecl_ir.cli compile th062/th15/st01.decl --kind Enemy --target th12 --index 0
python3 -m th062.ecl_ir.cli compile th062/th13/st01bs.decl --kind BossPattern --target th12 --index 0
python3 -m th062.ecl_ir.cli compile th062/th15/st01.decl --kind Timeline --target th12 --index 0
python3 -m th062.ecl_ir.cli transpile th062/th15/st01.decl --target th12 --output /tmp/st01.th12.draft.decl
```

## Files

- `model.py`: IR dataclasses.
- `parser.py`: `.decl` parser with resource, statement, and difficulty-block preservation.
- `lifter.py`: bullet emitter lifter.
- `object_lifter.py`: multi-object lifter.
- `timeline_lifter.py`: control-flow/time-line lifter.
- `backend.py`: target lowering.
- `cli.py`: command-line entrypoint.

## Commands

- `scan`: recursively scan `.decl` files and count lifted object kinds.
- `lift`: emit JSON IR, including resources, top-level declarations, Timeline objects, and semantic objects.
- `compile`: lower one selected lifted object.
- `transpile`: lower a whole `.decl` as an interleaved structured draft, keeping waits/control flow in place and replacing recognized clusters with target-family opcode drafts.

## Current Limits

This is not a verified binary-compatible transpiler yet. Missing or incomplete areas:

- Resource remapping for bullet styles, colors, ANM scripts, sounds, spell names.
- Exact transform semantic conversion, especially TH10/TH11 `409` and TH13+ `609..612` edge cases.
- TH06/TH07 lifting beyond generic unsupported/raw handling.
- Full expression normalization and async task graph recovery; Timeline currently identifies structure but does not prove binary-equivalent scheduling.
- Game-specific systems such as season, animal spirits, pointdevice, cards, score items, dialogue/UI.

Use the emitted target code as a structured draft that still needs semantic verification.
