from __future__ import annotations

import re
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ECLMAP_DIR = ROOT / "ecl_sources" / "eclmap"
REFERENCE_MD = ROOT / "ecl-reference-by-game.md"
ECL_BY_GAME_DIR = ROOT / "ecl-by-game"
THTK_THECL10 = ROOT.parent / "thtk" / "thecl" / "thecl10.c"


@dataclass(frozen=True)
class OpcodeInfo:
    game: str
    opcode: int
    name: str = ""
    signature: str = ""
    source: str = ""

    @property
    def arity(self) -> int | None:
        if not self.signature:
            return None
        if "*" in self.signature:
            return None
        return sum(1 for ch in self.signature if ch != "*")


def canonical_game(game: str) -> str:
    game = str(game).lower()
    if game in {"th06", "th07", "th08"}:
        return "th08"
    if game in {"th10", "th11"}:
        return game
    if game in {"th13", "th14", "th15", "th16", "th17", "th18"}:
        return game
    return game


def _parse_eclmap(path: Path, game: str) -> dict[int, OpcodeInfo]:
    infos: dict[int, OpcodeInfo] = {}
    if not path.exists():
        return infos
    text = path.read_text(errors="replace")
    if "<!DOCTYPE html" in text[:200] or "<html" in text[:200].lower():
        return infos
    section = ""
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if line.startswith("!"):
            section = line
            continue
        if section not in {"!ins_names", "!timeline_ins_names"}:
            continue
        parts = line.split(maxsplit=1)
        if not parts or not re.fullmatch(r"-?\d+", parts[0]):
            continue
        opcode = int(parts[0])
        name = parts[1].strip() if len(parts) > 1 else ""
        infos[opcode] = OpcodeInfo(game=game, opcode=opcode, name=name, source=str(path))
    return infos



def _signature_from_human_params(params: str) -> str:
    params = params.strip()
    if not params or params in {"—", "-"}:
        return ""
    if re.fullmatch(r"[SfmDotosx*]+(?:\s*\([^)]*\))?", params):
        return params.split(" ", 1)[0]
    signature: list[str] = []
    for raw_part in re.split(r"[,，]", params):
        part = raw_part.strip().lower()
        if not part or part in {"—", "-"}:
            continue
        if part.startswith('"') or "xxx" in part or "字符串" in part:
            signature.append("m")
        elif "float" in part or part.startswith("%") or "角" in part and "int" not in part:
            signature.append("f")
        elif "int" in part or part.startswith("$") or "编号" in part or "slot" in part or "num" in part or "time" in part or "mode" in part or "style" in part or "flag" in part:
            signature.append("S")
        else:
            signature.append("S")
    return "".join(signature)


def _parse_ecl_by_game_docs() -> dict[str, dict[int, OpcodeInfo]]:
    result: dict[str, dict[int, OpcodeInfo]] = {}
    if not ECL_BY_GAME_DIR.exists():
        return result
    for path in sorted(ECL_BY_GAME_DIR.glob("th*-ecl.md")):
        game = path.name.removesuffix("-ecl.md").replace("_", "").lower()
        in_table = False
        table_kind = ""
        for raw_line in path.read_text(errors="replace").splitlines():
            if raw_line.startswith("### "):
                in_table = "指令" in raw_line or "THBWiki" in raw_line
                table_kind = "priw8" if "指令：" in raw_line else "thbwiki"
                continue
            if not in_table or not raw_line.startswith("|"):
                continue
            cells = [cell.strip() for cell in raw_line.strip().strip("|").split("|")]
            if len(cells) < 3 or not re.fullmatch(r"\d+", cells[0]):
                continue
            opcode = int(cells[0])
            if cells[1] in {"助记名", "THBWiki 参数签名"}:
                continue
            if table_kind == "priw8" and len(cells) >= 4:
                name = cells[1]
                signature = _signature_from_human_params(cells[2])
                source = f"{path}:priw8"
            else:
                name = ""
                signature = _signature_from_human_params(cells[1])
                source = f"{path}:thbwiki"
            old = result.setdefault(game, {}).get(opcode)
            if old and old.name and old.signature:
                continue
            result[game][opcode] = OpcodeInfo(
                game=game,
                opcode=opcode,
                name=name or (old.name if old else ""),
                signature=signature or (old.signature if old else ""),
                source=source,
            )
    return result

