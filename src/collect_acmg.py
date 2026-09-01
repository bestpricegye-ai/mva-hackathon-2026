import gzip, io, json, requests, time, re
VCF=r'C:\starquake\hackathonmva\WGS_EX2312012_HGWCNDSX7.vcf.gz'
PANEL=json.load(open(r'C:\starquake\hackathonmva\_acmg_exons.json',encoding='utf-8'))
lookup={}
for gene,info in PANEL.items():
    ch=info.get('chr')
    if not ch: continue
    for (s,e) in info.get('exons',[]): lookup.setdefault(ch,[]).append((s,e,gene))
def find_genes(chrom,pos): return [g for (s,e,g) in lookup.get(chrom,[]) if s<=pos<=e]
# recopilar candidatos: hom-alt (1/1) o 1/2 o indels (ref!=alt len)
cands=[]
with gzip.open(VCF,'rt') as f:
    for line in f:
        if line.startswith('#'): continue
        c=line.split('\t')
        if len(c)<9: continue
        chrom,pos=c[0],int(c[1])
        genes=find_genes(chrom,pos)
        if not genes: continue
        fmt=c[8].split(':'); ss=c[9].split(':')
        d=dict(zip(fmt,ss))
        gt=d.get('GT','.')
        if gt=='1/1' or gt=='1/2' or gt=='.' or len(c[3])!=len(c[4]):
            for g in genes: cands.append((g,chrom,pos,c[3],c[4],gt,d.get('DP','.')))
# dedup y guardar
uniq={}
for g,ch,pos,ref,alt,gt,dp in cands:
    uniq.setdefault((ch,pos,ref,alt),{'genes':[],'gt':gt,'dp':dp})
    uniq[(ch,pos,ref,alt)]['genes'].append(g)
recs=[{'chrom':k[0],'pos':k[1],'ref':k[2],'alt':k[3],'genes':v['genes'],'gt':v['gt'],'dp':v['dp']} for k,v in uniq.items()]
json.dump(recs,open('_acmg_cand.json','w',encoding='utf-8'),indent=1)
print('candidatos unicos:',len(recs))
