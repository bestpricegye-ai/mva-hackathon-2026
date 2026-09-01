# FASE 3 - Paso A: Prediccion funcional de VUS (impacto + dominio activo)
# Clasifica el dano potencial de cada variante candidata (VUS) sobre la proteina:
#   - Consecuencia funcional (Ensembl VEP REST)
#   - Predictores de impacto: SIFT / PolyPhen / AlphaMissense (via VEP cuando disponible)
#   - Posicion en dominio funcional (kinasa para BUB1B / InterPro)
# Salida: docs/../data/results/fase3_impacto.txt
import json, os, time, urllib.request, urllib.parse

ENS = "https://rest.ensembl.org"
VEP_HDR = {"Content-Type": "application/json", "Accept": "application/json"}

# Variantes candidatas exonices a clasificar (VUS) - extraidas de Fase 2 (_fase2_gnomad ausentes)
# formato: (chrom,pos,ref,alt,gene,panel)
CANDIDATOS = [
    ("15", 40220612, "T", "G", "BUB1B", "MVA"),
    ("1",  201365254, "G", "A", "TNNT2", "panel2"),
    ("5",  256828,    "C", "T", "SDHA",  "SAC"),
    ("12", 68743447,  "C", "T", "NUP107","panel2"),
    ("21", 43053757,  "G", "C", "CBS",   "panel2"),
    ("21", 43065240,  "G", "A", "CBS",   "panel2"),
    ("22", 20996720,  "C", "G", "LZTR1", "panel2"),
    ("22", 20998981,  "C", "G", "LZTR1", "panel2"),
]

# Dominios funcionales relevantes (prot_aa_start..end) para el analisis de "sitio activo"
# BUB1B/BubR1 UniProt O60566: N-terminal BUB1_N (62-226), quinasa ser/thr (766-1050)
DOMINIOS = {"BUB1B": [("BUB1 N-terminal", 62, 226), ("Seg/Thr kinase Cat.", 766, 1050)]}
# residuo catalitico (proton acceptor) del dominio quinasa de BUBR1
CATALITICO = {"BUB1B": {882: "D882 (catalitic proton acceptor)"}}

def vep_annotate(chrom, pos, ref, alt):
    # formato VCF linea via POST body: {"variants": ["chrom pos . ref alt"]}
    vcf_line = f"{chrom} {pos} . {ref} {alt}"
    body = {"variants": [vcf_line]}
    params = {"variant_class": "1", "picked": "1", "protein": "1", "ccds": "1", "numbers": "1"}
    url = ENS + "/vep/human/region" + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, data=json.dumps(body).encode(), headers=VEP_HDR,
                                 method="POST")
    with urllib.request.urlopen(req, timeout=60) as resp:
        data = json.loads(resp.read().decode())
    return data

def classify(c):
    chrom, pos, ref, alt, gene, panel = c
    rec = {"var": f"{chrom}:{pos}:{ref}>{alt}", "gene": gene, "panel": panel}
    try:
        data = vep_annotate(chrom, pos, ref, alt)[0]
    except Exception as e:
        rec["error"] = str(e)
        return rec
    rec["most_severe"] = data.get("most_severe_consequence")
    # escoger transcripcion del gen (canonica / mejor impacto)
    _SEV_ORDER = {"HIGH": 4, "MODERATE": 3, "LOW": 2, "MODIFIER": 1}
    tcs = sorted(data.get("transcript_consequences", []),
                 key=lambda t: _SEV_ORDER.get(t.get("impact"), 0), reverse=True)
    tc = next((t for t in tcs if t.get("gene_symbol") == gene and t.get("protein_coding")), None) \
         or next((t for t in tcs if t.get("gene_symbol") == gene), None) \
         or (tcs[0] if tcs else None)
    if tc:
        rec["csq"] = ",".join(tc.get("consequence_terms", []))
        rec["impact"] = tc.get("impact")
        rec["sift"] = tc.get("sift_prediction", "")
        rec["polyphen"] = tc.get("polyphen_prediction", "")
        rec["am"] = tc.get("am_pathogenicity")
        rec["am_class"] = tc.get("am_class") or tc.get("am_pathogenic")
        rec["hgvsp"] = tc.get("hgvsp", "")
        prot = tc.get("protein_start") or tc.get("protein_end")
        if prot:
            rec["prot_pos"] = int(prot)
            # pertenece a dominio funcional / sitio activo?
            for dom, s, e in DOMINIOS.get(gene, []):
                if s <= int(prot) <= e:
                    rec.setdefault("dominios", []).append(dom)
            cat = CATALITICO.get(gene, {}).get(int(prot))
            if cat:
                rec["catalitico"] = cat
    return rec

def main():
    out = []
    for c in CANDIDATOS:
        r = classify(c)
        out.append(r)
        time.sleep(0.4)  # cortesia a Ensembl REST
        print(json.dumps(r, ensure_ascii=False))
    # conclusion funcional
    print("\n=== CONCLUSION F3-A: solo las variantes con impacto MODERATE/HIGH y en dominio funcional son candidatas funcionales ===")
    funcional = [r for r in out if r.get("impact") in ("HIGH", "MODERATE") and "error" not in r]
    for r in funcional:
        print(f"  {r['var']} {r['gene']}: {r.get('csq')} [{r.get('impact')}] sift={r.get('sift')} polyphen={r.get('polyphen')} dominios={r.get('dominios')}")
    if not funcional:
        print("  Ninguna VUS es funcionalmente danina (todas LOW/MODIFIER).")
    os.makedirs("data/results", exist_ok=True)
    with open("data/results/fase3_impacto.txt", "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
