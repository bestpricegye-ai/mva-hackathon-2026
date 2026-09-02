#!/usr/bin/env python3
"""
PGE-MVA1 / Pipeline stub (para el harness de HPC).
Simula la ejecucion del pipeline de variantes: lee el VCF golden de entrada y
produce el VCF de salida APLICANDO los filtros (calidad/cobertura/AF). Usado por
sbatch_regression.sh / pbs_regression.sh para poder probar el framework sin el
pipeline real.

Env MVA_STUB_MUTATION: si se define, el stub MUESTRA una regresion a proposito
(permite probar el fail-stop + alerta). Valores: none|drop|filter|info|order.
"""
import argparse
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from determinism import sort_records, canonical_key

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("in_vcf")
    ap.add_argument("out_vcf")
    ap.add_argument("--min-qual", type=float, default=0)
    ap.add_argument("--min-dp", type=int, default=0)
    ap.add_argument("--min-af", type=float, default=0.0)
    args = ap.parse_args()

    mut = os.environ.get("MVA_STUB_MUTATION", "none")

    with open(args.in_vcf, encoding="utf-8") as f:
        lines = f.readlines()
    recs = [l for l in lines if l and not l.startswith("#")]
    header = [l for l in lines if l.startswith("#")]

    # parsear INFO
    out_recs = []
    for l in recs:
        c = l.rstrip("\n").split("\t")
        info = dict(f.split("=", 1) for f in c[7].split(";") if "=" in f)
        keep = True
        q = float(c[5]) if c[5] != "." else 0
        if q < args.min_qual or float(info.get("DP", 0)) < args.min_dp \
           or float(info.get("AF", 0.0) if info.get("AF") else 0.0) < args.min_af:
            keep = False

        # mutaciones a proposito para probar el harness
        if mut == "drop" and c[0] == "chr15":
            keep = False
        if mut == "filter" and c[0] == "chr15":
            c[6] = "q10"
        if mut == "info" and c[0] == "chr15":
            dp = info.get("DP", "NA")
            c[7] = f"DP={dp};AF=0.99;EXTRA=MUTADO"
        if mut == "order" and c[0] == "chr15":
            # invertir orden a proposito -> fallo de determinismo
            out_recs.insert(0, c)
            continue
        if keep:
            out_recs.append(c)

    # orden canonico (determinismo); la mutacion 'order' simula un productor
    # externo (anotador paralelo) que NO garantiza orden -> debe quedar roto
    if mut == "order":
        out_recs_sorted = out_recs  # sin reordenar: simula no-determinismo
    else:
        out_recs_sorted = sort_records(out_recs)

    with open(args.out_vcf, "w", encoding="utf-8") as f:
        f.writelines(header)
        for c in out_recs_sorted:
            f.write("\t".join(c) + "\n")
    print(f"stub: {len(out_recs_sorted)} variantes emitidas; mutation={mut}")


if __name__ == "__main__":
    main()
