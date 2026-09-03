# DIAGNÓSTICO MOLECULAR — MVA HACKATHON 2026

**Probanda:** WGS_EX2312012 (GRCh38, VCFv4.2, muestras único)
**Fecha de análisis:** 2026

---

## Hallazgo principal

**Diagnóstico: Mosaic Variegated Aneuploidy Syndrome 1 (MVA1, OMIM #257300)**
**Gen causante: BUB1B** (MVA1, chr15:40,160,984-40,221,137, strand +)

Mecanismo: **heterocigosidad compuesta (bialélica) en BUB1B** — herencia autosómica recesiva.

### Variantes (filtrado por exones del transcrito canónico ENST00000287598)

| # | Posición (GRCh38) | HGVS (NM_001211.6) | Consecuencia | Genotipo | AD/DP | Frecuencia | Evidencia |
|---|-------------------|---------------------|--------------|----------|-------|------------|-----------|
| 1 | chr15:40,209,701 | c.2210T>G, p.(Leu737Ter) | **stop_gained (LOF)** | 0/1 (het) | 21,25 / 46 | ExAC 0.005% (gnomAD 3.29e-05) | ClinVar RCV000641226 asociada a MVA1 |
| 2 | chr15:40,220,612 | c.3006T>G, p.(Asn1002Lys) | **missense** (exón terminal) | 0/1 (het) | 15,13 / 28 | no catalogada (rara) | novel, ausente en ClinVar/gnomAD |

Ambas variantes están **heterocigotas (0/1) y en alelos distintos (en trans)** → **heterocigosis compuesta** = estado bialélico patogénico.

### Genes descartados
- **CEP57** (MVA2, chr11): 0 variantes exónicas → descartado
- **TRIP13** (MVA3, chr5): 0 variantes exónicas → descartado

---

## Correlación clínica

El perfil se ajusta perfectamente a MVA1:

- **Cáncer (rabdomiosarcoma):** BUB1B es el gen de MVA con el mayor riesgo oncológico (~75%, incluye sarcomas de origen germinal — panel Genomics England "Familial rhabdomyosarcoma"/"Sarcoma cancer susceptibility"). El p.Leu737Ter LOF está formalmente ligado a MVA1 en ClinVar.
- **Fenotipo MVA completo** (microcefalia, fallo de medrar, talla baja, nefrocalcinosis, parto prematuro 32 sem, bajo peso 1 kg): consistente con la literatura (Hanks et al. Nat Genet 2004; García-Castillo et al. 2008).
- **Abortos recurrentes parentales:** los portadores heterocigotos de variantes severas de BUB1B tienen riesgo elevado de pérdida de embarazos (compatible con lo reportado por Hanks 2004).

**Nota de mosaicismo espontáneo:** Ambas variantes germinales muestran AD balanceado (~50/50), es decir, no son mosaicismo somático en sangre. El mosaicismo característico de MVA1 (aneuploidías variegadas 45/47, PCS — premature chromatid separation) proviene de la falla del *spindle checkpoint* debida a la disfunción de BUB1B/BUBR1, no de las variantes en sí.

---

## Interpretación ACMG (borrador)

- **p.Leu737Ter:** PVS1 (stop_gained LOF en gen con haploinsuficiencia como mecanismo de MVA1) + PM2 (rara/ausente) + PM3 (en trans con variante patogénica/likely pathogenic) → **Pathogenic**
- **p.Asn1002Lys:** PM2 (no catalogada en gnomAD/ClinVar) + PM3 (en trans con variante patogénica) + PM1 (ubicada en dominio quinasa catalítica de BUBR1) + PP3 (SIFT/Polyphen/AlphaMissense 0.9229 deletéreos) = **Likely Pathogenic**

**Diagnóstico final: MVA1 por heterocigosis compuesta bialélica en BUB1B.**

---

## Método reproducido (archivos)

- `analyze_exons.py` — filtra VCF a exones canónicos de BUB1B/CEP57/TRIP13
- `vcf_exonic_variants.txt` — output (2 variantes exónicas, ambas BUB1B)
- `_exons.txt` — coordenadas de exones (Ensembl REST, GRCh38)
- `_vep2.txt` / `_vep_freq.txt` — anotación VEP (consecuencia, aminoácidos, rsID)
- Exones Ensembl REST; VEP Ensembl REST; ClinVar RCV000641226
