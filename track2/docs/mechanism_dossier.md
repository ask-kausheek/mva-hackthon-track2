# SageBio MVA Track2: conditional mechanism dossier

**Research hypothesis prioritization only: no treatment advice, prescription, dosing, or claim of clinical efficacy.**
Evidence reviewed on 2026-09-05; this is a targeted, non-exhaustive public-source review, not a systematic review.
No wet-lab work, drug exposure study, variant rescue experiment, or prospective clinical validation was completed.

## How to interpret the evidence

**A claim's `drug_ids` mapping is an explicit mechanistic or translation BRIDGE, not proof that the mapped drug was tested.**
`supports` means support for the narrowly stated claim and its scope, not endorsement of a candidate or proof of benefit.
Regulatory approval is eligibility only, not numeric translation evidence; none of these labels establishes MVA treatment.
Positive translation claims require primary drug-tested observations; both conditional candidates have only other-disease translation evidence.
`context` preserves limitations and safety observations; missing evidence is not encoded as harm or a contradictory result.
All variant-fit and exposure statuses remain `unresolved`; no `exact_variant` or `functional_rescue` claims are present.
Genetic overexpression and protein-abundance findings are mechanism evidence, not drug-mediated functional rescue.
Claims from one article or label share a `study_id`; multiple claims are not independent studies or replications.
Consult the generated `outputs/research_report.md` for the ranker's research ordering, not a clinical recommendation.
The weak-link evidence bridge is a heuristic, not a probability or expected benefit; scope discounts, weight sensitivity and ties remain material.
No confirmed live Track1 score is available, and no Track1 score or diagnostic certainty is inferred here.

## Conditional genetic starting point

The hypothetical pair is BUB1B p.Leu737Ter plus p.Asn1002Lys, each described as heterozygous in prior analysis.
Transcript-specific annotations have not been reverified; neither exact allele was demonstrated to respond in the cited literature.
Phase is unresolved: two heterozygous calls do not prove variants in trans, compound heterozygosity, or a recessive diagnosis.
Parental genotypes are unavailable. Family reproductive-loss context is not segregation evidence or proof of inheritance.
A premature-stop annotation does not establish nonsense-mediated decay (NMD), residual transcript, or a functional truncated protein.
The missense allele's abundance, localization, residual checkpoint activity and relationship to the phenotype remain unproven.
Protein stabilization is relevant only if a recoverable, functional protein species exists; more defective protein may not help.
Sequence retained around a regulatory site is insufficient to establish folding, partner binding or functional correction.

## Shared BUBR1 rationale and its limits

The 2010 MVA study linked some other BUBR1 missense alleles to reduced abundance and increased turnover (`bubr1_mva_mechanisms_2010`, Figs. 2-3).
Forced expression of I909T and L1012P to wild-type-like levels restored the nocodazole checkpoint response in engineered cells (Fig. 4).
That result was genetic expression manipulation, not arimoclomol, niacin, gentamicin, or rescue of the hypothetical alleles.
The stable Y155C protein retained chromosome-alignment activity but not checkpoint activity (Fig. 5): abundance and function are distinct.
Findings for other truncations supported possible transcript loss/NMD; they do not establish the fate of p.Leu737Ter.
Thus the shared chain is conditional: verified allele mechanism -> residual functional BUBR1 -> target engagement -> improved checkpoint fidelity.
Every arrow after the verified literature observation requires testing in the relevant genetic and cellular context.

## Conditional candidate: arimoclomol

**Proposed chain:** heat-shock co-induction -> suitable chaperone engagement -> stabilization of residual functional BUBR1 -> checkpoint improvement.
The MVA study actually inhibited HSP90 with geldanamycin; I909T and L1012P abundance fell (`bubr1_mva_mechanisms_2010`, Fig. 3).
Dependency under HSP90 inhibition does not prove reversibility by increasing chaperones, and HSP70 is not interchangeable with HSP90.
The sphingolipidosis study tested recombinant HSP70 broadly and arimoclomol in NPC models (`hsp_sphingolipidoses_2016`, Fig. 6).
Arimoclomol reduced lysosomal storage/cholesterol accumulation in NPC fibroblasts and increased brain HSF1 activation and HSP70 in NPC-model mice.
These drug-tested findings supply primary other-disease translation evidence, not evidence that HSP90-dependent BUBR1 folding is enhanced.
Those lysosomal-disease findings motivate a bridge; they did not test BUB1B, MVA or either hypothetical allele.
The MIPLYFFA label states that arimoclomol's clinical mechanism in NPC is unknown (`arimoclomol_miplyffa_label`, section 12.1).
Its US approval is with miglustat for neurological NPC manifestations at age 2 years and older, not for MVA.
Neither that combination nor its exposure regimen is transferred to this hypothesis; miglustat is not a Track2 candidate.
Renal impairment changes exposure; OCT2 inhibition may alter creatinine and concomitant OCT2-substrate exposure (sections 5.3, 7.1, 8.6, 12.3).
The label describes creatinine increases without measured glomerular-function change; such a signal is not automatically kidney injury.
Weight, appetite and gastrointestinal observations came from a combination-treatment population; sole-drug attribution is not justified.
**Decision gate:** demonstrate chaperone engagement, increased functional BUBR1 and improved segregation without a proliferative or toxicity artifact.

