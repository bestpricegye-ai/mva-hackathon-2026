# CHECKLIST — FASE 1: INGESTIÓN, ESTRUCTURACIÓN Y CONFIGURACIÓN DE DATOS (Días 1–5)

**Caso:** Rare Disease, Real Kid: MVA Hackathon 2026
**Proyecto:** `C:\starquake\hackathonmva\` | **Build:** GRCh38 | **Fecha de auditoría:** 2026-08-31
**Leyenda:** ✅ Cumplido · ⚠️ Cumplido con desvío documentado · ❌ Pendiente

---

## 1.1 Procesamiento del expediente clínico (DOCX → HPO)

| # | Ítem del requisito | Estado | Evidencia / Implementación |
|---|---|---|---|
| 1.1.1 | Leer/analizar `Challenge_Clinical_Phenotype_1.docx` | ✅ | Lectura del DOCX (párrafos + tabla `python-docx`) — expediente confidencial respetado |
| 1.1.2 | Script Python asistido por LLM de alta precisión | ✅ | El LLM estructuró el expediente en prosa → JSON; mapeo HPO automatizado |
| 1.1.3 | Extraer la **cronología de síntomas** | ✅ | 7 rasgos + historial familiar en `clinical_history.json` con `notes` (incl. presentación "desde el nacimiento", "32 sem") |
| 1.1.4 | Mapeo automatizado a códigos HPO estandarizados | ✅ | 8 términos HPO con IDs: HP:0002859, HP:0000121, HP:0004322, HP:0001508, HP:0003202, HP:0001622, HP:0001518, HP:0200067 |
| 1.1.5 | Reconocer el **cluster fenotípico** (no rasgos aislados) | ✅ | Cluster = predisposición a cáncer + crecimiento + renal + perinatal + pérdidas reproductivas → MVA |
| 1.1.6 | Tratar el historial familiar (abortos) como **señal**, no background | ✅ | HP:0200067 (Recurrent spontaneous abortion) tratado como input fenotípico |

**Artefactos:** `Challenge_Clinical_Phenotype_1.docx` (entrada), `clinical_history.json` (salida estructurada),
`CORRELACION_GENOTIPO_FENOTIPO.md` (Track 2: mapeo completo).

---

## 1.2 Configuración del entorno de datos

| # | Ítem del requisito | Estado | Evidencia / Implementación |
|---|---|---|---|
| 1.2.1 | Obtener el repositorio de datos del reto (~85 GB) | ⚠️ | Se descargaron **solo los archivos necesarios**: VCF WGS (315 MB gzip) + índice `.tbi`. **No** los 85 GB completos (FASTQ, BAM) porque el VCF es suficiente y los datos son confidenciales |
| 1.2.2 | Montar localmente el entorno | ✅ | `WGS_EX2312012_HGWCNDSX7.vcf.gz` (315 MB) + `WGS_EX2312012_HGWCNDSX7.vcf.gz.tbi` |
| 1.2.3 | Sistema de almacenamiento optimizado (SQLite/vector DB indexadas) | ⚠️ | **Desvío documentado:** se usó **índice tabix (`.tbi`)** + escaneo gzip de una pasada en lugar de SQLite. Ver §1.2.4 |
| 1.2.4 | Justificación del desvío `.tbi` vs. SQLite | ✅ | El VCF ya tiene indexación estándar de la industria (tabix); reindexar 5M variantes en SQLite es redundante y más lento para consultas por región/genotipo. El acceso tabix cumple el propósito (acceso optimizado) con la herramienta correcta |
| 1.2.5 | Integridad/contabilidad del dataset | ✅ | 5,012,204 variantes totales; 0 errores de parseo (logs de análisis) |

**Artefactos:** `WGS_EX2312012_HGWCNDSX7.vcf.gz`, `WGS_EX2312012_HGWCNDSX7.vcf.gz.tbi`, `README.md` (metadatos/privacy).

---

## 1.3 Pipeline de anotación genómica

| # | Ítem del requisito | Estado | Evidencia / Implementación |
|---|---|---|---|
| 1.3.1 | Herramienta estándar de anotación (Ensembl VEP o SnpEff) | ✅ | **Ensembl VEP (REST)** usado para anotar consecuencia, aa, rsID de las variantes BUB1B |
| 1.3.2 | Anotación de coordenadas genómicas → funcional | ✅ | Traducción `chr15:40,209,701 T>G` → `c.2210T>G p.Leu737Ter` (stop_gained); `chr15:40,220,612` → `c.3006T>G p.Asn1002Lys` (missense) |
| 1.3.3 | Enriquecimiento poblacional | ✅ | gnomAD v4 (GraphQL) + ExAC para frecuencias (AF/AC/AN) de los candidatos |
| 1.3.4 | Enriquecimiento clínico | ✅ | ClinVar (RCV000641226 asociado a MVA1), InterPro (dominio quinasa) |
| 1.3.5 | Enriquecimiento por predicción de impacto | ✅ | AlphaMissense (pLM), SIFT, PolyPhen |
| 1.3.6 | Scripts personalizados de filtrado/priorización | ✅ | `analyze_exons.py`, `analyze_sac_panel.py`, `analyze_panel2.py`, `scan_acmg.py`, `gnomad_panel2.py`, `build_panel2.py`, `_acmg_finish.py`, etc. |
| 1.3.7 | Frecuencias para descartar el 99.9% del ruido | ✅ | Anotación gnomAD completa: panel2 (110/110, 0 blocked), ACMG SF3 (102/102) |

**Artefactos:** `vcf_exonic_variants.txt`, `vcf_sac_panel_variants.txt`, `vcf_panel2_variants.txt`, `vcf_acmg_scan.txt`,
`_gnomad_resume.json`, `_acmg_gnomad.json`, `_vep*.txt`, `_vus_missense.txt`.

---

## Resumen del checklist

| Bloque | Cumplido | Con desvío | Pendiente |
|---|---|---|---|
| **1.1 Expediente → HPO** | 6/6 | 0 | 0 |
| **1.2 Entorno de datos** | 3/5 | 2 (1.2.1, 1.2.3) | 0 |
| **1.3 Anotación genómica** | 7/7 | 0 | 0 |
| **TOTAL** | **16/18** | **2** | **0** |

**Evaluación general: Fase 1 COMPLETA.** Los 2 desvíos son **optimizaciones técnicas justificadas**
(no descargar los 85 GB innecesarios por privacidad/eficiencia, y usar tabix en lugar de SQLite).
Ningún requisito funcional de la Fase 1 quedó incumplido: el pipeline de ingestión, estructuración y
anotación quedó operativo y produjo el diagnóstico en las fases siguientes.

---

*Nota de privacidad: conforme a las restricciones del expediente (CC-BY 4.0, borrar datos tras el evento,
no reidentificar), no se incluye ningún dato reidentificable del paciente ni su familia.*
