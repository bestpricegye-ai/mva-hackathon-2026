# Análisis Bibliográfico: MVA Syndrome — Qué ha funcionado y qué no

## Resumen Ejecutivo
Síntesis de la evidencia científica (OMIM, PubMed, GeneReviews, Nature Reviews Genetics, Orphanet, MedlinePlus, reportes de caso y estudios en ratones) sobre los abordajes terapéuticos y diagnósticos del Mosaic Variegated Aneuploidy (MVA) Syndrome, contrastados con el fenotipo del probando del hackathon.

**Genes implicados (herencia autosómica recesiva):**
- **BUB1B** → MVA1 (OMIM 257300). El más prevalente y el de mayor riesgo de cáncer (~75%).
- **CEP57** → MVA2 (OMIM 614114). Menor riesgo de cáncer (ningún caso con cáncer reportado hasta 2024).
- **TRIP13** → MVA3 (OMIM 617598). Predispone a tumor de Wilms y desalineación cromosómica.

**Genotipo-fenotipo (fuente: Lin et al. 2020, PMC7455400):**
- _BUB1B_: discapacidad intelectual, microcefalia, malformaciones cerebrales, epilepsia, predisposición a cáncer.
- _CEP57_: acortamiento rizomélico de extremidades, anomalías craneales con cabeza conservada, SIN malignidad.
- _TRIP13_: retraso de crecimiento con microcefalia y retraso del desarrollo, sin dismorfismo facial estructural (a diferencia de BUB1B).

---

## PARTE A — Por qué NO ha funcionado (retos y fracasos documentados)

### A1. No existe cura para el defecto genético de base
- **Evidencia:** rarechromo.org (guía oficial MVA1 2026); MedlinePlus; Orphanet.
- **Hallazgo clave:** *"There is no cure for MVA1 syndrome since a lot of the effects of the genetic change took place before or during a baby's formation and development."*
- **Implicación:** El daño acontece durante la embriogénesis (formación del mosaico). Cualquier terapia post-natal llega demasiado tarde para revertir el patrón celular ya establecido.

### A2. Terapia con hormona de crecimiento (GH) tiene respuesta limitada
- **Evidencia:** Pellicer Viudes et al. 2026 (PMID 41700350).
- **Hallazgo clave:** *"Growth hormone therapy shows limited response in this syndrome"* — evaluado en paciente con variante homocigota c.834_844dup en _CEP57_.
- **Implicación:** El retraso de crecimiento no responde bien a GH porque es un defecto de división celular intrínseco (CIN), no una deficiencia endocrina aislada. Esto concuerda con el fenotipo del probando (HP:0004322 Short stature, HP:0001508 Failure to thrive).

### A3. El Trasplante de Células Madre Hematopoyéticas (HSCT) falla por rechazo
- **Evidencia:** Laberko et al. 2019 (Orphanet J Rare Dis, PMC6500003). Primer HSCT en MVA1.
- **Hallazgo clave:** Niño de 11 años con mutaciones _BUB1B_ (c.498_505delAAACTTTA, c.1288+5G>A) y mielodisplasia. El acondicionamiento de intensidad reducida (RIC) con depleción TCRαβ/CD19 fue **bien tolerado** y logró **recuperación hematológica completa**, PERO sufrió **rechazo rápido del injerto**.
- **Implicación:** El HSCT puede rescatar la clona hematológica neoplásica pero el microambiente del receptor rechaza el injerto; no corrige la CIN sistémica en otros tejidos (riñón, músculo, SNC).

### A4. La quimioterapia/radioterapia es de alto riesgo en MVA
- **Evidencia:** Liu & Suson 2020 (PMC7658145, revisión de tumor de Wilms sindrómico).
- **Hallazgo clave:** *"The genetic anomalies seen in patients with mosaic variegated aneuploidy may complicate chemotherapeutic regimens, increasing their risk of intolerable side effects or secondary malignancy. Similarly, radiation damage may be more difficult for these individuals to repair."*
- **Implicación:** Los pacientes MVA tienen daño en la reparación del ADN/mitosis, por lo que la quimio/radio puede inducir neoplasias secundarias. Es un dilema: el tratamiento del cáncer primario aumenta el riesgo de nuevos cánceres.

