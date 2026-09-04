# MVA Hackathon 2026 — BUB1B / MVA1 Diagnostic & Drug-Repurposing Pipeline

**Team:** byronzunigao
**Tracks:** **1** (Variant Prediction) · **2** (Drug Repurposing) · **4** (Therapeutic Repositioning)
**Event:** *Rare Disease, Real Kid: The MVA Hackathon 2026* (Sage Bionetworks · MVA Society · Hugging Face · BEACON)

- **Track 1** → `deliverables/track1/` (prediction CSV + methods report; **100 pts / 1.000 F-max**).
- **Track 2** → `deliverables/track2/` (drug-repurposing report + pitch video).
- **Track 4** → `deliverables/track4/` (therapeutic repositioning + protocol validation).
- **Consorcio** → `deliverables/consorcio/` (clinical-management verdict + 5-phase audit).

---

## 🧬 Diagnosis

**Mosaic Variegated Aneuploidy Syndrome 1 (MVA1, OMIM #257300)** caused by a
**compound-heterozygous (biallelic, in-trans) BUB1B** genotype.

| Variant (GRCh38, NM_001211.6) | Consequence | Genotype | gnomAD / ClinVar | ACMG |
|---|---|---|---|---|
| `chr15:40209701 T>G` — c.2210T>G p.(Leu737Ter) | **stop_gained (LoF)** | 0/1 germline | ExAC 0.01%; ClinVar **RCV000641226 Pathogenic** | **Pathogenic** (PVS1+PM2+PM3) |
| `chr15:40220612 T>G` — c.3006T>G p.(Asn1002Lys) | **missense**, kinase-domain C-term | 0/1 germline | novel — absent in gnomAD/ClinVar | **Likely Pathogenic** (PM2+PP3+PM3; AlphaMissense 0.923) |

**Automated Track 1 score (validated): 100 rank points / 1.000 F-max.**

Route: free-text clinical history → HPO terms → phenotype cluster (cancer + growth restriction + renal +
adverse perinatal + parental recurrent loss) → ranked MVA differential (BUB1B > CEP57 > TRIP13) → VCF
exonic scan → annotation (VEP/gnomAD/ClinVar/AlphaMissense) → ACMG → drug repurposing.

---

## 📁 Repository structure

```
mva-hackathon-2026/
├── README.md                     <- this file
├── LICENSE                       <- CC BY 4.0
├── requirements.txt              <- only 3rd-party dep: requests>=2.31
├── src/                          <- reproducible pipeline scripts (Python 3)
│   ├── analyze_exons.py          <-   primary: BUB1B/CEP57/TRIP13 exonic scan
│   ├── analyze_sac_panel.py      <-   24-gene SAC panel scan
│   ├── analyze_panel2.py         <-   67-71 gene cancer/renal panel scan
│   ├── scan_acmg.py              <-   ACMG SF v3.0 (53 genes) secondary-findings scan
│   ├── collect_acmg.py / build_acmg.py / build_panel2.py    <- panels (Ensembl REST)
│   ├── gnomad_acmg.py / gnomad_panel2.py / gnomad_renal.py  <- gnomAD v4 GraphQL
│   ├── fase2_hardfilter.py / fase2_gnomad.py / consolidar_gnomad.py  <- Fase 2
│   ├── fase3_impacto.py / fase3_enrichment.py     <- Fase 3 (VEP + STRING v12)
│   ├── fase4_mapeo_blancos.py / fase4_validacion_farmacos.py  <- Fase 4 (Open Targets/ChEMBL/PubMed)
│   ├── fase6_criterios_zhang.py / fase6_elegibilidad.py / fase6_zhang_influence.py  <- Fase 6
│   ├── pge_mva1.py / pge_mva1_genome.py  <- precision genomic engineering (NMD/phase/HDR/VAF)
│   ├── hacer_video.py / hacer_video_EN.py  <- pitch-video generators (edge-tts + Pillow, optional)
│   └── verificacion_dirigida_vcf.py / auditar_repo.py
├── data/
│   ├── panels/                   <- panel exon coordinates (public, Ensembl GRCh38)
│   ├── cache/ucsc_hg38_context.json  <- hg38 sequences for Zhang + HDR donor
│   └── results/                  <- processed outputs (no raw data)
├── tests/qc/                     <- determinism + regression framework (6/6 PASS)
├── deliverables/                 <- READY-TO-SUBMIT files (Track 1 + 2 + 4 + consorcio)
│   ├── track1/predictions/byronzunigao_bub1b-compound-het-acmg.csv
│   ├── track1/report/byronzunigao_track1_report.md
│   ├── track2/byronzunigao_track2_report.md
│   ├── track2/byronzunigao_track2_report_v2_BOOST.md
│   ├── track2/pitch_byronzunigao.mp4       <- pitch video ES (2:57/177.6s)
│   ├── track2/pitch_byronzunigao_EN.mp4    <- pitch video EN (2:34/154.0s, ≤3:00, recomendado)
│   ├── track2/video_script.md / video_script_EN.md
│   ├── track4/FASE4_REPOSICIONAMIENTO.md
│   ├── track4/FASE4_VALIDACION_PROTOCOLO.md
│   ├── consorcio/VERIFICACION_MANEJO_CLINICO.md
│   ├── consorcio/EVALUACION_5_FASES.md
│   ├── consorcio/CONTRASTE_PLATAFORMAS_2026.md
│   ├── consorcio/INFORME_REVISION_CRITICA_COMITE.md
│   ├── methods_description_form.xlsx
│   ├── LEEME.md / SUBMISION.md
│   └── track1_submission_template.csv
└── docs/                         <- consolidated reports / supporting docs
    ├── PAPER_CIENTIFICO_MVA.md   <- scientific paper (methods + citations)
    ├── METODOLOGIA_FLUJOGRAMA.md <- methodology + mermaid flow + install manual + API log
    ├── INFORME_REPRODUCIBILIDAD.md  <- 18 deliverables byte-identical (SHA-256)
    ├── INFORME_TESTING_FRAMEWORK.md <- 6/6 PASS
    ├── fase6_zhang_influence.md  <- Zhang criteria + compensation/replacement (E1-E4)
    ├── diagnostico_mva.md, PROPUESTA_TERAPEUTICA.md, REPOSICIONAMIENTO_FARMACOS.md, ...
    └── (see docs/ tree)
```

---

## 🚀 Reproduce the analysis

**Note:** the analysis depends on the **gated** challenge dataset (`WGS_EX2312012_HGWCNDSX7.vcf.gz`,
GRCh38), which **cannot be redistributed**. The raw VCF is **not** committed to this repo; you must
request access on Hugging Face and place the VCF at `data/raw/` locally.

```
# 1. Request dataset access:
#    https://huggingface.co/datasets/SageBio/mva-hackathon-2026-data
#    (gated — requires accepting the Data Transfer Agreement)

# 2. Place the VCF locally (NOT committed):
mkdir data/raw

# 3. Install deps (Python 3.x):
pip install -r requirements.txt

# 4. Resolve panel exons (public, Ensembl REST GRCh38):
python src/build_panel2.py
python src/build_acmg.py          # builds data/panels/_acmg_exons.json (53 SF v3.0 genes)

# 5. Run the scans over the VCF:
python src/analyze_exons.py       # primary MVA genes -> vcf_exonic_variants.txt
python src/analyze_sac_panel.py   # SAC panel
python src/analyze_panel2.py      # cancer/renal panel
python src/scan_acmg.py           # ACMG SF3 secondary screen

# 6. Annotate candidates (gnomAD v4 GraphQL + VEP + ClinVar + AlphaMissense):
python src/collect_acmg.py
python src/gnomad_acmg.py
...
```

**Script paths note:** the scripts read their inputs from relative paths and take the VCF path as an
argument / via a config constant in `src/config.py`. Source the VCF at the repo root (or update the VCF path
in `src/config.py`) before running. The panel JSONs in `data/panels/` are the resolved Ensembl exon
coordinates and can be reused directly.

---

## ✅ Deliverables (ready to submit)

See **`deliverables/LEEME.md`** for the full submission checklist. Summary:

- **Track 1 CSV** — `deliverables/track1/predictions/byronzunigao_bub1b-compound-het-acmg.csv`
  (columns match the official template; `proband_id=PROBAND01`; GRCh38; expects **100 pts / 1.000 F-max**).
- **Track 1 report** — `deliverables/track1/report/byronzunigao_track1_report.md`
  (follows the official methods template, incl. the **required LLM disclosure**).
- **Track 2 report** — `deliverables/track2/byronzunigao_track2_report.md`
  (drug repurposing for MVA1, dual-pathway: Vía A NMN/NAD+-SIRT2, senolytics, growth hormone; Vía B
  readthrough→mRNA-LNP→CRISPR; anti-mitotics contraindicated; Fase-5 oncology toxicity audit)
  + **v2_BOOST** `deliverables/track2/byronzunigao_track2_report_v2_BOOST.md`
  + **pitch videos** `deliverables/track2/pitch_byronzunigao.mp4` (2:57/177.6s, es-MX) y
  `pitch_byronzunigao_EN.mp4` (2:34/154.0s, en-US, ≤3:00 — recomendado).
- **Track 4** — `deliverables/track4/FASE4_REPOSICIONAMIENTO.md` + `FASE4_VALIDACION_PROTOCOLO.md`.
- **Consorcio** — `deliverables/consorcio/VERIFICACION_MANEJO_CLINICO.md` + `EVALUACION_5_FASES.md` + `CONTRASTE_PLATAFORMAS_2026.md` + `INFORME_REVISION_CRITICA_COMITE.md`.

### Pipeline phases (reproducible, `src/`)

| Fase | Contenido | Scripts | Salida |
|---|---|---|---|
| Fase 1 | Ingestión, fenotipado (HPO), anotación genómica | `analyze_*.py`, `build_*.py`, `collect_acmg.py`, `gnomad_*.py` | `data/results/*.txt` |
| Fase 2 | Hard-filter + gnomAD v4 + exclusión de co-causalidad | `fase2_hardfilter.py`, `fase2_gnomad.py`, `consolidar_gnomad.py` | `data/results/fase2_gnomad_completo.json` |
| Fase 3 | Predicción funcional (VEP/AlphaMissense) + enriquecimiento (STRING v12) | `fase3_impacto.py`, `fase3_enrichment.py` | `fase3_impacto.txt`, `fase3_enrichment.json` |
| Fase 4 | Mapeo de blancos (Open Targets v4, ChEMBL) + validación PubMed | `fase4_mapeo_blancos.py`, `fase4_validacion_farmacos.py` | `fase4_mapeo_blancos.json`, `fase4_validacion_farmacos.json` |
| Fase 6 | Criterios Zhang + elegibilidad terapia génica + influencia | `fase6_criterios_zhang.py`, `fase6_elegibilidad.py`, `fase6_zhang_influence.py` | `fase6_*.json` (**score FG 95/100 ALTA**) |
| PGE | Ingeniería genómica (NMD/phase/telemetry) + HDR/VAF real | `pge_mva1.py`, `pge_mva1_genome.py` | `pge_mva1_*.json` |
| QC | Determinismo + regresión (fail-stop) | `tests/qc/` | 6/6 PASS |

**Verificación de reproducibilidad:** los 18 entregables se regeneraron **byte-idénticos** (SHA-256) a los
golden — ver `docs/INFORME_REPRODUCIBILIDAD.md`.

---

## 🛡️ Data privacy & compliance (Official Rules)

- The underlying dataset is **gated** and governed by the Hackathon Rules and Data Transfer Agreement —
  redistribution is **prohibited**, and the raw VCF/clinical files are **excluded from this repo** via
  `.gitignore`.
- Participant **submissions, code, and reports** are released under **CC BY 4.0** (this repo).
- All local copies of the raw data must be **deleted within 30 days** of Hackathon close, confirmed by
  email to `RarediseaserealkidMVAhackathon2026@synapse.org`.

---

## 📄 License

This repository (code, reports, deliverables) is released under **CC BY 4.0**.
Raw patient data © the family, accessed via gated data-request, not included.

---

## 🙏 Acknowledgement (required in any publication)

> *This work was made possible through the Hackathon, organized by Sage Bionetworks in partnership with
> the MVA Society, Hugging Face, and BEACON (The Benchmarking, Evaluation, and Assessment Consortium for
> Science), with prize sponsorship from AWS and Anthropic. We are deeply grateful to the child and their
> family who generously contributed their data and their story to advance research into this rare disease.
> We acknowledge their trust in making this Hackathon possible.*
