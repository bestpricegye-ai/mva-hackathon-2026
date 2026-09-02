#!/usr/bin/env bash
# =============================================================================
# PGE-MVA1 / HPC Regression Harness (SLURM)
# =============================================================================
# Corre el pipeline de analisis de variantes sobre el golden subset y, si la
# prueba de REGRESION falla (se pierde una variante, cambia un filtro, o cambia
# el orden), DETIENE el job con exit != 0 y envia una ALERTA.
#
# Uso (SLURM):
#   sbatch tests/qc/sbatch_regression.sh          # flags internos abajo
#
# El patron "fail-stop + alerta" aplica a cualquier gestor; version PBS al final.
#
#SBATCH --job-name=pge_regression
#SBATCH --output=logs/regression_%j.out
#SBATCH --error=logs/regression_%j.err
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=8G
#SBATCH --time=02:00:00
set -euo pipefail

# --- rutas ------------------------------------------------------------------
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
GOLDEN="${GOLDEN:-$ROOT/data/golden/gold_100.vcf.gz}"      # mini-VCF congelado
OUTPUT="${OUTPUT:-$ROOT/data/results/variants_candidatas.vcf.gz}"
REPORT="${REPORT:-$ROOT/data/results/regression_report.json}"
ALERT_CMD="${ALERT_CMD:-./tests/qc/alert.sh}"               # hook de alerta (email/slack)
mkdir -p "$ROOT/logs" "$ROOT/data/golden"

# 1) Sanidad: el golden DEBE existir; si no, abortar (fail-closed).
if [[ ! -f "$GOLDEN" ]]; then
    echo "[HPC] FATAL: golden no existe -> $GOLDEN" | tee "$REPORT"
    [[ -x "$ALERT_CMD" ]] && "$ALERT_CMD" "REGRESSION ABORT: golden faltante $GOLDEN" || true
    exit 1
fi

# 2) Determinismo: fijar hilos y orden antes de anotar (VEP/SnpEff).
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VEP_NUM_THREADS=1
export PYTHONHASHSEED=0 LC_ALL=C LANG=C

# 3) Ejecutar el PIPELINE REAL sobre el subset golden (aqui tu pipeline).
echo "[HPC] pipeline sobre $GOLDEN ..."
#   Reemplaza por tu llamada real, p.ej.:
#   bash run_pipeline.sh "$GOLDEN" "$OUTPUT"
python "$ROOT/tests/qc/run_pipeline_stub.py" "$GOLDEN" "$OUTPUT" || {
    echo "[HPC] el pipeline fallo; job detenido" | tee "$REPORT"
    exit 1
}

# 4) REGRESION: compara salida contra golden basal.
echo "[HPC] validando regresion..."
python "$ROOT/tests/qc/vcf_regression.py" \
    --golden "$GOLDEN" --current "$OUTPUT" \
    --require-info DP,AF --json "$REPORT"
RC=$?

# 5) Fail-stop + alerta si regresion falla.
if [[ $RC -ne 0 ]]; then
    echo "[HPC] REGRESION DETECTADA: variante perdida / filtro alterado. Deteniendo job."
    echo "[HPC] ver resumen -> $REPORT"
    [[ -x "$ALERT_CMD" ]] && "$ALERT_CMD" "REGRESSION FAIL en $OUTPUT (ver $REPORT)" || true
    exit 1
fi

echo "[HPC] PASS: sin regresion. Golden intacto."
exit 0
