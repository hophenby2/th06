"""Archived TH12 stage06 to TH15 package rewrite.

This one-to-one migration predates the canonical lowering pipeline. It is kept
for historical comparison and is intentionally not registered as a CLI
command.
"""

from __future__ import annotations


def stage06_th12_to_th15_resources(kind: str) -> dict[str, list[str]]:
    if kind == "stage":
        return {
            "anim": ["enemy.anm", "st06enm.anm"],
            "ecli": ["default.ecl", "st06bs.ecl"],
        }
    return {}


def is_stage06_boss_function(name: str) -> bool:
    return name.startswith("Boss") or name in {"HPWait", "MBossCard1LaserHit"}


def emit_th15_stage06_mainboss_wrapper() -> list[str]:
    return [
        "void MainBoss()",
        "{",
        "    // th15 stage-side boss wrapper, mirroring th15 st06.decl",
        "    ins_519();",
        '    ins_301("Boss", 144.0f, -16.0f, 40, 1000, 1);',
        "    ins_519();",
        "+1:",
        "    ins_520();",
        "    ins_524(81);",
        "+60:",
        "    ins_518(2);",
        "    ins_519();",
        "    return;",
        "}",
    ]


def emit_transpile_selected_functions(
    program,
    objects,
    target: str,
    selected_functions: set[str],
    resources: dict[str, list[str]],
    header_note: str,
    include_stage_wrapper: bool = False,
) -> str:
    # Importing this archive must not add a dependency to the production CLI.
    from ...commands import main as legacy_cli

    lines = [
        f"// source: {program.source}",
        f"// source game: {program.game}",
        f"// target: {target}",
        header_note,
    ]
    for resource, entries in resources.items():
        if not legacy_cli.should_emit_resource(resource, target):
            continue
        quoted = "; ".join(f'"{entry}"' for entry in entries)
        lines.append(f"{resource} {{ {quoted}; }}")
    if include_stage_wrapper:
        lines.extend(
            [
                "// top-level declarations",
                "void MainBossSpell();",
                "",
                *emit_th15_stage06_mainboss_wrapper(),
            ]
        )

    by_function: dict[str, list[object]] = {}
    for obj in objects:
        function = getattr(obj, "function", "")
        if function in selected_functions:
            by_function.setdefault(function, []).append(obj)

    function_params = legacy_cli.inferred_function_params(program)
    global_function_rewrites = by_function.get("", [])
    for function in [
        func.name for func in program.functions if func.name in selected_functions
    ]:
        function_objects = [*by_function.get(function, []), *global_function_rewrites]
        if not function_objects:
            continue
        params = function_params.get(function, "")
        lines.extend(["", legacy_cli.target_function_header(function, params, target), "{"])
        body_lines = legacy_cli.emit_function_body(function_objects, target)
        body_lines = legacy_cli.apply_timeline_order_rewrites(
            body_lines,
            function_objects,
            target,
        )
        if params:
            body_lines = legacy_cli.drop_redeclared_param_vars(body_lines, params)
        lines.extend([*body_lines, "}"])
    return "\n".join(lines)


def emit_th12_stage06_to_th15_pair(program, objects) -> tuple[str, str]:
    function_names = {func.name for func in program.functions}
    boss_functions = {
        name for name in function_names if is_stage06_boss_function(name)
    }
    stage_functions = function_names - boss_functions
    stage = emit_transpile_selected_functions(
        program,
        objects,
        "th15",
        stage_functions,
        stage06_th12_to_th15_resources("stage"),
        "// th12 stage06 -> th15 stage-side lowering; resources follow th15 st06.decl",
        include_stage_wrapper=True,
    )
    boss = emit_transpile_selected_functions(
        program,
        objects,
        "th15",
        boss_functions,
        stage06_th12_to_th15_resources("boss"),
        "// th12 stage06 -> th15 boss-side lowering; ANM bank follows th15 st06bs.decl",
    )
    return stage, boss
