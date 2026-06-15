# Standalone ECL IR Roadmap

Goal: make the pipeline work as `source .decl -> standalone .eclir.json -> source .decl` and `source .decl -> standalone .eclir.json -> target .decl`, without reparsing the original source during the compile step.

## Current State

- `lift` exports a semantic object summary, but it is not a full standalone program IR.
- `transpile` reparses source `.decl` and mixes raw program state with lifted objects.
- Most IR objects have `to_dict()`, but there is no complete `from_dict()` path.
- Exact byte roundtrip is implemented by storing `source_bytes_base64` plus `source_sha256` in `.eclir.json`.
- `source_layout` now stores per-line layout metadata, allowing byte-identical reconstruction without reading `source_bytes_base64`; Program canonical roundtrip is still structural and not byte-perfect.

## Required IR Layers

| Layer | Purpose | Required Data | Status |
|---|---|---|---|
| Raw Program IR | Lossless source preservation plus parsed fallback representation | game, source, raw source bytes/hash, source encoding, source layout lines, resources, top-level statements, functions, params, statements, instructions, raw text, line numbers, difficulty blocks | implemented in `ir_file.py` |
| Semantic Object IR | Cross-game objects used by target lowering | BulletEmitter, Enemy, Animation, Timeline, BossTimer, MotionModifier, policies, raw covered instructions | first implementation in `ir_file.py` |
| Rewrite/Policy IR | Non-local conversion policy | ResourcePlan, EntryAlias, TimelineRewrite, FunctionRewrite, lowering policies | included as normal objects |
| Identity Backend | Compile IR back to source generation | emits original source bytes by default; `--layout` emits line-layout reconstruction; canonical mode emits parsed Program IR | exact byte and layout roundtrip implemented; Program canonical mode is structural |
| Target Backend | Compile IR to target generation | uses semantic objects and raw fallback from IR file | first implementation: reuses existing `emit_transpile()` with reconstructed Program/objects |

## CLI Targets

| Command | Meaning | Status |
|---|---|---|
| `emit-ir source.decl -o file.eclir.json` | Parse and lift source into standalone IR JSON | first implementation |
| `roundtrip-ir file.eclir.json -o source.decl` | Reconstruct exact original `.decl` bytes from IR only | implemented |
| `roundtrip-ir file.eclir.json --layout -o source.decl` | Reconstruct `.decl` from line-level layout IR without using raw source bytes | implemented |
| `roundtrip-ir file.eclir.json --canonical -o source.decl` | Reconstruct canonical source from parsed Program IR | implemented, not byte-perfect |
| `validate-ir file.eclir.json` | Validate schema/hash/parse consistency | implemented |
| `compile-ir file.eclir.json --target th15 -o target.decl` | Compile target `.decl` from IR only | first implementation |

## What “Perfect Roundtrip” Still Needs

Exact byte roundtrip is handled by `source_bytes_base64`; layout roundtrip is handled by `source_layout`. These items remain for Program-only canonical roundtrip after intentionally dropping source bytes/layout:

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
| Source roundtrip | `roundtrip-ir src.eclir.json -o rt.decl` and `cmp src.decl rt.decl` | exact byte match, then `thecl -c source_game rt.decl rt.ecl` compiles |
| Layout roundtrip | `roundtrip-ir src.eclir.json --layout -o rt.decl` and `cmp src.decl rt.decl` | exact byte match from `source_layout` |
| Canonical roundtrip | `roundtrip-ir src.eclir.json --canonical -o rt.decl` | structure-preserving source-like output; formatting may differ |
| IR validation | `validate-ir src.eclir.json` | hash and parsed instruction/function counts are consistent |
| Target compile | `compile-ir src.eclir.json --target th15 -o out.decl` | `thecl -c 15 out.decl out.ecl` compiles |
| Equivalence scan | parse source and roundtrip | same function names/resources/instruction opcode+args order |

## Latest Validation

Validated on `th062/th10/stage01.decl`:

- `emit-ir` produced `/tmp/th10_stage01_layout.eclir.json` with 68 functions, 1032 instructions, 682 semantic objects, and 2042 `source_layout` lines.
- `validate-ir` passed with matching `source_sha256` and `source_layout_sha256_actual`.
- `roundtrip-ir --layout` produced `/tmp/th10_stage01_layout_roundtrip.decl`; `cmp th062/th10/stage01.decl /tmp/th10_stage01_layout_roundtrip.decl` returned `0`.
- `compile-ir --target th15` produced `/tmp/th10_stage01_layout_to_th15.decl`.
- `wine thtkGUI-th20tr/thtk/thtk12/thecl.exe -c 10 /tmp/th10_stage01_layout_roundtrip.decl /tmp/th10_stage01_layout_roundtrip.ecl` succeeded.
- `wine thtkGUI-th20tr/thtk/thtk12/thecl.exe -c 15 /tmp/th10_stage01_layout_to_th15.decl /tmp/th10_stage01_layout_to_th15.ecl` succeeded.
