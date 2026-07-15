# Legacy Schema-v1 Compatibility

These modules implement the schema-v1 object projection and legacy whole-file
transpiler. They remain loadable for `--legacy-patterns`, old `.eclir` files,
and compatibility diagnostics, but they do not own canonical lowering.

New semantic behavior must be implemented in `canonical/`, `analysis/`,
`dialects/`, or `target/`, not here.
