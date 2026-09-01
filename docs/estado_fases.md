# Estado de Fases — MVA Hackathon 2026 (byronzunigao)

**Diagnóstico:** MVA1 (OMIM 257300) por compound-heterocigosis **BUB1B**.
**Fecha de cierre de fases:** 2026-08-31
**Estado general:** **Fase 1 ✅ concluida (auditada)** · **Fase 2 ✅ concluida (verificada)** · **Fase 3 ✅ concluida (predicción funcional + enriquecimiento)** · **Fase 4 ✅ concluida (descubrimiento terapéutico y reposicionamiento)**.

> Nota de nomenclatura: aquí "Fase 1 / Fase 2" se refieren al **pipeline interno de análisis de
> variantes** (no a los Tracks del challenge ni a las fases temporales del plan de trabajo — véase
> `CHECKLIST_FASE1.md` para la cobertura de requisitos del pipeline).

---

## Fase 1 — Ingestión, fenotipado y anotación genómica ✅

Cobertura documentada en `CHECKLIST_FASE1.md` (todos los ítems cumplidos; 2 desvíos justificados).

| Bloque | Estado | Evidencia |
|---|---|---|
| 1.1 Expediente → HPO | **6/6 ✅** | `clinical_history.json` (7 rasgos + familia; 8 términos HPO; cluster = cáncer + crecimiento + renal + perinatal + pérdidas) |
| 1.2 Entorno de datos | **✅** | VCF (315 MB) + índice tabix; 5,012,204 variantes; desvíos: solo VCF (no FASTQ), tabix en vez de SQLite |
| 1.3 Anotación genómica | **7/7 ✅** | VEP + gnomAD v4 (GraphQL) + ClinVar + AlphaMissense/SIFT/PolyPhen + paneles SAC/cancer/ACMG |

**Fallo primario Fase 1:** BUB1B compound-het
- `chr15:40209701 T>G` → c.2210T>G p.Leu737Ter (stop_gained; ClinVar Pathogenic)
- `chr15:40220612 T>G` → c.3006T>G p.Asn1002Lys (missense; novel; AlphaMissense 0.923)

---

## Fase 2 — Filtrado y exclusión de co-causalidad ✅

Cadena de pasos verificada de extremo a extremo:

| Paso | Script | Entrada → Salida | Verificación |
|---|---|---|---|
| 2.1 Hard filter | `fase2_hardfilter.py` | VCF → `_fase2_variants.json` | QUAL≥30, DP≥10, GQ≥20; 68 KB output existe |
| 2.2 Re-filtro + dedup + flatten | `fase2_hardfilter2.py` | `_fase2_variants.json` → `_fase2_survivors.json` (104 genes) + `_fase2_flat.json` (509 vars) | dedup por posición; ambos outputs existen |
| 2.3 Anotación gnomAD v4 | `fase2_gnomad.py` | `_fase2_flat.json` → `_fase2_gnomad.json` | **307 nuevas anotadas**; `_f2g.out`="anotadas nuevas: 307"; `_f2g.err` vacío (sin errores) |
| 2.4 Filtro de frecuencia | (gnomAD AF/AC/AN) | `_fase2_gnomad.json` | 299 presentes + **8 ausentes** → candidatas raras |

### Variante ausente en gnomAD con re-evaluación funcional (Fase 3-A)

> **Corrección respecto al barrido inicial:** el pipeline inicial clasificó LZTR1 22:20996720 como `downstream_gene_variant` (no codificante). La re-evaluación individual de VEP (Fase 3-A) revela que es **`stop_gained` (LoF, HIGH)** en los transcritos canónicos de LZTR1 (ENST00000646124, ENST00000700578, ENST00000888029-032…), un hallazgo de alta impacto en un gen supresor tumoral (neurofibromatosis tipo 2, NF2). Se documenta como hallazgo secundario/incidental, NO como driver de MVA (el fenotipo del probando no es compatible con NF2; el driver confirma MVA1 via BUB1B).

| Variante | Gen | Panel | Interpretación |
|---|---|---|---|
| **15:40220612 T>G** | **BUB1B** | MVA | **Nuestra variante primaria** p.Asn1002Lys — missense en dominio quinasa (MODERATE, SIFT=deleterious, PolyPhen=probably_damaging, AlphaMissense 0.923) ✅ |
| **22:20996720 C>G** | **LZTR1** | panel2 | **stop_gained (LoF, HIGH)** — hallazgo secundario NF2, NO driver MVA ⚠️ |
| 5:256828 C>T | SDHA | SAC | Gen mitocondrial/SAC; sin correlato con fenotipo |
| 12:68743447 C>T | NUP107 | panel2 | Nucleoporina; sin correlato con fenotipo MVA |
| 1:201365254 G>A | TNNT2 | panel2 | Cardiomiopatía; fuera del cluster clínico |
| 21:43053757 G>C / 21:43065240 G>A | CBS | panel2 | Homocistinuria; fuera del cluster |
| 22:20998981 C>G | LZTR1 | panel2 | downstream_gene_variant (MODIFIER) — no funcional |

