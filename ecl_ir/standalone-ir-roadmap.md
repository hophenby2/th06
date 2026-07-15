# Standalone ECL IR Roadmap

Goal:

```text
source .decl -> standalone .eclir.json -> exact source bytes
source .decl -> standalone .eclir.json -> target .decl
```

The compile step must not read the original source or sibling files.

## Current Layers

| Layer | Role | Status |
|---|---|---|
| `SourceDocument` | Reversible bytes, encoding, malformed-byte escapes | implemented |
| `DeclTextCodec` | Artifact-level encoding of generated thecl source; separate from semantic/game profiles | implemented |
| Dialect `Program` | Parsed statements, resources, instructions, exact raw text | implemented |
| `SemanticModule` | Ordered canonical nodes with identity/ownership/provenance | implemented |
| `ExpressionIR` / dialect registries | `VariableUse/VariableRef` and `StackUse/StackRef` shared by instruction, selected-value, and syntax expressions | implemented conservative foundation |
| `DialectRegion` | Typed membership for legacy timeline syntax blocks | implemented; cross-game timeline lowering remains unsupported |
| Analysis projections | State, CFG, and pattern views that reference canonical nodes | bullet manager and conservative CFG cycle analysis implemented; others partial |
| `LoweringPlanner` | Target capability decisions and structured diagnostics | implemented foundation |
| `TargetModule` | Ordered string-backed `TargetStatement` envelopes and renderer | implemented foundation; typed statement union pending |
| Legacy Pattern objects | Compatibility with older specialized lowerers | retained behind `--legacy-patterns` |

Schema v2 serializes the Program, canonical IR, bullet analysis, legacy objects, source layout, exact bytes, and discovered external `RoutineSignature` records. `compile-ir` consumes only serialized data.

## Command Contract

| Command | Contract |
|---|---|
| `emit-ir source.decl -o file.eclir.json` | Parse once and serialize all standalone inputs |
| `roundtrip-ir file.eclir.json -o source.decl` | Restore exact stored source bytes |
| `roundtrip-ir file.eclir.json --layout -o source.decl` | Restore exact bytes through reversible layout metadata |
| `roundtrip-ir file.eclir.json --canonical -o source.decl` | Render structural Program IR |
| `validate-ir file.eclir.json` | Check hashes, structure, canonical counts, NodeIds, ownership, signatures, and analysis references |
| `compile-ir file.eclir.json --target X -o target.decl` | Strictly lower ordered canonical IR; return nonzero when unsupported nodes remain |
| `compile-ir ... --allow-lossy/--preserve-raw-*` | Explicitly opt into approximations or warned raw passthrough |
| `compile-ir ... --legacy-patterns` | Use schema-v1 Pattern compatibility lowering |

## Completed Invariants

1. Exact source and layout roundtrips do not decode with replacement characters.
2. CP932 spell names survive Program and canonical IR serialization.
3. Malformed TH08 files use reversible byte escapes and remain byte-identical.
4. Canonical routines preserve statement order and instruction count.
5. Canonical `NodeId` values are non-empty and unique; ownership is validated.
6. Analysis action IDs must reference canonical nodes.
7. External routine parameters are serialized; changing or deleting sibling files after `emit-ir` does not affect `compile-ir`.
8. TH06/TH07 do not inherit TH08 opcode numbers.
9. `DifficultyGuard` is an eight-lane mask (`E/N/H/L/X/O/6/7`); numeric and legacy marker spellings are dialect encodings, not different semantics. Ordinary rank markers persist until changed, while `!X:` is scoped to one instruction and then resets to `*`.
10. Runtime difficulty literal tables are represented by typed `SelectedValue` and `SelectionCase` records owned by the semantic, raw-instruction, or syntax node that consumes them. Only complete uninterrupted candidates are folded; ordinary ranked expressions remain syntax. Same-game identity emission reconstructs tables, while unimplemented cross-game selection lowering is structured unsupported.
11. Bullet transform replace/append/cursor/copy semantics are reduced through one state model. `TransformForm` is the single registry for concrete transform layouts.
12. Routine CFGs use Tarjan strongly connected components to identify loop-carried append writes. Their index is deliberately unresolved and cannot be materialized into a legacy indexed write.
13. Same-game canonical compilation uses the provenance opcode and canonical operands, avoiding cross-generation compatibility rewrites.
14. Bullet visual lowering uses source-game-first shape catalogs and reports missing or merged target shapes explicitly.
15. Transform sentinel decoding distinguishes unused, keep-current, and typed per-frame engine values by game, semantic mode, and operand role.
16. Numeric variable IDs decode through a per-game `VariableDialect`; semantic collisions, unavailable target slots, and unsafe access narrowing are structured unsupported. TH06/TH07 do not borrow TH08 variable meanings.
17. TH13+ relative stack slots are `StackRef` values and project only between compatible relative-stack routine dialects.
18. Named locals, declarations, routine parameters, calls, and structured stack-expression syntax cannot silently cross into the TH06-08 register ABI.
19. `RoutineDialect` is the shared profile contract for call, local, expression, and relative-stack encodings; lowering does not infer those contracts from opcode-generation labels.
20. Unknown bracket-number encodings are opaque and identity-only; a target cannot reinterpret them as its own variable or stack slot.
21. Legacy timeline members carry a typed `DialectRegion`; cross-game timeline opcode passthrough is structured unsupported.
22. Target opcode selection requires an exact target-game semantic registry entry; same-generation numeric fallback is forbidden.
23. Lossy policies and cross-game raw instructions are disabled by default. Explicitly enabled node warnings are rendered next to the emitted statement.
24. ANM bank/script operations require typed, verified resource projection before cross-game emission.
25. Unsupported target behavior remains visible as a structured diagnostic and source comment.
26. Generated `.decl` files use the standalone envelope's `DeclTextCodec`; character encoding is an artifact contract rather than canonical semantics or a per-game capability.
27. Physical line splitting recognizes LF/CRLF rather than Unicode control separators; embedded legacy string bytes survive Program, TargetModule, and `.decl` emission on one physical line.
28. Inferred external routine parameters replace matching decompiler-emitted local aliases in the target frame; they are never allocated twice.

