# FASE 6 — Zhang_Influence: Terapia Génica Programable para MVA1
## Biología de síntesis + ingeniería genética programable para corregir BUB1B

**Enfermedad objetivo:** Mosaic Variegated Anueploidy Syndrome 1 (MVA1, OMIM #257300)
**Gen causal:** BUB1B (BubR1, HGNC:1149, chr15:40.2 Mb, GRCh38)
**Genotipo paciente:** compound-heterocigoto BUB1B
  - Alele 1: chr15:40209701 T>G → c.2210T>G p.(Leu737Ter) — stop_gained (LoF)
  - Alele 2: chr15:40220612 T>G → c.3006T>G p.(Asn1002Lys) — missense (AlphaMissense 0.923)
**Herencia:** Autosomal recesivo
**Fenotipo:** Disregulación mitótica (aneuploidía variegada, predisposición a cáncer, retraso del crecimiento, alteraciones renales y perinatales)

---

## 1. Aplicación de los 4 métodos de Zhang_Influence a MVA1

### 1.1 Edición Génica de Precisión CRISPR-Cas9 (corrección definitiva)

**Objetivo:** Corregir ambos alelos BUB1B en células del paciente para restaurar la función completa de BubR1.

**Estrategia propuesta — corrección de exones:**

| Alele | Variante | Estrategia CRISPR-Cas9 |
|---|---|---|
| **Leu737Ter** (T>G chr15:40209701) | stop_gained en c.2210 | Corrección por HDR con plantilla sintética que restaure T>G → T (o ablación del sitio de corte para eliminar el stop premature) |
| **Asn1002Lys** (T>G chr15:40220612) | missense en quinasa C-term | Corrección por HDR: restablecer T>G → T para recuperar Asn1002, o edición base (adenina base editor) para convertir el Lys en Asn |

**Diseño de guías RNA (prototipo):**
- **gRNA-L737Ter:** dirigida a chr15:40209701 (±20 nt flanqueo), PAM NGG → corta a ~3 bp del error
- **gRNA-N1002K:** dirigida a chr15:40220612 (±20 nt), PAM NGG → corta cerca del codón 1002

**Vectores de reparación (donor):**
- Plantillas ssDNA con secuencia corregida + homologías laterales (500–800 bp)
- Para N1002K: ABE (adenine base editor) → A→G en el ADN complementario para revertir el Lys a Asn sin doble cadena

**Modelo celular de validación:**
- Fibroblastos del paciente (biopsia cutánea) → reprogramación a iPSC → diferenciación a progenitores hematopoyéticos
- Correción ex vivo + trasplante autólogo de células madre hematopoyéticas (HSC) corregidas

**Viabilidad:** ALTA — MVA1 es monogénico, las mutaciones son puntuales (ideales para HDR/ABE), y el fenotipo requiere restauración de función (no supresión, por lo que la corrección es beneficiosa y no oncogénica).

**Limitación:** BUB1B es grande (~30 exones). La corrección de ambos aleles requiere doble golpe en el mismo locus, lo que reduce eficiencia de HDR. Estrategia alternativa: **corrección alélica individual con donor específico por mutación**.

---

### 1.2 Edición Transitoria de ARN con CRISPR-Cas13 (puente terapéutico)

**Objetivo:** Corregir transitoriamente el ARNm mutado de BUB1B para restaurar temporalmente la proteína BubR1 funcional, mientras se desarrolla la terapia génica permanente.

**Mecanismo:**
- **Cas13** (dirigida a ARN, no ADN) + gRNA específica del transcrito mutado
- Modificación temporal de la traducción:
  - Para el transcrito p.Leu737Ter: Cas13 puede dirigirse al ARNm mutado y degradarlo selectivamente (RNA editing / RNA knockdown del alelo mutado) + expresión del alelo salvaje restante (si hay nivel residual)
  - Alternativa: **RNA base editing (ADAR)** → conversión temporal del codón mutado

**Ventaja médica para MVA1:**
- MVA1 requiere función BUB1B en células **dividiéndose** (mielopoiesis, embriogénesis). Una corrección transitoria en progenitores hematopoyéticos podría ser suficiente para un episodio terapéutico.
- **Sin alteración permanente del genoma** → seguridad en pacientes jóvenes (riesgo oncológico reducido).
- Ideal para pacientes que no son candidatos inmediatos a edición génica de ADN.

**Limitación:** Efecto transitorio (semafora 2–4 semanas) → requiere re-dosis o combinación con terapia génica permanente.

---

### 1.3 Cribado Genómico CRISPR (identificación de dianas y resistencia)

**Objetivo:** Descubrir modificadores genéticos y rutas compensatorias que mitiguen el fenotipo de pérdida de BUB1B.

**Pantallas propuestas:**

| Pantalla | Propósito | Modelo |
|---|---|---|
| **Knockout screen** (ko-CRISPR) | Identificar genes cuya pérdida compensa la deficiencia de BubR1 (supresores sintéticos) | iPSC del paciente → diferenciación a progenitores con BUB1B KO |
| **CRISPR activation (CRISPRa)** | Sobre-expresores que restauren el checkpoint mitótico | Línea celular con BUB1B bajo expresión inducible |
| **Screen de sensibilidad a aneuploidía** | Identificar genes que agravan o suprimen la aneuploidía en ausencia de BUB1B | Líneas con BUB1B haploinsuficiente |

**Candidatos a identificar (hipótesis basada en la red del checkpoint):**
- **BUB1** (paralogo): sobre-expresión podría compensar parcialmente la pérdida de BUB1B
- **MAD2L1 / MAD1L1** (clientes directos de BubR1): amplificación podría estabilizar el complejo mitótico
- **TTK (Mps1)** / **AURKB** / **PLK1**: kinases del checkpoint que podrían modular la severidad del fenotipo
- Genes de la vía de **respuesta al daño del ADN (DDR)** que convergen con el checkpoint

**Resultado esperado:** Identificar un "cocktail genético" de modificadores que reduzcan la severidad del fenotipo MVA1, permitiendo (a) una estratificación de riesgo más precisa y (b) nuevas dianas farmacológicas.

---

### 1.4 Plataforma SEND (Entrega Segura de Terapia Génica)

**Objetivo:** Empaquetar los componentes CRISPR-Cas9 o Cas13 para entrega segura y re-administrable en pacientes con MVA1.

**Aplicación a MVA1:**
- **Proteína PEG10** (humana, natural) → empaqueta mRNA de Cas9 + gRNA en partículas similares a virus (VLPs)
- **Ventaja para MVA1:**
  - BUB1B se expresa en células madre hematopoyéticas (HSC) y progenitoras → entrega in vivo a médula ósea
  - PEG10 evita inmunogenicidad → re-dosis posible (importante para pacientes pediátricos)
  - Componentes propios del cuerpo → menor rechazo inmune vs. AAV/LNP convencionales

**Estrategia de entrega:**
1. **Ex vivo:** Edición de HSC del paciente con Cas9 + gRNAs + donor HDR → trasplante autólogo (más control, menor riesgo inmunológico)
2. **In vivo (posterior):** VLP-SEND con Cas9/gRNA dirigidos a HSC → corrección directa en la médula ósea (sin extracción celular)

**Estado de la plataforma SEND:** Pre-clínico (publicado por Zhang Lab, 2023–2024). Aplicable a trastornos hematopoyéticos monogénicos como MVA1.

---

## 2. Propuesta terapéutica integrada para MVA1 (ruta de Fase 6)

**Estrategia escalonada ("hit-and-run" + corrección permanente):**

```
FASE 6A — Puente terapéutico (baja complejidad)
  └─ CRISPR-Cas13 (transitorio) → corrección de ARNm BUB1B en progenitores hematopoyéticos
     → restauración temporal de BubR1 funcional → reducción de aneuploidía

FASE 6B — Corrección génica definitiva (complejidad alta)
  └─ CRISPR-Cas9 / ABE + plataforma SEND
     → Edición ex vivo de HSC (corrección HDR de ambos alelos BUB1B)
     → Trasplante autólogo de HSC corregidas
     → Restauración permanente de la función BUB1B en la hematopoyesis

FASE 6C — Optimización de resistencia y seguridad
  └─ CRISPR Screening → identificación de modificadores y dianas de resistencia
     → Validación in vitro e in vivo (modelos de xenoinjerto)
```

---

## 3. Análisis de factibilidad

| Criterio | CRISPR-Cas9 (definitiva) | CRISPR-Cas13 (puente) | SEND | Screening |
|---|---|---|---|---|
| **Complejidad técnica** | Alta | Media | Alta | Media |
| **Eficiencia esperada** | Moderada (HDR ~10–30%) | Alta (knockdown >80%) | Media (pre-clínico) | Alta |
| **Seguridad** | Media (edición permanente) | Alta (transitorio) | Alta (componente humano) | Alta |
| **Reversibilidad** | No (permanente) | Sí (transitorio) | No (si es integración) | N/A |
| **Re-administración** | No | Sí | Sí | N/A |
| **Alineación con fenotipo MVA1** | ✅ (restaura BUB1B) | ✅ (restaura BubR1 transitoriamente) | ✅ (entrega segura) | ✅ (descubre mod.) |
| **Listo para traslación clínica** | Ensayos Fase I/II (2–3 años) | Pre-clínico (1–2 años) | Pre-clínico (2–3 años) | Investigación (1–2 años) |

**Conclusión:** MVA1 es una diana **excelente** para Zhang_Influence. BUB1B es un gen mono-génico, puntual, de mecanismo claro (checkpoint mitótico), y la corrección génica (restaurar función, no silenciar) es beneficiosa y no oncogénica. La terapia más prometedora es **CRISPR-Cas9/ABE + SEND** con corrección ex vivo de HSC.

---

## 4. Próximos pasos para Fase 6

1. Diseñar gRNAs específicas para cada alelo BUB1B (en silico)
2. Validar en células del paciente (fibroblastos → iPSC → progenitores)
3. Evaluar eficiencia de HDR/ABE para cada alele
4. Construir constructo SEND (peg10-mCherry reporter)
5. Screening CRISPR de modificadores del checkpoint BUB1B
6. Escribir `docs/fase6_zhang_influence.md` con propuesta completa

**Salida:** `data/results/fase6_zhang_influence.json` (análisis de factibilidad) + `docs/fase6_zhang_influence.md` (propuesta terapéutica completa)

---

## 5. Estrategias de compensación, estabilización y reemplazo (sin corrección genética directa)

> **Principio rector:** La Fase 6 no se limita a corregir el ADN. En MVA1, la corrección genética directa
> (CRISPR/HDR/ABE) es la de mayor complejidad por el **mosaicismo multiorgánico** (entrega sistémica a riñón,
> músculo, SNC) y porque el daño embriológico ya establecido **no es reversible** post-natal. Cuando corregir el
> defecto en el ADN o en la estructura original de la proteína es inviable, la farmacología y la bioingeniería
> operan por **mecanismos alternativos de compensación, estabilización o reemplazo**. Esta sección las organiza y
> las evalúa contra el genotipo BUB1B comp-het de la probanda.

### 5.1 Marco de evaluación

Cada estrategia se puntúa con una **escala de viabilidad clínica (0-100)** ponderando:
- **Mecanismo** (¿restaura función BUBR1 o la compensa de forma biológicamente coherente con el SAC?)
- **Seguridad en paciente oncológico pediátrico** (riesgo de inmunogenicidad / estimulación tumoral / toxicidad mitótica)
- **Logística de entrega multiorgánica** (¿resuelve el reto del mosaicismo?)
- **Madurez traslacional** (¿hay soporte preclínico/clínico publicado?)
- **Reversibilidad** (capacidad de interrupción, relevante en pediatría)

---

### E1. ARNm sintético de reemplazo (Terapia de transcripción)

**Concepto:** No se edita el gen nativo; se introducen **ARNm sintético codificante de BUBR1 sana** en
nanopartículas lipídicas (LNP). Las células del paciente traducen el ARNm exógeno y producen copias funcionales
de la proteína sin tocar el genoma original.

**Aplicación a BUB1B/MVA1:**
- BUB1B es **dosis-dependiente** (haploinsuficiente): restaurar niveles de BUBR1 rescata el SAC ([Baker 2013]).
- Al ser una proteína **citosólica/nuclear** (no secretada), la entrega por LNP-mRNA es factible para células en
  división (médula ósea, progenitores hematopoyéticos), el compartimento donde MVA1 causa el mayor daño oncogénico.
- **Efecto transitorio** (semanas) → re-dosificación; ventaja de **reversibilidad** en pediatría y en paciente oncológico.

**Distinción metodológica clave (rigor de reemplazo proteico vs. vehículo de edición):**

El ARNm optimizado aquí se utiliza **NO como vector para la maquinaria de edición genómica (CRISPR/Cas)**,
sino como **vehículo de traducción transitoria para reemplazo proteico**. Esta distinción es el estándar de oro
de seguridad terapéutica en **pediatría oncológica y enfermedades raras**: sustituye la proteína defectuosa con
una copia funcional sin introducir enzimas que corten el ADN. En el repositorio el ARNm existía únicamente como
LNP-mRNA de Cas9/Cas13 (sección 1.4); **redireccionarlo a codificar BUBR1 completa** es un cambio de paradigma de
bajo coste que reutiliza la misma infraestructura LNP/síntesis.

**Por qué la reversibilidad basada en ARNm es la estrategia óptima para MVA1:**

1. **Ventana farmacocinética autolimitada.** El ARNm es intrínsecamente efímero: no se integra en el genoma
   nuclear y se degrada de forma natural en el citoplasma en horas o pocos días. Cualquier desviación funcional,
   toxicidad mitocondrial o sobrecorrección del SAC se **revoca de inmediato al suspender la infusión**, dando al
   médico control absoluto y dinámico sobre la dosis intracelular.
2. **Supresión total de riesgos genotóxicos permanentes.** El paciente BUB1B ya tiene inestabilidad genómica y
   propensión tumoral crónicamente elevadas. Introducir editores de ADN o endonucleasas (CRISPR) conlleva un
   riesgo crítico de rupturas de doble cadena o **translocaciones cromosómicas secundarias**. El reemplazo por
   ARNm puro interactúa **exclusivamente a nivel ribosomal**, protegiendo la integridad del ADN genómico.
3. **Optimización directa de la infraestructura del repo.** Aprovechar las **LNP y los protocolos de síntesis de
   ARNm ya presentes** (concebidos para vehiculizar componentes de edición) permite un cambio de enfoque
   eficiente: en lugar de codificar una enzima de corte, la secuencia del ARNm se **rediseña (codon-optimized)**
   para codificar la longitud completa de la proteína BUBR1 funcional.

**Estado en repo:** el ARNm está usado como **vehículo** de CRISPR (LNP-mRNA de Cas9/Cas13, sección 1.4), pero
**no** como **reemplazo de la proteína BUBR1**. Este ángulo es nuevo y es la estrategia de mayor valor añadido que
aporta esta sección.

**Arquitectura de la solución (reemplazo proteico por ARNm-LNP):**

- **Carga útil (Payload):** ARNm sintético de alta estabilidad que codifica la isoforma canónica de BUBR1,
  flanqueado por regiones **UTR optimizadas** para maximizar la traducción en tejidos de alta tasa mitótica, sin
  desencadenar una respuesta inmune innata mediada por interferones.
- **Vehículo de entrega (Delivery):** nanopartículas lipídicas ionizables de **cuarta generación**, adaptadas con
  **ligandos de superficie específicos** para sortear el endotelio vascular y asegurar una **biodistribución
  equitativa** que compense parcialmente el mosaicismo tisular del paciente pediátrico.
- **Perfil de seguridad:** si un tejido responde con toxicidad a la restauración del ciclo celular, la
  interrupción del tratamiento **limpia el sistema por completo en menos de 48 horas**, cumpliendo la exigencia
  clínica de **reversibilidad absoluta**.

**Limitaciones:**
- BUBR1 es **grande** (~1050 aa; ARNm ~3.2 kb) → requiere optimización de codones/UTR para expresión estable en LNP.
- La sobreexpresión ectópica debe ser **fina** (sobreexpresar BUBR1 en exceso también es oncogénico).

**Viabilidad clínica: 72/100** — mecanismo sólido y específico, madurez traslacional media (tecnología LNP-mRNA
probada en vacunas), entrega multiorgánica parcial (buena en hematopoyético, limitada en SNC/riñón), con el
**diferenciador decisivo de reversibilidad absoluta (≤48 h al interrumpir) y cero genotoxicidad cromosómica**,
razón por la que se la posiciona como el **puente terapéutico de primera línea** en el esquema escalonado de la
Fase 6.

---

### E2. Estabilización mediante chaperonas farmacológicas

**Concepto:** Si la mutación produce una proteína **inestable que se degrada demasiado rápido**, pequeñas
moléculas (**chaperonas farmacológicas**) se unen al mutante, estabilizan su plegamiento 3D y alargan su
vida media en la célula.

**Aplicación a BUB1B/MVA1:**
- **p.Asn1002Lys** (missense, AlphaMissense 0.923, exón terminal de la kinasa) es candidata a proteína mal
  plegada → degradación proteosomal acelerada → **haploinsuficiencia funcional**.
- Una chaperona que estabilice el dominio kinasa C-terminal podría recuperar BUBR1 parcialmente funcional.
- Contexto ya documentado en el repo: la **estabilización de BUBR1 vía SIRT2/NAD+** (North 2014) es un caso
  particular; aquí se propone el **mecanismo general de chaperona farmacológica** sobre la proteína mutante.
- El **read-through (ataluren)** complementa: rescata la traducción del stop-gained (Leu737Ter), aunque produce un
  polipéptido más largo y no restaura el plegamiento del dominio C-terminal truncado.

**Estado en repo:** no hay chaperonas farmacológicas clásicas de plegamiento exploradas; solo read-through
(ataluren) y SIRT2/NAD+ como estabilizadores indirectos. Ángulo nuevo.

**Limitaciones:**
- Requiere que el mutante **conserve plegamiento parcial** y que la chaperona sea **alelo-específica**.
- La **Leu737Ter** no se beneficia de chaperonas (la truncación impide el plegamiento); solo la **missense N1002K**.

**Viabilidad clínica: 58/100** — mecanismo plausible solo para el alelo missense N1002K, madurez traslacional baja
(pocas chaperonas aprobadas fuera de Gaucher/fibrosis quística), no resuelve la haploinsuficiencia global.

---

### E3. Modulación de vías moleculares paralelas o redundantes del SAC

**Concepto:** Si un componente clave del SAC (BUBR1) está defectuoso, la terapia hiperactiva **otras quinasas o
proteínas de respaldo** que compensen parcialmente la falta de eficiencia del complejo fallido.

**Aplicación a BUB1B/MVA1:**
- Candidatos de la red del SAC ya identificados en Fase 3 (45 aristas; BUB1B hub con scores 0.999):
  - **BUB1** (parálogo): sobreexpresión compensa parcialmente la pérdida de BUB1B
  - **MAD2L1/MAD1L1** (clientes directos de BUBR1): amplificación estabiliza el complejo mitótico
  - **TTK/Mps1, AURKB, PLK1**: quinasas del checkpoint que modulan la severidad del fenotipo
- **CRISPRa** (activación transcripcional) de estos genes de respaldo podría restaurar la pausa mitótica que
  BUBR1 ya no logra imponer.
- **CRISPR screening** (ya propuesto en sección 1.3) alimenta esta estrategia: identificar supresores sintéticos.

**Estado en repo:** parcialmente cubierto (screening de supresores sintéticos en 1.3, sobreexpresión SIRT2→BUBR1
en propuesta terapéutica), pero **no** formalizado como estrategia de compensación de vías redundantes con
puntuación de viabilidad.

**Limitaciones:**
- Riesgo de **toxicidad mitótica** (hiperactivar quinasas del checkpoint puede detener la mitosis en exceso).
- **No corrige el riesgo oncológico** en las células que ya sobreexpresan BUBR1 (doble filo del tumor).

**Viabilidad clínica: 64/100** — racional mecanístico fuerte y enriquecimiento de red validado (Fase 3), pero
eficacia compensatoria no demostrada in vivo; perfil de seguridad delicado.

---

### E4. Intervención aguas abajo (downstream): ventana de oportunidad mitótica

**Concepto:** En lugar de reparar el sensor dañado, se administran compuestos que **ralentizan la mitosis** de
forma controlada, dando una "ventana de oportunidad" física más amplia para que la maquinaria defectuosa logre
ensamblarse correctamente antes de la división.

**Aplicación a BUB1B/MVA1:**
- El SAC disfuncional no bloquea la anafase; un freno mitótico temporal podría reducir la segregación errónea
  (aneuploidía variegada) al dar tiempo a la unión microtúbulo-cinetocoro.
- **El repo ya documenta un CANDIDATO CONCRETO:** inhibidores de **APC/C** (proTAME/apcin, tosina) que restauran
  de forma aguda y controlada la pausa mitótica que BUBR1 ya no impone (Propuesta terapéutica, Hipótesis A).

**ADVERTENCIA CRÍTICA (honestidad anti-reposicionamiento):**
- El repo marca a los **anti-mitóticos crónicos (taxanos)** como **contraindicados** por **ventana terapéutica
  estrechísima** y toxicidad mitótica. Esta estrategia downstream solo es viable como **intervención aguda
  controlada**, NO como terapia crónica.
- En un paciente con **rabdomiosarcoma**, añadir frenos mitóticos sistémicos podría **interferir con la
  quimioterapia anti-tumoral** (que depende de la mitosis para ser citotóxica).

**Viabilidad clínica: 31/100** — racional mecanístico atractivo pero **peligrosa** en el contexto del probando
(cáncer + tumor mitótico-dependiente + ventana estrecha). Prioridad media-baja, requiere calibración fina.

---

### 5.2 Matriz consolidada de viabilidad

| # | Estrategia | Mecanismo | Alelo diana | Seguridad oncol.ped. | Entrega multiorg. | Madurez | Revers. | **Viabilidad** |
|---|-----------|-----------|-------------|----------------------|-------------------|---------|---------|----------------|
| E1 | ARNm sintético de reemplazo | Reemplazo (transcripción) | ambos (BUBR1 sana) | Media (LNP probado) | Parcial (hemato. buena) | Media (LNP-mRNA) | Alta | **72/100** |
| E2 | Chaperonas farmacológicas | Estabilización | solo N1002K (missense) | Alta | Alta (oral) | Baja | Alta | **58/100** |
| E3 | Vías redundantes SAC (BUB1/MAD2L1/TTK/AURKB) | Compensación paralela | ninguno (sistema) | Media-baja (toxicidad mitótica) | N/A (intracelular) | Media | Media | **64/100** |
| E4 | Downstream (freno mitótico/APC/C) | Compensación downstream | ninguno | **Baja (contraindicado crónico)** | N/A | Baja | — | **31/100** |

---

### 5.3 Esquema de integración con la ruta de la Fase 6

```
DIMENSIÓN A: COMPENSACIÓN / REEMPLAZO (sin tocar ADN — puente inmediato)
  E1 ARNm-LNP BUBR1        → sobrescimiento transitorio de BUBR1 (hematopoyético)   [72/100]
  E3 Vías redundantes SAC    → CRISPRa BUB1/MAD2L1/TTK (compensación)               [64/100]
  E2 Chaperona N1002K        → estabilizar missense (aditiva con E1/E3)             [58/100]
  E4 Downstream (APC/C)      → SOLO agudo/controlado, NO crónico                    [31/100]

DIMENSIÓN B: CORRECCIÓN GENÉTICA PERMANENTE (desarrollada en secciones 1-2)
  6A Cas13 (puente ARN) → 6B Cas9/ABE + SEND (definitiva) → 6C screening

ELECCIÓN CLÍNICA RECOMENDADA (escalonada):
  1º E1 (ARNm-LNP BUBR1) como puente transitorio de rescate hematopoyético + vigilancia oncológica
  2º E3 (compensación de vías del SAC) como apoyo mecanístico — requiere más validación
  3º E2 (chaperona N1002K) como aditivo si la missense es degradada
  4º Mantener 6B (CRISPR definitivo) como ruta curativa a largo plazo
```

---

### 5.4 Conclusión de la sección

La Fase 6, vista de forma integral, no debe reducirse a la corrección genética directa. La propuesta de
**compensación/estabilización/reemplazo** aporta opciones clínicamente **más viables a corto plazo** en el contexto
del mosaicismo sistémico de MVA1. La **terapia de reemplazo por ARNm sintético (E1)** es la de mayor potencial,
ya que combina un mecanismo directamente dirigido a restaurar BUBR1 (la proteína dosis-dependiente afectada) con
la madurez probada de la plataforma LNP-mRNA y un perfil reversible apropiado para un paciente pediátrico
oncológico. La estrategia **downstream (E4)** es la menos recomendable y debe quedar **excluida como terapia
crónica**. La integración escalonada (puente ARNm → compensación de vías → chaperona aditiva → corrección
definitiva CRISPR) maximiza el rescate inmediato mientras la edición genética permanente madura.