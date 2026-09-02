# METODOLOGÍA Y FLUJOGRAMA — Pipeline de Diagnóstico y Reposicionamiento Terapéutico MVA

**Hackathon MVA 2026 — Track 2**
**Repositorio:** `C:\starquake\hackathonmva` · Git remoto: `github.com/bestpricegye-ai/mva-hackathon-2026`
**Probanda:** WGS_EX2312012 (GRCh38, VCFv4.2)

---

## 1. Flujograma general (Mermaid)

```mermaid
flowchart TD
    A[VCF fuente<br/>WGS_EX2312012_HGWCNDSX7.vcf.gz<br/>GRCh38 + tabix] --> B[Fase 0: QC<br/>tests/qc determinismo+regresión]
    B --> C[Fase 1: Filtrado VCF<br/>analyze_vcf / analyze_exons / analyze_sac_panel / analyze_panel2<br/>canonical BUB1B/CEP57/TRIP13]
    C --> D[Fase 2: Hard-filter + gnomAD<br/>fase2_hardfilter / fase2_gnomad / consolidar_gnomad]
    D --> E[Fase 3: Impacto + Enrichment<br/>fase3_impacto (VEP) / fase3_enrichment (STRING v12)]
    E --> F[Fase 4: Blancos + Validación<br/>fase4_mapeo_blancos (Open Targets, ChEMBL)<br/>fase4_validacion_farmacos (PubMed)]
    F --> G[Diagnóstico molecular<br/>BUB1B comp-het + descarte CEP57/TRIP13]
    G --> H[Fase 6: Criterios Zhang<br/>fase6_criterios_zhang / fase6_elegibilidad / fase6_zhang_influence]
    H --> I[Elegibilidad terapia génica<br/>score 95/100 ALTO]
    G --> J[PGE: Ingeniería genómica<br/>pge_mva1 (NMD/phase/telemetry)<br/>pge_mva1_genome (HDR, primers, VAF)]
    E --> K[Reposicionamiento terapéutico<br/>NAD+/SIRT2, senolíticos,<br/>inhibidores cinasa mitótica]
    I --> L[Entregables reproducibles<br/>data/results/*.json + docs/*.md]
    J --> L
    K --> L
    L --> M[Framework QC tests/qc<br/>golden_dataset / determinism / vcf_regression]
```

---

## 2. Variables de trabajo

| Variable | Valor |
|----------|-------|
| Dirección de trabajo | `C:\starquake\hackathonmva` |
| VCF fuente | `WGS_EX2312012_HGWCNDSX7.vcf.gz` (315 MB, GRCh38, índice `.tbi`) |
| Referencia | GRCh38 / hg38 |
| Transcrito canónico BUB1B | ENST00000287598 (NM_001211.6) |
| Genes MVA | BUB1B (chr15, MVA1), CEP57 (chr11, MVA2), TRIP13 (chr5, MVA3) |
| Python | 3.11.4 |
| Dependencias de terceros | `requests>=2.31` (resto: stdlib); opcional `edge-tts`+`Pillow` para `hacer_video.py` |

> **Nota:** `fase2_gnomad.py` debe ejecutarse **desde la raíz del repo** (usa la ruta relativa `_fase2_flat.json`).

---

## 3. Tabla de scripts: entrada / salida / API

### Fase 1 — Filtrado y análisis VCF

| Script | Entrada | Salida | API |
|--------|---------|--------|-----|
| `src/analyze_vcf.py` | VCF.gz | `data/results/vcf_acmg_scan.txt` | — |
| `src/analyze_exons.py` | VCF.gz + `_exons.txt` | `data/results/vcf_exonic_variants.txt` | Ensembl REST (exones) |
| `src/analyze_sac_panel.py` | VCF.gz | `data/results/vcf_sac_panel_variants.txt` | — |
| `src/analyze_panel2.py` | VCF.gz | `data/results/vcf_panel2_variants.txt` | — |
| `src/scan_acmg.py` | VCF.gz | `data/results/vcf_acmg_scan.txt` | — |

### Fase 2 — Hard-filter y gnomAD

| Script | Entrada | Salida | API |
|--------|---------|--------|-----|
| `src/fase2_hardfilter.py` | VCF.gz | filtros QC | — |
| `src/fase2_hardfilter2.py` | VCF.gz | filtros QC v2 | — |
| `src/fase2_gnomad.py` | VCF.gz (desde raíz) | `_fase2_flat.json` | Ensembl/VEP + gnomAD |
| `src/consolidar_gnomad.py` | `_fase2_flat.json`, VEP | `data/results/fase2_gnomad_completo.json` | — |