## Next Behavior Work

1. Replace `TargetStatement.lines` and remaining compatibility string emission with typed instruction, syntax, comment, and unsupported target nodes.
2. Expand `ExpressionIR` from typed variable and relative-stack source spans to a complete literal/variable/unary/binary/cast/call expression union with routine symbol binding.
3. Merge `DialectDecoder` operand names/use kinds and `arg_adapter` target layouts into one `OperationSchema`.
4. Add typed `AnmResourceRef` values and difficulty/CFG-aware current-bank analysis before enabling ANM resource projection.
5. Extend verified variable catalogs without treating eclmap supersets as availability, especially TH06/07 and TH18.5.
6. Extend CFG analysis from conservative SCC cycle rejection to full state joins for divergent branches and difficulty-lane append cursors.
7. Model laser definitions and instances with the same action/reducer approach as bullet managers.
8. Move movement, animation, enemy, boss, and resource Pattern objects to canonical analyses.
9. Add target compiler validation for every supported game and representative runtime equivalence tests.
10. Define schema migrations before changing canonical node layouts.

## Current Verification

- 90 Python unit tests cover source decoding and output codecs, embedded control bytes, persistent/scoped rank state, selected-value candidate rollback, standalone signatures and inferred frame reconciliation, typed variable/stack projection, routine/timeline ABI gates, exact opcode selection, strict RAW/lossy policy, ANM resource guards, semantic/backend compatibility, bullet state semantics, capability planning, `TargetStatement` rendering, and IR validation.
- All 210 repository `.decl` files parse, build canonical IR, and run bullet analysis without exceptions.
- All 210 source documents and source layouts roundtrip byte-identically.
- Representative TH12 -> TH15 canonical lowering selects indexed replace (`509 -> 609`).
- Representative TH13+ -> TH12 lowering materializes append cursors into explicit `509` indices when lanes agree.
- Cyclic TH13+ append writes are diagnosed instead of being assigned a static TH10/12 index.
- Same-target compilation covers 251,701 nodes (`160,275` instructions and `91,426` syntax nodes) with zero statement, instruction-shape, and effective-guard mismatches. This includes 1,978 semantic-operation and 104 syntax `SelectedValue` groups plus 56 typed timeline blocks / 12,707 timeline members.
- Independent rank-state replay over all 210 files reports zero statement/order mismatches and zero effective-guard mismatches; it covers 1,492 instructions affected by persistent inline rank markers and 1,948 complete selected-value candidates / 8,309 literal lines.
- Touhou Toolkit release 12 under Wine accepts both the original and canonical same-target source for 209/209 comparable repository files, and every resulting ECL pair is byte-identical. The remaining `th08/ecldata_yy.decl` input is baseline-invalid: both forms fail with the same unterminated-string and unexpected-EOF diagnostics.
- The final 210-file by 12-target strict matrix completed all 2,520 builds and 3,020,520 node decisions without an exception: `direct=950,485`, `raw=836,359`, `lossy=0`, `unsupported=1,233,676`. All 1,235,398 diagnostics are structured errors; the extra 1,722 are module-level routine-parameter ABI diagnostics.
- Same-target rendering intentionally normalizes 17,291 time-label comment attributes and 1,746 explicit `!*` spellings; time values and difficulty masks are unchanged.

Cross-game target `.decl` compiler success and runtime equivalence remain required before claiming cross-game behavioral parity.
