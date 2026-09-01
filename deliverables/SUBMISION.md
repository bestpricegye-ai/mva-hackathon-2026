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
- Consolidado completo sugerido para los jueces: pendiente generar `ENTREGABLE_FINAL_MVA.md`

## Trabajo pendiente (acciones manuales del usuario)

- [ ] Subir `pitch_byronzunigao.mp4` a YouTube/Vimeo (Unlisted) → pegar URL en Submit-Track 2.
- [ ] Subir CSV + reportes en Submit-Track 1 (y Track 2) en las tabs de Synapse.
- [ ] Decidir si se versiona el video (`pitch_byronzunigao.mp4`, 4.9 MB) y `src/hacer_video.py`
      (hoy **untracked**; recomendado: commit del script del video + `video_script.md`, el mp4 puede quedarse local).
- [ ] Tras el evento: `gh repo edit bestpricegye-ai/mva-hackathon-2026 --visibility public`.
- [ ] Rotar el token `ghp_*` con scope admin tras la publicación.
- [ ] Borrar datos locales (VCF, DOCX originales, caches, `.env`) y confirmar a
      `RarediseaserealkidMVAhackathon2026@synapse.org` (regla de los 30 días).
- [ ] Citación/acknowledgement oficial del challenge en cualquier publicación.

## Estado del repo (al pre-flight)

- `master` en `6d734f9`..`d1dd04e` → últimos módulos: elegibilidad de terapia (95/100 ALTA) y
  verificación de criterios Zhang (PAM verificado en hg38, eficiencia ALTA preliminar, off-target
  pendiente CRISPOR).
- Untracked al momento: `deliverables/track2/pitch_byronzunigao.mp4`, `deliverables/track2/pitch_build/`,
  `src/hacer_video.py`.
- Auditoría de secretos pre-publicación: **OK** (tree=0 history=0, `docs/auditoria_secretos.md`).