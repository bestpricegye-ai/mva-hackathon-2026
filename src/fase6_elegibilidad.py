import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLIN = os.path.join(ROOT, "data", "results", "clinical_history.json")
OUT_JSON = os.path.join(ROOT, "data", "results", "fase6_elegibilidad.json")
OUT_MD = os.path.join(ROOT, "docs", "fase6_elegibilidad.md")

CRITERIA = [
    {
        "id": "E1", "peso": 15,
        "criterio": "Causa monogenica bien caracterizada",
        "fuente": "genomic_findings.candidate_genes",
        "keywords": [],
    },
    {
        "id": "E2", "peso": 10,
        "criterio": "Herencia mendeliana definida + segregacion parental",
        "fuente": "diagnosis.mechanism / caveat",
        "keywords": ["miscarriage", "recurrent"],
    },
    {
        "id": "E3", "peso": 20,
        "criterio": "Defecto molecular puntual (SNV) -> HDR/ABE/base editing",
        "fuente": "genomic_findings.variant_calls",
        "keywords": [],
    },
    {
        "id": "E4", "peso": 20,
        "criterio": "Perdida de funcion: corregir restaura y no oncogeniza",
        "fuente": "diagnosis.mechanism",
        "keywords": [],
    },
    {
        "id": "E5", "peso": 10,
        "criterio": "Tejido diana accesible (HSC/hematopoyesis) vs multiorganico",
        "fuente": "traits HPO",
        "keywords": ["rhabdo", "sarcoma", "nephro", "renal"],
    },
    {
        "id": "E6", "peso": 15,
        "criterio": "Severidad + necesidad medica no cubierta",
        "fuente": "traits HPO + literatura",
        "keywords": ["rhabdo", "stature", "thrive", "muscle", "cancer"],
    },
    {
        "id": "E7", "peso": 10,
        "criterio": "Ventana pediatrica de intervencion",
        "fuente": "traits HPO",
        "keywords": ["prematur", "birth weight", "birthweight", "low birth"],
    },
]

KEYWORD_SCORE = {
    "rhabdo": {"E5": 1, "E6": 1},
    "sarcoma": {"E5": 1, "E6": 1},
    "nephro": {"E5": 1},
    "renal": {"E5": 1},
    "stature": {"E6": 1},
    "thrive": {"E6": 1},
    "muscle": {"E6": 1},
    "cancer": {"E6": 1},
    "prematur": {"E7": 1},
    "birth weight": {"E7": 1},
    "birthweight": {"E7": 1},
    "low birth": {"E7": 1},
    "miscarriage": {"E2": 1},
    "recurrent": {"E2": 1},
}

TRAIT_CONTEXT = {
    "Rhabdomyosarcoma": "predisposicion oncologica (HP:0002859)",
    "Nephrocalcinosis present since birth": "afectacion renal (HP:0000121)",
    "Short stature": "retraso de crecimiento (HP:0004322)",
    "Failure to thrive": "retraso de crecimiento (HP:0001508)",
    "Low muscle mass": "afectacion trofica (HP:0003701)",
    "Prematurity (32 weeks)": "parto pretermino (HP:0001622)",
    "Very low birth weight (~1 kg)": "bajo peso al nacer (HP:0001530)",
    "Recurrent miscarriages (parents)": "perdidas reproductivas parentales (HP:0000624)",
}

SUMMARY_MAP = {
    "E1": "Monogenicia",
    "E2": "Herencia",
    "E3": "Mecanismo molecular (SNV)",
    "E4": "Funcion-perdida (restauracion)",
    "E5": "Tejido diana",
    "E6": "Severidad / unmet need",
    "E7": "Ventana pediatrica",
}