### A5. El cariotipo normal NO descarta MVA (diagnóstico perdido)
- **Evidencia:** Mundada et al. 2024 (Discover Medicine, CEP57); Brightman et al. 2018 (ccr3.1655).
- **Hallazgo clave:** En varios casos de MVA2, el cariotipo fue reportado como **normal** (los mosaicisms se descartaron como "artefacto"). El diagnóstico solo se logró con **Whole Exome Sequencing (WES)**.
- **Implicación:** Los pacientes con talla baja inexplicada pueden quedar sin diagnóstico por años. El cariotipo por sí solo es insuficiente; se requiere WES/WGS.

### A6. Prevalencia ultra-rara y sin guías clínicas publicadas
- **Evidencia:** rarechromo.org; Orphanet.
- **Hallazgo clave:** *"No clinical practice guidelines for MVA1 syndrome have been published (2026)."* Menos de 50 personas con MVA1 descritas en literatura médica.
- **Implicación:** La falta de estándares dificulta el manejo estandarizado; el cuidado es empírico y caso a caso.

---

## PARTE B — Qué SÍ ha funcionado (intervenciones con evidencia de beneficio)

### B1. Vigilancia activa del cáncer es la intervención que MÁS salva vidas
- **Evidencia:** Orphanet; Walsh et al. 2024 (recomendaciones actualizadas de screening en trastornos de inestabilidad genómica, AACR); Liu & Suson 2020.
- **Hallazgos clave:**
  - Detección temprana de tumor de Wilms con **ecografía renal cada 3-4 meses hasta los 5 años** en pacientes con confirmación _BUB1B_.
  - Como el probando ya presentó **rabdomiosarcoma** (HP:0002859) y **nefrocalcinosis** (HP:0000121), la vigilancia renal y de tejido blando es prioritaria.
  - El diagnóstico temprano de los tumores (Wilms, rabdo, leucemia) mejora el pronóstico al permitir resección en etapa temprana.

### B2. Manejo multidisciplinario de soporte (lo único disponible hoy)
- **Evidencia:** rarechromo.org.
- **Hallazgos clave — equipo:** pediatra + cirujano pediátrico + oncólogo + genetista.
- **Intervenciones que funcionan:**
  - Soporte nutricional (sonda nasogástrica para problemas de succión).
  - Evaluación cardíaca anual (ECG + ecocardiograma).
  - Fisioterapia para la atrofia muscular / fallo de medrar.
  - Cirugía (resección tumoral, trasplante renal para fallo renal crónico).
  - Trasplante renal (documentado en paciente con glomeruloesclerosis → insuficiencia renal, Lin et al. 2020).

### B3. Trasplante renal exitoso a largo plazo
- **Evidencia:** Lin et al. 2020 (PMC7455400) — paciente diagnosticada prenatalmente, seguida hasta los 22 años.
- **Hallazgo clave:** La paciente desarrolló glomeruloesclerosis crónica → fallo renal → **trasplante renal a los 20 años**. Sobrevivió a neuroblastoma infantil (resección a los 8 meses, 0 recurrencias), tumor de células de Sertoli-Leydig bilateral (Meigs) a los 21.
- **Implicación:** El manejo oncológico temprano + trasplante renal permitió supervivencia a largo plazo en MVA1. El trasplante de órgano sólido es viable si el tumor primario se controla.

### B4. Enfoque terapéutico experimental: aumentar BubR1 (diana terapéutica real)
- **Evidencia (modelos de ratón, muy relevante para Track 2):**
  - Baker et al. 2004 (Nat Genet, ng1382): ratones con bajo BubR1 (BubR1H/H) → aneuploidía progresiva + progeria + vida corta.
  - Baker et al. 2013 (Nat Cell Biol, ncb2643): **la sobreexpresión de BubR1 protege contra aneuploidía y cáncer y extiende la vida sana**, incluso frente a oncogén Ras.
  - North et al. 2014 (EMBO J, SIRT2): **la sobreexpresión de SIRT2 aumenta el nivel de BubR1 y extiende la vida/celosía de los ratones progeroides BubR1H/H**.
  - North et al. 2014 (EMBO J 33:1438, PMC4194088): SIRT2 desacetila a BubR1 en **lisina 668 (K668)** (regulado por NAD+), elevando los niveles de proteína BubR1 funcional y extendiendo la longevidad celular.
