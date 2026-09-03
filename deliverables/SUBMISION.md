# Pre-flight de subida — MVA Hackathon 2026 (byronzunigao)

Checklist operativo para completar las pestañas de submit del challenge con los archivos
ya generados en `deliverables/`. Marca cada ítem y rellena lo que falte.

---

## Pestaña Submit-Track 1 (hasta 6 submissions; la mejor cuenta)

| Campo | Valor |
|---|---|
| Archivo de predicciones | `deliverables/track1/predictions/byronzunigao_bub1b-compound-het-acmg.csv` |
| Formato | Columnas idénticas a `track1_submission_template.csv` ✅ |
| Reporte de métodos | `deliverables/track1/report/byronzunigao_track1_report.md` (o export a PDF) |
| GitHub repo URL | `https://github.com/bestpricegye-ai/mva-hackathon-2026` (privado durante el evento; público al cierre) |
| Score esperado | 100 rank points / 1.000 F-max (máximo automático; el track se decide en el write-up por jueces) |

Contenido del CSV (4 filas, verificado):
- Fila 1: PROBAND01 · chr15:40209701 T>G + chr15:40220612 T>G · epcr 0.95 · compound-het BUB1B (MVA1)
- Filas 2-3: seguridad por variante individual (0.50 / 0.40)

## Pestaña Submit-Track 2 (hasta 3 submissions; el panel solo revisa la última)

| Campo | Valor |
|---|---|
| Reporte | `deliverables/track2/byronzunigao_track2_report.md` |
| Pitch video (ES) | `deliverables/track2/pitch_byronzunigao.mp4` (ES, **177.6s / 2:57**, 1280x720, es-MX) |
| Pitch video (EN) | `deliverables/track2/pitch_byronzunigao_EN.mp4` (EN, **154.0s / 2:34**, 1280x720, en-US) - recorte a <= 3:00 cumplido (2026-09-03) |
| URL del video (obligatoria) | ⏳ **PENDIENTE**: subir a YouTube/Vimeo (Unlisted) y pegar aquí |
| GitHub repo URL | mismo repo de Track 1 |

> **Estado de duraciones CORREGIDO (re-medido 2026-09-03 con ffprobe):**
> - `pitch_byronzunigao.mp4` (ES) = **177.6 s (2:57)** - recortado desde 227.5s (eliminada la cola
>   silenciosa; discurso completo a tempo natural 1.285, audio 177.1s). **Cumple límite 3:00** (margen 2.4s).
> - `pitch_byronzunigao_EN.mp4` (EN) = **154.0 s (2:34)** - recortado desde 195.4s (eliminada la cola
>   silenciosa; audio 152.1s). **Cumple límite 3:00** (margen 26s).
> - Ambos conservan TODO el discurso a tempo natural (1.285); solo se recortó el silencio de cola
>   que inflaba la duración. **Recomendado EN** (mayor margen + audiencia internacional del panel).

Candidatos Track 2: NMN/NAD+, senolíticos, GH individualizada + contraindicación explícita de
anti-mitóticos (regla 3.1 del Consorcio). + `byronzunigao_track2_report_v2_BOOST.md` (ampliación
contrataque 7 puntos, complementario del reporte base).

## Otros entregables (para jueces, opcional)

- `deliverables/methods_description_form.xlsx` (plantilla oficial de métodos, actualizada)
- `deliverables/consorcio/VERIFICACION_MANEJO_CLINICO.md` (veredicto médico MVA1)
- `deliverables/consorcio/EVALUACION_5_FASES.md`
- Track 4 (opcional): `deliverables/track4/FASE4_REPOSICIONAMIENTO.md` + `FASE4_VALIDACION_PROTOCOLO.md`
- `docs/ENTREGABLE_FINAL_MVA.md` (consolidado completo para jueces, incluye Track 2/3/4 + ACMG SF3)
- `docs/PAPER_CIENTIFICO_MVA.md` (paper científico con citas y discusión metodológica)
- `docs/METODOLOGIA_FLUJOGRAMA.md` (metodología + flujograma + manual + bitácora de API)
- `docs/INFORME_REPRODUCIBILIDAD.md` + `docs/INFORME_TESTING_FRAMEWORK.md`
  (18 entregables byte-idénticos, SHA-256; framework QC 6/6 PASS)

## Trabajo pendiente (acciones manuales del usuario)

- [x] **Pitch resuelto (2026-09-03):** ES = 177.6s (2:57) y EN = 154.0s (2:34); ambos cumplen el límite 3:00. Decisión: **subir EN** (mayor margen + panel internacional).
- [x] **Recorte ejecutado (2026-09-03):** ambos videos recortados al eliminar silencio de cola (ES 177.6s, EN 154.0s), re-ensamblados desde `pitch_build/` y `pitch_build_EN/` a tempo natural 1.285.
- [ ] Subir el pitch elegido a YouTube/Vimeo (Unlisted) → pegar URL en Submit-Track 2.
- [ ] Subir CSV + reportes en Submit-Track 1 (y Track 2) en las tabs de Synapse.
- [x] **Decisión tomada:** versionar el pitch (**mp4 + `pitch_build/`** y **`pitch_build_EN/`**) junto con
      `src/hacer_video.py` y `video_script.md` (todos ya trackeados en el repo).
- [ ] Tras el evento: `gh repo edit bestpricegye-ai/mva-hackathon-2026 --visibility public`.
- [ ] Rotar el token `ghp_*` con scope admin tras la publicación.
- [ ] Borrar datos locales (VCF, DOCX originales, caches, `.env`) y confirmar a
      `RarediseaserealkidMVAhackathon2026@synapse.org` (regla de los 30 días).
- [ ] Citación/acknowledgement oficial del challenge en cualquier publicación.

## Estado del repo (pre-subida final)

- `master` hasta `66dcdef` (push final pendiente hasta confirmar selección de pitch) → incluye:
  elegibilidad de terapia génica (95/100 ALTA), verificación de criterios Zhang, paper + metodología,
  ampliación de Fase 6 (E1–E4), entregables EN (`track1_report_EN`, `track2_report_EN`,
  `video_script_EN`), `track2_report_v2_BOOST` (contrataque 7 puntos), `docs/contrarataque_track2.md`,
  comparativa leaderboard 2026-09-02, y pitch EN (`pitch_byronzunigao_EN.mp4` + `pitch_build_EN/` +
  `src/hacer_video_EN.py`).
- **Todo versionado:** pitch mp4 ES + EN + `pitch_build/` + `pitch_build_EN/`, `src/hacer_video.py`,
  `src/hacer_video_EN.py`, `video_script.md` + `video_script_EN.md`.
- Auditoría de secretos pre-publicación: **OK** (tree=0 history=0, `docs/auditoria_secretos.md`).
  Datos de paciente (VCF/WGS `WGS_EX2312012_*.vcf.gz`) siguen **ignorados** (.gitignore).