def _parse_reference_md() -> dict[str, dict[int, OpcodeInfo]]:
    result: dict[str, dict[int, OpcodeInfo]] = {}
    if not REFERENCE_MD.exists():
        return result
    game = ""
    in_instruction_table = False
    for raw_line in REFERENCE_MD.read_text(errors="replace").splitlines():
        heading = re.match(r"^##\s+(TH\d+(?:\.\d+)?)\b", raw_line)
        if heading:
            game = heading.group(1).lower().replace(".", "")
            in_instruction_table = False
            continue
        if raw_line.startswith("### "):
            in_instruction_table = "指令" in raw_line
            continue
        if not game or not in_instruction_table or not raw_line.startswith("|"):
            continue
        cells = [cell.strip() for cell in raw_line.strip().strip("|").split("|")]
        if len(cells) < 3 or not re.fullmatch(r"\d+", cells[0]):
            continue
        signature = "" if cells[2] in {"—", "-"} else cells[2].split(" ", 1)[0]
        result.setdefault(game, {})[int(cells[0])] = OpcodeInfo(
            game=game,
            opcode=int(cells[0]),
            name=cells[1],
            signature=signature,
            source=str(REFERENCE_MD),
        )
    return result


def _parse_thtk_format_array(array_name: str, game: str) -> dict[int, OpcodeInfo]:
    infos: dict[int, OpcodeInfo] = {}
    if not THTK_THECL10.exists():
        return infos
    text = THTK_THECL10.read_text(errors="replace")
    match = re.search(rf"static const id_format_pair_t {array_name}\[\]\s*=\s*\{{(.*?)\n\}};", text, re.S)
    if not match:
        return infos
    for opcode, signature in re.findall(r"\{\s*(\d+)\s*,\s*\"([^\"]*)\"\s*\}", match.group(1)):
        infos[int(opcode)] = OpcodeInfo(game=game, opcode=int(opcode), signature=signature, source=f"{THTK_THECL10}:{array_name}")
    return infos


def _parse_thtk_formats() -> dict[str, dict[int, OpcodeInfo]]:
    arrays = {
        "th10": ["th10_fmts"],
        "th11": ["th11_fmts", "th10_fmts"],
        "th12": ["th12_fmts", "th11_fmts", "th10_fmts"],
        "th13": ["th13_fmts", "th128_fmts", "th125_fmts", "th12_fmts", "th11_fmts", "th10_fmts"],
        "th14": ["th14_fmts", "th13_fmts", "th128_fmts", "th125_fmts", "th12_fmts", "th11_fmts", "th10_fmts"],
        "th15": ["th15_fmts", "th143_fmts", "th14_fmts", "th13_fmts", "th128_fmts", "th125_fmts", "th12_fmts", "th11_fmts", "th10_fmts"],
        "th16": ["th16_fmts", "th15_fmts", "th143_fmts", "th14_fmts", "th13_fmts", "th128_fmts", "th125_fmts", "th12_fmts", "th11_fmts", "th10_fmts"],
        "th17": ["th17_fmts", "th165_fmts", "th16_fmts", "th15_fmts", "th143_fmts", "th14_fmts", "th13_fmts", "th128_fmts", "th125_fmts", "th12_fmts", "th11_fmts", "th10_fmts"],
        "th18": ["th18_fmts", "th17_fmts", "th165_fmts", "th16_fmts", "th15_fmts", "th143_fmts", "th14_fmts", "th13_fmts", "th128_fmts", "th125_fmts", "th12_fmts", "th11_fmts", "th10_fmts"],
    }
    result: dict[str, dict[int, OpcodeInfo]] = {}
    for game, chain in arrays.items():
        merged: dict[int, OpcodeInfo] = {}
        for array in chain:
            for opcode, info in _parse_thtk_format_array(array, game).items():
                merged.setdefault(opcode, OpcodeInfo(game=game, opcode=opcode, signature=info.signature, source=info.source))
        if merged:
            result[game] = merged
    return result


