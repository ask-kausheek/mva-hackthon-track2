# Team Soul — Track 2 Submission Report

## Allele-aware, evidence-gated hypotheses for residual BUBR1 stabilization

**Team:** Soul  
**Track:** 2 — approved-drug repurposing  
**Evidence access date:** 5 September 2026  
**Outcome:** two tied conditional research hypotheses; one held exploratory route.

This computational/evidence hypothesis proposal is not experimental validation, diagnosis, or treatment advice. No experimental work or clinician review is claimed.

## 1. Method abstract

We developed an offline, allele-aware evidence-engineering prototype for approved-drug repurposing in suspected BUB1B-related mosaic variegated aneuploidy (MVA). Seven public sources support 20 manually curated claims concerning three candidates: arimoclomol, prescription nicotinic acid (niacin), and a held gentamicin readthrough route. The proposed direction is stabilization of residual functional BUBR1, not inhibition of an already compromised checkpoint.

Structured records distinguish gene-mechanism evidence, drug-tested translation, functional rescue, regulatory eligibility, and safety context. Required mechanism groups prevent a candidate from retaining support after an indispensable pathway study is removed. A weakest-link bridge combines mechanism and drug-translation support approval and safety gates precede ranking. Scope discounts, preserved ties, three weight profiles, and leave-one-primary-study-out analyses expose assumptions and evidence dependence.

Both conditional candidates receive baseline index 10, with no qualifying drug-mediated BUBR1 functional-rescue evidence. Gentamicin remains held. These indices are human-designed research heuristics, not calibrated efficacy estimates, success probabilities, or judging-rubric scores. Strengths are auditable provenance, explicit mechanistic direction, reproducible computation, and visible abstention. Limitations include non-exhaustive selection, uncertain allelic phase and function, indirect disease-model extrapolation, abstract-only access to one primary study, and unresolved formulation, exposure, renal, and oncology constraints. Neither exact case allele was experimentally tested in the retrieved publications. The output prioritizes falsifiable questions rather than selecting a drug winner.

## 2. Genetic starting point and mechanism

Prior controlled-case analysis identified a putative heterozygous pair, **BUB1B p.Leu737Ter and p.Asn1002Lys**. Transcript-specific labels have not been reverified. Phase is unknown; two heterozygous findings do not establish variants in trans, compound heterozygosity, or a recessive diagnosis. Parents' genomes and live Track 1 confirmation are unavailable.

**Use of organizer data:** the earlier Track 1 analysis used the VCF for variant retrieval, annotation, genotype/QC assessment and ranking; clinical HPO terms informed gene ranking, and FASTQ analysis provided read support for shortlisted alleles. These findings were manually carried into this proposal. The Track 2 program does not ingest the VCF, reprocess FASTQs, or infer a drug directly from the genome. It processes curated public evidence. Clinical and family-history context informs written constraints and manual review, not an automatically computed phenotype-to-drug score.

BUB1B encodes BUBR1, involved in spindle-checkpoint signaling and chromosome segregation. In other MVA-associated mutants, reduced abundance and increased turnover provided a rationale for investigating protein stabilization. Forced expression of I909T and L1012P to wild-type-like abundance restored a nocodazole checkpoint response in engineered cells; this was **genetic overexpression, not drug rescue**. Stable Y155C retained chromosome-alignment activity but not checkpoint activity, demonstrating that more protein need not mean restored function. [R1]

The case hypothesis therefore requires residual, recoverable, functional protein. A premature-stop label alone establishes neither nonsense-mediated decay (NMD) nor a surviving transcript or useful truncated protein. Findings for other truncations do not establish p.Leu737Ter's fate. Retaining sequence around a regulatory site does not establish folding, partner binding, or correction. [R1,R2]

**Directionality:** test restoration of normal-cell checkpoint fidelity, not inhibition of the failing checkpoint. Stabilization cannot replace missing sequence and could preserve defective protein. Normal-cell rescue must be distinguished from support of tumor-cell survival; neither benefit nor tumor protection is established here.

