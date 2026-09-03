# Contrataque Track 2 v3 — Sustancial (vs campo completo de 82 + los 10 sólidos)

**Equipo:** byronzunigao
**Fecha:** 2026-09-03
**Fuente:** Leaderboard oficial completo (82 equipos, extraído por API) + análisis metodológico de filenames + repos de los competidores fuertes + estructura oficial del Track 2 (FAQ/Rules/format).

---

## 0. Reglas del juego real (lo que el panel puntúa) — base del contrataque

Del espacio oficial (FAQ + Official Rules + Track 2 submission format):

1. **Track 2 = Drug Repurposing:** *"identify existing market-approved medications whose mechanism of action may target the disease-causing pathway(s)."* → **El entregable se puntúa por reposicionar fármacos aprobados, sobre el mecanismo del variant.**
2. **4 criterios del panel:** *scientific rigor, potential impact, innovation, scalability.*
3. **Hasta 3 submissions por equipo; solo revisan la ÚLTIMA.** → Guarda la mejor para el final.
4. **Disclosure de LLM obligatoria** (update 28 ago 2026). Ya la tenemos (sección 3 del reporte base). ✓
5. **Pitch video = 3 minutos** (≤3:00). Nuestro EN mide 3:15 → **hay que recortarlo**.
6. **Requiere:** reporte PDF/MD + GitHub público con código reproducible + pitch.

**Implicación estratégica mayor:** el panel valora **scalability** y **impacto a corto plazo**. Un candidato
aprobado ya comercializado (NMN/NR, senolíticos) puntúa más en viabilidad que una bioingeniería LNP aún
preclínica. → **Nuestro reporte debe ABRIR y CERRAR con el eje de reposicionamiento de aprobados; la
ingeniería génica es el diferencial de "innovación", no el entregable de "impacto inmediato".**

---

## 1. Posición competitiva frente a los 82 (dato duro)

- **76/82** puntúan 100/1.0 en Track 1 → **el diagnóstico NO diferencia** (incluidos nosotros).
- **Solo una minoría** propone método Track 2 sustantivo:
  - **texdata (tfius):** GNN/PrimeKG → "BubR1 undrugged" → 6 vías (NAD+/SIRT2, CBP/p300, readthrough).
  - **bralewild:** screen DGIdb + readthrough → **Escina** (comercializada).
  - **nosotros:** NAD+/SIRT2 (aprobado) + senolíticos + GH + readthrough + **ARNm-LNP resolver** + plan clínico + toxicidad pediátrica.
- Los otros ~79 ganan Track 1 con pipelines estándar (VEP/gnomAD/ACMG/compound-het) y NO declaran terapia reposicionable.

**Conclusión:** la carrera de Track 2 es de facto **texdata vs bralewild vs nosotros**. Nuestro contrataque se diseña para ganar esa comparación directa, y de paso ser inalcanzable para el resto.

---

## 2. Tabla de fuerza: nosotros vs los 2 únicos competidores reales + los 8 del top

| Criterio del panel | texdata (tfius) | bralewild | **nosotros** | Veredicto |
|---|---|---|---|---|
| **Rigor científico** | Alto (GNN + autocrítica 5 errores) | Alto (controles +/- CFTR/PAH) | **Alto-Máx** (evidencia in-vivo Baker 2013 + AAAA/McElroy + reproducibilidad sha256) | Empate técnico, superiores en in-vivo |
| **Impacto potencial** | Medio (6 mecanismos sin candidato único) | Medio-Bajo (escina, efecto pequeño admitido) | **Alto** (candidato aprobado accionable NMN + plan clínico + resolver definitivo) | **Nosotros** |
| **Innovación** | Alto (knowledge-graph, detecta "undrugged") | Medio (directional filter) | **Alto** (integra biología del variant + guardrail anti-mitótico + ARNm-LNP) | Empate texdata/nosotros |
| **Escalabilidad / viabilidad inmediata** | Baja (CBP/p300 especulativo, sin in-vivo) | Medio (escina de OTC, pero readthrough incierto) | **Alta** (NMN/NR es suplemento OTC, transición a IRB logística) | **Nosotros** |

