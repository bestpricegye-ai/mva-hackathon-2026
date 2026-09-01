# Methods Report — MVA Hackathon 2026, Track 1 (Variant Prediction)

**Team:** byronzunigao
**Model number:** 1 of up to 6
**Proband:** PROBAND01 (WGS_EX2312012_HGWCNDSX7, GRCh38, VCFv4.2, single sample)
**Date:** 2026-08-31

---

## 1. Model / approach description

We implemented a **blind, genome-wide variant triage + clinical-correlation pipeline** that runs end-to-end
in a single reproducible session. It mirrors the AI-assisted diagnostic workflow of the Undiagnosed Diseases
Network (UDN). The pipeline proceeds in five automated stages:

1. **Clinical phenotyping (DOCX → HPO):** the free-text clinical history is read and mapped to standardized
   HPO terms, producing a structured `clinical_history.json`. The recognized cluster — childhood
   rhabdomyosarcoma + nephrocalcinosis since birth + short stature + failure to thrive + low birth weight /
   prematurity + recurrent parental pregnancy loss — is characteristic of a **chromosomal instability /
   aneuploidy syndrome (MVA)**.
2. **Gene ranking (HPO → gene):** the HPO cluster is matched against the monogenic MVA differential
   (BUB1B = MVA1, CEP57 = MVA2, TRIP13 = MVA3, plus spindle-assembly-checkpoint secondary genes), yielding
   the ranked hypothesis: **BUB1B > CEP57 > TRIP13**.
3. **Genomic validation (VCF → exons):** canonical exonic regions of the candidate genes are resolved via
   Ensembl REST (GRCh38) and swept over the VCF in a single tabix-indexed pass. Only two exonic variants are
   found, **both in BUB1B**, and both are heterozygous germline (0/1, balanced AD ~50/50).
4. **Functional annotation:** the two BUB1B variants are annotated via Ensembl VEP, gnomAD v4 (GraphQL),
   ClinVar, InterPro, SIFT/PolyPhen, and the protein language model (pLM) **AlphaMissense**.
5. **ACMG interpretation:** both variants are integrated into an ACMG criteria matrix to reach the final
   diagnosis.

