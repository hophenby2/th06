# Experimental ECL IR Tool

This package is an experimental cross-game Touhou ECL parser, semantic IR, and lowering pipeline. It favors explicit preservation and diagnostics over guessed opcode equivalence.

## Architecture

For a current-state, implementation-oriented architecture description, see
[`current-architecture.md`](current-architecture.md). It distinguishes the
canonical pipeline from legacy compatibility projections and records the
verified boundaries of cross-game lowering.

The schema-v2 pipeline is:

```text
source bytes
  -> SourceDocument + lossless dialect Program
  -> per-game DialectDecoder
  -> ordered SemanticModule
  -> optional state/pattern analyses
  -> LoweringPlanner(GameProfile capabilities)
  -> TargetModule
  -> DeclTextCodec
  -> target .decl bytes
```

Important boundaries:

- `SemanticModule` is the ordered canonical effect stream. Every source statement has a stable `NodeId` and one lowering owner.
- Confirmed instructions become typed `SemanticOperation` nodes. Unconfirmed instructions remain `RawInstructionOp` nodes with provenance.
- `analysis_projections` are derived views. They reference canonical `NodeId` values and never own lowering.
- Target policy is computed by `LoweringPlanner`; it is not stored on canonical nodes.
- `DeclTextCodec` is an artifact/toolchain contract restored from the standalone envelope. Text encoding is not ECL semantics and is not a `GameProfile` capability.
- Schema-v1 `objects` remain available as a compatibility backend through `compile-ir --legacy-patterns`.

## Implemented Foundations

- Byte-exact source handling:
  - strict UTF-8/CP932/Shift-JIS decoding;
  - reversible private-use byte escapes for malformed legacy files;
  - physical source lines split only on LF/CRLF, so in-string control bytes are never reinterpreted as layout;
  - exact `source_bytes_base64` and `source_layout` roundtrip;
  - canonical `.decl` output encoded through the serialized source codec contract, including direct compatibility commands.
- Ordered semantic IR:
  - typed operands, provenance, ownership, and raw fallback;
  - source-preserving `ExpressionIR` values with typed `VariableUse` and `StackUse` spans;
  - `VariableRef` records that separate semantic identity, value/storage type, scope, access, propagation, confidence, and source encoding;
  - `StackRef` records for TH13+ routine-relative slots, kept separate from semantic game variables because their offsets belong to the routine ABI;
  - unknown bracket-number encodings become identity-only opaque references instead of being reinterpreted by a target dialect;
  - one per-game `VariableDialect` registry shared by instruction operands, selected values, and syntax expressions;
  - syntax lvalues are tracked as `WRITE`, while mutation operators are `READ_WRITE`, so target access checks use the actual operand role;
  - eight-lane `DifficultyGuard` masks (`E/N/H/L/X/O/6/7`) with the source dialect spelling retained; ordinary thecl rank markers persist, while the colon form is scoped to one instruction;
  - typed `SelectedValue` / `SelectionCase` records owned by their consuming semantic, raw-instruction, or syntax node; only complete uninterrupted rank-value table candidates are folded, so ordinary ranked expressions remain ordered syntax;
  - serialized external `RoutineSignature` records for standalone compilation; inferred parameters are reconciled with their decompiler-emitted `var` aliases exactly once in the target frame;
  - separate TH06, TH07, TH08, TH10/11, TH12, TH13+, TH14+, and TH18 profiles, with a profile-level `RoutineDialect` for call, local, expression, and relative-stack conventions.
  - typed `DialectRegion` membership for legacy timeline blocks, so their game-specific timeline opcodes cannot pass through to another game as ordinary syntax.
- Bullet state analysis:
  - persistent manager definitions and immutable fire snapshots;
  - guarded difficulty lanes;
  - transform slot maps, last-write-wins replacement, holes, append cursor, copy-without-cursor, patch, and cursor decrement;
  - routine CFG construction and Tarjan strongly connected components; append writes in a cycle keep an unresolved index instead of guessing a loop-carried cursor;
  - TH08 defer/enable/immediate fire and auto-fire schedule separation;
  - contextual sentinel states (`unused` versus `keep_current`) selected by game, transform mode, and operand role, with raw tokens retained;
  - typed per-frame engine values for live player/random angles, re-encoded with the target game's sentinel token when representable.
- Canonical transform ABI:
  - `game_profile.TransformForm` is the encoding registry for opcode, write kind (`replace`/`append`), parameter set (`base`/`extended`), and operand order;
  - `BulletTransformIR` carries canonical operands and semantic modes independently of source opcode layout;
  - TH13+ `609/610/611/612` forms and legacy indexed writes lower through the same registry rather than pairwise opcode rewrites;
  - TH12 registers only `509` as a transform form; `510`, `511`, and `512` are clear-all, manager-copy, and cancel operations.
