# FASE 4 — Descubrimiento Terapéutico y Reposicionamiento
**Proyecto:** MVA Hackathon 2026 · **Equipo:** byronzunigao
**Diagnóstico:** MVA1 (OMIM 257300) — BUB1B compound-heterocigosis
**Evidencia empírica:** `data/results/fase4_mapeo_blancos.json` · **Código:** `src/fase4_mapeo_blancos.py`

---

## 4.0 Mapeo de blancos farmacológicos (Open Targets Platform v4 — resultados reales)

Se consultó la **API GraphQL pública de Open Targets Platform** (`api.platform.opentargets.org/api/v4/graphql`)
para los **10 genes del Spindle Assembly Checkpoint** (BUB1B + interactores con score ≥0.99 en STRING,
Fase 3). Se extrajo `tractability` y `drugAndClinicalCandidates` (fármacos con candidatura clínica por
blanco), clasificados por fase máxima.

### Resultado por blanco

| Blanco SAC | Fármacos clínicos | Fase máxima | Rol en SAC (según bibliografía) |
|------------|------------------|-------------|-------------------------------|
| **BUB1B** (causal) | **0** | — | Undrugged: ningún compuesto clínico modula BUBR1 |
| BUB1 | 0 | — | Undrugged |
| MAD2L1 | 0 | — | Undrugged |
| BUB3 | 0 | — | Undrugged |
| CDC20 | 0 | — | Undrugged |
| MAD1L1 | 0 | — | Undrugged |
| CENPE | 0 | — | Undrugged |
| **PLK1** | 8 | **Volasertib (Fase III)** | Inhibidores de PLK1 (antimitóticos) |
| **AURKB** | 18 | **Ibcasertib, AT-9283 (Fase III)** | Inhibidores de Aurora B (antimitóticos) |
| **TTK/MPS1** | 2 | BAY-1161909, BAY-1217389 (Fase I) | Inhibidores de MPS1 (antimitóticos) |

**7 de 10 blancos están "undrugged"** (sin candidatos clínicos), incluido el causal **BUB1B**.

### Hallazgo clave del mapeo

> Todos los fármacos que modulan los interactores del SAC son **inhibidores** de quinasas mitóticas
> (volasertib, ibcasertib, AT-9283, BAY-1161909…). En un paciente con **pérdida de función de BUB1B**,
> reducir aún más la señal del checkpoint **agravaría la aneuploidía**. Estos compuestos son
> precisamente los **contraindicados** documentados en el reporte Track 2 (anti-mitóticos / MPS1-TTK).
>
> **Interpretación:** no existe fármaco aprobado que module la vía **por activación**. El candidato
> reposicionable real debe actuar sobre la **DOSIS de BUBR1** (eje NAD+ → SIRT2 → K668), no sobre las
> quinasas del SAC. El mapeo empírico valida la hipótesis mecanismo-primero de Track 2.

---

## 4.1 Red del SAC y dianas modulables indirectamente

| Interactor | Proteína | Estrategia compensatoria (teórica) | Fármacos aprobados candidatos | Estado |
|-----------|----------|-----------------------------------|-------------------------------|--------|
| BUB1B/BUBR1 | Kinasa SAC haploinsuficiente | **Restaurar DOSIS proteica** (deacetilación SIRT2 en K668 elevada por NAD+) | **NMN/NAD+** (suplemento) | ✅ hipótesis Track 2 (evidencia in vivo) |
| — | Senescencia tisular progeroide | **Clearance de células senescentes** | **Dasatinib + Quercetina** (senolíticos) | ⚠️ investigacional |
| — | Retraso de crecimiento | Hormona de crecimiento (estándar en MVA) | **GH** | ✅ aprobado / supportive |
| PLK1/AURKB/TTK | Kinasas SAC | Inhibición NO (debilita checkpoint) | — | 🚫 **contraindicado** |
| Proteasoma | Salida de mitosis | Inhibición prolongaría fase M | Bortezomib/carfilzomib | 🚫 riesgo: toxicidad + sin respaldo causal |
| CDK4/6 | Entrada a mitosis | Reducir carga mitótica | Palbociclib | ⚠️ hipótesis no respaldada en BUB1B |
| XPO1 | Localización nuclear p53/MAD2 | Inhibición retiene MAD2 nuclear | Selinexor | ⚠️ sin datos funcionales en BUB1B |

> **Nota de rigor:** los candidatos bortezomib, carfilzomib, palbociclib, selinexor y nab-paclitaxel
> (hipótesis exploradas en el borrador inicial) carecen de respaldo funcional directo en BUB1B-LoF y, en
> su mayoría, **ejercen estrés mitótico** que un SAC defectivo no puede compensar. Se desechan en favor
> de la vía de restauración de dosis (NMN/NAD+), única con evidencia in vivo de elevar BUBR1
> (Baker et al. Nat Cell Biol 2013; North et al. EMBO J 2014).

---

## 4.2 Hipótesis de tratamiento priorizadas (análisis PK pediátrico preliminar)

### Candidato 1 — NMN / NAD+ (rescate de dosificación de BUBR1)

- **Mecanismo:** BUBR1 es deacetilado por SIRT2 en K668; la suplementación con el precursor de NAD+
  incrementa la actividad SIRT2, **eleva los niveles de BUBR1 in vivo** y reduce aneuploidía/cáncer en
  ratones hipomorfos Bub1b, extendiendo la vida media.
- **PK pediátrica:** BBB — atraviesa barrera hematoencefálica (precursor de NAD+, esencial en desarrollo
  neuronal). **CYP** — no es sustrato de CYP; metabolismo vía NMNAT (genéricamente madura en el primer
  año). **Formulación** — polvo/dispersable oral, tolerable en pediatría.