**Conclusión de exclusión:** de las 8 variantes ausentes, las únicas con relevancia funcional son **BUB1B 15:40220612** (missense causal MVA1) y **LZTR1 22:20996720** (LoF secundario, NF2). Las otras 6 están en genes sin correlato clínico con el cluster del probando y fueron evaluadas como no-causales.

---

## Resultado consolidado

- **No queda co-causalidad pendiente** en los paneles ampliados (SAC 24 genes, panel cancer/renal
  67–71 genes, ACMG SF3 53 genes).
- El diagnóstico queda sustentado como **BUB1B compound-het causa única**, Fases 1 y 2 cerradas y
  reproducibles desde `src/` + `data/`.

**Artefactos:** `docs/CHECKLIST_FASE1.md`, `docs/diagnostico_mva.md`, `docs/comparativa_participantes.md`,
`data/results/vcf_exonic_variants.txt` (hallazgo), `data/results/vcf_sac_panel_variants.txt`,
`data/results/vcf_panel2_variants.txt`, `data/results/vcf_acmg_scan.txt`.

---

## Fase 3 — Predicción funcional y análisis de enriquecimiento de rutas ✅

### F3-A: Clasificación de impacto de VUS (`src/fase3_impacto.py`)

Consulta Ensembl VEP REST (POST `/vep/human/region` con input VCF) para cada variante candidata. Clasifica por consecuencia, impacto, SIFT/PolyPhen/AlphaMissense y ubicación en dominio funcional.

| Variante | Gen | Consecuencia | Impacto | SIFT | PolyPhen | Dominio funcional |
|---|---|---|---|---|---|---|
| 15:40220612:T>G | BUB1B | missense_variant | MODERATE | deleterious | probably_damaging | **Seg/Thr kinase Cat.** (prot 1002) ✅ |
| 22:20996720:C>G | LZTR1 | stop_gained | HIGH | — | — | — (LoF) ⚠️ |
| 1:201365254:G>A | TNNT2 | synonymous_variant | LOW | — | — | — |
| 5:256828:C>T | SDHA | 3_prime_UTR_variant | MODIFIER | — | — | — |
| 12:68743447:C>T | NUP107 | 3_prime_UTR_variant | MODIFIER | — | — | — |
| 21:43053757:G>C | CBS | 3_prime_UTR_variant | MODIFIER | — | — | — |
| 21:43065240:G>A | CBS | synonymous_variant | LOW | — | — | — |
| 22:20998981:C>G | LZTR1 | downstream_gene_variant | MODIFIER | — | — | — |

**AlphaMissense** (BUB1B N1002K): 0.9229 (pathogenic, reporte previo `PREDICCION_IMPACTO_PROTEINAS.md`).
**Conclusión F3-A:** la única variante con impacto funcional MODERATE/HIGH *en dominio activo* es **BUB1B 15:40220612** (quinasa ser/thr, residuo 1002). LZTR1 22:20996720 es LoF (HIGH) pero en gen distinto al fenotipo MVA (NF2, hallazgo secundario).

### F3-B: Enriquecimiento de rutas e interacción proteica (`src/fase3_enrichment.py`)

Consulta STRING API (`string-db.org/api/json`) para la red del Spindle Assembly Checkpoint y enriquecimiento funcional.

**Red del checkpoint (BUB1B + core):** 45 aristas con score ≥400. BUB1B es hub central:
- BUB1B–BUB1: 0.999 · BUB1B–MAD2L1: 0.999 · BUB1B–BUB3: 0.999 · BUB1B–CDC20: 0.999
- BUB1B–PLK1: 0.999 · BUB1B–AURKB: 0.999 · BUB1B–TTK: 0.991 · BUB1B–MAD1L1: 0.993 · CENPE–BUB1B: 0.999

**Vías significativamente enriquecidas** (FDR corregido):
| Vía | Fuente | FDR | Genes |
|---|---|---|---|
| Regulation of sister chromatid separation at metaphase-anaphase transition | WikiPathways WP4240 | 6.97e-17 | 7 |
| Cell cycle | KEGG hsa04110 | 3.79e-14 | 8 |
| Cell cycle | WikiPathways WP179 | 4.86e-09 | 6 |
| Oocyte meiosis | KEGG hsa04114 | 4.07e-07 | 5 |

**Co-candidatos vs checkpoint:** `co_candidatos_en_checkpoint = []` — los co-candidatos (TNNT2, SDHA, NUP107, CBS, LZTR1) NO interactúan con la red del checkpoint.

