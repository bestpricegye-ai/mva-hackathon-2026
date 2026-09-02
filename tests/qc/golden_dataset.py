#!/usr/bin/env python3
"""
PGE-MVA1 / Golden Dataset Generator
====================================
Estrategia de "Golden Dataset" para un pipeline de analisis de variantes (VCF).

Objetivo:
  Extraer un mini-VCF de control (ej. cromosoma 21, o un subset de ~100 variantes
  conocidas con patogenicas de control) para evaluar el pipeline de forma rapida
  en el HPC sin reprocesar el WGS completo.

Principios:
  - EL GOLDEN NUNCA SE REGENERA: se congela en git una vez aceptado. Es el origen
    de verdad para las pruebas de regresion.
  - INCLUYE CONTROLES PATOGENICOS: variantes ClinVar P/LP y alelos comunes gnomAD
    para que el pipeline tenga "senuelos" conocidos que DEBEN aparecer (o excluirse)
    de forma estable.
  - DETERMINISTA: extraccion con ventana fija, semilla fija y orden canonicamente
    ordenado (seccion/ordenacion determinista).

Uso:
  python golden_dataset.py extract  --vcf WGS.vcf.gz --region chr21  --out gold_chr21.vcf.gz
  python golden_dataset.py extract  --vcf WGS.vcf.gz --n 100       --controls pm5.json --out gold_100.vcf.gz
  python golden_dataset.py demo     --out data/results/golden_demo.json
"""
import argparse
import hashlib
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RESULTS = os.path.join(ROOT, "data", "results")


# ---------------------------------------------------------------------------
# 1) Mini-VCF de prueba (region o subset con controles patogenicos)
# ---------------------------------------------------------------------------
def extract_region(vcf, region, out, bcftools="bcftools"):
    """Extrae una region (ej. chr21) y la ordena canonicamente (vcf-sort desc).
    Comprime con bgzip y indexa con tabix para reproducibilidad de hilos."""
    subprocess.run([bcftools, "view", "-r", region, "-O", "z", "-o", out + ".raw.gz", vcf],
                   check=True)
    subprocess.run([bcftools, "sort", "-O", "z", "-o", out, out + ".raw.gz"], check=True)
    subprocess.run([bcftools, "index", "-t", out], check=True)
    os.remove(out + ".raw.gz")
    return out


def extract_subset(vcf, out, controls_json, n=100, seed=0, provariants="python"):
    """Subset deterministico de ~n variantes: incluye controles patogenicos primero
    y completa con un muestreo semilla-fija del resto. La semilla fija es CLAVE
    para el determinismo."""
    rng = __import__("random").Random(seed)
    with open(controls_json, encoding="utf-8") as f:
        controls = json.load(f)["controls"]      # lista de "CHROM POS REF ALT"
    with open(vcf, encoding="utf-8") as f:
        lines = [l for l in f if l and not l.startswith("#")]
    # conservar solo las columnas esenciales en orden CHROM,POS
    def key(l):
        c = l.split("\t")
        return (c[0], int(c[1]))
    lines = sorted(set(lines), key=key)          # dedup + orden canonico
    chosen = []
    for c in controls:
        found = [l for l in lines if l.split("\t")[0] == c["chrom"]
                 and l.split("\t")[1] == c["pos"] and l.split("\t")[3] == c["ref"]
                 and l.split("\t")[4] == c["alt"]]
        if found:
            chosen.append(found[0])
    rest = [l for l in lines if l not in chosen]
    chosen.extend(rng.sample(rest, max(0, n - len(chosen))))
    # cabecera base (sin fechas de runtime)
    header = ("##fileformat=VCFv4.2\n"
              "##source=PGE-MVA1_golden\n"
              "##contig=<ID=chr21>\n"
              "#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\n")
    with open(out, "w", encoding="utf-8") as f:
        f.write(header)
        for c in sorted(chosen, key=key):
            f.write(c if c.endswith("\n") else c + "\n")
    return out


