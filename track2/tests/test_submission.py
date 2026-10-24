import copy
import hashlib
import json
import re
import tempfile
import unittest
from html.parser import HTMLParser
from pathlib import Path

from mva_track2.pipeline import ROOT, evaluate, load_inputs
from mva_track2.submission import (
    EVIDENCE_FILES, REPORT, acknowledgement, build_submission, deck,
    load_pitch, recording_script, verify_review,
)


class DeckParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.slides = 0
        self.external_resources = []
        self.ids = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "section" and attrs.get("class") == "slide":
            self.slides += 1
        if tag in ("script", "img", "link") and ("src" in attrs or "href" in attrs):
            self.external_resources.append(attrs)
        if "id" in attrs:
            self.ids.append(attrs["id"])


class SubmissionTests(unittest.TestCase):
    def setUp(self):
        self.bundle, self.settings = load_inputs(ROOT / "data", ROOT / "config" / "prioritization.json")
        self.pitch = load_pitch(ROOT / "config" / "pitch.json", set(self.bundle.sources))

    def test_deck_is_offline_six_slides_with_controls_and_real_results(self):
        content = deck(self.pitch, self.bundle.sources, evaluate(self.bundle, self.settings), "Acknowledgement")
        parser = DeckParser()
        parser.feed(content)
        self.assertEqual(parser.slides, 6)
        self.assertEqual(parser.external_resources, [])
        self.assertEqual(len(parser.ids), len(set(parser.ids)))
        self.assertTrue({"next", "previous", "fullscreen", "progress"} <= set(parser.ids))
        self.assertEqual(content.count("<td>10.0</td>"), 2)
        self.assertIn("Held", content)
        self.assertIn("not demonstrated treatments", content)

    def test_three_minute_script_has_complete_narration(self):
        words = sum(len(slide["narration"].split()) for slide in self.pitch["slides"])
        self.assertTrue(330 <= words <= 420)
        self.assertEqual(sum(slide["seconds"] for slide in self.pitch["slides"]), 180)
        script = recording_script(self.pitch, "test")
        self.assertIn("2:30-3:00", script)
        self.assertIn("not a recorded duration", script)
        self.assertIn("not a video submission", script)

    def test_bad_pitch_timing_and_unknown_sources_fail(self):
        for kind in ("duration", "source"):
            pitch = copy.deepcopy(self.pitch)
            if kind == "duration":
                pitch["slides"][0]["seconds"] = 31
            else:
                pitch["slides"][0]["source_ids"] = ["missing"]
            with tempfile.TemporaryDirectory() as temp:
                path = Path(temp) / "pitch.json"
                path.write_text(json.dumps(pitch), encoding="utf-8")
                with self.assertRaises(ValueError):
                    load_pitch(path, set(self.bundle.sources))

    def test_review_hashes_cover_exact_evidence_and_reject_changes(self):
        verify_review(ROOT)
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            for name in EVIDENCE_FILES | {"config/submission_review.json"}:
                source = ROOT.joinpath(*name.split("/"))
                target = root.joinpath(*name.split("/"))
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(source.read_bytes())
            with (root / "data" / "claims.json").open("a", encoding="utf-8") as handle:
                handle.write("\n")
            with self.assertRaisesRegex(ValueError, "Evidence/configuration changed"):
                verify_review(root)

    def test_report_is_standalone_and_abstract_under_500_words(self):
        report = (ROOT / "submission" / REPORT).read_text(encoding="utf-8")
        abstract = report.split("## 1. Method abstract")[1].split("## 2.")[0]
        self.assertLessEqual(len(abstract.split()), 500)
        self.assertIn("does not ingest the VCF", report)
        self.assertEqual(len(re.findall(r"\*\*\[R[1-7]\]\*\*", report)), 7)
        self.assertNotRegex(report, r"(?i)\bTODO\b|INSERT_HERE|YOUR_GITHUB")
        self.assertIn("BEACON", acknowledgement(report))

    def test_submission_manifest_does_not_claim_packaged_or_hosted_video(self):
        # Use a temporary package so tests do not modify the user's report or outputs.
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            names = EVIDENCE_FILES | {
                "config/submission_review.json", "config/pitch.json", f"submission/{REPORT}",
            }
            for name in names:
                target = root.joinpath(*name.split("/"))
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(ROOT.joinpath(*name.split("/")).read_bytes())
            manifest = build_submission(root)
            self.assertEqual(manifest["completion"]["recorded_video"], "prepared_locally_not_packaged")
            self.assertEqual(manifest["completion"]["hosted_video_url"], "user_action_required")
            self.assertEqual(manifest["completion"]["github_repository_url"], "user_action_required")
            for name, digest in manifest["files_sha256"].items():
                self.assertEqual(hashlib.sha256((root / "submission" / name).read_bytes()).hexdigest(), digest)
            original = {path.name: path.read_bytes() for path in (root / "submission").iterdir()}
            build_submission(root)
            self.assertEqual(original, {path.name: path.read_bytes() for path in (root / "submission").iterdir()})


if __name__ == "__main__":
    unittest.main()
