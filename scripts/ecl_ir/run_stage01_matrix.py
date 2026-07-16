#!/usr/bin/env python3
"""Run the TH10-TH18 stage-01 cross-game package verification matrix."""

from __future__ import annotations

import argparse
import json
import os
import re
import shlex
import shutil
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Sequence


REPO_ROOT = Path(__file__).resolve().parents[2]
GAMES = tuple(f"th{version}" for version in range(10, 19))
ENTRY_NAMES = {
    "th10": "stage01.decl",
    "th11": "stage01.decl",
    "th12": "stage01.decl",
    "th13": "st01.decl",
    "th14": "st01.decl",
    "th15": "st01.decl",
    "th16": "st01.decl",
    "th17": "st01.decl",
    "th18": "st01.decl",
}
DEFAULT_THECL = Path(
    "/Users/happyelements/crack/thtkGUI-th20tr/thtk/thtk12/thecl.exe"
)
SCHEMA = "th062.stage01-cross-game-matrix"
SCHEMA_VERSION = 1

# thecl normally emits no text for a successful compilation. WINEDEBUG=-all
# suppresses Wine debug chatter, so any thecl-prefixed line is actionable.
LOG_FAILURE_PATTERNS = (
    ("thecl_diagnostic", re.compile(r"\bthecl(?:\.exe)?:", re.IGNORECASE)),
    ("too_few_arguments", re.compile(r"\btoo\s+few\s+arguments?\b", re.IGNORECASE)),
    ("too_many_arguments", re.compile(r"\btoo\s+many\s+arguments?\b", re.IGNORECASE)),
    ("error", re.compile(r"\berrors?\b", re.IGNORECASE)),
    ("fatal", re.compile(r"\bfatal\b", re.IGNORECASE)),
    ("failed", re.compile(r"\b(?:failed|failure)\b", re.IGNORECASE)),
    (
        "unsupported_or_unknown",
        re.compile(
            r"\b(?:not\s+(?:found|known|supported)|unsupported|unknown)\b",
            re.IGNORECASE,
        ),
    ),
)

SUMMARY_COLUMNS = (
    "source",
    "target",
    "status",
    "compile_rc",
    "compile_log_failures",
    "check_rc",
    "check_complete",
    "check_errors",
    "check_warnings",
    "states_explored",
    "wine_modules",
    "wine_failures",
    "reasons",
)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def command_text(command: Sequence[str]) -> str:
    return shlex.join(str(item) for item in command)


def parse_pair(value: str) -> tuple[str, str]:
    parts = value.lower().split(":")
    if len(parts) != 2 or any(part not in GAMES for part in parts):
        raise argparse.ArgumentTypeError(
            "pair must be SOURCE:TARGET using th10 through th18"
        )
    source, target = parts
    if source == target:
        raise argparse.ArgumentTypeError("source and target must differ")
    return source, target


def selected_pairs(explicit: Sequence[tuple[str, str]]) -> list[tuple[str, str]]:
    if not explicit:
        return [(source, target) for source in GAMES for target in GAMES if source != target]
    result: list[tuple[str, str]] = []
    seen: set[tuple[str, str]] = set()
    for pair in explicit:
        if pair not in seen:
            result.append(pair)
            seen.add(pair)
    return result


def entry_path(repo_root: Path, game: str) -> Path:
    path = repo_root / game / ENTRY_NAMES[game]
    if path.name == "default.decl":
        raise ValueError(f"default.decl cannot be a matrix entry: {game}")
    if not path.is_file():
        raise ValueError(f"stage-01 entry does not exist: {path}")
    return path


def resolve_executable(value: str, label: str) -> str:
    candidate = Path(value).expanduser()
    if candidate.parent != Path(".") or candidate.is_absolute():
        if not candidate.is_file():
            raise ValueError(f"{label} executable does not exist: {candidate}")
        return str(candidate.resolve())
    resolved = shutil.which(value)
    if resolved is None:
        raise ValueError(f"{label} executable is not on PATH: {value}")
    return resolved


def scan_log_failures(output: str) -> list[dict[str, str]]:
    failures: list[dict[str, str]] = []
    for line in output.splitlines():
        matched = [name for name, pattern in LOG_FAILURE_PATTERNS if pattern.search(line)]
        if matched:
            failures.append({"categories": ",".join(matched), "line": line})
    return failures


