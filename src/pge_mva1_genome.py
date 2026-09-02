"""PGE-MVA1 / GenomeKernel: consume el VCF real (GRCh38) y la referencia hg38 para
generar los artefactos de edicion (donor HDR, primers de verificacion por amplicon)
y el reporte de fase/af reales. Las etapas de wet-lab (MD, ARN-seq, readthrough,
base editing) quedan enlazadas aqui como passos que consumen estos artefactos,
pero necesitan biobanco/HPC (documentado en el json de salida).
"""
import argparse
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "data", "results")
CACHE = os.path.join(ROOT, "data", "cache", "ucsc_hg38_context.json")

VCF_TXT = os.path.join(ROOT, "data", "results", "vcf_exonic_variants.txt")
GNOMAD = os.path.join(ROOT, "data", "results", "fase2_gnomad_completo.json")

EXON17 = "AAACCCTACTCAGTCACCATGGTGTTCACAGTATCGCAGACAGCTACTGAAGTCCCTACCAGAGTTAAGTGCCTCTGCAGAGTTGTGTATAGAAGACAGACCAATGCCTAAGTTGGAAATTGAGAAGGAAATTGAATTAG"


def parse_vcf_txt(path):
    """Devuelve {pos: {ref,alt,gt,ad,dp,qual,filter}} desde el txt de variantes exonicas."""
    res = {}
    head = None
    with open(path, encoding="utf-8") as f:
        for line in f:
            m = re.search(r"pos=(\d+)\s+([ACGT]+)>([ACGT]+)\s+GT=(\S+)\s+AD=(\S+)\s+DP=(\d+)\s+Q=([\d.]+)\s+FILTER=(\S+)", line)
            if m:
                res[m.group(1)] = {
                    "ref": m.group(2), "alt": m.group(3), "gt": m.group(4),
                    "ad": m.group(5), "dp": int(m.group(6)),
                    "qual": float(m.group(7)), "filter": m.group(8)}
    return res


def vaf(ad):
    try:
        a, b = (int(x) for x in ad.split(","))
    except Exception:
        return None
    return b / (a + b) if (a + b) else None


def donor_hdr(seq, off, ref, alt, arm5=30, arm3=30):
    """Muestra de donor HDR de hebra simple (ssDNA) centrado en el sitio editado."""
    left = seq[off - arm5:off]
    right = seq[off + 1:off + 1 + arm3]
    corrected = ref  # devolver la secuencia nativa (correccion a WT)
    return {"template_ssDNA": left + corrected + right,
            "left_homology_arm": left, "right_homology_arm": right,
            "edited_base_is_wt": corrected,
            "arm_lengths_nt": [arm5, arm3]}


def amplicon_primers(seq, site0, target_off, fwd_len=20, span=80):
    """Primers de verificacion (amplicon-PCR) que flanquean el sitio editado."""
    start = max(0, target_off - span // 2)
    fwd = seq[start:start + fwd_len]
    idx = start + span - fwd_len
    rev_rc = seq[idx:idx + fwd_len]
    comp = str.maketrans("ACGT", "TGCA")
    rev = rev_rc.translate(comp)[::-1]
    return {"chr": "chr15", "site": site0,
            "forward_5p_3p": fwd, "reverse_5p_3p": rev,
            "amplicon_span_nt": span}


def main():
    ap = argparse.ArgumentParser(prog="pge_mva1_genome")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("artifacts")
    args = ap.parse_args()

    vcf = parse_vcf_txt(VCF_TXT)
    ctx = json.load(open(CACHE, encoding="utf-8"))
    gnom = json.load(open(GNOMAD, encoding="utf-8"))
    gnom_key = {pos: (ref, alt) for pos, ref, alt in
                [(k.split(":")[1], k.split(":")[2].split(">")[0], k.split(":")[2].split(">")[1])
                 for k in gnom if k.startswith("15:")]}
    out = {"schema": "pge_mva1_genome_v1",
           "ensamblaje": "GRCh38/hg38 (GATK: GRCh38) - referencia real del VCF pull-down",
           "fuente_vcf": "WGS_EX2312012_HGWCNDSX7.vcf.gz -> vcf_exonic_variants.txt",
           "variantes": []}
    for site0, w in ctx["windows"].items():
        pos = int(site0.split(":")[1])
        offset = w["variant_offset_in_window"]
        seq = w["seq"]
        rec = vcf.get(str(pos))
        if not rec:
            print("AVISO: pos", pos, "no encontrada en VCF txt; uso datos del cache")
            rec = {"ref": w["vcf_ref"], "alt": w["vcf_alt"], "gt": "0/1",
                   "ad": "?,?", "dp": None, "qual": None, "filter": "N/A"}
        af_key = "15:%d" % pos
        gd = {"af": None, "found": False}
        for k, v in gnom.items():
            if k.startswith(af_key + ":"):
                gd = v
        donor = donor_hdr(seq, offset, w["vcf_ref"], w["vcf_alt"])
        pr = amplicon_primers(seq, site0, offset)
        entry = {
            "site": site0, "ref_hg38": w["vcf_ref"], "alt": w["vcf_alt"],
            "genotipo_vcf": rec["gt"], "ad_vcf": rec["ad"], "dp_vcf": rec["dp"],
            "vaf_observado": vaf(rec["ad"]), "qual": rec["qual"], "filter": rec["filter"],
            "gnomAD_af": gd.get("af"), "gnomAD_presente": gd.get("found"),
            "donor_hdr_ssDNA": donor,
            "primers_verificacion_amplicon": pr,
            "fase_in_trans": "REQUIERE_SEGREGACION_PARENTAL",
            "wet_lab_requerido": ["MD-µs (OpenMM/GROMACS FEP)", "ARN-seq alta profundidad",
                                  "readthrough reporter", "base/prime editing celular"],
        }
        out["variantes"].append(entry)
        a = donor["template_ssDNA"]
        print(site0, "VAF", entry["vaf_observado"], "AF_gnomAD", gd.get("af"))
        print("   donor", a[:25], "...", a[-25:], "len", len(a))
        print("   fwd", pr["forward_5p_3p"], "rev", pr["reverse_5p_3p"])

    out["nota_wetlab"] = ("Los pasos que consumen estos artefactos (MD-µs FEP del dominio quinasa, "
                          "ARN-seq para medir escape NMD, reportero readthrough, y edicion de bases en "
                          "linea celular del paciente) son WET-LAB/HPC y quedan fuera del entorno local; "
                          "los donors y primers aqui generados son los inputs reproductibles exactos.")
    out["fail_closed_escalonado"] = {
        "fase_in_trans": "BLOQUEO hasta segregacion parental",
        "edicion_celular": "BLOQUEO sin biobanco (iPSC/PBMC del paciente)",
    }
    with open(os.path.join(OUT, "pge_mva1_genome.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print("-> data/results/pge_mva1_genome.json")


if __name__ == "__main__":
    main()