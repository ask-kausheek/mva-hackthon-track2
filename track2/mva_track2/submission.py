"""Build recording assets and bind the authored proposal to its reviewed evidence."""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
from pathlib import Path

from .pipeline import ROOT, evaluate, load_inputs, read_json, run

EVIDENCE_FILES = {
    "data/sources.json", "data/drugs.json", "data/claims.json",
    "config/prioritization.json",
}
REPORT = "Soul_track2_report.md"

STYLE = """
*{box-sizing:border-box}body{margin:0;background:#091923;color:#f4f7f9;
font-family:Segoe UI,Arial,sans-serif}header{height:62px;padding:14px 4vw;
display:flex;justify-content:space-between;align-items:center;color:#82dfbd}
button{background:#153745;color:#fff;border:1px solid #61808d;border-radius:6px;
padding:8px 14px;cursor:pointer}main{max-width:1500px;margin:auto}
.slide{min-height:calc(100vh - 114px);padding:3vh 5vw}
.label{text-transform:uppercase;letter-spacing:.14em;color:#82dfbd;font-size:18px}
h1{font-size:clamp(28px,3.3vw,48px);line-height:1.12;margin:18px 0 22px;max-width:1150px}
li{font-size:clamp(18px,1.7vw,28px);line-height:1.35;margin:12px 0}
ul{padding-left:28px;max-width:1150px}.refs{font-size:14px;color:#b6c7cf;margin-top:28px}
a{color:#82dfbd}footer{height:52px;padding:10px 4vw;display:flex;justify-content:space-between;
font-size:15px;color:#b6c7cf;border-top:1px solid #294554}.status{color:#ffd27b}
table{border-collapse:collapse;width:100%;font-size:18px;margin:16px 0}
td,th{padding:9px;text-align:left;border-bottom:1px solid #31515e}
th{color:#82dfbd}.credits{font-size:15px;line-height:1.45;color:#b6c7cf;max-width:1200px;
border-top:1px solid #31515e;margin-top:20px;padding-top:14px}
#error{color:#ffb1a8;padding:0 4vw}
@media print{body{background:white;color:black}header,footer,button,#error{display:none}
.slide,.slide[hidden]{display:block!important;break-after:page;min-height:90vh}
a,.label,th,.credits{color:#153745}}
"""


def verify_review(root: Path) -> None:
    review = read_json(root / "config" / "submission_review.json")
    if not isinstance(review, dict) or not isinstance(review.get("reviewed_sha256"), dict):
        raise ValueError("submission_review.json requires reviewed_sha256")
    expected = review["reviewed_sha256"]
    if set(expected) != EVIDENCE_FILES:
        raise ValueError("The submission review must cover all four evidence/config files")
    changed = [
        name for name in sorted(EVIDENCE_FILES)
        if hashlib.sha256(root.joinpath(*name.split("/")).read_bytes()).hexdigest() != expected[name]
    ]
    if changed:
        raise ValueError(
            "Evidence/configuration changed: " + ", ".join(changed)
            + ". Reconcile the authored report and pitch with the new results before "
            "recording new hashes in config/submission_review.json."
        )


def load_pitch(path: Path, valid_sources: set[str]) -> dict:
    pitch = read_json(path)
    if not isinstance(pitch, dict) or set(pitch) != {"team", "title", "slides"}:
        raise ValueError("pitch.json: expected team, title and slides")
    if not all(isinstance(pitch[key], str) and pitch[key].strip() for key in ("team", "title")):
        raise ValueError("Pitch team and title must be nonempty strings")
    if not isinstance(pitch["slides"], list) or len(pitch["slides"]) != 6:
        raise ValueError("The recording deck must have six slides")
    fields = {"title", "label", "seconds", "kind", "bullets", "source_ids", "narration"}
    for slide in pitch["slides"]:
        if not isinstance(slide, dict) or set(slide) != fields:
            raise ValueError("Invalid pitch slide fields")
        for field in ("title", "label", "narration"):
            if not isinstance(slide[field], str) or not slide[field].strip():
                raise ValueError(f"Pitch {field} must be a nonempty string")
        if type(slide["seconds"]) is not int or slide["seconds"] <= 0:
            raise ValueError("Slide seconds must be a positive integer")
        if slide["kind"] not in {"standard", "results", "credits"}:
            raise ValueError("Unknown slide kind")
        if not isinstance(slide["bullets"], list) or not 1 <= len(slide["bullets"]) <= 3:
            raise ValueError("Each slide requires one to three bullets")
        if not all(isinstance(item, str) and item.strip() for item in slide["bullets"]):
            raise ValueError("Slide bullets must be nonempty strings")
        if not isinstance(slide["source_ids"], list) or any(
            not isinstance(item, str) or item not in valid_sources for item in slide["source_ids"]
        ):
            raise ValueError("Slide references an unknown source")
    if sum(slide["seconds"] for slide in pitch["slides"]) != 180:
        raise ValueError("Pitch target duration must total 180 seconds")
    if sum(slide["kind"] == "results" for slide in pitch["slides"]) != 1:
        raise ValueError("The deck requires one generated results slide")
    if sum(slide["kind"] == "credits" for slide in pitch["slides"]) != 1:
        raise ValueError("The deck requires one acknowledgement slide")
    words = sum(len(slide["narration"].split()) for slide in pitch["slides"])
    if not 330 <= words <= 420:
        raise ValueError(f"Pitch narration has {words} words; expected 330-420")
    return pitch