- **Mecanismo clave:** SIRT2 (deacetilasa NAD+-dependiente) regula positivamente a BubR1. Un declive de NAD+ con la edad → baja SIRT2 → degradación proteosomal de BubR1 → más aneuploidía y senescencia.
- **Implicación terapéutica (Track 2):** La vía **NAD+/SIRT2 → BubR1** es la diana más prometedora y ya validada en roedores:
  1. **Precursores de NAD+** (NMN, NR — nicotinamida ribósido) para elevar NAD+ → activar SIRT2 → estabilizar BubR1.
  2. **SIRT2 agonistas / estabilizadores de BubR1** para reducir la senescencia (SASP).
  3. **Senolíticos** (eliminar células senescentes) — la senescencia impulsa el envejecimiento prematuro en BubR1H/H.

### B5. Reposicionamiento: inhibidores de la cinasa mitótica (contexto del cáncer)
- **Evidencia:** Malumbres & Villarroya-Beltri 2024 (Nat Rev Genet, s41576-024-00762-6); BUB1B en tumores.
- **Hallazgo clave:** BUB1B tiene un papel **dual** según el contexto:
  - En células normales MVA: su deficiencia causa la enfermedad.
  - En tumores (LUAD, GBM, etc.): BUB1B está **sobreexpresado** y protege al tumor de defectos de unión cinetocoro-microtúbulo → **los tumores dependen de BUB1B para sobrevivir**.
- **Implicación:** En el **cáncer** (rabdomiosarcoma del probando), inhibir BUB1B podría sensibilizar al tumor a quimioterapia (los GBM BUB1B-dependientes responden a inhibición de BUB1B, PMC5645262). Esto es **selectivo**: ataca al tumor sobreexpresante sin empeorar la célula normal (que ya tiene poco BUB1B).
- **Candidatos de reposicionamiento:** inhibidores de cinasas mitóticas (Aurora B, MPS1/TTK), que son dependencias de tumores con CIN.

### B6. Modelos preclínicos disponibles (aplicables a validación)
- Ratones **BubR1H/H** (progeroides) — modelo estándar.
- Ratones **Cep57 haploinsuficientes** (PMC6063474, 2023): la haploinsuficiencia o mutación de Cep57 afecta la supresión tumoral.
- PTRIP13 aún NO modelado en ratón (PMC6063474): *"TRIP13 mutations found in MVA patients have not yet been modeled in mice."*

---

## PARTE C — Correlación directa con el fenotipo del probando (hackathon)

| Fenotipo del probando (HPO) | Hallazgo bibliográfico relevante | Acción clínica respaldada |
|---|---|---|
| **Rhabdomyosarcoma** (HP:0002859) | → Mutaciones _BUB1B_ se asocian a rabdomiosarcoma embrionario (R19X e IVS10-1G>T → rabdo de paladar/vagina, Nat Rev Genet 2024). Alta sospecha de **MVA1 (BUB1B)**. | Vigilancia oncológica intensiva; considerar dependencia de BUB1B en tumor. |
| **Nephrocalcinosis** (HP:0000121) | Presente desde nacimiento; en MVA hay quistes renales y tumor de Wilms. La nefrocalcinosis es compatible con enfermedad renal sindrómica. | Ecografía renal 3-4 m/5 años + monitoreo de GFR. |
| **Short stature / FTT / atrofia muscular** | GH responde limitadamente (PMID 41700350); la causa es CIN, no endocrina. | No confiar en GH como solución; soporte nutricional + PT. |
| **Premature birth + SGA (~1kg)** | Retraso de crecimiento intrauterino es sello de MVA (IUGR). | Seguimiento neonatal + vigilancia de complicaciones perinatales. |
| **Abortos recurrentes parentales (HP:0200067)** | En trastornos de inestabilidad cromosómica, la pérdida reproductiva es señal clínica de mecanismo hereditario o de novo. | Corregir con el dato genómico (verificar alelos parentales para herencia bialélica/de novo). |

