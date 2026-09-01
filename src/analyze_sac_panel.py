import gzip, io, json
from config import VCF, resolve_panel, resolve_output

PANEL = json.load(open(resolve_panel('sac'), encoding='utf-8'))

# build lookup: (chrom -> [(start,end,gene)])
lookup = {}
for gene,info in PANEL.items():
    chr = info.get('chr')
    if not chr or chr in ('ERR','0',''): continue
    for (s,e) in info.get('exons',[]):
        lookup.setdefault(chr, []).append((s,e,gene))

def find_genes(chrom, pos):
    res=[]
    for (s,e,g) in lookup.get(chrom,[]):
        if s<=pos<=e:
            res.append(g)
    return res

results = {}
with gzip.open(VCF,'rt') as f:
    for line in f:
        if line.startswith('#'): continue
        c=line.split('\t')
        if len(c)<9: continue
        chrom=c[0]; pos=int(c[1]); ref=c[3]; alt=c[4]
        genes = find_genes(chrom,pos)
        if not genes: continue
        fmt=c[8].split(':'); ss=c[9].split(':')
        d=dict(zip(fmt,ss))
        rec={'pos':pos,'ref':ref,'alt':alt,'gt':d.get('GT','.'),'ad':d.get('AD','.'),'dp':d.get('DP','.'),'filter':c[6],'qual':c[5]}
        for g in genes:
            results.setdefault(g,[]).append(rec)

out=io.StringIO()
out.write("VARIANTES EXONICAS EN PANEL SAC (spindle assembly checkpoint) — excluye BUB1B/CEP57/TRIP13 ya analizados\n")
out.write("="*110+"\n")
total=0
for g in sorted(results):
    if g in ('BUB1B','CEP57','TRIP13'): continue
    v=results[g]; total+=len(v)
    out.write("\n### %s (%d variantes exonicas)\n"%(g,len(v)))
    out.write("-"*110+"\n")
    for r in v:
        out.write("  chr=x pos=%d %s>%s GT=%s AD=%s DP=%s FILTER=%s Q=%s\n"%(r['pos'],r['ref'],r['alt'],r['gt'],r['ad'],r['dp'],r['filter'],r['qual']))
out.write("\n\nTOTAL variantes exonicas en panel SAC (excl. MVA core): %d\n"%total)
open(resolve_output('vcf_sac_panel_variants.txt'),'w',encoding='utf-8').write(out.getvalue())
print(out.getvalue())
