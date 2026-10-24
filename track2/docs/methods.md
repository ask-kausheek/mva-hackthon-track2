# Methods and Evidence Contract

**Team:** Soul  
**Approach:** Allele-aware, evidence-gated repurposing prototype

## Abstract

We built a local evidence-engineering prototype for prioritizing approved-drug
research hypotheses in suspected BUB1B-related MVA. A manually curated public
source registry links regulatory labels and primary studies to structured
claims about gene mechanism, drug translation, functional rescue and safety.
The system distinguishes evidence involving other BUB1B mutations from
unrelated disease models and exact-variant evidence. A weakest-link bridge
requires both a gene-mechanism rationale and primary evidence connecting the
drug to the proposed process. Approved indication, incompatible evidence,
contradictory claims and manual safety holds constrain research eligibility.
Scope-discounted component maxima prevent citation-count inflation, and ties
remain tied. Weight profiles and leave-one-study-out analyses expose dependence
on assumptions and individual publications. Outputs include a cited report,
research-priority table, claim audit and reproducibility fingerprints. The
initial set comprises two conditional hypotheses and a held readthrough route;
no case-specific efficacy has been demonstrated. Strengths are transparent
provenance, direction-aware review and inexpensive reproducibility. Limitations
include a small non-exhaustive corpus, unverified variant functional effects,
no patient-response measurements, heuristic weights and unresolved exposure,
oncology and renal context. Proposed experiments are follow-up plans only.

## Inputs

All three `data/` files are JSON arrays. Unknown fields, duplicate identifiers,
unknown drug/source references and invalid enum values are rejected.

| File | Record fields |
|---|---|
| `sources.json` | `source_id`, `title`, `url`, `kind`, `study_id`, `accessed_on` |
| `drugs.json` | `drug_id`, `name`, `approved_indication`, `approval_status`, `approval_source_id`, `mechanism_id`, `mechanism_description`, `mechanism_claim_groups`, `variant_fit`, `variant_fit_note`, `exposure_status`, `safety_status`, `safety_note` |
| `claims.json` | `claim_id`, `drug_ids`, `source_id`, `dimension`, `relation`, `scope`, `summary` |

### Source and drug fields

- Source `kind`: `primary`, `regulatory`, or `review`.
- `study_id`: stable underlying-study identifier, preferably DOI or PMCID;
  use the same value for all mirrors, and a label identifier for regulatory sources.
- `approval_status`: `approved`, `unverified`, or `not_approved`.
  Approved status requires an existing regulatory source. Indication text must
  identify the jurisdiction/formulation and must not imply MVA approval.
- `variant_fit` and `exposure_status`: `supported`, `unresolved`, or `contradicted`.
- `safety_status`: `unresolved` or `hold`. There is intentionally no automatic
  "safe" state. A hold is a documented research-triage decision, not a diagnosis.
- `mechanism_claim_groups`: required mechanistic steps, each expressed as an
  array of alternative supporting claim IDs. Every group must retain primary
  support; an empty outer array means no established mechanism bridge.
  References must be primary supporting mechanism claims mapped to this drug.

### Claim fields

| Field | Meaning |
|---|---|
| `drug_ids` | Hypotheses for which the claim is relevant; does not imply the study tested those drugs |
| `mechanism` dimension | Gene/pathway link relevant to the proposed intervention direction |
| `translation` dimension | Evidence that the drug acts on the relevant process; another disease is explicitly indirect |
| `functional_rescue` dimension | Actual drug-treatment rescue of a BUBR1-related functional endpoint, not genetic overexpression or protein abundance alone |
| `safety` dimension | Safety evidence or context; not positive efficacy evidence |
| `supports` relation | Supports the stated claim, not necessarily the complete therapeutic hypothesis |
| `contradicts` relation | Directional opposing evidence requiring adjudication |
| `context` relation | Informative limitation, label caution or non-directional evidence |

Scope values are `exact_variant`, `same_gene_other_variant`,
`same_gene_nonvariant`, `other_disease`, `general`, and `regulatory`.
Regulatory scope and regulatory source type must agree.

The schema cannot detect a scientifically mislabeled claim. Human review must
verify species, variant numbering, intervention, experimental context, endpoint,
exposure and whether the paper is corrected/retracted. Mouse variant numbering
must not be transferred directly to a human allele.

## Prioritization

For each required mechanism group, select the maximum configured scope weight
among its available primary supporting claims. The weakest required group
determines mechanism support. Translation and functional rescue use their
strongest qualifying claims. Reviews and regulatory labels contribute zero
numeric support. Repeating a claim or a study adds no points.

```text
M = minimum support across all required mechanism groups
T = strongest qualifying drug-translation support
F = strongest qualifying BUBR1 functional-rescue support
B = min(M, T)

Baseline index = 100 * (0.5 * B + 0.5 * F)
```

