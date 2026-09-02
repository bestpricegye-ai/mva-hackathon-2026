# PGE-MVA1 — Ingeniería Genómica de Precisión para MVA1 (L737Ter + N1002K)

**Paradigma:** transformar la auditoría pasiva de riesgos en **intervención biológica activa y
medible**. Documento técnico nivel laboratorio clínico y computacional. Nomenclatura original, sin
derivación de propuestas de terceros (ver §8. Originalidad).

**Caso:** PROBAND01 · BUB1B compound-het en GRCh38:
- **Alelo 1 — p.Leu737Ter** (c.2210T>G · chr15:40209701): stop-gain, PVS1 (ClinVar RCV000641226).
- **Alelo 2 — p.Asn1002Lys** (c.3006T>G · chr15:40220612): missense novel, dominio quinasa-like
  C-terminal, AlphaMissense 0.923 (Cheng 2023).

**Análisis de fase:** ambos alelos en trans inferido; pendiente segregación parental (§ Ej.1.1).

---

## 0. Tesis de superioridad (corta, para decisión)

| Dimensión | Enfoque pasivo (filtros + arimoclomol) | **PGE-MVA1 (esta propuesta)** |
|---|---|---|
| Causalidad alélica | Llama a "no probado" y se detiene | **Corrección experimental directa**: edición de bases + ensayos isogénicos (Eje 1 y 3) |
| Conteo de aneuploidía | Advera sesgo (muerte de clones) sin resolverlo | **Telemetría por división completada** (Eje 2): descarta citostasis/apoptosis por cinética real |
| Fármaco | Sonda inespecífica (arimoclomol) sin datos BUB1B | **Rescate dirigido**: ASO/NMD-evasión + readthrough estructura-informado del alelo L737Ter (Eje 1) + edición de bases alélico-específica (Eje 3) |
| Decisión | Firewall "no avance" binario | **Fail-closed matemático** con telemetría y umbrales preespecificados (Eje 4) |

---

## EJE 1 · Genotipado Dinámico y Corrección Alélica In-Trans

### 1.1 Conﬁrmación de fase (previo a todo ensayo)

- **Acción:** WGS/WES trios (proband → padres) en GRCh38 → algoritmo de desambiguación de fase
  (`src/pge_mva1.py phase`, §Eje4.1). Salida esperada: L737Ter paterno/materno definido far a (no
  inferido). Si un progenitor es portador solo de uno de los alelos y el otro es *de novo* →
  recalcular diagnóstico (PGE nunca asume fase).
- **Confirmación ortogonal:** ARN-seq en sangre/tejido (corriente abajo): 50×100 pb, alineador
  STAR 2.7 → per-cel.: cobertura alélica por base de los rs sitios L737Ter/N1002K → proporción de
  transcritos por alelo (desambiguación a nivel de ARNm).

### 1.2 Simulación de Dinámica Molecular (MD) del dominio de interacción kinetocoro — ΔΔG

**Objetivo:** localizar el punto exacto de disrupción del motivo Asn-contacto del alelo N1002K, con
energía libre de Gibbs relativa (FEP/MBAR), no con ruido estructural.

**Inputs de estructura (sin fabricación):** AlphaFold2 (AF2) de BUBR1 humano (global) y complejos
depositados homologues de kinetocoro (PDB: 6in8 - Bub1 kinetochore domain; argivos SAC) → se
modelan los segmentos N1002 + contacto candidato.

| Parámetro | Especificación |
|---|---|
| Motor / campo | OpenMM 8 (CUDA) o GROMACS 2024, **AMBER ff19SB** + solvatación TIP3P/OPC, iones 150 mM (monovalente) |
| Cavidades / régimen | Replica-exchange (REMD) inicial (8 réplicas, 300–380 K, 100 ns, solo el dominio) |
| Producción | 4 réplicas × **1.1 µs** de MD libre del dominio quinasa-like 700–1050 (HMR, paso 4 fs), NPT |
| ΔΔG (alquímico) | FEP alquímico Asn→Lys (sistema único, anclajes poraminósidos flanqueantes RMSD-anclados), 12–18 ventanas λ, **MBAR** → diferencia de unión libre kinetocoro (o plegado del dominio) |
| Umbral de impacto | `\|ΔΔG_unión\| ≥ 0.8 kcal/mol` **y** pérdida ≤1.7 Å del puente H Donor/Asn observado en PDB → N1002K etiquetado: **disruptivo (Hipótesis 1)** vs **neutral (Hipótesis 0)** |
| Métricas adicionales | Ocupación de H-bonds por residuo (PLIP), RMSF diferencial (localización de flexibilidad inducida), número de contactos nativos (Q-score) |
| Entrega | `data/results/pge_mva1_ddG.json`: tabla por replica, ΔΔG±SEM, decisión binaria + calor de clúster |

