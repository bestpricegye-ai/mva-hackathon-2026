import gzip, json, sys

VCF = r"C:\starquake\hackathonmva\WGS_EX2312012_HGWCNDSX7.vcf.gz"
REGION = (40_190_000, 40_230_000)
TARGETS = {40_209_701, 40_220_612}

variants = []
hits = []

with gzip.open(VCF, "rt", encoding="utf-8") as f:
    for line in f:
        if line[0] == "#":
            continue
        if not (line.startswith("chr15\t") or line.startswith("15\t")):
            continue
        col = line.rstrip("\n").split("\t")
        pos = int(col[1])
        if not (REGION[0] <= pos <= REGION[1]):
            continue
        rec = {
            "pos": pos, "id": col[2], "ref": col[3], "alt": col[4],
            "qual": col[5], "filter": col[6], "info": col[7],
            "format": col[8], "sample": col[9],
        }
        variants.append(rec)
        if pos in TARGETS:
            hits.append(rec)

report = []
report.append("# Verificación dirigida de la región chr15:40.19-40.23 Mb (VCF)\n")
report.append(f"Fuente: `WGS_EX2312012_HGWCNDSX7.vcf.gz` (GRCh38)\n")
report.append(f"Región analizada: chr15:40,190,000-40,230,000 — variantes: **{len(variants)}**\n")

for v in variants:
    fmt = v["format"].split(":")
    gt = dict(zip(fmt, v["sample"].split(":")))
    vaf = ""
    if "AD" in gt and "DP" in gt:
        ad = [int(x) for x in gt["AD"].split(",")]
        dp = int(gt["DP"])
        vaf = round(ad[1] / dp, 4) if dp and len(ad) > 1 else ""
    line = (f"- `{v['pos']} {v['ref']}>{v['alt']}` GT={gt.get('GT')} "
            f"AD={gt.get('AD')} DP={gt.get('DP')} VAF={vaf} "
            f"Q={v['qual']} FILTER={v['filter']} ID={v['id']}")
    if v["pos"] in TARGETS:
        line += "  **← TARGET**"
        report.append(f"\n### TARGET {line}\n")
    else:
        report.append(line)

with open(r"C:\starquake\hackathonmva\docs\verificacion_dirigida_vcf.md", "w", encoding="utf-8") as f:
    f.write("\n".join(report) + "\n")

print("variantes en region:", len(variants))
for h in hits:
    fmt = h["format"].split(":")
    gt = dict(zip(fmt, h["sample"].split(":")))
    print(h["pos"], h["ref"], ">", h["alt"], "GT=", gt.get("GT"), "AD=", gt.get("AD"), "DP=", gt.get("DP"), "Q=", h["qual"], h["filter"])