Case-context constraints are cancer history/predisposition, renal calcification, growth/muscle vulnerability, developmental/perinatal features, and reproductive family context. Calcification is not renal failure. Family reproductive loss does not establish causal miscarriage inheritance or segregation. Current filtration, hepatic status, hearing baseline, and oncology/other medication exposures remain unresolved. Cellular correction would not necessarily reverse established developmental effects.

## 3. Proposed candidates and existing approvals

The cited US prescribing information confirms existing approved products and indications—not MVA approval. This is not a fresh, comprehensive live regulatory-database check.

| Candidate | Existing approved indication/formulation | Research disposition |
|---|---|---|
| Arimoclomol | MIPLYFFA capsules, with miglustat, for neurological manifestations of Niemann-Pick disease type C (NPC), adults and children aged 2 years and older. [R5] | Conditional stabilization hypothesis |
| Niacin | Prescription nicotinic-acid extended-release tablets for labeled lipid disorders, including primary hyperlipidemia and mixed dyslipidemia. [R6] | Conditional NAD/SIRT2 hypothesis |
| Gentamicin | Injectable antibacterial for serious infections caused by susceptible bacteria. [R7] | Held exploratory readthrough route |

### Arimoclomol: chaperone support, with an untested bridge

**Proposed chain:** heat-shock co-induction → appropriate chaperone engagement → stabilization of functional BUBR1 → improved checkpoint fidelity.

The BUBR1 study inhibited HSP90 with geldanamycin and observed reduced I909T/L1012P abundance. Dependency under inhibition does not demonstrate rescue by chaperone induction. [R1] A separate sphingolipidosis study examined recombinant HSP70 broadly and arimoclomol in NPC models. Arimoclomol reduced lysosomal storage/cholesterol accumulation in NPC fibroblasts and increased brain HSF1 activation and HSP70 in NPC-model mice. These are drug-tested, other-disease observations, not HSP90-dependent BUBR1-mutant rescue. HSP70 and HSP90 are not interchangeable. [R3]

MIPLYFFA's label states that its clinical mechanism in NPC is unknown. Its approved combination does not validate this proposed mechanism; miglustat is not a candidate here, and no combination regimen is transferred. Renal impairment changes exposure. OCT2 inhibition can affect other substrates and raise creatinine without measured glomerular-function change; that signal is not automatically kidney injury. Weight, appetite, and gastrointestinal observations in a concomitant-miglustat population cannot be attributed solely to arimoclomol. [R5]

**Falsifier:** relevant chaperone engagement without improved endogenous BUBR1 function rejects the proposed rescue bridge.

### Niacin: NAD availability is not demonstrated checkpoint rescue

**Proposed chain:** nicotinic acid → target-cell NAD availability → SIRT2 activity → functional BUBR1 stabilization → checkpoint improvement.

The prescription label describes metabolism contributing to NAD, not MVA target engagement. [R6] Pirinen and colleagues reported increased blood NAD after niacin in adult-onset mitochondrial-myopathy patients and matched controls, with patient muscle NAD reaching control levels. Only the primary abstract and bibliographic metadata were verified through Europe PMC; full methods and formulation equivalence were not verified. The abstract also reports an anemia tendency in some patients. These observations establish neither NAD deficiency nor muscle benefit, pediatric safety, or BUBR1 correction in this case. [R4]

North and colleagues linked SIRT2-dependent deacetylation at BubR1 lysine 668 to stability. Their pharmacological abundance experiment used **NMN**, whereas the lifespan experiment used **genetic SIRT2 overexpression** in mice—not niacin treatment. Neither increased protein nor mouse lifespan establishes drug-mediated checkpoint rescue. Nicotinic acid, nicotinamide, and NMN are distinct; nicotinamide's inhibitory cell-experiment effects cannot be assigned to niacin. [R2]

The referenced extended-release product is not interchangeable with supplements or other release formulations. Its label does not establish safety/effectiveness at age 16 years or younger, advises renal caution, and identifies hepatic contraindications and statin-associated muscle toxicity. These are review constraints, not asserted case findings or assumed statin exposure. [R6] Suitable exposure and equivalence to the studied niacin preparation remain unknown.