**Uso de la decisión:** si ΔΔG marca neutral → el alelo N1002K se reclasifica como VUS (el score
AlphaMissense 0.923 es solo levantamiento de sospecha, jamás prueba); el ensayo de rescate (1.3 y
Eje 3) se orienta exclusivamente al alelo L737Ter. Si disruptivo → entrada al ensayo readthrough +
edición bialélica dirigida.

### 1.3 Rescate transcripcional y evasión de NMD (alelo L737Ter)

**Fundamento computacional de NMD (ejecutado con anotación real):** BUB1B canónico
ENST00000287598.11 (23 exones, chr15:40161272–40221123+, strand +). p.Leu737Ter = c.2210T>G en el
**exón 17** (40209635–40209775); distancia del PTC al splice-junction aguas abajo =
**74 nt > 55 nt** → el alelo es **NMD-competente** (regla EJC clásica; Silva & Romão 2009). El
transcrito mutante se degrada en el primer round-traducción; el rescate requiere **suprimir la
degradación y restaurar un ARNm estable que se traduzca a proteína completa**.

**Estrategia ASO de diseño propio (nombres y composición originales):**
- **BUB1B-ASO-E17-e2** — gapmer 2′-MOE (5-10-5), 20 mer, complementario a la secuencia del exón 17
  contigua al PTC (base j-effect: evitar híbridos en el codón stop). Mecanismo: conferir pasaje de
  plataforma al ribosoma durante el primer round (evita disparo de NMD vía UPF1/SMG1 en el entorno
  del stop). **Uso en modo exploratorio** con entrega (LNP-galNAc-liver / LNP-TfR1-CNS) y monitor
  de seguridad hepática.
- Punto de partida secuencia (hg38, strand +):
  `...AGTTAC...CTGGGTACTCGA...` → ASO candidato obtener de `src/pge_mva1.py nmd` (genera hélices
  20 mer flanqueantes del PTC con score de acceso Arnafold).

**Readthrough optimizado (estructura-informado, no genérico):**
- Codón de parada del alelo = **TGA** (derivado de la variante curada ClinVar RCV000641226).
- Candidatos a inserción readthrough: near-cognate (Trp = TGG, Arg = CGA/CGG, Cys = TGC) probados en
  orden de fidelidad con ensayo de reportero dual (luciferasa-NanoLuc con el contexto exónico real de
  BUB1B §ulgarios seguidores) → selección de la línea con *incorporación del amino ácido natural
  correcto* y lectura completa del frame.
- Panel de agentes readthrough **optimizados por química**: G418 (aminoglucósido de referencia),
  ataluren (PTC124), y un análogo de aminoácido-tRNA sintetasa screening *in silico* para el contexto
  BUB1B (docking en el A-site del ribosoma 80S humano).

**Cuantificación de recuperación (método y umbrales):**
- **ARN-seq de alta profundidad ≥ 140 M reads mapeables** (total RNA, rRNA depletion) — lectura final:
  TPM del transcrito mutante vs WT en células portadoras pre/post-ASO, y **razón de isoformas NMD
  (stop-mRNA estable / total = fracción de escape NMD)** con 3 réplicas biológicas, ≥ 6 × 10⁶ reads
  sobre el exón 17.
- **Métrica principal de éxito (preespecificada en §Eje4.4):** relación de escape NMD ≥ 25% de la
  razón WT, cualquier reorganización de splicing anómala del exón 15–18 ≤ 2% de transcritos.
- **Verificación proteica:** anticuerpo anti-BUBR1 (C-terminal) → detección de banda de tamaño
  completo (1050 aa, ~120 kDa); si hay solo banda truncada → NMD-rescate no implica rescate de
  proteína, imposible avanzar (fail-closed).

---

## EJE 2 · Telemetría Mitótica Real-Time (neutraliza "menos aneuploidía puede mentir")

### 2.1 Sistema óptico dual

- **Líneas isogénicas del paciente** (fibroblastos inducidos iPSC → linaje condrocitos/mesenquimal;
  y células primarias disponibles): CRISPR-corregidas (rescatadas) vs parental mutante, mismas
  pasadas de cultivo, 3 clones cada una.
