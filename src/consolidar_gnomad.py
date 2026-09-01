import json, os
from config import ROOT, RESULTS_DIR

def loadj(p, default=None):
    return json.load(open(p, encoding='utf-8')) if os.path.exists(p) else default

# Fuentes de anotacion gnomAD
srcs = {
    '_acmg_gnomad.json': os.path.join(ROOT, '_acmg_gnomad.json'),
    '_gnomad_resume.json': os.path.join(ROOT, '_gnomad_resume.json'),
    '_fase2_gnomad.json': os.path.join(ROOT, '_fase2_gnomad.json'),
}
flat = loadj(os.path.join(ROOT, '_fase2_flat.json'), [])

# cache de conocidas (misma logica de claves que fase2_gnomad.py)
cache = {}
for name, p in srcs.items():
    d = loadj(p, {})
    for k, vv in d.items():
        if all(x in vv for x in ('pos', 'ref', 'alt')):
            ch = str(vv.get('chrom', '')).replace('chr', '')
            cache["%s:%s:%s>%s" % (ch, vv['pos'], vv['ref'], vv['alt'])] = vv
        else:
            cache[k] = vv

# Consolidar: todas las variantes del flat con su anotacion (clave canónica)
consolidado = {}
missing = []
for r in flat:
    k = "%s:%s:%s>%s" % (r['chrom'], r['pos'], r['ref'], r['alt'])
    if k in cache:
        consolidado[k] = cache[k]
    else:
        consolidado[k] = {'af': None, 'ac': None, 'an': None, 'found': False}
        missing.append((k, r['gene']))

out = os.path.join(RESULTS_DIR, 'fase2_gnomad_completo.json')
json.dump(consolidado, open(out, 'w', encoding='utf-8'), indent=1)

print('flat           :', len(flat))
print('caches         :', {n: len(loadj(p, {})) for n, p in srcs.items()})
print('consolidado    :', len(consolidado))
print('sin anotacion  :', len(missing))
if missing:
    print('primeros sin anotar:', missing[:10])
print('output         :', out)