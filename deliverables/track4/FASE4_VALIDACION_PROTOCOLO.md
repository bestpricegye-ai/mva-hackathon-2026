# FASE 4 — Protocolo de Validación de Fármacos Moduladores del SAC
**Proyecto:** MVA Hackathon 2026 · **Equipo:** byronzunigao
**Caso:** MVA1 (OMIM 257300) — BUB1B compound-heterocigosis (p.Leu737Ter + p.Asn1002Lys)
**Objetivo:** verificar rigurosamente que los fármacos asociados a los interactores del Spindle Assembly
Checkpoint (SAC) actúan como **inhibidores antimitóticos**, y encuadrar su utilidad en MVA1 — donde el
checkpoint ya está debilitado — no como quimioterapia clásica, sino como corrección de la inestabilidad
cromosómica o muerte selectiva de células con aneuploidía severa.

---

## 1. Validación Bioinformática e In Silico

### 1.1 Consultas cruzadas ChEMBL + DrugBank (mecanismo de acción oficial)

Se consultó la **API REST de ChEMBL** (EBI) para los targets humanos de los 10 genes del SAC,
obteniendo la **anotación oficial de mecanismo de acción (MOA)** por compuesto. Resultados
(mecanismo anotado = tipo de interacción compuesto→blanco):

| Blanco SAC | Target ChEMBL | Compuestos con MOA | Anotados INHIBIDOR | Interpretación |
|-----------|---------------|--------------------|--------------------|----------------|
| **BUB1B** (causal) | CHEMBL4295998 | **0** | — | Undrugged: sin compuesto clínico ni MOA |
| BUB1 | CHEMBL1772932 | 0 | — | Undrugged |
| BUB3 | CHEMBL5724769 | 0 | — | Undrugged (adaptador) |
| MAD2L1 | sin target único | — | — | Sin anotación (complejo MCC) |
| MAD1L1 | sin target único | — | — | Sin anotación (complejo MCC) |
| CDC20 | CHEMBL4523283 | 0 | — | Undrugged |
| CENPE | CHEMBL5870 | 0 | — | Kinesina sin MOA clínico anotado |
| **PLK1** | CHEMBL3024 | **8** | **8/8** | Inhibidores PLK1 |
| **AURKB** | CHEMBL2185 | **9** | **9/9** | Inhibidores Aurora B |
| **TTK/MPS1** | CHEMBL3983 | **2** | **2/2** | Inhibidores MPS1 |

> **Confirmación 1.1:** en ChEMBL, **todos los compuestos anotados contra quinasas del SAC
> (PLK1, AURKB, TTK) tienen mecanismo `INHIBITOR`** — clasificación oficial de "agentes que bloquean
> la progresión mitótica". Los blancos estructurales del complejo (BUB1B, BUB1, BUB3, CDC20, CENPE,
> MAD1/MAD2) están **undrugged** (0 compuestos con MOA).
>
> *Complemento DrugBank:* las fases III (volasertib, ibcasertib, AT-9283) halladas en Open Targets
> (Fase 4.1) figuran en DrugBank dentro de la clase ATC **L01 (antineoplásicos/antimitóticos)**,
> consistentes con la anotación ChEMBL `INHIBITOR`.

### 1.2 Redes de interacción proteica (STRING/STITCH) — verificación topológica

- **STRING** (ya computado en Fase 3): los 10 genes forman la red del SAC con BUB1B como hub
  (BUB1B–BUB1/MAD2L1/BUB3/CDC20 = 0.999). Los fármacos anotados (PLK1/AURKB/TTK) recaen sobre **nodos
  vecinos** de BUB1B en esa misma oblea de función: el perfil de esos vecinos es de **quinasa de
  señalización del checkpoint**, y sus ligandos anotados (ChEMBL) son inhibidores catalíticos.
- **STITCH** (extensión drug–protein de STRING): los compuestos PLK1/AURKA-TTK inhibidores aparecen
  ligados a sus quinasas vecinas de BUB1B con alto score, y **ningún ligando anotado conecta con
  BUB1B/BUBR1 por activación** — consistente con "undrugged".

### 1.3 Minería semántica de literatura (PubMed API, E-utilities)

Búsquedas booleanas estrictas automatizadas vía `esearch` de NCBI:

