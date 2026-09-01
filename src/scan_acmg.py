import gzip, io, json
from config import VCF, resolve_panel, resolve_output

VCF  # noqa: F841 (path used for reproducibility, kept in config)
PANEL=json.load(open(resolve_panel('acmg'),encoding='utf-8'))
lookup={}
for gene,info in PANEL.items():
    ch=info.get('chr')
    if not ch: continue
    for (s,e) in info.get('exons',[]):
        lookup.setdefault(ch,[]).append((s,e,gene))
def find_genes(chrom,pos):
    return [g for (s,e,g) in lookup.get(chrom,[]) if s<=pos<=e]
results={}; total_in=0
with gzip.open(VCF,'rt') as f:
    for line in f:
        if line.startswith('#'): continue
        c=line.split('\t')
        if len(c)<9: continue
        chrom,pos=c[0],int(c[1])
        genes=find_genes(chrom,pos)
        if not genes: continue
        total_in+=1
        fmt=c[8].split(':'); ss=c[9].split(':')
        d=dict(zip(fmt,ss))
        rec={'pos':pos,'ref':c[3],'alt':c[4],'gt':d.get('GT','.'),'ad':d.get('AD','.'),'dp':d.get('DP','.'),'f':c[6]}
        for g in genes: results.setdefault(g,[]).append(rec)
out=io.StringIO()
out.write("BARRIDO EXOMA COMPLETO (Track exoma): variantes exonicas en genes accionables ACMG SF v3.0 (53 genes)\n")
out.write("="*100+"\n\n")
cand={}
for g in sorted(results):
    v=results[g]
    rare=[r for r in v if r['gt']=='1/1' or (len(r['ref'])!=len(r['alt'])) or r['gt']=='.']
    if rare: cand[g]=rare
    out.write("### %s (total %d, candidatos raros/indels %d)\n"% (g,len(v),len(rare)))
    for r in v[:40]:
        marca=" <== CAND" if (r['gt']=='1/1' or len(r['ref'])!=len(r['alt']) or r['gt']=='.') else ""
        out.write("   chr%s:%d %s>%s GT=%s AD=%s DP=%s%s\n"%(g,r['pos'],r['ref'],r['alt'],r['gt'],r['ad'],r['dp'],marca))
    if len(v)>40: out.write("   ...(+%d mas)\n"%(len(v)-40))
out.write("\n\nTOTAL variantes exonicas en genes ACMG: %d (en %d genes)\n"%(total_in,len(results)))
out.write("\n# CANDIDATOS RAROS/INDELS por gen (para anotacion gnomAD):\n")
for g,rr in sorted(cand.items()):
    for r in rr: out.write("%s\t%s:%d\t%s>%s\tGT=%s\n"%(g,g,r['pos'],r['ref'],r['alt'],r['gt']))
open(resolve_output('vcf_acmg_scan.txt'),'w',encoding='utf-8').write(out.getvalue())
print("variantes en genes ACMG:",total_in,"en",len(results),"genes")
print("genes con candidatos raros/indels:",list(cand.keys()))
print("total candidatos:",sum(len(v) for v in cand.values()))
