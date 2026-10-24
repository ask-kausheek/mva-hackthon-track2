from __future__ import annotations

import copy
import csv
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from mva_track2.pipeline import (
    RANKABLE, ROOT, evaluate, load_inputs, run, sensitivity, validate_bundle, validate_settings,
    write_csv,
)


def fixture():
    sources = [
        {
            "source_id": key, "title": key, "url": f"https://example.org/{key}",
            "kind": kind, "study_id": study, "accessed_on": "2026-09-05",
        }
        for key, kind, study in [
            ("label", "regulatory", "label-1"),
            ("gene", "primary", "study-gene"),
            ("drug", "primary", "study-drug"),
            ("review", "review", "review-1"),
        ]
    ]
    drugs = [{
        "drug_id": "test_drug", "name": "Synthetic test drug",
        "approved_indication": "Synthetic indication; test fixture only",
        "approval_status": "approved", "approval_source_id": "label",
        "mechanism_id": "test_mechanism", "mechanism_description": "Synthetic bridge",
        "mechanism_claim_groups": [["gene_claim"]],
        "variant_fit": "unresolved", "variant_fit_note": "Not measured",
        "exposure_status": "unresolved", "safety_status": "unresolved",
        "safety_note": "Not evaluated",
    }]
    claims = [
        {
            "claim_id": "gene_claim", "drug_ids": ["test_drug"], "source_id": "gene",
            "dimension": "mechanism", "relation": "supports",
            "scope": "same_gene_other_variant", "summary": "Synthetic gene mechanism",
        },
        {
            "claim_id": "drug_claim", "drug_ids": ["test_drug"], "source_id": "drug",
            "dimension": "translation", "relation": "supports",
            "scope": "other_disease", "summary": "Synthetic drug evidence",
        },
    ]
    settings = {
        "team": "Synthetic",
        "scope_weights": {
            "exact_variant": 1, "same_gene_other_variant": 0.6,
            "same_gene_nonvariant": 0.4, "other_disease": 0.2,
            "general": 0.1, "regulatory": 0,
        },
        "profiles": {
            "baseline": {"bridge": 0.5, "functional_rescue": 0.5},
            "bridge_emphasis": {"bridge": 0.8, "functional_rescue": 0.2},
        },
    }
    return sources, drugs, claims, settings