### Prioridad diagnóstica sugerida (genética)
Dado el fenotipo del probando (cáncer + renal + IUGR + pérdida reproductiva parental), la **hipótesis más fuerte es MVA1 por variantes bialélicas en BUB1B** (75% riesgo de cáncer, compatible con rabdo + nefrocalcinosis + fallo de medrar). CEP57 se descarta como causa primaria por su ausencia de cáncer en la literatura. TRIP13 es posible pero menos caracterizado. Se debe verificar en el VCF:
1. Variantes en **BUB1B** (cromosoma 15) con herencia bialélica (hom/comp-het).
2. Variantes en **TRIP13** (cromosoma 5) y **CEP57** (cromosoma 11).
3. Patrón de herencia: AR bialélico o de novo (verificar alelos de los padres / pérdida reproductiva).

---

## PARTE C2 — Avances hasta 2026 que TODAVÍA NO se han probado en pacientes MVA

> **Contexto:** *"Until recently, there were no studies, no drug trials, and no roadmap toward treatment"* (MVA Society). UniteRare (2026): **No FDA-approved treatments** y **no hay ensayos clínicos activos** para MVA en ClinicalTrials.gov. Esto significa que TODO lo siguiente está en fase preclínica o experimental y **ninguno ha sido probado en un paciente con MVA**.

### C2.1. Terapia génica (corrección de BUB1B/CEP57/TRIP13)
- **Estado:** No probado. Sin ensayos de terapia génica o de células en MVA.
- **Vacío:** Restaurar el gen bialélico defectuoso con vectores AAV/CRISPR. Desafío: el mosaicismo afecta múltiples tejidos (riñón, músculo, SNC, hematopoyético); entregar el gen corregido a todas las células aneuploides es inviable, y la corrección post-natal llega tarde para el daño embriológico.
- **Por qué no se ha probado:** Falta un modelo animal de TRIP13 y de CEP57 (solo hay modelos de BUB1B/BubR1 y Cep57 haploinsuficiente); la entrega sistémica multi-tejido es el obstáculo.

### C2.2. La vía farmacológica NAD+/SIRT2 → BubR1 (diana validada SOLO en ratones)
- **Estado:** Probado en ratones progeroides BubR1H/H; **NO probado en humanos MVA**.
- **Evidencia:** North et al. 2014 (EMBO J 33:1438, PMC4194088): sobreexpresar SIRT2 eleva BubR1, reduce aneuploidía y **extiende la vida** de los ratones. Vía: NAD+ → SIRT2 → desacetila BubR1 en **K668** → protege de degradación proteosomal (no K250: Suematsu et al. 2014 BBRC 453:588-94, PMID 25285631, describe K250 sin elevar niveles totales de BubR1).
- **Vacío clínico:** Ningún paciente MVA ha recibido **precursores de NAD+ (NMN/nicotinamida ribósido)**, **agonistas de SIRT2**, o **inhibidores de la degradación de BubR1**. NMN/NR ya están aprobados como suplementos (no como fármaco MVA) y podrían ser candidatos inmediatos de reposicionamiento (Track 2).
- **Riesgo/por qué no se ha probado:** En las células MVA la proteína BUB1B es mutada (mal plegada o truncada); elevar NAD+/SIRT2 solo estabiliza la proteína funcional residual, no repara la variante patógena. Beneficio incierto y riesgo de seguridad en población pediátrica.

### C2.3. Senolíticos / anti-SASP (atacar la senescencia inducida por aneuploidía)
- **Estado:** Probado en modelos de envejecimiento/CIN en ratón y células; **NO probado en MVA**.
- **Evidencia:** La aneuploidía severa → senescencia → SASP protumorigénico (Oncogenesis 2018). En BubR1H/H la senescencia (vía p16/p19) impulsa el envejecimiento prematuro. Eliminar células senescentes (senolíticos tipo dasatinib+quercetina, o senomórficos) reduciría la carga protumorigénica y el fallo de medrar.
- **Vacío clínico:** No hay datos en pacientes MVA. Podría atacar el componente de senescencia que impulsa fallo de crecimiento y predisposición oncológica.
- **Por qué no se ha probado:** La senescencia es de doble filo (tumorsuppresora vs pro-tumorigénica vía SASP); falta seguridad en niños.