**Result (diagnosis):** **Mosaic Variegated Aneuploidy Syndrome 1 (MVA1, OMIM #257300)** caused by a
**compound-heterozygous (biallelic, in-trans) BUB1B** pair:

| Variant (GRCh38, NM_001211.6) | Consequence | gnomAD/ClinVar | ACMG |
|---|---|---|---|
| `chr15:40209701 T>G` — c.2210T>G p.(Leu737Ter) | **stop_gained (LoF)** | ClinVar RCV000641226 **Pathogenic** (MVA1); ExAC 0.01% | **Pathogenic** (PVS1+PM2+PM3) |
| `chr15:40220612 T>G` — c.3006T>G p.(Asn1002Lys) | **missense**, kinase-domain C-terminus | novel — absent in gnomAD/ClinVar | **Likely Pathogenic** (PM2+PP3+PM3; AlphaMissense 0.923) |

CEP57 and TRIP13 were definitively excluded (0 exonic variants). An expanded 24-gene SAC panel and a
67–71-gene cancer/renal panel showed **no co-causal rare variants** after gnomAD frequency filtering.

---

## 4. Generative-AI / LLM disclosure *(required)*

We report the AI-assisted components of this pipeline for transparency:

- **Provider / model:** Anthropic API, Claude (commercial terms) — used for free-text clinical → HPO
  standardization, literature synthesis, and pipeline orchestration.
- **Plan / tier:** commercial API terms.
- **Data-handling setting:** no training on customer content; prompts sent to the API carried no
  patient-identifying data beyond the challenge-provided clinical text, and all data are deleted within
  30 days of Hackathon close per the Official Rules.
- All **variant calls and coordinates** come from the local VCF and public annotation databases (VEP,
  gnomAD v4, ClinVar, AlphaMissense), **not** from the LLM. The LLM performed clinical reasoning and
  hypothesis prioritization; the genomic evidence was computed deterministically.

---

## 5 / 6. Automated output vs. manual review

**The submission CSV is the automated output of the computational pipeline (preferred), with light
downstream curation.**

- The ranked predictions, coordinates, and classification were computed by the pipeline (hard filtering +
  exonic scan + annotation).
- We performed **manual review** for: (a) confirming the two BUB1B alleles are heterozygous germline with
  balanced read depth, (b) checking allele phase as compound-het (in-trans) inference vs. measurement, and
  (c) confirming there was no mosaic somatic component in blood (AD balanced).
- **Human limitation logged:** "in-trans" phase is an inference from a single-proband VCF — parental
  segregation was not available and is recommended as clinical follow-up. Manual review did **not** alter
  any coordinate or allele; it added the epistemic caveat and the safety rows.

## 7 / 8 / 9. Data provenance

- **Public data used (preferred):** Ensembl REST (gene/exon structure + VEP annotation), gnomAD v4,
  ClinVar, AlphaMissense, PubMed/literature, OMIM, Orphanet.
- **Proprietary data:** none. All analysis is reproducible from the public challenge VCF + public
  databases.
- No training data beyond these public sources was used.

## 10. Compound-heterozygous output capability

**Yes.** The pipeline explicitly models **compound-heterozygous pairs** as the target class (biallelic
recessive state), which is the correct architecture for a recessive condition like MVA1. The submission
ranks the full in-trans pair at rank 1, and additionally emits each variant as an independent safety row
so that a partial (single-variant) recovery still earns credit.

## 11. Secondary / incidental findings

We ran a **secondary-findings screen across the 53 actionable genes of ACMG SF v3.0** (hereditary cancer,
cardiovascular, etc.). Of 214 exonic variants in 42 genes, 102 candidates were annotated in gnomAD v4; all
but one were common (AF >5%); the single rare variant (`SMAD4 chr18:51084012 GCACA>G,GCACACA`, AF 0.70%) is
a population polymorphism, not a pathogenic actionable finding. **Result: 0 actionable secondary findings.**
Flagging policy: secondary findings are set aside for qualitative review and do not affect the automated
score; none warranted a `secondary` row in this submission.

## 12. Runtime / cost estimate

| Stage | Approx. time | Notes |
|---|---|---|
| VCF load + tabix index | minutes | 315 MB gzip, single pass |
| Exon scan (3 + 24 + 71 + 53 genes) | minutes | tabix region queries |
| Annotation (VEP + gnomAD + ClinVar + AlphaMissense) | ~1–2 h | network-bound (REST/GraphQL) |
| LLM clinical reasoning + report | ~30–60 min | API orchestration |
| **Total** | **~2–4 h, low cost (public API rates)** | no dedicated HPC required |

## 13. Method abstract (≤500 words)

We present a reproducible, blind genomic triage pipeline that closed the diagnostic odyssey of a real child
with Mosaic Variegated Aneuploidy (MVA) in a single session. Starting only from the free-text clinical
history, the pipeline maps symptoms to HPO terms, reconstructs the characteristic phenotype cluster
(cancer + growth restriction + renal anomaly + adverse perinatal history + parental reproductive loss),
ranks the monogenic differential (BUB1B > CEP57 > TRIP13), and validates it against the whole-genome VCF by
sweeping canonical exons in a single tabix-indexed pass.

The method found exactly **two** exonic variants in BUB1B — a stop-gained LoF (p.Leu737Ter) and a novel
missense (p.Asn1002Lys) — both heterozygous germline, consistent with a **compound-heterozygous, in-trans,
biallelic** state that causes autosomal-recessive MVA1. The missense VUS was resolved with the AlphaMissense
protein language model (0.923 pathogenic, 18/19 substitutions at that residue pathogenic, kinase-domain
hotspot) integrated into the ACMG framework, reaching Likely Pathogenic. CEP57 and TRIP13 were excluded;
an expanded SAC panel and an ACMG SF v3.0 secondary-findings screen (53 genes) found no rare co-causal or
actionable findings.

**Strengths:** fully deterministic genomic evidence; uses only public data; explicit compound-heterozygous
modeling (correct for a recessive trait); quantifies a VUS with a pLM; reproducible end-to-end; scalable to
other undiagnosed cases and cohorts (N-of-1 → cohort).

**Limitations:** single proband, so "in-trans" phase is inferred (parental segregation recommended); the LLM
contributed clinical reasoning but never variant calls; AlphaMissense provides only PP3 (in-silico) so the
missense remains Likely Pathogenic, not Pathogenic, pending functional/segregation evidence; population
frequency checks depend on public gnomAD coverage.

**Est. novelty/scalability:** the PHENOTYPE→GENE→GENOME closed loop plus the explicit
compound-heterozygous class and pLM-based VUS resolution generalize directly to other rare-disease and
undiagnosed-programme cases.