class RankingTests(unittest.TestCase):
    def setUp(self):
        self.sources, self.drugs, self.claims, self.config = fixture()

    def results(self):
        return evaluate(
            validate_bundle(self.sources, self.drugs, self.claims),
            validate_settings(self.config),
        )

    def test_weakest_link_not_strongest_claim_controls_bridge(self):
        row = self.results()[0]
        self.assertEqual(row.status, RANKABLE)
        self.assertEqual(row.mechanism_support, 0.6)
        self.assertEqual(row.translation_support, 0.2)
        self.assertEqual(row.bridge_support, 0.2)
        self.assertEqual(row.functional_rescue_support, 0)
        self.assertEqual(row.priority_index, 10)
        self.assertNotEqual(row.priority_index, 100)

    def test_missing_translation_is_deferred_not_negative_efficacy(self):
        self.claims = self.claims[:1]
        row = self.results()[0]
        self.assertEqual(row.status, "deferred_no_bridge_evidence")
        self.assertIsNone(row.rank)

    def test_regulatory_label_cannot_complete_a_bridge(self):
        self.claims[1].update(source_id="label", scope="regulatory")
        self.assertEqual(self.results()[0].status, "deferred_no_bridge_evidence")

    def test_review_does_not_add_numeric_evidence(self):
        self.claims[1].update(source_id="review", scope="exact_variant")
        self.assertEqual(self.results()[0].translation_support, 0)

    def test_duplicating_claims_or_study_mirrors_cannot_inflate_score(self):
        original = self.results()[0]
        duplicate = copy.deepcopy(self.claims[0])
        duplicate["claim_id"] = "duplicate_claim"
        self.sources.append({**self.sources[1], "source_id": "gene_mirror"})
        duplicate["source_id"] = "gene_mirror"
        self.claims.append(duplicate)
        changed = self.results()[0]
        self.assertEqual(original.priority_index, changed.priority_index)
        self.assertEqual(original.primary_studies, changed.primary_studies)

    def test_same_study_all_mirrors_removed_in_ablation(self):
        self.sources.append({**self.sources[1], "source_id": "gene_mirror"})
        self.claims.append({**self.claims[0], "claim_id": "mirror", "source_id": "gene_mirror"})
        self.drugs[0]["mechanism_claim_groups"][0].append("mirror")
        bundle = validate_bundle(self.sources, self.drugs, self.claims)
        settings = validate_settings(self.config)
        rows = evaluate(bundle, settings, excluded_studies=frozenset({"study-gene"}))
        self.assertEqual(rows[0].status, "deferred_no_bridge_evidence")
        self.assertEqual(rows[0].mechanism_support, 0)

    def test_missing_required_step_cannot_be_replaced_by_other_gene_evidence(self):
        self.sources.append({**self.sources[1], "source_id": "step_two", "study_id": "step-two-study"})
        self.claims.append({
            **self.claims[0], "claim_id": "step_two", "source_id": "step_two",
            "scope": "same_gene_nonvariant",
        })
        self.drugs[0]["mechanism_claim_groups"].append(["step_two"])
        bundle = validate_bundle(self.sources, self.drugs, self.claims)
        settings = validate_settings(self.config)
        self.assertEqual(evaluate(bundle, settings)[0].mechanism_support, 0.4)
        result = evaluate(bundle, settings, excluded_studies=frozenset({"step-two-study"}))[0]
        self.assertEqual(result.status, "deferred_no_bridge_evidence")
        self.assertEqual(result.mechanism_support, 0)

    def test_other_disease_rescue_is_not_bubr1_functional_rescue(self):
        self.claims.append({
            **self.claims[1], "claim_id": "rescue", "dimension": "functional_rescue",
        })
        self.assertEqual(self.results()[0].functional_rescue_support, 0)

    def test_explicit_same_gene_drug_rescue_receives_support(self):
        self.claims.append({
            **self.claims[1], "claim_id": "rescue", "dimension": "functional_rescue",
            "scope": "same_gene_other_variant",
        })
        self.assertEqual(self.results()[0].functional_rescue_support, 0.6)

    def test_safety_hold_is_not_overridden_by_evidence(self):
        self.drugs[0]["safety_status"] = "hold"
        row = self.results()[0]
        self.assertEqual(row.status, "held_safety")
        self.assertIsNone(row.rank)

    def test_unverified_approval_is_not_rankable(self):
        self.drugs[0].update(approval_status="unverified", approval_source_id="")
        row = self.results()[0]
        self.assertEqual(row.status, "ineligible_approval")
        self.assertIsNone(row.rank)

    def test_incompatible_variant_is_held(self):
        self.drugs[0]["variant_fit"] = "contradicted"
        self.assertEqual(self.results()[0].status, "held_incompatible")

    def test_opposing_evidence_is_not_averaged_away(self):
        self.claims.append({
            **self.claims[0], "claim_id": "opposed", "relation": "contradicts",
        })
        self.assertEqual(self.results()[0].status, "held_conflicting_evidence")

    def test_equal_evidence_keeps_tied_ranks(self):
        self.drugs.append({**self.drugs[0], "drug_id": "second", "name": "Second"})
        for claim in self.claims:
            claim["drug_ids"].append("second")
        self.assertEqual([row.rank for row in self.results()], [1, 1])

    def test_sensitivity_crosses_profiles_and_primary_studies(self):
        rows = sensitivity(
            validate_bundle(self.sources, self.drugs, self.claims),
            validate_settings(self.config),
        )
        self.assertEqual(len(rows), 2 * (1 + 2))
        held_out = [row for row in rows if row["excluded_study"]]
        self.assertTrue(all(row["status"] == "deferred_no_bridge_evidence" for row in held_out))