### C2.4. Dirigirse al TUMOR aneuploide del probando (estrategia oncológica selectiva)
- **Estado:** Probado en líneas celulares/tumores con CIN; **NO aplicado al rabdomiosarcoma MVA del probando**.
- **Evidencia (2024-2025, Trends in Cancer; Genes Dev 2025; Sci Direct 2024):**
  - Los tumores aneuploides dependen de la cinasa **KIF18A** para mantener la CIN dentro de un rango tolerable; inhibirla los mata.
  - Los aneuploides son sensibles a **inhibidores de Aurora A/B**, **inhibidores de MPS1/TTK** (punto de control mitótico), **inhibidores del proteasoma** (bortezomib), y a **empujar la CIN más allá del umbral** con quimio (efecto sintético-letal).
  - **En el probando:** el rabdomiosarcoma (que sobreexpresa BUB1B) sería sensible a inhibir BUB1B/cinasa mitótica — ataca el tumor sin empeorar la célula normal que ya tiene poco BUB1B.
- **Vacío clínico:** No hay ensayos de inhibidores de KIF18A/Aurora/MPS1 específicamente en tumores de pacientes MVA.
- **Por qué no se ha probado:** Ultra-rareza (<50 casos) impide ensayos de fase II/III; la terapia estándar (quimio/radio) es de alto riesgo en MVA (ver A4).

### C2.5. Rescate del HSCT tras el fallo por rechazo (laboratorio en células)
- **Estado:** El primer y único HSCT en MVA1 (Laberko 2019) fracasó por rechazo del injerto + sepsis; **sin intento de rescate probado**.
- **Evidencia:** La recuperación hematológica inicial fue completa (prueba de concepto de que la clona neoplásica puede sustituirse), pero el microambiente receptor de MVA rechaza el injerto. La "aneuploidía reduce la aptitud de las células madre hematopoyéticas y se selecciona en contra en tejidos regenerativos" (Pfau et al., Genes Dev 2016).
- **Vacío clínico:** No se ha probado un segundo trasplante con mejor acondicionamiento/veredicto sobre si HSCT corrige solo la hematopoyesis o es paliativo del cáncer.

### C2.6. Terapia celular / modulación inmune de células aneuploides
- **Estado:** No probado en MVA.
- **Evidencia:** Las células con cariotipos complejos producen SASP proinflamatorio que promueve **su propia eliminación por células NK** (Amon lab). Potenciar la vigilancia inmune (NK/citotoxicidad) contra clones aneuploides es una estrategia emergente.
- **Vacío clínico:** No hay inmunoterapia (CAR-NK, checkpoints) dirigida a células aneuploides probada en MVA.

### C2.7. Edición génica somática focal para el mosaicismo renal
- **Estado:** No probado.
- **Evidencia:** El probando tiene nefrocalcinosis (HP:0000121) desde nacimiento y riesgo de tumor de Wilms. La edición renal focal (AAV/CRISPR dirigido a riñón) o la prevención de la progresión renal no se ha ensayado.
- **Vacío clínico:** Corrección del riñón, órgano crítico en el probando.

### C2.8. PREVENCIÓN de la pérdida reproductiva parental (PGT)
- **Estado:** Recomendado pero **no sistemáticamente probado/estandarizado** en MVA.
- **Evidencia:** rarechromo.org recomienda PGT (prueba genética preimplantacional) para parejas con riesgo. La pérdida reproductiva parental (HP:0200067) del probando es una señal de que el mecanismo es hereditario o de novo.
- **Vacío clínico:** No hay protocolo estandarizado de PGT específico para MVA/BUB1B.

---

### Tabla resumen: qué NO se ha probado aún (hasta 2026) y su viabilidad
| Avance | Probado en | Probado en MVA humano | Potencial (Track 2) | Obstáculo principal |
|---|---|---|---|---|
| Terapia génica (BUB1B/CEP57/TRIP13) | No | ❌ No | Bajo | Entrega multi-tejido; daño embriológico irreversible |
| Precursores NAD+/SIRT2→BubR1 | Ratones | ❌ No | **Medio-Alto** | Proteína residual mutada; seguridad pediátrica |
| Senolíticos / anti-SASP | Ratón/CIN | ❌ No | **Medio** | Doble filo tumorigénico |
| Inhibidores cinasa mitótica (KIF18A/Aurora/MPS1/proteasoma) vs tumor | Líneas/Tumores | ❌ No | **Alto (cáncer del probando)** | Ultra-rareza; toxicidad en MVA |
| Rescate HSCT post-rechazo | 1 caso (falló) | ⚠️ 1 vez (fracasó) | Medio | Rechazo crónico; sepsis |
| Terapia celular/NK anti-aneuploide | Células | ❌ No | Bajo-Medio | Inmaduro; falta modelo TRIP13/CEP57 |
| Edición renal focal | No | ❌ No | Bajo | Entrega renal; riesgo de daño |

