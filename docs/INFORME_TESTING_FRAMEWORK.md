# INFORME TÉCNICO — Marco de Pruebas Automatizado (Testing Framework)
## Determinismo y Regresión para el Pipeline de Análisis de Variantes (VCF)

**Autor:** Ingeniero de Software Bioinformático · Especialista en Genómica de Enfermedades Raras
**Proyecto:** PGE-MVA1 · Pipeline de variantes de biobanco (VCF WGS personalizado, GRCh38)
**Fecha:** 2026-09-02
**Estado:** ENTREGADO y VERIFICADO sobre el repositorio real (test de integración: 6/6 PASS)

---

## 0. Resumen ejecutivo

Se diseñó, implementó y **verificó en el repositorio** un framework de pruebas enfocado
exclusivamente en **Determinismo** y **Regresión** para el pipeline de análisis de variantes
(VCF). El framework garantiza dos propiedades críticas:

1. **Determinismo:** ante el mismo VCF de entrada y las mismas bases de datos, el pipeline
   identifica exactamente las mismas variantes y produce el mismo archivo final, controlando
   el orden de filas y la reproducibilidad de los filtros.
2. **Regresión:** cualquier actualización del código de filtrado, cambio en los scripts de
   priorización o actualización de las bases de anotación **no altera** los resultados
   históricos validados ("Golden Dataset") sin autorización explícita.

**Resultado de la prueba integral (`tests/qc/test_integration.py`):**
```
== 1) Determinism selftest            [OK]
== 2) Pipeline stub sin mutación      [OK] REGRESSION PASS
== 3) Salida == golden                [OK] PASS (n_golden==3, n_current==3, deficits==0, orden OK)
== 4) Mutación `drop`                 [OK] FAIL rc=1 (variante perdida ⇒ detener job)
== 5) Mutación `filter` (q10)         [OK] FAIL rc=1 (FILTER alterado)
== 6) Mutación `order`                [OK] FAIL rc=1 (orden roto ⇒ no-determinismo)
INTEGRATION TEST: TODO PASS
```

---

## 1. Contexto y objetivo

El pipeline procesa VCFs de un biobanco usando un genoma secuenciado personalizado, y ejecuta:
1. **Filtrado** de variantes (calidad, cobertura y frecuencia alélica).
2. **Anotación clínica** (VEP/SnpEff/Annovar con ClinVar y gnomAD).
3. **Priorización** de variantes candidatas para la enfermedad rara en estudio.

**Problema:** los resultados dependen de fuentes de no-determinismo (orden de cromosomas,
compresión, hilos de anotación, fechas de cabecera) y pueden **regresar silenciosamente**
al actualizar código o bases de datos, erosionando la confianza de los hallazgos clínicos.

**Objetivo:** un framework que haga la reproducibilidad **exigible** (no optativa) y la
detección de regresión **automática y bloqueante** (fail-stop en HPC).

---

## 2. Arquitectura del framework

```
├── tests/qc/
│   ├── golden_dataset.py        # [1] Estrategia Golden Dataset + fingerprint SHA-256
│   ├── determinism.py           # [2] Configuración de Determinismo (contigs/bgzip/hilos/fechas)
│   ├── vcf_regression.py        # [3] Script de Validación (comparador basal vs actual)
│   ├── sbatch_regression.sh     # [4] Harness HPC SLURM (fail-stop + alerta)
│   ├── pbs_regression.sh        # [4] Harness HPC PBS/Torque (fail-stop + alerta)
│   ├── alert.sh                 # Hook de alerta (webhook Slack/Teams / email)
│   ├── run_pipeline_stub.py     # Stub del pipeline (simula filtrado) para probar el framework
│   ├── test_integration.py      # Prueba integral (6 escenarios)
│   └── README.md                # Documentación operativa
└── data/results/golden_demo.json  # Golden real generado (variantes BUB1B + hash)
```

El framework es **agnóstico al pipeline**: `run_pipeline_stub.py` (o la llamada real en el
harness) es el único punto a sustituir por la ejecución real. Determinismo, comparación y
fail-stop permanecen idénticos.

---

## 3. Entregable 1 — Estrategia de "Golden Dataset"

### 3.1 Principios
- El **golden se genera una sola vez, se revisa por un humano y se congela en git**.
  Nunca se regenera en el pipeline.
- Incluye **controles patogénicos** conocidos (deben recuperarse siempre) y **controles
  negativos/benignos** (deben excluirse establemente).
- Su integridad se asegura con un **fingerprint SHA-256** del contenido normalizado.