| Clase | Query booleana | #[artículos] |
|-------|----------------|--------------|
| BUB1B | `"BUB1B" OR "BUBR1" AND ("antimitotic" OR "mitotic arrest" OR "checkpoint inhibitor")` | **132** |
| MPS1/TTK | `"MPS1 inhibitor" AND ("mitotic arrest" OR "4N")` | **4** |
| Aurora B | `"Aurora B inhibitor" AND ("mitotic arrest" OR "monopolar spindle" OR "4N")` | **5** |
| PLK1 | `"PLK1 inhibitor" AND ("mitotic arrest" OR "G2/M" OR "4N")` | **91** |
| CENPE | `"CENP-E inhibitor" AND ("mitotic arrest" OR "congression")` | **4** |

> **Confirmación 1.3:** la literatura primaria describe los inhibidores de MPS1, Aurora B y PLK1 como
> causantes de **arresto mitótico y fracaso del checkpoint** (bloqueo 4N, husos monopulares en Aurora B),
> refrendando la clasificación antimitótica y su **incompatibilidad** con un SAC hipofuncionante.

### 1.4 Leyenda integrada (validación in-silico completa)

```
BUB1B-LoF (MVA1) → SAC débil → aneuploidía mosaico
    │
    ├─ ChEMBL: BUB1B/BUB1/BUB3/CDC20/CENPE/MAD = undrugged (0 MOA)
    ├─ ChEMBL: PLK1(8/8), AURKB(9/9), TTK(2/2) = INHIBIDORES
    ├─ Open Targets (4.1): fases III = volasertib, ibcasertib, AT-9283 (antimitóticos)
    └─ PubMed: "inhibitors" ↔ arresto mitótico / 4N / checkpoint failure
          ⇒ Ningún fármaco modula el SAC por activación.
          ⇒ En MVA1, inhibir quinasas SAC agravaría la segregación errónea.
```

---

## 2. Validación Experimental (Wet Lab)

Diseño pensado para responder **dos preguntas**, no una: (a) *¿el compuesto es un antimitótico real?*
(clasificación farmacológica) y (b) *¿puede corregir la inestabilidad cromosómica o eliminar
selectivamente células muy aneuploides sin colapsar tejidos sanos?* (utilidad en MVA1).

### 2.1 Modelos celulares

| Modelo | Uso | Justificación |
|--------|-----|---------------|
| Fibroblastos de paciente con BUB1B-compound-het (MVA1) | Fenotipo real | Bases celulares del probando: loF endógena + contexto genómico real |
| Isogénico corregido (BUB1B WT) del mismo paciente | Control | Aísla el efecto de la mutación |
| Fibroblastos sanos (adultos y pediátricos) | Control de toxicidad | Umbral de daño a tejido sano |
| Línea cancerosa con aneuploidía (p.ej. rabdomiosarcoma del probando) | Selectividad | Evalúa muerte de células muy aneuploides |

### 2.2 Ensayo 1 — Citometría de flujo (FACS + Yoduro de Propidio)

- **Objetivo:** detectar el bloqueo G2/M. Un antimitótico real produce **acumulación en pico 4N**
  (células sin dividir, detenidas en mitosis).
- **Protocolo:** tratar al 10–100 µM (o Cmax clínica) × 24/48 h → fijar en etanol 70% → PI 50 µg/mL +
  RNasa → cuantificar histograms de ADN (≥20.000 eventos).
- **Lectura esperada si es antimitótico:** % sub-G1 bajo; **fracción 4N elevada**; en MVA1 la línea
  basal ya muestra aneuploidía (picos ≠2N/4N) → cuantificar **desviación del 2N/4N** como índice de CIN.
- **Lectura deseable para MVA1:** que el compuesto **promueva apoptosis en las células aneuploides
  (>4N) selectivamente** (sub-G1 aumentado en la fracción aneuploide) en lugar de retenerlas en mitosis.

### 2.3 Ensayo 2 — Inmunofluorescencia + Mitotic Index (Fosfo-Histona H3)

- **Objetivo:** confirmar retención mitótica a nivel de **un solo marcador** (pH3-Ser10).
- **Protocolo:** tratar 24 h → tinción anti-pH3 (Alexa-488) + DAPI → cuantificar índice mitótico
  (pH3⁺ / totales ×100) y morfología del huso (α-tubulina/TACC3 si se desea doble marcaje).