def acknowledgement(report: str) -> str:
    parts = report.split("## 9. Hackathon acknowledgement")
    if len(parts) != 2:
        raise ValueError("Standalone report must retain its acknowledgement section")
    lines = [line[2:].strip() for line in parts[1].splitlines() if line.startswith("> ")]
    if not lines:
        raise ValueError("Acknowledgement text missing")
    return " ".join(lines)


def deck(pitch: dict, sources: dict, results: list, credits: str) -> str:
    escape = html.escape
    source_numbers = {key: index for index, key in enumerate(sources, 1)}
    sections = []
    for index, slide in enumerate(pitch["slides"]):
        body = (
            f'<p class="label">{escape(slide["label"])}</p>'
            f'<h1>{escape(slide["title"])}</h1>'
            '<ul>' + "".join(f"<li>{escape(item)}</li>" for item in slide["bullets"]) + "</ul>"
        )
        if slide["kind"] == "results":
            body += "<table><thead><tr><th>Research priority</th><th>Hypothesis</th><th>Index / 100</th></tr></thead><tbody>"
            for result in results:
                name = "Prescription nicotinic acid" if result.drug_id == "niacin" else result.name
                rank = str(result.rank) + " (tied)" if result.rank is not None else "Held"
                score = f"{result.priority_index:.1f}" if result.rank is not None else "Not ranked"
                body += f"<tr><td>{rank}</td><td>{escape(name)}</td><td>{score}</td></tr>"
            body += "</tbody></table>"
        if slide["source_ids"]:
            body += '<p class="refs">Sources: ' + " | ".join(
                f'<a href="{escape(sources[key].url, quote=True)}" target="_blank" rel="noreferrer" '
                f'title="{escape(sources[key].title, quote=True)}">'
                f'[R{source_numbers[key]}]</a>' for key in slide["source_ids"]
            ) + "</p>"
        if slide["kind"] == "credits":
            body += f'<aside class="credits">{escape(credits)}</aside>'
        hidden = "" if index == 0 else " hidden"
        sections.append(f'<section class="slide" aria-label="Slide {index + 1}"{hidden}>{body}</section>')
    script = """
const slides = [...document.querySelectorAll('.slide')]; let current = 0;
function show(n) {
  current = Math.max(0, Math.min(slides.length - 1, n));
  slides.forEach((slide, i) => slide.hidden = i !== current);
  document.getElementById('progress').textContent = `${current + 1} / ${slides.length} | Target: 30 seconds per slide`;
}
document.getElementById('next').addEventListener('click', () => show(current + 1));
document.getElementById('previous').addEventListener('click', () => show(current - 1));
document.getElementById('fullscreen').addEventListener('click', async () => {
  try { await document.documentElement.requestFullscreen(); }
  catch (error) { document.getElementById('error').textContent = 'Fullscreen unavailable. Use your browser fullscreen command.'; }
});
document.addEventListener('keydown', event => {
  if (event.key === 'ArrowRight' || event.key === 'PageDown' || event.key === ' ') {
    event.preventDefault(); show(current + 1);
  } else if (event.key === 'ArrowLeft' || event.key === 'PageUp') {
    event.preventDefault(); show(current - 1);
  } else if (event.key === 'Home') show(0);
  else if (event.key === 'End') show(slides.length - 1);
});
const requestedSlide = Number(location.hash.slice(1)) - 1;
show(location.hash && Number.isInteger(requestedSlide) ? requestedSlide : 0);
"""
    return (
        '<!doctype html><html lang="en"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        f'<title>{escape(pitch["team"])} - Track 2 pitch</title><style>{STYLE}</style></head><body>'
        f'<header><strong>{escape(pitch["team"])} | MVA Hackathon 2026</strong>'
        '<nav><button id="previous" aria-label="Previous slide">Back</button> '
        '<button id="next" aria-label="Next slide">Next</button> '
        '<button id="fullscreen">Fullscreen</button></nav></header>'
        '<p id="error" role="alert"></p><main>' + "".join(sections)
        + '</main><footer><span class="status">Research hypotheses - not demonstrated treatments</span>'
        '<span id="progress" aria-live="polite"></span></footer>'
        f'<script>{script}</script></body></html>\n'
    )