**Falsifier:** niacin-associated NAD elevation without SIRT2-dependent functional improvement rejects the complete proposed chain.

### Gentamicin: explicitly held, not a third recommendation

Readthrough would require surviving endogenous premature-stop RNA, appropriate stop context, a correctly identified full-length product, and functional checkpoint restoration. Other BUBR1 truncation findings motivate RNA assessment but do not establish this allele's transcript availability. [R1] No direct gentamicin/BUB1B or exact-allele readthrough support was retrieved in this curated corpus. A retracted gentamicin B1 study was excluded; other-team proposals are not evidence.

The injection label warns of nephrotoxicity and potentially irreversible auditory/vestibular toxicity. [R7] These hazards plus the unsupported bridge justify a **manual research-triage hold**, not a proven individual contraindication or a failed rescue experiment. Reporter-only or intron-free-construct results would not resolve endogenous NMD and functional-product uncertainties.

## 4. Detailed method, resources, and human decisions

**Inputs and inclusion:** Three public-evidence JSON files contain source provenance, drug records, and claim records. The seven sources comprise four primary articles and three regulatory labels: PMC full-text resources, Europe PMC abstract/metadata, and DailyMed prescribing information. [R1–R7] Manual, AI-assisted curation selected relevant mechanism, drug-tested pharmacodynamic, approval, and safety claims; it did not systematically screen all approved medicines or negative literature.

Claims identify source, underlying study, candidates, dimension, direction, and scope. Drug mapping means hypothesis relevance not drug administration. Context and missing evidence are not demonstrated harm. Shared article claims are not independent replications.

**Automation:** local Python code validates schemas/references, applies gates, calculates indices, preserves ties, generates claim audits/reports, performs sensitivity analysis, and fingerprints inputs/configuration/code. No trained machine-learning model, LLM inference, network request, or genome-scale reanalysis occurs in the delivered ranker. Scientific inclusion, scope labels, required mechanism groups, safety holds, and candidate selection remain human judgments assisted by AI; schema validity cannot guarantee scientific validity.

For each required mechanism group, the strongest qualifying primary claim supplies its support; the weakest required group determines **M**. Strongest qualifying drug-translation and functional-rescue claims determine **T** and **F**. The bridge is **B = min(M,T)**; baseline index is **100 × (0.5B + 0.5F)**.

Scope weights are exact variant 1.0, same gene/other variant 0.6, same gene/nonvariant 0.4, other disease 0.2, and general 0.1. Reviews and labels contribute no numeric support; labels establish approval eligibility. Repetition adds no points. Functional rescue requires drug-treated BUBR1-related functional evidence, not abundance, overexpression, or unrelated disease improvement.

Ordered disposition gates address approval, incompatible variant/exposure evidence, manual safety holds, conflicting evidence, and absent complete bridges/rescue before assigning conditional ranks. Unknown fit, exposure, and safety never become “safe.” These human-chosen weights are neither efficacy-calibrated nor judging-rubric weights.

## 5. Computational results and sensitivity

| Candidate | Mechanism M | Translation T | Bridge B | Functional rescue F | Index | Rank |
|---|---:|---:|---:|---:|---:|---|
| Arimoclomol | 0.6 | 0.2 | 0.2 | 0.0 | 10.0 | 1, tied |
| Niacin | 0.4 | 0.2 | 0.2 | 0.0 | 10.0 | 1, tied |
| Gentamicin | 0.0 | 0.0 | 0.0 | 0.0 | Unassigned | Held |

Niacin's required SIRT2–BUBR1 group limits mechanism support to **0.4, not 0.6**. Arimoclomol has two supporting primary studies and niacin three, but neither count represents independent rescue replications. No qualifying functional-rescue evidence exists for either candidate; zero denotes an evidence gap, not measured inefficacy.

Three bridge/rescue profiles—50/50, 80/20, and 20/80—were crossed with the intact corpus and four single-primary-study exclusions: **15 scenarios per drug, 45 rows**.

