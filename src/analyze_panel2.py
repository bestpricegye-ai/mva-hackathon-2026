import gzip, io, json

VCF = r'C:\starquake\hackathonmva\WGS_EX2312012_HGWCNDSX7.vcf.gz'
PANEL = json.load(open(r'C:\starquake\hackathonmva\_panel2.json', encoding='utf-8'))

lookup = {}
for gene, info in PANEL.items():
    chr = info.get('chr')
    if not chr: continue
    for (s, e) in info.get('exons', []):
        lookup.setdefault(chr, []).append((s, e, gene))

def find_genes(chrom, pos):
    return [g for (s, e, g) in lookup.get(chrom, []) if s <= pos <= e]

results = {}
# recuento bruto: cuantas variantes caen en exones del panel
with gzip.open(VCF, 'rt') as f:
    for line in f:
        if line.startswith('#'): continue
        c = line.split('\t')
        if len(c) < 9: continue
        chrom, pos = c[0], int(c[1])
        genes = find_genes(chrom, pos)
        if not genes: continue
        fmt = c[8].split(':'); ss = c[9].split(':')
        d = dict(zip(fmt, ss))
        rec = {'pos': pos, 'ref': c[3], 'alt': c[4], 'gt': d.get('GT','.'),
               'ad': d.get('AD','.'), 'dp': d.get('DP','.'), 'filter': c[6], 'qual': c[5]}
        for g in genes:
            results.setdefault(g, []).append(rec)

out = io.StringIO()
out.write("FILTRADO PANEL2 (Track 1): variantes exonicas en genes de predisposicion a cancer/renal/inestabilidad cromosomica\n")
out.write("="*100+"\n\n")
total=0
for g in sorted(results):
    v = results[g]; total += len(v)
    # marcar candidatos: homocigotos alternas (1/1) o indels o baja DP no balanceada
    cand = [r for r in v if r['gt']=='1/1' or (len(r['ref'])!=len(r['alt'])) or r['gt']=='.']
    out.write("### %s  (total %d, candidatos raros %d)\n" % (g, len(v), len(cand)))
    for r in v:
        marca = " <== CANDIDATO(RARO)" if (r['gt']=='1/1' or len(r['ref'])!=len(r['alt']) or r['gt']=='.') else ""
        out.write("   chr%s:%d %s>%s GT=%s AD=%s DP=%s%s\n" % (g, r['pos'], r['ref'], r['alt'], r['gt'], r['ad'], r['dp'], marca))
out.write("\n\nTOTAL variantes exonicas panel2: %d\n" % total)
open(r'C:\starquake\hackathonmva\vcf_panel2_variants.txt','w',encoding='utf-8').write(out.getvalue())
print(out.getvalue())
