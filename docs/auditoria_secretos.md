# Auditoría de Secretos — Repositorio MVA Hackathon 2026

**Fecha:** 2026-09-01
**Repositorio:** `https://github.com/bestpricegye-ai/mva-hackathon-2026` (privado)
**Estado:** ✅ LÍMPIO — sin secretos versionados

## Alcance

- Working tree completo (archivos trackeados y untrackeados, excluyendo `.git/`,
  `.venv/`, caches).
- Historial completo de git (`git rev-list --all` + `git grep` en cada commit).

## Patrones escaneados

`ghp_*` (tokens GitHub), `hf_*` (tokens Hugging Face), `AKIA/ASIA*` y
`aws_secret_access_key` (AWS), `BEGIN OPENSSH/RSA/EC/DSA PRIVATE KEY` (claves SSH),
`password|secret|api_key|token =` genéricos.

## Resultados

| Hallazgo | Ubicación | Veredicto |
|---|---|---|
| `HF_TOKEN=hf_AeyQ...` | `.env` (raíz) | ⚠️ Token REAL pero **NO versionado**; ignorado por `.gitignore:47` (`# Environments → .env`). Existe solo en disco local |
| `token = f"phase{i}"` | `src/fase4_mapeo_blancos.py` | ✅ Código legítimo (variable de fase), no un secreto |
| `ghp_*`, `hf_*`, `AKIA*`, claves SSH, `aws_secret_access_key` en historial | — | ✅ 0 hits en todos los commits |

## Observaciones

- `.env` no está en `git ls-files` y `git check-ignore` confirma la exclusión.
- No hay `.aws/credentials`, claves `id_ed25519/id_rsa` ni tokens en el repo.
- El token GitHub `ghp_*` quedó almacenado en el keyring de `gh` (fuera del repo);
  se recomienda **rotarlo/caducarlo al cierre del evento**.

## Acciones registradas

- [x] Escaneo working tree + historial (2026-09-01) — sin secretos versionados.
- [x] **Re-verificación pre-publicación** (2026-09-01) con `src/auditar_repo.py` v2:
  scan sobre **archivos trackeados** (los que se publicarían) + historial completo.
  Resultado: `tree=0 history=0` (exit 0). Discriminación de PII real (contexto
  identitario) para evitar falsos positivos de coordenadas genómicas, rsIDs, PMIDs,
  HPO/OMIM y IDs de fármacos.
- [ ] Hacer repo público al cierre del evento (`gh repo edit --visibility public`).
- [ ] Rotar token GitHub `ghp_*` al cierre.
- [ ] (Opcional) Rotar `HF_TOKEN` local en `.env`.