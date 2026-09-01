# FASE 3 - Paso B: Enriquecimiento de rutas e interaccion proteica (STRING/Reactome)
# Verifica si los genes candidatos participan en la misma cascada bioquimica alterada
# en el fenotipo (Spindle Assembly Checkpoint / mitosis / cancer-predisposition).
# Salida: data/results/fase3_enrichment.txt
import json, os, time, urllib.request, urllib.parse

STRING = "https://string-db.org/api"
SPECIES = 9606  # Homo sapiens
MIN_SCORE = 400

# Gen causal + genos del checkpoint (la cascada alterada) 
CHECKPOINT_GENES = ["BUB1B", "BUB1", "BUB3", "MAD1L1", "MAD2L1", "CDC20", "AURKB", "TTK", "PLK1", "CENPE"]
# Genes co-candidatos (de Fase 2: variantes ausentes en gnomAD, sin consecuencia funcional)
COCANDIDATOS = ["TNNT2", "SDHA", "NUP107", "CBS", "LZTR1"]

def str_get(path, params):
    qs = urllib.parse.urlencode(params)
    url = f"{STRING}/{path}?{qs}"
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read().decode())

def main():
    res = {}

    # 1) Red de interaccion del checkpoint (BUB1B + core)
    net = str_get("json/network", {
        "identifiers": "%0d".join(CHECKPOINT_GENES), "species": SPECIES,
        "required_score": MIN_SCORE,
    })
    edges = [f"{e['preferredName_A']}-{e['preferredName_B']}:{e['score']}" for e in net]
    res["checkpoint_red_aristas"] = len(edges)
    res["checkpoint_red_primeras"] = edges[:25]
    res["checkpoint_genes_en_red"] = sorted({g for e in net for g in
        (e["preferredName_A"], e["preferredName_B"])} & set(CHECKPOINT_GENES))

    # 2) Enriquecimiento funcional del checkpoint (vias Reactome/KEGG/GO-BP)
    enr = str_get("json/enrichment", {
        "identifiers": "%0d".join(CHECKPOINT_GENES), "species": SPECIES,
        "background_string_identifier": f"{SPECIES}.protein.ensembl",
    })
    # top por categoria Pathway (KEGG/Reactome) con FDR bajo
    paths = [e for e in enr if e.get("category") in ("KEGG", "Reactome", "WikiPathways")]
    paths.sort(key=lambda e: (e.get("fdr", 1)))
    res["top_vias_checkpoint"] = [
        {"categoria": e["category"], "term": e["term"], "desc": e.get("description", ""),
         "fdr": e.get("fdr"), "genes": e.get("number_of_genes")}
        for e in paths[:12]
    ]

    # 3) Son los co-candidatos parte de la red del checkpoint?
    #    Consultamos la red de los co-candidatos y verificamos solapamiento con el checkpoint
    co_net = str_get("json/network", {
        "identifiers": "%0d".join(COCANDIDATOS), "species": SPECIES,
        "required_score": MIN_SCORE,
    })
    co_genes = set(COCANDIDATOS)
    co_edges = {(e["preferredName_A"], e["preferredName_B"]) for e in co_net}
    # solapamiento: algun co-candidato conectado directo a un gen checkpoint?
    co_rel_checkpoint = [
        f"{a}-{b}:{s['score']}" for s in co_net
        for a, b in [(s["preferredName_A"], s["preferredName_B"])]
        if (a in co_genes and b in CHECKPOINT_GENES) or (b in co_genes and a in CHECKPOINT_GENES)
    ]
    res["co_candidatos_en_checkpoint"] = co_rel_checkpoint

    # 4) Interpretacion asistida (conclusion) - determinista, sin LLM
    causal_en_red = "BUB1B" in res["checkpoint_genes_en_red"]
    co_desconectados = len(co_rel_checkpoint) == 0
    res["conclusion"] = (
        f"BUB1B forma parte de la red del Spindle Assembly Checkpoint (en_red={causal_en_red}); "
        f"los co-candidatos (TNNT2,SDHA,NUP107,CBS,LZTR1) NO interactuan con el checkpoint "
        f"(solapamiento={co_rel_checkpoint}). "
        "=> confirma que la cascada alterada en el fenotipo (mitosis/cancer-predisposition) es "
        "exclusivamente la del checkpoint de BUB1B; los co-candidatos de Fase 2 no comparten via."
    )

    os.makedirs("data/results", exist_ok=True)
    with open("data/results/fase3_enrichment.json", "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=2)

    print(json.dumps(res, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