def recording_script(pitch: dict, snapshot: str) -> str:
    words = sum(len(slide["narration"].split()) for slide in pitch["slides"])
    lines = [
        "# Soul - Three-Minute Pitch Script", "",
        f"**Target:** 180 seconds; {words} spoken words, about {words / 3:.0f} words/minute.",
        "**Delivery:** Narration for the pitch video, in your own voice or a clearly labelled synthetic voice. Timing is a rehearsal target, not a recorded duration.",
        f"**Results snapshot:** `{snapshot}`", "",
        "Open `Soul_track2_slides.html` in a browser. Use Fullscreen and the arrow",
        "keys. Record the slides and your microphone using your preferred local",
        "screen recorder. Keep this script off the recorded screen. Rehearse and",
        "adjust your pace to three minutes; do not describe proposed work as completed.", "",
    ]
    elapsed = 0
    for index, slide in enumerate(pitch["slides"], 1):
        end = elapsed + slide["seconds"]
        lines += [
            f"## {elapsed // 60}:{elapsed % 60:02d}-{end // 60}:{end % 60:02d} | "
            f"Slide {index}: {slide['title']}", "",
            slide["narration"], "",
        ]
        elapsed = end
    lines += [
        "## Recording and hosting", "",
        "Keep the final acknowledgement slide visible during the closing narration.",
        "Verify microphone clarity, readable slides and the finished duration.",
        "Upload the recorded video to YouTube or Vimeo and use that URL in the",
        "Track 2 form. A local HTML deck or this script is not a video submission.", "",
    ]
    return "\n".join(lines)


def build_submission(root: Path = ROOT) -> dict:
    verify_review(root)
    bundle, settings = load_inputs(root / "data", root / "config" / "prioritization.json")
    pitch = load_pitch(root / "config" / "pitch.json", set(bundle.sources))
    output = root / "submission"
    report_path = output / REPORT
    report = report_path.read_text(encoding="utf-8")
    credits = acknowledgement(report)
    manifest = run(root / "data", root / "config" / "prioritization.json", root / "outputs")
    snapshot = manifest["snapshot_id"]
    report, replacements = re.subn(
        r"(\*\*Input/code snapshot:\*\* `)[0-9a-f]{64}(`)",
        rf"\g<1>{snapshot}\g<2>", report,
    )
    if replacements != 1:
        raise ValueError("Report must contain exactly one Input/code snapshot fingerprint")
    results = evaluate(bundle, settings)
    artifacts = {
        REPORT: report,
        "Soul_track2_slides.html": deck(pitch, bundle.sources, results, credits),
        "Soul_track2_pitch_script.md": recording_script(pitch, snapshot),
    }
    for name, content in artifacts.items():
        (output / name).write_text(content, encoding="utf-8")
    final_manifest = {
        "research_snapshot_id": snapshot,
        "files_sha256": {
            name: hashlib.sha256((output / name).read_bytes()).hexdigest()
            for name in sorted(artifacts)
        },
        "recording_target_seconds": 180,
        "spoken_word_count": sum(len(slide["narration"].split()) for slide in pitch["slides"]),
        "completion": {
            "standalone_report": "prepared",
            "slides_and_script": "prepared_for_user_recording",
            "recorded_video": "prepared_locally_not_packaged",
            "github_repository_url": "user_action_required",
            "hosted_video_url": "user_action_required",
            "clinician_review": "not_claimed",
        },
    }
    (output / "submission_manifest.json").write_text(
        json.dumps(final_manifest, indent=2) + "\n", encoding="utf-8",
    )
    return final_manifest


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    try:
        manifest = build_submission()
    except (OSError, ValueError) as error:
        parser.exit(1, f"ERROR: {error}\n")
    print(f"Standalone report and six-slide recording deck prepared "
          f"({manifest['spoken_word_count']} words; target 3 minutes). "
          "Video upload and the GitHub and video URLs remain user actions.")


if __name__ == "__main__":
    main()
