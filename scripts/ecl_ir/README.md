# ECL IR integration scripts

`run_stage01_matrix.py` is the repeatable TH10-TH18 cross-game integration
runner.  Every selected direction performs these steps in order:

1. `compile-package` converts the source `stage01.decl` (TH10-TH12) or
   `st01.decl` (TH13-TH18), including all recursive `ecli` dependencies.
2. `check-ecl` starts at that generated stage root's `main` routine and checks
   the E, N, H, and L lanes against the target game's original stage package.
3. Wine/thecl compiles every generated `.decl` module, not only the root.

`default.decl` can be converted and compiled as a package dependency, but is
never used as the matrix or checker entry.

Use one or more explicit directions for a smoke run:

```sh
python3 scripts/ecl_ir/run_stage01_matrix.py \
  --output-dir /private/tmp/th062-stage01-smoke \
  --pair th10:th11 \
  --pair th15:th12
```

Omit `--pair` to select all 72 ordered directions:

```sh
python3 scripts/ecl_ir/run_stage01_matrix.py \
  --output-dir /private/tmp/th062-stage01-matrix
```

The output directory must be new or empty. Each direction gets its own package,
checker report, Wine ECL tree, logs, and `result.json`. Top-level `summary.json`
and `summary.tsv` are updated after every completed direction, so an interrupted
run retains its completed evidence.

A direction fails when any pipeline command returns nonzero, checker analysis
is incomplete, a checker report is invalid, Wine/thecl emits a diagnostic such
as `error` or `too few arguments`, or an expected compiled ECL is absent/empty.
This deliberately treats thecl's return-code-zero diagnostics as failures.

Use `--dry-run` to validate all source/reference entry paths and inspect the
selected directions without creating the output directory.
