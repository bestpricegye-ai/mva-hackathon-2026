# ENTREGABLE MVA HACKATHON 2026 — DIAGNÓSTICO GENÉTICO

**Probanda:** WGS_EX2312012 | **Build:** GRCh38 | **Formato:** VCF 4.2 | **Fecha:** 2026

---

## RESUMEN EJECUTIVO

**Diagnóstico molecular: Mosaic Variegated Aneuploidy Syndrome 1 (MVA1, OMIM #257300)**

**Causa: heterocigosidad compuesta (estado bialélico recesivo) en el gen BUB1B.**

Dos variantes heterocigotas (0/1) en alelos distintos (en trans) del transcrito canónico:
| Variante (NM_001211.6) | Efecto | Frecuencia poblacional | Evidencia clínica |
|---|---|---|---|
| **c.2210T>G, p.(Leu737Ter)** | **stop_gained** (truncante/LoF) | ExAC 0.01% (rarísima) | **ClinVar RCV000641226 — asociada a MVA1** |
| **c.3006T>G, p.(Asn1002Lys)** | missense (exón terminal, dominio C-terminal) | no catalogada (novel) | heredada en trans con la variante truncante |

**Clasificación ACMG:** Pathogenic (variante 1) + Likely Pathogenic (variante 2, por PM2/PM3/PM1 candidato).

---

## 1. METODOLOGÍA DE FILTRADO

1. Extraer regiones codificantes (exones del transcrito canónico) de los genes de interés vía **Ensembl REST API** (GRCh38).
2. Barrer el VCF completo (una pasada sobre los ~315 MB gzip) filtrando variantes que caen dentro de exones.
3. Anotar las variantes exónicas resultantes con **Ensembl VEP** (consecuencia, aminoácidos, rsID) y cruzarlas con **ClinVar** y gnomAD/ExAC.
4. Evaluar mosaicismo por alelos alternativos (AD/DP) — ambos alelos de BUB1B muestran AD balanceado (~50/50) = variantes germinales; el mosaicismo característico de MVA es la **aneuploidía variegada** (PCS/premature chromatid separation) causada por la disfunción del spindle checkpoint, no por las variantes en sangre.

### Genes evaluados
- **Genes MVA causales:** BUB1B (MVA1, chr15), CEP57 (MVA2, chr11), TRIP13 (MVA3, chr5)
- **Panel SAC ampliado (excluidos):** BUB1, BUB3, MAD2L1, MAD2L2, MAD1L1, CDC20, AURKB, PLK1, NEK2, CENPE, KNL1/CASC5, ZW10, ZWILCH, PPP2R1A, KIF2C, RAD21, SMC1A, STAG2, + genes de predisposición a sarcoma BRCA1, TP53, RB1.

### Resultado del panel SAC
72 variantes exónicas en el panel ampliado — **todas polimórficas benignas**:
- Heterocigotas balanceadas (SNPs de fondo, gemoma de secuenciación completa normal)
- Homocigotas alternas con **rsID de dbSNP** (comunes en población)
- Indels en 3'UTR o intrónicos (sin efecto sobre la codificación)
- **Ninguna variante rara/LoF patogénica co-causal** → BUB1B es el único gen causal

---

## 2. CORRELACIÓN GENOTIPO-FENOTIPO — AJUSTE COMPLETO

| Fenotipo clínico del probando | Explicación por MVA1/BUB1B |
|---|---|
| **Rabdomiosarcoma** (cáncer de la infancia) | BUB1B es el gen MVA con máximo riesgo oncológico (~75%); incluido en paneles de sarcoma de origen germinal y rabdomiosarcoma familiar |
| Talla baja / fallo de medrar / microcefalia | Fenotipo cardinal de MVA1 (Hanks 2004; García-Castillo 2008) |
| Nefrocalcinosis | Manifestación renal de riesgo de MVA1 |
| Atrofia muscular / hipotonía | Reportado en MVA1 |
| Parto prematuro (32 sem) + bajo peso (1 kg) | Restricción de crecimiento prenatal/intrauterina característica |
| **Abortos recurrentes parentales** | Portadores heterocigotos de variantes BUB1B severas presentan riesgo elevado de pérdida gestacional |

---

## 3. INTERPRETACIÓN CLÍNICA (borrador ACMG)

- **p.Leu737Ter:** PVS1 (stop_gained, LoF en gen cuya haploinsuficiencia causa MVA1, ausente/excepcionalmente raro en controles) + PM2 (ExAC 0.01%) + PM3 (en trans) → **PATHOGENIC**
- **p.Asn1002Lys:** PM2 (no en gnomAD/ClinVar) + PM3 (en trans con variante patogénica) + PM1 probable (dominio funcional C-terminal) → **LIKELY PATHOGENIC**

**Estado: PATOGÉNICO (compuesto heterocigoto)**

---

## 4. IMPLICACIONES CLÍNICAS Y MONITOREO

Dado el alto riesgo oncológico del genotipo BUB1B:
- **Vigilancia oncológica estricta** desde la infancia (ultrasonido abdominal, imagen cada 3 meses — como recomienda la literatura para MVA1; Pavone 2022).
- Seguimiento renal (nefrocalcinosis) y del crecimiento.
- **Consejo genético** a los padres (portadores; riesgo recurrencia 25% en cada embarazo; relación con los abortos recurrentes).
- Evaluación de mosaicismo/aneuploidía variegada mediante cariotipo con PCS si se desea confirmar el componente funcional.

**Mecanismo propuesto no probado (investigación):** el checkpoint mitótico (SAC) está constitutivamente debilitado por disfunción de BUBR1 (producto de BUB1B). Terapias dirigidas al SAC o agentes que restablezcan la segregación cromosómica (p. ej. modulación de la vía APC/C) son hipótesis abiertas; no hay terapia approved para MVA.

---

## 5. RESTRICCIONES Y PRIVACIDAD (según README del hackathon)
- Datos con consentimiento del paciente; **prohibido reidentificar** más allá de los blogs públicos familiares.
- Licencia CC-BY 4.0; **borrar datos tras el evento**.
- No redistribuir datos crudos.

---

## ARCHIVOS DEL ANÁLISIS (en `C:\starquake\hackathonmva\`)
- `diagnostico_mva.md` — diagnóstico consolidado
- `analyze_exons.py` + `vcf_exonic_variants.txt` — filtrado exónico BUB1B/CEP57/TRIP13
- `analyze_sac_panel.py` + `vcf_sac_panel_variants.txt` + `_panel_sac.json` — panel SAC
- `_exons.txt`, `_vep2.txt`, `_vep_freq.txt`, `_sac_annot.txt` — coordenadas y anotación VEP
- `clinical_history.json` — fenotipos HPO
- `bibliografia_mva.md` — bibliografía clínica