## Conditional candidate: niacin

**Proposed chain:** nicotinic acid -> target-cell NAD availability -> SIRT2 activity -> BUBR1 stabilization -> checkpoint improvement.
The niacin label describes metabolism to NAD, but not NAD or SIRT2 target engagement in MVA (`niacin_extended_release_label`, section 12.3).
Pirinen et al. administered niacin to adult-onset mitochondrial-myopathy patients and matched controls (`niacin_human_nad_myopathy_2020`).
The retrieved primary abstract reports increased blood NAD and patient muscle NAD reaching control levels: human pharmacodynamic evidence in another disease.
It does not establish NAD deficiency or muscle benefit in this hypothetical case, pediatric translation, BUBR1 correction or an appropriate MVA exposure.
The abstract also reports an anemia tendency in some patients; it is not evidence of pediatric or MVA safety.
Only the abstract and bibliographic metadata were verified via the Europe PMC API, not the full study methods or formulation equivalence.
The BUBR1 study linked SIRT2-mediated deacetylation at lysine 668 to protein stability (`sirt2_bubr1_nad_2014`).
Its pharmacological abundance experiment used NMN in mice, not niacin; its lifespan experiment used genetic SIRT2 overexpression.
Neither mouse lifespan findings nor increased protein abundance establish niacin-mediated checkpoint rescue or benefit in this setting.
Nicotinic acid, nicotinamide and NMN are distinct; nicotinamide used as a sirtuin inhibitor reduced BubR1 in the paper's cell experiments.
That observation is a specificity warning, not evidence that niacin itself worsens BUBR1 function.
The referenced prescription extended-release product has lipid indications; dietary supplements and release formulations are not interchangeable.
The label does not establish pediatric safety/effectiveness at age 16 years or younger and advises renal caution (sections 8.4-8.6).
Active liver disease and specified unexplained hepatic abnormalities are labeled contraindications; no such case finding is asserted.
Labeled statin-associated muscle toxicity warrants interaction review, but statin exposure is not assumed (section 5.2).
**Decision gate:** establish niacin-specific NAD/SIRT2 engagement and functional improvement rather than inferring equivalence to NMN.

## Held exploratory route: gentamicin

**Hypothetical chain, not supported drug rescue:** surviving premature-stop transcript -> readthrough -> correctly functioning full-length BUBR1.
No direct gentamicin/BUB1B or exact-allele readthrough evidence was retrieved for this curated set; no positive readthrough claim is encoded.
The retracted gentamicin B1 PNAS study is excluded; no other-team hackathon proposal is treated as evidence.
Stop-codon context, transcript abundance, NMD, inserted amino acid, protein identity and checkpoint function would each need verification.
An artificial reporter or intron-free construct can bypass endogenous RNA constraints and cannot by itself establish endogenous rescue.
The injection label supports antibacterial approval and warns of nephrotoxicity and potentially irreversible ototoxicity (`gentamicin_injection_label`).
**Manual research-triage hold:** weak mechanism bridge plus labeled toxicity; this is not a proven contraindication for an individual.
The hold is not evidence that the drug failed a rescue experiment, and it is not a suggestion to use it for MVA.

## Phenotype and safety constraint categories

| Context category | Role in research prioritization | Boundary or missing information |
| --- | --- | --- |
| Cancer history/predisposition | Separate checkpoint correction in nonmalignant cells from tumor survival and treatment-interaction questions. | No current oncology regimen, tumor response or candidate-specific cancer risk is established. |
| Renal calcification | Prioritize renal-exposure, nephrotoxicity and biomarker-interpretation review. | Calcification is not renal failure; current filtration measurements and electrolyte status are unavailable. |
| Growth/nutritional vulnerability | Include viability and growth-confounding controls; interpret weight/appetite/GI label concerns. | No body measurements or documented drug intolerance are invented. |
| Muscle phenotype | Distinguish baseline muscle dysfunction from toxicity or altered proliferation; review interacting medicines. | No statin exposure, muscle laboratory value or drug-induced myopathy is assumed. |
| Early developmental phenotype | Consider relevant nonmalignant lineages and developmental timing; separate reversible cell defects from established development. | No assumption that cellular correction reverses prior developmental effects. |
| Family reproductive loss | Retain as broad genetic-context information only. | No parental genotype, phase confirmation or segregation inference. |
| Pediatric context | Keep age-specific label boundaries visible; require independent exposure assessment. | Approval in another pediatric disease does not establish safe MVA exposure. |

