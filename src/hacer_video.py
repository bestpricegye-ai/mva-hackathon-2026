import asyncio
import subprocess
import os
import math

from PIL import Image, ImageDraw, ImageFont

ROOT = r"C:\starquake\hackathonmva"
BUILD = os.path.join(ROOT, "deliverables", "track2", "pitch_build")
OUT = os.path.join(ROOT, "deliverables", "track2", "pitch_byronzunigao.mp4")
W, H = 1280, 720
VOICE = "es-MX-JorgeNeural"
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
        "id": "s1", "title": "Caso: MVA1 (OMIM #257300) — WGS real GRCh38",
        "accent": (255, 179, 71),
        "bullets": [
            "PROBAND01 · WGS GRCh38 + HPO clínica (8 rasgos)",
            "CIN: aneuploidía variegada en mosaico",
            "Rabdomiosarcoma en la infancia",
            "Sin tratamiento aprobado (Malumbres, Nat Rev Genet 2024)",
        ],
        "footer": "Fuente: VCF WGS_EX2312012 + clinical_history.json · OMIM #257300 · Orphanet #1052",
        "text": "Hola, soy Byron Zúñiga, del equipo byronzunigao. Presentamos un caso real de aneuploidía variegada en mosaico, MVA tipo 1, OMIM 257300: una enfermedad ultra rara. La entrada del análisis es un exoma completo en GRCh38 y el fenotipo clínico del probando. Las células pierden y ganan cromosomas por un punto de control mitótico deficiente, y el paciente desarrolló un rabdomiosarcoma. Malumbres, en Nature Reviews Genetics, confirma que hoy no existe tratamiento aprobado. Proponemos un reposicionamiento mecanismo-primero, anclado a la proteína causal.",
    },
    {
        "id": "s2", "title": "Diagnóstico molecular: BUB1B compound-het",
        "accent": (97, 205, 233),
        "bullets": [
            "p.Leu737Ter — stop-gain, PVS1 (trunca BUBR1)",
            "p.Asn1002Lys — novel, dominio quinasa · AlphaMissense 0.923",
            "BUBR1 haploinsuficiente → SAC débil",
            "Hanks 2004 (Nat Genet): bialélicas BUB1B → MVA1",
        ],
        "footer": "GRCh38: chr15:40209701 T>G + chr15:40220612 T>G · PASS QUAL 708.77 · gnomAD 3.29e-5 / novel",
        "text": "El diagnóstico se ancla al genotipo. El probando es heterocigoto compuesto en BUB1B: p.Leu737Ter, stop-gain que trunca la proteína, criterio PVS1; y p.Asn1002Lys, missense novel en el dominio quinasa, con puntaje AlphaMissense 0.923. Hanks, en Nature Genetics de dos mil cuatro, estableció que las mutaciones bialélicas de BUB1B predisponen a aneuploidía y cáncer. El resultado es BUBR1 haploinsuficiente: punto de control del huso debilitado. El defecto es de pérdida de función: lo que pide la biología es más BUBR1 funcional.",
    },
    {
        "id": "s3", "title": "Restauración de BUBR1: eje SIRT2/NAD+",
        "accent": (118, 217, 155),
        "bullets": [
            "↑BUBR1 protege de aneuploidía/cáncer · Baker, NCB 2013",
            "BUBR1 se deacetila en K668 por SIRT2 (in vivo) · North, EMBO J 2014",
            "SIRT2 = deacetilasa NAD+-dependiente",
            "NMN → NAD+ → SIRT2 → estabiliza BUBR1",
        ],
        "footer": "Ratón progeroide BubR1H/H · ↑BUBR1 = única vía publicada que sube la proteína causal",
        "text": "La literatura aporta una diana con datos in vivo. Baker, en Nature Cell Biology de dos mil trece, demostró que aumentar BUBR1 protege de aneuploidía, de cáncer y prolonga la vida sana en ratones hipomorfos. North, en EMBO Journal de dos mil catorce, precisó el mecanismo: la deacetilación de la lisina seiscientos sesenta y ocho de BUBR1, mediada por SIRT2, una deacetilasa dependiente de NAD. Su precursor, NMN, eleva NAD y vía SIRT2 incrementa BUBR1. Es la única estrategia publicada que sube directamente la proteína afectada.",
    },
    {
        "id": "s4", "title": "Seguridad: salvaguarda explícita + candidatos",
        "accent": (246, 121, 121),
        "bullets": [
            "Contraindicado: taxanos · vincristina · MPS1/TTK (debilitan el SAC)",
            "Validado: ChEMBL + Open Targets + PubMed",
            "Senolíticos (dasatinib+quercetina) → solo oncología",
            "GH → individualizada (respuesta limitada en MVA)",
        ],
        "footer": "Resultado negativo clínicamente accionable (guardrail) · Liu & Suson 2020",
        "text": "Encerramos la hipótesis en una salvaguarda de seguridad: cualquier fármaco que debilite más el punto de control mitótico está contraindicado: taxanos, vincristina, inhibidores de MPS1 o de TTK. Validamos este resultado negativo en ChEMBL, Open Targets y PubMed. Los candidatos secundarios atacan las consecuencias: senolíticos, como dasatinib con quercetina, eliminan la senescencia inflamatoria, solo bajo oncología por el sarcoma; y la hormona de crecimiento, de respuesta limitada en MVA, se individualiza.",
    },
    {
        "id": "s5", "title": "Plan integral y marco escalable",
        "accent": (143, 137, 233),
        "bullets": [
            "Vigilancia oncológica c/3 meses hasta 7 años (Orphanet · SIOP-Europe 2021)",
            "Hemograma → MDS (Laberko 2019)",
            "Régimen pediátrico de rabdomiosarcoma",
            "Genotipado parental → riesgo de recurrencia 25 %",
        ],
        "footer": "Consorcio: VERIFICACION_MANEJO_CLINICO.md (A1–A8 + 7 correcciones)",
        "text": "El manejo fue auditado por un panel médico. Vigilancia oncológica cada tres meses hasta los siete años, según Orphanet y SIOP-Europe de dos mil veintiuno; hemograma seriado para mielodisplasia, como documentó Laberko; régimen estándar de rabdomiosarcoma; rescate experimental monitoreado con NMN y NAD; senolíticos bajo oncología; y genotipado parental para cerrar el diagnóstico en trans y el riesgo de recurrencia del veinticinco por ciento por embarazo. Este marco se generaliza a otros síndromes de insuficiencia e inestabilidad cromosómica.",
    },
    {
        "id": "s6", "title": "Cierre",
        "accent": (255, 212, 96),
        "bullets": [
            "Vía traslacional, honesta y accionable",
            "Restaura la dosis de la proteína causal",
            "Pipeline reproducible F1→F6, salidas versionadas",
            "Gracias",
        ],
        "footer": "byronzunigao · MVA Hackathon 2026 · Track 1+2 · github.com/bestpricegye-ai/mva-hackathon-2026",
        "text": "A este paciente no podemos reconstruirle el punto de control hoy. Pero sí ofrecer una vía traslacional, honesta y accionable, que restaura la dosis de su proteína causal con apoyo de evidencia primaria. Reposicionar no es hallar una droga nueva para una enfermedad vieja: es escuchar qué necesita la biología de ese paciente y buscar un fármaco aprobado que ya sabe hacerlo. Gracias.",
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
    tw = d.textlength(sc["title"], font=ftitle)
    d.text((50, 36), sc["title"], font=ftitle, fill=(245, 248, 255))
    fbody = font(False, 29)
    fb = font(True, 29)
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
    segs = []
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
            segs.append(seg)
    subprocess.run(
        ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", listpath,
         "-filter_complex", f"[0:a]atempo={ATEMPO}[a]",
         "-map", "0:v", "-map", "[a]", "-c:v", "libx264", "-preset", "medium",
         "-crf", "21", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart",
         OUT],
        check=True, capture_output=True,
    )
    total = audio_duration(OUT)
    print("duraciones por escena:", {k: round(v, 2) for k, v in durations.items()})
    print("duracion total:", round(total, 2))
    print("OUT:", OUT)


if __name__ == "__main__":
    build()