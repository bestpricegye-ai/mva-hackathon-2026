import os
import re
import subprocess
import sys

ROOT = r"C:\starquake\hackathonmva"

SECRET_PATTERNS = [
    ("GitHub token (ghp_)", r"ghp_[A-Za-z0-9]{36}"),
    ("HuggingFace token (hf_)", r"hf_[A-Za-z0-9]{30,}"),
    ("AWS access key (AKIA/ASIA)", r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b"),
    ("aws_secret_access_key", r"(?i)aws_secret_access_key\s*[=:]\s*\S+"),
    ("aws_access_key_id =", r"(?i)aws_access_key_id\s*[=:]\s*\S+"),
    ("SSH private key", r"BEGIN (?:OPENSSH|RSA|EC|DSA) PRIVATE KEY"),
    ("private key PKCS8", r"BEGIN PRIVATE KEY"),
    ("JWT", r"eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}"),
    ("API key sk-", r"\bsk-[A-Za-z0-9]{20,}"),
]

PII_PATTERNS = [
    ("email", r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"),
    ("telefono", r"(?<!\d)(?:\+?\d{1,3}[\s.-]?)?(?:\(\d{2,3}\)[\s.-]?)?\d{3}[\s.-]?\d{3,4}[\s.-]?\d{3,4}(?!\d)"),
    ("DNI/CUIL 11 digitos", r"\b\d{8}\b"),
    ("fecha nacimiento en clave", r"(?i)(fec[a-z]*\s*(?:nac|birth)|na(dio|cimi|da)\s*[=:])"),
    ("direccion", r"(?i)\b(calle|avda?\.|carrera|domicilio)\s+[A-Za-z0-9 ,.-]{5}"),
]

SENSITIVE_FILES = [
    (".env", r"\.env$"),
    ("credenciales", r"credentials(\.json|\.ini|\.txt)?$"),
    ("VCF crudo", r"\.(vcf\.gz|vcf|bam|cram|fastq|fq\.gz|bcf)$"),
    ("DOCX/XLSX crudos", r"\.(docx|xlsx|xls)$"),
    ("claves ssh", r"id_(ed25519|rsa|ecdsa|dsa)(\.pub)?$"),
]

SKIP_DIRS = {".git", ".venv", "venv", "__pycache__", "node_modules"}
SKIP_EXT = {".pyc", ".png", ".jpg", ".jpeg", ".gif", ".pdf"}
# El propio auditor no debe autodetectarse (contiene los patrones como texto).
SELF = "src/auditar_repo.py"

# PII REAL: solo se flaggea si la linea ademas contiene contexto identitario
# (evita falsos positivos de coordenadas genomicas/rsIDs/PMIDs/IDs HPO/OMIM).
PII_CONTEXT = re.compile(
    r"(?i)(dni|cuil|cuit|pasaporte|c[ée]dula|nacionalidad|nacimiento|birth"
    r"|sexo|femenino|masculino|edad|tel[ée]fono|celular|m[óo]vil|fax"
    r"|domicilio|direcci[óo]n|contacto)\s*[:=]"
)
PII_PATTERNS_REAL = [
    ("telefono", r"(?:\+?\d{1,3}[\s.-]?)?(?:\(\d{2,4}\)[\s.-]?)?\d{3,4}[\s.-]\d{3,4}[\s.-]\d{2,4}"),
    ("identidad/DNI", r"\b(?:DNI|CUIL|CUIT|PASAPORTE)\b\s*\d{6,11}\b"),
    ("nacimiento/edad", r"(?:fecha de nacimiento|birthdate|edad)\b\s*[:=]\s*\S+"),
]


def scan_text(text):
    hits = []
    for name, pat in SECRET_PATTERNS:
        for m in re.finditer(pat, text):
            hits.append((name, m.group(0)[:50]))
    return hits


def scan_pii_line(line):
    if not PII_CONTEXT.search(line):
        return []
    hits = []
    for name, pat in PII_PATTERNS_REAL:
        for m in re.finditer(pat, line):
            hits.append((name, m.group(0)[:50]))
    return hits


def tracked_files():
    import subprocess
    out = subprocess.run(
        ["git", "-C", ROOT, "ls-files"], capture_output=True, text=True, encoding="utf-8",
    ).stdout.split()
    return [os.path.join(ROOT, p.replace("/", os.sep)) for p in out]


def walk_tree():
    findings = []
    for p in tracked_files():
        rel = os.path.relpath(p, ROOT).replace("\\", "/")
        if rel == SELF:
            continue
        f = os.path.basename(p)
        ext = os.path.splitext(f)[1].lower()
        if ext in SKIP_EXT:
            continue
        for name, pat in SENSITIVE_FILES:
            if re.search(pat, f, re.IGNORECASE | re.S):
                if rel == "deliverables/methods_description_form.xlsx":
                    continue
                findings.append((name + " (nombre)", rel))
        if os.path.getsize(p) > 10_000_000:
            continue
        try:
            data = open(p, "rb").read()
            if b"\x00" in data[:8000]:
                continue
            text = data.decode("utf-8", "ignore")
        except Exception:
            continue
        for name, val in scan_text(text):
            findings.append((name, f"{rel} :: {val}"))
        for lineno, line in enumerate(text.splitlines(), 1):
            for name, val in scan_pii_line(line):
                findings.append((name, f"{rel}:{lineno} :: {val}"))
    return findings


def scan_history():
    findings = []
    commits = subprocess.run(
        ["git", "-C", ROOT, "rev-list", "--all"],
        capture_output=True, text=True, encoding="utf-8",
    ).stdout.split()
    pats = SECRET_PATTERNS
    for c in commits:
        try:
            out = subprocess.run(
                ["git", "-C", ROOT, "grep", "-n", "-I", "-E",
                 "|".join(f"({p})" for _, p in pats), c],
                capture_output=True, text=True, encoding="utf-8",
            )
        except Exception:
            continue
        if out.returncode == 0 and out.stdout.strip():
            for line in out.stdout.splitlines():
                findings.append((f"historial {c[:8]}", line[:120]))
    return findings


if __name__ == "__main__":
    tree = walk_tree()
    hist = scan_history()
    print("=== WORKING TREE / PII / SENSITIVE FILES ===")
    for n, v in tree:
        print(f"[{n}] {v}")
    print("=== HISTORY ===")
    for n, v in hist:
        print(f"[{n}] {v}")
    print(f"--- TOTAL: tree={len(tree)} history={len(hist)} ---")
    sys.exit(0 if not tree and not hist else 1)