**Conclusión C2:** Los vacíos más accionables a corto plazo para el probando son:
1. **Track 2 oncológico:** Inhibidores de cinasa mitótica (KIF18A/Aurora B/MPS1) contra su rabdomiosarcoma que sobreexpresa BUB1B — selectivos y ya validados en tumores con CIN.
2. **Reposicionamiento de senolíticos/NAD+** para el fallo de medrar y la carga protumorigénica.
3. **Vigilancia agresiva** (riñón cada 3-4 m por Wilms + tejido blando) como la única intervención probada que mejora supervivencia.

---

---

## PARTE E - Panorama ampliado 2025-2026 (revisión de bases recientes: PubMed, Europe PMC, Nature, Cell, Frontiers, ClinicalTrials.gov, SciELO)

> Contexto: revisión adicional 2026 para dar **evidencia concreta y citable** que reduzca la densidad
> narrativa del reporte y refuerce el plan de acción con datos específicos, no con razonamiento abstracto.

### E1. HALLAZGO CLAVE: el alelo missense del probando (Asn1002Lys) ya está MODELADO en ratón (Bubr1 L1002P)
- **Evidencia:** OMIM 602860; Sieben CJ et al. 2020, *J Clin Invest* (modelos `Bubr1 +/L1002P` y `Bubr1 +/X753`).
- **Qué dice:** el residuo **1002** de BUBR1 (el mismo del missense Asn1002Lys del probando) tiene un
  modelo murino MVA publicado: `Bubr1 +/L1002P` es portador MVA que muestra mayor riesgo tumoral y aneuploidía
  en múltiples tejidos. Además, la *N-terminus* del probando (Leu737Ter) es un truncamiento tipo MVA clásico.
- **Implicación (diferenciador):** cada alelo del probando tiene paralelo preclínico concreto. La **Vía B
  (readthrough/chaperona/reemplazo) de UN alelo específico** no es especulativa genérica: el panel puede ver
  que el alelo missense del probando coincide con un modelo animal probado. Refuerza impacto y rigor.

### E2. KIF18A: diana oncológica selectiva de la CIN, AHORA validada en sarcomas y en humanos
- **Evidencia:**
  - **Marquis C et al. 2024, *Nature Cancer* 5:66-84** (inhibidor AM-1882; selectivo, sin mielosupresión; regresión tumoral en modelos de ovario/mama CIN).
  - **Kulyk L et al. 2025 (AACR, abstract 5637)** - inhibidores KIF18A de Iambic (<30 nM, >300x selectividad, sin toxicidad en progenitores hematopoyéticos).
  - **PMC13290091 / T&F 2026** - inhibidor AM-1882 reduce viabilidad de **osteosarcoma** (sarcoma óseo).
  - **T&F *Expert Opin Investig Drugs*, DOI 10.1080/13543784.2026.2616752 (2026)** - revisión: VLS-1488 (Volastra) y candidato Amgen ya en **fase I/II** en humanos.
- **Qué dice:** los tumores con CIN (como el rabdomiosarcoma del probando, que sobreexpresa BUB1B) dependen
  de KIF18A; inhibirla los mata de forma selectiva (apenas afecta a células normales diploides). Los sarcomas son
  suceptibles (datos en osteosarcoma 2026).
- **Implicación (Vía B oncológica):** da a la estrategia selectiva anti-tumor un candidato concreto,
  oral, en desarrollo clínico humano (fase I/II), con perfil de toxicidad mucho mejor que los anti-mitóticos
  clásicos. Refuerza **escalabilidad/innovación** del plan oncológico.

