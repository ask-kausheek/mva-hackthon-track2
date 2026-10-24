# Track 2 Research Evidence Report

**Team:** Soul  
**Status:** Exploratory research prototype; not a treatment recommendation.  
**Snapshot:** `c057862d598f59dcc6d2223c88a79cd46c7f532e3bd68e625aefab961ad6ed77`

## Scope

This report summarizes a manually curated, non-exhaustive public-evidence snapshot.
It is not a validated drug screen, clinical safety clearance, or evidence that a
medicine works in MVA. No patient treatment or wet-lab experiments were performed.
Market approval applies only to the cited indication and formulation, not this case.

## Conditional research shortlist

| Priority (ties retained) | Drug | Status | Evidence index / 100 | BUBR1 functional-rescue evidence |
|---|---|---|---:|---|
| 1 | Arimoclomol | conditional_research | 10.00 | Not found in snapshot |
| 1 | Niacin (nicotinic acid; extended-release label reference) | conditional_research | 10.00 | Not found in snapshot |
| - | Gentamicin | held_safety | Not ranked | Not found in snapshot |

## Interpretation

Ranks prioritize further literature and experimental work, not administration.
Zero component support means missing qualifying evidence, not proof of no effect.
Ties are genuine; alphabetical display order does not break them.
A claim associated with a drug can describe a proposed mechanistic bridge rather
than an experiment testing that drug. Read the claim summary and scope.

## Per-hypothesis rationale and gaps

### Arimoclomol

