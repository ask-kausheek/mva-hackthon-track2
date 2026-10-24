# Track 2 Upload Materials

## What to upload

**Report:** `Soul_track2_report.md` is the standalone methods and hypothesis
report. It includes the abstract, mechanism, candidate rationale, limitations,
actual computational results, public sources, AI disclosure and acknowledgement.
It is a research proposal, not evidence that a medicine works.

**GitHub URL:** create your repository from the ZIP contents. The form requires
the URL, not the ZIP. The curated `data/` JSON files belong in the repository;
raw genomic files and clinical source documents do not.

**Video URL:** the three-minute pitch video follows the six slides and the
narration in `Soul_track2_pitch_script.md` (`config/pitch.json`). We
build uses a synthetic text-to-speech voice and says so on its footer and in its
description. The MP4 is not part of this repository or the ZIP: upload it to
YouTube , then provide that URL in the form. The HTML deck and script
do not substitute for the video. To use your own voice instead, record the
slides with `Soul_track2_slides.html` and the script, and update
`docs/ai_disclosure.md` and report section 7 to match.

No XLSX or drug-ranking CSV upload is required by the Track 2 form.
The `outputs/` CSVs remain reproducibility and evidence-audit artifacts.

## Reproduce the local materials

From the `track2` directory:

```powershell
python -m mva_track2.submission
python -m mva_track2.package
```

`submission_manifest.json` distinguishes prepared local files from the video
upload, hosting and GitHub steps that you will complete (`recorded_video` is
`prepared_locally_not_packaged`; the hosted URL and repository URL remain
`user_action_required`). Source/configuration hashes
prevent an unchanged scientific report from silently accompanying changed
evidence. If that guard fails, reconcile the report and pitch before updating
`config/submission_review.json`; do not treat hash changes as scientific review.

## Input provenance

The VCF, HPO and limited FASTQ work occurred in the earlier Track 1 analysis.
Its putative BUB1B findings were manually carried into this proposal. Track 2
does not reread the VCF/FASTQs, confirm the diagnosis, or infer parental
genotypes. Its code operates on curated public-literature and regulatory
evidence; clinical context informs written limitations and manually curated
dispositions rather than an automatic phenotype-to-drug score.