### 3.2 Método de extracción (mini-VCF)
```bash
# Opción A — por región: cromosoma 21 completo (ordenado + bgzip + tabix para HPC)
python tests/qc/golden_dataset.py extract \
    --vcf WGS.vcf.gz --region chr21 --out data/golden/gold_chr21.vcf.gz

# Opción B — subset determinista de ~100 variantes con controles patogénicos primero
python tests/qc/golden_dataset.py extract \
    --vcf WGS.vcf.gz --n 100 --controls controls_patogenicos.json \
    --out data/golden/gold_100.vcf.gz
```
- Controles patogénicos BUB1B: `chr15:40209701 T>G` (L737Ter, PVS1) y `chr15:40220612 T>G`
  (N1002K, dominio quinasa).
- Determinismo: **semilla fija** (`seed=0`), deduplicación y **orden canónico**
  (CHROM lex + POS numérico) al extraer → el golden es reproducible byte a byte.

### 3.3 Verificación real
`golden_dataset.py demo` ejecutado sobre los datos reales del repo generó
`data/results/golden_demo.json`:
```
n_variantes 2 | hash 64a7f53a7d00f409
  chr15 40209701 T>G DP=46 PASS   (L737Ter, PVS1)
  chr15 40220612 T>G DP=28 PASS   (N1002K, dominio quinasa)
```
El hash canónico permite detectar cualquier alteración accidental del golden.

---

## 4. Entregable 2 — Configuración de Determinismo

Fuentes de no-determinismo y su control (implementado y probado en `determinism.py`):

| # | Fuente de no-determinismo | Control | Evidencia (selftest) |
|---|---|---|---|
| 1 | **Orden de cromosomas** | Contigs GRCh38 canónicos (`chr1..22, chrX, chrY, chrM`) + ordenamiento estable por `(canonical_key(CHROM), POS, REF, ALT)` | `chr1 < chr2 < chr10` |
| 2 | **Compresión bgzip / tabix** | El pipeline SIEMPRE emite VCF comprimido + indexado; nunca plano sin índice | `bgzip_index()` |
| 3 | **Hilos en paralelo al anotar** | `OMP_NUM_THREADS=1`, `OPENBLAS=1`, `MKL=1`, `VECLIB=1`, `VEP_NUM_THREADS=1`, `GATK_NUM_THREADS=1`, `PYTHONHASHSEED=0`, `LC_ALL=C` | `DETERMINISTIC_ENV` |
| 4 | **Fechas en cabecera** (VEP/SnpEff `fileDate`) | `sterilize_header()` → reemplaza por `__STERILE__` | `##fileDate=__STERILE__` |
| 5 | **Orden de registros / carreras de hilos** | dedup + sort canónico en la salida | `4 filas → 3` (dedup) |

```python
from determinism import run_deterministic
run_deterministic(["vep", "-i", "in.vcf", "-o", "out.vcf", "--fork", "1"])
```

---

## 5. Entregable 3 — Script de Validación (Regresión)

`tests/qc/vcf_regression.py` compara la **salida actual** contra el **basal (golden)**:

### 5.1 Qué compara (exacto)
- **Columnas esenciales:** `CHROM`, `POS`, `REF`, `ALT`, `INFO` (claves seleccionadas
  mediante `--require-info`, p.ej. `DP,AF,VEP`), `FILTER`.
- **Set de variantes:** toda variante del golden DEBE estar en la salida.
- **Orden canónico:** verifica determinismo del orden de filas.
- **INFO:** se parsea a claves y se comparan (permite reordenar claves internas sin falsa
  alarma, pero detecta cambios de valor).

### 5.2 Qué ignora (a propósito, configurable)
- **Cabeceras `##`** — incluida la eliminación de fechas (fileDate/source/contig).
- **Orden interno de claves** dentro de un mismo campo INFO/VEP (misma información).
- **QUAL y GT** — no bloquean por defecto (flags `--require-quality`, `--require-gt`).

### 5.3 Criterios de fallo (regresión)
- **Déficit** (variante del golden ausente en la salida) → **FAIL** ⛔ (se "perdió" algo).
- **Orden roto** (salida no canónica) → **FAIL** ⛔ (no-determinismo).
- **Exceso** (variante nueva sin cambio autorizado del golden/código/DB) → **aviso** ⚠️
  (requiere autorización explícita para aceptarse).
- `--allow-lost CHROM:POS:REF>ALT;...` permite declarar exclusiones legítimas (p.ej.
  controles negativos que el pipeline decide excluir) sin contar como déficit.

### 5.4 Códigos de salida
```
0 = PASS       1 = FAIL (regresión detectada; detener job)       2 = error de invocación/IO
```

```bash
python tests/qc/vcf_regression.py \
    --golden data/golden/gold_100.vcf.gz \
    --current data/results/variants_candidatas.vcf.gz \
    --require-info DP,AF,VEP --json data/results/regression_report.json
echo $?   # 0 / 1 / 2
```

