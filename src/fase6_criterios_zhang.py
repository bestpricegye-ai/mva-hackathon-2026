import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE = os.path.join(ROOT, "data", "cache", "ucsc_hg38_context.json")
OUT_JSON = os.path.join(ROOT, "data", "results", "fase6_criterios_zhang.json")
OUT_MD = os.path.join(ROOT, "docs", "fase6_criterios_zhang.md")

PAM_CRITERIA = {
    "spcas9_ngg": {"name": "SpCas9 (NGG)", "same_strand": "GG", "other_strand": "CC"},
}

BC = str.maketrans("ACGT", "TGCA")


def revcomp(s):
    return s.translate(BC)[::-1]


def eff_score(spacer):
    gc = (spacer.count("G") + spacer.count("C")) / 20.0
    gc_ok = 0 <= gc - 0.5 <= 0.15 if gc >= 0.40 else gc >= 0.30
    s = 0.0
    if 0.40 <= gc <= 0.65:
        s += 40
    elif 0.65 < gc <= 0.80 or 0.30 <= gc < 0.40:
        s += 20
    else:
        s += 5
    if "TTTT" in spacer.upper():
        s += 0
    else:
        s += 25
    if re.search(r"([ATGC])\1{4}", spacer.upper()):
        s += 0
    else:
        s += 15
    seed = spacer.upper()[17:20]
    s += 20 if seed.count("G") >= 1 else 5
    return round(min(s, 100)), round(gc * 100)


def scan_candidates(seq, variant_idx, ref_alt_ok):
    cands = []
    for strand, pat, pam_rc in (("+", r"([ACGT]{20}GG)", False),
                                ("-", r"([ACGT]{20}CC)", True)):
        for m in re.finditer(r"(?=(" + pat + r"))", seq):
            block = m.group(1)
            spacer_obs = block[:20]
            spacer = revcomp(spacer_obs) if pam_rc else spacer_obs
            start = m.start(1)
            v_in_spacer = start <= variant_idx < start + 20
            rel = variant_idx - start
            v_seed = 17 <= rel <= 19
            v_pam = start + 20 <= variant_idx <= start + 22
            if not (v_in_spacer or v_pam):
                continue
            ef, gc = eff_score(spacer)
            distance = abs(rel - 10) if v_in_spacer else 99
            cands.append({
                "strand": strand,
                "spacer": spacer,
                "pam": revcomp("GG") if pam_rc else "GG",
                "variant_in_spacer": v_in_spacer,
                "variant_in_seed": v_seed,
                "variant_in_pam_triple": v_pam,
                "allele_specific": v_seed or v_pam,
                "off_target": "NO_CALCULADO_LOCAL",
                "eff_heur": {"score": ef, "gc_pct": gc, "bin": "ALTA" if ef >= 70 else ("MEDIA" if ef >= 40 else "BAJA"),
                             "etiqueta": "heuristico_preliminar_Doench-ste_/DeepCRISPR_subset_validar_CRISPOR"},
                "cut_rel": start + 17,
                "dist_rel": distance,
            })
    cands.sort(key=lambda c: (c["allele_specific"], -c["eff_heur"]["score"], c["dist_rel"]))
    return cands


def main():
    with open(CACHE, encoding="utf-8") as f:
        ctx = json.load(f)
    out = {
        "schema": "fase6_criterios_zhang_v1",
        "principio": "Criterios de diseno de terapias CRISPR-Cas9 de Feng Zhang (MIT/Broad): "
                    "(1) Especificidad/off-target, (2) Eficiencia/on-target, (3) PAM (SpCas9 NGG).",
        "secuencia_referencia": ctx["source"],
        "variantes": [],
    }
    for key, w in ctx["windows"].items():
        seq = w["seq"]
        vi = w["variant_offset_in_window"]
        ok = seq[vi] == w["vcf_ref"]
        cands = scan_candidates(seq, vi, ok)
        best = cands[0] if cands else None
        out["variantes"].append({
            "pos": key,
            "ref_vcf": w["vcf_ref"], "alt_vcf": w["vcf_alt"], "tipo": w["type"],
            "ref_verificado_en_hg38": ok,
            "contexto": seq,
            "criterio_3_pam": {
                "spcas9_NGG_presente_cerca_sitio": bool(cands),
                "modo": "mismo_strand" if (best and best["strand"] == "+") else ("strand_opuesto" if best else "NO"),
                "pam_observado": (best["pam"] if best else "ninguno en +/-35nt del sitio"),
            },
            "criterio_2_eficiencia": (best["eff_heur"] if best else None),
            "criterio_1_especificidad": {
                "estado": "PENDIENTE_CRISPOR",
                "razon": "El scrapeo off-target del genoma completo requiere indice hg38 "
                        "(CRISPOR/CasOFFinder, 751 MB); no ejecutable en el entorno del hackathon.",
                "plan": [
                    "Ejecutar CRISPOR v4 o CasOFFinder contra GRCh38 con los espaciadores y el PAM NGG.",
                    "Aceptar gRNA solo con sitio canonicos 0-3 mismatches fuera del gen BUB1B.",
                    "Excluir sitios en oncogenes y genes del SAC (BUB1, MAD2L1, etc.) para no inducir aneuploidia.",
                    "Re-grasping alergico: desecho de gRNA con potenciales cortes en genomas paralogos.",
                ],
            },
            "mejor_gRNA_candidato": best,
        })
    verdict = "COBERTURA_PARCIAL"
    out["veredicto_global"] = {
        "criterio_3_pam": "VERIFICADO (secuencia hg38 con PAM NGG cercano en ambos sitios)",
        "criterio_2_eficiencia": "ESTIMADO (heuristica preliminar; requiere puntaje oficial CRISPOR/Doench)",
        "criterio_1_especificidad": "PENDIENTE (off-target requiere indice hg38; plan definido)",
        "nivel": verdict,
    }
    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    for v in out["variantes"]:
        b = v["mejor_gRNA_candidato"]
        print(f"{v['pos']} ref_ok={v['ref_verificado_en_hg38']} PAM={'+' if b else '-'} "
              f"eff={b['eff_heur']['bin']} allele_specific={b['allele_specific']} spacer={b['spacer']} {b['pam']}")
    print(f"veredicto: {out['veredicto_global']['nivel']}")


if __name__ == "__main__":
    main()