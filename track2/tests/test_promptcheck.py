import copy
import json
import re
import unittest
from pathlib import Path

from mva_track2.promptcheck import KINDS, check, load_vetoes
from mva_track2.pipeline import ROOT

PROMPTS = ROOT / "prompts"
PROMPT_FILES = {
    "mechanism": "01_mechanism.md",
    "longlist": "02_longlist.md",
    "claims": "03_claims.md",
    "falsifier": "04_falsifier.md",
}


def example(kind):
    return json.loads((PROMPTS / "examples" / f"{kind}.json").read_text(encoding="utf-8"))


def reply(value):
    return json.dumps(value)


class GoldenExampleTests(unittest.TestCase):
    def test_every_golden_example_meets_its_contract(self):
        for kind in KINDS:
            with self.subTest(kind=kind):
                self.assertEqual(check(kind, reply(example(kind))), [])

    def test_chatty_fenced_reply_is_accepted(self):
        text = "Here is the result:\n```json\n" + reply(example("mechanism")) + "\n```\nHope it helps."
        self.assertEqual(check("mechanism", text), [])

    def test_reply_without_json_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "no parseable JSON"):
            check("mechanism", "I think the answer is arimoclomol.")


class MechanismTests(unittest.TestCase):
    def test_fact_without_citation_is_rejected(self):
        bad = example("mechanism")
        bad["chain"][2]["source_ids"] = []
        with self.assertRaisesRegex(ValueError, "FACT must cite"):
            check("mechanism", reply(bad))

    def test_fabricated_source_is_rejected(self):
        bad = example("mechanism")
        bad["chain"][0]["source_ids"] = ["smith_2031_made_up"]
        with self.assertRaisesRegex(ValueError, "unknown source IDs"):
            check("mechanism", reply(bad))

    def test_steps_must_be_numbered_in_order(self):
        bad = example("mechanism")
        bad["chain"][1]["step"] = 5
        with self.assertRaisesRegex(ValueError, "numbered"):
            check("mechanism", reply(bad))


class LonglistTests(unittest.TestCase):
    def test_advancing_a_vetoed_candidate_is_rejected(self):
        bad = example("longlist")
        bad["longlist"][3]["verdict"] = "advance"
        bad["longlist"][3]["first_experiment"] = "Any concrete measurement."
        with self.assertRaisesRegex(ValueError, "advance requires veto_code none"):
            check("longlist", reply(bad))

    def test_rejection_without_a_veto_code_is_rejected(self):
        bad = example("longlist")
        bad["longlist"][4]["veto_code"] = "none"
        with self.assertRaisesRegex(ValueError, "require a veto code"):
            check("longlist", reply(bad))

    def test_unknown_veto_code_is_rejected(self):
        bad = example("longlist")
        bad["longlist"][4]["veto_code"] = "V_SOUNDS_BAD"
        with self.assertRaisesRegex(ValueError, "must be one of"):
            check("longlist", reply(bad))

    def test_short_screen_is_rejected(self):
        bad = example("longlist")
        bad["longlist"] = bad["longlist"][:5]
        with self.assertRaisesRegex(ValueError, "at least 8"):
            check("longlist", reply(bad))

    def test_single_axis_screen_is_rejected(self):
        bad = example("longlist")
        for row in bad["longlist"]:
            row["axis"] = "one axis"
        with self.assertRaisesRegex(ValueError, "at least 3 axes"):
            check("longlist", reply(bad))

    def test_too_many_advancing_candidates_are_rejected(self):
        bad = example("longlist")
        template = copy.deepcopy(bad["longlist"][0])
        for index in range(4):
            extra = copy.deepcopy(template)
            extra["name"] = f"extra {index}"
            bad["longlist"].append(extra)
        with self.assertRaisesRegex(ValueError, "at most 5"):
            check("longlist", reply(bad))

    def test_duplicate_candidate_is_rejected(self):
        bad = example("longlist")
        bad["longlist"][1]["name"] = "Arimoclomol"
        with self.assertRaisesRegex(ValueError, "duplicate candidate"):
            check("longlist", reply(bad))

    def test_advancing_candidate_needs_a_first_experiment(self):
        bad = example("longlist")
        bad["longlist"][0]["first_experiment"] = ""
        with self.assertRaisesRegex(ValueError, "nonempty string"):
            check("longlist", reply(bad))

    def test_every_veto_code_in_the_registry_is_well_formed(self):
        self.assertGreaterEqual(len(load_vetoes()), 5)


