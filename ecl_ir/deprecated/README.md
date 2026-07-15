# Deprecated Code

This directory is reserved for unreferenced one-off implementations. Code in
this directory must not be imported by the canonical, target, or compatibility
pipelines.

Archived one-offs:

- `oneoffs/th12_stage06_to_th15.py`: the removed
  `transpile-stage06-th15` pair-specific package rewrite.

Schema-v1 projections that are still part of the standalone envelope contract
live in `../legacy/`; the text backend still called by canonical lowering lives
in `../compat/`. Neither is dead code yet.
