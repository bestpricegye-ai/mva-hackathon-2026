# INFORME DE REPRODUCIBILIDAD — Pipeline de Análisis de Variantes (Fases 1–6)

**Proyecto:** MVA Hackathon 2026 · Team `byronzunigao` · **PGE-MVA1**
**Fecha:** 2026-09-02
**Objetivo:** ejecutar el proceso completo (Fase 1 → última fase) desde la extracción del VCF hasta
los entregables finales, y verificar que **los resultados y entregables son reproducibles
(idénticos byte a byte)**.

---

## 0. Método de verificación

1. Se **congelaron los fingerprints** SHA-256 (primeros 16 hex) de cada entregable *golden* ya
   versionado en git.
2. Se **re-ejecutó cada fase** mediante sus scripts de `src/` sobre el VCF real y las bases durante
   esta sesión.
3. Se **compararon** los hashes regenerados contra los golden.
4. Reproducible = el `git diff` de los entregables está **vacío** (ningún archivo versionado cambió
   tras la regeneración) + hashes idénticos.

Fuente primaria replicada: `WGS_EX2312012_HGWCNDSX7.vcf.gz` (GRCh38, 315 MB, índice tabix).

---

## 1. Resultado consolidado (matriz de reproducibilidad)

**VEREDICTO GLOBAL: 100% de los entregables computacionales se regeneraron IDÉNTICOS.**

| Fase | Script(s) ejecutado(s) | Entregable | Hash golden | Hash regenerado | IDÉNTICO |
|---|---|---|---|---|---|
| **1** | `analyze_exons.py` | `vcf_exonic_variants.txt` | `27bb0219a6b8a695` | `27bb0219a6b8a695` | ✅ SÍ |
| **1** | `analyze_sac_panel.py` | `vcf_sac_panel_variants.txt` | `01d6f3218f5cac83` | `01d6f3218f5cac83` | ✅ SÍ |
| **1** | `analyze_panel2.py` | `vcf_panel2_variants.txt` | `98e3a4dd9cd430a8` | `98e3a4dd9cd430a8` | ✅ SÍ |
| **1** | `scan_acmg.py` | `vcf_acmg_scan.txt` | `84eb9c17c945ab44` | `84eb9c17c945ab44` | ✅ SÍ |
| **1** | `verificacion_dirigida_vcf.py` | `docs/verificacion_dirigida_vcf.md` | (commit) | idéntico (`fc` sin diferencias) | ✅ SÍ |
| **2** | `fase2_hardfilter.py` | `fase2_hardfilter_variants.json` | `ab8cbc05cb847e83` | `ab8cbc05cb847e83` | ✅ SÍ |
| **2** | `fase2_hardfilter2.py` → `fase2_gnomad.py` → `consolidar_gnomad.py` | `fase2_gnomad_completo.json` | `c5b57d08924eab6d` | `c5b57d08924eab6d` | ✅ SÍ |
| **3** | `fase3_enrichment.py` (STRING) | `fase3_enrichment.json` | `66e8e0e846f7ac51` | `66e8e0e846f7ac51` | ✅ SÍ |
| **4** | `fase4_mapeo_blancos.py` (Open Targets) | `fase4_mapeo_blancos.json` | `e74ac54e6bdad8c1` | `e74ac54e6bdad8c1` | ✅ SÍ |
| **4** | `fase4_validacion_farmacos.py` (ChEMBL/PubMed) | `fase4_validacion_farmacos.json` | `1a0de8443c326f98` | `1a0de8443c326f98` | ✅ SÍ |
| **6** | `fase6_criterios_zhang.py` (local, cache UCSC) | `fase6_criterios_zhang.json` | `e8b17f9e0f706c93` | `e8b17f9e0f706c93` | ✅ SÍ |
| **6** | `fase6_elegibilidad.py` (local) | `fase6_elegibilidad.json` | `b4250948402c1870` | `b4250948402c1870` | ✅ SÍ |
| **6** | `fase6_zhang_influence.py` (local) | `fase6_zhang_influence.json` | `655bdfa402430345` | `655bdfa402430345` | ✅ SÍ |
| **PGE** | `pge_mva1.py selftest -n 2000 --seed 42` | `pge_mva1_selftest.json` | — | `61cab9bb44501285` (×2 runs idénticos) | ✅ SÍ |
| **PGE** | `pge_mva1.py nmd` / `phase` / `pge_mva1_genome.py` | `pge_mva1_*.json` | (commit) | sin cambios en git | ✅ SÍ |
| **TEST** | `tests/qc/test_integration.py` | framework | — | 6/6 PASS | ✅ SÍ |

**Confirmación decisiva:** `git status --porcelain` mostró **cero modificaciones** en todo archivo
versionado tras la regeneración. `git diff --stat` sobre los entregables: **vacío**.

---

## 2. Detalle por fase

### Fase 1 — Ingestión, fenotipado y anotación genómica (desde el VCF)
- **Origen:** leída directa del VCF `WGS_EX2312012_HGWCNDSX7.vcf.gz` (GRCh38, tabix indexado).
- **Regenerados:** los 4 txt (exonic, SAC, panel2, ACMG scan) de sus respectivos scripts. Todos
  **idénticos** a los golden.
