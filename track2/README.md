# Soul - Track 2 Research Package

An offline evidence-engineering prototype for approved-drug repurposing
hypotheses in BUB1B-related MVA. **Research hypotheses only: no drug has been
shown by this package to work for this case, and none is recommended for use.**

## Start here

| File | Purpose |
|---|---|
| [Mechanism dossier](docs/mechanism_dossier.md) | Scientific argument, evidence gaps, candidate hypotheses and proposed follow-up |
| [Generated research report](outputs/research_report.md) | Current evidence, disposition, citations and sensitivity summary |
| [Ranked hypotheses](outputs/ranked_hypotheses.csv) | Conditional research priorities; held candidates are not ranked |
| [Evidence audit](outputs/evidence_audit.csv) | Every drug-claim-source relationship |
| [Methods](docs/methods.md) | Input schemas, heuristic scoring and limitations |
| [Architecture](docs/architecture.md) | Components and data flow |
| [Pitch outline](docs/pitch_outline.md) | Three-minute presentation structure; not a recorded video |
| [AI disclosure](docs/ai_disclosure.md) | Provider/model, participant-reported plan and handling limitations |

The initial curated set contains arimoclomol and prescription nicotinic acid
(niacin) as conditional research hypotheses, and gentamicin as a held
exploratory route. This is a small literature-led starting set, not an exhaustive
screen or a clinically validated drug ranking.

## Run locally

Python 3.11 or newer; standard library only. No downloads, API keys, GPU,
external services or dependency installation are needed to run the package.

From the containing folder in PowerShell:

```powershell
Set-Location .\track2
python -m mva_track2
python -m unittest discover -s tests -v
python -m mva_track2.package
```

The package command regenerates the outputs and writes
`Soul-track2-research.zip` in the containing folder. It uses an explicit
allowlist and verifies every archive member against a SHA-256 manifest.

To use a separate curated snapshot:

```powershell
python -m mva_track2 --data-dir .\data --config .\config\prioritization.json --output-dir .\outputs
```

## How prioritization works

1. Validate identifiers, enums, citations and regulatory approval provenance.
2. Require every declared mechanistic step, then separate this support from
   evidence that the drug perturbs the proposed process. Their weaker component
   defines the evidence bridge.
3. Track functional BUBR1 rescue separately. Other-disease outcomes do not
   establish rescue of BUBR1 or the case variants.
4. Apply approval, compatibility, conflict and manually curated safety gates.
5. Rank only conditional research candidates, preserving ties.
6. Cross weight profiles with leave-one-primary-study-out analyses.

There is no min-max normalization, EPCR, clinical probability or trained model.
The numeric index is a transparent heuristic for prioritizing further work.
It cannot override a safety hold. A missing component is an evidence gap, not
evidence that the drug fails.

## Repository map

```text
config/         Explicit scope discounts and sensitivity profiles
data/           Small, manually curated public-literature and label records
docs/           Mechanism dossier, methods, architecture and pitch outline
mva_track2/     Offline validation, prioritization, reporting and packaging
outputs/        Reproducible tables, research report and provenance manifest
tests/          Synthetic fixtures; no patient data
```

Unlike the Track 1 genome-scale data directory, this package's `data/` contains
only the three allowlisted public-evidence JSON files and belongs in the ZIP.
Do not put VCFs, FASTQs, patient tables or clinical source documents there.

## What is and is not ready

This package is a working research foundation: curated evidence, source
provenance, reproducible calculations, uncertainty analysis and proposed
validation. It does not include functional experiments, a comprehensive
database retrieval run, a recorded pitch, a published GitHub repository or a
clinician-reviewed final proposal.

Before final submission, an appropriately qualified genetics/pharmacology
reviewer should assess the variant mechanism, renal and oncology context,
exposure feasibility and omitted evidence. Update drug labels and evidence
dates when extending the snapshot.

The current [Track 2 instructions](https://huggingface.co/spaces/SageBio/rare-disease-real-kid-mva-hackathon-2026/blob/main/tabs/submit_track2.py)
ask for a PDF/Markdown report, a GitHub link and a three-minute pitch video.
The generated research CSV is an internal audit artifact, not a required
Track 2 upload format. The panel reviews the latest team entry.

## Privacy and attribution

The pipeline makes no network requests. Public references were consulted while
curating the package. No source genomic files, genotype-scale derivatives,
credentials, private machine paths, model prompts or clinical documents are
included in the ZIP. Limited named variant findings in the dossier are retained
as research context, not as verified functional measurements.

The package is not a complete audit of earlier conversations, other folders,
backups or prior archives. Those remain subject to the hackathon's data rules.
Source data and publications retain their own terms; links do not grant rights
to redistribute full papers or entire external databases.

### Hackathon acknowledgement

> This work was made possible through the Hackathon, organized by Sage
> Bionetworks in partnership with the MVA Society, Hugging Face, and BEACON
> (The Benchmarking, Evaluation, and Assessment Consortium for Science), with
> prize sponsorship from AWS and Anthropic. We are deeply grateful to the child
> and their family who generously contributed their data and their story to
> advance research into this rare disease. We acknowledge their trust in making
> this Hackathon possible.