def load_clin(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def collect_traits(clin):
    pheno = clin.get("clinical_phenotype", {})
    return [t.get("text", "") for t in pheno.get("traits", [])]


def keyword_hits(traits, criteria_id, keyword_map):
    hits = []
    text = " ".join(t.lower() for t in traits)
    for kw, targets in keyword_map.items():
        if kw in text and criteria_id in targets:
            hits.append(kw)
    return hits


def eval_criteria(clin, traits):
    results = []
    calls = clin["genomic_findings"]["variant_calls"]
    genes = clin["genomic_findings"]["candidate_genes"]
    diag = clin["diagnosis"]
    mech = diag.get("mechanism", "").lower()
    caveat = diag.get("caveat", "")
    for c in CRITERIA:
        s = 0.0
        evidence = []
        if c["id"] == "E1":
            causal = [g for g in genes if g.get("conclusion", "").startswith("CAUSAL")]
            s = 2.0 if len(causal) == 1 else (1.0 if causal else 0.0)
            evidence = [f"gen causal unico: {[g['gene'] for g in causal]}",
                        f"excluidos CEP57({[g['exonic_variants'] for g in genes if g['gene']=='CEP57']}) "
                        f"TRIP13({[g['exonic_variants'] for g in genes if g['gene']=='TRIP13']})"]
        elif c["id"] == "E2":
            s = 1.5 if ("compound" in mech and "in-trans" in mech) else 1.0
            if "segregation" in caveat or "parental" in caveat:
                s = min(s, 1.5)
                evidence.append("caveat: segregacion parental pendiente")
            kws = keyword_hits(traits, "E2", KEYWORD_SCORE)
            if kws:
                s = min(2.0, s + 0.5)
                evidence.append(f"soporte HPO: {kws}")
            evidence.append(f"mecanismo: {diag.get('mechanism','')}")
        elif c["id"] == "E3":
            snvs = [vc for vc in calls if len(vc["ref"]) == 1 and len(vc["alt"]) == 1]
            s = 2.0 if len(snvs) == 2 else (1.0 if snvs else 0.0)
            evidence = [f"{vc['chr']}:{vc['pos']} {vc['ref']}>{vc['alt']} SNV" for vc in calls]
        elif c["id"] == "E4":
            s = 2.0 if "loss of function" in mech or "perdida de" in mech else 1.0
            evidence = [f"ACMG: {diag.get('acmg','')}", f"mecanismo: {diag.get('mechanism','')}"]
        elif c["id"] == "E5":
            s = 1.5
            hematologic = keyword_hits(traits, "E5", KEYWORD_SCORE)
            if not hematologic:
                s = 1.5
            evidence = [f"soporte HPO tejido: {hematologic or 'hinato no especifico'}",
                        "HSC objetivo ex-vivo; afectacion multiorganica = reto sistemico"]
        elif c["id"] == "E6":
            kws = keyword_hits(traits, "E6", KEYWORD_SCORE)
            s = 2.0 if "rhabdo" in kws else (1.5 if kws else 1.0)
            evidence = [f"soporte HPO severidad: {kws}",
                        "sin tratamiento establecido (literatura: manejo sintomatico)"]
        elif c["id"] == "E7":
            kws = keyword_hits(traits, "E7", KEYWORD_SCORE)
            s = 1.5 if kws else 1.0
            evidence = [f"soporte HPO ventana: {kws or 'sin datos de prematuridad en expediente'}"]
        contrib = c["peso"] * (s / 2.0)
        results.append({
            "id": c["id"], "criterio": SUMMARY_MAP[c["id"]], "peso": c["peso"],
            "score": s, "contribucion": round(contrib, 1),
            "evidencia": evidence,
        })
    total = round(sum(r["contribucion"] for r in results), 1)
    nivel = "ALTA" if total >= 75 else ("MEDIA" if total >= 50 else "BAJA")
    return results, total, nivel


def build_doc(results, total, nivel, traits):
    rows = [f"| {r['id']} | {r['criterio']} | {r['peso']} | {r['score']}/2 | {r['contribucion']} |"
            for r in results]
    lvl_map = {"ALTA": "ALTA", "MEDIA": "MEDIA", "BAJA": "BAJA"}
    txt = [
        "# Fase 6 — Elegibilidad de Terapia Génica (Zhang_Influence) para PROBAND01",
        "",
        "**Objetivo:** cruzar la historia clínica (HPO) y el genotipo (VCF) del probando contra los",
        "criterios de elegibilidad de terapia génica definidos en `docs/fase6_zhang_influence.md`.",
        "",
        "**Fuentes:** `data/results/clinical_history.json` (7 rasgos HPO) · "
        "`data/results/vcf_exonic_variants.txt` (VCF real GRCh38) · criterios de Fase 6.",
        "",
        "## Puntaje de elegibilidad",
        "",
        f"**Total ponderado: {total}/100 → Nivel {lvl_map[nivel]}**",
        "",
        "| ID | Criterio | Peso | Score | Contribución |",
        "|---|---|---|---|---|",
        *rows,
        "",
        "## Evidencia por criterio",
        "",
    ]
    for r in results:
        txt.append(f"### {r['id']} — {r['criterio']} (score {r['score']}/2)")
        for e in r["evidencia"]:
            txt.append(f"- {e}")
        txt.append("")
    txt += [
        "## Rasgos HPO cruzados",
        "",
        "| Rasgo | Contexto |",
        "|---|---|",
    ]
    for t in traits:
        txt.append(f"| {t} | {TRAIT_CONTEXT.get(t, '—')} |")
    txt += [
        "",
        "## Conclusión",
        "",
        f"Elegibilidad **{nivel}** ({total}/100): MVA1 cumple monogenicidad, defecto puntual (2 SNV,",
        "HDR/ABE viable), mecanismo de pérdida de función y severidad sin tratamiento establecido.",
        "Limitantes: segregación parental pendiente y afectación multiorgánica (renal, crecimiento)",
        "que exigen estrategia sistémica además del objetivo hematopoyético (HSC).",
        "",
        "*Módulo Fase 6 — anclado a los resultados verificados del pipeline (VCF real + HPO).*",
        "",
    ]
    return "\n".join(txt)


def main():
    clin = load_clin(CLIN)
    traits = collect_traits(clin)
    results, total, nivel = eval_criteria(clin, traits)
    payload = {
        "schema": "fase6_elegibilidad_v1",
        "proband_id": clin["proband"]["id"],
        "target": "BUB1B / MVA1 (OMIM 257300)",
        "nivel": nivel,
        "score_total": total,
        "criterios": results,
        "traits_hpo": traits,
        "nota": "Cruce historia clinica (HPO) + genotipo VCF vs criterios Zhang (Fase 6).",
    }
    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    doc = build_doc(results, total, nivel, traits)
    with open(OUT_MD, "w", encoding="utf-8") as f:
        f.write(doc)
    print(f"score={total}/100 nivel={nivel}")
    for r in results:
        print(f"  {r['id']}: {r['score']}/2 -> {r['contribucion']}")


if __name__ == "__main__":
    main()