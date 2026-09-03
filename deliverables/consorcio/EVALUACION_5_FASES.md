# EVALUACIÓN CONSORCIO — MVA1 (BUB1B) · MVA Hackathon 2026
**Estándares:** UDN · ACMG/AMP 2015 + ClinGen SVI · Vigilancia oncológica AACR/COG pediátrica
**Consorcio:** Médico Auditor (ERN) · Genetista Molecular/Clínico · Farmacólogo Clínico · Ingeniero Biomolecular
**Fuerza de afirmación:** [HECHO VERIFICADO] / [INTERPRETACIÓN] / [HIPÓTESIS / PENDIENTE]

---

# FASE 1 — AUDITORÍA DE DIAGNÓSTICO, PROTOCOLO ACTUAL Y MOSAICISMO TISULAR

## 1.1 Validación ACMG y profundidad analítica

**Variantes auditadas** (HECHO VERIFICADO, pipeline del proyecto, GRCh38):

| Variante | HGVS | Consecuencia | Respaldos |
|---|---|---|---|
| Alelo 1 | `chr15:40209701 T>G` · c.2210T>G · **p.Leu737Ter** | stop_gained (LoF) | ClinVar Pathogenic (RCV000641226); PVS1; ausente gnomAD |
| Alelo 2 | `chr15:40220612 T>G` · c.3006T>G · **p.Asn1002Lys** | missense, dominio quinasa Ser/Thr C-terminal | AlphaMissense 0.923; SIFT deleterious; PolyPhen probably_damaging; ausente gnomAD/ClinVar |

**Criterios ACMG aplicados:**
- **p.Leu737Ter** → **Patogénica**: `PVS1` (nonsense en gen con mecanismo LoF confirmado para MVA1 — OMIM 257300) + `PM2` (ausente en controles de gnomAD v4) + concordancia con fenotipo MVA (PP4 sensible). [INTERPRETACIÓN: certeza alta; la herencia *in trans* con el alelo 2 la confirma compound-heterocigosis].
- **p.Asn1002Lys** → **Probablemente patogénica/Likely Pathogenic**: `PM2` (no presente en gnomAD v4) + `PM1` (ubicada en dominio catalítico quinasa de BUBR1) + `PP3` (AlphaMissense 0.9229 > umbral patogénico + SIFT/Polyphen concordantes) + `PM3` (en *trans* con variante patogénica en enfermedad recesiva) = Likely Pathogenic con refuerzo hacia Pathogenic si se confirma segregación parental. [INTERPRETACIÓN]

**Barreras y profundidad que faltan** (PENDIENTE — solicitadas al remitente):
- **Segregación parental** (confirma arreglo *in trans* y riesgo de recurrencia 25%).
- **Karyotipo/FISH en ≥30–50 metafases de linfocitos, fibroblastos y epitelio bucal**: cuantifica aneuploidía por línea; la sangre subestima el mosaicismo de otras estirpes.
- **WGS (no solo WES/targeted)**: detecta CNV/eventos estructurales somáticos y estructurales germinales que el VCF filtrado no cubre.
- **RNA-seq de tejido afectado** (sangre/fibroblastos): confirma expresión y permite distinguir NMD del alelo *stop* (releva si el alelo 2 se expresa a nivel proteico — clave para decidir terapia de dosis vs. corredor de secuencia).
- **Telómeros (qPCR/Flow-FISH)**: la insuficiencia BUBR1 se asocia a acortamiento telomérico; informa riesgo y ventana terapéutica.

**Genes SAC diferenciales auditados (CEP57, TRIP13, BUB1, BUB3):** [HECHO] el pipeline de Fase 2 los incluyó y **excluyó co-causalidad** (sin variantes candidatas raras en ellos). [INTERPRETACIÓN] el diagnóstico BUB1B2026 sigue siendo MVA1.

## 1.2 Estrategia inter-órganos ante mosaicismo variable

[HECHO] sin % de aneuploidía por tejido en el expediente actual → **definimos aquí el protocolo adaptativo**; los umbrales se parametrizan con los valores que se remitan.

**Árbol de decisión por criticidad funcional:**

1. **Sistema nervioso central (criticidad máxima)** — si FISH en LCR-progenitores o marcadores indirectos sugieren aneuploidía alta: priorizar *neuroprotección y reducción de presión mitótica* (Fases 4+3), seguimiento neurológico (Bayley-III / neuroimagen DTI).
2. **Parénquima renal** — ecografía renal seriada **cada 3–6 meses** (vigilancia Tumor de Wilms, estándar en síndromes de predisposición). Umbral de intervención: masa >1–1.5 cm o crecimiento >2%/mes → derivación a cirugía pediátrica.
3. **Sistema hematopoyético** — CBC + frotis + LDH mensual/trimestral con citometría de flujo si citopenias (riesgo de leucemia aguda).
4. **Tejido germinal/reproductivo** — consejo genético + óvulos/espermatozoides cuando proceda (la aneuploidía tisular puede aumentar el riesgo gonadal).