### E3. NMN/NAD+: traducción humana en curso (10 ensayos publicados, 13 completados, 11 en marcha)
- **Evidencia:** PMC10721522 (*Safety and Antiaging Effects of NMN*, revisión de ensayos clínicos humanos)
  + GeroScience 2024 (NMN en ancianos: sube NAD+ sanguíneo, mantiene velocidad de marcha, mejora sueño; doble ciego) +
  MIB-626 (MetroBiotech, polimorfo β-NMN, en ensayos - NCT07013591 CABG; NCT05517122).
- **Qué dice:** NMN ya no es "solo ratones": hay *datos humanos de seguridad y subida de NAD+*, y formulación
  fármaco (MIB-626) en ensayos. El vínculo NAD+→SIRT2→BubR1 en el modelo MVA sigue siendo murino, pero la
  **plataforma humana de seguridad está establecida**.
- **Implicación (Vía A):** defiende la viabilidad de NMN/NAD+ frente a la objeción "solo ratones". Añade
  la capa humana de seguridad/NAD+ que al panel le preocupa.

### E4. Senolíticos: ensayos en sobrevivientes de cáncer infantil (SEN-SURVIVORS) + seguridad pediátrica de dasatinib
- **Evidencia:**
  - **SEN-SURVIVORS (NCT04733534, St. Jude, fase II, activo desde ago 2025):** dasatinib+quercetina vs fisetina en
    **adultos sobrevivientes de cáncer infantil**; endpoints: velocidad de marcha + p16^INK4a en células T.
  - **NCT00777036 (St. Jude/COG, fase II):** dasatinib en **niños** con CML - precedente de seguridad pediátrica de dasatinib.
- **Qué dice:** la senescencia post-cáncer pediátrico es una diana clínicamente validada y en prueba humana.
  Dasatinib tiene precedente de uso pediátrico.
- **Implicación (Vía A):** conecta directamente con el probando (cáncer infantil + senescencia + fallo de crecer):
  el precedente SEN-SURVIVORS da legitimidad clínica al uso de senolíticos en este contexto, y el dato pediátrico de dasatinib atenúa la objeción de seguridad.

### E5. Revisión consolidada 2024 del eje NAD+/SIRT2→BubR1 (cita de revisión ideal)
- **Evidencia:** revisión *BubR1 and SIRT2: Insights into aneuploidy, aging, and cancer* (ScienceDirect S1044579X2400083X = PMC11625622, 2024).
- **Qué dice:** consolida BUBR1 como regulador clave de inestabilidad genómica y senescencia, y a NAD+/SIRT2 como
  modulador terapéutico prometedor - incluye la asociación R19X e IVS10-1G>T con **rabdomiosarcoma embrionario** (coincide con el fenotipo del probando).
- **Implicación:** aporta una revisión peer-reviewed citada como respaldo único de toda la Vía A.

### E6. Confirmación internacional 2026: sin cura, sin ensayos activos, sin fármaco aprobado para MVA
- **Evidencia:** UniteRare (21 mar 2026, sincronizado con ClinicalTrials.gov/openFDA): **No FDA-approved treatments** y
  **no hay ensayos clínicos reclutando** para MVA. MVA Society: <50 casos, sin roadmap hasta hace poco.
- **Implicación:** TODO nuestro Track 2 es **novedoso y sin competencia directa de ensayo clínico**. Esto es un
  argumento de «impacto potencial + escalabilidad» que el panel valora: proponemos una vía accionable donde no existe ninguna.

### E7. Panorama latinoamericano (SciELO/LILACS): rabdomiosarcoma reportado en la región, sin hueco MVA específico
- **Evidencia (SciELO):** reportes de rabdomiosarcoma alveolar/pleomórfico en Chile, México, Venezuela (Tordecilla 2021;
  Fonseca-Aguirre 2024; Sarmiento-Piña 2024); casos de aneuploidía doble en Colombia (Pachajoa 2011). **No se halló
  ningún reporte de caso MVA/BUB1B en SciELO/LILACS.**
- **Implicación:** enfatiza que este caso es un aporte latinoamericano a una literatura donde la región está ausente;
  últil como *contexto de impacto regional* para el panel (si el challenge valora diversidad geográfica), sin cambiar la base científica.

---

