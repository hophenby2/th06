# Standalone ECL IR Roadmap

Goal: make the pipeline work as `source .decl -> standalone .eclir.json -> source .decl` and `source .decl -> standalone .eclir.json -> target .decl`, without reparsing the original source during the compile step.

## Current State

- `lift` exports a semantic object summary, but it is not a full standalone program IR.
- `transpile` reparses source `.decl` and mixes raw program state with lifted objects.
- Most IR objects have `to_dict()`, but there is no complete `from_dict()` path.
- Roundtrip to source is not guaranteed because comments/blank lines/resource formatting/function braces are not fully represented as an identity backend.

## Required IR Layers

| Layer | Purpose | Required Data | Status |
|---|---|---|---|
| Raw Program IR | Lossless-ish source representation for roundtrip and fallback | game, source, resources, top-level statements, functions, params, statements, instructions, raw text, line numbers, difficulty blocks | first implementation in `ir_file.py` |
| Semantic Object IR | Cross-game objects used by target lowering | BulletEmitter, Enemy, Animation, Timeline, BossTimer, MotionModifier, policies, raw covered instructions | first implementation in `ir_file.py` |
| Rewrite/Policy IR | Non-local conversion policy | ResourcePlan, EntryAlias, TimelineRewrite, FunctionRewrite, lowering policies | included as normal objects |
| Identity Backend | Compile IR back to source generation | emits original raw statements where possible | first implementation: source-like roundtrip |
| Target Backend | Compile IR to target generation | uses semantic objects and raw fallback from IR file | first implementation: reuses existing `emit_transpile()` with reconstructed Program/objects |

## CLI Targets

| Command | Meaning | Status |
|---|---|---|
| `emit-ir source.decl -o file.eclir.json` | Parse and lift source into standalone IR JSON | first implementation |
| `roundtrip-ir file.eclir.json -o source.decl` | Reconstruct source-like `.decl` from IR only | first implementation |
| `compile-ir file.eclir.json --target th15 -o target.decl` | Compile target `.decl` from IR only | first implementation |

## What “Perfect Roundtrip” Still Needs

1. Preserve every blank line and comment position in `Program.top_level` and `Function.statements`.
2. Preserve resource block formatting, not just entries.
3. Preserve exact function header spelling and brace style.
4. Ensure difficulty literal groups (`!E`, `!*`) are emitted exactly as read.
5. Store non-instruction raw statements and labels in a single ordered stream.
6. Add schema version migrations so old `.eclir.json` files remain loadable.
7. Add tests that compare instruction/resource/function equivalence after `source -> ir -> source`.

## What “IR -> Any Target” Still Needs

1. Finish `backend-special-cases.md` remaining `todo`/`partial` entries.
2. Move dynamic bullet/timeline lowering out of `cli.py` into IR policies.
3. Move ANM generic remap logic fully into animation semantic objects.
4. Make LuaSTG lifter emit standard BulletEmitter/LaserEmitter objects, not backend-specific objects.
5. Add target capability metadata for unsupported lasers/bullet shapes/tool ABI hazards.

## Acceptance Tests

| Test | Command Pattern | Expected |
|---|---|---|
| IR generation | `emit-ir src.decl -o src.eclir.json` | JSON contains `program` and `objects` |
| Source roundtrip | `roundtrip-ir src.eclir.json -o rt.decl` | `thecl -c source_game rt.decl rt.ecl` compiles |
| Target compile | `compile-ir src.eclir.json --target th15 -o out.decl` | `thecl -c 15 out.decl out.ecl` compiles |
| Equivalence scan | parse source and roundtrip | same function names/resources/instruction opcode+args order |