**Posición neta:** somos los únicos con **candidato aprobado + in-vivo + plan clínico + ruta definitiva**.
El riesgo es que el panel valore la innovación algorítmica de texdata por encima de la entrega clínica.
Nuestro contrataque debe hacer innegable la superioridad **clínica-translacional**.

---

## 3. Nuestra única debilidad real (ventana de ataque) y cómo cerrarla

| Debilidad | Riesgo | Acción de cierre (sustancial) |
|---|---|---|
| **Acento en bioingeniería puede leerse como fuera del encargo ("reposicionar aprobados")** | Panel baja "impacto inmediato/scalability" | **Reordenar el hilo narrativo del reporte:** Abrir con NMN/NAD+ (aprobado, lista para clínica) → senolíticos (aprobados) → readthrough (investigativo) → ARNm-LNP presentado como **fase futura de resolución**, explícitamente enmarcado como "más allá del reposicionamiento, la ruta de curación". |
| **Pitch EN 3:15 > 3:00 (infracción de formato)** | Descuento por formato | **Recortar a ≤3:00** (editar s1-s5 en `src/hacer_video_EN.py`, re-render, ffprobe de control). |
| **Filename del reporte no sigue la convención** (`usuario_track2_report.*`) | Fricción de revisión | Verificar que el archivo de submission se llama `byronzunigao_track2_report.*` en la carpeta de entrega. |
| **Sin "nota de LLM" visible en la portada del v2_BOOST** | El panel revisa la ÚLTIMA entrega; si subimos v2, debe llevar disclosure | Añadir la línea de disclosure de LLM también al v2_BOOST (o garantizar que la base con disclosure es la que se sube). |

---

## 4. El contrataque sustancial — 8 acciones integradas

> Principio rector: **mejorar lo nuestro hasta hacer inalcanzable la comparación, no copiar al rival.**

### A1. Reordenar la "pregunta del panel" con la tesis de doble vía (CRÍTICA)
Reestructurar la narrativa del reporte como:
- **Vía A — Reposicionamiento accionable HOY (aprobados):** NMN/NAD+ vía SIRT2 (top, in-vivo), senolíticos (dasatinib+quercetina), GH (con sign-off oncológico).
- **Vía B — Resolución definitiva (innovación):** readthrough PTC (investigativo), chaperonas N1002K, ARNm-LNP → CRISPR.
Cada vía con su puntaje de viabilidad (Zhang) y su auditoría Fase 5. Esta arquitectura muestra a la vez **impacto inmediato (A)** e **innovación (B)**, cubriendo los 4 criterios del panel en una sola propuesta.

### A2. Convertir el "anti-mitótico error" de texdata en nuestra evidencia diferencial
texdata documentó que su GNN recomendó paclitaxel/vinblastina (anti-mitóticos) por error, porque el grafo no sabe que el checkpoint está roto. Nosotros **lo evitamos desde el diseño**. En el reporte: una sub-sección explícita "**Por qué los anti-mitóticos están contraindicados aquí**" con la **dicotomía operativa vincristina (SOC obligado) vs TTK/MPS1 (sabotaje deliberado)** — demuestra un razonamiento de biología del mecanismo que ningún grafo puede replicar y que el panel valora como rigor.

### A3. Reforzar la cobertura de AMBOS alelos (ventaja sobre bralewild)
bralewild ataca solo el alelo nulo (readthrough del PTC Leu737Ter). Nosotros:
- **NAD+/SIRT2** sube BUBR1 **globalmente** (ambos alelos) — ataca la haploinsuficiencia en la raíz.
- **Chaperonas N1002K** estabilizan el missense del dominío quinasa (alelo 2).
- **ARNm-LNP** reemplaza la proteína completa de ambos.
Declarar esta triple cobertura en el reporte cierra la crítica de "no resuelven el missense".

### A4. Exponer la auditoría de toxicidad severa (Fase 5) como tabla por candidato
Tabla riesgo/beneficio en **contexto de sarcoma activo pediátrico** (NAD+ fueling tumoral Nacarelli 2019; GH/IGF-1 oncogénico; senolíticos antiproliferativos; aminoglucósidos nefrotóxicos vs nefrocalcinosis). Esta severidad pediátrica no existe en los repos de los 79 ni con la profundidad de texdata/bralewild. Es nuestro moat de "rigor".

