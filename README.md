# MVA Hackathon 2026 — BUB1B / MVA1 Diagnostic & Drug-Repurposing Pipeline

**Team:** byronzunigao
**Track 1 (Variant Prediction)** + **Track 2 (Drug Repurposing)**
**Event:** *Rare Disease, Real Kid: The MVA Hackathon 2026* (Sage Bionetworks · MVA Society · Hugging Face · BEACON)

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
├── requirements.txt
├── src/                          <- reproducible pipeline scripts (Python 3)
│   ├── analyze_exons.py          <-   primary: BUB1B/CEP57/TRIP13 exonic scan
│   ├── analyze_sac_panel.py      <-   24-gene SAC panel scan
│   ├── analyze_panel2.py         <-   67-71 gene cancer/renal panel scan
│   ├── scan_acmg.py              <-   ACMG SF v3.0 (53 genes) secondary-findings scan
│   ├── collect_acmg.py           <-   candidate collection + gnomAD annotation
│   ├── build_acmg.py / build_panel2.py  <- panel exon resolution (Ensembl REST)
│   ├── gnomad_acmg.py / gnomad_panel2.py / gnomad_renal.py  <- gnomAD v4 GraphQL
│   └── fase2_hardfilter.py / fase2_gnomad.py  <- phase-2 hard-filter + frequency
├── data/
│   ├── panels/                   <- panel exon coordinates (public, Ensembl GRCh38)
│   └── results/                  <- processed outputs (no raw data)
├── deliverables/                 <- READY-TO-SUBMIT files (Track 1 + Track 2)
│   ├── track1/predictions/byronzunigao_bub1b-compound-het-acmg.csv
│   ├── track1/report/byronzunigao_track1_report.md
│   └── track2/byronzunigao_track2_report.md
└── docs/                         <- consolidated reports / supporting docs
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

**Script paths note:** the original working scripts hard-code absolute Windows paths
(e.g. `C:\starquake\hackathonmva\...`). Before running, update the `VCF` and panel paths at the top of
each script to your local layout. The panel JSONs in `data/panels/` are the resolved Ensembl exon
coordinates and can be reused directly.

---

## ✅ Deliverables (ready to submit)

See **`deliverables/LEEME.md`** for the full submission checklist. Summary:

- **Track 1 CSV** — `deliverables/track1/predictions/byronzunigao_bub1b-compound-het-acmg.csv`
  (columns match the official template; `proband_id=PROBAND01`; GRCh38; expects **100 pts / 1.000 F-max**).
- **Track 1 report** — `deliverables/track1/report/byronzunigao_track1_report.md`
  (follows the official methods template, incl. the **required LLM disclosure**).
- **Track 2 report** — `deliverables/track2/byronzunigao_track2_report.md`
  (drug repurposing for MVA1: NMN/NAD+, senolytics, growth hormone; anti-mitotics contraindicated).

### Pipeline phases (reproducible, `src/`)

| Fase | Contenido | Scripts | Salida |
|---|---|---|---|
| Fase 1 | Ingestión, fenotipado (HPO), anotación genómica | `analyze_*.py`, `build_*.py`, `collect_acmg.py`, `gnomad_*.py` | `data/results/*.txt` |
| Fase 2 | Hard-filter + gnomAD v4 + exclusión de co-causalidad | `fase2_hardfilter.py`, `fase2_gnomad.py` | 8 variantes ausentes |
| **Fase 3** | **Predicción funcional (VEP) + enriquecimiento de rutas (STRING)** | `fase3_impacto.py`, `fase3_enrichment.py` | `data/results/fase3_impacto.txt`, `fase3_enrichment.json` |

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