class ClaimsTests(unittest.TestCase):
    def test_unknown_drug_is_rejected(self):
        bad = example("claims")
        bad[0]["drug_ids"] = ["miracle_drug"]
        with self.assertRaisesRegex(ValueError, "unknown drug IDs"):
            check("claims", reply(bad))

    def test_unknown_source_is_rejected(self):
        bad = example("claims")
        bad[0]["source_id"] = "invented_2031"
        with self.assertRaisesRegex(ValueError, "unknown source"):
            check("claims", reply(bad))

    def test_reusing_an_existing_claim_id_is_rejected(self):
        bad = example("claims")
        bad[0]["claim_id"] = "sirt2_bubr1_stability_bridge"
        with self.assertRaisesRegex(ValueError, "Duplicate claim_id"):
            check("claims", reply(bad))

    def test_regulatory_scope_on_a_primary_source_is_rejected(self):
        bad = example("claims")
        bad[0]["scope"] = "regulatory"
        with self.assertRaisesRegex(ValueError, "regulatory source and scope must agree"):
            check("claims", reply(bad))

    def test_extra_field_is_rejected(self):
        bad = example("claims")
        bad[0]["confidence"] = "high"
        with self.assertRaisesRegex(ValueError, "exactly these fields"):
            check("claims", reply(bad))

    def test_overlong_summary_is_rejected(self):
        bad = example("claims")
        bad[0]["summary"] = "x" * 451
        with self.assertRaisesRegex(ValueError, "exceeds 450"):
            check("claims", reply(bad))

    def test_overclaiming_language_is_flagged_not_hidden(self):
        bad = example("claims")
        bad[0]["summary"] = "Niacin cures BubR1 loss in mice."
        self.assertTrue(any("overclaiming" in w for w in check("claims", reply(bad))))

    def test_exact_variant_scope_is_flagged_for_human_review(self):
        flagged = example("claims")
        flagged[0]["scope"] = "exact_variant"
        self.assertTrue(any("exact_variant" in w for w in check("claims", reply(flagged))))

    def test_empty_array_is_an_honest_answer(self):
        warnings = check("claims", "[]")
        self.assertEqual(len(warnings), 1)
        self.assertIn("nothing", warnings[0])


class FalsifierTests(unittest.TestCase):
    def test_non_numeric_gate_is_rejected(self):
        bad = example("falsifier")
        bad["kill_criteria"][0]["threshold"] = "a clear improvement"
        with self.assertRaisesRegex(ValueError, "must be numeric"):
            check("falsifier", reply(bad))

    def test_unknown_candidate_is_rejected(self):
        bad = example("falsifier")
        bad["kill_criteria"][0]["candidate"] = "miracle_drug"
        with self.assertRaisesRegex(ValueError, "must be one of"):
            check("falsifier", reply(bad))

    def test_too_few_confounds_are_rejected(self):
        bad = example("falsifier")
        bad["confounds"] = bad["confounds"][:2]
        with self.assertRaisesRegex(ValueError, "at least three"):
            check("falsifier", reply(bad))

    def test_decision_must_be_no_go_or_defer(self):
        bad = example("falsifier")
        bad["kill_criteria"][0]["decision_if_fail"] = "go"
        with self.assertRaisesRegex(ValueError, "must be one of"):
            check("falsifier", reply(bad))


class PromptPackStructureTests(unittest.TestCase):
    def read(self, kind):
        return (PROMPTS / PROMPT_FILES[kind]).read_text(encoding="utf-8")

    def prompt_block(self, kind):
        blocks = re.findall(r"```text\n(.*?)\n```", self.read(kind), re.S)
        self.assertEqual(len(blocks), 1, f"{kind}: expected exactly one prompt block")
        return blocks[0]

    def test_every_documented_slot_is_used_and_every_used_slot_is_documented(self):
        for kind in PROMPT_FILES:
            with self.subTest(kind=kind):
                documented = set(re.findall(r"^\| `\{([A-Z_]+)\}`", self.read(kind), re.M))
                used = set(re.findall(r"\{([A-Z_]+)\}", self.prompt_block(kind)))
                self.assertEqual(documented, used)

    def test_each_prompt_names_its_validator_command(self):
        for kind in PROMPT_FILES:
            with self.subTest(kind=kind):
                self.assertIn(f"promptcheck {kind} reply.txt", self.read(kind))

    def test_prompts_forbid_inventing_evidence(self):
        for kind in ("mechanism", "claims"):
            with self.subTest(kind=kind):
                self.assertRegex(self.prompt_block(kind), r"(?i)invent|outside knowledge")

    def test_example_veto_codes_exist_in_the_registry(self):
        registry = set(load_vetoes()) | {"none"}
        used = {row["veto_code"] for row in example("longlist")["longlist"]}
        self.assertLessEqual(used, registry)


if __name__ == "__main__":
    unittest.main()
