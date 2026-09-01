import os

# Paths centralized as parameters. Override any via env var (MVA_VCF, MVA_PANEL_DIR, MVA_RESULTS_DIR).
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

VCF = os.environ.get("MVA_VCF", os.path.join(ROOT, "WGS_EX2312012_HGWCNDSX7.vcf.gz"))

PANEL_DIR = os.environ.get("MVA_PANEL_DIR", os.path.join(ROOT, "data", "panels"))
RESULTS_DIR = os.environ.get("MVA_RESULTS_DIR", os.path.join(ROOT, "data", "results"))

PANEL_SAC = os.environ.get("MVA_PANEL_SAC", os.path.join(PANEL_DIR, "panel_sac.json"))
PANEL2 = os.environ.get("MVA_PANEL2", os.path.join(PANEL_DIR, "panel2.json"))
ACMG_EXONS = os.environ.get("MVA_ACMG_EXONS", os.path.join(PANEL_DIR, "acmg_exons.json"))

# Legacy fallbacks (older runs stored panels/outputs at the repo root).
LEGACY_PANELS = {
    "panel_sac": os.path.join(ROOT, "_panel_sac.json"),
    "panel2": os.path.join(ROOT, "_panel2.json"),
    "acmg": os.path.join(ROOT, "_acmg_exons.json"),
}


def _first(*cands):
    for c in cands:
        if c and os.path.exists(c):
            return c
    return cands[0] or None


def resolve_panel(kind):
    cands = {
        "sac": [PANEL_SAC, LEGACY_PANELS["panel_sac"], os.path.join(PANEL_DIR, "panel_sac.json")],
        "panel2": [PANEL2, LEGACY_PANELS["panel2"], os.path.join(PANEL_DIR, "panel2.json")],
        "acmg": [ACMG_EXONS, LEGACY_PANELS["acmg"], os.path.join(PANEL_DIR, "acmg_exons.json")],
    }[kind]
    return _first(*cands)


def resolve_output(name):
    return os.path.join(RESULTS_DIR, name)