- **Verificación dirigida** de chr15:40.19-40.23 Mb: 16 variantes; targets **L737Ter** (VAF 0.54,
  AD 21/25, DP 46) y **N1002K** (VAF 0.46, AD 15/13, DP 28) — `fc` sin diferencias contra el
  archivo previo a la regeneración.
- **Hallazgo corregido:** los 4 `analyze_*.py` que una auditoría previa marcó como "stubs de 11
  líneas con imports rotos" **ya fueron refactorizados** a módulos funcionales (rc=0) y son los
  productores reales de los txt de Fase 1.

### Fase 2 — Filtrado y exclusión de co-causalidad
- Cadena `hardfilter → hardfilter2 → gnomad → consolidar`. Ambos entregables **idénticos**.
- Nota: `fase2_gnomad.py` debe ejecutarse **desde la raíz del repo** (usa ruta relativa
  `_fase2_flat.json`); desde `src/` falla con `FileNotFoundError`. Documentado; sin impacto en el
  resultado (no altera entregables).

### Fase 3 — Predicción funcional y enriquecimiento
- `fase3_enrichment.json` **idéntico**. Un subagente reportó fallo DNS transitorio de
  `string-db.org`; re-ejecutado directamente, STRING respondió y el hash coincide
  (`66e8e0e846f7ac51`). La red del checkpoint (45 aristas; BUB1B hub con scores 0.999) y las vías
  enriquecidas (WP4240 FDR 6.97e-17, KEGG cell cycle FDR 3.79e-14) se reproducen.

### Fase 4 — Descubrimiento terapéutico y reposicionamiento
- `fase4_mapeo_blancos.json` y `fase4_validacion_farmacos.json` **idénticos** (Open Targets
  GraphQL, ChEMBL, PubMed E-utilities alcanzados; output función pura de las APIs, sin
  timestamps/random).

### Fase 6 — Terapia génica / elegibilidad (criterios Zhang)
- Los 3 JSON **idénticos**. Puramente locales (cache UCSC + `clinical_history.json` + datos
  estáticos) → reproducibilidad total.

### PGE / Ingeniería Genómica de Precisión
- `selftest` con semilla fija (seed=42) es **determinista**: dos ejecuciones → mismo hash
  `61cab9bb44501285`. `nmd`, `phase` y `genome` no cambiaron vs git.
- `tests/qc/test_integration.py` (framework Determinismo+Regresión): **6/6 PASS**, incluidos los
  casos de fallo forzado (drop/filter/order) que detienen.

---

## 3. Diagnóstico reproducido (salida estable en todas las ejecuciones)

- **Diagnóstico molecular:** BUB1B compound-heterocigoto (causa única MVA1, OMIM #257300).
  - `chr15:40209701 T>G` · c.2210T>G · p.Leu737Ter · stop_gained · PVS1 · ClinVar Pathogenic ·
    NMD-competente · AF gnomAD 3.29e-05
  - `chr15:40220612 T>G` · c.3006T>G · p.Asn1002Lys · missense · novel · AlphaMissense 0.923 ·
    dominio quinasa · AF 0
- **Exclusión de co-causalidad:** LZTR1 `22:20996720` LoF (hallazgo secundario NF2, no driver MVA).
- **Reposicionamiento:** NMN/NAD+→SIRT2 (dosificación BUBR1) · senolíticos · GH; **contraindicados**
  los anti-mitóticos (PLK1/AURKB/TTK = todos INHIBITOR según ChEMBL/Open Targets).
- **Elegibilidad terapia génica:** 95/100 (nivel ALTO) · PAM V · eficiencia ALTA · off-target
  pendiente de índice GRCh38.

---

## 4. Limitaciones y transparencia

- **Etapas dependientes de API externa (F3/F4):** reproducibles si la API devuelve datos
  consistentes. Existe un riesgo residual de *drift* futuro si Open Targets/STRING/ChEMBL/PubMed
  actualizan sus datos. Para blindar, está disponible el framework de regresión
  (`tests/qc/vcf_regression.py` + harness HPC) que detecta este drift automáticamente.
- **Fase 1 read-based (FASTQ):** no disponible en infraestructura (solo VCF) — documentado en
  `docs/decision_reads_no_analizados.md`; no afecta a la reproducibilidad de los entregables VCF.
- **Off-target CRISPOR:** pendiente del índice GRCh38 (751 MB) fuera del entorno local; no por
  no-determinismo sino por recurso.

---

## 5. Conclusión

El pipeline completo (Fases 1–6, PGE y framework de pruebas) es **reproducible**: ante el mismo
VCF GRCh38 y las mismas bases, **todos los entregables se regeneraron byte-identicos** a los
golden congelados en git (`git diff` vacío, hashes SHA-256 coincidentes 100%). El diagnóstico de
BUB1B compound-heterocigoto como causa única de MVA1 es estable en todas las ejecuciones.

*Fin del informe de reproducibilidad.*