# ---------------------------------------------------------------------------
# 2) Golden almacen (frozen + fingerprint)
# ---------------------------------------------------------------------------
def fingerprint(vcf):
    """Hash SHA-256 del contenido NORMALIZADO (lineas no-# ordenadas). Sirve de
    'sello' del golden: si el pipeline regenera otra cosa, el hash cambia."""
    with open(vcf, "rb") as f:
        raw = f.read()
    body = b"\n".join(sorted(l for l in raw.split(b"\n")
                             if l and not l.startswith(b"#")))
    return hashlib.sha256(body).hexdigest()


def freeze(golden_vcf, meta):
    """Guarda el sello junto a metadatos de la version de DB/codigo usados."""
    rec = {"fingerprint": fingerprint(golden_vcf), "meta": meta}
    out = os.path.join(RESULTS, "golden_dataset.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(rec, f, ensure_ascii=False, indent=2)
    return out


# ---------------------------------------------------------------------------
# 3) Demo: construye un golden a partir de los textos reales ya existentes
# ---------------------------------------------------------------------------
def demo(out_path):
    """Demo reproducible sobre el dataset real del repo (textos VCF derivados)."""
    vcf_txt = os.path.join(RESULTS, "vcf_exonic_variants.txt")
    variants = []
    with open(vcf_txt, encoding="utf-8") as f:
        for line in f:
            m = re.search(r"pos=(\d+)\s+(\w)>(\w)\s+GT=\S+\s+AD=(\S+)\s+DP=(\d+)\s+Q=([\d.]+)\s+FILTER=(\S+)", line)
            if m:
                variants.append({
                    "chrom": "chr15", "pos": int(m.group(1)),
                    "ref": m.group(2), "alt": m.group(3),
                    "gt": "0/1", "ad": m.group(4), "dp": int(m.group(5)),
                    "qual": float(m.group(6)), "filter": m.group(7)})
    # orden canonico: CHROM lexicografico, luego POS numerico (clave determinismo)
    variants.sort(key=lambda v: (v["chrom"], v["pos"]))
    rec = {
        "schema": "pge_mva1_golden_v1",
        "fuente": "vcf_exonic_variants.txt (WGS_EX2312012, GRCh38)",
        "n_variantes": len(variants),
        "variantes_orden_canonico": variants,
        "hash_canonico": hashlib.sha256(
            json.dumps(variants, sort_keys=True).encode()).hexdigest(),
        "control_patogenico_L737Ter": "chr15:40209701 T>G PVS1 NMD-competente",
        "control_patogenico_N1002K": "chr15:40220612 T>G novel, dominio quinasa",
        "nota_determinismo": ("orden canonico (CHROM lex, POS num); mismo VCF+DB => mismo "
                              "hash. Este golden se congela y NO se regenera."),
    }
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(rec, f, ensure_ascii=False, indent=2)
    return rec, out_path


def main():
    ap = argparse.ArgumentParser(prog="golden_dataset")
    sub = ap.add_subparsers(dest="cmd", required=True)
    pe = sub.add_parser("extract")
    pe.add_argument("--vcf", required=True)
    pe.add_argument("--region")
    pe.add_argument("--n", type=int, default=100)
    pe.add_argument("--controls")
    pe.add_argument("--out", required=True)
    pd = sub.add_parser("demo")
    pd.add_argument("--out", default=os.path.join(RESULTS, "golden_demo.json"))
    args = ap.parse_args()

    if args.cmd == "extract":
        if args.region:
            extract_region(args.vcf, args.region, args.out)
        else:
            extract_subset(args.vcf, args.out, args.controls, n=args.n)
        print("golden ->", args.out, "| fingerprint", fingerprint(args.out)[:16])
    else:
        rec, fp = demo(args.out)
        print("demo ->", fp)
        print("n_variantes", rec["n_variantes"], "| hash", rec["hash_canonico"][:16])
        for v in rec["variantes_orden_canonico"]:
            print("  ", v["chrom"], v["pos"], v["ref"], ">", v["alt"],
                  "DP=", v["dp"], v["filter"])


if __name__ == "__main__":
    main()
