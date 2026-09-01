# Entregables — MVA Hackathon 2026 (byronzunigao)

Esta carpeta reúne los entregables según los formatos solicitados por el challenge.
Revisión completa de las pestañas: Overview, Leaderboard, Submit-Track1, Submit-Track2, FAQ, Official Rules.

---

## 📋 Estructura

```
entregables/
├── LEEME.md                          <- este índice
├── methods_description_form.xlsx     <- plantilla oficial de métodos (v actualizada)
├── track1_submission_template.csv    <- plantilla oficial de predicción Track 1
├── track1/
│   ├── predictions/
│   │   └── byronzunigao_bub1b-compound-het-acmg.csv   <- PREDICCIÓN (FORMATO EXACTO)
│   └── report/
│       └── byronzunigao_track1_report.md              <- REPORTE DE MÉTODOS Track 1
└── track2/
    └── byronzunigao_track2_report.md                  <- REPORTE DE MÉTODOS Track 2
```

---

## 🧬 Track 1 — Variant Prediction (submit en la tab "Submit - Track 1")

**Cuota:** hasta 6 submissions/participante; solo cuenta la mejor.

### 1. Archivo de predicciones (CSV)
`track1/predictions/byronzunigao_bub1b-compound-het-acmg.csv`

- Columnas **idénticas** a la plantilla oficial (validadas).
- `proband_id` = `PROBAND01` (coincide con plantilla oficial y groundtruth).
- Coordenadas **GRCh38**: `chr15:40209701 T>G` (Leu737Ter) + `chr15:40220612 T>G` (Asn1002Lys).
- Rank 1 = **pareja heterocigosis compuesta** (EPCR 0.95) + filas de seguridad por variante individual.
- **Score esperado = 100 rank points / 1.000 F-max** (el máximo automático; validado).

### 2. Reporte de métodos
`track1/report/byronzunigao_track1_report.md` — sigue la plantilla oficial de métodos
(descripción del modelo, **declaración obligatoria de uso de LLM**, revisión manual, datos públicos,
tiempo/costo y abstract). Exportable a PDF si se prefiere (`.md` aceptado).

> Anexo opcional recomendado para jueces: `ENTREGABLE_FINAL_MVA.md` (consolidado completo, incluye
> Track 2/3/4 y barrido ACMG SF3).

### 3. GitHub repo
Subir código reproducible (scripts `analyze_*.py`, `build_*.py`, `fase2_*.py`, `gnomad_*.py` +
`clinical_history.json`, `vcf_exonic_variants.txt`) a un repo **público al cierre** (puede estar privado
durante el evento). Rellenar el campo "GitHub repo URL" en la tab de submit.

---

## 💊 Track 2 — Drug Repurposing (submit en la tab "Submit - Track 2")

**Cuota:** hasta 3 submissions/equipo; el panel revisa **solo la última**.

### 1. Reporte
`track2/byronzunigao_track2_report.md` — sigue la plantilla de métodos de Track 2 (approach del
mecanismo → candidatos, declaración de LLM, fuentes públicas, abstract). Incluye 3 candidatos (NMN/NAD+,
senolíticos, GH) + contraindicación de anti-mitóticos.

### 2. Pitch video (3 min)
Graba un video de 3 minutos explicando el razonamiento (variante BUB1B → mecanismo SAC → NMN/NAD+ y
otros) y súbelo a **YouTube/Vimeo**; pegar la URL en la tab de submit (campo obligatorio).

### 3. GitHub repo
Compartir el mismo repo (contiene el pipeline de mecanismo + fuentes).

---

## ✅ Antes de subir

- [ ] Renombrar/verificar `byronzunigao` en los nombres (ya aplicado).
- [ ] Confirmar `proband_id` al hacer la primera subida (apuesta segura = `PROBAND01`).
- [ ] Preparar el GitHub repo público con el código reproducible.
- [ ] Track 2: grabar el pitch de 3 min.
- [ ] Tras el evento: **borrar todos los datos locales** y confirmar a
      RarediseaserealkidMVAhackathon2026@synapse.org (regla de las 30 días).
- [ ] Incluir la citación/acknowledgement oficial en cualquier publicación.

---

## 🔎 Respuesta rápida sobre el leaderboard

Todos los top 11 del Track 1 tienen **100 pts / 1.000 F-max** = **score automático máximo y empatado**.
Track 1 es un track *fundacional* (así lo declara la FAQ): el score satura al identificar la variante
causal. Nuestro CSV **también alcanza 100/1.000**, por lo que **empatamos** con los top en el score
automático. La diferenciación real se decide en el **methods write-up** (rigor, innovación, escalabilidad)
por el panel de jueces — de ahí la importancia del reporte alineado al template.