These categories constrain interpretation, not efficacy scores; medication, renal, hepatic and hearing baselines remain incomplete.
Public-source retrieval used generic article/label URLs only; no coordinates, phenotype combinations, sample identifiers or read tables were transmitted.

## Proposed validation design: not completed work

1. Reverify reference transcript and annotations; establish phase with appropriate consented genetic evidence before assuming a biallelic mechanism.
2. Quantify allele-specific RNA, endogenous full-length/truncated BUBR1, turnover and kinetochore localization; test NMD only as a research question.
3. Compare appropriate nonmalignant models with matched corrected/wild-type, single-allele and phase-resolved paired-allele controls where feasible.
4. Include vehicle, baseline disease-model, genetic BUB1B correction and assay controls; do not substitute overexpression alone for endogenous correction.
5. For arimoclomol, assess the relevant heat-shock/chaperone response; for niacin, measure NAD-related target engagement and SIRT2 dependence.
6. Assess checkpoint response to spindle perturbation, mitotic timing, chromosome alignment, lagging chromosomes and micronuclei with orthogonal assays.
7. Couple those readouts to viability, proliferation, cell-cycle composition and longitudinal chromosome stability; exclude killing or selecting abnormal cells as apparent rescue.
8. Use biological replicates, blinded image scoring and predefined functional/viability criteria; report unsuccessful experiments and uncertainty.
9. Before translation, compare any active cellular exposure with independently established feasible exposure and safety constraints; no regimen is proposed here.

An increase in protein, longer mitosis, fewer surviving abnormal cells or a reporter signal alone is not sufficient functional rescue.
Nonmalignant checkpoint fidelity and tumor-cell fitness are separate endpoints; rescue in cancer-derived assay lines is not proof of normal-tissue benefit.
Conversely, a hypothesis about tumor protection is not established harm: tumor-context and oncology-interaction studies would be separate requirements.
All candidates remain hypotheses unless target engagement, relevant function, exposure and safety are independently substantiated.

## Bibliography and provenance

- `bubr1_mva_mechanisms_2010`: Suijkerbuijk et al., Cancer Research (2010), [Molecular Causes for BUBR1 Dysfunction in the Human Cancer Predisposition Syndrome Mosaic Variegated Aneuploidy](https://pmc.ncbi.nlm.nih.gov/articles/PMC2887387/). DOI: 10.1158/0008-5472.CAN-09-4319.
- `sirt2_bubr1_nad_2014`: North et al., The EMBO Journal (2014), [SIRT2 induces the checkpoint kinase BubR1 to increase lifespan](https://pmc.ncbi.nlm.nih.gov/articles/PMC4194088/). DOI: 10.15252/embj.201386907.
- `hsp_sphingolipidoses_2016`: Kirkegaard et al., Science Translational Medicine (2016), [Heat Shock Protein-based therapy as a potential candidate for treating sphingolipidoses](https://pmc.ncbi.nlm.nih.gov/articles/PMC6821533/). DOI: 10.1126/scitranslmed.aad9823; PMC availability in 2019 is not the publication year.
- `niacin_human_nad_myopathy_2020`: Pirinen et al., Cell Metabolism (2020), [Niacin Cures Systemic NAD+ Deficiency and Improves Muscle Performance in Adult-Onset Mitochondrial Myopathy](https://europepmc.org/article/MED/32386566). DOI: [10.1016/j.cmet.2020.04.008](https://doi.org/10.1016/j.cmet.2020.04.008); PMID 32386566. The title is bibliographic, not an MVA efficacy claim.
- `arimoclomol_miplyffa_label`: [MIPLYFFA US prescribing information](https://dailymed.nlm.nih.gov/dailymed/fda/fdaDrugXsl.cfm?setid=5feffc0e-453d-47fa-91dd-38d4952309bc); canonical label set ID: 5feffc0e-453d-47fa-91dd-38d4952309bc.
- `niacin_extended_release_label`: [Niacin extended-release US prescribing information](https://dailymed.nlm.nih.gov/dailymed/fda/fdaDrugXsl.cfm?setid=dd60fe81-3d54-4a29-9502-601be89c575e); canonical label set ID: dd60fe81-3d54-4a29-9502-601be89c575e.
- `gentamicin_injection_label`: [Gentamicin Injection, USP US prescribing information](https://dailymed.nlm.nih.gov/dailymed/fda/fdaDrugXsl.cfm?setid=84f5c763-1cd3-4d85-9afb-934db8666fbf); canonical label set ID: 84f5c763-1cd3-4d85-9afb-934db8666fbf.

DOIs identify underlying primary studies; label set IDs identify regulatory documents, not independent experimental replications.
URLs and access date document retrieval, not a frozen label version; labels and publication status should be rechecked before further decisions.
