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
| Pitch video | `deliverables/track2/pitch_byronzunigao.mp4` (3:01, 1280x720, es-MX) |
| URL del video (obligatoria) | ⏳ **PENDIENTE**: subir a YouTube/Vimeo (Unlisted) y pegar aquí |
| GitHub repo URL | mismo repo de Track 1 |

Candidatos Track 2: NMN/NAD+, senolíticos, GH individualizada + contraindicación explícita de
anti-mitóticos (regla 3.1 del Consorcio).

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

- [ ] Subir `pitch_byronzunigao.mp4` a YouTube/Vimeo (Unlisted) → pegar URL en Submit-Track 2.
- [ ] Subir CSV + reportes en Submit-Track 1 (y Track 2) en las tabs de Synapse.
- [x] **Decisión tomada:** versionar el pitch (**mp4 + `pitch_build/`**) junto con `src/hacer_video.py` y
      `video_script.md` (todos ya trackeados en el repo).
- [ ] Tras el evento: `gh repo edit bestpricegye-ai/mva-hackathon-2026 --visibility public`.
- [ ] Rotar el token `ghp_*` con scope admin tras la publicación.
- [ ] Borrar datos locales (VCF, DOCX originales, caches, `.env`) y confirmar a
      `RarediseaserealkidMVAhackathon2026@synapse.org` (regla de los 30 días).
- [ ] Citación/acknowledgement oficial del challenge en cualquier publicación.

## Estado del repo (pre-subida final)

- `master` hasta `b409371` (y push final con pitch + docs) → incluye: elegibilidad de terapia génica
  (95/100 ALTA), verificación de criterios Zhang (PAM verificado en hg38, eficiencia ALTA preliminar,
  off-target pendiente CRISPOR), paper + metodología, ampliación de Fase 6 con estrategias de
  compensación/reemplazo (sección 5, E1–E4).
- **Todo versionado:** pitch mp4 + `pitch_build/`, `src/hacer_video.py`, `video_script.md`.
- Auditoría de secretos pre-publicación: **OK** (tree=0 history=0, `docs/auditoria_secretos.md`).