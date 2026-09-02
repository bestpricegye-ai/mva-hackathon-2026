# PGE-MVA1 · Testing Framework (Determinismo + Regresión) para Pipeline de Variantes VCF

Framework automatizado para asegurar que el pipeline de análisis de variantes (VCF de
biobanco + genoma secuenciado personalizado) sea **100% determinista** y **no sufra
regresiones** frente a su "Golden Dataset" sin autorización explícita.

## Entregables (los 4 pedidos)

| # | Entregable | Archivo | Estado |
|---|---|---|---|
| 1 | **Estrategia de Golden Dataset** (mini-VCF de prueba con controles patogénicos) | `golden_dataset.py` | ✅ ejecutado sobre datos reales (`golden_demo.json`) |
| 2 | **Configuración de Determinismo** (orden cromosomas, bgzip/tabix, hilos) | `determinism.py` | ✅ selftest OK |
| 3 | **Script de Validación** (compara salida vs basal, ignora fechas, CHROM/POS/REF/ALT/INFO/FILTER) | `vcf_regression.py` | ✅ integrado |
| 4 | **Integración HPC** (fail-stop + alerta en SLURM y PBS) | `sbatch_regression.sh`, `pbs_regression.sh`, `alert.sh` | ✅ |

**Prueba integral:** `python tests/qc/test_integration.py` → valida los 6 escenarios (PASS + 3 fallos forzados).

---

## 1 · Estrategia de Golden Dataset

**Regla de oro:** el *golden* se genera **una sola vez, se revisa por un humano, y se
congela en git**. Nunca se regenera en el pipeline. Es el origen de verdad.

### Cómo extraerlo

```bash
# Opción A — por región (cromosoma 21 completo, ordenado + indexado para HPC)
python tests/qc/golden_dataset.py extract \
    --vcf WGS.vcf.gz --region chr21 --out data/golden/gold_chr21.vcf.gz

# Opción B — subset de ~100 variantes con CONTROLES PATOGÉNICOS primero
python tests/qc/golden_dataset.py extract \
    --vcf WGS.vcf.gz --n 100 --controls controls_patogenicos.json \
    --out data/golden/gold_100.vcf.gz
```

`controls_patogenicos.json`:
```json
{"controls": [
  {"chrom":"chr15","pos":"40209701","ref":"T","alt":"G"},   // BUB1B L737Ter (PVS1)
  {"chrom":"chr15","pos":"40220612","ref":"T","alt":"G"}    // BUB1B N1002K (dominio quinasa)
]}
```

### Controles que DEBE contener
- **Patogénicos conocidos** (ej. L737Ter, N1002K) → el pipeline DEBE recuperarlos siempre.
- **Alelos comunes gnomAD** → el pipeline DEBE manejarlos de forma estable (no flapear).
- **Controles negativos / benignos** → para verificar que el filtrado no los infla.
- **Baja cobertura / FILTER no-PASS** → para validar el fail-closed.

### Demo ejecutada sobre datos reales
`golden_dataset.py demo` → `data/results/golden_demo.json`: golden con las 2 variantes
reales BUB1B, orden canónico, y **hash SHA-256** como sello de integridad.

---

## 2 · Configuración de Determinismo

Fuentes típicas de no-determinismo y su control (implementado en `determinism.py`):

| No-determinismo | Control | Evidencia |
|---|---|---|
| **Orden de cromosomas** | Contigs GRCh38 canónicos (`chr1..22,chrX,chrY,chrM`) + `sort_records` estable | `canonical_key`, selftest |
| **Compresión bgzip/tabix** | El pipeline SIEMPRE emite bgzip + índice tabix, nunca VCF plano sin indexar | `bgzip_index()` |
| **Hilos en paralelo al anotar** | `OMP_NUM_THREADS=1`, `OPENBLAS=1`, `VEP_NUM_THREADS=1`, `PYTHONHASHSEED=0`, `LC_ALL=C` | `DETERMINISTIC_ENV` |
| **Fechas en cabecera** (VEP/SnpEff `fileDate`) | `sterilize_header()` → `__STERILE__` | selftest |
| **Orden de registros / carreras** | dedup + sort canónico antes de escribir | selftest (4→3 filas) |

