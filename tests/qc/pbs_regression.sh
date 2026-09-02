#!/usr/bin/env bash
# =============================================================================
# PGE-MVA1 / HPC Regression Harness (PBS/Torque) - variante del SLURM
#   #PBS -N pge_regression
#   #PBS -l nodes=1:ppn=1,mem=8gb,walltime=02:00:00
# =============================================================================
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
GOLDEN="${GOLDEN:-$ROOT/data/golden/gold_100.vcf.gz}"
OUTPUT="${OUTPUT:-$ROOT/data/results/variants_candidatas.vcf.gz}"
REPORT="${REPORT:-$ROOT/data/results/regression_report.json}"

export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VEP_NUM_THREADS=1 PYTHONHASHSEED=0 LC_ALL=C

[[ -f "$GOLDEN" ]] || { echo "FATAL: golden faltante"; exit 1; }
python "$ROOT/tests/qc/run_pipeline_stub.py" "$GOLDEN" "$OUTPUT"
python "$ROOT/tests/qc/vcf_regression.py" --golden "$GOLDEN" --current "$OUTPUT" --json "$REPORT"
RC=$?
if [[ $RC -ne 0 ]]; then
    echo "REGRESION DETECTADA; job detenido. Ver $REPORT"
    exit 1
fi
echo "PASS"
exit 0
