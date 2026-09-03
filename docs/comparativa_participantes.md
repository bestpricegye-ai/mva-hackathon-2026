# Comparativa Completa de Participantes — MVA Hackathon 2026 (82 equipos)

**Equipo:** byronzunigao (nosotros)
**Fuente:** Leaderboard oficial (extraído por API Gradio del espacio, snapshot **3 sept 2026**, 82 filas)
**Alcance:** Comparativa 82 participantes vs nuestro trabajo, con fortalezas/debilidades y selección final.

---

## 0. Lo que el leaderboard revela (dato duro)

- **82 equipos** registrados, **76 con Rank Points = 100.0 y F-max = 1.000** (éxito total en el par BUB1B).
- **4 equipos por debajo:** kathya-sanchez (RP 50), mateooSM (RP 50), Remek (RP 25, F 0.571), y 3 a 0 pts (f6/F606, steppenwolf0, sangulfost).
- **Conclusión 1:** Track 1 **satúrado e irrelevante para diferenciación**. El caso es un estándar de oro cerrado; quien acierta el par BUB1B en rank 1 obtiene 100/1.0.
- **Conclusión 2:** la **diferenciación real ocurre en Track 2**, evaluado por panel independiente con **4 criterios: rigor científico, impacto potencial, innovación, escalabilidad**.
- **Conclusión 3:** Track 2 es **"Drug Repurposing" de medicamentos APROBADOS** (no diseño nuevo). Nuestra bioingeniería (mRNA-LNP/ASO) es el *resolver futuro*, pero el eje del track son **fármacos aprobados reposicionados** → nuestra vía NAD+/SIRT2 (NMN/NR, suplementos aprobados) y senolíticos (dasatinib+quercetina, aprobados) son los que encajan.

---

## 1. Distribución metodológica de los 82 (por nombre de archivo de submission)

| Categoría | # equipos | Ejemplos | Implicación para nosotros |
|---|---|---|---|
| **Compound-het estándar BUB1B** | 24 | noqcks, michailch, silico-evEE, gummietech… | El enfoque mayoritario; sin diferenciación. |
| **Generic / sin método visible** | 25 | bigbag, 0xbryce, psydoc, track1_predictions… | Mayoría sin mérito metodológico declarado. |
| **ACMG-based** | 8 | Gamow (sentieon+acmg), genobank, axolotl… | Clasificación ACMG = estándar, como nosotros. |
| **VEP-based** | 6 | samistus, mikerecognex, saruman, sniffle… | Herramienta de anotación, no método. |
| **Exomiser (fenotipo-gen)** | 4 | paraxaQQ, droov, swoopeagle, agentis | Priorización clínica gold-standard (fenotipo). |
| **Panel/targeted SAC** | 4 | IaSantiago, octagono, ciberpty, floodemo | Enfoque panel = como nuestro panel SAC ampliado. |
| **HPO-driven** | 3 | matcha, k-dense, ciberpty | Fenotipo→genes (como nuestro primer paso). |
| **WGS blind** | 2 | bralewild, jakeelamb | Ciego genoma-completo, sin pistas. |
| **AlphaFold / estructura** | 1 | meanjanroy | Uso de estructura proteica (cercano a nuestro PM1/dominio). |
| **Alignment-free / kmer** | 1 | ericmodesitt, antocad3, mikerecognex | Innovación algorítmica (sin alineación). |
| **CADD-tiered** | 1 | benshap | Escalado por CADD + herencia recesiva. |
| **Readthrough / GNN / fetal** | (ver Track 2) | texdata (GNN), bralewild (readthrough) | Solo estos 2 + nosotros profundizan Track 2. |

> **Lectura:** El 95% de los equipos ganó Track 1 con pipelines estándar (VEP+gnomAD+ACMG+compound-het).
> Solo una minoría aporta método diferenciado (WGS blind, kmer/alignment-free, GNN, estructura).
> **Ningún filenombre de Track 1 anuncia bioingeniería o plan clínico** → nuestro Track 2 es estructuralmente único.

---

## 2. Fortalezas y debilidades — nosotros vs el campo

### 2.1 Nuestras FORTALEZAS (ventajas defensivas)
| Fortaleza | Detalle | Contestación al campo |
|---|---|---|
| **Evidencia-first determinista** | LLM nunca toca coordenadas; escaneo de exones tabix → anotación → ACMG | 24 equipos lo resuelven igual; nosotros lo documentamos con reproducibilidad e testing (sha256 de 14 archivos) |
| **Exclusión de co-causa con paneles ampliados** | Panel SAC 24 genes + cáncer/renal; 72 variantes polimórficas benignas excluidas | Equivalente al mejor manejo de fase (mikerecognex), documentado en discard ledger |
| **Guardrail anti-mitótico explícito** | Dicotomía vincristina (SOC) vs anti-SAC (sabotaje); auditoría Fase 5 severa | Casi nadie en el campo distingue esto con severidad pediátrica |
| **Integración de la biología del variant** | Hypomorph BubR1; checkpoint roto → descarta taxanos/TTK | texdata (GNN) cometió el error y lo autocrítica; nosotros lo evitamos **desde el diseño** |
| **Plan clínico integral** | Vigilancia oncológica q3m, GH con sign-off, senolíticos under oncology, consejo reproductivo | Bienes muebles que ningún filenombre del campo declara |
| **Ruta de reemplazo génico** | mRNA-LNP BUBR1 (roadmap E1, reversibilidad 48h) | **Único** en el campo para resolver la dosis cuando la química no baste |
| **Reproducibilidad total** | 14 archivos regenerados byte-idénticos (SHA-256) | Prueba de software engineering que el panel valora en "rigor" |

