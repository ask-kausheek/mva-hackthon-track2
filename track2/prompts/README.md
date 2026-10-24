# Verifiable prompt pack for rare-disease drug-repurposing hypotheses

Four reusable prompts, one shared veto registry, and a deterministic checker.
Swap the `{SLOTS}` and the same chain works for another gene or disease.

The point is not that the prompts are clever. It is that **every reply can be
machine-checked** against a contract, so a prompt that "works" is demonstrable
rather than anecdotal, and a model that invents a citation, advances a vetoed
drug or sets a vague gate is rejected by code, not by trust.

## The chain

| Step | Prompt | Output | Checked for |
|---|---|---|---|
| 1 | [P1 mechanism](01_mechanism.md) | Tiered LoF/GoF chain, harm directions, unknowns | FACT needs a known source; steps are ordered; no fabricated IDs |
| 2 | [P2 longlist](02_longlist.md) | At least 8 screened candidates with veto codes | At least 3 axes; at most 5 advance; advance if and only if no veto |
| 3 | [P3 claims](03_claims.md) | Rows for `data/claims.json` | Full pipeline schema, unknown drug or source, duplicate IDs, scope and source-kind agreement, length, overclaiming |
| 4 | [P4 falsifier](04_falsifier.md) | Numeric kill gates, confounds, weakest link, experiment zero | Gates contain a number; candidates exist; at least 3 confounds |

The deterministic engine (`python -m mva_track2`) still decides every score. The
model curates and argues; it never assigns weight.

[`vetoes.json`](vetoes.json) is the shared exclusion vocabulary
(checkpoint-weakening, no approved product, pediatric tissue harm, chemotherapy
interaction, uncertain direction of effect, not approved, transcript fate
unresolved). Two runs can be compared by veto code.

## Use it with any model

1. Fill the slots in a prompt and send it to any model.
2. Save the reply to a file (fenced or bare JSON both work).
3. Check it from the `track2` folder:

```powershell
python -m mva_track2.promptcheck mechanism reply.txt
python -m mva_track2.promptcheck longlist  reply.txt
python -m mva_track2.promptcheck claims    reply.txt
python -m mva_track2.promptcheck falsifier reply.txt
```

`ACCEPTED` means the reply meets its contract. `REJECTED: <reason>` names the
exact field. `WARNING` lines flag overclaiming wording and every `exact_variant`
label, which a human must re-read against the source.

[`examples/`](examples) holds one hand-authored reply per prompt, built from this
case. Tests run all four through the checker, so an example cannot drift from its
contract.

## Reusing it for another disease

Change `{GENE}`, `{DISEASE}`, `{VARIANTS}`, `{SOURCES}`, `{AXES}`,
`{PATIENT_CONTEXT}`, and replace `data/sources.json`, `drugs.json` and
`claims.json`. The prompts, validator and engine do not change. Add
disease-specific vetoes to `vetoes.json` using a `V_UPPER_CASE` code.

## What has and has not been verified

- Verified: every prompt's slots are documented and used, each golden example
  passes its checker, and each documented rejection rule fires on a deliberately
  broken reply (see `tests/test_promptcheck.py`).
- **Not verified:** how often any particular model produces replies that pass.
  No cross-model benchmark has been run, and none is claimed. The examples are
  illustrations of the contract, not recorded model output.
- A reply that passes is well formed, not scientifically correct. Claims must
  still be re-read against the cited source before they enter `data/claims.json`.
- Output is for research hypotheses only; nothing here recommends treatment.
