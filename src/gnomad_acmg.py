import json, requests, time
recs=json.load(open('_acmg_cand.json',encoding='utf-8'))
SAVE=r'C:\starquake\hackathonmva\_acmg_gnomad.json'
import os
res={}
if os.path.exists(SAVE):
    try: res=json.load(open(SAVE,encoding='utf-8'))
    except: res={}
def query(ch,pos,ref,alt):
    q="query v($v:String!,$d:DatasetId!){variant(variantId:$v,dataset:$d){variantId genome{af ac an}}}"
    for attempt in range(6):
        try:
            r=requests.post('https://gnomad.broadinstitute.org/api/',json={'query':q,'variables':{'v':f"chr{ch}-{pos}-{ref}-{alt}",'d':'gnomad_r4'}},timeout=60)
            if r.status_code==429: time.sleep(8+attempt*5); continue
            if r.status_code!=200: time.sleep(4); continue
            j=r.json()
            try: g=(j['data'] or {}).get('variant',{}).get('genome')
            except Exception: g=None
            return {'af':g.get('af') if g else None,'ac':g.get('ac') if g else None,'an':g.get('an') if g else None,'found':bool(g)}
        except Exception: time.sleep(4)
    return {'af':None,'ac':None,'an':None,'found':False,'err':True}
def split_alt(alt):
    # manejar multi-alelios: consultar el primer alelo de referencia util y devolver lista
    if ',' in alt: return [a for a in alt.split(',')]
    return [alt]
for r in recs:
    key=f"{r['chrom']}:{r['pos']}:{r['ref']}>{r['alt']}"
    if key in res: continue
    alts=split_alt(r['alt'])
    best=None
    for a in alts:
        q=query(r['chrom'].replace('chr',''),r['pos'],r['ref'],a)
        if q.get('af') is not None: best=q
    res[key]=best if best else {'af':None,'ac':None,'an':None,'found':False}
    json.dump(res,open(SAVE,'w',encoding='utf-8'))
    time.sleep(0.3)
# resumen
rare=[ (k,v,r) for (k,v),r in zip(res.items(),recs) if v.get('af') is not None and v.get('af')<0.01 ]
print('anotados:',len(res),'de',len(recs))
print('RAROS <1%:',len(rare))
for k,v,r in rare:
    print('  RARO',r['genes'],k,'AF=%.5f'%v['af'],'AC=%s'%v.get('ac'),'GT=%s'%r['gt'])
errs=[k for k,v in res.items() if v.get('err')]
print('errores:',len(errs),errs)