### 5.5 Resultados verificados
| Escenario | rc | Observación |
|---|---|---|
| Salida == golden | 0 | PASS; `n_golden==3`, `n_current==3`, `deficits==0`, orden OK |
| Mutación `drop` (pérdida de variante) | 1 | déficits detectados para L737Ter, N1002K y control |
| Mutación `filter` (FILTER→q10) | 1 | cambio de FILTER reflejado |
| Mutación `order` (orden invertido) | 1 | `orden_canonico_ok=False` |

---

## 6. Entregable 4 — Integración en HPC (fail-stop + alerta)

### 6.1 Patrón
Corremos el pipeline **sobre el mini-VCF golden**, validamos la regresión, y si falla:
**`exit 1` (el job de HPC se detiene) + alerta** al responsable. El job nunca produce
entregables si el golden se rompió (principio *fail-closed*).

### 6.2 SLURM
```bash
sbatch tests/qc/sbatch_regression.sh
```
Internamente:
```bash
set -euo pipefail
[[ -f "$GOLDEN" ]] || { alerta "golden faltante"; exit 1; }      # fail-closed
export OMP_NUM_THREADS=1 ...                                      # determinismo
run_pipeline.sh "$GOLDEN" "$OUTPUT"                               # tu pipeline real
python vcf_regression.py --golden "$GOLDEN" --current "$OUTPUT" --json "$REPORT"
RC=$?
[[ $RC -ne 0 ]] && { alerta "REGRESSION FAIL"; exit 1; }          # fail-stop + alerta
```

### 6.3 PBS/Torque
```bash
qsub tests/qc/pbs_regression.sh
```
Misma lógica: `exit 1` al fallar ⇒ el gestor marca el job como FAILED.

### 6.4 Alerta (`alert.sh`)
Hook reemplazable por el canal real: **webhook Slack/Teams** (env `REGRESSION_WEBHOOK`) o
`mail`. Nunca enmascara un fallo de regresión, solo lo notifica. Así, un cambio en el código
de filtrado, en la priorización o en las bases de anotación que altere resultados históricos
validados **se detecta y bloquea automáticamente** hasta autorización explícita.

---

## 7. Prueba integral (evidencia de funcionamiento)

```bash
python tests/qc/test_integration.py
```
- **1. Determinismo selftest** → OK (orden canónico, dedup, sterilize fechas).
- **2. Stub sin mutación** → REGRESSION PASS.
- **3. Salida == golden** → PASS.
- **4. Mutación `drop`** → FAIL (pérdida de variante; detiene job).
- **5. Mutación `filter`** → FAIL (FILTER alterado).
- **6. Mutación `order`** → FAIL (no-determinismo de orden).

Todo `py_compile` en verde. **Verificación reproducida en el repositorio `mva-hackathon-2026`**
(commit del framework).

---

## 8. Integración con el pipeline real

El framework es agnóstico al pipeline. Para producción:
1. **Congelar** el mini-VCF golden en git (revisado por un humano).
2. Sustituir `run_pipeline_stub.py` (paso 3 del harness) por la llamada real del pipeline.
3. Configurar `GOLDEN`/`OUTPUT`/`REPORT`/`ALERT_CMD` como variables de entorno del job HPC.
4. Ejecutar el harness en cada release de código o cada actualización de bases (ClinVar/gnomAD).

Determinismo, comparación exacta y fail-stop quedan idénticos independientemente del pipeline
subyacente.

---

## 9. Limitaciones y transparencia

- `QUAL` y `GT` no se exigen por defecto (comparación mínima = CHROM/POS/REF/ALT/INFO/FILTER,
  como se solicitó); si la aplicación lo requiere, se activan con `--require-*`.
- El framework garantiza **reproducibilidad del pipeline**, no la veracidad clínica de las
  variantes; la priorización se valida contra los controles patogénicos del golden.
- El harness de HPC asume que `bcftools`/`bgzip`/`tabix` están disponibles en el entorno de
  cómputo; la comparación de regresión no depende de ellos (leer/gzip nativo).

---

## 10. Conclusiones

1. El framework **elimina el no-determinismo** (orden, compresión, hilos, fechas) mediante una
   capa de configuración determinista y un ordenamiento canónico verificable.
2. La **regresión se detecta automáticamente y bloquea el job** (fail-stop + alerta) ante
   pérdida de variantes, alteración de filtros o ruptura del orden — sin depender de la
   autorización manual tardía.
3. El mini-VCF golden con controles patogénicos permite **evaluar el pipeline en minutos en el
   HPC**, sin reprocesar el WGS completo.
4. Todo está **verificado en el repositorio** (`tests/qc/`, prueba integral 6/6 PASS) y es
   agnóstico al pipeline para uso en producción.

*Fin del informe.*
