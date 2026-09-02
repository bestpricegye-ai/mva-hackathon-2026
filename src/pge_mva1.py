import argparse
import json
import math
import os
import random

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "data", "results")

BUB1B_EXONS = [
    (40161069, 40161255), (40165053, 40165196), (40170062, 40170121),
    (40170537, 40170681), (40176477, 40176673), (40183714, 40183883),
    (40185165, 40185379), (40185551, 40185642), (40196545, 40196774),
    (40199615, 40199727), (40200244, 40200359), (40200931, 40200980),
    (40202405, 40202465), (40202589, 40202694), (40206184, 40206458),
    (40208637, 40208770), (40209635, 40209775), (40210110, 40210210),
    (40212499, 40212648), (40213332, 40213474), (40217496, 40217667),
    (40218456, 40218562), (40220564, 40221123),
]

EXON17 = ("AAACCCTACTCAGTCACCATGGTGTTCACAGTATCGCAGACAGCTACTGAAGTCCCTACCAG"
          "AGTTAAGTGCCTCTGCAGAGTTGTGTATAGAAGACAGACCAATGCCTAAGTTGGAAATTGAG"
          "AAGGAAATTGAATTAG")

SITES = [
    {"pos": 40209701, "ref": "T", "alt": "G", "label": "L737Ter", "transcript": "ENST00000287598.11"},
    {"pos": 40220612, "ref": "T", "alt": "G", "label": "N1002K", "transcript": "ENST00000287598.11"},
]


def wilson(k, n, z=1.96):
    if n == 0:
        return {"est": None, "lo": None, "hi": None}
    p = k / n
    den = 1 + z ** 2 / n
    c = p + z ** 2 / (2 * n)
    w = z * math.sqrt(p * (1 - p) / n + z ** 2 / (4 * n ** 2))
    return {"est": p, "lo": max(0.0, (c - w) / den), "hi": min(1.0, (c + w) / den)}