**Approved indication:** US MIPLYFFA, in combination with miglustat, for neurological manifestations of Niemann-Pick disease type C in adults and pediatric patients aged 2 years and older; not an MVA indication. ([arimoclomol_miplyffa_label](https://dailymed.nlm.nih.gov/dailymed/fda/fdaDrugXsl.cfm?setid=5feffc0e-453d-47fa-91dd-38d4952309bc))

**Proposed mechanism:** Conditional research bridge from heat-shock protein co-induction in other disease models to stabilization of residual functional BUBR1. HSP70-centered observations do not establish enhancement of the HSP90-dependent folding reported for other BUBR1 mutants; the label states the clinical mechanism in NPC is unknown.

**Disposition:** Research prioritization only; variant fit, exposure and safety require review.

**Variant fit (unresolved):** Neither hypothetical allele has demonstrated arimoclomol responsiveness. The missense allele may or may not be unstable yet functional; phase, transcript annotation, protein abundance and checkpoint function remain unverified. Stabilization cannot be assumed to replace missing sequence from a truncating allele.

**Exposure relevance:** unresolved.

**Safety (unresolved):** Renal impairment alters exposure; OCT2 inhibition can change serum creatinine without reduced glomerular function and can affect other OCT2 substrates. Decreased weight, appetite and gastrointestinal events were reported in a population receiving concomitant miglustat. Current renal function, oncology regimen and interaction profile are unknown; no case-specific contraindication or safe MVA exposure is established.

| Claim | Domain / relation / scope | Source |
|---|---|---|
| Several other MVA-associated BUBR1 missense mutants had reduced protein abundance and increased turnover. This supports investigating residual-protein stabilization, not instability of the hypothetical alleles or activity of either mapped drug. | mechanism / supports / same_gene_other_variant | [bubr1_mva_mechanisms_2010](https://pmc.ncbi.nlm.nih.gov/articles/PMC2887387/) |
| HSP90 inhibition with geldanamycin reduced I909T and L1012P mutant BUBR1 abundance in cells. Loss under inhibition is not evidence that arimoclomol or HSP70 induction stabilizes BUBR1. | mechanism / context / same_gene_other_variant | [bubr1_mva_mechanisms_2010](https://pmc.ncbi.nlm.nih.gov/articles/PMC2887387/) |
| Forced expression of I909T and L1012P to levels comparable to wild-type restored the nocodazole checkpoint response in a replacement-cell assay. This was genetic expression manipulation, not treatment with either mapped drug and not exact-variant rescue. | mechanism / supports / same_gene_other_variant | [bubr1_mva_mechanisms_2010](https://pmc.ncbi.nlm.nih.gov/articles/PMC2887387/) |
| The stable Y155C mutant restored chromosome alignment but not checkpoint activity in the studied assay. Protein abundance alone therefore cannot establish functional correction of a different BUBR1 allele. | mechanism / context / same_gene_other_variant | [bubr1_mva_mechanisms_2010](https://pmc.ncbi.nlm.nih.gov/articles/PMC2887387/) |
| Figure 6 reports arimoclomol treatment of NPC patient fibroblasts and NPC-model mice: reduced fibroblast lysosomal storage and cholesterol accumulation, and increased brain HSF1 activation and HSP70 in treated mice. This is primary drug-tested evidence in another disease, not BUBR1 stabilization, MVA efficacy or exact-variant rescue. | translation / supports / other_disease | [hsp_sphingolipidoses_2016](https://pmc.ncbi.nlm.nih.gov/articles/PMC6821533/) |
| Section 1 lists MIPLYFFA with miglustat for neurological manifestations of NPC in adults and pediatric patients aged 2 years and older. This establishes approved-product eligibility only, not numeric translation evidence, approval or efficacy for MVA. | translation / context / regulatory | [arimoclomol_miplyffa_label](https://dailymed.nlm.nih.gov/dailymed/fda/fdaDrugXsl.cfm?setid=5feffc0e-453d-47fa-91dd-38d4952309bc) |
| Section 12.1 states that the mechanism of arimoclomol's clinical effects in NPC is unknown. Regulatory approval does not validate the proposed BUBR1 chaperone mechanism. | translation / context / regulatory | [arimoclomol_miplyffa_label](https://dailymed.nlm.nih.gov/dailymed/fda/fdaDrugXsl.cfm?setid=5feffc0e-453d-47fa-91dd-38d4952309bc) |
| Sections 8.6 and 12.3 describe increased arimoclomol exposure with moderate to severe renal impairment and an unevaluated lowest-renal-function category. These are labeled population constraints, not evidence of renal impairment in the hypothetical case. | safety / context / regulatory | [arimoclomol_miplyffa_label](https://dailymed.nlm.nih.gov/dailymed/fda/fdaDrugXsl.cfm?setid=5feffc0e-453d-47fa-91dd-38d4952309bc) |
| Sections 5.3, 7.1 and 12.3 describe reversible creatinine increases without measured glomerular-function change, OCT2 inhibition and possible increased exposure of OCT2 substrates. Creatinine changes should not automatically be equated with kidney injury. | safety / context / regulatory | [arimoclomol_miplyffa_label](https://dailymed.nlm.nih.gov/dailymed/fda/fdaDrugXsl.cfm?setid=5feffc0e-453d-47fa-91dd-38d4952309bc) |
| Section 6.1 reports decreased weight, decreased appetite and diarrhea in the subgroup also receiving miglustat, and hypersensitivity reactions in the trial. Combination-population observations cannot be assigned solely to arimoclomol or assumed to occur in MVA. | safety / context / regulatory | [arimoclomol_miplyffa_label](https://dailymed.nlm.nih.gov/dailymed/fda/fdaDrugXsl.cfm?setid=5feffc0e-453d-47fa-91dd-38d4952309bc) |

### Niacin (nicotinic acid; extended-release label reference)

**Approved indication:** US prescription extended-release niacin for labeled lipid disorders, including primary hyperlipidemia and mixed dyslipidemia; not an MVA indication. ([niacin_extended_release_label](https://dailymed.nlm.nih.gov/dailymed/fda/fdaDrugXsl.cfm?setid=dd60fe81-3d54-4a29-9502-601be89c575e))

**Proposed mechanism:** Conditional research chain: nicotinic-acid metabolism contributes to NAD, which may support SIRT2-dependent BUBR1 stabilization if residual protein remains functional. A separate adult mitochondrial-myopathy study reported niacin-associated NAD increases, not BUBR1 correction. Retrieved BUBR1 experiments used NMN or genetic SIRT2 manipulation, not niacin; niacin, nicotinamide and NMN are not interchangeable.

**Disposition:** Research prioritization only; variant fit, exposure and safety require review.

**Variant fit (unresolved):** No niacin rescue of either hypothetical allele has been demonstrated. A retained SIRT2-regulated sequence or increased BUBR1 abundance would not by itself establish correct checkpoint function, phase or transcript validity.

**Exposure relevance:** unresolved.

**Safety (unresolved):** The referenced label does not establish safety or effectiveness at age 16 years or younger and advises renal caution; active liver disease and certain unexplained hepatic abnormalities are contraindications. Muscle toxicity with concomitant statins is labeled, but no such concomitant treatment is assumed. The adult mitochondrial-myopathy study reported an anemia tendency in some patients, not pediatric or MVA safety. Current renal and hepatic measurements and medication list are unavailable. Formulations are not presumed interchangeable.

| Claim | Domain / relation / scope | Source |
|---|---|---|
| Several other MVA-associated BUBR1 missense mutants had reduced protein abundance and increased turnover. This supports investigating residual-protein stabilization, not instability of the hypothetical alleles or activity of either mapped drug. | mechanism / supports / same_gene_other_variant | [bubr1_mva_mechanisms_2010](https://pmc.ncbi.nlm.nih.gov/articles/PMC2887387/) |
| Forced expression of I909T and L1012P to levels comparable to wild-type restored the nocodazole checkpoint response in a replacement-cell assay. This was genetic expression manipulation, not treatment with either mapped drug and not exact-variant rescue. | mechanism / supports / same_gene_other_variant | [bubr1_mva_mechanisms_2010](https://pmc.ncbi.nlm.nih.gov/articles/PMC2887387/) |
| The stable Y155C mutant restored chromosome alignment but not checkpoint activity in the studied assay. Protein abundance alone therefore cannot establish functional correction of a different BUBR1 allele. | mechanism / context / same_gene_other_variant | [bubr1_mva_mechanisms_2010](https://pmc.ncbi.nlm.nih.gov/articles/PMC2887387/) |
| Cell and biochemical experiments linked SIRT2-dependent deacetylation of BubR1 lysine 668 to reduced ubiquitylation and increased stability. This supplies pathway rationale, not niacin treatment evidence or correction of a specific BUB1B variant. | mechanism / supports / same_gene_nonvariant | [sirt2_bubr1_nad_2014](https://pmc.ncbi.nlm.nih.gov/articles/PMC4194088/) |
| NMN treatment increased BubR1 abundance in wild-type mice. The paper's lifespan experiment used SIRT2 overexpression in hypomorphic mice, not niacin or NMN treatment; neither result establishes niacin-mediated checkpoint rescue. | mechanism / supports / same_gene_nonvariant | [sirt2_bubr1_nad_2014](https://pmc.ncbi.nlm.nih.gov/articles/PMC4194088/) |
| Nicotinamide used as a sirtuin inhibitor reduced BubR1 levels in the reported cell experiments. This is a compound-and-context caution against treating nicotinic acid, nicotinamide and NMN as interchangeable, not proof that niacin harms BUBR1 function. | mechanism / context / same_gene_nonvariant | [sirt2_bubr1_nad_2014](https://pmc.ncbi.nlm.nih.gov/articles/PMC4194088/) |
| The primary study abstract reports that administered niacin increased blood NAD in adult-onset mitochondrial-myopathy patients and matched controls, with patient muscle NAD reaching control levels. This establishes human pharmacodynamic observations in a different disease, not NAD deficiency, muscle benefit, BUBR1 correction or feasible exposure in the hypothetical MVA case. | translation / supports / other_disease | [niacin_human_nad_myopathy_2020](https://europepmc.org/article/MED/32386566) |
| Sections 11 and 12.3 identify the product as nicotinic acid and describe a metabolic pathway producing NAD. This biochemical entry point does not establish a target-tissue NAD increase, SIRT2 engagement or BUBR1 rescue in MVA. | mechanism / supports / regulatory | [niacin_extended_release_label](https://dailymed.nlm.nih.gov/dailymed/fda/fdaDrugXsl.cfm?setid=dd60fe81-3d54-4a29-9502-601be89c575e) |
| Section 1 lists lipid-disorder indications for prescription extended-release niacin. This is approved-product eligibility only, not numeric translation evidence, MVA treatment evidence or interchangeability with supplements or other formulations. | translation / context / regulatory | [niacin_extended_release_label](https://dailymed.nlm.nih.gov/dailymed/fda/fdaDrugXsl.cfm?setid=dd60fe81-3d54-4a29-9502-601be89c575e) |
| Sections 4 and 8.4-8.7 state that safety and effectiveness at age 16 years or younger are unestablished, advise renal caution, and list active liver disease and specified unexplained hepatic abnormalities as contraindications. No individual contraindication is inferred without relevant clinical data. | safety / context / regulatory | [niacin_extended_release_label](https://dailymed.nlm.nih.gov/dailymed/fda/fdaDrugXsl.cfm?setid=dd60fe81-3d54-4a29-9502-601be89c575e) |
| Section 5.2 describes rhabdomyolysis associated with concomitant niacin and statins. This is a medication-review constraint, not evidence of statin exposure or drug-induced muscle injury in the hypothetical case. | safety / context / regulatory | [niacin_extended_release_label](https://dailymed.nlm.nih.gov/dailymed/fda/fdaDrugXsl.cfm?setid=dd60fe81-3d54-4a29-9502-601be89c575e) |

### Gentamicin

**Approved indication:** US injectable antibacterial for serious infections caused by susceptible bacteria; not an MVA or premature-stop-codon indication. ([gentamicin_injection_label](https://dailymed.nlm.nih.gov/dailymed/fda/fdaDrugXsl.cfm?setid=84f5c763-1cd3-4d85-9afb-934db8666fbf))

**Proposed mechanism:** Held exploratory premature-stop-codon readthrough hypothesis. The curated evidence provides no direct gentamicin rescue of BUB1B or the hypothetical truncating allele; transcript survival, stop context, full-length product identity and checkpoint function would all require demonstration.

**Disposition:** Manual research-triage hold, not a proven individual contraindication: the mechanism bridge is weak and the injection label carries nephrotoxicity and potentially irreversible ototoxicity warnings. Renal calcification does not establish renal failure. Current renal function, hearing baseline and potentially nephrotoxic or ototoxic oncology exposures are unknown; absence of efficacy evidence is not encoded as evidence of harm.

**Variant fit (unresolved):** A protein-level premature-stop annotation alone does not establish a readable transcript or a functional readthrough product. The exact transcript, local stop context and nonsense-mediated decay status have not been reverified. No positive drug-specific BUB1B readthrough evidence is encoded.

**Exposure relevance:** unresolved.

**Safety (hold):** Manual research-triage hold, not a proven individual contraindication: the mechanism bridge is weak and the injection label carries nephrotoxicity and potentially irreversible ototoxicity warnings. Renal calcification does not establish renal failure. Current renal function, hearing baseline and potentially nephrotoxic or ototoxic oncology exposures are unknown; absence of efficacy evidence is not encoded as evidence of harm.

| Claim | Domain / relation / scope | Source |
|---|---|---|
| Transcript and protein findings for other BUBR1 truncations were consistent with transcript loss and possible nonsense-mediated decay. This motivates measuring transcript availability before any readthrough experiment; it is not gentamicin evidence or proof of decay for the hypothetical allele. | mechanism / context / same_gene_other_variant | [bubr1_mva_mechanisms_2010](https://pmc.ncbi.nlm.nih.gov/articles/PMC2887387/) |
| The boxed warning describes nephrotoxicity, potentially irreversible auditory or vestibular toxicity, and added concern with other nephrotoxic or ototoxic drugs. These labeled hazards inform research triage but do not prove a case-specific contraindication. | safety / context / regulatory | [gentamicin_injection_label](https://dailymed.nlm.nih.gov/dailymed/fda/fdaDrugXsl.cfm?setid=84f5c763-1cd3-4d85-9afb-934db8666fbf) |

## Transparent prioritization

Only primary supporting claims receive numeric scope discounts. Regulatory
labels establish approval and safety context; reviews and labels add no points.
Each declared mechanism step uses its strongest qualifying evidence; the weakest
required step controls mechanism support. Other components use maxima, not citation counts.
The evidence bridge uses the weaker of mechanism and drug-translation support.

```text
mechanism_support = min(max(support for each required mechanism step))
bridge = min(mechanism_support, translation_support)
index = 100 * (0.5 * bridge + 0.5 * functional_rescue_support)
```

Discounts and profile weights are explicit human heuristics, not learned or
calibrated probabilities and not the judges' rubric. There is no Top-K min-max
normalization. Safety holds, incompatible evidence and unverified approval
cannot be overridden by a high index.

| Evidence scope | Discount |
|---|---:|
| exact_variant | 1 |
| same_gene_other_variant | 0.6 |
| same_gene_nonvariant | 0.4 |
| other_disease | 0.2 |
| general | 0.1 |
| regulatory | 0 |

## Sensitivity and fragility

All weight profiles are crossed with leave-one-primary-study-out ablations.
All claims from a study are removed together, including mirrored source entries.
Approval labels and curated safety holds remain in place. This tests dependence
on the small curated corpus, not predictive accuracy or out-of-sample performance.

| Drug | Scenarios rankable / total | Top-priority scenarios (including ties) |
|---|---:|---:|
| Arimoclomol | 9/15 | 9/15 |
| Niacin (nicotinic acid; extended-release label reference) | 6/15 | 6/15 |
| Gentamicin | 0/15 | 0/15 |

## Required next evidence

- Reverify transcript-specific allele annotation, residual protein function and phase.
- Establish current renal function, oncology context and exposure feasibility through qualified review.
- Separate normal-cell functional rescue from tumor-cell survival or treatment interference.
- Test functional chromosome-segregation endpoints, not protein abundance alone.
- Distinguish genuine rescue from cell-cycle arrest or selective death of abnormal cells.
- Obtain genetics/pharmacology review before any clinical interpretation.

## Reproducibility and limitations

The pipeline is offline and uses the Python standard library. Evidence inclusion,
scope labels and safety dispositions were manually curated with AI assistance.
Automated output does not imply automated discovery or independent verification.
There is no patient RNA/protein assay, drug response dataset, complete candidate
universe, or trained efficacy model. This package cannot infer parental genotypes.
Source fingerprints and code fingerprints are in `run_manifest.json`;
claim-level provenance is in `evidence_audit.csv`.

See `../docs/mechanism_dossier.md` for the scientific argument and proposed
follow-up, `../docs/methods.md` for schema and scoring details, and
`../docs/ai_disclosure.md` for assistance and data-handling disclosures.

## Sources

- **arimoclomol_miplyffa_label**: [MIPLYFFA (arimoclomol) capsules: US prescribing information](https://dailymed.nlm.nih.gov/dailymed/fda/fdaDrugXsl.cfm?setid=5feffc0e-453d-47fa-91dd-38d4952309bc). regulatory; study `5feffc0e-453d-47fa-91dd-38d4952309bc`; accessed 2026-09-05.
- **bubr1_mva_mechanisms_2010**: [Molecular Causes for BUBR1 Dysfunction in the Human Cancer Predisposition Syndrome Mosaic Variegated Aneuploidy](https://pmc.ncbi.nlm.nih.gov/articles/PMC2887387/). primary; study `10.1158/0008-5472.CAN-09-4319`; accessed 2026-09-05.
- **gentamicin_injection_label**: [Gentamicin Injection, USP: US prescribing information](https://dailymed.nlm.nih.gov/dailymed/fda/fdaDrugXsl.cfm?setid=84f5c763-1cd3-4d85-9afb-934db8666fbf). regulatory; study `84f5c763-1cd3-4d85-9afb-934db8666fbf`; accessed 2026-09-05.
- **hsp_sphingolipidoses_2016**: [Heat Shock Protein-based therapy as a potential candidate for treating sphingolipidoses](https://pmc.ncbi.nlm.nih.gov/articles/PMC6821533/). primary; study `10.1126/scitranslmed.aad9823`; accessed 2026-09-05.
- **niacin_extended_release_label**: [Niacin extended-release tablets: US prescribing information](https://dailymed.nlm.nih.gov/dailymed/fda/fdaDrugXsl.cfm?setid=dd60fe81-3d54-4a29-9502-601be89c575e). regulatory; study `dd60fe81-3d54-4a29-9502-601be89c575e`; accessed 2026-09-05.
- **niacin_human_nad_myopathy_2020**: [Niacin Cures Systemic NAD+ Deficiency and Improves Muscle Performance in Adult-Onset Mitochondrial Myopathy](https://europepmc.org/article/MED/32386566). primary; study `10.1016/j.cmet.2020.04.008`; accessed 2026-09-05.
- **sirt2_bubr1_nad_2014**: [SIRT2 induces the checkpoint kinase BubR1 to increase lifespan](https://pmc.ncbi.nlm.nih.gov/articles/PMC4194088/). primary; study `10.15252/embj.201386907`; accessed 2026-09-05.