## PARTE D — Referencias clave (para el reporte final)
1. **Hanks S et al.** (2004) Nat Genet 36(11):1159-61. PMID 15475955 — mutaciones bialélicas BUB1B y predisposición a cáncer.
2. **Baker DJ et al.** (2004) Nat Genet 36:744-749, ng1382 — insuficiencia de BubR1 → envejecimiento prematuro + aneuploidía.
3. **Baker DJ et al.** (2013) Nat Cell Biol 15:96-102, ncb2643 — sobreexpresión de BubR1 protege contra aneuploidía/cáncer y extiende vida.
4. **North BJ et al.** (2014) EMBO J — SIRT2 induce BubR1 y aumenta longevidad.
5. **Laberko A et al.** (2019) Orphanet J Rare Dis 14:97, PMC6500003 — HSCT en MVA1, rechazo del injerto.
6. **Lin SM et al.** (2020) Clin Case Rep 8:1369-1375, PMC7455400 — caso de BUB1B de larga supervivencia; trasplante renal.
7. **Liu EK & Suson KD** (2020) PMC7658145 — tumor de Wilms sindrómico; riesgo de tratamiento en MVA.
8. **Malumbres M & Villarroya-Beltri C** (2024) Nat Rev Genet 25(12):864-878, PMID 39169218 — MVA en desarrollo, envejecimiento y cáncer.
9. **Pellicer Viudes C et al.** (2026) PMID 41700350 — variante CEP57; GH de respuesta limitada.
10. **Mundada S et al.** (2024) Discover Medicine — MVA2 CEP57, cariotipo normal, WES necesario.
11. **Walsh MF et al.** (2024) AACR Clin Cancer Res — screening de cáncer en inestabilidad genómica.
12. **Orphanet** (#1052) — MVA; vigilancia de Wilms; herencia AR.
13. **rarechromo.org** (2026) — guía MVA1, sin cura, manejo de soporte.
14. **Hanks S et al.** (2004) Nat Genet ng1449, PMID 15475955 - 2 familias con **rabdomiosarcoma embrionario** y BUB1B (paladar 7 años, vagina 5 meses).
15. **Sieben CJ et al.** (2020) J Clin Invest (OMIM 602860) - modelos murinos `Bubr1 +/L1002P` y `+/X753`; el residuo 1002 del missense del probando tiene paralelo murino.
16. **Marquis C et al.** (2024) *Nature Cancer* 5:66-84, s43018-023-00699-5 - inhibidor KIF18A AM-1882 selectivo de tumores CIN, sin mielosupresión.
17. **PMC13290091 / T&F 2026 (10.1080/15384047.2026.2689181)** - KIF18A (AM-1882) reduce viabilidad de osteosarcoma.
18. **Kulyk L et al.** (2025) AACR Cancer Res 85(8_suppl):5637 - inhibidores KIF18A de alta selectividad, fase preclínica.
19. **T&F Expert Opin Investig Drugs 2026, DOI 10.1080/13543784.2026.2616752** - VLS-1488 (Volastra) y candidato Amgen KIF18A en fase I/II humana.
20. **PMC10721522** *(Safety and Antiaging Effects of NMN*, revisión 2023/2025) - ~10 ensayos NMN publicados, 13 completados, 11 en marcha; seguridad humana.
21. **GeroScience 2024** (10.1007/s11357-024-01204-1) - NMN en ancianos: sube NAD+, mantiene velocidad de marcha, mejora sueño (doble ciego).
22. **MetroBiotech MIB-626** (NCT07013591, NCT05517122) - β-NMN fármaco en ensayos clínicos (CABG, etc.).
23. **SEN-SURVIVORS (NCT04733534, St. Jude, fase II)** - dasatinib+quercetina vs fisetina en sobrevivientes adultos de cáncer infantil.
24. **NCT00777036 (St. Jude/COG, fase II)** - dasatinib en niños con CML (precedente de seguridad pediátrica).
25. **PMC11625622 (2024)** - revisión *BubR1 and SIRT2*: eje NAD+/SIRT2→BubR1 como diana terapéutica; vínculo con rabdomiosarcoma embriónico.
26. **UniteRare (2026)** - sin fármacos FDA aprobados ni ensayos reclutando para MVA (openFDA/ClinicalTrials.gov sincronizados).
27. **SciELO** (Tordecilla 2021; Fonseca-Aguirre 2024; Sarmiento-Piña 2024) - rabdomiosarcoma en LatAm; sin casos MVA/BUB1B publicados en SciELO/LILACS.

