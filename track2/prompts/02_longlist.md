# P2 - Candidate longlist with a veto registry

Purpose: a screen that shows what was considered and why each option was
dropped, so the shortlist cannot be accused of cherry-picking. The veto codes
live in [`vetoes.json`](vetoes.json) and are the same for every disease; add
disease-specific vetoes there.

Output contract: one JSON object, validated with
`python -m mva_track2.promptcheck longlist reply.txt`. The validator requires at
least 8 screened candidates, no duplicates, at most 5 advancing, and a veto code
on every non-advancing row.

## Slots

| Slot | Meaning |
|---|---|
| `{MECHANISM_JSON}` | Validated output of prompt P1 |
| `{AXES}` | Intervention axes to screen, for example `restore protein abundance; stabilize protein; correct splicing; suppress NMD; readthrough; selective lethality of aneuploid cells; supportive` |
| `{VETOES}` | Contents of `vetoes.json` |
| `{PATIENT_CONTEXT}` | Age, organ involvement, anticipated therapies |

## Prompt

```text
You are a clinical pharmacologist screening approved drugs as research
hypotheses. Nothing you output is a recommendation to treat.

MECHANISM
{MECHANISM_JSON}

PATIENT CONTEXT
{PATIENT_CONTEXT}

AXES TO COVER
{AXES}

VETO CODES (use exactly these)
{VETOES}

RULES
1. Screen at least 8 distinct candidates spanning at least 3 axes. Include
   candidates you expect to reject; the rejections are the point.
2. Every candidate gets exactly one verdict:
   advance   survives every veto; veto_code must be "none".
   hold      plausible but blocked by an unresolved question; give a veto_code.
   exclude   fails a veto; give the veto_code.
   Any verdict other than advance requires a veto_code from the list.
3. At most 5 candidates may advance. Prefer fewer. Rank by how cheaply the
   first experiment could disprove the idea, not by how appealing it sounds.
4. For advance rows, first_experiment must be one concrete measurement in the
   patient's own cells or an exact-allele model, not a trial.
5. Check the patient context against each candidate: pediatric safety,
   interaction with anticipated chemotherapy, organ toxicity.
6. Do not claim efficacy. Do not state an approval, dose, label wording or
   trial number you cannot verify; say "verify against label" instead.

OUTPUT: only this JSON.
{
  "longlist": [
    {"name": "", "axis": "", "verdict": "advance|hold|exclude",
     "veto_code": "none|V_...", "reason": "", "first_experiment": ""}
  ]
}
```

## Why it is built this way

- A fixed veto vocabulary turns "I excluded it" into an auditable, reusable
  rule. Two runs can be diffed by veto code.
- Rejections carry equal weight to selections, which is the opposite of the
  usual "here is my favourite drug" answer.
- The `advance <=> none` rule is checked by code, so a model cannot advance a
  vetoed candidate or reject one without a reason.
