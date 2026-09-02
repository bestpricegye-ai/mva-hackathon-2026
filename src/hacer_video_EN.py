import asyncio
import subprocess
import os

from PIL import Image, ImageDraw, ImageFont

ROOT = r"C:\starquake\hackathonmva"
BUILD = os.path.join(ROOT, "deliverables", "track2", "pitch_build_EN")
OUT = os.path.join(ROOT, "deliverables", "track2", "pitch_byronzunigao_EN.mp4")
W, H = 1280, 720
VOICE = "en-US-ChristopherNeural"
EXTRA = 0.6
ATEMPO = 1.285

FONT_DIR = r"C:\Windows\Fonts"

def font(bold=False, size=28):
    names = (["segoeuib.ttf", "segoeui.ttf"] if bold else ["segoeui.ttf", "segoeui.ttf"])\
        + ["arial.ttf"]
    for n in names:
        p = os.path.join(FONT_DIR, n)
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                pass
    return ImageFont.load_default()

SCENES = [
    {
        "id": "s1", "title": "Case: MVA1 (OMIM #257300) - real WGS on GRCh38",
        "accent": (255, 179, 71),
        "bullets": [
            "PROBAND01 - WGS GRCh38 + clinical HPO (8 traits)",
            "CIN: mosaic variegated aneuploidy",
            "Childhood rhabdomyosarcoma",
            "No approved treatment (Malumbres, Nat Rev Genet 2024)",
        ],
        "footer": "Source: VCF WGS_EX2312012 + clinical_history.json - OMIM #257300 - Orphanet #1052",
        "text": "Hello, I am Byron Zuniga of team byronzunigao. This is a real case of mosaic variegated aneuploidy, MVA type 1, OMIM 257300, an ultra rare disease. The input is a whole exome on GRCh38 and the proband phenotype. Cells gain and lose chromosomes from a defective mitotic checkpoint, and the patient developed rhabdomyosarcoma. No approved treatment exists, so we propose a mechanism-first repurposing anchored to the causal protein.",
    },
    {
        "id": "s2", "title": "Molecular diagnosis: compound-heterozygous BUB1B",
        "accent": (97, 205, 233),
        "bullets": [
            "p.Leu737Ter - stop-gain, PVS1 (truncates BUBR1)",
            "p.Asn1002Lys - novel, kinase domain - AlphaMissense 0.923",
            "Haploinsufficient BUBR1 - weak SAC",
            "Hanks 2004 (Nat Genet): biallelic BUB1B - MVA1",
        ],
        "footer": "GRCh38: chr15:40209701 T>G + chr15:40220612 T>G - PASS QUAL 708.77 - gnomAD 3.29e-5 / novel",
        "text": "The diagnosis is anchored to the genotype. The proband is compound heterozygous in BUB1B: p.Leu737Ter, a stop gain that truncates the protein, PVS1; and p.Asn1002Lys, a novel missense in the kinase domain, AlphaMissense zero point nine two three. Biallelic BUB1B mutations predispose to aneuploidy and cancer. The result is haploinsufficient BUBR1, a weakened spindle assembly checkpoint. The defect is loss of function; the biology demands more functional BUBR1.",
    },
    {
        "id": "s3", "title": "Restoring BUBR1: the SIRT2/NAD+ axis",
        "accent": (118, 217, 155),
        "bullets": [
            "More BUBR1 protects against aneuploidy/cancer - Baker, NCB 2013",
            "BUBR1 deacetylated at K668 by SIRT2 (in vivo) - North, EMBO J 2014",
            "SIRT2 = NAD+-dependent deacetylase",
            "NMN - NAD+ - SIRT2 - stabilizes BUBR1",
        ],
        "footer": "Progeroid mouse BubR1H/H - more BUBR1 = only published route that raises the causal protein",
        "text": "The literature provides a target with in vivo data. Baker showed that raising BUBR1 protects against aneuploidy and cancer and extends healthy lifespan in hypomorphic mice. North defined the mechanism: deacetylation of lysine six hundred sixty eight of BUBR1 by SIRT2, a NAD dependent deacetylase. Its precursor, NMN, raises NAD and, through SIRT2, increases BUBR1. This is the only published strategy that directly raises the affected protein.",
    },
    {
        "id": "s4", "title": "Safety: explicit safeguard + candidates",
        "accent": (246, 121, 121),
        "bullets": [
            "Contraindicated: taxanes - vincristine - MPS1/TTK (weaken the SAC)",
            "Validated: ChEMBL + Open Targets + PubMed",
            "Senolytics (dasatinib+quercetin) - oncology only",
            "GH - individualized (limited response in MVA)",
        ],
        "footer": "Clinically actionable negative result (guardrail) - Liu & Suson 2020",
        "text": "We enclose the hypothesis in a safety safeguard: any drug that weakens the mitotic checkpoint further is contraindicated: taxanes, vincristine, MPS1 or TTK inhibitors. We validated this in ChEMBL, Open Targets and PubMed. Secondary candidates address the consequences: senolytics, such as dasatinib with quercetin, clear inflammatory senescence, only under oncology because of the sarcoma; and growth hormone, of limited response in MVA, is individualized.",
    },
    {
        "id": "s5", "title": "Integrated plan and scalable framework",
        "accent": (143, 137, 233),
        "bullets": [
            "Oncology surveillance q3mo until age 7 (Orphanet - SIOP-Europe 2021)",
            "Serial blood counts - MDS (Laberko 2019)",
            "Standard pediatric rhabdomyosarcoma regimen",
            "Parental genotyping - 25% recurrence risk",
        ],
        "footer": "Consortium: VERIFICACION_MANEJO_CLINICO.md (A1-A8 + 7 corrections)",
        "text": "The management was audited by a medical panel. Oncology surveillance every three months until age seven, per Orphanet and SIOP Europe; serial blood counts for myelodysplasia, per Laberko; the standard rhabdomyosarcoma regimen; a monitored experimental rescue with NMN and NAD; senolytics under oncology; and parental genotyping to close the in trans diagnosis and the twenty five percent recurrence risk. This framework generalizes to other instability syndromes.",
    },
    {
        "id": "s6", "title": "Closing",
        "accent": (255, 212, 96),
        "bullets": [
            "Translational, honest and actionable path",
            "Restores the dosage of the causal protein",
            "Reproducible F1-F6 pipeline, versioned outputs",
            "Thank you",
        ],
        "footer": "byronzunigao - MVA Hackathon 2026 - Track 1+2 - github.com/bestpricegye-ai/mva-hackathon-2026",
        "text": "For this patient, we cannot rebuild the checkpoint today. But we can offer a translational, honest and actionable path that restores the dosage of the causal protein. Repurposing is listening to what that patient's biology needs and finding an approved drug that already knows how to do it. Thank you.",
    },
]