### 2.2 Nuestras DEBILIDADES (ventanas de ataque del campo — a corregir)
| Debilidad | Riesgo | Corrección necesaria |
|---|---|---|
| **El foco debe abrir con aprobados, no con bioingeniería** | Panel puede puntuar "viabilidad inmediata" bajo si solo subrayamos mRNA-LNP | **RESUELTO (A1):** el reporte ahora abre con la tesis de doble vía A/B: Vía A = NMN/NAD+ vía SIRT2 (aprobado, in-vivo Baker 2013) + senolíticos (aprobados) + GH (SOC) primero; Vía B = readthrough ➔ ARNm-LNP ➔ CRISPR como ruta de futuro. El reporte «abre con el reposicionable ya», no con la ingeniería. |
| **Disclosure de LLM obligatorio** (update 28 ago 2026) | No declarar uso de IA puede descalificar | **RESUELTO (A7):** disclosure añadido a v2_BOOST (provider Anthropic/Claude, plan comercial, sin training, 30 días); el reporte base ya lo tenía (sec. 3). |
| **Pitch a 3:48/3:15 fuera de límite** | Infracción de formato = descuento | **RESUELTO (A5):** ambos videos recortados - ES=177.6s (2:57), EN=154.0s (2:34); cumplen ≤ 3:00 conservando todo el discurso (tempo 1.285, solo se quitó cola silenciosa). |
| **2 entregables con errores ACMG/K250 ya corregidos** | Corregidos en docs; falta verificar que no estén en el reporte final | **RESUELTO:** K250→K668 en la bibliografía del reporte final, ExAC 0.01%→0.005% en los 5 docs, y matriz ACMG unificada (PM2+PM1+PP3+PM3) aplicada en el reporte de submission. |

---

## 3. Progreso de los 82 — los competidores realmente fuertes (top defensa)

Solo 3-5 equipos muestran método Track 2 sustantivo en el líder (por filenames + repos conocidos):

| Competidor | Método Track 2 | Debilidad que explotamos |
|---|---|---|
| **texdata (tfius)** | GNN (TxGNN/PrimeKG) → "BubR1 undrugged" + CBP/p300 | GNN recomendó anti-mitóticos (error que autocrítica, pero no es candidato accionable); CBP/p300 es epigenéticamente promiscuo, sin in-vivo |
| **bralewild** | Screen DGIdb + readthrough → **Escina** | Escina = efecto pequeño admitido; readthrough es el mecanismo más incierto (PTC124 falló ensayos independientes); ignora el alelo missense Asn1002Lys |
| **meanjanroy (AlphaFold)** | Estructura + panel → uso de AlphaFold | Estructura in-silico sin plan clínico ni toxicidad |
| **mikerecognex** | kmer/readlevel/alignment-free + phase audit | Innovación algorítmica fuerte en Track 1, sin entregable terapéutico documentado |
| **matcha / k-dense (HPO)** | Fenotipo→genes | Sin especificidad terapéutica para MVA |

---

## 4. Selección — Los 10 candidatos sólidos más fuertes (top 10 del campo)

Criterio: solidez del método + calidad/rigor documentado + señal de Track 2, por evidencias del leaderboard y repos públicos.

| # | Equipo (handle) | Método (Track 1 / señal Track 2) | Fortaleza | Debilidad |
|---|---|---|---|---|
| 1 | **Gamow (@GamowLabs)** | Sentieon VCF + targeted ACMG (RP 100, rank1🥇) | Pipeline de grado clínico industrial (Sentieon); rank #1 | Enfoque estándar ACMG; sin Track 2 declarado |
| 2 | **bralewild** | Blind WGS triage + HPO semantic + screen readthrough→**Escina** | Método ciego + control positivo CFTR/PAH (validación robusta); candidato comercializado | Readthrough = mecanismo incierto; efecto pequeño; ignora missense |
| 3 | **texdata (tfius)** | Exomiser + GNN/PrimeKG → "BubR1 undrugged" + CBP/p300 | Análisis de knowledge-graph genuino; autocrítica honesta | GNN recomendó anti-mitóticos; CBP/p300 especulativo; sin in-vivo ni plan clínico |
| 4 | **matcha (@ChaimaeEH)** | HPO-variants-top (rank2🥈, RP 100) | Priorización fenotipo→gen limpia; rank #2 | Sin especificidad terapéutica MVA |
| 5 | **@scottmastro** | BUB1B-targeted-ACMG (rank3🥉) | ACMG targeted; rank #3 | Estándar; sin diferenciación Track 2 |
| 6 | **mikerecognex** | kmer/readlevel-verified + phase audit + VEP | Innovación alignment-free + mejor manejo de fase/discard ledger | Algoritmo fuerte Track 1, sin entregable terapéutico |
| 7 | **@ericmodesitt** | readlevel-verified-ACMG | Verificación a nivel read + ACMG | Método de verificación, no terapéutico |
| 8 | **meanjanroy** | MVA-panel + AlphaFold (estructura) | Uso de estructura proteica para priorización | In-silico sin validación funcional ni plan clínico |
| 9 | **@antocad3** | Ensemble sin alineación | Ensamble de modelos sin alineación (ingeniería) | Innovación técnica; sin Track 2 |
| 10 | **@benshap (Eleanor-)** | GO-tiered-CADD-recessive | Escalado por CADD + ontología GO + recesivo (rank4) | Std. por CADD; sin terapéutica |