| Candidate | Conditional / all scenarios | Top-ranked, including ties / all scenarios | Conditional / study-exclusion scenarios | Other outcomes |
|---|---:|---:|---:|---|
| Arimoclomol | 9/15 | 9/15 | 6/12 | Deferred 6/15 |
| Niacin | 6/15 | 6/15 | 3/12 | Deferred 9/15 |
| Gentamicin | 0/15 | 0/15 | 0/12 | Held 15/15 |

Without study removal, both remain tied in all three profiles, at indices 10, 16, and 4 respectively. Removing the shared MVA study defers both. Removing the NPC study defers arimoclomol; removing either the NAD/SIRT2 study or adult niacin study defers niacin. There are three tied-top scenarios, nine sole-top scenarios, and three with no conditional candidate. Counts include ties and are **not success probabilities**; arimoclomol's higher survival count does not establish superiority.

**Input/code snapshot:** `c057862d598f59dcc6d2223c88a79cd46c7f532e3bd68e625aefab961ad6ed77`. Reproducible outputs comprise the ranking, claim audit, sensitivity table, generated research report, and SHA-256 manifest. CSVs are supporting audit artifacts; Track 2 does not require a CSV upload.

## 6. Falsifiable next validation—not completed work

1. **Establish the mechanism:** reverify transcript annotations and consented phase evidence; quantify allele-specific RNA, endogenous full-length/truncated BUBR1, turnover, and kinetochore localization. Investigate NMD rather than assume it.
2. **Use discriminating controls:** nonmalignant disease-relevant cells, matched corrected/wild-type controls, single-allele and phase-resolved paired-allele models where feasible; vehicle, untreated disease-model, genetic-correction, and assay controls. Overexpression alone is not endogenous correction.
3. **Test target engagement:** measure relevant heat-shock/chaperone effects for arimoclomol and niacin-specific NAD changes plus SIRT2 dependence. Antibody-based abundance/localization measurements do not establish functional rescue.
4. **Require orthogonal function:** spindle-perturbation checkpoint response, mitotic timing, chromosome alignment, lagging chromosomes, micronuclei, and longitudinal chromosome stability. Pair these with viability, proliferation, and cell-cycle composition to exclude apparent rescue caused by killing or selecting abnormal cells.
5. **Predefine rejection criteria:** biological replicates, blinded scoring, and predefined functional/viability thresholds. Increased protein, prolonged mitosis, or reporter signal alone is insufficient. Report unsuccessful experiments.
6. **Assess translation separately:** independently establish formulation-relevant feasible exposure, renal/hepatic constraints, and medication interactions. Separate normal-cell correction from tumor-cell fitness and oncology-interaction testing; neither substitutes for the other.

No doses or clinical regimens are proposed. Qualified genetics, pharmacology, renal, and oncology review is recommended before further translation; this recommendation is not presented as an official eligibility requirement.

## 7. AI disclosure, data handling, practicality, and novelty

**Provider/model/plan:** GitHub Copilot , powered by GPT models and by Claude free tier. In  session that added the prompt pack, its checker and tests, assisted with code, literature retrieval, evidence structuring, drafting, and tests. There is no training on customer content, assumed unchanged across sessions.

 The three public-evidence JSON files. Public literature queries concerned gene/drug mechanisms and regulatory sources, not patient identifiers or genotype-scale data. No additional proprietary databases were used. The delivered evidence package contains no raw genomic files, genotype-scale tables, clinical source documents, credentials, or conversation logs. No-training and time/purpose-limited retention terms.

**Runtime/cost:** the standard-library Python ranker needs an ordinary local computer, no GPU, API key, or paid external inference. A seconds-scale run and negligible marginal local compute expense are **unbenchmarked estimates**, not measured runtime or cost. Subscription access, hardware, curation, and expert review remain additional costs; no zero-total-cost claim is made.

