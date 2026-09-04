?# Entregables — MVA Hackathon 2026 (byronzunigao)

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
├── track2/
│   ├── byronzunigao_track2_report_FINAL.md            <- REPORTE ÚNICO/CANÓNICO Track 2 (entrega)
│   ├── byronzunigao_track2_report.md                  <- base EN (plantilla 1-11, respaldo histórico)
│   ├── byronzunigao_track2_report_EN.md               <- copia byte-idéntica del base (respaldo)
│   ├── byronzunigao_track2_report_v2_BOOST.md         <- refuerzos 7 puntos (respaldo)
│   ├── video_script.md / video_script_EN.md           <- SCRIPT del pitch (ES/EN)
│   ├── pitch_byronzunigao.mp4                         <- PITCH GRABADO (2:57/177.6s, es-MX)
│   ├── pitch_byronzunigao_EN.mp4                      <- PITCH EN (2:34/154.0s, en-US) — recorte ≤3:00 (recomendado)
│   └── pitch_build/ + pitch_build_EN/                 <- assets de montaje del video
├── track4/
│   ├── FASE4_REPOSICIONAMIENTO.md                     <- Descubrimiento terapéutico (track 4)
│   └── FASE4_VALIDACION_PROTOCOLO.md                  <- Validación en bases públicas
├── consorcio/
│   ├── EVALUACION_5_FASES.md                          <- Auditoría interna de las 5 fases
│   ├── VERIFICACION_MANEJO_CLINICO.md                 <- Veredicto médico del manejo MVA1
│   ├── CONTRASTE_PLATAFORMAS_2026.md                  <- Contraste de plataformas 2026
│   └── INFORME_REVISION_CRITICA_COMITE.md             <- Revisión crítica del comité
└── (SUBMISION.md, pitch_byronzunigao.mp4)             <- pre-flight + assets
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
`track2/byronzunigao_track2_report_FINAL.md` — **entrega ÚNICA y canónica** de Track 2. Sigue la plantilla
de métodos (approach del mecanismo → candidatos, declaración de LLM, fuentes públicas, abstract) y **consolida**:
el reporte base (plantilla 1-11) + los 7 puntos de refuerzo del v2_BOOST (readthrough candidato #4, dicotomía
clínica vincristina vs TTK/MPS1, ARNm-LNP como sección propia, control NMN/NAD+, plan clínico integrado, tabla
de toxicidad Fase-5 por candidato, matriz competitiva) + evidencia 2025-2026 (E1-E7: paralelo murino L1002P,
vacío terapéutico 2026, KIF18A, NMN humano) + matriz de trazabilidad por fuente. Estrategia de **doble vía**:
Vía A (rescate de dosis con agentes aprobados: NMN/NAD+ vía SIRT2, senolíticos, GH) + Vía B (reparación de
alelo: readthrough → ARNm-LNP → CRISPR), con guardrail dicotómico anti-mitótico (TTK/MPS1 contraindicados,
vincristina SOC con monitorización) y auditoría de toxicidad Fase-5 por candidato en sarcoma activo.
Los archivos `byronzunigao_track2_report.md`, `_EN.md` y `_v2_BOOST.md` se conservan **solo como respaldo de
trazabilidad**; no se suben para evitar duplicidad (el panel revisa solo la última submission).

### 2. Pitch video (3 min)
Video de 3 minutos explicando el razonamiento (variante BUB1B → mecanismo SAC → NMN/NAD+ y otros):
- **Grabado ES:** `track2/pitch_byronzunigao.mp4` (**2:57/177.6s**, 1280x720, es-MX) — versionado.
- **Grabado EN:** `track2/pitch_byronzunigao_EN.mp4` (**2:34/154.0s**, 1280x720, en-US) — recorte a ≤3:00 cumplido. **Recomendado subir EN** (mayor margen + panel internacional).
- **Scripts:** `track2/video_script.md` + `video_script_EN.md` · **Assets:** `track2/pitch_build/` + `pitch_build_EN/`.
- **Pendiente (manual):** subir a **YouTube/Vimeo** (Unlisted) y **pegar la URL** en la tab de submit
  (campo obligatorio).

### 3. GitHub repo
Compartir el mismo repo (contiene el pipeline de mecanismo + fuentes).

---

## ✅ Antes de subir

- [x] Renombrar/verificar `byronzunigao` en los nombres (ya aplicado).
- [x] Confirmar `proband_id` = `PROBAND01` (apuesta segura = `PROBAND01`).
- [x] Archivos de reproducibilidad versionados: `vcf_exonic_variants.txt`,
      `vcf_acmg_scan.txt`, `vcf_sac_panel_variants.txt`, `vcf_panel2_variants.txt`
      (en `data/results/`, byte-idénticos al pipeline reproducido) + `clinical_history.json`,
      `src/config.py` y scripts parametrizados.
- [x] Verificación dirigida de la región chr15:40.19-40.23 Mb desde VCF
      (`docs/verificacion_dirigida_vcf.md`) y registro de decisión sobre reads
      (`docs/decision_reads_no_analizados.md`).
- [x] Veredicto médico del manejo clínico MVA1 (`consorcio/VERIFICACION_MANEJO_CLINICO.md`).
- [x] Track 2: **pitch grabado y recortado a ≤3:00** — ES `track2/pitch_byronzunigao.mp4` (2:57/177.6s) + EN `track2/pitch_byronzunigao_EN.mp4` (2:34/154.0s) — **falta pegar la URL** (YouTube/Vimeo) en la tab Submit-Track2.
- [x] Track 2: **pitch mp4 + `pitch_build/` versionados** en el repo (decisión de equipo).
- [x] Documentación de metodología y paper científico (`docs/PAPER_CIENTIFICO_MVA.md`,
      `docs/METODOLOGIA_FLUJOGRAMA.md`) y ampliación de Fase 6 con estrategias de compensación/
      reemplazo (`docs/fase6_zhang_influence.md`, sección 5, E1–E4).
- [x] **GitHub repo** creado y pusheado: `https://github.com/bestpricegye-ai/mva-hackathon-2026`
      (privado; pegar la URL en la tab de submit — el LEEME recomienda hacerlo público al cierre).
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

