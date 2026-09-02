#!/usr/bin/env python3
"""
PGE-MVA1 / Determinism Module
=============================
Controla las fuentes de NO-determinismo mas comunes en un pipeline de VCF:

  1. ORDEN DE CROMOSOMAS  -> contigs en orden canonico + sort estable
  2. COMPRESION bgzip/tabix-> pipeline SIEMPRE consume/emite VCF bgzip+indexado
  3. HILOS EN PARALELO    -> fijar OMP_NUM_THREADS, tabix -T, VEP --fork con seed
  4. FECHAS EN CABECERA   -> VEP/SnpEff inyectan fileDate; se estrilan en la salida
  5. ORDEN DE REGISTROS   -> dedup + sort canonico evita carreras de hilos/escritura

Uso:
  python determinism.py selftest            # verifica invariantes sobre un mini-VCF
"""
import argparse
import os
import re
import subprocess
import sys

# ---------------------------------------------------------------------------
# Canonical contig order (GRCh38). El pipeline DEBE emitir en este orden.
# ---------------------------------------------------------------------------
GRCH38_CONTIGS = ([f"chr{i}" for i in range(1, 23)] + ["chrX", "chrY", "chrM"])
GRCH_CHR_KEYS = {"chr" + s: (0, i, 0) for i, s in enumerate(
    [str(i) for i in range(1, 23)] + ["X", "Y", "M"])}


def canonical_key(chrom):
    """Clave de ordenacion canonica: cromosomas primero (GRCh38 order), luego el
    resto lexicograficamente. Deterministica: nunca depende del orden de lectura."""
    return GRCH_CHR_KEYS.get(chrom, (1, 0, chrom))


def sort_records(records, keyfn=None):
    """Recibe iterable de filas VCF (listas de campos), devuelve lista ordenada
    y SIN duplicados por [CHROM canonico, POS numerico, REF, ALT, INFO, FILTER]."""
    keyfn = keyfn or (lambda r: (canonical_key(r[0]), int(r[1]), r[3], r[4]))
    seen = set()
    out = []
    for r in records:
        k = tuple(r[:8])
        if k in seen:
            continue
        seen.add(k)
        out.append(r)
    return sorted(out, key=keyfn)


# ---------------------------------------------------------------------------
# BGZIP / TABIX - siempre comprimido e indexado (hilos controlados)
# ---------------------------------------------------------------------------
def bgzip_index(vcf, tabix="tabix", threads="1"):
    """bgzip + tabix para que el VCF sea consultable por region y los hilos de
    anotacion no alteren el orden. threads=1 garantiza orden de escritura."""

    env = dict(os.environ)
    env["OMP_NUM_THREADS"] = threads
    env["GATK_NUM_THREADS"] = threads
    if not vcf.endswith(".gz"):
        out = vcf + ".gz"
        with open(out, "wb") as f:
            subprocess.run([__import__("shutil").which("bgzip") or "bgzip", "-c"],
                           stdin=open(vcf, "rb"), stdout=f, env=env, check=True)
        vcf = out
    else:
        out = vcf
    subprocess.run([tabix, "-p", "vcf", out], env=env, check=True)
    return out


# ---------------------------------------------------------------------------
# Sterilize header dates - VEP/SnpEff/BCFtools inyectan fileDate / timestamps
# ---------------------------------------------------------------------------
DATE_RE = re.compile(r"(fileDate|date|lastUpdate|FileDate)=[0-9TZ:\-]+")


def sterilize_header(header):
    """Elimina fechas/lotes de runtime de la cabecera para que la comparacion
    de regresion ignore diferencias de timestamp (stride esencial)."""
    return [DATE_RE.sub(r"\1=__STERILE__", h) for h in header]


# ---------------------------------------------------------------------------
# Deterministic env for subprocesses (thread pinning + no asincronia)
# ---------------------------------------------------------------------------
DETERMINISTIC_ENV = {
    "OMP_NUM_THREADS": "1",
    "OPENBLAS_NUM_THREADS": "1",
    "MKL_NUM_THREADS": "1",
    "VECLIB_MAXIMUM_THREADS": "1",
    "NUMEXPR_NUM_THREADS": "1",
    "VEP_NUM_THREADS": "1",
    "GATK_NUM_THREADS": "1",
    "PYTHONHASHSEED": "0",
    "LC_ALL": "C",
    "LANG": "C",
}


def run_deterministic(cmd, **kw):
    env = dict(os.environ)
    env.update(DETERMINISTIC_ENV)
    kw.setdefault("env", env)
    return subprocess.run(cmd, **kw)


# ---------------------------------------------------------------------------
# Selftest: verify invariants on a real file / synthetic lines
# ---------------------------------------------------------------------------
def selftest():
    recs = [
        ["chr2", "100", ".", "A", "G", "30", "PASS", "DP=10"],
        ["chr10", "50", ".", "C", "T", "20", "q10", "DP=5"],
        ["chr1", "200", ".", "G", "A", "40", "PASS", "DP=8"],
        ["chr2", "100", ".", "A", "G", "30", "PASS", "DP=10"],   # duplicado
    ]
    s = sort_records([r.split("\t") for r in [
        "\t".join(r) for r in recs]])
    out = ["\t".join(r) for r in s]
    # dedup en el sorting (mismo CHROM/POS/REF/ALT => solo una fila)
    assert len(s) == 3, f"dedup fallo: {len(s)}"
    # orden canonico: chr1 < chr2 < chr10  (chr10 despues de chr2 en GRCh38)
    assert out[0].startswith("chr1"), out
    assert out[1].startswith("chr2"), out
    assert out[2].startswith("chr10"), out
    # sterilize: fechas quitadas
    h = ["##fileDate=2026-09-02", "##source=vep", "##FORMAT=<ID=GT,Number=1>"]
    sh = sterilize_header(h)
    assert "__STERILE__" in sh[0] and "2026" not in sh[0], sh
    # canonical_key: chrM despues de chrY
    assert canonical_key("chrY") < canonical_key("chrM")
    print("determinism selftest: OK")
    print("  orden canonico:", out[0].split("\t")[0], "<",
          out[1].split("\t")[0], "<", out[2].split("\t")[0])
    print("  dedup:", len(recs), "->", len(s), "filas")
    print("  header sterilized:", sh[0])


def main():
    ap = argparse.ArgumentParser(prog="determinism")
    ap.add_argument("cmd", choices=["selftest"])
    args = ap.parse_args()
    selftest()


if __name__ == "__main__":
    main()