**Reusable prompt pack:** `prompts/` in the repository holds four slot-based prompts (mechanism characterization, veto-coded candidate longlist, claim curation, false-rescue falsifier), a shared veto registry and golden examples, so the same workflow can be pointed at another gene or disease by changing the slots. `python -m mva_track2.promptcheck` machine-validates any model's reply against the engine's own schemas: it rejects fabricated source or drug IDs, ungrounded FACT labels, advancing a vetoed candidate, non-numeric go/no-go thresholds and malformed claim rows, and flags overclaiming wording. The model proposes and argues; the deterministic engine alone assigns weight. What is verified is the checker and the golden examples (`tests/test_promptcheck.py`); **no cross-model benchmark of the prompts has been run**, so their pass rate on any given model is unknown.

**Pitch video:** The three-minute video presents the same  slides and reads `config/pitch.json` verbatim. Its narration is a **synthetic text-to-speech voice** (a Windows desktop voice), and its slides are rendered from the same pitch text; the video build tooling is local and is not part of this repository.

**Novelty and scalability:** the modest contribution is an auditable combination of required mechanism links, weakest-link scoring, explicit holds, and preserved ties—not a new biological discovery. Computation scales more readily than scientific judgment. Other cases require new allele characterization, mechanism/gate curation, candidate retrieval, and safety/exposure assessment; reuse is not effortless automated discovery.

## 8. Public bibliography

**[R1]** Suijkerbuijk et al. *Molecular Causes for BUBR1 Dysfunction in the Human Cancer Predisposition Syndrome Mosaic Variegated Aneuploidy.* Cancer Research (2010). Relevant experiments: Figs. 2–5. DOI: 10.1158/0008-5472.CAN-09-4319.  
https://pmc.ncbi.nlm.nih.gov/articles/PMC2887387/

**[R2]** North et al. *SIRT2 induces the checkpoint kinase BubR1 to increase lifespan.* The EMBO Journal (2014). DOI: 10.15252/embj.201386907.  
https://pmc.ncbi.nlm.nih.gov/articles/PMC4194088/

**[R3]** Kirkegaard et al. *Heat Shock Protein-based therapy as a potential candidate for treating sphingolipidoses.* Science Translational Medicine (2016); arimoclomol experiments: Fig. 6. DOI: 10.1126/scitranslmed.aad9823.  
https://pmc.ncbi.nlm.nih.gov/articles/PMC6821533/

**[R4]** Pirinen et al. *Niacin Cures Systemic NAD+ Deficiency and Improves Muscle Performance in Adult-Onset Mitochondrial Myopathy.* Cell Metabolism (2020). DOI: 10.1016/j.cmet.2020.04.008; PMID 32386566. Abstract/metadata only; title is not an MVA efficacy claim.  
https://europepmc.org/article/MED/32386566

**[R5]** *MIPLYFFA (arimoclomol) capsules: US prescribing information.* DailyMed; sections 1, 5.3, 6.1, 7.1, 8.6, 12.1, 12.3.  
https://dailymed.nlm.nih.gov/dailymed/fda/fdaDrugXsl.cfm?setid=5feffc0e-453d-47fa-91dd-38d4952309bc

**[R6]** *Niacin extended-release tablets: US prescribing information.* DailyMed; sections 1, 4, 5.2, 8.4–8.7, 11, 12.3.  
https://dailymed.nlm.nih.gov/dailymed/fda/fdaDrugXsl.cfm?setid=dd60fe81-3d54-4a29-9502-601be89c575e

**[R7]** *Gentamicin Injection, USP: US prescribing information.* DailyMed; indications and boxed warning.  
https://dailymed.nlm.nih.gov/dailymed/fda/fdaDrugXsl.cfm?setid=84f5c763-1cd3-4d85-9afb-934db8666fbf

## 9. Hackathon acknowledgement

> This work was made possible through the Hackathon, organized by Sage
> Bionetworks in partnership with the MVA Society, Hugging Face, and BEACON
> (The Benchmarking, Evaluation, and Assessment Consortium for Science), with
> prize sponsorship from AWS and Anthropic. We are deeply grateful to the child
> and their family who generously contributed their data and their story to
> advance research into this rare disease. We acknowledge their trust in making
> this Hackathon possible.