def run_command(
    command: Sequence[str],
    *,
    cwd: Path,
    timeout_seconds: int,
    environment: dict[str, str] | None = None,
) -> dict[str, Any]:
    started = time.monotonic()
    try:
        process = subprocess.run(
            [str(item) for item in command],
            cwd=cwd,
            env=environment,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout_seconds,
            check=False,
        )
        return {
            "command": [str(item) for item in command],
            "return_code": process.returncode,
            "stdout": process.stdout,
            "stderr": process.stderr,
            "timed_out": False,
            "duration_seconds": round(time.monotonic() - started, 3),
        }
    except subprocess.TimeoutExpired as exc:
        stdout = exc.stdout.decode("utf-8", "replace") if isinstance(exc.stdout, bytes) else (exc.stdout or "")
        stderr = exc.stderr.decode("utf-8", "replace") if isinstance(exc.stderr, bytes) else (exc.stderr or "")
        return {
            "command": [str(item) for item in command],
            "return_code": 124,
            "stdout": stdout,
            "stderr": stderr + f"\ncommand timed out after {timeout_seconds} seconds\n",
            "timed_out": True,
            "duration_seconds": round(time.monotonic() - started, 3),
        }


def write_process_log(path: Path, result: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = (
        f"command: {command_text(result['command'])}\n"
        f"return_code: {result['return_code']}\n"
        f"duration_seconds: {result['duration_seconds']}\n"
        "--- stdout ---\n"
        f"{result['stdout']}"
        "\n--- stderr ---\n"
        f"{result['stderr']}"
    )
    if not text.endswith("\n"):
        text += "\n"
    path.write_text(text, encoding="utf-8")


def checker_counts(report: dict[str, Any]) -> tuple[int, int]:
    diagnostics = report.get("diagnostics", [])
    if not isinstance(diagnostics, list):
        return 0, 0
    errors = sum(
        1 for item in diagnostics if isinstance(item, dict) and item.get("severity") == "error"
    )
    warnings = sum(
        1 for item in diagnostics if isinstance(item, dict) and item.get("severity") == "warning"
    )
    return errors, warnings


def run_direction(
    source: str,
    target: str,
    *,
    repo_root: Path,
    output_root: Path,
    python: str,
    wine: str,
    thecl: Path,
    timeout_seconds: int,
    state_budget: int,
    strict_lowering: bool,
) -> dict[str, Any]:
    direction_name = f"{source}_to_{target}"
    direction_dir = output_root / direction_name
    package_dir = direction_dir / "package"
    source_entry = entry_path(repo_root, source)
    target_entry = entry_path(repo_root, target)
    direction_dir.mkdir(parents=True, exist_ok=False)

    compile_command = [
        python,
        "-m",
        "ecl_ir.cli",
        "compile-package",
        str(source_entry),
        "--target",
        target,
        "--reference-package",
        str(target_entry),
        "--output-dir",
        str(package_dir),
    ]
    if not strict_lowering:
        compile_command.append("--allow-lossy")
    compile_result = run_command(
        compile_command,
        cwd=repo_root,
        timeout_seconds=timeout_seconds,
    )
    write_process_log(direction_dir / "compile-package.log", compile_result)
    compile_output = compile_result["stdout"] + "\n" + compile_result["stderr"]
    compile_log_failures = scan_log_failures(compile_output)

    generated_root = package_dir / target_entry.name
    reasons: list[str] = []
    if compile_result["return_code"] != 0:
        reasons.append("compile_return_code")
    if compile_log_failures:
        reasons.append("compile_log_diagnostic")
    if not generated_root.is_file():
        reasons.append("generated_root_missing")

    check_result: dict[str, Any] | None = None
    check_report: dict[str, Any] | None = None
    check_parse_error = ""
    check_errors = 0
    check_warnings = 0
    check_complete = False
    states_explored = 0
    if generated_root.is_file():
        check_command = [
            python,
            "-m",
            "ecl_ir.cli",
            "check-ecl",
            str(generated_root),
            "--game",
            target,
            "--reference-package",
            str(target_entry),
            "--difficulty",
            "ENHL",
            "--state-budget",
            str(state_budget),
            "--json",
        ]
        check_result = run_command(
            check_command,
            cwd=repo_root,
            timeout_seconds=timeout_seconds,
        )
        (direction_dir / "check-ecl.json").write_text(
            check_result["stdout"], encoding="utf-8"
        )
        write_process_log(direction_dir / "check-ecl.log", check_result)
        try:
            parsed = json.loads(check_result["stdout"])
            if not isinstance(parsed, dict):
                raise ValueError("checker JSON root is not an object")
            check_report = parsed
            check_errors, check_warnings = checker_counts(parsed)
            check_complete = parsed.get("analysis_complete") is True
            states_explored = int(parsed.get("states_explored", 0))
        except (json.JSONDecodeError, TypeError, ValueError) as exc:
            check_parse_error = str(exc)

        if check_result["return_code"] != 0:
            reasons.append("check_return_code")
        if check_parse_error:
            reasons.append("check_invalid_json")
        if check_report is not None and not check_complete:
            reasons.append("check_incomplete")

    wine_results: list[dict[str, Any]] = []
    if package_dir.is_dir():
        declarations = sorted(package_dir.rglob("*.decl"))
        if generated_root in declarations:
            declarations.remove(generated_root)
            declarations.insert(0, generated_root)
        wine_environment = os.environ.copy()
        wine_environment["WINEDEBUG"] = "-all"
        for declaration in declarations:
            relative = declaration.relative_to(package_dir)
            ecl_output = direction_dir / "wine-ecl" / relative.with_suffix(".ecl")
            log_output = direction_dir / "wine-logs" / relative.with_suffix(".log")
            ecl_output.parent.mkdir(parents=True, exist_ok=True)
            wine_command = [
                wine,
                str(thecl),
                "-c",
                target[2:],
                str(declaration),
                str(ecl_output),
            ]
            process = run_command(
                wine_command,
                cwd=declaration.parent,
                timeout_seconds=timeout_seconds,
                environment=wine_environment,
            )
            write_process_log(log_output, process)
            log_text = process["stdout"] + "\n" + process["stderr"]
            log_failures = scan_log_failures(log_text)
            output_size = ecl_output.stat().st_size if ecl_output.is_file() else 0
            failure_reasons: list[str] = []
            if process["return_code"] != 0:
                failure_reasons.append("return_code")
            if log_failures:
                failure_reasons.append("log_diagnostic")
            if output_size == 0:
                failure_reasons.append("missing_or_empty_output")
            wine_results.append(
                {
                    "module": relative.as_posix(),
                    "command": process["command"],
                    "return_code": process["return_code"],
                    "duration_seconds": process["duration_seconds"],
                    "output": ecl_output.relative_to(direction_dir).as_posix(),
                    "output_size": output_size,
                    "log": log_output.relative_to(direction_dir).as_posix(),
                    "log_failures": log_failures,
                    "failure_reasons": failure_reasons,
                    "status": "failed" if failure_reasons else "passed",
                }
            )
    if not wine_results:
        reasons.append("wine_no_modules")
    if any(item["status"] == "failed" for item in wine_results):
        reasons.append("wine_module_failure")

    result = {
        "source": source,
        "target": target,
        "source_entry": str(source_entry.relative_to(repo_root)),
        "target_reference": str(target_entry.relative_to(repo_root)),
        "generated_root": (
            generated_root.relative_to(direction_dir).as_posix()
            if generated_root.is_file()
            else ""
        ),
        "status": "failed" if reasons else "passed",
        "reasons": reasons,
        "compile": {
            "command": compile_result["command"],
            "return_code": compile_result["return_code"],
            "duration_seconds": compile_result["duration_seconds"],
            "log": "compile-package.log",
            "log_failures": compile_log_failures,
        },
        "check": {
            "command": check_result["command"] if check_result else [],
            "return_code": check_result["return_code"] if check_result else None,
            "duration_seconds": check_result["duration_seconds"] if check_result else 0,
            "analysis_complete": check_complete,
            "errors": check_errors,
            "warnings": check_warnings,
            "states_explored": states_explored,
            "parse_error": check_parse_error,
            "report": "check-ecl.json" if check_result else "",
            "log": "check-ecl.log" if check_result else "",
        },
        "wine": wine_results,
    }
    (direction_dir / "result.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return result


def tsv_value(value: object) -> str:
    return str(value).replace("\t", " ").replace("\r", " ").replace("\n", " ")


def summary_row(result: dict[str, Any]) -> dict[str, object]:
    check = result["check"]
    wine = result["wine"]
    return {
        "source": result["source"],
        "target": result["target"],
        "status": result["status"],
        "compile_rc": result["compile"]["return_code"],
        "compile_log_failures": len(result["compile"]["log_failures"]),
        "check_rc": check["return_code"] if check["return_code"] is not None else "",
        "check_complete": str(check["analysis_complete"]).lower(),
        "check_errors": check["errors"],
        "check_warnings": check["warnings"],
        "states_explored": check["states_explored"],
        "wine_modules": len(wine),
        "wine_failures": sum(item["status"] == "failed" for item in wine),
        "reasons": ",".join(result["reasons"]),
    }


def write_summaries(output_root: Path, summary: dict[str, Any]) -> None:
    json_tmp = output_root / "summary.json.tmp"
    json_path = output_root / "summary.json"
    json_tmp.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    json_tmp.replace(json_path)

    tsv_tmp = output_root / "summary.tsv.tmp"
    lines = ["\t".join(SUMMARY_COLUMNS)]
    for result in summary["directions"]:
        row = summary_row(result)
        lines.append("\t".join(tsv_value(row[column]) for column in SUMMARY_COLUMNS))
    tsv_tmp.write_text("\n".join(lines) + "\n", encoding="utf-8")
    tsv_tmp.replace(output_root / "summary.tsv")


def ensure_empty_output(path: Path) -> None:
    if path.exists():
        if not path.is_dir():
            raise ValueError(f"output path is not a directory: {path}")
        if any(path.iterdir()):
            raise ValueError(
                f"output directory must be empty so existing evidence is preserved: {path}"
            )
    else:
        path.mkdir(parents=True)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "convert, check, and Wine-compile TH10-TH18 stage01/st01 packages; "
            "default.decl is never used as the checker entry"
        )
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        required=True,
        help="new or empty directory for packages, logs, ECL files, and summaries",
    )
    parser.add_argument(
        "--pair",
        action="append",
        default=[],
        type=parse_pair,
        metavar="SOURCE:TARGET",
        help="run one ordered pair; repeat as needed (default: all 72 directions)",
    )
    parser.add_argument(
        "--repo-root", type=Path, default=REPO_ROOT, help=argparse.SUPPRESS
    )
    parser.add_argument("--python", default=sys.executable)
    parser.add_argument("--wine", default="wine")
    parser.add_argument("--thecl", type=Path, default=DEFAULT_THECL)
    parser.add_argument("--state-budget", type=int, default=200000)
    parser.add_argument("--timeout-seconds", type=int, default=600)
    parser.add_argument(
        "--strict-lowering",
        action="store_true",
        help="omit --allow-lossy when running compile-package",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="validate inputs and print the selected directions without writing output",
    )
    return parser