class ValidationTests(unittest.TestCase):
    def test_unknown_source_fails(self):
        sources, drugs, claims, _ = fixture()
        claims[0]["source_id"] = "missing"
        with self.assertRaisesRegex(ValueError, "unknown source"):
            validate_bundle(sources, drugs, claims)

    def test_unknown_drug_fails(self):
        sources, drugs, claims, _ = fixture()
        claims[0]["drug_ids"] = ["missing"]
        with self.assertRaisesRegex(ValueError, "unknown drug"):
            validate_bundle(sources, drugs, claims)

    def test_duplicate_identifiers_fail(self):
        sources, drugs, claims, _ = fixture()
        for data in (sources, drugs, claims):
            with self.subTest(data=data[0]):
                data.append(copy.deepcopy(data[0]))
                with self.assertRaisesRegex(ValueError, "Duplicate"):
                    validate_bundle(sources, drugs, claims)
                data.pop()

    def test_approval_requires_label(self):
        sources, drugs, claims, _ = fixture()
        drugs[0]["approval_source_id"] = "gene"
        with self.assertRaisesRegex(ValueError, "regulatory source"):
            validate_bundle(sources, drugs, claims)

    def test_wrong_scope_and_unknown_fields_fail(self):
        sources, drugs, claims, _ = fixture()
        claims[0]["scope"] = "regulatory"
        with self.assertRaisesRegex(ValueError, "scope must agree"):
            validate_bundle(sources, drugs, claims)
        claims[0]["scope"] = "general"
        claims[0]["invented"] = "field"
        with self.assertRaisesRegex(ValueError, "exactly these fields"):
            validate_bundle(sources, drugs, claims)

    def test_required_step_must_reference_correct_positive_mechanism_evidence(self):
        for claim_id in ("missing", "drug_claim"):
            sources, drugs, claims, _ = fixture()
            drugs[0]["mechanism_claim_groups"] = [[claim_id]]
            with self.subTest(claim_id=claim_id):
                with self.assertRaisesRegex(ValueError, "required mechanism link"):
                    validate_bundle(sources, drugs, claims)

    def test_invalid_settings_fail(self):
        for edit in ("nan", "sum", "regulatory", "bool"):
            *_, config = fixture()
            with self.subTest(edit=edit):
                if edit == "nan":
                    config["scope_weights"]["general"] = float("nan")
                elif edit == "sum":
                    config["profiles"]["baseline"]["bridge"] = 0.9
                elif edit == "bool":
                    config["scope_weights"]["general"] = True
                else:
                    config["scope_weights"]["regulatory"] = 0.5
                with self.assertRaises(ValueError):
                    validate_settings(config)

    def test_csv_formula_text_is_escaped(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "table.csv"
            write_csv(path, [{"note": "=1+1", "value": 2}])
            with path.open(newline="", encoding="utf-8") as handle:
                row = next(csv.DictReader(handle))
            self.assertEqual(row, {"note": "'=1+1", "value": "2"})


class EndToEndTests(unittest.TestCase):
    def test_outputs_shapes_provenance_and_repeatability(self):
        sources, drugs, claims, config = fixture()
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            data = root / "data"
            data.mkdir()
            for name, value in [("sources", sources), ("drugs", drugs), ("claims", claims)]:
                (data / f"{name}.json").write_text(json.dumps(value), encoding="utf-8")
            cfg = root / "settings.json"
            cfg.write_text(json.dumps(config), encoding="utf-8")
            output = root / "outputs"
            manifest = run(data, cfg, output)
            original = {path.name: path.read_bytes() for path in output.iterdir()}
            run(data, cfg, output)
            self.assertEqual(original, {path.name: path.read_bytes() for path in output.iterdir()})
            self.assertEqual(set(original), set(manifest["outputs"]))
            self.assertEqual(manifest["counts"]["sensitivity_rows"], 6)
            report = (output / "research_report.md").read_text(encoding="utf-8")
            self.assertIn("not a treatment recommendation", report)
            self.assertIn("https://example.org/gene", report)
            self.assertIn("Not found in snapshot", report)
            with (output / "ranked_hypotheses.csv").open(encoding="utf-8", newline="") as handle:
                rows = list(csv.DictReader(handle))
            self.assertEqual(rows[0]["research_priority_rank"], "1")
            self.assertEqual(rows[0]["priority_index"], "10.0")
            self.assertNotIn("epcr", rows[0])
            self.assertTrue(all(not Path(name).is_absolute() for name in manifest["files_sha256"]))

    def test_cli_failure_does_not_create_success_artifact(self):
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp) / "outputs"
            process = subprocess.run(
                [sys.executable, "-m", "mva_track2", "--data-dir", str(Path(temp) / "missing"),
                 "--output-dir", str(output)],
                cwd=ROOT, capture_output=True, text=True,
            )
            self.assertNotEqual(process.returncode, 0)
            self.assertIn("ERROR:", process.stderr)
            self.assertFalse(output.exists())


class EvidenceSnapshotTests(unittest.TestCase):
    def setUp(self):
        self.bundle, self.settings = load_inputs(
            ROOT / "data", ROOT / "config" / "prioritization.json",
        )

    def test_initial_candidates_remain_conditional_or_held(self):
        results = {row.drug_id: row for row in evaluate(self.bundle, self.settings)}
        self.assertEqual(set(results), {"arimoclomol", "niacin", "gentamicin"})
        for drug_id in ("arimoclomol", "niacin"):
            self.assertEqual(results[drug_id].status, RANKABLE)
            self.assertEqual(results[drug_id].rank, 1)
            self.assertEqual(results[drug_id].priority_index, 10)
        self.assertEqual(results["gentamicin"].status, "held_safety")
        self.assertIsNone(results["gentamicin"].rank)

    def test_snapshot_does_not_claim_case_specific_efficacy(self):
        self.assertTrue(all(claim.scope != "exact_variant" for claim in self.bundle.claims))
        self.assertTrue(all(claim.dimension != "functional_rescue" for claim in self.bundle.claims))
        for drug in self.bundle.drugs.values():
            self.assertEqual(drug.variant_fit, "unresolved")
            self.assertEqual(drug.exposure_status, "unresolved")
        for result in evaluate(self.bundle, self.settings):
            self.assertEqual(result.functional_rescue_support, 0)

    def test_snapshot_study_removal_exposes_bridge_gaps(self):
        rows = sensitivity(self.bundle, self.settings)
        for drug_id in ("arimoclomol", "niacin"):
            self.assertTrue(any(
                row["drug_id"] == drug_id and row["status"] == "deferred_no_bridge_evidence"
                for row in rows
            ))
        self.assertTrue(all(
            row["status"] == "held_safety" for row in rows if row["drug_id"] == "gentamicin"
        ))


if __name__ == "__main__":
    unittest.main()
