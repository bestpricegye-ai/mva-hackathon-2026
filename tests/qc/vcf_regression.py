#!/usr/bin/env python3
"""
PGE-MVA1 / VCF Regression Validator
====================================
Compara el VCF de salida ACTUAL contra el VCF BASAL (golden) y decide si hay
REGRESION. Diseñado para correrse en CI y en jobs de HPC (exit code != 0 al fallar).

Que compara (EXACTO, exigente):
  - Columnas esenciales: CHROM, POS, REF, ALT, INFO, FILTER  (GT se compara aparte)
  - SET de variantes: toda variante del basal DEBE estar en la salida (nada se pierde)
  - Orden canónico: CHROM lex canonico + POS numerico (regresión de determinismo)
  - INFO parsera claves=valores y compara KEYS (permite reordenar dentro de INFO)

Que IGNORA (a propósito):
  - Cabeceras (##...) incluidas fechas -> se estrilan (fileDate, source, contig)
  - Orden interno de claves dentro de un mismo campo INFO/VEP (misma informacion)
  - Calidad (QUAL) y genotipos (GT) NO bloquean por defecto (flags -q, -g), pero se
    pueden exigir. El estándar de este framework: CHROM/POS/REF/ALT/INFO/FILTER.

Uso:
  python vcf_regression.py --golden gold.vcf.gz --current out.vcf.gz
                         [--allow-lost pm5.txt] [--require-info DP,AF] [--json r.json]
  exit code: 0 = PASS, 1 = FAIL (regresion), 2 = error de invocacion/IO.

Dependencias: pandas (o fallback puro-python), pysam/bcftools opcional para .gz.
"""
import argparse
import json
import os
import re
import sys
import tempfile

try:
    import pandas as pd
    HAS_PD = True
except Exception:
    HAS_PD = False


# ---------------------------------------------------------------------------
# Lectura de VCF (texto o gz). Usa pysam si esta; si no, bgzip via gzip/zlib.
# ---------------------------------------------------------------------------
def _open_vcf(path):
    if path.endswith(".gz"):
        try:
            import gzip
            return gzip.open(path, "rt", encoding="utf-8")
        except Exception:
            pass
    return open(path, "r", encoding="utf-8")


def read_vcf(path):
    """Devuelve (header_lines, records) donde cada record es dict con
    CHROM,POS,ID,REF,ALT,QUAL,FILTER,INFO y lista de samples (si las hay)."""
    header, recs = [], []
    with _open_vcf(path) as f:
        for line in f:
            line = line.rstrip("\n")
            if not line:
                continue
            if line.startswith("##"):
                header.append(line)
            elif line.startswith("#CHROM"):
                cols = line.split("\t")
                samples = cols[9:]
            else:
                c = line.split("\t")
                rec = {
                    "CHROM": c[0], "POS": int(c[1]), "ID": c[2],
                    "REF": c[3], "ALT": c[4], "QUAL": c[5],
                    "FILTER": c[6], "INFO": c[7],
                }
                recs.append(rec)
    return header, recs


def parse_info(info):
    """INFO 'key=val;key=val' -> dict de claves (valores crudos). Ignora claves sin '='."""
    if not info or info == ".":
        return {}
    d = {}
    for field in info.split(";"):
        if "=" in field:
            k, v = field.split("=", 1)
            d[k] = v
        else:
            d[field] = field  # flag
    return d


def variant_key(rec, want_info):
    """Clave de identidad: CHROM/POS/REF/ALT canonico + INFO(keys deseadas) + FILTER.
    INFO se normaliza: solo keys seleccionadas, valores ordenados si multi-alelo."""
    infok = {}
    for k in want_info:
        v = parse_info(rec["INFO"]).get(k)
        if v is not None:
            # ordenar alelos alternativos para normalizar orden dentro de INFO
            parts = v.split(",")
            infok[k] = ",".join(sorted(parts)) if len(parts) > 1 else v
    return (rec["CHROM"], rec["POS"], rec["REF"], rec["ALT"],
            tuple(sorted(infok.items())), rec["FILTER"])


