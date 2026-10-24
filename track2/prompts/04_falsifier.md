# P4 - False-rescue firewall (adversarial falsifier)

Purpose: for every candidate that survives screening, force the model to argue
against it and to write numeric go/no-go gates before any result exists. In
aneuploidy diseases a lower aneuploidy rate, or more of the causal protein, can
come from dead daughter cells, cell-cycle arrest, or assay artefacts rather than
from rescue. This prompt is gene-agnostic; replace the slots to reuse it.

Output contract: one JSON object, validated with
`python -m mva_track2.promptcheck falsifier reply.txt`. Every kill criterion must
contain a number, name a known drug ID or `all`, and end in `no-go` or `defer`.

## Slots

| Slot | Meaning |
|---|---|
| `{CANDIDATES}` | Drug IDs and one-line hypotheses that survived P2 |
| `{READOUTS}` | Assays the lab can run, for example `BUBR1 immunoblot; mitotic timing; micronuclei; karyotype` |
| `{EXPOSURE}` | Clinically relevant exposure range with its source, or `unknown` |
| `{MECHANISM_JSON}` | Validated output of prompt P1 |

## Prompt

```text
You are a skeptical assay scientist. Your job is to make this hypothesis fail
before anyone spends money on it.

MECHANISM
{MECHANISM_JSON}

CANDIDATES
{CANDIDATES}

AVAILABLE READOUTS
{READOUTS}

CLINICALLY RELEVANT EXPOSURE
{EXPOSURE}

RULES
1. kill_criteria: for each candidate, at least one pre-specified rule of the
   form measurement + numeric threshold + consequence. The threshold must
   contain a number. decision_if_fail is "no-go" (drop) or "defer"
   (inconclusive). Use candidate "all" for rules that apply to every candidate.
2. A rescue claim requires more than one signal. State that "more protein" is
   not rescue unless a functional readout improves in the same cells.
3. confounds: at least three specific ways a positive result could be false,
   for example cell death, cytostasis, fewer divisions, measurement failure,
   supraphysiological dose.
4. Test concentrations must not exceed the stated clinical exposure; if
   exposure is "unknown", say so and make this a defer rule, not a pass.
5. weakest_link: name the single claim in the mechanism or candidate chain
   whose failure would collapse the hypothesis, and why.
6. experiment_zero: the one cheapest measurement, in the patient's own cells or
   the exact-allele model, to run before any drug. If its result is normal, the
   hypothesis is dropped.
7. Do not speculate about efficacy.

OUTPUT: only this JSON.
{
  "kill_criteria": [
    {"candidate": "drug_id|all", "measurement": "", "threshold": "",
     "decision_if_fail": "no-go|defer"}
  ],
  "confounds": ["", "", ""],
  "weakest_link": {"claim": "", "why": ""},
  "experiment_zero": ""
}
```

## Why it is built this way

- Thresholds are written before data exists, so they cannot be tuned to a
  favourable result.
- `weakest_link` mirrors the engine's weakest-link bridge scoring: the claim
  the model names should agree with the lowest-scoring step in the
  deterministic report. A mismatch is a finding.