- **Dosis propuesta (a validar):** iniciar 250–500 mg/día oral en el niño (≈10–15 mg/kg), escalando bajo
  monitorización de biomarcadores (nivel de NAD+, aneuploidía por FISH en sangre periférica).
- **Riesgo/beneficio:** perfil de seguridad alto (suplemento; sin citotoxicidad); beneficio potencial
  en desarrollo neurológico y menor inestabilidad cromosómica. Requiere supervisión IRB/ético.

### Candidato 2 — Senolíticos (dasatinib + quercetina), bajo oncología

- **Mecanismo:** la insuficiencia de BUBR1 impulsa senescencia celular (p16/p19/p21/p53) que media la
  degeneración progeroide; eliminarla atenúa la fragmentación tisular (Baker et al.).
- **PK pediátrica:** dasatinib es sustrato de CYP3A4 (actividad reducida en <2 años → ajuste); quercetina
  se elimina conjugada. Ambas cruzan BBB parcialmente.
- **Restricción:** únicamente bajo equipo oncológico, dado el rabdomiosarcoma activo. Ciclos intermitentes
  con monitorización de células senescentes periféricas.

### Candidato 3 — Hormona de crecimiento (manejo estándar)

- **Mecanismo:** corrige el retraso de crecimiento/estatura baja característico de MVA (Orphanet #1052).
- **PK pediátrica:** SC; no sustrato de CYP; dosis por kg según protocolo pediátrico habitual.
- **Estado:** aprobado, supportive care — no es novedad de reposicionamiento pero forma parte del plan
  integral del paciente.

### Contraindicaciones confirmadas (resultado negativo clínicamente útil)

| Clase | Ejemplos (hallados en el mapeo Open Targets) | Razón |
|-------|----------------------------------------------|-------|
| Inhibidores PLK1 | Volasertib, onvansertib, BI-2536 | Debilitan aún más el SAC |
| Inhibidores AURKB | Ibcasertib, AT-9283, barasertib | Ídem — errores cromosómicos sin corrección |
| Inhibidores TTK/MPS1 | BAY-1161909, BAY-1217389 | Ídem — colapsan el checkpoint residual |
| Anti-mitóticos clásicos | Taxanos, vincristina | Estrés mitótico no compensable |

---

## 4.3 Estrategia clínica propuesta

1. **Genotipado de segregación parental** (cierra diagnóstico in-trans y riesgo de recurrencia 25%).
2. **Vigilancia oncológica trimestral** + régimen estándar de rabdomiosarcoma (sin antimitóticos que dañen el SAC).
3. **GH** para crecimiento.
4. **NMN/NAD+** como rescate experimental monitoreado de la dosis de BUBR1 (eje SIRT2).
5. **Senolíticos** solo bajo oncología con demostrada carga senescente.
6. **Paradigma escalable:** mapa gen haploinsuficiente → eje restaurador de dosis → barrera de seguridad de vía — generaliza a otros síndromes de inestabilidad cromosómica / haploinsuficiencia.

---

## 4.4 Evidencia 2025–2026 que refuerza el reposicionamiento (ver `docs/bibliografia_mva.md` Parte E)

- **Vacío terapéutico:** a 2026 **no existe fármaco aprobado por la FDA ni ensayo clínico reclutando para
  MVA** (UniteRare/openFDA/ClinicalTrials.gov, mar 2026; < 50 casos MVA Society) → alto impacto/escalabilidad.
- **Alelo missense con modelo murino directo:** el missense **Asn1002Lys** del probando está en el
  **residuo 1002, el modelado en ratones MVA** (`Bubr1 +/L1002P`, Sieben CJ et al., *J Clin Invest* 2020;
  OMIM 602860) → refuerza la estrategia dirigida al alelo (estabilización/readthrough del compañero missense).
- **NAD+/NMN humano:** ~10 ensayos publicados + ~13 completados + ~11 en marcha, y MIB-626 (MetroBiotech)
  en ensayos (PMC10721522; GeroScience 2024) → plataforma humana de seguridad contra la objeción "solo ratones".
- **Oncología selectiva CIN - KIF18A:** inhibidores KIF18A (AM-1882, Marquis *Nat Cancer* 2024) selectivos
  de tumores CIN, no mielosupresores, superan osteosarcoma (PMC13290091) y la clase (VLS-1488/Amgen) entró
  en **fase I/II humana** (Expert Opin Investig Drugs, 2026) — opción oncológica experimental distinta de
  los anti-SAC contraindicados.
- **Senolíticos en sobrevivientes de cáncer infantil:** SEN-SURVIVORS (NCT04733534, St. Jude) +
  precedente pediátrico de dasatinib (NCT00777036).

---

## Artefactos de Fase 4

| Artefacto | Ruta |
|-----------|------|
| Script de mapeo Open Targets | `src/fase4_mapeo_blancos.py` |
| Evidencia JSON (mapeo real) | `data/results/fase4_mapeo_blancos.json` |
| Presencia de fármacos por blanco | `data/results/_f4_sac_presencia.txt` |
| Guion video Track 2 | `deliverables/track2/video_script.md` |
| Reporte Track 2 | `deliverables/track2/byronzunigao_track2_report.md` |

---

*Documento generado con apoyo de LLM para integración de hipótesis; el mapeo de blancos es resultado
empírico de Open Targets Platform v4 (script reproducible). Ningún dato clínico identifica al paciente
más allá del texto clínico del challenge. No constituye recomendación médica.*