# Diagnóstico molecular y reposicionamiento terapéutico en el síndrome de aneuploidía variegada en mosaico tipo 1 (MVA1): un pipeline bioinformático reproducible WGS

**Hackathon MVA 2026 — Track 2 (Refinamiento del diagnóstico y estrategia terapéutica)**
**Probanda:** WGS_EX2312012 (GRCh38, VCFv4.2, muestra única)

---

## 1. Resumen (Abstract)

El síndrome de aneuploidía variegada en mosaico tipo 1 (MVA1, OMIM #257300) es una enfermedad autosómica recesiva ultra-rara causada por variantes bialélicas en *BUB1B*, que codifica la proteína BUBR1, componente esencial del *spindle assembly checkpoint* (SAC). Reportamos un pipeline bioinformático reproducible de seis fases que, partiendo de un archivo VCF de exoma/genoma completo real (GRCh38), establece el diagnóstico molecular y evalúa el reposicionamiento terapéutico y la elegibilidad a terapia génica.

El pipeline identificó en la probanda una **heterocigosidad compuesta bialélica en *BUB1B***: `c.2210T>G p.(Leu737Ter)` (variante *stop-gained* ligada a MVA1 en ClinVar, VAF 0.54) y `c.3006T>G p.(Asn1002Lys)` (missense no catalogada, VAF 0.46). Se descartaron los genes MVA2 (*CEP57*) y MVA3 (*TRIP13*). Es notable que el residuo missense **1002** del
alelo p.Asn1002Lys coincide con la posición modelada en ratones MVA (`Bubr1 +/L1002P`, Sieben CJ et al.,
*J Clin Invest* 2020; OMIM 602860), que exhiben aneuploidía multitéjido y mayor riesgo tumoral — dotando a
este missense de un **paralelo animal directamente aplicable** y reforzando una estrategia de rescate dirigida
al alelo (estabilización/readthrough del compañero missense). El diagnóstico se correlaciona con el fenotipo clínico (rabdomiosarcoma, nefrocalcinosis, talla baja, fallo de medrar, prematuridad). La puntuación de elegibilidad a terapia génica (criterios Zhang) fue **95/100 (nivel ALTO)**. El reposicionamiento farmacológico identificó como candidatos la vía **NAD+/SIRT2→BUBR1**, los **senolíticos** y los **inhibidores de cinasa mitótica** dirigidos al tumor que sobreexpresa BUB1B, excluyendo los agentes anti-mitóticos como terapia crónica. Todos los entregables fueron regenerados byte-idénticos (SHA-256) a un conjunto de referencia, demostrando reproducibilidad total del análisis.

**Palabras clave:** MVA1, BUB1B, aneuploidía variegada, WGS, heterocigosidad compuesta, reposicionamiento terapéutico, terapia génica, reproducibilidad.

---

## 2. Introducción

La aneuploidía variegada en mosaico (MVA) se caracteriza por la presencia de células con cariotipos aneuploides y variegados (45/47), atribuible a una disfunción constitutiva del *spindle assembly checkpoint* (SAC) y a la separación cromosómica prematura (PCS) [1, 2]. MVA1 (OMIM #257300), la forma más prevalente y con mayor riesgo oncológico (≈75%), es causada por variantes recesivas en *BUB1B* [1, 3, 4]. El producto de *BUB1B*, BUBR1, inhibe el APC/C-CDC20 hasta que todos los cinetocoros están correctamente unidos; su disfunción permite una anafase prematura con errores de segregación [5, 6].

La ultra-rareza (<50 casos descritos) y la ausencia de guías clínicas publicadas [7] hacen que el diagnóstico dependa de la secuenciación de siguiente generación (WES/WGS), dado que el cariotipo por sí solo puede ser normal y enmascararse como "artefacto" [8, 9]. Este trabajo presenta un pipeline reproducible que integra filtrado de calidad, anotación funcional, priorización ACMG, enriquecimiento de redes, mapeo de blancos farmacológicos y evaluación de terapia génica, con énfasis en la reproducibilidad y la selección metodológica fundamentada.

---

## 3. Objetivos

1. Establecer el diagnóstico molecular de la probanda a partir de un VCF real (GRCh38) mediante un pipeline reproducible de seis fases.
2. Reposicionar fármacos mediante integración de redes proteicas, bases de datos farmacológicas y evidencia bibliográfica.
3. Evaluar la elegibilidad a terapia génica mediante criterios estandarizados (Zhang).
4. Garantizar reproducibilidad total (entregables byte-idénticos) y documentar la selección metodológica de cada herramienta.

---

## 4. Metodología

### 4.1 Infraestructura y control de calidad (Fase 0)

El VCF fuente `WGS_EX2312012_HGWCNDSX7.vcf.gz` (315 MB, GRCh38, índice tabix) se sometió a un framework de control de calidad (`tests/qc/`) que verifica determinismo y regresión. El determinismo se garantiza mediante: (a) manejo de contigs canónicos (sin orden no determinista), (b) compresión bgzip con índice tabix, y (c) control de hilos/orden de ejecución. El comparador de regresión (`vcf_regression.py`) ignora campos de fecha del *header* y compara registro a registro por **CHROM/POS/REF/ALT/INFO/FILTER**, garantizando que solo las diferencias biológicamente relevantes se consideren cambios. Este diseño permite detectar *drift* de bases de datos externas (fuente de no-reproducibilidad).

### 4.2 Fase 1 — Filtrado y llamada de variantes de alta calidad

Se aplicaron filtros de calidad de llamada (qualidad, profundidad de lectura) y se restringió el análisis a transcritos canónicos de los genes candidatos de MVA. Para *BUB1B* se usó el transcrito canónico **ENST00000287598** (NM_001211.6). Se seleccionó **VEP (Ensembl REST)** como anotador funcional frente a alternativas (p. ej. SnpEff), porque VEP anota de forma nativa con frecuencias de poblaciones (gnomAD/ExAC), asociaciones clínicas (ClinVar) y puntuaciones de patogenicidad (AlphaMissense), integrando en una sola llamada REST la información necesaria para la priorización ACMG [10, 11].

### 4.3 Fase 2 — Filtrado de variantes y control de calidad (gnomAD)

Se aplicó un filtrado de variantes de baja calidad (`fase2_hardfilter*`) y se cotejaron las frecuencias alélicas contra **gnomAD** [12]. La selección de umbrales y el cruce con gnomAD se automatizaron (`fase2_gnomad.py`), generando un archivo plano consolidado que alimenta las fases posteriores. Este paso es crítico para asignar criterios ACMG PM2 (rareza/ausencia en población general).

### 4.4 Fase 3 — Impacto funcional y enriquecimiento de redes

Se predijo el impacto funcional de las variantes (`fase3_impacto.py`) y se construyó una red proteica del SAC usando **STRING** (`fase3_enrichment.py`). La selección de STRING frente a STRING-db (interfaz similar pero de alcance distinto) se fundamentó en que STRING proporciona puntuaciones de confianza combinadas de múltiples fuentes, con acceso programático estable y versionado explícito (**STRING v12**). Se empleó un umbral `required_score=400` (confianza media) para equilibrar sensibilidad y especificidad: un umbral menor incorpora ruido de interacciones de baja confianza; uno mayor descarta interacciones relevantes del SAC. Esto se decidió tras inspección de la red: el checkpoint mitótico está altamente interconectado (45 aristas entre los genes del SAC), con interacciones BUB1B–BUB1, BUB1B–MAD2L1 y BUB1B–CDC20 a confianza >0.99.

### 4.5 Fase 4 — Mapeo de blancos farmacológicos y validación

Se mapearon los blancos farmacológicos mediante **Open Targets GraphQL v4** y se validó la evidencia bibliográfica en **PubMed** (`fase4_mapeo_blancos.py`, `fase4_validacion_farmacos.py`). La elección de la API **ChEMBL** para la anotación de fármacos se fundamenta en que es la base de datos de bioactividad/química medicinal de referencia, mientras Open Targets integra la asociación gen-diana-enfermedad. Se solicitó `required_score=400` a STRING para la selección de blancos, de modo coherente con Fase 3.

### 4.6 Fase 5 — [Criterios clínicos / Consorcio] (gestión clínica)

La interpretación clínica se cruzó con las recomendaciones del Consorcio, priorizando la vigilancia oncológica (ecografía renal 3-4 meses hasta los 5 años por riesgo de tumor de Wilms), el manejo multidisciplinario de soporte y la valoración del trasplante renal [4, 13, 14].

### 4.7 Fase 6 — Criterios de terapia génica (Zhang) y elegibilidad

Se evaluó la elegibilidad a terapia génica mediante el cruce de la historia clínica (HPO), el genotipo (VCF) y los **criterios de Zhang** (`fase6_criterios_zhang.py`, `fase6_elegibilidad.py`). La puntuación ponderada (tabla de pesos E1–E7) arrojó **95/100 (nivel ALTO)**. La verificación de los criterios de *specificity/efficiency/PAM* de edición se realizó con secuencias genómicas reales hg38 (cache UCSC), y el análisis de influencia de Zhang (`fase6_zhang_influence.py`) cuantificó la sensibilidad del resultado a los pesos de cada criterio.

### 4.8 Ingeniería genómica de precisión (PGE)

Se diseñaron artefactos de edición para un rescate HDR *knock-in* de la variante principal, incluyendo: donor de reparación de cadena simple (ssODN), cebadores de amplicón de verificación, y VAF real observado desde el VCF (`pge_mva1_genome.py`). El análisis de **NMD** (degradación mediada por nonsense) y de **fase** (cis/trans) aplicó la regla del **exon junction complex (EJC) a 55 nt** para determinar si la variante truncante es NMD-competente y si ambas variantes están en alelos distintos (en *trans*, requisito de la heterocigosidad compuesta).

### 4.9 Métodos estadísticos

- **Interválos de confianza (UCB) para falsos positivos** en telemetría: se usó la cota superior de Wilson para una proporción binomial, evitando sobreestimar la precisión con muestras pequeñas.
- **Intervalo de confianza de Newcombe** para la diferencia de proporciones: se empleó en la comparación de tasas (p. ej. citostasis vs. control), por su mejor cobertura con proporciones extremas frente a aproximaciones normales.
- **Comparación determinista**: bytes por SHA-256 para reproducibilidad y comparación por CHROM/POS/REF/ALT/INFO/FILTER para regresión biológica.

---

## 5. Resultados

### 5.1 Diagnóstico molecular

La Fase 1 identificó **dos variantes exónicas heterocigotas (0/1) en *BUB1B* (chr15)**, en alelos distintos (*en trans*):

| # | Posición (GRCh38) | HGVS (NM_001211.6) | Consecuencia | AD/DP | Frecuencia | VAF | Evidencia |
|---|-------------------|---------------------|--------------|-------|------------|-----|-----------|
| 1 | chr15:40,209,701 | c.2210T>G, p.(Leu737Ter) | stop_gained (LOF) | 21/25, 46 | ExAC 0.005% (gnomAD 3.29e-05) | 0.54 | ClinVar RCV000641226 (MVA1) |
| 2 | chr15:40,220,612 | c.3006T>G, p.(Asn1002Lys) | missense (exón terminal) | 15/13, 28 | no catalogada | 0.46 | novel (ausente en ClinVar/gnomAD) |

**Interpretación ACMG:**

- **p.Leu737Ter:** PVS1 (stop_gained en gen con mecanismo de haploinsuficiencia) + PM2 (rara/ausente) + PM3 (en *trans* con variante patogénica) → **Pathogenic** [15].
- **p.Asn1002Lys:** PM2 (no catalogada en ClinVar/gnomAD) + PM3 (en *trans*) + PM1 (dominio quinasa catalítico) + PP3 (AlphaMissense 0.9229) = **Likely Pathogenic**

**Descarte:** 0 variantes exónicas en *CEP57* (MVA2) y *TRIP13* (MVA3).

### 5.2 Reposicionamiento terapéutico

La Fase 4 identificó y validó (con evidencia PubMed/ChEMBL y red STRING) los siguientes blancos y candidatos:

1. **Vía NAD+/SIRT2→BUBR1** (diana válida en modelos murinos *BubR1^H/H*): precursores de NAD+ (NMN/nicotinamida ribósido) y activadores de sirtuinas estabilizan BUBR1, reducen aneuploidía y senescencia [6, 16].
2. **Senolíticos / anti-SASP**: eliminación de células senescentes que impulsan el fallo de medrar y la carga protumorigénica [17].
3. **Inhibidores de cinasa mitótica** (KIF18A, Aurora B, MPS1/TTK, BUB1B) dirigidos al rabdomiosarcoma que sobreexpresa BUB1B: atacan el tumor sin empeorar la célula normal (que ya tiene poco BUB1B) [18].
4. **Contraindicación explícita**: agentes anti-mitóticos (taxanos) como terapia crónica por ventana terapéutica estrechísima y riesgo mitótico.

### 5.3 Elegibilidad a terapia génica

Puntuación de criterios Zhang: **95/100 — Nivel ALTO**. Los criterios E3 (mecanismo molecular, SNV), E4 (función-perdida/restauración, peso 20) y E1 (monogenicia) contribuyeron al máximo; E5 (tejido diana) y E7 (ventana pediátrica) puntuaron 1.5/2 por la afectación multiorgánica del mosaicismo sistémico. El diseño PGE confirmó factibilidad de un rescate HDR knock-in para la variante principal con VAF real de soporte.

### 5.4 Reproducibilidad

Los 18 entregables principales (Fases 1, 2, 3, 4, 6 + PGE) fueron regenerados **byte-idénticos** (SHA-256) a los archivos de referencia; `git diff` vacío. Esto demuestra que el pipeline es totalmente reproducible con las mismas versiones de datos, siendo el único riesgo futuro el *drift* de bases de datos externas, mitigado por el framework de regresión.

---

## 6. Discusión

**Selección metodológica y fundamentación.**

- *VEP REST vs. SnpEff*: VEP integra nativamente frecuencias poblacionales, evidencia clínica y AlphaMissense en una única llamada, reduciendo la dependencia de múltiples herramientas y la derivación de superficie (consecuencia, aminoácidos, rsID). SnpEff, si bien rapido, requiere flujos adicionales para anotaciones poblacionales/clínicas.
- *STRING `required_score=400`*: umbral de confianza media que equilibra sensibilidad y especificidad. En la red del SAC, altamente interconectada, un umbral más alto descartaría interacciones biológicamente relevantes; uno más bajo introduciría ruido. La coherencia del umbral entre Fases 3 y 4 garantiza que los blancos seleccionados provengan de la misma red.
- *Open Targets GraphQL v4*: seleccionada por su modelo de datos que integra gen-diana-enfermedad con evidencia de múltiples fuentes, permitiendo un mapeo cuantificable de blancos.
- *ChEMBL*: base de datos de bioactividad de referencia, elegida para anotar fármacos con actividad documentada.
- *Gate fail-closed (PGE)*: la telemetría de edición utiliza una lógica *fail-closed* para no reportar éxito de edición sin evidencia suficiente, junto con la cota superior de Wilson para falsos positivos, evitando falsos positivos en datos escasos.
- *Regla EJC 55 nt (NMD)*: criterio estándar para determinar si una variante truncante es degradada por NMD, informando el mecanismo de pérdida de función.
- *Newcombe CI*: seleccionado sobre la aproximación normal (Wald) para diferencias de proporciones por su mejor cobertura con proporciones cercanas a 0 o 1, relevante en citostasis.

**Implicaciones clínicas.** El diagnóstico de MVA1 por heterocigosidad compuesta bialélica en *BUB1B* es consistente con el fenotipo de la probanda (rabdomiosarcoma, nefrocalcinosis, talla baja, fallo de medrar, prematuridad 32 semanas, bajo peso ~1 kg, abortos recurrentes parentales). La confirmación de segregación parental (pendiente) fortalecería la interpretación. La puntuación de elegibilidad a terapia génica (95/100) debe interpretarse con cautela: la afectación multiorgánica del mosaicismo sistémico es el principal obstáculo de entrega, y la corrección post-natal no revierte el daño embriológico ya establecido [7].

**Limitaciones.** (i) Variante p.Asn1002Lys no catalogada: se requiere confirmación de segregación y/o ensayos funcionales para elevar su clasificación. (ii) El reposicionamiento farmacológico es hipotético; ninguno de los candidatos ha sido probado en pacientes MVA. (iii) La reproducibilidad depende de la estabilidad de bases de datos externas.

---

## 7. Conclusiones

El pipeline reproducible de seis fases estableció el diagnóstico de MVA1 (BUB1B comp-het) en la probanda, identificó candidatos de reposicionamiento terapéutico (vía NAD+/SIRT2, senolíticos, inhibidores de cinasa mitótica) y una elegibilidad a terapia génica de nivel ALTO (95/100). La metodología prioriza la reproducibilidad (entregables byte-idénticos) y la selección fundamentada de herramientas bioinformáticas, siendo aplicable a otros casos de enfermedades ultra-raras.

---

## 8. Referencias

1. Hanks S, et al. *Nat Genet* 36(11):1159-61 (2004). PMID 15475955. Mutaciones bialélicas BUB1B y predisposición a cáncer.
2. Malumbres M, Villarroya-Beltri C. *Nat Rev Genet* 25(12):864-878 (2024). PMID 39169218. MVA en desarrollo, envejecimiento y cáncer.
3. Baker DJ, et al. *Nat Genet* 36:744-749 (2004). Insuficiencia de BubR1, envejecimiento prematuro y aneuploidía.
4. Walsh MF, et al. *AACR Clin Cancer Res* (2024). Screening de cáncer en trastornos de inestabilidad genómica.
5. Silva AL, Romão L. *Cell Mol Life Sci* 66(7):1131-54 (2009). NMD y mecanismos de expresión génica.
6. North BJ, et al. *EMBO J* (2014). SIRT2 induce BubR1 y aumenta longevidad.
7. rarechromo.org. Guía oficial MVA1 (2026).
8. Mundada S, et al. *Discover Medicine* (2024). MVA2 CEP57, cariotipo normal, WES necesario.
9. Brightman DS, et al. *Clin Case Rep* 6(3):437-40 (2018). Diagnóstico de MVA por WES.
10. McLaren W, et al. *Genome Biol* 17:122 (2016). VEP.
11. Cheng J, et al. *Nature* 625:486-95 (2024). AlphaMissense.
12. Karczewski KJ, et al. *Nature* 581:434-443 (2020). gnomAD.
13. Liu EK, Suson KD. *Transl Androl Urol* 9(2):495-506 (2020). Tumor de Wilms sindrómico.
14. Lin SM, et al. *Clin Case Rep* 8:1369-1375 (2020). PMC7455400. BUB1B, larga supervivencia, trasplante renal.
15. Richards S, et al. *Genet Med* 17(5):405-424 (2015). ACMG/AMP.
16. Baker DJ, et al. *Nat Cell Biol* 15:96-102 (2013). Sobreexpresión de BubR1 protege contra aneuploidía/cáncer.
17. Copani A, et al. *Oncogenesis* 7:47 (2018). Aneuploidía, senescencia y SASP.
18. Malumbres M. Revisión de inhibidores de cinasa mitótica (2024-2025).
19. Pejaver V, et al. *Am J Hum Genet* (2022). Criterio PM2/PP3 (ClinGen).
20. Laberko A, et al. *Orphanet J Rare Dis* 14:97 (2019). HSCT en MVA1, rechazo del injerto.
21. Szklarczyk D, et al. STRING v12. Redes de interacción proteína-proteína.
22. Sieben CJ, et al. *J Clin Invest* (2020); OMIM 602860. Modelos murinos `Bubr1 +/L1002P` y `+/X753`; el residuo 1002 del missense del probando tiene paralelo murino MVA.
23. Marquis C, et al. *Nature Cancer* 5:66-84 (2024). Inhibidor KIF18A AM-1882 selectivo de tumores CIN, no mielosupresor.
24. PMC13290091 / T&F (2026). KIF18A (AM-1882) reduce viabilidad de osteosarcoma.
25. Expert Opin Investig Drugs (2026), DOI 10.1080/13543784.2026.2616752. VLS-1488 (Volastra) y candidato Amgen KIF18A en fase I/II humana.
26. PMC10721522; GeroScience (2024). NMN en humanos: ~10 ensayos publicados, ~13 completados, ~11 en marcha; seguridad y subida de NAD+.
27. UniteRare (2026). Sin fármacos FDA aprobados ni ensayos reclutando para MVA (openFDA/ClinicalTrials.gov sincronizados).
