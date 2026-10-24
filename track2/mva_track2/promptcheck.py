"""Machine-check any LLM reply against the prompt pack's output contracts.

A prompt is only reusable if its output can be verified. A reply is accepted
only if it parses, cites known IDs, and meets the declared contract.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

from .pipeline import ROOT, array, choice, read_json, record, text, validate_bundle

PROMPTS = ROOT / "prompts"
KINDS = ("mechanism", "longlist", "claims", "falsifier")
MIN_LONGLIST = 8
MIN_AXES = 3
MAX_ADVANCE = 5
MAX_SUMMARY = 450
TIERS = {"FACT", "INFERENCE", "HYPOTHESIS"}
EFFECTS = {"LoF", "hypomorph", "GoF", "unknown"}
LESIONS = {"abundance", "catalysis", "localization", "unknown"}
VERDICTS = {"advance", "hold", "exclude"}
OVERCLAIM = re.compile(
    r"\b(cures?|cured|proven|proves|will (?:treat|work)|should be (?:given|prescribed)"
    r"|safe and effective)\b", re.I)
FENCE = re.compile(r"```(?:json)?\s*(.*?)```", re.S | re.I)


def extract_json(reply: str) -> Any:
    """Parse a bare JSON reply or the first parseable fenced block in a chatty one."""
    candidates = [reply.strip()] + [block.strip() for block in FENCE.findall(reply)]
    for candidate in candidates:
        if candidate[:1] in "{[":
            try:
                return json.loads(candidate)
            except json.JSONDecodeError:
                continue
    raise ValueError("reply contains no parseable JSON object or array")


def load_vetoes(path: Path = PROMPTS / "vetoes.json") -> dict[str, str]:
    raw = read_json(path)
    if not isinstance(raw, dict) or not raw:
        raise ValueError("vetoes.json: expected a nonempty object of code -> description")
    for code, description in raw.items():
        if not re.fullmatch(r"V_[A-Z_]+", code):
            raise ValueError(f"vetoes.json: invalid veto code {code!r}")
        text(description, f"vetoes.{code}")
    return raw


def known_ids(data_dir: Path) -> tuple[set[str], set[str]]:
    sources = {row["source_id"] for row in read_json(data_dir / "sources.json")}
    drugs = {row["drug_id"] for row in read_json(data_dir / "drugs.json")}
    return sources, drugs


def cited(value: Any, sources: set[str], ctx: str) -> list[str]:
    if not isinstance(value, list):
        raise ValueError(f"{ctx}: expected an array of source IDs")
    ids = [text(item, ctx) for item in value]
    unknown = sorted(set(ids) - sources)
    if unknown:
        raise ValueError(f"{ctx}: unknown source IDs {unknown}")
    return ids


def check_mechanism(raw: Any, sources: set[str]) -> list[str]:
    root = record(raw, {"variants", "chain", "lesion_type", "harm_directions", "unknowns"}, "response")
    for i, row in enumerate(array(root["variants"], "variants")):
        ctx = f"variants[{i}]"
        item = record(row, {"label", "effect_class", "tier", "source_ids"}, ctx)
        text(item["label"], ctx)
        choice(item["effect_class"], EFFECTS, ctx)
        tier = choice(item["tier"], TIERS, ctx)
        if tier == "FACT" and not cited(item["source_ids"], sources, ctx):
            raise ValueError(f"{ctx}: a FACT must cite at least one known source")
    steps = array(root["chain"], "chain")
    for i, row in enumerate(steps):
        ctx = f"chain[{i}]"
        item = record(row, {"step", "statement", "tier", "source_ids"}, ctx)
        if item["step"] != i + 1:
            raise ValueError(f"{ctx}: steps must be numbered 1..n in order")
        text(item["statement"], ctx)
        tier = choice(item["tier"], TIERS, ctx)
        if tier == "FACT" and not cited(item["source_ids"], sources, ctx):
            raise ValueError(f"{ctx}: a FACT must cite at least one known source")
        cited(item["source_ids"], sources, ctx)
    choice(root["lesion_type"], LESIONS, "lesion_type")
    for key in ("harm_directions", "unknowns"):
        for item in array(root[key], key):
            text(item, key)
    return []


def check_longlist(raw: Any, vetoes: dict[str, str]) -> list[str]:
    rows = array(record(raw, {"longlist"}, "response")["longlist"], "longlist")
    if len(rows) < MIN_LONGLIST:
        raise ValueError(f"longlist: need at least {MIN_LONGLIST} screened candidates, got {len(rows)}")
    names: set[str] = set()
    axes: set[str] = set()
    advancing = 0
    for i, row in enumerate(rows):
        ctx = f"longlist[{i}]"
        item = record(row, {"name", "axis", "verdict", "veto_code", "reason", "first_experiment"}, ctx)
        name = text(item["name"], ctx).lower()
        if name in names:
            raise ValueError(f"{ctx}: duplicate candidate {name}")
        names.add(name)
        axes.add(text(item["axis"], ctx).lower())
        text(item["reason"], ctx)
        verdict = choice(item["verdict"], VERDICTS, ctx)
        code = choice(item["veto_code"], set(vetoes) | {"none"}, ctx)
        text(item["first_experiment"], ctx, allow_empty=verdict != "advance")
        if (verdict == "advance") != (code == "none"):
            raise ValueError(f"{ctx}: advance requires veto_code none; hold/exclude require a veto code")
        advancing += verdict == "advance"
    if len(axes) < MIN_AXES:
        raise ValueError(f"longlist: candidates must span at least {MIN_AXES} axes, got {len(axes)}")
    if advancing > MAX_ADVANCE:
        raise ValueError(f"longlist: at most {MAX_ADVANCE} candidates may advance, got {advancing}")
    return []


def check_claims(raw: Any, data_dir: Path) -> list[str]:
    if not isinstance(raw, list):
        raise ValueError("claims: expected a JSON array of claim rows")
    if not raw:
        return ["no claims returned: nothing in the supplied sources was supportable"]
    existing = read_json(data_dir / "claims.json")
    validate_bundle(
        read_json(data_dir / "sources.json"), read_json(data_dir / "drugs.json"), existing + raw
    )
    warnings = []
    for row in raw:
        if len(row["summary"]) > MAX_SUMMARY:
            raise ValueError(f"{row['claim_id']}: summary exceeds {MAX_SUMMARY} characters")
        if OVERCLAIM.search(row["summary"]):
            warnings.append(f"{row['claim_id']}: overclaiming language in summary")
        if row["scope"] == "exact_variant":
            warnings.append(f"{row['claim_id']}: exact_variant carries full weight; verify by hand")
    return warnings


def check_falsifier(raw: Any, drugs: set[str]) -> list[str]:
    root = record(raw, {"kill_criteria", "confounds", "weakest_link", "experiment_zero"}, "response")
    for i, row in enumerate(array(root["kill_criteria"], "kill_criteria")):
        ctx = f"kill_criteria[{i}]"
        item = record(row, {"candidate", "measurement", "threshold", "decision_if_fail"}, ctx)
        choice(item["candidate"], drugs | {"all"}, ctx)
        text(item["measurement"], ctx)
        if not re.search(r"\d", text(item["threshold"], ctx)):
            raise ValueError(f"{ctx}.threshold: a pre-specified gate must be numeric")
        choice(item["decision_if_fail"], {"no-go", "defer"}, ctx)
    if len(array(root["confounds"], "confounds")) < 3:
        raise ValueError("confounds: list at least three ways a result could fake rescue")
    for item in root["confounds"]:
        text(item, "confounds")
    weakest = record(root["weakest_link"], {"claim", "why"}, "weakest_link")
    text(weakest["claim"], "weakest_link.claim")
    text(weakest["why"], "weakest_link.why")
    text(root["experiment_zero"], "experiment_zero")
    return []


def check(kind: str, reply: str, data_dir: Path = ROOT / "data") -> list[str]:
    """Validate a model reply; raise ValueError on any contract breach, else return warnings."""
    raw = extract_json(reply)
    sources, drugs = known_ids(data_dir)
    if kind == "mechanism":
        return check_mechanism(raw, sources)
    if kind == "longlist":
        return check_longlist(raw, load_vetoes())
    if kind == "claims":
        return check_claims(raw, data_dir)
    if kind == "falsifier":
        return check_falsifier(raw, drugs)
    raise ValueError(f"unknown kind {kind!r}; expected one of {KINDS}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("kind", choices=KINDS)
    parser.add_argument("reply", help="file holding the model reply, or - for stdin")
    parser.add_argument("--data-dir", type=Path, default=ROOT / "data")
    args = parser.parse_args()
    try:
        reply = sys.stdin.read() if args.reply == "-" else Path(args.reply).read_text(encoding="utf-8")
        warnings = check(args.kind, reply, args.data_dir)
    except (OSError, ValueError) as error:
        parser.exit(1, f"REJECTED: {error}\n")
    for warning in warnings:
        print(f"WARNING: {warning}")
    print(f"ACCEPTED: {args.kind} reply meets its output contract")


if __name__ == "__main__":
    main()
