#!/usr/bin/env bash
# =============================================================================
# PGE-MVA1 / Alert hook - notifica fallo de regresion (email/Slack/webhook).
# Reemplaza la implementacion por tu canal real (cosas.env, webhook, etc.).
#   arg1 = mensaje corto
# =============================================================================
set -uo pipefail
MSG="${1:-REGRESSION ALERT sin detalle}"
WEBHOOK="${REGRESSION_WEBHOOK:-}"

echo "[alert] $MSG" >&2

if [[ -n "$WEBHOOK" ]]; then
    curl -fsS -X POST -H 'Content-Type: application/json' \
        -d "{\"text\":\"[pge-mva1] $MSG\"}" "$WEBHOOK" >/dev/null 2>&1 \
        || echo "[alert] webhook fallo (no fatal)" >&2
fi

# Ejemplo email (descomenta y configura):
#   echo "$MSG" | mail -s "[PGE] Regresion VCF" equipo@lab.org
exit 0