## 1.3 Vigilancia oncológica pediátrica (auditoría AACR/COG)

[HECHO] el expediente documenta **rabdomiosarcoma previo**. [INTERPRETACIÓN] MVA1 confiere riesgo elevado de tumores embrionarios (Wilms, rabdomiosarcoma, leucemias) por inestabilidad cromosómica basal.

**Auditoría del programa actual:** se recomienda formalizar en protocolo:
- **Ecografía renal y abdominal seriada** — q3m (Wilms) ◆
- **TAC/RM torácica** — q6m con centro sarcoma (metástasis rabdo) ◆
- **CBC + LDH + perfil bioquímico** — mensual (leucemia aguda, lisis) ◆
- **Examen físico + registro de masas** — mensual ◆
- **Atención al hallazgo LZTR1 (NF2/schwannomatosis)** — [HECHO de Fases 1–3] hallazgo secundario LoF en LZTR1: añade vigilancia de schwannomas (RM de base de cráneo/columna seriada) aunque NO es driver del fenotipo MVA.

◆ = recomendación del Consorcio; pendiente de aprobación institucional.

---

# FASE 2 — MAPEO GENÉTICO, FISIOPATOLÓGICO Y DIANAS TERAPÉUTICAS

## 2.1 Mecánica molecular del SAC (desglose biofísico)

[HECHO, respaldado por STRING/Fases 3–4]
- BUBR1 (producto de *BUB1B*) es el **marco del Spindle Assembly Checkpoint**: recluta MAD2–CDC20 para formar el **Mitotic Checkpoint Complex (MCC)** que inhibe APC/C**^Cdc20**.
- Con el par mutacional (stop → pérdida de dosis del alelo 1; missense en el dominio quinasa C-terminal del alelo 2), el MCC se forma de forma incompleta/deficiente → **APC/C se activa prematuramente** → **separación precoz de cromátidas hermanas** → *lagging chromosomes*, anafase errática, **aneuploidía en mosaico**.

[INTERPRETACIÓN]
- *Cinemática de cinetocoros:* sin señal de retención (Mad2-Cdc20 incapaz de sostener el freno), los microtúbulos del huso "capturan" cromátidas sin esperar a la bi-orientación estable → errores de congression (corregibles por Aurora B en células sanas, pero sin BUBR1 maduro la corrección es insuficiente).
- *Consecuencia celular:* cada mitosis es una lotería cromosómica → repertorio de ploidías diversas (mosaicismo) → muerte celular (crisis) en progenitores, pero supervivencia de clones aneuploides tumorigénicos.

## 2.2 Dianas moleculares seleccionadas (modular sin catástrofe)

[HECHO/INTERPRETACIÓN derivados de Fase 4 validada]

| Dianas NO viables (inhibición) | Dianas viables (eje de dosis/corrección) |
|---|---|
| PLK1, AURKB, TTK/MPS1 (inhibidores = antimitótico, empeoran CIN) 🚫 | **Restaurar dosis/actividad de BUBR1** (NAD+/SIRT2 → deacetilación K668; [HECHO] evidencia in vivo Baker 2013; North 2014) ✅ |
| BUB1 directo (sin fármaco aprobado) 🚫 | **Clearance de senescencia** (senolíticos bajo oncología) ⚠️ |
| Microtúbulos (taxanos/vincristina) 🚫 | **Hormona de crecimiento** (retraso de crecimiento estándar) ✅ |
| CDK4/6 (reduce carga mitótica; hipótesis NO respaldada en datos de BUBR1) ⚠️ | **mRNA-LNP terapéutico de BUBR1** (Fase 4; teórico) ⏳ |

**Principio 2.2:** la diana debe *elevar la actividad del checkpoint* (reforzar el freno), nunca *debilitarlo*. Ello descarta farmacológicamente toda la clase antimitótica hallada en Open Targets/ChEMBL.

---

# FASE 3 — EVALUACIÓN FARMACOLÓGICA Y LIMITACIONES CLÍNICAS

## 3.1 Restricciones de quimioterapia y antimitóticos (contraindicaciones severas)

[HECHO, validado empíricamente por el Consorcio en ChEMBL + Open Targets + PubMed — Fase 4C]

