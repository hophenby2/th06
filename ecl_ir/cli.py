"""Stable entry point for ``python -m ecl_ir.cli``."""

from .commands.main import main


if __name__ == "__main__":
    raise SystemExit(main())