@lru_cache(maxsize=1)
def opcode_reference() -> dict[str, dict[int, OpcodeInfo]]:
    result: dict[str, dict[int, OpcodeInfo]] = {}
    for path in sorted(ECLMAP_DIR.glob("th*.eclm")):
        game = path.stem.lower().replace(".", "")
        parsed = _parse_eclmap(path, game)
        if parsed:
            result.setdefault(game, {}).update(parsed)
    for table_source in (_parse_reference_md(), _parse_ecl_by_game_docs()):
        for game, table in table_source.items():
            target = result.setdefault(game, {})
            for opcode, info in table.items():
                old = target.get(opcode)
                if old:
                    target[opcode] = OpcodeInfo(game=game, opcode=opcode, name=info.name or old.name, signature=info.signature or old.signature, source=f"{old.source}; {info.source}")
                else:
                    target[opcode] = info
    for game, table in _parse_thtk_formats().items():
        target = result.setdefault(game, {})
        for opcode, info in table.items():
            old = target.get(opcode)
            if old and old.signature and ":priw8" in old.source:
                signature = old.signature
            else:
                signature = info.signature
            target[opcode] = OpcodeInfo(game=game, opcode=opcode, name=(old.name if old else ""), signature=signature, source=f"{old.source}; {info.source}" if old else info.source)
    if "th10" in result and "th11" not in result:
        result["th11"] = dict(result["th10"])
    if "th10" in result and "th11" in result:
        for opcode, th11_info in result["th11"].items():
            th10_info = result["th10"].get(opcode)
            if th10_info and not th10_info.name and th11_info.name:
                result["th10"][opcode] = OpcodeInfo(
                    game="th10",
                    opcode=opcode,
                    name=th11_info.name,
                    signature=th10_info.signature or th11_info.signature,
                    source=f"{th10_info.source}; name inherited from th11 same-generation table",
                )
    if "th12" in result:
        info = result["th12"].get(445)
        if info and info.name == "laserCancel":
            result["th12"][445] = OpcodeInfo(
                game="th12",
                opcode=445,
                name=info.name,
                signature="",
                source=f"{info.source}; signature forced from no-arg laser cancel semantic",
            )
        info = result["th12"].get(405)
        if info and info.name == "moveLimitReset":
            result["th12"][405] = OpcodeInfo(
                game="th12",
                opcode=405,
                name=info.name,
                signature="",
                source=f"{info.source}; signature forced from no-arg move limit reset semantic",
            )
        for opcode, signature in ((523, "Sff"), (524, "Sf"), (525, "Sff")):
            info = result["th12"].get(opcode)
            if info:
                result["th12"][opcode] = OpcodeInfo(
                    game="th12",
                    opcode=opcode,
                    name=info.name,
                    signature=signature,
                    source=f"{info.source}; signature forced from ecl3 bullet origin semantic",
                )
        # TH13+ kept several TH12 opcodes with identical signatures but the scraped
        # eclmap rows are blank.  Inherit only exact-signature matches so op_key
        # generation stays semantic without inventing pairwise conversions.
        inherited_exact_names = {"anmOnEt", "anmRotate", "zIndex", "hitSound"}
        for game in ("th13", "th14", "th15", "th16", "th165", "th17", "th18", "th185"):
            if game not in result:
                continue
            existing_names = {info.name for info in result[game].values() if info.name}
            for opcode, th12_info in result["th12"].items():
                if th12_info.name not in inherited_exact_names:
                    continue
                if th12_info.name in existing_names:
                    continue
                info = result[game].get(opcode)
                if info and not info.name and th12_info.name and info.signature == th12_info.signature:
                    result[game][opcode] = OpcodeInfo(
                        game=game,
                        opcode=opcode,
                        name=th12_info.name,
                        signature=info.signature,
                        source=f"{info.source}; name inherited from th12 exact-signature table",
                    )
    for game in ("th13", "th14", "th15", "th16", "th165", "th17", "th18", "th185"):
        if game not in result:
            continue
        for opcode in (12, 13, 14):
            info = result[game].get(opcode)
            if info:
                result[game][opcode] = OpcodeInfo(
                    game=game,
                    opcode=opcode,
                    name=info.name,
                    signature="ot",
                    source=f"{info.source}; signature forced to thecl format ot",
                )
        info = result[game].get(17)
        if info and info.name == "killAsync":
            result[game][17] = OpcodeInfo(
                game=game,
                opcode=17,
                name=info.name,
                signature="S",
                source=f"{info.source}; signature forced from original TH13+ usage",
            )
        for opcode in (505, 506, 509, 513, 519, 520, 523, 525, 545):
            info = result[game].get(opcode)
            if info:
                result[game][opcode] = OpcodeInfo(
                    game=game,
                    opcode=opcode,
                    name=info.name,
                    signature="",
                    source=f"{info.source}; signature forced from no-arg unit/boss semantic",
                )
        info = result[game].get(512)
        if info and info.name == "setBoss":
            result[game][512] = OpcodeInfo(
                game=game,
                opcode=512,
                name=info.name,
                signature="S",
                source=f"{info.source}; signature forced from setBoss semantic layout",
            )
        info = result[game].get(514)
        if info and info.name == "setInterrupt":
            result[game][514] = OpcodeInfo(
                game=game,
                opcode=514,
                name=info.name,
                signature="SSSm",
                source=f"{info.source}; signature forced from setInterrupt semantic layout",
            )
        for opcode in (537, 538, 539):
            info = result[game].get(opcode)
            if info and info.name in {"spell", "spell2", "spell3"}:
                result[game][opcode] = OpcodeInfo(
                    game=game,
                    opcode=opcode,
                    name=info.name,
                    signature="SSSm",
                    source=f"{info.source}; signature forced from spell semantic layout",
                )
    return result