### Fase 3 — Impacto y enrichment

| Script | Entrada | Salida | API |
|--------|---------|--------|-----|
| `src/fase3_impacto.py` | VCF | `data/results/fase3_impacto.txt` | VEP (AlphaMissense) |
| `src/fase3_enrichment.py` | genes SAC | `data/results/fase3_enrichment.json` | STRING v12 (`required_score=400`) |

### Fase 4 — Mapeo de blancos y validación

| Script | Entrada | Salida | API |
|--------|---------|--------|-----|
| `src/fase4_mapeo_blancos.py` | genes/blancos | `data/results/fase4_mapeo_blancos.json` + `_f4_sac_presencia.txt` | Open Targets GraphQL v4, STRING |
| `src/fase4_validacion_farmacos.py` | blancos | `data/results/fase4_validacion_farmacos.json` + `_f4_val_pubmed.txt` | ChEMBL, PubMed |

### Fase 6 — Criterios Zhang y elegibilidad

| Script | Entrada | Salida | API |
|--------|---------|--------|-----|
| `src/fase6_criterios_zhang.py` | secuencia hg38 | `data/results/fase6_criterios_zhang.json` | UCSC hg38 (cache local `data/cache/ucsc_hg38_context.json`) |
| `src/fase6_elegibilidad.py` | HPO + VCF + Zhang | `data/results/fase6_elegibilidad.json` | — |
| `src/fase6_zhang_influence.py` | Zhang | `data/results/fase6_zhang_influence.json` | — |

### PGE — Ingeniería genómica de precisión

| Script | Entrada | Salida | API |
|--------|---------|--------|-----|
| `src/pge_mva1.py` (subcomandos nmd/phase/telemetry/selftest) | VCF + contexto | `data/results/pge_mva1_{nmd,phase,selftest}.json` | — |
| `src/pge_mva1_genome.py` | VCF + hg38 | `data/results/pge_mva1_genome.json` | UCSC hg38; índice GATK requerido para off-target |

### Soporte / utilidades

| Script | Función |
|--------|---------|
| `src/verificacion_dirigida_vcf.py` | Verificación dirigida de la región chr15 (16 variantes; VAF reales) |
| `src/auditar_repo.py` | Auditoría de secretos del repositorio |
| `src/config.py` | Configuración (contigs canónicos, hilos, etc.) |
| `src/hacer_video.py` | Generación de vídeo científico (usa `edge-tts` + `Pillow`, opcional) |

---

## 4. Manual de instalación y ejecución (Windows)

### 4.1 Instalación

```powershell
# 1. Requisitos
#    - Python 3.11+ instalado y en PATH
#    - Git para Windows

# 2. Clonar el repositorio
git clone https://github.com/bestpricegye-ai/mva-hackathon-2026.git
cd hackathonmva

# 3. (Recomendado) Entorno virtual
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# 4. Dependencias de terceros (solo requests es imprescindible)
pip install -r requirements.txt
# requirements.txt:  requests>=2.31

# 5. (Opcional) Para generar el vídeo científico
pip install edge-tts pillow
```

### 4.2 Preparación de datos

```powershell
# El VCF debe estar en la raíz del repo:
Test-Path .\WGS_EX2312012_HGWCNDSX7.vcf.gz        # True
Test-Path .\WGS_EX2312012_HGWCNDSX7.vcf.gz.tbi    # True (índice tabix)
```

### 4.3 Ejecución del pipeline (desde la raíz del repo)

```powershell
# Fase 1 — filtrado y análisis
python src\analyze_vcf.py
python src\analyze_exons.py
python src\analyze_sac_panel.py
python src\analyze_panel2.py

# Fase 2 — hard-filter + gnomAD  (fase2_gnomad DESDE LA RAÍZ)
python src\fase2_hardfilter.py
python src\fase2_hardfilter2.py
python src\fase2_gnomad.py
python src\consolidar_gnomad.py

# Fase 3 — impacto + enrichment
python src\fase3_impacto.py
python src\fase3_enrichment.py

# Fase 4 — blancos + validación
python src\fase4_mapeo_blancos.py
python src\fase4_validacion_farmacos.py

# Fase 6 — criterios Zhang + elegibilidad
python src\fase6_criterios_zhang.py
python src\fase6_elegibilidad.py
python src\fase6_zhang_influence.py

# PGE — ingeniería genómica
python src\pge_mva1.py selftest
python src\pge_mva1.py nmd
python src\pge_mva1.py phase
python src\pge_mva1_genome.py

# Verificación dirigida chr15
python src\verificacion_dirigida_vcf.py
```

