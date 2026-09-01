import requests, io, json, time
# Panel de 2nd pass: predisposicion tumor pediatrico/sarcoma + genes renales/nefrocalcinosis
# + genes de inestabilidad cromosomica no cubiertos
genes = [
 # predisposicion a cancer/sarcoma pediatrico
 'LZTR1','NF1','DICER1','SMARCB1','SMARCA4','HRAS','KRAS','NRAS','FGFR1','ALK',
 'PTCH1','SUFU','GPC3','TSC1','TSC2','WT1','CTNNB1','TP53','RB1','STK11',
 'DOCK8','SH2B3','MSH2','MLH1','MSH6','PMS2','EPCAM',
 # nefrocalcinosis / renal (parte del fenotipo)
 'CLCN5','CLCNKB','SLC12A1','KCNJ1','CASR','SLC34A1','SLC34A3','ATP6V0A4','SLC4A1',
 'ADCY10','TRPV5','TRPV6','CLDN16','CLDN19','HSD11B2','CYP11B1','CYP11B2',
 # inestabilidad cromosomica / checkpoint adicional
 'AURKA','AURKC','PLK4','CDK1','CCNB1','MAD2L2','REV7','TTK','NUP107','NUP133',
 'SGO1','SGO2','MIS12','NSL1','PMF1','DCTN1','BICD2','SPDL1','ZW10','BUBR1',
 'ESPL1','PDS5A','PDS5B','NIPBL','HDAC8'
]
# eliminar duplicados
genes = list(dict.fromkeys(genes))
# guardar progreso incremental
_saved = r'C:\starquake\hackathonmva\_panel2.json'
import os
panel={}
if os.path.exists(_saved):
    try: panel=json.load(open(_saved,encoding='utf-8'))
    except: panel={}

def canonical(gene):
    try:
        u='https://rest.ensembl.org/lookup/symbol/human/%s?content-type=application/json;expand=1'%gene
        d=requests.get(u,timeout=40).json()
        seq=d.get('seq_region_name'); start=d.get('start'); end=d.get('end')
        if not seq: return gene,None
        canon=[t for t in d.get('Transcript',[]) if t.get('is_canonical')]
        exons=sorted([(x['start'],x['end']) for x in canon[0].get('Exon',[])]) if canon else []
        return gene,{'chr':seq,'start':start,'end':end,'exons':exons,'nexons':len(exons)}
    except Exception as e:
        return gene,None

panel={}
out=io.StringIO()
for g in genes:
    if g in panel:
        continue
    name,info=canonical(g)
    if info: panel[name]=info
    json.dump(panel,open(_saved,'w',encoding='utf-8'))
    time.sleep(0.12)
json.dump(panel,open(r'C:\starquake\hackathonmva\_panel2.json','w',encoding='utf-8'),indent=2)
out.write('Resueltos %d/%d genes\n'%(len(panel),len(genes)))
for g in genes:
    out.write('  %r -> %s\n'%(g, 'OK  chr%s %d exons'%(panel[g]['chr'],panel[g]['nexons']) if g in panel else 'NO RESUELTO'))
open(r'C:\starquake\hackathonmva\_panel2_resolved.txt','w',encoding='utf-8').write(out.getvalue())
print(out.getvalue())