### A5. Cerrar el gap de formato (video + filename)
- Recortar pitch EN a ≤3:00.
- Asegurar `byronzunigao_track2_report.*` y subir **una sola entrega final** (la mejor), respetando "solo revisan la última".
- Verificar URL del video en SUBMISION.md (pendiente).

### A6. Blindaje de reproducibilidad (ya lo tenemos, cuantificarlo en el reporte)
Documentar en el reporte que 14 entregables son **byte-idénticos tras regeneración (SHA-256)** → prueba de rigor computacional que el panel puntúa en "rigor científico". Ningún otro equipo lo declara.

### A7. Disclosure de LLM en TODAS las versiones que se suban
Ya está en la base. Si la entrega final es v2_BOOST, añadir la misma línea de disclosure (Anthropic API, Claude, términos comerciales, sin training) a su portada.

### A8. Cierre con plan clínico integral (tesis de impacto)
Cerrar el reporte con el estándar clínico: vigilancia oncológica q3m, monitoreo de mielodisplasia, régimen sarcoma estándar, GH con sign-off, consejo reproductivo (25%). **"El mejor fármaco sin plan clínico no es medicina; nosotros entregamos el plan."** Es el mensaje con más "impacto potencial" del track.

---

## 5. Los 10 candidatos sólidos del campo (de la comparativa) y cómo los superamos

| # sólido | Equipo | Su mejor activo | Nuestro contrapeso |
|---|---|---|---|
| 1 | Gamow (Sentieon+ACMG) | Pipeline grado industrial rank#1 | Solo Track 1; sin terapia → no compite en Track 2 |
| 2 | bralewild (Escina) | Control +/- CFTR/PAH; candidato comercial | Readthrough incierto; ignora missense → los superamos en cobertura de ambos alelos |
| 3 | texdata (GNN) | Detecta "BubR1 undrugged"; autocrítica | GNN recomendó anti-mitóticos; CBP/p300 especulativo → los superamos en impacto inmediato |
| 4 | matcha (HPO) | Rank#2 fenotipo→gen | Sin terapéutica MVA |
| 5 | scottmastro (ACMG) | Rank#3 ACMG | Estándar |
| 6 | mikerecognex (kmer+phase) | Algoritmo alignment-free + phase audit | Innovación Track 1; sin Track 2 |
| 7 | ericmodesitt (readlevel) | Verificación read + ACMG | Técnica de verificación |
| 8 | meanjanroy (AlphaFold) | Estructura proteica | In-silico sin plan clínico |
| 9 | antocad3 (ensemble sin alineación) | Ensemble de ingeniería | Técnica; sin terapéutica |
| 10 | benshap (CADD+GO) | Escalado CADD+ontología | Track 1 estándar |

**Conclusión:** dentro del top-10 metodológico, solo 2 tienen Track 2; los superamos en impacto (texdata) y
en cobertura/rigor (bralewild). Los otros 8 no proponen terapia -> fuera de nuestra arena.

---

## 6. Métrica de éxito y prioridades (orden de ejecución)

| # | Acción | Prioridad | Esfuerzo | Impacto en panel |
|---|---|---|---|---|
| A1 (doble vía A/B) | Alta | Alto | **Crítico** (impacto inmediato + innovación) |
| A2 (anti-mitótico diferencial) | Alta | Bajo | Alto (rigor) |
| A3 (cubrir missense) | Alta | Bajo | Alto (cobertura) |
| A4 (tabla toxicidad) | Alta | Medio | Alto (rigor pediátrico) |
| A5 (video ≤3:00 + filename) | **Crítica** | Bajo | Adherencia de formato |
| A6 (assurances sha256) | Media | Bajo | Rigor |
| A7 (disclosure en versión final) | **Crítica** | Bajo | Cumplimiento |
| A8 (plan clínico de cierre) | Alta | Bajo | Impacto |

**Secuencia recomendada:** A5 → A7 (formato) → A1 → A2/A3/A4 → A6/A8. Priorizar lo que toca el encargo
(repurposing de aprobados) y el cumplimiento de formato (video ≤3:00, disclosure, filename).

---

## 7. Verificación final antes de submission (checklist)

