# TH15 stage1 -> TH12 conversion package

Regenerated after thtk format-table fixes.

## Format check
- TH12 missing opcode ids in generated active instructions: 0
- Coarse fixed-arity mismatches in generated active instructions: 0
- Active `ins_23(...)` tokens: 0
- Active `ins_514(...)` tokens: 0

## Files
- `default.decl`: lines=386, unlifted=23, unsupported=5, fallback=35, collapsed_wait=0
- `st01bs.decl`: lines=832, unlifted=37, unsupported=32, fallback=48, collapsed_wait=14
- `st01mbs.decl`: lines=433, unlifted=27, unsupported=16, fallback=22, collapsed_wait=7
- `st01mbs2.decl`: lines=478, unlifted=26, unsupported=19, fallback=28, collapsed_wait=6
- `stage01.decl`: lines=1747, unlifted=29, unsupported=42, fallback=96, collapsed_wait=13

## Notes
- TH12 has no normal opcode 23; TH15 `ins_23(wait)` is now emitted as `+wait:` time advancement.
- TH15 `ins_614(...)` is no longer lowered to TH12 `ins_514(...)`; their formats differ.
- TH13+ bullet transforms `609..612` are preserved as comments unless a TH12 format-safe equivalent is known.
- Unsupported TH15-specific behavior is commented out rather than emitted as invalid TH12 bytecode.
- TH15 dynamic wait expressions such as `ins_23(60 + ([-10000] % 80))` are collapsed to literal TH12 time labels such as `+60:` because thtk TH12 time labels only accept integer literals.

## Runtime entry fix

- Added TH12 stage01 compatibility wrapper functions such as `BGirl00`, `GGirl00`, `RGirl00`, `YGirl00`, `Boss`, `MBoss`, and missing `MainSub08..13` names.
- Reason: TH12 stage scheduling / existing STD-side references expect those stage01 sub names. The converted TH15 script originally only had TH15 names like `MainFront`, `MainLatter`, and `MainSub00..07`, so the ECL could compile but nothing was called at runtime.
- The wrappers call the converted TH15 main flow functions. This is a runtime connectivity patch, not a complete STD conversion.

- Regenerated stage01 with compatibility wrappers from the transpiler; no manual-only wrapper patch is required now.

## Wait fix

- TH15 `ins_23(wait)` is now lowered to TH12 `ins_83(wait)` based on `th062/ecl.txt`.
- Remaining `+N:` lines are source time labels/time anchors, not translated waits.

- Source `+N:` time anchors are also lowered to `ins_83(N)` for TH12 testing, because leaving them as scheduler time markers made converted sequential main flow effectively skip waits.
