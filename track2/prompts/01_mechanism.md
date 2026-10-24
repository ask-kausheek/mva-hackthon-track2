# P1 - Variant mechanism characterization

Purpose: turn a variant list into an explicit loss/gain-of-function mechanism
chain in which every step is labelled by how well it is known. Reusable for any
gene and disease by filling the slots.

Output contract: one JSON object, validated with
`python -m mva_track2.promptcheck mechanism reply.txt`.

## Slots

| Slot | Meaning |
|---|---|
| `{GENE}` | Gene symbol, for example `BUB1B` |
| `{DISEASE}` | Disease name and inheritance, for example `mosaic variegated aneuploidy 1, autosomal recessive` |
| `{VARIANTS}` | One line per variant: HGVS or protein change, zygosity, ClinVar class, population frequency, in-silico scores |
| `{SOURCES}` | Allowed source IDs, each with title and one-line gist |

## Prompt

```text
You are a rare-disease molecular geneticist. Characterize the mechanism of
{GENE}-related {DISEASE} for this case. This is hypothesis generation for
expert review, not clinical advice.

VARIANTS
{VARIANTS}

ALLOWED SOURCES (the only citations you may use)
{SOURCES}

RULES
1. Label every statement with exactly one tier:
   FACT        directly stated by an allowed source; cite its source_ids.
   INFERENCE   follows from facts by a stated logical step; no new data.
   HYPOTHESIS  plausible but untested.
   A FACT without an allowed source_id is invalid. Never invent a citation,
   number, quote or database record. If unsure, downgrade the tier.
2. Classify each variant: LoF, hypomorph, GoF, or unknown. State separately
   whether the variant is expected to change protein abundance, catalysis,
   localization, or is unknown. Do not assume haploinsufficiency or
   dominant-negative action without a cited basis.
3. If two variants are in one gene, state that phase (cis/trans) is unknown
   unless a source or parental data establishes it.
4. Build a numbered chain: variant -> molecular consequence -> pathway
   consequence -> cellular phenotype -> patient phenotype. Do not skip a link.
5. List harm_directions: interventions that would worsen this mechanism
   (for example weakening an already-impaired checkpoint).
6. List unknowns: the specific measurements that would settle each open step.
7. Do not name or recommend any drug in this task.

OUTPUT: only this JSON, no prose before or after.
{
  "variants": [
    {"label": "", "effect_class": "LoF|hypomorph|GoF|unknown",
     "tier": "FACT|INFERENCE|HYPOTHESIS", "source_ids": []}
  ],
  "chain": [
    {"step": 1, "statement": "", "tier": "FACT|INFERENCE|HYPOTHESIS", "source_ids": []}
  ],
  "lesion_type": "abundance|catalysis|localization|unknown",
  "harm_directions": [""],
  "unknowns": [""]
}
```

## Why it is built this way

- The tier labels make unsupported steps visible instead of buried in prose.
- The validator rejects any FACT that cites nothing, and any citation outside
  the supplied source list, so fabricated references fail mechanically.
- Forbidding drug names here keeps mechanism reasoning independent of the
  candidate it later has to support.
