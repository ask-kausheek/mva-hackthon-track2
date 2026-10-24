"""Build an allowlisted archive; never glob arbitrary case data into a ZIP."""

from __future__ import annotations

import argparse
import hashlib
import json
import zipfile
from pathlib import Path

from .pipeline import ROOT
from .submission import build_submission

FILES = (
    ".gitignore", "README.md", "config/prioritization.json",
    "config/submission_review.json", "config/pitch.json",
    "data/sources.json", "data/drugs.json", "data/claims.json",
    "docs/architecture.md", "docs/methods.md", "docs/mechanism_dossier.md",
    "docs/ai_disclosure.md", "docs/pitch_outline.md",
    "mva_track2/__init__.py", "mva_track2/__main__.py",
    "mva_track2/pipeline.py", "mva_track2/package.py", "mva_track2/submission.py",
    "mva_track2/promptcheck.py",
    "prompts/README.md", "prompts/01_mechanism.md", "prompts/02_longlist.md",
    "prompts/03_claims.md", "prompts/04_falsifier.md", "prompts/vetoes.json",
    "prompts/examples/mechanism.json", "prompts/examples/longlist.json",
    "prompts/examples/claims.json", "prompts/examples/falsifier.json",
    "tests/test_pipeline.py", "tests/test_package.py", "tests/test_submission.py",
    "tests/test_promptcheck.py",
    "outputs/ranked_hypotheses.csv", "outputs/evidence_audit.csv",
    "outputs/sensitivity.csv", "outputs/research_report.md", "outputs/run_manifest.json",
    "submission/README.md", "submission/Soul_track2_report.md",
    "submission/Soul_track2_slides.html", "submission/Soul_track2_pitch_script.md",
    "submission/submission_manifest.json",
)


def archive(output: Path) -> int:
    payloads = {}
    for relative in FILES:
        path = ROOT.joinpath(*relative.split("/"))
        if path.is_symlink():
            raise ValueError(f"Refusing to package symlink: {relative}")
        payloads[f"track2/{relative}"] = path.read_bytes()
    fingerprints = {
        name: hashlib.sha256(content).hexdigest() for name, content in sorted(payloads.items())
    }
    payloads["track2/ARTIFACT_MANIFEST.json"] = (
        json.dumps({"files_sha256": fingerprints}, indent=2) + "\n"
    ).encode()
    if output.resolve().is_relative_to(ROOT.resolve()):
        raise ValueError("Save the ZIP outside the package directory")
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as handle:
        for name, content in sorted(payloads.items()):
            info = zipfile.ZipInfo(name, date_time=(2026, 9, 5, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            handle.writestr(info, content)
    with zipfile.ZipFile(output) as handle:
        if handle.testzip() is not None or set(handle.namelist()) != set(payloads):
            raise ValueError("ZIP integrity or member verification failed")
        for name, expected in fingerprints.items():
            if hashlib.sha256(handle.read(name)).hexdigest() != expected:
                raise ValueError(f"ZIP checksum mismatch: {name}")
    return len(payloads)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT.parent / "Soul-track2-submission.zip")
    args = parser.parse_args()
    try:
        build_submission()
        count = archive(args.output)
    except (OSError, ValueError, zipfile.BadZipFile) as error:
        parser.exit(1, f"ERROR: {error}\n")
    print(f"ZIP created and verified: {args.output} ({count} files)")


if __name__ == "__main__":
    main()
