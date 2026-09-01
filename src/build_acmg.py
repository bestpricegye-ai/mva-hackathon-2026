import requests, json, time, os
acmg=json.load(open('_acmg_sf3.json',encoding='utf-8'))
_saved=r'C:\starquake\hackathonmva\_acmg_exons.json'
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
for g in acmg:
    if g in panel: continue
    name,info=canonical(g)
    if info: panel[name]=info
    json.dump(panel,open(_saved,'w',encoding='utf-8'))
    time.sleep(0.15)
json.dump(panel,open(_saved,'w',encoding='utf-8'),indent=2)
resolved=[g for g in acmg if g in panel]
print('ACMG SF3 exons resueltos: %d/%d'%(len(resolved),len(acmg)))
print('No resueltos:', [g for g in acmg if g not in panel])
