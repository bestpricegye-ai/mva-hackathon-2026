# Video pitch — Track 2 (MVA Hackathon 2026) | byronzunigao

English script (3:00), **scientific/paper-grade level**, with primary citations and the provenance of
each data point. The reconstructed narration is the sole source of the video; render via
`src/hacer_video.py` and `pitch_byronzunigao.mp4`.

> This is the English version to be submitted. Content, conclusions, ranking and citations are
> identical to the Spanish original.

---

## Scene 1 — Case: MVA1 (OMIM #257300) — real WGS on GRCh38

**Narration:**
> Hello, I am Byron Zúñiga, from team byronzunigao. We present a real case of mosaic variegated
> aneuploidy, MVA type 1, OMIM 257300, an ultra-rare disease. The analytical input is a whole-exome
> in GRCh38 and the proband's clinical phenotype. Cells gain and lose chromosomes because of a
> defective mitotic checkpoint, and the patient developed rhabdomyosarcoma. Malumbres, in Nature
> Reviews Genetics, confirms that no approved treatment exists today. We propose a mechanism-first
> repurposing anchored to the causal protein.

**Bullets:**
- PROBAND01 — WGS GRCh38 + clinical HPO (8 traits)
- CIN: mosaic variegated aneuploidy
- Childhood rhabdomyosarcoma
- No approved treatment (Malumbres 2024)

**Footer:** Source: VCF `WGS_EX2312012` + `clinical_history.json` — OMIM #257300 — Orphanet #1052

**Evidence provenance:**
| Data point | Where obtained |
|---|---|
| Genotype/GRCh38 | `data/results/vcf_exonic_variants.txt` (provided VCF, FILTER=PASS) |
| HPO phenotype (8 traits) | `data/results/clinical_history.json` (challenge clinical text) |
| No approved treatment | Malumbres & Villarroya-Beltri, **Nat Rev Genet 2024;25:864** (PMID 39169218) |

---

## Scene 2 — Molecular diagnosis: compound-heterozygous BUB1B

**Narration:**
> The diagnosis is anchored to the genotype. The proband is compound heterozygous in BUB1B:
> p.Leu737Ter, a stop-gain that truncates the protein, PVS1 criterion; and p.Asn1002Lys, a novel
> missense in the kinase domain, with an AlphaMissense score of 0.923. Hanks, in Nature Genetics in
> 2004, established that biallelic BUB1B mutations predispose to aneuploidy and cancer. The result is
> haploinsufficient BUBR1: a weakened spindle assembly checkpoint. The defect is a loss of function,
> and what the biology demands is more functional BUBR1.

**Bullets:**
- p.Leu737Ter — stop-gain, PVS1 (truncates BUBR1)
- p.Asn1002Lys — novel, kinase domain — AlphaMissense 0.923
- Haploinsufficient BUBR1 — weak SAC
- Hanks 2004 (Nat Genet): biallelic BUB1B — MVA1

**Footer:** GRCh38: chr15:40209701 T>G + chr15:40220612 T>G — PASS QUAL 708.77 — gnomAD 3.29e-5 / novel

**Evidence:**
| Data point | Evidence / provenance |
|---|---|
| Coordinates, QUAL, AD (VAF 0.54/0.46) | `vcf_exonic_variants.txt` + `verificacion_dirigida_vcf.py` (chr15:40.19–40.23) |
| p.Leu737Ter Pathogenic | ClinVar **RCV000641226**; VCF genotype |
| 1000G/gnomAD AF | gnomAD v2.1.1 — `fase2_gnomad_completo.json` |
| Biallelic BUB1B — MVA1 | Hanks et al., **Nat Genet 2004;36:1159** (PMID 15475955) |
| AlphaMissense 0.923 | Cheng et al., **Nature 2023;625:321** |

---

## Scene 3 — Restoring BUBR1: the SIRT2/NAD+ axis

**Narration:**
> The literature provides a target with in vivo data. Baker, in Nature Cell Biology in 2013, showed
> that raising BUBR1 protects against aneuploidy, against cancer, and extends healthy lifespan in
> hypomorphic mice. North, in EMBO Journal in 2014, defined the mechanism: deacetylation of lysine
> 668 of BUBR1, mediated by SIRT2, a NAD+-dependent deacetylase. Its precursor, NMN, raises NAD and,
> through SIRT2, increases BUBR1. This is the only published strategy that directly raises the
> affected protein.

**Bullets:**
- ↑BUBR1 protects against aneuploidy/cancer — Baker, NCB 2013
- BUBR1 is deacetylated at K668 by SIRT2 (in vivo) — North, EMBO J 2014
- SIRT2 = NAD+-dependent deacetylase
- NMN — NAD+ — SIRT2 — stabilizes BUBR1