- **Transfectores estables integrados (S/MAR + piggyBac? no, lentiviral integración constituyente):**
  - **H2B-mRuby3** (histona → cromosomas visibles para conteo de mis-segregación),
  - **α-tubulina-GFP** (microtúbulos → huso bipo), conjugados con **TagRFP-Casp3? no**: usar
    **caspasa-3 biosensor (DEVD-icVenus)** para apoptosis y **Ki67-CLIP-?** — simplificado: evaluar
    proliferación por **incorporación de EdU al término del tracking**.

### 2.2 Adquisición y métricas por división completada (no por conteo)

| Métrica | Definición operativa | Umbral de diseño |
|---|---|---|
| **Duración SAC** | tiempo desde la consolidación bipo (huso formado) hasta anafase onset; medido en cada célula | esperado 8–20 min WTref; patológico > 2σ |
| **Tasa de error de segregación** | # eventos de cromátida rezagada / # **divisiones completadas** (intervalos hasta citocinesis) | relative ratio mutant/WT |
| **Tasa de división** | # citocinesis por célula·hora (ventana 72 h) | `div_rate` |
| **Apoptosis** | % células con activación de caspasa-3 (DEVD) durante la ventana | `Δapop ≤ +15 pt` |
| **Senescencia** | SA-β-Gal al final + p16/p21 (ICC) | `Δsense ≤ +15 pt` |
| **Arresto mitótico prolongado** | células con huso persistente > 90 min → "mitótico largo" inducible | conteo separado |

### 2.3 Estadística de decisión (preespecificada)

- Unidades de inferencia = **divisiones completadas**, no células (elimina la trampa de que la
  muerte de progenie reduzca el conteo).
- Modelo de conteos jerárquicos (poisson-binomial por clon) con test exacto de Fisher o estimación
  bayesiana (Beta-binomial, prior débil) → comparación mutant-rescate.
- **Condición de rescate funcional (todas simultáneas):**
  1. reducción de tasa de error/segregación: `límite inferior de Wilson(δ) ≥ 20% de reducción`,
  2. `div_rate` no reducida (no citostasis): `ratio ≥ 0.85` (lím. inferior),
  3. `Δapoptosis ≤ +15 pt`, `Δsenescencia ≤ +15 pt`,
  4. **n ≥ 80 divisiones completadas y ≥ 450 eventos de segregación** para tolerar el sistema óptico.
- Cualquier condición incumplida → **fail-closed** (§Eje4.4), sin importar cómo se vea el conteo crudo.

### 2.4 Neutralización del sesgo de selección clonal

El competidor señala que "menos aneuploidía puede ser muerte de clones": correcto y asumido.
PGE lo elimina porque la métrica es *por división completada* y la apoptosis/arresto se miden en
paralelo: un clon que muere (apoptosis elevada) o deja de dividirse (div_rate baja) **invalida el
avance por la condición (2)-(3)**, aunque su tubo muestre menos células aneuploides. El "firewall"
pasa de ser una advertencia a ser un instrumento de medida.

---

## EJE 3 · Ingeniería de Intervención Activa (edición de bases y corrección génica)

### 3.1 Abandono formal de sondas inespecíficas

Declaración explícita en el reporte: arimoclomol y genéricos heat-shock **quedan excluidos** del
programa (sin evidencia BUB1B, endpoints clínicos negativos históricos, ojo de pediatría). No
entran en ningún brazo terapéutico; solo como control negativo de esfuerzo en un panel de
transcripto? no — fuera del programa.

### 3.2 Pipeline de edición de bases y CRISPR alélico-específico (hg38)

Reutiliza y extiende los resultados **ya ejecutados** en nuestra fase 6:
- `fase6_criterios_zhang.json` — PAM NGG verificado en hg38 para ambos sitios (secuencia UCSC real),
  espaciadores candidatos:
  - alelo 1 (chr15:40209701): gRNA candidato `CACTTAACTCTGGTAGGGAC`,
  - alelo 2 (chr15:40220612): gRNA candidato `CCTCATCATTGGCATTCAGA`.