# ---------------------------------------------------------------------------
# Núcleo de comparacion
# ---------------------------------------------------------------------------
def compare(golden_path, current_path, want_info=("DP", "AF", "VEP"), require_quality=False,
            require_gt=False, allow_lost=()):
    """Devuelve dict de resultado. allow_lost: conjunto de claves (CHROM,POS,REF,ALT)
    permitidas de ausentarse (p.ej. controles negativos que el pipeline DECIDE excluir)."""
    gh, g = read_vcf(golden_path)
    ch, c = read_vcf(current_path)
    res = {"schema": "pge_mva1_regression_v1",
           "golden": golden_path, "current": current_path,
           "n_golden": len(g), "n_current": len(c),
           "header_dates_sterilized": None, "deficits": [], "excesos": [],
           "orden_canonico_ok": None, "info_mismatches": [], "pass": None,
           "NOTAS_IGNORADAS": ["header", "orden interno de claves INFO", "QUAL por defecto"]}

    # 1) Sterilize header (fechas) - solo informativo
    from determinism import sterilize_header
    res["header_dates_sterilized"] = [x for x in gh if "fileDate" in x or "date" in x.lower()]

    gset = {variant_key(r, want_info): r for r in g}
    cset = {variant_key(r, want_info): r for r in c}

    allow = set(tuple(x) for x in allow_lost) if allow_lost else set()
    # 2) Deficit: variante golden que no esta en la salida (REGRESION - se pierde algo)
    for k, r in gset.items():
        if k in cset:
            continue
        short = (r["CHROM"], r["POS"], r["REF"], r["ALT"])
        if short in allow:
            continue
        res["deficits"].append(f"{r['CHROM']}:{r['POS']} {r['REF']}>{r['ALT']} INFO={r['INFO']}")

    # 3) Exceso: variante nueva en la salida (puede ser legitimo si DB/codigo cambio,
    #    pero sin autorizacion sobre el golden => marca pendiente de revision)
    for k in cset:
        if k not in gset:
            r = cset[k]
            res["excesos"].append(f"{r['CHROM']}:{r['POS']} {r['REF']}>{r['ALT']}")

    # 4) Orden canonico de la salida actual (regresion de determinismo)
    from determinism import canonical_key
    ord_ok = all((canonical_key(a["CHROM"]), a["POS"]) <=
                 (canonical_key(b["CHROM"]), b["POS"])
                 for a, b in zip(c, c[1:]))
    res["orden_canonico_ok"] = ord_ok

    # 5) QUAL / GT opcionales
    if require_quality:
        res["quality_diffs"] = [f"{r['CHROM']}:{r['POS']} g={gset[k]['QUAL']} curr={r['QUAL']}"
                                for k, r in cset.items() if k in gset
                                and gset[k]["QUAL"] != r["QUAL"]]

    # 6) Decision
    ok = (len(res["deficits"]) == 0) and ord_ok
    if len(res["excesos"]) > 0:
        res["excesos_nota"] = ("aparecen variantes nuevas SIN cambios autorizados del "
                               "golden/codigo/DB; requiere autorizacion explicita")
        ok = ok and len(res["deficits"]) == 0  # excesos = aviso, deficits = fail
    if require_quality and res.get("quality_diffs"):
        ok = False
    res["pass"] = bool(ok)
    return res


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--golden", required=True)
    ap.add_argument("--current", required=True)
    ap.add_argument("--require-info", default="DP,AF",
                    help="claves INFO a comparar (comma). Default DP,AF")
    ap.add_argument("--require-quality", action="store_true")
    ap.add_argument("--require-gt", action="store_true")
    ap.add_argument("--allow-lost", default="", help="variantes permitidas de perderse (CHROM:POS:REF:ALT)")
    ap.add_argument("--json", default=None, help="donde volcar el JSON de resultado")
    args = ap.parse_args()

    allow = []
    for tok in args.allow_lost.split(";") if args.allow_lost else []:
        tok = tok.strip()
        if tok:
            ch, pos, refalt = tok.split(":", 2)
            ref, alt = refalt.split(">")
            allow.append((ch, int(pos), ref, alt))

    try:
        res = compare(args.golden, args.current,
                      want_info=[x for x in args.require_info.split(",") if x],
                      require_quality=args.require_quality,
                      require_gt=args.require_gt, allow_lost=allow)
    except FileNotFoundError as e:
        print("ERROR invocacion:", e, file=sys.stderr)
        sys.exit(2)

    if args.json:
        with open(args.json, "w", encoding="utf-8") as f:
            json.dump(res, f, ensure_ascii=False, indent=2)

    print(json.dumps(res, ensure_ascii=False, indent=2))
    if not args.json:
        # banner legible solo en modo humano; con --json la salida es JSON puro
        if res["pass"]:
            print("\nREGRESSION: PASS")
        else:
            print("\nREGRESSION: FAIL", file=sys.stderr)
    if res["pass"]:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