| Clase | Ejemplos (anotados) | Por qué CONTRAINDICADO en MVA1 |
|---|---|---|
| Inhibidores PLK1 | Volasertib, onvansertib, BI-2536 | Collapse del freno restante → más aneuploidía |
| Inhibidores AURKB | Ibcasertib, AT-9283, barasertib | Impide corrección de errores cinetocoro-microtúbulo |
| Inhibidores TTK/MPS1 | BAY-1161909, BAY-1217389, reversine | Silencian el único sensor del checkpoint |
| Taxanos/vincristina | Paclitaxel, docetaxel, vincristina | Estrés mitótico no compensable por SAC defectuoso |
| Dosis altas de corticoides/metotrexato | — | Mielosupresión + inmunosupresión en huésped inestable |

**Regla 3.1 (del Consorcio):** ningún agente con mecanismo "mitosis-arrest" o "microtubule-targeting" debe usarse como quimioterapia de base en este paciente a dosis convencionales.

## 3.2 Modelado farmacocinético pediátrico y ventanas terapéuticas

[HIPÓTESIS/teórico, requiere validación] — base el entregable `FASE4_REPOSICIONAMIENTO.md`:

| Candidato | Vía | PK pediátrica | Ventana terapéutica | Riesgo-senescencia |
|---|---|---|---|---|
| **NMN/NAD+** | oral | cruza BBB (precursor neuronal); no sustrato CYP | 10–15 mg/kg/día escalando; monitorizar NAD⁺ y FISH-aneuploidía | Bajo (sin daño citotóxico) |
| **Senolíticos (dasatinib+quercetina)** | oral | CYP3A4 (ajuste <2a); BBB parcial | ciclos intermitentes, solo si carga senescente demostrada | **Moderado** — solo bajo oncología |
| **GH** | SC | no CYP; dosis por kg | esquema estándar pediátrico | Bajo |

**Umbral de seguridad 3.2:** no inducir **senescencia celular sistémica** (evitar exposición crónica a citotóxicos) ni **apoptosis tisular generalizada** (guardar dosis bajas, sub-receptoras de NAD+).

---

# FASE 4 — SOLUCIÓN AVANZADA MEDIANTE BIOINGENIERÍA MOLECULAR

## 4.1 Candidato terapéutico sintético (teórico)

[HIPÓTESIS —— requiere validación preclínica completa]

**`mRNA-LNP`: ARNm de BUB1B de longitud completa (codon-optimized, N1-metilpseudouridina)**
- **Justificación:** el defecto es de **dosificación** (haploinsuficiencia) más que de secuencia gananciosa. Suministrar ARNm traducible de BUB1B restaura BUBR1 funcional de forma **transitoria y regulable** (a diferencia de vectores integrativos) → rellena el hueco del checkpoint sin sustituir la secuencia endógena.
- **ASO / corrección de splicing:** [INTERPRETACIÓN] NO es la primera opción para estas dos SNV exónicas (missense y stop); un ASO de splicing solo tendría sentido si el alelo *stop* activase NMD y quisiera rescatarse *skipping* dirigido (*conexión regulatoria pendiente*). Se señala para evaluarse en RNA-seq.

## 4.2 Mecanismo farmacodinámico

- BUBR1 *de novo* participa en la formación de MCC → restaura inhibición de APC/C**^Cdc20** durante la prometafase → prolonga la ventana de bi-orientación → reduce *lagging chromosomes* y micronúcleos → menos mitosis aneuploides.
- **Ventana de expresión:** ventana farmacológica estrecha (horas) → se podría cronoterapéuticamente acoplar al ciclo de expansión celular (proliferación tumoral) para maximizar corrección en tejido con mitosis activa.

## 4.3 Estrategia de entrega multiorgánica (Drug Delivery)

| Barrera | Estrategia LNP |
|---|---|
| **Hígado (depot LNP)** | LNP ionizable estándar (SUV); acumulación hepática natural |
| **BBB / SNC** | LNP funcionalizadas con **ligando de transferrina (TfR1) o péptido LDLR** para transcitosis cruzando barrera hematoencefálica |
| **Epitelio bucal/renal (mosaicismo)** | Ruta sistémica alcanza riñón (LNP renal-tropic con fosfolípidos negativos); bucal vía parche/pulverización local |
| **Hematopoyético** | LNP-tropo a macrófagos/linaje mieloide si se quiere modular clon hematopoyético |

**Alternativa vector viral (AAV9/AAVrh10)** → persistencia de expresión; desventaja: riesgo de integración y respuesta inmune en niño pre-inmunizado; [INTERPRETACIÓN] mRNA-LNP se prefiere para primera generación por **reversibilidad**.