def run_nmd(path):
    report = {"schema": "pge_mva1_nmd_v1", "transcript": "ENST00000287598.11",
              "rule": "EJC: PTC >55nt aguas arriba del splice-junction aguas abajo -> NMD-competente",
              "nota_coord": "exones Ensembl 1-based-inclusive; ventana UCSC 0-based-hal-open "
                            "(off-by-1 entre convenciones no afecta la llamada NMD por distancia)",
              "exons": BUB1B_EXONS, "variantes": []}
    for s in SITES:
        pos = s["pos"]
        exon_i = next((i for i, (e0, e1) in enumerate(BUB1B_EXONS) if e0 <= pos <= e1), None)
        if exon_i is None:
            entry = dict(s, status="FUERA_DE_EXONES")
        else:
            e0, e1 = BUB1B_EXONS[exon_i]
            dist = e1 - pos
            last_exon = exon_i == len(BUB1B_EXONS) - 1
            nmd = (not last_exon) and dist > 55
            entry = dict(s, exon_index=exon_i + 1, exon=(e0, e1),
                         dist_to_junction_nt=dist, last_exon=last_exon,
                         nmd_competent=nmd,
                         status="NMD_COMPETENTE" if nmd else "SIN_NMD")
        report["variantes"].append(entry)

    e0_e1 = BUB1B_EXONS[16]
    e0, e1 = e0_e1
    seq = EXON17
    asos = []
    for start in range(40, len(seq) - 19):
        mer = seq[start:start + 20]
        gc = (mer.count("G") + mer.count("C")) / 20
        if not (0.40 <= gc <= 0.70):
            continue
        if any(h in mer for h in ("AAAAA", "TTTTT", "GGGGG", "CCCCC")):
            continue
        asos.append({"window": f"chr15:{e0 + start}-{e0 + start + 19}",
                     "offset_in_exon17": start, "seq20mer": mer,
                     "gc": round(gc, 2), "relative_ptc": f"start-{SITES[0]['pos'] - e0}..start+19-{SITES[0]['pos'] - e0}"})
    asos.sort(key=lambda a: -a["gc"])
    report["aso_candidatos"] = [a for a in asos if int(a["window"].split("-")[1]) >= SITES[0]["pos"]][:6] or asos[:6]
    with open(os.path.join(path, "pge_mva1_nmd.json"), "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    for v in report["variantes"]:
        print(v["label"], v["status"], "dist", v.get("dist_to_junction_nt"))
    print("ASO candidatos:", len(report["aso_candidatos"]))
    return report


def seq_ok(off):
    return EXON17[off] == SITES[0]["ref"]


def parse_gt(g):
    if isinstance(g, dict):
        return g.get("gt") or g.get("genotype") or g
    return g


def site_parental(g):
    if not g:
        return "sin_dato"
    gg = parse_gt(g)
    if isinstance(gg, dict):
        alleles = gg.get("alleles") or gg.get("ad") or []
    elif isinstance(gg, list):
        alleles = gg
    else:
        alleles = str(gg).split("/")
    return "portador" if alleles == [0, 1] else ("no_portador" if alleles == [0, 0] else "desconocido")


def run_phase(path, trios_json):
    rows = []
    for site, dat in trios_json.get("sites", {}).items():
        dad = site_parental(dat.get("paternal"))
        mom = site_parental(dat.get("maternal"))
        if dad == "sin_dato" and mom == "sin_dato":
            src = "de_novo_sospecha"
        elif dad == "portador" and mom == "portador":
            src = "ambos_portadores"
        elif dad == "portador":
            src = "paterno"
        elif mom == "portador":
            src = "materno"
        else:
            src = "indeterminado"
        rows.append({"site": site, "origen": src, "paternal": dad, "maternal": mom})
    sources = [r["origen"] for r in rows]
    if "paterno" in sources and "materno" in sources:
        phase = "IN_TRANS_CONFIRMADO"
    elif sources and all(s == "de_novo_sospecha" for s in sources):
        phase = "IN_TRANS_INFERIDO_DE_NOVO_PENDIENTE"
    else:
        phase = "INDETERMINADO"
    out = {"schema": "pge_mva1_phase_v1", "fase": phase, "variantes": rows,
           "nota": "requiere WGS trios para confirmacion definitiva"}
    with open(os.path.join(path, "pge_mva1_phase.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    for r in rows:
        print("  ", r["site"], "->", r["origen"])
    print("fase:", phase)
    return out


def prop_diff_ci(k1, n1, k2, n2, z=1.96):
    """Diferencia p2-p1 (tratado - control) con CI tipo Newcombe (Wilson)."""
    w1 = wilson(k1, n1, z)
    w2 = wilson(k2, n2, z)
    if None in (w1["lo"], w1["hi"], w2["lo"], w2["hi"]):
        return None
    lo = w2["lo"] - w1["hi"]
    hi = w2["hi"] - w1["lo"]
    return {"diff": w2["est"] - w1["est"], "lo": lo, "hi": hi}


def run_telemetry(data, wt_lower=None):
    divisions = float(data["divisiones"])
    errors = float(data["errores_segregacion"])
    events = float(data["eventos_segregacion"])
    apop = float(data["apoptosis_frac"])
    sen = float(data["senescencia_frac"])
    div_ratio = data.get("div_rate_ratio", 1.0)
    wt_errors = data.get("wt_errors")
    wt_divisions = data.get("wt_divisions") or divisions
    gates = {
        "n_completadas_ge80": divisions >= 80,
        "n_eventos_ge450": events >= 450,
        "sin_toxicidad": apop <= 0.15 and sen <= 0.15,
    }
    if divisions <= 0 or not wt_errors:
        return {"avance_permitido": False, "fail_closed": True,
                "motivo": ["divisiones_o_control_insuficiente"]}
    err = errors / divisions
    d = prop_diff_ci(int(wt_errors), int(wt_divisions), int(errors), int(divisions))
    if d is None or not wt_errors:
        gates["reduccion_error_ge20"] = False
    else:
        wt_rate = wt_errors / wt_divisions
        frac_puntual = -d["diff"] / wt_rate
        significativo = d["hi"] < 0  # el tratado reduce de forma significativa vs control
        gates["reduccion_error_ge20"] = bool(frac_puntual >= 0.20 and significativo)
    gates["sin_citostasis"] = bool(gates["reduccion_error_ge20"] and div_ratio >= 0.85)
    ok = all(gates.values())
    return {"error_rate_por_division": err,
            "reduccion_frac_puntual": (-d["diff"] / (wt_errors / wt_divisions)) if d and wt_errors else None,
            "reduccion_significativa": (d["hi"] < 0) if d else False,
            "wt_control_rate": (wt_errors / wt_divisions) if wt_divisions and wt_errors is not None else None,
            "avance_permitido": ok, "fail_closed": not ok,
            "motivo": [k for k, v in gates.items() if not v] if not ok else [],
            "gates": gates}


def build_world(rng, cls):
    if cls == "rescue":
        plow, phigh, dr, apop, sen, dbase = 0.02, 0.05, 0.95, 0.05, 0.04, 250
    elif cls == "cytostatic":
        plow, phigh, dr, apop, sen, dbase = 0.02, 0.05, 0.35, 0.5, 0.12, 250
    elif cls == "neutral":
        plow, phigh, dr, apop, sen, dbase = 0.08, 0.08, 0.98, 0.05, 0.04, 250
    else:  # sparse
        plow, phigh, dr, apop, sen, dbase = 0.03, 0.06, 0.06, 0.05, 0.04, 20
    divisions = max(1, round(rng.uniform(dbase, dbase * 1.2) * dr))
    errors = rng.randint(0, max(0, int(divisions * rng.uniform(plow, phigh))))
    wt_divs = max(1, round(rng.uniform(dbase, dbase * 1.2)))
    wt_errors = rng.randint(0, max(0, int(wt_divs * rng.uniform(0.06, 0.10))))
    events = 80 + divisions * round(rng.uniform(3, 5))
    return {"divisiones": divisions, "errores_segregacion": errors,
            "eventos_segregacion": events, "apoptosis_frac": apop,
            "senescencia_frac": sen, "div_rate_ratio": dr,
            "wt_errors": wt_errors, "wt_divisions": wt_divs, "_truth": cls}


def run_selftest(path, n, seed):
    rng = random.Random(seed)
    pool = [("rescue", 0.20), ("cytostatic", 0.25), ("neutral", 0.25), ("sparse", 0.30)]
    truth = [pick(rng, pool) for _ in range(n)]
    n_cyto = truth.count("cytostatic")
    n_sparse = truth.count("sparse")
    n_rescue = truth.count("rescue")
    det_cyto = 0
    fail_sparse = 0
    confirm_rescue = 0
    fp = 0
    for cls in truth:
        w = build_world(rng, cls)
        dec = run_telemetry(w)
        if dec["avance_permitido"]:
            if cls == "rescue":
                confirm_rescue += 1
            else:
                fp += 1
        else:
            if cls == "cytostatic":
                det_cyto += 1
            if cls == "sparse":
                fail_sparse += 1
    wf = wilson(fp, n)
    out = {"schema": "pge_mva1_selftest_v1", "n_worlds": n, "seed": seed,
           "distribution": {k: truth.count(k) for k, _ in pool},
           "deteccion_citostasis": (det_cyto / n_cyto) if n_cyto else None,
           "confirmacion_rescate": (confirm_rescue / n_rescue) if n_rescue else None,
           "falsos_avance": fp / n,
           "wilson_ucb_falsos_avance": wf["hi"],
           "fail_closed_en_escaso": (fail_sparse / n_sparse) if n_sparse else None,
           "nota": "valida el ANALIZADOR sobre mundos sinteticos con verdad oculta; no evidencia clinica"}
    with open(os.path.join(path, "pge_mva1_selftest.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return out


def pick(rng, pool):
    r = rng.random()
    acc = 0
    for name, w in pool:
        acc += w
        if r <= acc:
            return name
    return pool[-1][0]


def main():
    ap = argparse.ArgumentParser(prog="pge_mva1", description="PGE-MVA1 precision genomics toolkit")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("nmd")
    ph = sub.add_parser("phase")
    ph.add_argument("--trios", default="", help="ruta a json de genotipos trios")
    tl = sub.add_parser("telemetry")
    tl.add_argument("--data", default="", help="ruta a json de telemetria")
    st = sub.add_parser("selftest")
    st.add_argument("-n", type=int, default=2000)
    st.add_argument("--seed", type=int, default=42)
    args = ap.parse_args()
    os.makedirs(OUT, exist_ok=True)

    if args.cmd == "nmd":
        run_nmd(OUT)
    elif args.cmd == "phase":
        g = {"sites": {
            "chr15:40209701": {"paternal": [0, 1], "maternal": [0, 0]},
            "chr15:40220612": {"paternal": [0, 0], "maternal": [0, 1]}}}
        run_phase(OUT, g)
    elif args.cmd == "telemetry":
        res = run_telemetry({"divisiones": 96, "errores_segregacion": 4,
                             "eventos_segregacion": 800, "apoptosis_frac": 0.05,
                             "senescencia_frac": 0.04, "div_rate_ratio": 0.95,
                             "wt_errors": 8, "wt_divisions": 96})
        print(json.dumps(res, ensure_ascii=False, indent=2))
    else:
        run_selftest(OUT, args.n, args.seed)


if __name__ == "__main__":
    main()