**Diseño de editores:**
| Parámetro | Especificación |
|---|---|
| Estrategia alelo 2 (T>G,**transversión**) | **ABE8e+SpG** no aplicable directo (transversión); dos opciones: (a) **Prime Editing PE3** (versión nativa repara T>G sin doble DBS), (b) **NHEJ-KO alélico** como última opción solo si la pérdida del alelo N1002K es neutral funcional (depende de ΔΔG del Eje 1.2) |
| Estrategia alelo 1 (stop TGA) | **Readthrough (Eje 1.3)** o **CBE en el codón sesgando a Trp/RArg de mayor fidelidad** (C-to-T libre) — decisión por reportero NanoLuc |
| gRNA validación PAM | NGG estricto, `Feng Zhang criteria` = especificidad (off-target), eficiencia (on-target), PAM — verificado en `fase6_criterios_zhang.json` (PAM ✓; eficiencia ALTA preliminar; off-target → CRISPOR pendiente de índice completo) |
| Off-target cuantitativo | **CRISPR-Cas9 OFF-Target vía DeepSpCas9 2.0 (Kim 2022)** + CasOFFinder (≤ 6 mismatches, índice GRCh38) → métricas: fondo no canónico, 0 off-target reales simlab /< 1e-4 de edición en cualquier OT oncogénico |
| Edición | electroporación Neon / LNP mRNA, 3 condiciones de dosis (0.2 / 1 / 5 µM eq. de gRNA) |

### 3.3 Ensayo funcional de rescate proteico (half-life y actividad)

- **Pulso:** cicloheximida 50 µg/mL bloqueadora de elongación; muestras a t=0,2,4,8,16,24 h.
- **Western blot cuantitativo por quimioluminiscencia digital** (ChemiDoc MP imaga, anti-BUBR1
  N-term + C-term y anti-α-tubulina como loading) → decay monoexponencial, `t½` por ajuste no lineal
  (curve_fit, R²≥0.9).
- **Decisión:** `t½(rescatado) ≥ 0.85 × t½(WT)` y estabilidad de banda completa a 24 h →
  rescue funcional; `t½` corta (≤0.5×WT) pero banda completa → proteína inestable, fail-closed para
  readthrough, entrar en edición génica.

---

### 3.4 Genoma real (GRCh38 + VCF WGS del paciente) → artefactos de edición y verificación

Los pasos wet-lab de MD-µs, ARN-seq, readthrough y base editing **consumen inputs que aquí se generan desde el genoma realmente secuenciado**, no desde plantillas genéricas. Ejecutado con `src/pge_mva1_genome.py` (`artifacts`) sobre:

- **VCF real** `WGS_EX2312012_HGWCNDSX7.vcf.gz` (GRCh38, FILTER=PASS) → `vcf_exonic_variants.txt`
- **Referencia hg38 real** (ventanas UCSC cacheadas) para las homologías de reparación.
- **Índice de referencia requerido:** los flujos GATK/CRISPOR/MD exigen el índice **GRCh38/hg38** (build oficial GATK, `gatk.broadinstitute.org/...-GRCh38-or-hg38`); el entorno local no montó el FASTA+dict indexado (751 MB), por lo que el off-target DeepSpCas9/CasOFFinder queda pendiente.

**Artefactos reales por sitio (`data/results/pge_mva1_genome.json`):**

| Sitio | VAF observado (VCF) | AF gnomAD | Donor HDR ssDNA | Primers amplicón (verificación edición) |
|---|---|---|---|---|
| chr15:40209701 (L737Ter) | 0.543 | 3.29e-05 | 61 nt, corr. a WT | `TCACAGTATCGCAGACAGCT` / `ATTGGTCTGTCTTCTATACA` |
| chr15:40220612 (N1002K) | 0.464 | novel (AF=None) | 61 nt, corr. a WT | `ATGGTGAATTGTGGAATAAA` / `AAGCTCCCCAAGAACAGACA` |

**Uso downstream (wet-lab, requiere HPC + biobanco):**
- Donor HDR → HDR/prime editing en línea celular del paciente; la verificación por amplicón-PCR usa los primers generados.
- VAF real → dosaje alélico para interpretar escape NMD por ARN-seq (fracción transcrito mutante).
- BLOQUEO escalonado: fase in-trans sin segregación parental y edición celular sin biobanco se marcan **fail-closed** en el JSON, no se sobre-venden como confirmadas.

---

## EJE 4 · Orquestación Autónoma (Closed-Loop · Python)

### 4.1 Módulos ejecutables (implementados en `src/pge_mva1.py`)

| Comando | Función | Salida |
|---|---|---|
| `phase` | Algoritmo de desambiguación in-trans con genotipos trios (inputs: VCF proband+padres, gene BUB1B) | `pge_mva1_phase.json` + llamada "in-trans confirmado/indeterminado" |
| `nmd` | Regla 55 nt / EJC sobre exones reales de ENST00000287598.11 → predicción NMD del alelo L737Ter + generación de ASO candidatos flanqueantes | `pge_mva1_nmd.json` |
| `telemetry` | Analizador agnóstico de telemetría: por-división error rate, división rate, apoptosis/senescence gates, decisión binaria | `pge_mva1_telemetry.json` |
| `selftest` | Benchmark sintético **con verdad simulada oculta al analizador** (n=2000 ejecutables): detección de falso-rescate (citostasis/apoptosis), FP Wilson, fail-closed (datos escasos) | `pge_mva1_selftest.json` |

