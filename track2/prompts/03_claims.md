# P3 - Evidence claim curation

Purpose: convert source excerpts into rows for `data/claims.json` in exactly the
schema the scoring engine accepts. The model never scores anything; it only
curates claims, and the deterministic engine decides what they are worth.

Output contract: a JSON array validated with
`python -m mva_track2.promptcheck claims reply.txt`. The validator appends the
rows to the current claim set and runs the full pipeline validator, so unknown
drugs, unknown sources, bad enums, duplicate IDs and regulatory-scope mismatches
all fail.

## Slots

| Slot | Meaning |
|---|---|
| `{SOURCE_ID}` | An ID already present in `data/sources.json` |
| `{SOURCE_KIND}` | `primary`, `regulatory` or `review` |
| `{EXCERPT}` | The text actually read: abstract, label section or figure legend |
| `{DRUG_IDS}` | Drug IDs already present in `data/drugs.json` |
| `{EXISTING_CLAIM_IDS}` | Claim IDs already in use |

## Prompt

```text
You are an evidence curator. Extract only claims that the excerpt itself
supports. You are not allowed to use outside knowledge.

SOURCE_ID: {SOURCE_ID}   KIND: {SOURCE_KIND}
EXCERPT
"""
{EXCERPT}
"""

DRUG IDs YOU MAY REFERENCE: {DRUG_IDS}
CLAIM IDs ALREADY USED (do not reuse): {EXISTING_CLAIM_IDS}

RULES
1. One claim per independent finding. If the excerpt supports nothing about
   the listed drugs, return [] rather than stretching it.
2. dimension: mechanism | translation | functional_rescue | safety
   relation:  supports | contradicts | context
   scope:     exact_variant | same_gene_other_variant | same_gene_nonvariant
              | other_disease | general | regulatory
3. scope is the biggest honesty lever. Use exact_variant only if the excerpt
   studies this patient's exact variant. A different disease or gene is
   other_disease. A regulatory label is regulatory and only for a regulatory
   source.
4. summary: one line, at most 450 characters, stating what was observed and
   what it does NOT show (population, model system, exposure). Neutral wording:
   never "cures", "proven", "safe and effective", "will work".
5. A study that reports a negative, null or contrary result is a contradicts
   claim. Do not omit it.
6. Do not copy a number or quote unless it is in the excerpt.

OUTPUT: only a JSON array of objects with exactly these fields.
[
  {"claim_id": "snake_case_unique", "drug_ids": [""], "source_id": "{SOURCE_ID}",
   "dimension": "", "relation": "", "scope": "", "summary": ""}
]
```

## Why it is built this way

- The engine, not the model, assigns weight. A model that over-labels scope
  still cannot raise a score without the scope appearing in the audit table.
- The validator warns on overclaiming vocabulary and on every `exact_variant`
  label, which is the one place a human must re-read the source.
- Returning `[]` is a valid, rewarded outcome.
