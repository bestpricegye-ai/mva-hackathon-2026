#!/usr/bin/env python3
"""
PGE-MVA1 / Integration test del Testing Framework (Determinismo + Regresion).
Construye un mini-VCF golden (variantes reales BUB1B + controles), corre el stub
del pipeline y valida con vcf_regression. Tambien demuestra que una MUTACION
introducida a proposito hace FALLAR la regresion (fail-stop).

Uso:
  python tests/qc/test_integration.py            # exit 0 = todo PASS
"""
import json
import os
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
QC = os.path.join(ROOT, "tests", "qc")

HDR = ("##fileformat=VCFv4.2\n"
       "##source=PGE-MVA1_golden\n"
       "##fileDate=2026-09-02\n"
       "##contig=<ID=chr15>\n"
       "##INFO=<ID=DP,Number=1,Type=Integer>\n"
       "##INFO=<ID=AF,Number=A,Type=Float>\n"
       "##INFO=<ID=VEP,Number=1,Type=String>\n"
       "#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\n")

# variantes golden: incluye controles patogenicos (L737Ter, N1002K) y una comun.
GOLD_VARS = [
    "chr15\t40209701\t.\tT\tG\t708.77\tPASS\tDP=46;AF=0.543;VEP=L737Ter_PVS1",
    "chr15\t40220612\t.\tT\tG\t344.77\tPASS\tDP=28;AF=0.464;VEP=N1002K_kinase",
    "chr15\t10000000\t.\tA\tG\t120.5\tPASS\tDP=30;AF=0.050;VEP=benign_ctrl",
]


def write_golden(path):
    with open(path, "w", encoding="utf-8") as f:
        f.write(HDR)
        f.write("\n".join(GOLD_VARS) + "\n")
    return path


def run(cmd, cwd=ROOT, env=None):
    return subprocess.run(cmd, cwd=cwd, env=env, capture_output=True, text=True)


def check(name, cond, extra=""):
    print(("  [OK] " if cond else "  [FAIL] ") + name + (f" {extra}" if extra else ""))
    if not cond:
        raise SystemExit(f"FAIL: {name}")


def main():
    tmp = tempfile.mkdtemp()
    golden = os.path.join(tmp, "gold.vcf")
    out_ok = os.path.join(tmp, "out_ok.vcf")
    write_golden(golden)

    print("== 1) Determinism selftest ==")
    r = run([sys.executable, os.path.join(QC, "determinism.py"), "selftest"])
    check("determinism selftest rc=0", r.returncode == 0, r.stdout.strip())

    print("== 2) Pipeline stub (MVA_STUB_MUTATION=none => sin regresion) ==")
    env = {"MVA_STUB_MUTATION": "none"}
    r = run([sys.executable, os.path.join(QC, "run_pipeline_stub.py"), golden, out_ok], )
    check("stub rc=0", r.returncode == 0, r.stdout.strip())

    print("== 3) Regression: salida == golden (debe PASS) ==")
    r = run([sys.executable, os.path.join(QC, "vcf_regression.py"),
             "--golden", golden, "--current", out_ok,
             "--require-info", "DP,AF,VEP", "--json", os.path.join(tmp, "r_ok.json")])
    check("regression PASS rc=0", r.returncode == 0)
    rep = json.loads(r.stdout)
    check(" n_golden==3", rep["n_golden"] == 3, str(rep["n_golden"]))
    check(" n_current==3", rep["n_current"] == 3, str(rep["n_current"]))
    check(" deficits==0", rep["deficits"] == [])
    check(" orden_canonico_ok", rep["orden_canonico_ok"] is True)

    print("== 4) Regression con MUTACION (drop) => debe FALLAR (fail-stop) ==")
    out_bad = os.path.join(tmp, "out_bad.vcf")
    run([sys.executable, os.path.join(QC, "run_pipeline_stub.py"), golden, out_bad],
        env={**os.environ, "MVA_STUB_MUTATION": "drop"})
    r = run([sys.executable, os.path.join(QC, "vcf_regression.py"),
             "--golden", golden, "--current", out_bad, "--require-info", "DP,AF,VEP",
             "--json", os.path.join(tmp, "r_bad.json")])
    check(" regression FAIL rc=1 (variante perdida => detener job)", r.returncode == 1)
    rep = json.loads(r.stdout)
    check(" deficits detectados >0", len(rep["deficits"]) > 0, str(rep["deficits"]))

    print("== 5) Regression con MUTACION (filter q10) => FAIL ==")
    out_f = os.path.join(tmp, "out_f.vcf")
    run([sys.executable, os.path.join(QC, "run_pipeline_stub.py"), golden, out_f],
        env={**os.environ, "MVA_STUB_MUTATION": "filter"})
    r = run([sys.executable, os.path.join(QC, "vcf_regression.py"),
             "--golden", golden, "--current", out_f, "--require-info", "DP,AF,VEP",
             "--json", os.path.join(tmp, "r_f.json")])
    check(" regression FAIL rc=1 (FILTER alterado)", r.returncode == 1)
    rep = json.loads(r.stdout)
    check(" FILTER mismatch reflejado (deficit/exceso)", len(rep["deficits"]) + len(rep["excesos"]) > 0)

    print("== 6) Regression con MUTACION (order invertido) => FAIL determinismo ==")
    out_o = os.path.join(tmp, "out_o.vcf")
    run([sys.executable, os.path.join(QC, "run_pipeline_stub.py"), golden, out_o],
        env={**os.environ, "MVA_STUB_MUTATION": "order"})
    r = run([sys.executable, os.path.join(QC, "vcf_regression.py"),
             "--golden", golden, "--current", out_o, "--require-info", "DP,AF,VEP",
             "--json", os.path.join(tmp, "r_o.json")])
    check(" regression FAIL rc=1 (orden roto)", r.returncode == 1)
    rep = json.loads(r.stdout)
    check(" orden_canonico_ok=False", rep["orden_canonico_ok"] is False)

    print("\nINTEGRATION TEST: TODO PASS")

if __name__ == "__main__":
    main()