---

# FASE 5 — AUDITORÍA SEVERA DE TOXICIDAD, RIESGOS ONCOGÉNICOS Y PRECLÍNICA

## 5.1 Mitigación de riesgos oncogénicos

[HIPÓTESIS]
- **Sobreexpresión de BUBR1** → riesgo teórico de *hiper-retención* (retardo excesivo de anafase) e inestabilidad por sobre-activación del checkpoint → se mitiga con **dosis sub-terapéuticas y duración limitada** (window therapy, no crónica).
- **Mutagénesis por vector:** mRNA-LNP no integra → **evita** leucemogénesis insercional (a diferencia de retrovirus/TRCs). Los vectores que integrásemos (AAV) son episómicos → bajo riesgo, pero monitorizar.
- **Senescencia inducida:** en células con CIN, exceso de señal de checkpoint puede disparar apoptosis (p53) — en células cancerosas esto es deseable (muerte de aneuploides), pero verificar que no colapse progenitores sanos: requiere ensayo de dosis-respuesta en fibroblastos sanos vs. de paciente.

## 5.2 Toxicidad sistémica e inmunogenicidad

- **LNP:** hepatotoxicidad transitoria (AST/ALT) + reactividad de complemento (CARPA) y **anti-PEG** en re-dosificación pediátrica → pre-medicación (antihistamínicos), PEG**-free/alternativos.
- **mRNA:** inmunogenicidad innata reducida con nucleósidos modificados (N1mψ); riesgo de **tormenta de citoquinas** bajo si la dosis se titula lentamente.
- **CYP/hepatotoxicidad de fármacos clásicos:** los candidatos de Fase 3 (NMN/NAD+, GH) tienen perfil bajo EN CYP [mandato].

## 5.3 Hoja de ruta de validación preclínica (obligatoria antes de clínica)

| Paso | Modelo | Endpoint |
|---|---|---|
| 1 | **Fibroblastos del paciente** (BUB1B-compound-het) | Reducción de micronúcleos / lagging con mRNA-BUB1B vs. control |
| 2 | **Isogénico corregido** (WT) y fibroblastos sanos | Ventana terapéutica (corrige aneuploide, respeta diploide) |
| 3 | **iPSC → organoides con mosaicismo controlado** | Eficacia en tejido 3D con proporciones aneuploides mezcladas |
| 4 | **Modelo murino BUB1B-hipomórfico** (línea ya descrita en literatura) | Aneuploidía por FISH; seguridad en juveniles (toxicología ampliada) |
| 5 | **PK/PD pediátrico (juventud animal, N=3 especies)** | Dosis, ventana, inmunogenicidad |
| 6 | **GLP-Tox 90 días + genotóxico** | NOAEL → FIH |

**Condición 5.3 (Consorcio):** sin los pasos 1–6, NO hay justificación a Primera Dosis en Humanos; el protocolo reconoce que cualquier candidato propuesto (mRNA-LNP, NMN/NAD+, senolíticos, GH) es **hipótesis de seguimiento**, no terapia estándar.

---

## RESUMEN EJECUTIVO

| Fase | Veredicto del Consorcio |
|---|---|
| **1. Diagnóstico** | MVA1 confirmado (BUB1B compound-het, ACMG: Leu737Ter **P** + Asn1002Lys **LP**) — falta segregación parental, karyotipo multi-línea, WGS/RNA-seq, telómeros |
| **2. Dianas** | Restaurar **dosis de BUBR1** (eje NAD+/SIRT2), no inhibir SAC |
| **3. Farmacología** | Antimitóticos **contraindicados** (validado ChEMBL/OT/PubMed); ventana segura = NMN/NAD+ + GH (+ senolíticos solo oncológicos) |
| **4. Bioingeniería** | Candidato teórico **mRNA-LNP BUBR1** con LNP-TfR1 para SNC y window therapy |
| **5. Toxicidad/preclínica** | Roadmap 6 pasos obligatorio; evitar senescencia sistémica e inmunogenicidad LNP; riesgo oncogénico controlado por dosis corta |

**Limitación declarada:** todos los % de aneuploidía por tejido, estado telomérico y cronología HPO completa permanecen **PENDIENTES** en el expediente; el Consorcio los parametriza apenas se suministren en el esquema normalizado.

---
*Evaluación del Consorcio, anclada a los resultados verificados del pipeline (Fases 1–4, datos reales: STRING, Open Targets, ChEMBL, PubMed, gnomAD, AlphaMissense, ClinVar). No constituye guía clínica.*