### 4.4 Framework de pruebas (determinismo + regresión)

```powershell
# Los 6 escenarios de integración
python -m pytest tests\qc\test_integration.py -v

# Generar golden dataset / comparar regresión de VCF
python tests\qc\golden_dataset.py
python tests\qc\vcf_regression.py
```

---

## 5. Bitácora de API

### 5.1 Endpoints utilizados

| Servicio | Endpoint / API | Uso | Versión |
|----------|----------------|-----|---------|
| Ensembl REST | `/vep/human/{coords}` | Anotación funcional (consecuencia, aminoácidos, rsID) + frecuencias + AlphaMissense | VEP (McLaren 2016) |
| Ensembl REST | exones del transcrito canónico | Coordenadas de exones de BUB1B/CEP57/TRIP13 | GRCh38 |
| gnomAD | frecuencias alélicas | Criterio ACMG PM2 (rareza/ausencia) | gnomAD v2/v3 (Karczewski 2020) |
| STRING | API de red de interacciones | Enriquecimiento de red del SAC | v12, `required_score=400` |
| Open Targets | GraphQL v4 | Mapeo gen–diana–enfermedad | v4 |
| ChEMBL | API de bioactividad | Anotación de fármacos | — |
| PubMed | API E-utilities | Validación de evidencia bibliográfica | — |
| ClinVar | RCV | Asociación clínica de variantes (RCV000641226) | — |
| UCSC | secuencias hg38 (cache local) | Criterios Zhang (specificity/efficiency/PAM) y donor HDR | GRCh38 |

### 5.2 Endpoints / errores / aciertos notables

| API | Error/evento | Manejo | Acierto |
|-----|--------------|--------|---------|
| Ensembl VEP | Tiempo de espera ocasional | Reintentos con backoff; respuestas en caché local | Anotación completa de las 2 variantes BUB1B |
| STRING | Límite de resultados | Uso de `required_score` para filtrar | Red SAC con 45 aristas; interacciones BUB1B–BUB1/MAD2L1/CDC20 >0.99 |
| Open Targets GraphQL | Complejidad de esquema v4 | Consultas parametrizadas por gen | Mapeo coerente de blancos de BUB1B/SAC |
| gnomAD | Variante no catalogada | Se registra como novel/ausente | Soporta PM2 para p.Asn1002Lys |
| PubChem/ChEMBL | Endpoints de datos | Parseo de bioactividad | Validación de candidatos de reposicionamiento |

> **Nota sobre credenciales:** No se requieren API keys para los endpoints públicos utilizados (Ensembl, STRING, Open Targets, ChEMBL, PubMed, UCSC, gnomAD). Si algún entorno exigiera credenciales, estas deben inyectarse mediante variables de entorno y **nunca** integrarse en el código o en los documentos.

---

## 6. Anexos

- **Anexo A — Diagnóstico:** `docs/diagnostico_mva.md`
- **Anexo B — Reproducibilidad:** `docs/INFORME_REPRODUCIBILIDAD.md` (18 entregables byte-idénticos, SHA-256, `git diff` vacío)
- **Anexo C — Framework de pruebas:** `docs/INFORME_TESTING_FRAMEWORK.md` (6/6 PASS)
- **Anexo D — Elegibilidad FG:** `docs/fase6_elegibilidad.md`
- **Anexo E — PGE:** `docs/PGE_MVA1_INGENIERIA_GENOMICA.md`
- **Anexo F — Reposicionamiento:** `docs/REPOSICIONAMIENTO_FARMACOS.md`, `docs/PROPUESTA_TERAPEUTICA.md`
- **Anexo G — Bibliografía:** `docs/bibliografia_mva.md`
- **Anexo H — Verificación dirigida:** `docs/verificacion_dirigida_vcf.md`
- **Anexo I — Auditoría de secretos:** `docs/auditoria_secretos.md`

---

## 7. Notas de reproducibilidad

- Los 18 entregables (Fases 1, 2, 3, 4, 6 + PGE) se regeneraron **byte-idénticos** a los golden (SHA-256 coincidentes; `git diff` vacío), confirmando reproducibilidad total con las mismas versiones de datos.
- La única fuente potencial de no-reproducibilidad a futuro es el **drift de bases de datos externas** (STRING, Open Targets, ChEMBL, PubMed, gnomAD), mitigado por el comparador de regresión de VCF (`tests/qc/vcf_regression.py`).
- **Actualización (2026):** el estado de las bases de datos y de los endpoints debe verificarse antes de re-ejecutar una fase que dependa de API externas.
