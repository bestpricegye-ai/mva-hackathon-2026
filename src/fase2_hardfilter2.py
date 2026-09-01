# FASE 2 - Paso 2: Re-filtro + dedup + flatten
# _fase2_variants.json (dict gene -> variantes) -> _fase2_survivors.json (dedup por pos, +chrom) -> _fase2_flat.json (planas, +gene)
import json, os
from config import ROOT, RESULTS_DIR, resolve_panel

def load_input():
    """_fase2_variants.json vive en raiz (intermedio); si no existe, cae a data/results."""
    p = os.path.join(ROOT, '_fase2_variants.json')
    if os.path.exists(p):
        return json.load(open(p, encoding='utf-8')), p
    p2 = os.path.join(RESULTS_DIR, 'fase2_hardfilter_variants.json')
    if os.path.exists(p2):
        return json.load(open(p2, encoding='utf-8')), p2
    raise FileNotFoundError("No existe _fase2_variants.json ni data/results/fase2_hardfilter_variants.json")

def load_chr_map():
    """gene -> chrom desde todos los paneles disponibles en data/panels."""
    m = {}
    for name in ['sac', 'panel2', 'acmg']:
        try:
            p = resolve_panel(name)
        except Exception:
            continue
        if not os.path.exists(p):
            continue
        d = json.load(open(p, encoding='utf-8'))
        if not isinstance(d, dict):
            continue
        for g, info in d.items():
            if isinstance(info, dict) and info.get('chr'):
                m[g] = info['chr']
    return m

def main():
    variants, src_path = load_input()
    chr_map = load_chr_map()

    survivors = {}
    missing = set()
    for gene, vlist in variants.items():
        seen = set()
        out = []
        for v in vlist:
            key = (v['pos'], v['ref'], v['alt'])
            if key in seen:
                continue
            seen.add(key)
            entry = {'chrom': chr_map.get(gene, ''), **v}
            out.append(entry)
            if gene not in chr_map:
                missing.add(gene)
        survivors[gene] = out

    flat = []
    for gene, vlist in survivors.items():
        for v in vlist:
            flat.append({**v, 'gene': gene})

    sv_path = os.path.join(ROOT, '_fase2_survivors.json')
    fl_path = os.path.join(ROOT, '_fase2_flat.json')
    json.dump(survivors, open(sv_path, 'w', encoding='utf-8'))
    json.dump(flat, open(fl_path, 'w', encoding='utf-8'))

    total_in = sum(len(v) for v in variants.values())
    total_sv = sum(len(v) for v in survivors.values())
    print(f"input : {src_path} | {total_in} variantes en {len(variants)} genes")
    print(f"survivors: {total_sv} variantes en {len(survivors)} genes (dedup: {total_in - total_sv} removidas)")
    print(f"flat   : {len(flat)} variantes")
    print(f"outputs: {sv_path} | {fl_path}")
    if missing:
        print(f"WARN genes sin chrom (vacio): {sorted(missing)}")

if __name__ == '__main__':
    main()