def validate_positive(value: int, label: str) -> None:
    if value <= 0:
        raise ValueError(f"{label} must be greater than zero")


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        repo_root = args.repo_root.expanduser().resolve()
        pairs = selected_pairs(args.pair)
        validate_positive(args.state_budget, "state budget")
        validate_positive(args.timeout_seconds, "timeout")
        for game in GAMES:
            entry_path(repo_root, game)
        python = resolve_executable(args.python, "Python")
        wine = resolve_executable(args.wine, "Wine")
        thecl = args.thecl.expanduser().resolve()
        if not thecl.is_file():
            raise ValueError(f"thecl executable does not exist: {thecl}")
        output_root = args.output_dir.expanduser().resolve()
    except ValueError as exc:
        print(f"run-stage01-matrix: {exc}", file=sys.stderr)
        return 2

    if args.dry_run:
        print("source\ttarget\tsource_entry\ttarget_reference")
        for source, target in pairs:
            print(
                f"{source}\t{target}\t"
                f"{entry_path(repo_root, source).relative_to(repo_root)}\t"
                f"{entry_path(repo_root, target).relative_to(repo_root)}"
            )
        print(f"directions={len(pairs)}")
        return 0

    try:
        ensure_empty_output(output_root)
    except (OSError, ValueError) as exc:
        print(f"run-stage01-matrix: {exc}", file=sys.stderr)
        return 2

    summary: dict[str, Any] = {
        "schema": SCHEMA,
        "schema_version": SCHEMA_VERSION,
        "started_at": utc_now(),
        "finished_at": "",
        "repo_root": str(repo_root),
        "output_dir": str(output_root),
        "entry_policy": "stage01/st01 main; never default",
        "difficulty": "ENHL",
        "allow_lossy": not args.strict_lowering,
        "state_budget": args.state_budget,
        "timeout_seconds": args.timeout_seconds,
        "wine": wine,
        "thecl": str(thecl),
        "planned_directions": len(pairs),
        "directions": [],
    }
    write_summaries(output_root, summary)

    try:
        for index, (source, target) in enumerate(pairs, start=1):
            print(f"[{index}/{len(pairs)}] {source} -> {target}", flush=True)
            result = run_direction(
                source,
                target,
                repo_root=repo_root,
                output_root=output_root,
                python=python,
                wine=wine,
                thecl=thecl,
                timeout_seconds=args.timeout_seconds,
                state_budget=args.state_budget,
                strict_lowering=args.strict_lowering,
            )
            summary["directions"].append(result)
            write_summaries(output_root, summary)
    except KeyboardInterrupt:
        summary["finished_at"] = utc_now()
        summary["interrupted"] = True
        write_summaries(output_root, summary)
        print("run-stage01-matrix: interrupted; partial summaries were retained", file=sys.stderr)
        return 130
    except (OSError, ValueError) as exc:
        summary["finished_at"] = utc_now()
        summary["runner_error"] = str(exc)
        write_summaries(output_root, summary)
        print(f"run-stage01-matrix: {exc}", file=sys.stderr)
        return 2

    summary["finished_at"] = utc_now()
    write_summaries(output_root, summary)
    failures = sum(result["status"] == "failed" for result in summary["directions"])
    print(
        f"summary directions={len(summary['directions'])} failures={failures} "
        f"json={output_root / 'summary.json'} tsv={output_root / 'summary.tsv'}"
    )
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
