import gzip, io, json

VCF = r'C:\starquake\hackathonmva\WGS_EX2312012_HGWCNDSX7.vcf.gz'

EXONS = {
    'BUB1B': [(40161069,40161255),(40165053,40165196),(40170062,40170121),(40170537,40170681),
              (40176477,40176673),(40183714,40183883),(40185165,40185379),(40185551,40185642),
              (40196545,40196774),(40199615,40199727),(40200244,40200359),(40200931,40200980),
              (40202405,40202465),(40202589,40202694),(40206184,40206458),(40208637,40208770),
              (40209635,40209775),(40210110,40210210),(40212499,40212648),(40213332,40213474),
              (40217496,40217667),(40218456,40218562),(40220564,40221123)],
    'CEP57': [(95790498,95790743),(95799232,95799388),(95812932,95813111),(95813468,95813589),
              (95817787,95817903),(95818827,95818904),(95821871,95821978),(95822499,95822576),
              (95827786,95828027),(95829187,95829331),(95831026,95832693)],
    'TRIP13': [(892884,893090),(894787,894952),(896665,896794),(900494,900549),(901341,901431),
               (904148,904220),(907130,907193),(907988,908074),(908355,908461),(911843,911996),
               (914465,914577),(915904,915973),(917008,918120)],
}
CHROM = {'BUB1B':'15','CEP57':'11','TRIP13':'5'}

def find_gene(chrom, pos):
    for g in EXONS:
        if chrom != CHROM[g]: continue
        for (s,e) in EXONS[g]:
            if s <= pos <= e:
                return g
    return None

results = {'BUB1B': [], 'CEP57': [], 'TRIP13': []}
with gzip.open(VCF, 'rt') as f:
    for line in f:
        if line.startswith('#'):
            continue
        c = line.split('\t')
        if len(c) < 9: continue
        chrom, pos_s, ref = c[0], c[1], c[3]
        alt = c[4]; qual = c[5]; filt = c[6]
        pos = int(pos_s)
        g = find_gene(chrom, pos)
        if g is None: continue
        fmt = c[8]; sample = c[9]
        ad = dp = gt = None
        ff = fmt.split(':')
        ss = sample.split(':')
        d = dict(zip(ff, ss))
        gt = d.get('GT','.')
        ad = d.get('AD','.'); dp = d.get('DP','.')
        results[g].append({
            'pos': pos, 'ref': ref, 'alt': alt, 'qual': qual,
            'filter': filt, 'gt': gt, 'ad': ad, 'dp': dp
        })

out = io.StringIO()
out.write("VARIANTES EN EXONES CANONICOS (BUB1B / CEP57 / TRIP13)\n")
out.write("=" * 100 + "\n")
total = 0
for g in EXONS:
    v = results[g]
    total += len(v)
    out.write("\n### %s  (%d variantes exonicas)\n" % (g, len(v)))
    out.write("-" * 100 + "\n")
    for r in v:
        out.write("pos=%d  %s>%s  GT=%s  AD=%s  DP=%s  Q=%s  FILTER=%s\n" % (
            r['pos'], r['ref'], r['alt'], r['gt'], r['ad'], r['dp'], r['qual'], r['filter']))

out.write("\n\nTOTAL variantes exonicas en 3 genes: %d\n" % total)

with open(r'C:\starquake\hackathonmva\vcf_exonic_variants.txt', 'w', encoding='utf-8') as fo:
    fo.write(out.getvalue())
print(out.getvalue())