- [x] Pitch EN recortado a ≤3:00 — **hecho (154.0s = 2:34)**; ES recortado a 177.6s (2:57). ffprobe OK, h264 1280x720, audio 152.1s (speech intacto).
- [x] Reporte final `byronzunigao_track2_report.*` con disclosure LLM en portada — **hecho**: base EN (sección 3) y v2_BOOST (header) contienen Anthropic API/Claude, sin training, limpieza 30 días.
- [x] Reporte abre con **Vía A (aprobados: NMN/NAD+ vía SIRT2, senolíticos, GH)** y cierra con Vía B (readthrough → ARNm-LNP → CRISPR) + plan clínico — **hecho (A1 en base y v2)**.
- [x] Tabla de toxicidad Fase 5 por candidato en contexto de sarcoma activo — **hecho (A4 en base)**.
- [x] Sección “ambos alelos” (NMN global + chaperona missense + ARNm-LNP reemplazo total) — **hecho (A3)**.
- [ ] URL del video registrada en SUBMISION.md — **pendiente**: subir a YouTube/Vimeo Unlisted, pegar URL en fila 29 de SUBMISION.md. **Decision: subir EN**.
- [x] Repo GitHub público al cierre con código reproducible + sha256 — **hecho** (`docs/INFORME_REPRODUCIBILIDAD.md`, sha256=4094d92bb276810b, 6/6 QC PASS). Falta sólo push/commit final.
- [x] Una sola entrega final consolidada — base + v2 = única entrega (opener S9 de v2 actualizado).

---
### 7.1 Evidencia nueva 2025-2026 (ver `bibliografia_mva.md` Parte E) — reduce densidad narrativa
- **L1002P (E1):** el missense Asn1002Lys del probando coincide con el modelo murino `Bubr1 +/L1002P` (Sieben 2020). Ambos alelos tienen paralelo preclínico → refuerza Vía B específica.
- **KIF18A (E2):** diana selectiva de CIN ahora validada en osteosarcoma (AM-1882) y en fase I/II humana (VLS-1488/Amgen). Refuerza Vía B oncológica.
- **NMN (E3):** datos humanos de seguridad/subida NAD+ (10 publicados, 13 completados, 11 en curso; MIB-626 en ensayos). Refuerza Vía A frente a “solo ratones”.
- **Senolíticos (E4):** SEN-SURVIVORS (NCT04733534) en sobrevivientes de cáncer infantil + precedente pediátrico de dasatinib. Refuerza Vía A.
- **Revisión eje SIRT2/BubR1 (E5):** PMC11625622 consolida la Vía A + vínculo rhabdo embrionario.
- **Confirmación (E6):** UniteRare 2026 — sin fármaco aprobado ni ensayos reclutando para MVA. Argumento impacto/escalabilidad para el panel.
- **LatAm (E7):** rabdomiosarcoma reportado en región pero sin casos MVA/BUB1B en SciELO/LILACS — aporte regional.

> Decisión abierta para el usuario: incorporar un pequeño subconjunto de estas citas (E1/E2/E6 son de mayor impacto
> y específicas del probando) en el cuerpo del reporte base/v2 para anclar la narrativa, o dejarlas solo en la
> sección de literatura/Parte E. Recomendación: añadir E1 + E2 al cuerpo (anclan Vía B), y E6 como apertura
> de la sección de impacto/escalabilidad.


- [ ] Pitch EN recortado a ≤3:00 (ffprobe de control).
- [ ] Reporte final nombrado `byronzunigao_track2_report.*` (PDF/MD), con disclosure LLM en portada.
- [ ] Reporte abre con **Vía A (aprobados: NMN/NAD+ vía SIRT2, senolíticos, GH)** y cierra con Vía B (readthrough → ARNm-LNP → CRISPR) + plan clínico.
- [ ] Tabla de toxicidad Fase 5 por candidato en contexto de sarcoma activo.
- [ ] Sección "ambos alelos" (NMN global + chaperona missense + ARNm-LNP reemplazo total).
- [ ] URL del video registrada en SUBMISION.md.
- [ ] Repo GitHub público al cierre con código reproducible + sha256.
- [ ] Una sola entrega final (la mejor) para que el panel revise la correcta.