> **Nota de calidad:** entre los 10 más sólidos, SOLO 2 (bralewild, texdata) son competidores reales en
> Track 2. El resto gana Track 1 con pipelines sólidos pero **no proponen terapia reposicionable**.
> Nuestro Track 2 (candidatos + plan clínico + reemplazo génico + toxicidad) **no tiene homólogo en el top 10**.

---


---

## 4.5 ¿Hay oportunidad real de ganar vs los 10 mejores? (análisis honesto)

Respuesta corta: **sí, pero solo en Track 2, y la ventana es estrecha.** Peso la evidencia:

**Por qué sí (a favor nuestro):**
- Track 1 no decide (76/82 empate a 100/1.0). Quien entre en el top-3 de Track 2 marca la diferencia real.
- De los 10 competidores más sólidos, **solo 2 (texdata, bralewild) proponen terapia reposicionable**; el resto gana Track 1 sin entregable terapéutico. Nuestro Track 2 integra: candidato aprobado con in-vivo (NAD+/SIRT2, Baker 2013) + plan clínico + resolver génico + auditoría de toxicidad pediátrica. **Ningún rival ofrece ese paquete completo.**
- Los 4 criterios del panel (rigor, impacto, innovación, escalabilidad): cubrimos los 4 en una sola propuesta, mientras texdata (innovación, débil en viabilidad) y bralewild (impacto dudoso, mecanismo incierto) cubren parcialmente.
- Diferenciadores que acabamos de blindar (A1-A8): doble vía explícita, tabla Fase-5 de toxicidad en sarcoma activo, diferencial anti-mitótico, reproducibilidad cuantificada (SHA-256, 6/6 QC), disclosure LLM, plan clínico integral.

**Por qué es estrecho (riesgos que nos quitan la victoria):**
- **texdata en innovación:** un knowledge-graph (TxGNN/PrimeKG) genuino impresiona al panel más que un razonamiento manual, aún si su candidato (CBP/p300) es especulativo. Pueden robar el criterio "innovación".
- **bralewild en rigor/validación:** su triage ciego WGS + control positivo CFTR/PAH es metodológicamente limpio y les da credibilidad de "método validado".
- **Riesgo de que el panel lea APROBADOS de forma literal** y descuente a cualquiera que acentúe no-aprobados (NMN/NAD+ es suplemento, no fármaco aprobado para MVA). Nuestra Vía A mitiga esto al abrir con GH (aprobado SOC) y senolíticos (aprobados), pero NMN/NAD+ requiere que la evidencia in-vivo hable por sí misma.
- **Jurado humano:** subjetividad. Un panel puede premiar la historia más clara; nosotros tenemos la narrativa más densa y argumentos que exigirán atención, no una lectura de 2 min.

**Veredicto ponderado:** probabilidad subjetiva de top-3 Track 2 ~40-55% (somos el único paquete completo), y de **ganar (~25-30%)** - la competencia real es texdata (innovación) y bralewild (rigor), y ambos tienen un hueco que explotamos (anti-mitótico erróneo / mecanismo incierto + alelo ignorado). Es una oportunidad genuina, no una certeza.

---

## 5. Conclusión competitiva

1. **Track 1:** 76/82 empatados a 100/1.0 → **no diferencia**. Nuestro pipeline es equivalente y reproducible.
2. **Track 2:** compiten de verdad **solo texdata, bralewild y nosotros**. Su punto débil común:
   - texdata: GNN que erró el anti-mitótico + CBP/p300 especulativo.
   - bralewild: readthrough (mecanismo incierto) como única apuesta + ignora alelo missense.
   - **Nosotros: única propuesta que integra candidato aprobado (NAD+/SIRT2 con in-vivo Baker 2013) + plan clínico + resolver génico + auditoría de toxicidad pediátrica.**
3. **Acción crítica:** reordenar el reporte Track 2 para **abrir con el reposicionamiento de aprobados** (NAD+/SIRT2, senolíticos) y presentar mRNA-LNP como futuro — alineando con el encargo del track y cerrando nuestra única ventana de debilidad.