@lru_cache(maxsize=1)
def thtk_supported_opcodes() -> dict[str, set[int]]:
    return {game: set(table) for game, table in _parse_thtk_formats().items()}


def is_opcode_supported(game: str, opcode: int) -> bool:
    game = canonical_game(game)
    supported = thtk_supported_opcodes().get(game)
    if supported is not None:
        return int(opcode) in supported
    return opcode_info(game, opcode) is not None


def opcode_info(game: str, opcode: int) -> OpcodeInfo | None:
    return opcode_reference().get(canonical_game(game), {}).get(int(opcode))


def opcode_name(game: str, opcode: int, default: str = "") -> str:
    info = opcode_info(game, opcode)
    return info.name if info and info.name else default


def opcode_signature(game: str, opcode: int) -> str:
    info = opcode_info(game, opcode)
    return info.signature if info else ""


def opcode_arity(game: str, opcode: int) -> int | None:
    info = opcode_info(game, opcode)
    return info.arity if info else None


def validate_opcode_args(game: str, opcode: int, args: list[object]) -> str | None:
    if not is_opcode_supported(game, opcode):
        return f"{game} ins_{opcode} is not in thecl format table"
    signature = opcode_signature(game, opcode)
    arity = opcode_arity(game, opcode)
    if arity is None:
        return None
    actual = len(args)
    if actual != arity:
        name = opcode_name(game, opcode, f"ins_{opcode}")
        return f"{game} ins_{opcode} {name} expects {arity} args ({signature}), got {actual}"
    concrete_signature = [ch for ch in signature if ch != "*"]
    for index, (expected, value) in enumerate(zip(concrete_signature, args), start=1):
        if not argument_matches_type(str(value), expected):
            name = opcode_name(game, opcode, f"ins_{opcode}")
            return f"{game} ins_{opcode} {name} parameter {index} expects {expected}, got {argument_type_name(str(value))}"
    return None


def argument_type_name(value: str) -> str:
    text = value.strip()
    if text.startswith('"') and text.endswith('"'):
        return "m"
    if re.fullmatch(r"[A-Za-z_]\w*", text):
        return "o"
    if re.fullmatch(r"[-+]?\d+(?:\.\d+)?f|[-+]?\d*\.\d+", text):
        return "f"
    if re.fullmatch(r"\[-?\d+(?:\.0f)?\]", text):
        return "S" if ".0f" not in text else "f-var"
    if re.fullmatch(r"[-+]?\d+", text):
        return "S"
    if text.startswith("$"):
        return "S"
    if text.startswith("%"):
        return "f"
    return "expr"


def argument_matches_type(value: str, expected: str) -> bool:
    actual = argument_type_name(value)
    if expected in {"S", "D", "H"}:
        return actual in {"S", "expr"}
    if expected == "f":
        return actual in {"f", "f-var", "expr"}
    if expected == "m":
        return actual in {"m", "expr"}
    if expected in {"o", "t"}:
        return actual in {"o", "S", "expr"}
    return True
