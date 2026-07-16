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
  - `check-ecl` 对目标 package 做全节点符号/opcode/参数预检，包括 named/numeric/relative-stack 变量、访问权限和已知 byte 参数范围，并从 `main` 分别抽象执行 E/N/H/L；同步调用共享单位 ANM 状态，spawn 使用 fresh unit state，async ANM 写入保留竞态 warning；
  - ANM 检查覆盖 manifest、默认/显式 bank、slot 使用前绑定、完整原子组合、单位 stage/boss/midboss role，以及每个生成 ecli 成员逐难度、逐 CFG 路径的 source-plan/target trace 与 call/async/spawn edge 对比；
  - conservative legacy macro rejection for opaque TH06 runtime behavior, dynamic/nonzero transform flags, unverified colors, and dynamic random ranges.

## Commands

Run from the repository root:

```bash
python3 -m ecl_ir.cli emit-ir th12/stage01.decl -o /tmp/stage01.eclir.json
python3 -m ecl_ir.cli validate-ir /tmp/stage01.eclir.json
python3 -m ecl_ir.cli roundtrip-ir /tmp/stage01.eclir.json --layout -o /tmp/stage01.roundtrip.decl
python3 -m ecl_ir.cli compile-ir /tmp/stage01.eclir.json --target th15 -o /tmp/stage01.th15.decl
python3 -m ecl_ir.cli compile-package th15/st01.decl --target th12 --reference-package th12/stage01.decl --output-dir /tmp/th15-to-th12 --allow-lossy
python3 -m ecl_ir.cli check-ecl th15/st01.decl --difficulty ENHL
python3 -m ecl_ir.cli check-ecl /tmp/st01.th15.decl --game th15 --reference-package th15/st01.decl --json
```

`compile-ir` uses ordered canonical IR and a strict policy by default. It writes `.decl` bytes with the codec serialized in the standalone envelope, which is required by older thecl builds that do not provide UTF-8 conversion. `--allow-lossy`, `--preserve-raw-same-family`, and `--preserve-raw-cross-family` are explicit unsafe/approximation opt-ins; node warnings are rendered beside the affected statement. Use `--legacy-patterns` only to compare against the older object-cluster backend.

`compile-package` applies the same canonical planner and policy flags to the
root and every recursively referenced `ecli` module, including `default.ecl`.
The generated root takes the basename of `--reference-package`; other modules
keep their source-package-relative paths. The reference root also supplies the
target ANM candidate pool. All modules are written even when a lowering remains
unsupported (exit `1`). A missing source dependency or an invalid package/path
configuration is rejected before output is written and returns `2`.

`check-ecl` first validates the input package and then abstractly executes the
selected entry from the beginning in independent difficulty lanes. It checks
`E`, `N`, `H`, and `L` by default; use `--difficulty` to select a subset,
`--all-routines` to include unreachable routines, and `--state-budget` to bound
execution (`200000` states per difficulty by default). `--all-routines` first
runs the normal entry graph, then locally audits other routines with unknown
entry state without recursively expanding their call/spawn graphs.
`--reference-package` supplies the corresponding original target
package and its sibling files as the actual resource-evidence pool. Non-default
`ecli` dependencies must exist relative to the input package; only
`default.ecl` may fall back to the target/reference corpus, and unresolved
dependencies are errors. Human-readable diagnostics include severity, lane,
module, routine, and source line; `--json` emits the complete structured report.
Exhausting one lane's budget marks the report incomplete but does not skip the
remaining selected lanes.

The `check-ecl` exit codes are:

- `0`: no diagnostic reached the configured `--fail-on` threshold;
- `1`: at least one diagnostic reached the threshold (`error` by default, or
  warnings and errors with `--fail-on warning`);
- `2`: invalid arguments, input, game, package configuration, or state budget.

Original-package evidence proves that a resource number or ANM combination is
loaded and used by that target package. It does not prove that the selected
animation is visually equivalent to the source behavior. Bounded CFG path
comparison preserves both sides of unknown conditions; it detects structural
and action differences but does not prove predicate or scheduling equivalence.

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
  analysis/      bullet/CFG/transform state, ANM candidates, and execution checks
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