**Conclusión F3-B:** BUB1B es el hub central del Spindle Assembly Checkpoint; las vías enriquecidas (metaphase-anaphase transition, cell cycle) coinciden exactamente con el fenotipo MVA (disregulación mitótica). Los co-candidatos de Fase 2 NO comparten vía con BUB1B → confirma que la cascada alterada es exclusivamente la del checkpoint de BUB1B.

### Salida Fase 3
- `data/results/fase3_impacto.txt` (JSON: clasificación funcional)
- `data/results/fase3_enrichment.json` (JSON: red, vías, co-candidatos, conclusión)

---

## Fase 4 — Descubrimiento terapéutico y reposicionamiento ✅

**Objetivo:** vincular los genes/proteínas patógenos de Fase 3 con bases de datos de farmacología abierta
(Open Targets Platform, DrugBank) y redactar hipótesis de tratamiento con análisis farmacocinético
preliminar pediátrico (barreras fisiológicas, maduración CYP, dosis/formulación).

### F4-A: Mapeo de blancos a Open Targets (`src/fase4_mapeo_blancos.py`)

Consulta la **API GraphQL pública de Open Targets Platform v4** para los **10 genes del SAC**
(BUB1B + interactores STRING ≥0.99 de Fase 3): `tractability` + `drugAndClinicalCandidates`.

| Resultado | Valor |
|---|---|
| Blancos con fármacos clínicos | **3/10** (PLK1=8, AURKB=18, TTK=2) |
| Blancos "undrugged" (incl. **BUB1B causal**) | **7/10** |
| Fármacos de última etapa (Fase III+) | 3 — **todos inhibidores** (volasertib, ibcasertib, AT-9283) |
| Concernencia Open Targets → hipótesis | Ningún modulador por **activación**; los fármacos del SAC son **inhibidores antimitóticos** |

**Hallazgo clave:** BUB1B es "undrugged" (0 candidatos clínicos). Todos los fármacos que modulan los
interactores del SAC son **inhibidores** de quinasas mitóticas → en un probando con **BUB1B-LoF** agravarían
la aneuploidía → **confirmación empírica** del guardrail / lista de contraindicaciones del Track 2
(volasertib, BAY-1161909, taxanos, vincristina…).

### F4-B: Hipótesis de tratamiento (LLM + integración experta)

- **Candidato 1 — NMN/NAD+**: rescate de **dosificación de BUBR1** vía SIRT2 (K668); única estrategia con
  evidencia in vivo de elevar la proteína afectada (Baker 2013; North 2014). PK: cruza BBB, no sustrato CYP.
- **Candidato 2 — Senolíticos** (dasatinib+quercetina): clearance de senescencia progeroide, solo bajo oncología.
- **Candidato 3 — GH**: manejo estándar del retraso de crecimiento (supportive).
- **Descartados por rigor**: bortezomib, carfilzomib, palbociclib, selinexor, nab-paclitaxel (estrés
  mitótico no compensable + falta de respaldo funcional en BUB1B-LoF).

**Artefactos:** `src/fase4_mapeo_blancos.py`, `data/results/fase4_mapeo_blancos.json`,
`deliverables/track4/FASE4_REPOSICIONAMIENTO.md`, `deliverables/track2/video_script.md` (guion 3 min).

### F4-C: Validación in-silico de farmacomoduladores (`src/fase4_validacion_farmacos.py`)

Cruza **ChEMBL (MOA oficial)** + **PubMed (E-utilities)** para verificar la clase de los compuestos que
tocan el SAC:

| Blanco | Compuestos con MOA | Anotados INHIBIDOR |
|--------|--------------------|--------------------|
| BUB1B/BUB1/BUB3/CDC20/CENPE/MAD | **0 (undrugged)** | — |
| PLK1 (CHEMBL3024) | 8 | 8/8 |
| AURKB (CHEMBL2185) | 9 | 9/9 |
| TTK/MPS1 (CHEMBL3983) | 2 | 2/2 |

PubMed: `"PLK1 inhibitor"+arresto (91)`, `"MPS1 inhibitor"+4N (4)`, `"Aurora B inhibitor"+arresto (5)`,
`"CENP-E inhibitor"+congression (4)`, BUB1B+antimitótico (132).

**Conclusión validada:** todos los compuestos anotados contra quinasas SAC son `INHIBITOR` (antimitóticos);
ningún fármaco modula el SAC por activación → en MVA1 quedan descartados como tratamiento (guardrail
confirmado en 3 bases de datos), y el candidato reposicionable real es el eje de restauración de dosis
de BUBR1 (NMN/NAD+→SIRT2). Protocolo wet-lab (FACS/PI 4N, IF-pH3, time-lapse) documentado para validar
corrección de CIN o muerte selectiva de aneuploides.

**Artefactos:** `src/fase4_validacion_farmacos.py`, `data/results/fase4_validacion_farmacos.json`,
`data/results/_f4_val_pubmed.txt`, `deliverables/track4/FASE4_VALIDACION_PROTOCOLO.md`.