Functional-rescue support additionally requires exact-variant or same-gene
scope. A drug improving another disease does not establish BUBR1 rescue.
Genetic overexpression studies can motivate mechanism claims but not establish
drug-mediated functional rescue.

The scope discounts are explicit heuristics: exact variant 1.0, other variants
in the same gene 0.6, nonvariant same-gene models 0.4, other diseases 0.2 and
general evidence 0.1. They are not estimates of success probability. A missing
component numerically contributes zero because evidence is absent, not because
the intervention is disproven.

For example, the niacin chain explicitly requires the SIRT2-BUBR1 link.
Removing its supporting study cannot leave the bridge intact merely because
another paper describes generic BUBR1 mutant instability. Declared steps remain
human-curated; they do not prove that every inference in the proposed pathway
has been experimentally tested.

An index of 100 would require qualifying evidence with maximal scope in the
configured dimensions; it would still not be a clinical efficacy claim.
The leading item is never automatically normalized to 100 or EPCR 1.0.

## Disposition gates

The following ordered rules precede rank assignment:

1. Unverified/non-approved medication status: `ineligible_approval`.
2. Contradicted variant fit or exposure: `held_incompatible`.
3. Curated safety hold: `held_safety`.
4. Contradictory mechanism/translation/rescue claims: `held_conflicting_evidence`.
5. Neither a complete evidence bridge nor functional rescue: `deferred_no_bridge_evidence`.
6. Otherwise: `conditional_research`.

Safety context does not imply proven harm in this individual. Missing clinical
information does not silently become a favorable safety value.
Only conditional candidates receive ranks; tied indices retain the same rank.
Unresolved fit/exposure/safety are prominently disclosed even for ranked items.

## Sensitivity

The baseline 50/50 bridge/rescue profile is compared with 80/20 and 20/80
profiles. Each is also rerun after removing each primary study, one at a time.
Removing a study removes every linked claim and source mirror. Approval labels
and manual safety dispositions stay fixed.

`sensitivity.csv` records all statuses, including candidates that become
deferred. Top-priority counts include ties and are not confidence intervals.
Stable ranks in a tiny corpus do not demonstrate predictive performance.
There is no labeled efficacy benchmark or model-accuracy claim.

## Automation and human review

Sources, hypothesis selection, claim summaries and gates were curated with AI
assistance. The output tables, reports, indices and ablations are generated by
code. This is not fully automated drug discovery. The initial three-drug set
reflects literature-led hypothesis selection and selection bias must be
acknowledged.

The package does not require proprietary drug databases or the raw case genome.
Public source records are linked, not full publications redistributed.
Future retrieval should cover plausible alternatives and negative evidence
systematically before this prototype is described as a comprehensive screen.

## Reusable prompt pack

[`prompts/`](../prompts/README.md) holds four slot-based prompts (mechanism
characterization, veto-coded candidate longlist, claim curation, false-rescue
falsifier), a shared veto registry and golden examples. `mva_track2.promptcheck`
validates any model reply against the same schemas the engine uses: it rejects
unknown or fabricated source and drug IDs, ungrounded FACT labels, advancing a
vetoed candidate, non-numeric go/no-go gates, and malformed claim rows, and it
flags overclaiming wording. The model curates and argues; the deterministic
engine alone assigns weight.

Checked: slot consistency, each golden example, and each rejection rule
(`tests/test_promptcheck.py`). Not checked: how often a given model passes. No
cross-model benchmark has been run or is claimed.

## Runtime and cost

The ranker operates on a small cached ledger and needs no API calls or paid
compute. No universal runtime benchmark or zero-total-cost claim is made.
Literature review, existing hardware and AI subscription access are additional
costs. A local run can be measured in PowerShell:

```powershell
Measure-Command { python -m mva_track2 }
```

## Mapping to the judging rubric

| Criterion | Contribution | Still required |
|---|---|---|
| Scientific rigor (35%) | Citation-level claims, explicit extrapolation, negative evidence and allele uncertainty | Expert mechanism review and functional follow-up |
| Potential impact (25%) | A falsifiable rescue question constrained by renal, growth and cancer context | Evidence of functional benefit without harm |
| Innovation (25%) | Weakest-link evidence paths, preserved ties, abstention/hold decisions and a machine-checkable prompt pack with a veto registry | Comparison with broader retrieval baselines; cross-model testing of the prompts |
| Scalability (15%) | Reusable JSON schema, deterministic local processing, no genome rescans and slot-based prompts for other genes | Validation on additional genes/cases |

Rubric percentages are not drug-score weights. No treatment advice, safety
clearance or efficacy result should be inferred from this package.
