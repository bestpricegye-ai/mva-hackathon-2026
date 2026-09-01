# FASE 2 - Paso 1: Hard Filtering + recopilacion de variantes exonicas sobre union de paneles
import gzip, io, json, os
from config import VCF, resolve_panel, ROOT, RESULTS_DIR

def loadj(f):
    return json.load(open(f,encoding='utf-8')) if os.path.exists(f) else {}
# union de paneles
panels={'MVA':None,'SAC':loadj(resolve_panel('sac')),'panel2':loadj(resolve_panel('panel2')),'ACMG':loadj(resolve_panel('acmg'))}
lookup={}  # chrom -> [(start,end,gene,panel)]
for pname,p in panels.items():
    if not p: continue
    for gene,info in p.items():
        ch=info.get('chr')
        if not ch: continue
        for (s,e) in info.get('exons',[]):
            lookup.setdefault(ch,[]).append((s,e,gene,pname))
# genes MVA curados manualmente (chr coords ya usadas) - incluir si faltan
mva={ 'BUB1B':('15',39901037,40150001), 'CEP57':('11',95529035,95660231), 'TRIP13':('5',887203,914065)}
for gene,(ch,s,e) in mva.items():
    # solo si no esta ya en paneles
    if not any(g==gene for vals in lookup.values() for (_,_,g,_) in vals):
        lookup.setdefault(ch,[]).append((s,e,gene,'MVA'))

def find_genes(chrom,pos):
    return [(g,p) for (s,e,g,p) in lookup.get(chrom,[]) if s<=pos<=e]

# parametros de hard filtering
QUAL_MIN=30.0; DP_MIN=10; GQ_MIN=20
stats={'total_exonic':0,'pass_qual':0,'pass_depth':0,'pass_gq':0,'survivors':0}
results={}
with gzip.open(VCF,'rt') as f:
    for line in f:
        if line.startswith('#'): continue
        c=line.split('\t')
        if len(c)<9: continue
        chrom,pos=c[0],int(c[1])
        genes=find_genes(chrom,pos)
        if not genes: continue
        stats['total_exonic']+=1
        quals=float(c[5]) if c[5] not in ('.','') else 0.0
        fmt=c[8].split(':'); ss=c[9].split(':')
        d=dict(zip(fmt,ss))
        gt=d.get('GT','.'); dp=d.get('DP','0'); gq=d.get('GQ','0')
        try: dpv=int(dp or '0')
        except: dpv=0
        try: gqv=int(gq or '0')
        except: gqv=0
        # hard filters
        if quals < QUAL_MIN: continue
        stats['pass_qual']+=1
        if dpv < DP_MIN: continue
        stats['pass_depth']+=1
        if gqv < GQ_MIN: continue
        stats['pass_gq']+=1
        stats['survivors']+=1
        rec={'pos':pos,'ref':c[3],'alt':c[4],'gt':gt,'qual':round(quals,1),'dp':dpv,'gq':gqv,'ad':d.get('AD','.'),'filter':c[6]}
        for gene,pname in genes:
            results.setdefault(gene,[]).append(rec)
print('=== HARD FILTERING ===')
for k,v in stats.items(): print('  %s: %d'%(k,v))
print('  genes con supervivientes:',len(results))
json.dump(results,open(os.path.join(RESULTS_DIR,'fase2_hardfilter_variants.json'),'w',encoding='utf-8'))
# resumen por gen
tot=sum(len(v) for v in results.values())
print('  total variantes supervivientes (por gen):',tot)