**Footer:** Progeroid mouse BubR1^H/H — ↑BUBR1 = only published route that raises the causal protein

**Evidence:**
| Data point | Evidence / provenance |
|---|---|
| ↑BUBR1 — less aneuploidy/cancer, longer healthy life | Baker et al., **Nat Cell Biol 2013;15:96** (ncb2643) |
| Hypomorphic BUBR1 — progeria + aneuploidy | Baker et al., **Nat Genet 2004;36:744** |
| SIRT2 deacetylates/stabilizes BUBR1 (NAD+ dep.) | North et al., **EMBO J 2014;33:1438** (PMC4194088) |
| NMN NAD+ precursor, pharmacological target | Blanco `fase4_mapeo_blancos.json` (ChEMBL/Open Targets) |

---

## Scene 4 — Safety: explicit safeguard + secondary candidates

**Narration:**
> We enclose the hypothesis within a safety safeguard: any drug that further weakens the mitotic
> checkpoint is contraindicated: taxanes, vincristine, MPS1 or TTK inhibitors. We validated this
> negative result in ChEMBL, Open Targets and PubMed. Secondary candidates address the consequences:
> senolytics, such as dasatinib plus quercetin, clear inflammatory senescence, only under oncology
> because of the sarcoma; and growth hormone, of limited response in MVA, is individualized.

**Bullets:**
- Contraindicated: taxanes — vincristine — MPS1/TTK (weaken the SAC)
- Validated: ChEMBL + Open Targets + PubMed
- Senolytics (dasatinib+quercetin) — oncology only
- GH — individualized (limited response in MVA)

**Footer:** Clinically actionable negative result (guardrail) — Liu & Suson 2020

**Evidence:**
| Data point | Evidence / provenance |
|---|---|
| Anti-mitotic contraindication | ChEMBL/Open Targets/PubMed (MPS1/TTK targets) — `fase4_validacion_farmacos.json` |
| Chemo/radio risk in MVA | Liu & Suson 2020 (PMC7658145) |
| Senescence in BUBR1 insufficiency | Malumbres & Villarroya-Beltri 2024 (PMID 39169218) |
| GH of limited response | Pellicer Viudes et al. 2026 (PMID 41700350) |

---

## Scene 5 — Integrated plan and scalable framework

**Narration:**
> The management was audited by a medical panel. Oncology surveillance every three months until age
> seven, according to Orphanet and SIOP-Europe 2021; serial blood counts for myelodysplasia, as
> documented by Laberko; the standard rhabdomyosarcoma regimen; a monitored experimental rescue with
> NMN and NAD; senolytics under oncology; and parental genotyping to close the in-trans diagnosis and
> the 25% per-pregnancy recurrence risk. This framework generalizes to other haploinsufficiency and
> chromosomal-instability syndromes.

**Bullets:**
- Oncology surveillance q3mo until age 7 (Orphanet — SIOP-Europe 2021)
- Blood counts — MDS (Laberko 2019)
- Standard pediatric rhabdomyosarcoma regimen
- Parental genotyping — 25% recurrence risk

**Footer:** Consortium: `VERIFICACION_MANEJO_CLINICO.md` (A1–A8 + 7 corrections)

**Evidence:**
| Data point | Evidence / provenance |
|---|---|
| Renal/ECO surveillance q3mo—age 7 | Orphanet #1052 — Hol et al., **Eur J Cancer 2021;153:51** (SIOP-Europe) |
| MDS/blood counts | Laberko et al., **Orphanet J Rare Dis 2019** (PMID 31040233) |
| Onset at diagnosis, tumor spectrum | Nakano et al., **Clin Cancer Res 2024;30:5009** (AACR) |
| Parental segregation / 25% risk | Consortium verification — OMIM #257300 (AR) |

---

## Scene 6 — Closing

**Narration:**
> For this patient, we cannot rebuild the checkpoint today. But we can offer a translational,
> honest and actionable path that restores the dosage of the causal protein, supported by primary
> evidence. Repurposing is not about finding a new drug for an old disease: it is about listening to
> what that patient's biology needs and finding an approved drug that already knows how to do it.
> Thank you.

**Bullets:**
- Translational, honest and actionable path
- Restores the dosage of the causal protein
- Reproducible F1–F6 pipeline, versioned outputs
- Thank you

**Footer:** byronzunigao — MVA Hackathon 2026 — Track 1+2 — github.com/bestpricegye-ai/mva-hackathon-2026

---

## Transcription note (LLM disclosure)

Narration and script curated via Anthropic API (Claude, commercial terms); every claim is cross-checked
against the cited primary literature; no patient-identifying data (PROBAND01, processed and anonymized
in `clinical_history.json`).
