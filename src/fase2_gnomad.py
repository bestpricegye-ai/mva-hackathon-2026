# FASE 2 - anotacion gnomAD de supervivientes faltantes
import json, requests, time, os
flat=json.load(open('_fase2_flat.json',encoding='utf-8'))
acmg=json.load(open('_acmg_gnomad.json',encoding='utf-8')) if os.path.exists('_acmg_gnomad.json') else {}
resume=json.load(open('_gnomad_resume.json',encoding='utf-8')) if os.path.exists('_gnomad_resume.json') else {}
SAVE=r'C:\starquake\hackathonmva\_fase2_gnomad.json'
res={}
if os.path.exists(SAVE):
    try: res=json.load(open(SAVE,encoding='utf-8'))
    except: res={}
# cache de conocidas
cache={}
for k,vv in acmg.items(): cache[k]=vv
for k,vv in resume.items():
    if all(x in vv for x in ('pos','ref','alt')):
        ch=str(vv.get('chrom','')).replace('chr','')
        cache["%s:%s:%s>%s"%(ch,vv['pos'],vv['ref'],vv['alt'])]=vv
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
    return [a for a in alt.split(',')] if ',' in alt else [alt]
todo=[]
for r in flat:
    k="%s:%s:%s>%s"%(r['chrom'],r['pos'],r['ref'],r['alt'])
    if k in cache or k in res: continue
    todo.append((k,r))
print('a anotar:',len(todo))
for k,r in todo:
    best=None
    for a in split_alt(r['alt']):
        q=query(r['chrom'].replace('chr',''),r['pos'],r['ref'],a)
        if q.get('af') is not None: best=q
    res[k]=best if best else {'af':None,'ac':None,'an':None,'found':False}
    json.dump(res,open(SAVE,'w',encoding='utf-8'))
    time.sleep(0.25)
print('anotadas nuevas:',len(res))