def render_slide(idx, sc):
    img = Image.new("RGB", (W, H), (16, 24, 44))
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, 10], fill=sc["accent"])
    d.rectangle([0, 10, W, 138], fill=(22, 32, 58))
    d.line([0, 138, W, 138], fill=sc["accent"], width=3)
    fnum = font(True, 22)
    d.text((W - 70, 16), f"{idx:02d}", font=fnum, fill=(120, 140, 170))
    ftitle = font(True, 40)
    d.text((50, 36), sc["title"], font=ftitle, fill=(245, 248, 255))
    fbody = font(False, 29)
    y = 182
    for b in sc["bullets"]:
        d.ellipse([58, y + 13, 66, y + 21], fill=sc["accent"])
        d.text((82, y), b, font=fbody, fill=(225, 232, 246))
        y += 46
    ff = font(True, 25)
    d.text((50, H - 62), sc["footer"], font=ff, fill=sc["accent"])
    return img


async def tts(text, path):
    import edge_tts
    cm = edge_tts.Communicate(text, VOICE, rate="-4%")
    await cm.save(path)


def make_audio(idx, text, path):
    asyncio.run(tts(text, path))
    return audio_duration(path)


def audio_duration(path):
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=nw=1:nk=1", path],
        capture_output=True, text=True,
    ).stdout.strip()
    return float(out) if out else 0.0


def build():
    os.makedirs(BUILD, exist_ok=True)
    durations = {}
    listpath = os.path.join(BUILD, "concat.txt")
    with open(listpath, "w", encoding="utf-8") as lst:
        for i, sc in enumerate(SCENES, 1):
            idx = sc["id"]
            img_path = os.path.join(BUILD, f"{idx}.png")
            img = render_slide(i, sc)
            img.save(img_path)
            mp3 = os.path.join(BUILD, f"{idx}.mp3")
            dur = make_audio(i, sc["text"], mp3) + EXTRA
            durations[idx] = dur
            seg = os.path.join(BUILD, f"{idx}.mp4")
            cmd = [
                "ffmpeg", "-y", "-loop", "1", "-framerate", "30", "-i", img_path,
                "-i", mp3, "-vf", f"scale={W}:{H},format=yuv420p",
                "-t", f"{dur:.2f}", "-c:v", "libx264", "-preset", "medium",
                "-crf", "21", "-c:a", "aac", "-b:a", "192k", "-ar", "44100",
                "-shortest", "-avoid_negative_ts", "make_zero", seg,
            ]
            subprocess.run(cmd, check=True, capture_output=True)
            lst.write(f"file '{os.path.abspath(seg).replace(chr(39), '')}'\n")
    subprocess.run(
        ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", listpath,
         "-filter_complex", f"[0:a]atempo={ATEMPO}[a]",
         "-map", "0:v", "-map", "[a]", "-c:v", "libx264", "-preset", "medium",
         "-crf", "21", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart",
         OUT],
        check=True, capture_output=True,
    )
    total = audio_duration(OUT)
    print("durations per scene:", {k: round(v, 2) for k, v in durations.items()})
    print("total duration:", round(total, 2))
    print("OUT:", OUT)


if __name__ == "__main__":
    build()
