import requests, json, io, time

PANEL = json.load(open(r'C:\starquake\hackathonmva\_panel2.json', encoding='utf-8'))

# candidatos 1/1 renales: {gene: [(pos,ref,alt),...]} con chr real de PANEL
cand = {
 'CASR':  [(122284198,'G','C'),(122284985,'G','C'),(122285251,'A','T'),(122285765,'C','G'),
           (122287287,'T','C'),(122288033,'T','C'),(122289866,'T','C'),(122291061,'C','A'),
           (122291128,'G','A'),(122291137,'C','T')],
 'CLCN5': [(50081733,'A','G')],
 'CLCNKB':[(16046629,'A','G'),(16048038,'G','C'),(16048568,'C','G'),(16048569,'A','C'),
           (16049696,'C','T'),(16049824,'T','C'),(16053701,'T','C'),(16053748,'A','G'),
           (16053757,'C','T'),(16056953,'A','C'),(16057173,'T','G')],
 'SLC12A1':[(48288516,'T','C'),(48302995,'G','T'),(48303169,'A','G'),(48303969,'A','T')],
 'SLC34A3':[(137236154,'A','T')],
 'CLDN16':[(190411799,'T','A')],
 'CLDN19':[(42734855,'T','C')],
 'TRPV5':[(142908170,'A','T'),(142912583,'T','C'),(142925619,'A','G'),(142928154,'C','T'),(142928787,'A','G')],
 'TRPV6':[(142872464,'T','C')],
 'SLC4A1':[(44248890,'C','T')],
 'KCNJ1':[(128867293,'A','G')],
}

def query(ch,pos,ref,alt):
    q = ("query v($v: String!, $d: DatasetId!) { variant(variantId: $v, dataset: $d) { "
         "variantId genome { af ac an } } }")
    vid = 'chr%s-%d-%s-%s' % (ch,pos,ref,alt)
    try:
        r = requests.post('https://gnomad.broadinstitute.org/api/', json={'query':q,'variables':{'v':vid,'d':'gnomad_r4'}}, timeout=90, headers={'Content-Type':'application/json'})
        if r.status_code != 200 or r.text.strip()[:1] != '{':
            return {'err':'HTTP %d: %r' % (r.status_code, r.text[:120])}
        j = r.json()
        g = (j.get('data') or {}).get('variant',{}).get('genome')
        if g is None:
            return None
        return {'af':g.get('af'),'ac':g.get('ac'),'an':g.get('an')}
    except Exception as e:
        return {'err':str(e)}
out=io.StringIO()
for gene, vlist in cand.items():
    chr = PANEL.get(gene,{}).get('chr')
    out.write('=== %s (chr%s) ===\n'%(gene,chr))
    n_rare=0
    for (pos,ref,alt) in vlist:
        res = query(chr.replace('chr',''),pos,ref,alt)
        if res is None:
            out.write('  chr%s:%d %s>%s  gnomAD: AUSENTE (ref)  <== RARA\n'%(chr,pos,ref,alt))
            n_rare+=1
        elif 'err' in res:
            out.write('  chr%s:%d %s>%s  ERR %s\n'%(chr,pos,ref,alt,res['err']))
        else:
            af=res['af']
            rare = af is None or af < 0.01
            tag = '<== RARA' if rare else '(comun %.3f%%)'%((af or 0)*100)
            out.write('  chr%s:%d %s>%s  gnomAD af=%s ac=%s an=%s  %s\n'%(chr,pos,ref,alt,res['af'],res['ac'],res['an'],tag))
    out.write('\n')
open(r'C:\starquake\hackathonmva\_gnomad_renal.txt','w',encoding='utf-8').write(out.getvalue())
print(out.getvalue())