**Env deterministic** para lanzar subprocesos reales (VEP, SnpEff, bcftools):
```python
from determinism import run_deterministic
run_deterministic(["vep", "-i", "in.vcf", "-o", "out.vcf", "--fork", "1"])
```

---

## 3 · Script de Validación (Regresión)

`vcf_regression.py` compara la salida actual contra el **basal (golden)** de forma exacta:

- **Columnas esenciales comparadas:** `CHROM`, `POS`, `REF`, `ALT`, `INFO` (claves
  seleccionadas), `FILTER`.
- **Ignora (a propósito):** cabeceras `##` (incluidas fechas `fileDate`), el *orden interno*
  de claves dentro de un mismo campo `INFO`, y por defecto `QUAL`/`GT` (flags opcionales).
- **Detección de regresión:**
  - *Déficit* → una variante del golden se perdió (falta en la salida) ⛔ **FAIL**
  - *Exceso* → apareció una variante nueva sin cambio autorizado del golden/código/DB ⚠️ aviso
  - *Orden* → la salida ya no está en orden canónico (no-determinismo) ⛔ **FAIL**

```bash
python tests/qc/vcf_regression.py \
    --golden data/golden/gold_100.vcf.gz \
    --current data/results/variants_candidatas.vcf.gz \
    --require-info DP,AF,VEP \
    --json data/results/regression_report.json
echo $?     # 0=PASS, 1=FAIL(regresión), 2=error de invocación
```

Argumentos útiles:
- `--allow-lost CHROM:POS:REF>ALT;...` → variantes que *decisivamente* deben excluirse
  (p.ej. controles negativos), no cuentan como déficit.
- `--require-quality` / `--require-gt` → exige además igualdad en QUAL/GT (más estricto).

---

## 4 · Integración en HPC (fail-stop + alerta)

El patrón: **correr el pipeline sobre el golden, validar regresión, y si falla → `exit 1`
(detiene el job) + alerta**. El job de HPC NO produce entregables si el golden se rompió.

### SLURM
```bash
sbatch tests/qc/sbatch_regression.sh
```
Internamente (ver archivo):
```bash
set -euo pipefail
[[ -f "$GOLDEN" ]] || { alerta "golden faltante"; exit 1; }   # fail-closed
export OMP_NUM_THREADS=1 ...                                   # determinismo
run_pipeline.sh "$GOLDEN" "$OUTPUT"                            # tu pipeline real
python vcf_regression.py --golden "$GOLDEN" --current "$OUTPUT" --json "$REPORT"
RC=$?
[[ $RC -ne 0 ]] && { alerta "REGRESSION FAIL"; exit 1; }       # fail-stop + alerta
```

### PBS/Torque
```bash
qsub tests/qc/pbs_regression.sh
```
misma lógica (`exit 1` al fallar la regresión → el gestor marca el job como FAILED).

### Alerta (`alert.sh`)
Hook reemplazable por tu canal real: webhook Slack/Teams (env `REGRESSION_WEBHOOK`) o
`mail`. Se invoca con el mensaje de fallo. El script **nunca** enmascara un fallo de
regresión — solo lo notifica.

---

## Cómo probar el framework completo

```bash
python tests/qc/test_integration.py
```

Escenarios que cubre:
1. Determinismo selftest (orden canónico + dedup + sterilize fechas).
2. Pipeline stub sin mutación → **REGRESSION PASS**.
3. Mutación `drop` (pérdida de variante) → **FAIL** (job se detiene).
4. Mutación `filter` (FILTER alterado) → **FAIL**.
5. Mutación `order` (orden roto) → **FAIL** determinismo.

---

## Integración con el pipeline real del repo

Deliberadamente el framework es **agnóstico al pipeline** (`run_pipeline_stub.py` simula la
ejecución). Para usarlo con el pipeline real basta reemplazar el paso 3 del harness
(`sbatch_regression.sh`) por tu llamada real y proporcionar el mini-VCF golden. El resto
(determinismo, comparación, fail-stop) queda igual.
