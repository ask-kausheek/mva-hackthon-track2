"""Validate curated evidence, prioritize research hypotheses, and report provenance."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
SCOPES = {
    "exact_variant", "same_gene_other_variant", "same_gene_nonvariant",
    "other_disease", "general", "regulatory",
}
DIMENSIONS = {"mechanism", "translation", "functional_rescue", "safety"}
RANKABLE = "conditional_research"


@dataclass(frozen=True)
class Source:
    source_id: str
    title: str
    url: str
    kind: str
    study_id: str
    accessed_on: str


@dataclass(frozen=True)
class Drug:
    drug_id: str
    name: str
    approved_indication: str
    approval_status: str
    approval_source_id: str
    mechanism_id: str
    mechanism_description: str
    mechanism_claim_groups: tuple[tuple[str, ...], ...]
    variant_fit: str
    variant_fit_note: str
    exposure_status: str
    safety_status: str
    safety_note: str


@dataclass(frozen=True)
class Claim:
    claim_id: str
    drug_ids: tuple[str, ...]
    source_id: str
    dimension: str
    relation: str
    scope: str
    summary: str


@dataclass(frozen=True)
class Bundle:
    sources: dict[str, Source]
    drugs: dict[str, Drug]
    claims: tuple[Claim, ...]


@dataclass(frozen=True)
class Settings:
    team: str
    scope_weights: dict[str, float]
    profiles: dict[str, dict[str, float]]


@dataclass(frozen=True)
class Result:
    drug_id: str
    name: str
    status: str
    reason: str
    mechanism_support: float
    translation_support: float
    bridge_support: float
    functional_rescue_support: float
    priority_index: float
    primary_studies: tuple[str, ...]
    claim_ids: tuple[str, ...]
    rank: int | None = None


def read_json(path: Path) -> Any:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def record(value: Any, fields: set[str], context: str) -> dict[str, Any]:
    if not isinstance(value, dict) or set(value) != fields:
        raise ValueError(f"{context}: expected exactly these fields: {sorted(fields)}")
    return value


def text(value: Any, context: str, allow_empty: bool = False) -> str:
    if not isinstance(value, str) or (not value.strip() and not allow_empty):
        raise ValueError(f"{context}: expected a nonempty string")
    if any(char in value for char in "\r\n"):
        raise ValueError(f"{context}: strings must be single-line")
    return value.strip()


def choice(value: Any, allowed: set[str], context: str) -> str:
    value = text(value, context)
    if value not in allowed:
        raise ValueError(f"{context}: must be one of {sorted(allowed)}")
    return value


def array(value: Any, context: str) -> list[Any]:
    if not isinstance(value, list) or not value:
        raise ValueError(f"{context}: expected a nonempty array")
    return value


def validate_bundle(raw_sources: Any, raw_drugs: Any, raw_claims: Any) -> Bundle:
    sources: dict[str, Source] = {}
    for index, raw in enumerate(array(raw_sources, "sources")):
        ctx = f"sources[{index}]"
        row = record(raw, set(Source.__dataclass_fields__), ctx)
        values = {key: text(value, f"{ctx}.{key}") for key, value in row.items()}
        choice(values["kind"], {"primary", "regulatory", "review"}, f"{ctx}.kind")
        if urlparse(values["url"]).scheme != "https" or not urlparse(values["url"]).netloc:
            raise ValueError(f"{ctx}.url: expected an absolute HTTPS URL")
        if date.fromisoformat(values["accessed_on"]).isoformat() != values["accessed_on"]:
            raise ValueError(f"{ctx}.accessed_on: expected YYYY-MM-DD")
        source = Source(**values)
        if source.source_id in sources:
            raise ValueError(f"Duplicate source_id: {source.source_id}")
        sources[source.source_id] = source

    drugs: dict[str, Drug] = {}
    for index, raw in enumerate(array(raw_drugs, "drugs")):
        ctx = f"drugs[{index}]"
        row = record(raw, set(Drug.__dataclass_fields__), ctx)
        values = {
            key: text(value, f"{ctx}.{key}", allow_empty=key == "approval_source_id")
            for key, value in row.items() if key != "mechanism_claim_groups"
        }
        raw_groups = row["mechanism_claim_groups"]
        if not isinstance(raw_groups, list):
            raise ValueError(f"{ctx}.mechanism_claim_groups: expected an array")
        groups = tuple(
            tuple(text(item, ctx) for item in array(group, ctx)) for group in raw_groups
        )
        if any(len(set(group)) != len(group) for group in groups):
            raise ValueError(f"{ctx}: duplicate mechanism claim references")
        choice(values["approval_status"], {"approved", "unverified", "not_approved"}, ctx)
        choice(values["variant_fit"], {"unresolved", "supported", "contradicted"}, ctx)
        choice(values["exposure_status"], {"unresolved", "supported", "contradicted"}, ctx)
        choice(values["safety_status"], {"unresolved", "hold"}, ctx)
        source_id = values["approval_source_id"]
        if source_id and source_id not in sources:
            raise ValueError(f"{ctx}: unknown approval source {source_id}")
        if values["approval_status"] == "approved":
            if not source_id or sources[source_id].kind != "regulatory":
                raise ValueError(f"{ctx}: approved status requires a regulatory source")
        drug = Drug(**values, mechanism_claim_groups=groups)
        if drug.drug_id in drugs:
            raise ValueError(f"Duplicate drug_id: {drug.drug_id}")
        drugs[drug.drug_id] = drug

    claims: list[Claim] = []
    seen: set[str] = set()
    for index, raw in enumerate(array(raw_claims, "claims")):
        ctx = f"claims[{index}]"
        row = record(raw, set(Claim.__dataclass_fields__), ctx)
        drug_ids = tuple(text(item, ctx) for item in array(row["drug_ids"], ctx))
        if len(set(drug_ids)) != len(drug_ids) or set(drug_ids) - drugs.keys():
            raise ValueError(f"{ctx}: duplicate or unknown drug IDs")
        source_id = text(row["source_id"], f"{ctx}.source_id")
        if source_id not in sources:
            raise ValueError(f"{ctx}: unknown source {source_id}")
        scope = choice(row["scope"], SCOPES, ctx)
        if (scope == "regulatory") != (sources[source_id].kind == "regulatory"):
            raise ValueError(f"{ctx}: regulatory source and scope must agree")
        claim = Claim(
            claim_id=text(row["claim_id"], ctx), drug_ids=drug_ids,
            source_id=source_id,
            dimension=choice(row["dimension"], DIMENSIONS, ctx),
            relation=choice(row["relation"], {"supports", "contradicts", "context"}, ctx),
            scope=scope, summary=text(row["summary"], ctx),
        )
        if claim.claim_id in seen:
            raise ValueError(f"Duplicate claim_id: {claim.claim_id}")
        seen.add(claim.claim_id)
        claims.append(claim)
    by_id = {claim.claim_id: claim for claim in claims}
    for drug in drugs.values():
        for group in drug.mechanism_claim_groups:
            for claim_id in group:
                claim = by_id.get(claim_id)
                if (
                    claim is None or drug.drug_id not in claim.drug_ids
                    or claim.dimension != "mechanism" or claim.relation != "supports"
                    or sources[claim.source_id].kind != "primary"
                ):
                    raise ValueError(
                        f"{drug.drug_id}: required mechanism link {claim_id} must reference "
                        "a primary supporting mechanism claim mapped to this drug"
                    )
    return Bundle(sources, drugs, tuple(claims))


def number(value: Any, context: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (float, int)):
        raise ValueError(f"{context}: expected a number")
    if not math.isfinite(value) or not 0 <= value <= 1:
        raise ValueError(f"{context}: expected a finite number in [0, 1]")
    return float(value)


def validate_settings(raw: Any) -> Settings:
    row = record(raw, {"team", "scope_weights", "profiles"}, "settings")
    weights = record(row["scope_weights"], SCOPES, "scope_weights")
    scope_weights = {key: number(value, key) for key, value in weights.items()}
    if scope_weights["regulatory"] != 0:
        raise ValueError("Regulatory approval cannot contribute efficacy/bridge points")
    if not isinstance(row["profiles"], dict) or "baseline" not in row["profiles"]:
        raise ValueError("profiles: a baseline profile is required")
    profiles = {}
    for name, values in row["profiles"].items():
        text(name, "profile name")
        values = record(values, {"bridge", "functional_rescue"}, name)
        profile = {key: number(value, f"{name}.{key}") for key, value in values.items()}
        if not math.isclose(sum(profile.values()), 1.0, abs_tol=1e-9):
            raise ValueError(f"{name}: profile weights must sum to 1")
        profiles[name] = profile
    return Settings(text(row["team"], "team"), scope_weights, profiles)


def load_inputs(data_dir: Path, config_path: Path) -> tuple[Bundle, Settings]:
    bundle = validate_bundle(
        read_json(data_dir / "sources.json"),
        read_json(data_dir / "drugs.json"),
        read_json(data_dir / "claims.json"),
    )
    return bundle, validate_settings(read_json(config_path))


def evaluate(
    bundle: Bundle, settings: Settings, profile_name: str = "baseline",
    excluded_studies: frozenset[str] = frozenset(),
) -> list[Result]:
    profile = settings.profiles[profile_name]
    results = []
    for drug in bundle.drugs.values():
        claims = [
            claim for claim in bundle.claims
            if drug.drug_id in claim.drug_ids
            and bundle.sources[claim.source_id].study_id not in excluded_studies
        ]
        support = {"mechanism": 0.0, "translation": 0.0, "functional_rescue": 0.0}
        studies: set[str] = set()
        for claim in claims:
            source = bundle.sources[claim.source_id]
            if source.kind != "primary" or claim.relation != "supports":
                continue
            if claim.dimension not in support:
                continue
            if claim.dimension == "functional_rescue" and claim.scope not in {
                "exact_variant", "same_gene_other_variant", "same_gene_nonvariant",
            }:
                continue
            strength = settings.scope_weights[claim.scope]
            # Maxima prevent duplicated claims, reviews and study mirrors adding points.
            support[claim.dimension] = max(support[claim.dimension], strength)
            if strength:
                studies.add(source.study_id)
        active_claims = {claim.claim_id: claim for claim in claims}
        group_support = [
            max(
                (settings.scope_weights[active_claims[claim_id].scope]
                 for claim_id in group if claim_id in active_claims),
                default=0.0,
            )
            for group in drug.mechanism_claim_groups
        ]
        # All declared mechanistic steps are required; unrelated gene evidence cannot substitute.
        support["mechanism"] = min(group_support, default=0.0)
        bridge = min(support["mechanism"], support["translation"])
        index = 100 * (
            profile["bridge"] * bridge
            + profile["functional_rescue"] * support["functional_rescue"]
        )
        conflicts = any(
            claim.relation == "contradicts"
            and claim.dimension in {"mechanism", "translation", "functional_rescue"}
            for claim in claims
        )
        if drug.approval_status != "approved":
            status, reason = "ineligible_approval", "Approved medication status is not established."
        elif "contradicted" in {drug.variant_fit, drug.exposure_status}:
            status, reason = "held_incompatible", "Curated variant or exposure incompatibility needs resolution."
        elif drug.safety_status == "hold":
            status, reason = "held_safety", drug.safety_note
        elif conflicts:
            status, reason = "held_conflicting_evidence", "Contradictory claims require manual adjudication."
        elif bridge == 0 and support["functional_rescue"] == 0:
            status, reason = "deferred_no_bridge_evidence", "No complete primary-evidence bridge in this snapshot."
        else:
            status, reason = RANKABLE, "Research prioritization only; variant fit, exposure and safety require review."
        results.append(Result(
            drug.drug_id, drug.name, status, reason,
            support["mechanism"], support["translation"], bridge,
            support["functional_rescue"], round(index, 6),
            tuple(sorted(studies)), tuple(sorted(claim.claim_id for claim in claims)),
        ))

    results.sort(key=lambda row: (row.status != RANKABLE, -row.priority_index, row.drug_id))
    score_ranks: dict[float, int] = {}
    ranked = []
    for result in results:
        rank = None
        if result.status == RANKABLE:
            if result.priority_index not in score_ranks:
                score_ranks[result.priority_index] = len(score_ranks) + 1
            rank = score_ranks[result.priority_index]
        ranked.append(Result(**{**result.__dict__, "rank": rank}))
    return ranked


def sensitivity(bundle: Bundle, settings: Settings) -> list[dict[str, Any]]:
    rows = []
    primary_studies = sorted({
        source.study_id for source in bundle.sources.values() if source.kind == "primary"
    })
    for profile in settings.profiles:
        for study in [None, *primary_studies]:
            excluded = frozenset({study}) if study else frozenset()
            for result in evaluate(bundle, settings, profile, excluded):
                rows.append({
                    "profile": profile, "excluded_study": study or "",
                    "drug_id": result.drug_id, "status": result.status,
                    "research_priority_rank": result.rank if result.rank is not None else "",
                    "priority_index": result.priority_index if result.rank is not None else "",
                })
    return rows


def csv_cell(value: Any) -> Any:
    if isinstance(value, str) and value.lstrip().startswith(("=", "+", "-", "@")):
        return "'" + value
    return value


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"Refusing to emit an empty table: {path.name}")
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows({key: csv_cell(value) for key, value in row.items()} for row in rows)


def md(value: str) -> str:
    return value.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("|", "\\|")


def render_report(
    bundle: Bundle, settings: Settings, results: list[Result],
    scenarios: list[dict[str, Any]], snapshot_id: str,
) -> str:
    lines = [
        "# Track 2 Research Evidence Report", "",
        f"**Team:** {md(settings.team)}  ",
        "**Status:** Exploratory research prototype; not a treatment recommendation.  ",
        f"**Snapshot:** `{snapshot_id}`", "",
        "## Scope", "",
        "This report summarizes a manually curated, non-exhaustive public-evidence snapshot.",
        "It is not a validated drug screen, clinical safety clearance, or evidence that a",
        "medicine works in MVA. No patient treatment or wet-lab experiments were performed.",
        "Market approval applies only to the cited indication and formulation, not this case.", "",
        "## Conditional research shortlist", "",
        "| Priority (ties retained) | Drug | Status | Evidence index / 100 | BUBR1 functional-rescue evidence |",
        "|---|---|---|---:|---|",
    ]
    for row in results:
        index = f"{row.priority_index:.2f}" if row.rank is not None else "Not ranked"
        rescue = "Present in curated ledger; inspect scope" if row.functional_rescue_support else "Not found in snapshot"
        lines.append(f"| {row.rank or '-'} | {md(row.name)} | {row.status} | {index} | {rescue} |")
    lines += [
        "", "## Interpretation", "",
        "Ranks prioritize further literature and experimental work, not administration.",
        "Zero component support means missing qualifying evidence, not proof of no effect.",
        "Ties are genuine; alphabetical display order does not break them.",
        "A claim associated with a drug can describe a proposed mechanistic bridge rather",
        "than an experiment testing that drug. Read the claim summary and scope.", "",
        "## Per-hypothesis rationale and gaps", "",
    ]
    for result in results:
        drug = bundle.drugs[result.drug_id]
        label = bundle.sources.get(drug.approval_source_id)
        approval = f"[{label.source_id}]({label.url})" if label else "Not established"
        lines += [
            f"### {md(drug.name)}", "",
            f"**Approved indication:** {md(drug.approved_indication)} ({approval})", "",
            f"**Proposed mechanism:** {md(drug.mechanism_description)}", "",
            f"**Disposition:** {md(result.reason)}", "",
            f"**Variant fit ({drug.variant_fit}):** {md(drug.variant_fit_note)}", "",
            f"**Exposure relevance:** {drug.exposure_status}.", "",
            f"**Safety ({drug.safety_status}):** {md(drug.safety_note)}", "",
            "| Claim | Domain / relation / scope | Source |",
            "|---|---|---|",
        ]
        for claim in bundle.claims:
            if drug.drug_id not in claim.drug_ids:
                continue
            source = bundle.sources[claim.source_id]
            lines.append(
                f"| {md(claim.summary)} | {claim.dimension} / {claim.relation} / {claim.scope} "
                f"| [{source.source_id}]({source.url}) |"
            )
        lines.append("")
    baseline = settings.profiles["baseline"]
    lines += [
        "## Transparent prioritization", "",
        "Only primary supporting claims receive numeric scope discounts. Regulatory",
        "labels establish approval and safety context; reviews and labels add no points.",
        "Each declared mechanism step uses its strongest qualifying evidence; the weakest",
        "required step controls mechanism support. Other components use maxima, not citation counts.",
        "The evidence bridge uses the weaker of mechanism and drug-translation support.", "",
        "```text",
        "mechanism_support = min(max(support for each required mechanism step))",
        "bridge = min(mechanism_support, translation_support)",
        f"index = 100 * ({baseline['bridge']} * bridge + "
        f"{baseline['functional_rescue']} * functional_rescue_support)",
        "```", "",
        "Discounts and profile weights are explicit human heuristics, not learned or",
        "calibrated probabilities and not the judges' rubric. There is no Top-K min-max",
        "normalization. Safety holds, incompatible evidence and unverified approval",
        "cannot be overridden by a high index.", "",
        "| Evidence scope | Discount |", "|---|---:|",
    ]
    lines += [f"| {scope} | {weight:g} |" for scope, weight in settings.scope_weights.items()]
    lines += [
        "", "## Sensitivity and fragility", "",
        "All weight profiles are crossed with leave-one-primary-study-out ablations.",
        "All claims from a study are removed together, including mirrored source entries.",
        "Approval labels and curated safety holds remain in place. This tests dependence",
        "on the small curated corpus, not predictive accuracy or out-of-sample performance.", "",
        "| Drug | Scenarios rankable / total | Top-priority scenarios (including ties) |",
        "|---|---:|---:|",
    ]
    for result in results:
        group = [row for row in scenarios if row["drug_id"] == result.drug_id]
        rankable = sum(row["status"] == RANKABLE for row in group)
        top = sum(row["research_priority_rank"] == 1 for row in group)
        lines.append(f"| {md(result.name)} | {rankable}/{len(group)} | {top}/{len(group)} |")
    lines += [
        "", "## Required next evidence", "",
        "- Reverify transcript-specific allele annotation, residual protein function and phase.",
        "- Establish current renal function, oncology context and exposure feasibility through qualified review.",
        "- Separate normal-cell functional rescue from tumor-cell survival or treatment interference.",
        "- Test functional chromosome-segregation endpoints, not protein abundance alone.",
        "- Distinguish genuine rescue from cell-cycle arrest or selective death of abnormal cells.",
        "- Obtain genetics/pharmacology review before any clinical interpretation.", "",
        "## Reproducibility and limitations", "",
        "The pipeline is offline and uses the Python standard library. Evidence inclusion,",
        "scope labels and safety dispositions were manually curated with AI assistance.",
        "Automated output does not imply automated discovery or independent verification.",
        "There is no patient RNA/protein assay, drug response dataset, complete candidate",
        "universe, or trained efficacy model. This package cannot infer parental genotypes.",
        "Source fingerprints and code fingerprints are in `run_manifest.json`;",
        "claim-level provenance is in `evidence_audit.csv`.", "",
        "See `../docs/mechanism_dossier.md` for the scientific argument and proposed",
        "follow-up, `../docs/methods.md` for schema and scoring details, and",
        "`../docs/ai_disclosure.md` for assistance and data-handling disclosures.", "",
        "## Sources", "",
    ]
    lines += [
        f"- **{source.source_id}**: [{md(source.title)}]({source.url}). "
        f"{source.kind}; study `{source.study_id}`; accessed {source.accessed_on}."
        for source in sorted(bundle.sources.values(), key=lambda item: item.source_id)
    ]
    return "\n".join(lines) + "\n"


def run(data_dir: Path, config_path: Path, output_dir: Path) -> dict[str, Any]:
    bundle, settings = load_inputs(data_dir, config_path)
    inputs = {
        "data/sources.json": data_dir / "sources.json",
        "data/drugs.json": data_dir / "drugs.json",
        "data/claims.json": data_dir / "claims.json",
        "config/prioritization.json": config_path,
    }
    if output_dir.resolve() == data_dir.resolve():
        raise ValueError("The output directory must differ from the input data directory")
    inputs.update({
        f"mva_track2/{path.name}": path
        for path in sorted(Path(__file__).parent.glob("*.py"))
    })
    fingerprints = {
        name: hashlib.sha256(path.read_bytes()).hexdigest()
        for name, path in sorted(inputs.items())
    }
    snapshot_id = hashlib.sha256(json.dumps(fingerprints, sort_keys=True).encode()).hexdigest()
    results = evaluate(bundle, settings)
    scenarios = sensitivity(bundle, settings)
    report = render_report(bundle, settings, results, scenarios, snapshot_id)
    rankings = [{
        "research_priority_rank": row.rank if row.rank is not None else "",
        "drug_id": row.drug_id, "name": row.name, "status": row.status,
        "priority_index": row.priority_index if row.rank is not None else "",
        "mechanism_support": row.mechanism_support,
        "translation_support": row.translation_support,
        "bridge_support": row.bridge_support,
        "functional_rescue_support": row.functional_rescue_support,
        "independent_primary_studies": len(row.primary_studies),
        "reason": row.reason,
    } for row in results]
    audit = [{
        "drug_id": drug_id, "claim_id": claim.claim_id,
        "dimension": claim.dimension, "relation": claim.relation, "scope": claim.scope,
        "summary": claim.summary, "source_id": claim.source_id,
        "study_id": bundle.sources[claim.source_id].study_id,
        "source_kind": bundle.sources[claim.source_id].kind,
        "url": bundle.sources[claim.source_id].url,
    } for claim in bundle.claims for drug_id in claim.drug_ids]
    manifest = {
        "schema_version": 1, "snapshot_id": snapshot_id, "files_sha256": fingerprints,
        "profiles": settings.profiles,
        "counts": {"drugs": len(bundle.drugs), "sources": len(bundle.sources),
                   "claims": len(bundle.claims), "sensitivity_rows": len(scenarios)},
        "outputs": ["ranked_hypotheses.csv", "evidence_audit.csv", "sensitivity.csv",
                    "research_report.md", "run_manifest.json"],
        "interpretation": "Research-only evidence index; not efficacy or safety predictions.",
    }
    output_dir.mkdir(parents=True, exist_ok=True)
    write_csv(output_dir / "ranked_hypotheses.csv", rankings)
    write_csv(output_dir / "evidence_audit.csv", audit)
    write_csv(output_dir / "sensitivity.csv", scenarios)
    (output_dir / "research_report.md").write_text(report, encoding="utf-8")
    (output_dir / "run_manifest.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=True) + "\n", encoding="utf-8",
    )
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", type=Path, default=ROOT / "data")
    parser.add_argument("--config", type=Path, default=ROOT / "config" / "prioritization.json")
    parser.add_argument("--output-dir", type=Path, default=ROOT / "outputs")
    args = parser.parse_args()
    try:
        manifest = run(args.data_dir, args.config, args.output_dir)
    except (OSError, ValueError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        raise SystemExit(1) from error
    print(f"Research package generated: {manifest['counts']['drugs']} hypotheses, "
          f"{manifest['counts']['claims']} cited claims. No clinical efficacy asserted.")


if __name__ == "__main__":
    main()
