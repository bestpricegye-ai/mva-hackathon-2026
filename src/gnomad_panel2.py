import requests, json, io, time, os

PANEL = json.load(open(r'C:\starquake\hackathonmva\_panel2.json', encoding='utf-8'))
SAVE = r'C:\starquake\hackathonmva\_gnomad_resume.json'

# Re-analizar panel2 del VCF para extraer la lista completa de candidatos 1/1 con chr real
VCF = r'C:\starquake\hackathonmva\WGS_EX2312012_HGWCNDSX7.vcf.gz'
import gzip
lookup = {}
for gene, info in PANEL.items():
    chr = info.get('chr')
    if not chr: continue
    for (s, e) in info.get('exons', []):
        lookup.setdefault(chr, []).append((s, e, gene))

def find_genes(chrom, pos):
    return [g for (s, e, g) in lookup.get(chrom, []) if s <= pos <= e]

cands = []
with gzip.open(VCF, 'rt') as f:
    for line in f:
        if line.startswith('#'): continue
        c = line.split('\t')
        if len(c) < 9: continue
        chrom, pos = c[0], int(c[1])
        genes = find_genes(chrom, pos)
        if not genes: continue
        d = dict(zip(c[8].split(':'), c[9].split(':')))
        gt = d.get('GT','.')
        ref, alt = c[3], c[4]
        is_indel = len(ref) != len(alt)
        cand = (gt == '1/1') or is_indel
        if not cand: continue
        for g in genes:
            cands.append({'gene': g, 'chrom': chrom, 'pos': pos, 'ref': ref, 'alt': alt})

# dedup
seen = set(); uniq = []
for x in cands:
    k = (x['gene'], x['chrom'], x['pos'], x['ref'], x['alt'])
    if k not in seen:
        seen.add(k); uniq.append(x)

print('Candidatos 1/1 + indels totales:', len(uniq))

resume = {}
if os.path.exists(SAVE):
    resume = json.load(open(SAVE, encoding='utf-8'))

def query(ch, pos, ref, alt):
    q = ("query v($v: String!, $d: DatasetId!) { variant(variantId: $v, dataset: $d) { "
         "variantId genome { af ac an } } }")
    vid = 'chr%s-%d-%s-%s' % (ch, pos, ref, alt)
    last = None
    for attempt in range(4):
        try:
            r = requests.post('https://gnomad.broadinstitute.org/api/',
                              json={'query': q, 'variables': {'v': vid, 'd': 'gnomad_r4'}},
                              timeout=90, headers={'Content-Type': 'application/json'})
            if r.status_code == 429:
                last = ('429', r.text[:60])
                time.sleep(3 + attempt * 4)
                continue
            if r.status_code != 200 or r.text.strip()[:1] != '{':
                last = ('HTTP%d' % r.status_code, r.text[:60])
                time.sleep(2)
                continue
            j = r.json()
            g = (j.get('data') or {}).get('variant', {}).get('genome')
            return {'af': g.get('af'), 'ac': g.get('ac'), 'an': g.get('an')}
        except Exception as e:
            last = ('exc', str(e))
            time.sleep(2)
    return {'af': None, 'ac': None, 'an': None, 'blocked': True}

# annotate missing, save incrementally
pending = [x for x in uniq if x['gene']+':'+str(x['pos']) not in resume]
for i, x in enumerate(pending):
    key = x['gene'] + ':' + str(x['pos'])
    res = query(x['chrom'].replace('chr', ''), x['pos'], x['ref'], x['alt'])
    resume[key] = {'chrom': x['chrom'], 'pos': x['pos'], 'ref': x['ref'], 'alt': x['alt'],
                   'gt': x['gt'] if 'gt' in x else '1/1', **res}
    json.dump(resume, open(SAVE, 'w', encoding='utf-8'))
    if i % 5 == 0 or res.get('blocked'):
        print('  [%d/%d] %s:%s' % (i, len(pending), key, res.get('af')))
    time.sleep(0.4)

print('Anotados/guardados:', len(resume), 'de', len(uniq))
