import gzip, sys, io
from config import VCF, resolve_output

# Candidate genes (GRCh38)
GENES = {
    'BUB1B': {'chrom': '15', 'start': 39901037, 'end': 40150001},
    'CEP57': {'chrom': '11', 'start': 95529035, 'end': 95660231},
    'TRIP13': {'chrom': '5',  'start': 887203,  'end': 914065},
}

out = io.StringIO()
def log(s):
    out.write(s + '\n')

log("== MVA CANDIDATE GENE VARIANT SCAN ==")
log("Sample: WGS_EX2312012  |  Build: GRCh38 (contig lengths)")

# parse header FORMAT
sample_idx = None
format_idx = None

found = {g: [] for g in GENES}
total_variants = 0
passed_variants = 0

with gzip.open(VCF, 'rt') as f:
    for line in f:
        line = line.rstrip('\n')
        if line.startswith('##'):
            continue
        cols = line.split('\t')
        if line.startswith('#CHROM'):
            header = cols
            # find sample column
            sample_idx = len(cols) - 1
            log("Columns: " + ", ".join(header))
            log("")
            continue
        if len(cols) < 9:
            continue
        chrom, pos_s, vid, ref, alt, qual, filt, info, fmt = cols[:9]
        total_variants += 1
        try:
            pos = int(pos_s)
        except ValueError:
            continue
        # check if in any candidate gene
        for gname, rng in GENES.items():
            if chrom == rng['chrom'] and rng['start'] <= pos <= rng['end']:
                sample = cols[sample_idx] if sample_idx < len(cols) else ''
                found[gname].append((pos, ref, alt, qual, filt, info, fmt, sample))
                break

log("Total variant records scanned: %d" % total_variants)
log("")

for gname in GENES:
    variants = found[gname]
    log("=" * 70)
    log("%s  (chr%s:%d-%d)  -> %d variant records" % (
        gname, GENES[gname]['chrom'], GENES[gname]['start'], GENES[gname]['end'], len(variants)))
    for pos, ref, alt, qual, filt, info, fmt, sample in variants:
        log("-" * 70)
        log("POS %d  REF=%s  ALT=%s  QUAL=%s  FILTER=%s" % (pos, ref, alt, qual, filt))
        log("  INFO: %s" % info)
        log("  FORMAT: %s" % fmt)
        log("  SAMPLE: %s" % sample)

with open(resolve_output('vcf_candidates.txt'), 'w', encoding='utf-8') as fo:
    fo.write(out.getvalue())
print("done")
print(out.getvalue())