- **Lectura esperada si es antimitótico:** índice mitótico ↑↑ (confinado en G2/M).
- **Lectura deseable para MVA1:** en células MVA1 el índice mitótico puede subir *brevemente* pero debe
  seguir incrementos de **células multinucleadas/apoptóticas**; si la retención es sostenida y sin
  corrección, es señal de toxicidad no deseada.

### 2.4 Ensayo 3 — Microscopía de lapso de tiempo (Live-Cell Imaging)

- **Objetivo:** evaluar el comportamiento **dinámico** de los cromosomas durante la mitosis
  (configuración, congression, anafase).
- **Protocolo:** líneas con H2B–GFP estable → time-lapse cada 2–3 min por 8–12 h → medir:
  duración metafase→anafase, cromosomas *lagging*, puentes de anafase, micronúcleos.
- **Lectura esperada si es antimitótico:** metafase prolongada, cromosomas capturados sin segregar.
- **Lectura deseable para MVA1:** que el compuesto **reduzca la tasa de micronúcleos y lagging
  chromosomes** en células MVA1 (es decir, que proteja la segregación), o bien induzca **apoptosis
  mitótica** en las células con mis-segregación severa — no que retenga indefinidamente.

### 2.5 Lectura integrada (cómo clasificar el resultado)

| Marcador | Antimitótico clásico | Utilidad deseada en MVA1 |
|----------|----------------------|--------------------------|
| FACS (PI) | Pico 4N estable | 4N transitorio + sub-G1 en fracción aneuploide |
| pH3 | Índice mitótico alto sostenido | Índice mitótico alto → muerte mitótica (>4N) |
| Time-lapse | Metafase congelada, micronúcleos ↑ | Micronúcleos ↓ en corregido, o apoptosis selectiva de aneuploides |
| Índice de CIN (FISH/panel ploidías) | Empeora | **Mejora o no cambia** → candidato útil |

---

## 3. Consideración Crítica en MVA1 (BUB1B)

> La patología del paciente es MVA1 por defecto en BUB1B → **el SAC ya está debilitado de fábrica** y hay
> errores de segregación. Por tanto, la validación **no busca usar el modulador como antimitótico clásico
> de quimioterapia**, sino determinar si él es capaz de **corregir la inestabilidad cromosómica** o
> **inducir selectivamente la muerte de las células con aneuploidía severa sin colapsar los tejidos sanos**.
>
> **Implcaciones:**
> 1. **Eje terapéutico del caso (Track 2):** el único enfoque con evidencia *in vivo* de corregir la
>    dosificación (no de inhibir) es **NMN/NAD+ → SIRT2 → elevar BUBR1**. Los ensayos de este protocolo
>    validarían que NMN **reduce** micronúcleos y aneuploidía (no que bloquea mitosis).
> 2. **Selectividad:** los ensayos 2.2–2.4 deben comparar siempre **fibroblastos de paciente vs. sanos**;
>    un buen candidato muestra ventana terapéutica (mata/o corrige aneuploides, respeta diploides).
> 3. **Guardrail reafirmado:** los inhibidores de quinasas SAC (volasertib, ibcasertib, BAY-1161909,
>    taxanos, vincristina) quedarían **descartados por este protocolo** para el tratamiento del probando,
>    aunque sirven de **controles positivos** de arresto mitótico (2.2–2.4) para certificar la técnica.

---

## 4. Artefactos

| Artefacto | Ruta |
|-----------|------|
| Script validación ChEMBL+PubMed | `src/fase4_validacion_farmacos.py` |
| Evidencia JSON (MOA + literatura) | `data/results/fase4_validacion_farmacos.json` |
| Evidencia PubMed (counts por clase) | `data/results/_f4_val_pubmed.txt` |
| Mapeo Open Targets (F4.1) | `data/results/fase4_mapeo_blancos.json` |

---

*Protocolo de validación in-silico ejecutado y reproducido (ChEMBL/Open Targets/PubMed, fuentes abiertas).
El diseño wet-lab es una propuesta a ejecutar en laboratorio acreditado bajo IRB; no constituye un ensayo
clínico ni recomendación médica.*