- Capability lowering:
  - `direct`, `lossy`, `raw`, and `unsupported` decisions;
  - structured diagnostics tied to `NodeId`;
  - a `TargetStatement` rendering envelope that preserves unsupported source and node-level warnings as comments;
  - strict defaults: lossy policies and cross-game raw opcode passthrough require explicit opt-in;
  - same-game identity lowering from provenance opcode plus canonical operands, including reconstruction of selected literal tables;
  - source-game-first bullet-shape catalogs, including separate TH06/TH07/TH08 and pre-TH15 layouts, with explicit unsupported/lossy decisions when a semantic shape has no exact target entry;
  - stateful TH13+ append-to-TH10/12 indexed-transform materialization when the resolved slot is unambiguous.
  - semantic variable projection with structured `variable.target_unavailable`, `variable.semantic_collision`, and storage/access diagnostics; TH06/07 stay opaque instead of borrowing TH08 IDs;
  - routine ABI gates for named calls, structured stack syntax, locals, parameters, and relative stack slots instead of silently passing incompatible TH10+ source into TH06-08;
  - exact target-game opcode lookup with no same-generation numeric fallback;
  - ANM 跨游戏 lowering 使用目标同关卡原版 package 的 manifest-scoped 候选池；连续 `select + set_main/set_sprite` 作为原子组合选择，不再静默舍弃资源设置语句；
  - `AnmCandidateSelection` 保留目标原版文件/routine evidence，`AnmCallSiteMaterialization` 只在所有同步直接调用都能把 formal script 绑定为整数 literal 且 semantic-purpose 匹配成功时前移资源组合；
  - 目标 `anim` 声明投影自目标关卡 manifest；semantic-purpose/routine-sequence 候选可用于 strict lowering，仅数字/频率 fallback 与动态 script 固定替代必须显式 `--allow-lossy`；
  - conservative legacy macro rejection for opaque TH06 runtime behavior, dynamic/nonzero transform flags, unverified colors, and dynamic random ranges.

## Commands

Run from the repository root:

```bash
python3 -m ecl_ir.cli emit-ir th12/stage01.decl -o /tmp/stage01.eclir.json
python3 -m ecl_ir.cli validate-ir /tmp/stage01.eclir.json
python3 -m ecl_ir.cli roundtrip-ir /tmp/stage01.eclir.json --layout -o /tmp/stage01.roundtrip.decl
python3 -m ecl_ir.cli compile-ir /tmp/stage01.eclir.json --target th15 -o /tmp/stage01.th15.decl
```

`compile-ir` uses ordered canonical IR and a strict policy by default. It writes `.decl` bytes with the codec serialized in the standalone envelope, which is required by older thecl builds that do not provide UTF-8 conversion. `--allow-lossy`, `--preserve-raw-same-family`, and `--preserve-raw-cross-family` are explicit unsafe/approximation opt-ins; node warnings are rendered beside the affected statement. Use `--legacy-patterns` only to compare against the older object-cluster backend.

Other compatibility commands remain available:

- `lift`: inspect legacy lifted objects.
- `compile`: lower one selected legacy object.
- `transpile`: run the legacy interleaved whole-file backend directly from source.
- `scan`: count liftable legacy object kinds.

## Package Layout

```text
ecl_ir/
  source/        source bytes, Program model, and parser
  canonical/     ordered semantic IR, lifter, operations, and variables
  dialects/      game profiles, references, semantic catalogs, and ANM data
  analysis/      bullet state, CFG, transform, and ANM candidate analysis
  target/        capability planner, target module, and argument encoding
  artifact/      standalone schema-v2 serialization and validation
  compat/        text backend still used at the canonical encoding boundary
  legacy/        schema-v1 object projections retained for compatibility
  integrations/  optional LuaSTG integration
  commands/      CLI implementation
  deprecated/    unreferenced one-off code only
  cli.py          stable `python -m ecl_ir.cli` facade
```

The legacy and compatibility directories are deliberately separate. Code in
`legacy/` remains part of the schema-v1 compatibility contract; code in
`compat/` is still called by canonical target encoding. Neither may be treated
as dead code. See [`legacy/README.md`](legacy/README.md) and
[`deprecated/README.md`](deprecated/README.md).

## Current Limits

This is not a verified binary-equivalent transpiler. Remaining work includes:

- target-dialect rewriting for all control-flow and expression syntax, especially TH06-08;
- a complete expression-node union and routine symbol table beyond the current source-preserving typed variable and relative-stack spans;
- one shared `OperationSchema` for canonical operand names/use kinds and target layouts; anonymous `operand_N` values still defer too much meaning to `arg_adapter`;
- additional verified variable catalog entries for TH06/07, game-specific overlays, and currently opaque TH18.5 slots;
- full CFG state joins beyond conservative cycle detection, including transform branches whose difficulty lanes resolve to different append cursors;
- long transform forms that have no representable target form;
- replacement of `TargetStatement.lines` with a typed target union such as instruction, syntax, comment, and unsupported nodes;
- ANM 候选池尚缺完整的 typed `AnmResourceRef`、CFG state join 与逐 difficulty lane bank-flow；当前目标原版组合证据只能证明 package 内编号有效，不能证明运行时视觉等价；
- complete laser lifecycle, other resource projections, and game-specific system semantics;
- target compiler checks and runtime equivalence tests across the full corpus;
- migration of remaining schema-v1 object-specific behavior into canonical analyses and capability lowerers.

Unsupported behavior is retained with a structured diagnostic; it is not silently dropped.