### 4.2 Fail-closed matemático (preespecificado, no negociable)

Avance clínico bloqueado si NO se cumplen simultáneamente:
1. `in-trans = confirmado` (Eje 4.1 phase),
2. NMD-rescate: escape NMD ≥ 25% o edición alélica verificada ≥ 20% de células (edición por
   amplicón-seq, LOD ≤ 0.5%),
3. telemetría: 4 condiciones del §2.3,
4. half-life §3.3 ≥ 0.85×WT,
5. **ratio beneficio/citotoxicidad**: `(reducción adicional de error rate) / (Σ Δapop+Δsenes+Δarresto)` ≥ 2.0,
   con costo ≥ 1 unidad de citotoxicidad → bloqueo del avance, registro del gate fallido.

### 4.3 Evaluación estocástica (honestidad vs. decoro)

El `selftest` valida el **analizador**, no el bioensayo: se generan mundos sintéticos (simulación
oculta; el analizador no recibe la verdad), se reportan sensibilidad (detección de falso-rescate),
tasa de falsos-avance (Wilson UCB) y correcto-fail-closed en datos escasos. Cifras reales se
publican tras ejecución local (§5). Nunca se presentan como evidencia clínica.

---

## 5. Estado de ejecución (transparencia absoluta)

| Artefacto | Estado | Dónde |
|---|---|---|
| PAM verificado ambos alelos, ref hg38 | **EJECUTADO (real)** | `fase6_criterios_zhang.json` |
| Espaciadores candidatos + eficiencia ALTA heurística | **EJECUTADO (real)** | `data/results/fase6_criterios_zhang.json` |
| Análisis NMD (exón 17, 74 nt > 55 nt) | **EJECUTADO (anotación real)** | §1.3 → `pge_mva1_nmd.json` |
| Fase/paes in-trans | Implementado, **datos trios pendientes** (seg. parental) | `pge_mva1_phase.json` (sintético) |
| Telemetría + fail-closed | Implementado, **validado en simulación sintética** | `pge_mva1_selftest.json` |
| **Genoma real → artefactos de edición** (GRCh38 + VCF WGS real): donor HDR ssDNA, primers de amplicón-seq para verificación, VAF observado, AF gnomAD | **EJECUTADO (genoma real)** | `src/pge_mva1_genome.py` → `pge_mva1_genome.json` |
| MD-µs, ARN-seq, readthrough, base editing wet-lab | **PROTOCOLO**; inputs reproductibles desde el genoma real ya generados | §Ejes 1/3 + `pge_mva1_genome.json` |
| Off-target CRISPOR | Pendiente **índice GRCh38** (751 MB, entorno sin HPC); requerido para run → `gatk.broadinstitute.org GRCh38/hg38` | `fase6_criterios_zhang.md` |

## 8. Originalidad e independencia

- Términos, nomenclatura y arquitectura propios (Ejes 1–4, PGE-MVA1); no se incorpora texto,
  figuras ni estructuras de la propuesta similar del mercado.
- Las técnicas (MD/FEP, ASO gapmer, live-cell, prime/base editing, fail-closed) son instrumentos
  científicos estándar y de uso libre; la coordinación, umbrales y decisiones para **BUB1B-MVA1**
  son diseño propio.
- Todo dato de simulación se etiqueta como sintético; ningún resultado simulado se presenta como
  clínico.

## Referencias (fuentes primarias consultadas)

- Ensembl GRCh38, transcrito canónico ENST00000287598.11 (exones BUB1B; CDS 40161272–40221123).
- ClinVar RCV000641226; gnomAD v2.1.1 (Karczewski 2020); AlphaMissense (Cheng 2023).
- North BJ et al. EMBO J 2014;33:1438 (SIRT2→BUBR1) · Baker DJ et al. Nat Cell Biol 2013;15:96 ·
  Baker DJ et al. Nat Genet 2004;36:744.
- Silva AL, Romão L Hum Mol Genet 2009 (regla 55 nt/EJC, NMD).
- Kim N et al. 2022 DeepSpCas9 2.0 (off-target) · Haeussler M 2016 (CRISPOR) · Doench J 2016.
- Segel M 2021 (SEND) · Gaudelli N 2017 (ABE) · Anzalone A 2019 (prime editing).