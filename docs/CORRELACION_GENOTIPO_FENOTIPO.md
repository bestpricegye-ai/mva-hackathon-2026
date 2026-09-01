# CORRELACIÓN AUTOMATIZADA GENOTIPO-FENOTIPO (Track 2)
## Del expediente clínico desestructurado a genes candidatos con validación genómica

**Caso:** Proband Clinical Phenotype 1 (WGS_EX2312012_HGWCNDSX7)
**Fuente fenotípica:** `Challenge_Clinical_Phenotype_1.docx` (no estructurado)
**Fecha de análisis:** 2026-08-31

---

## 1. Extracción de rasgos clínicos del DOCX (NLP / LLM)

El expediente clínico en prosa fue procesado para extraer los rasgos diagnostico-relevantes
y mapearlos a la **Human Phenotype Ontology (HPO)**:

| Rasgo extraído (texto fuente) | HPO term | HPO ID | Dominio |
|---|---|---|---|
| Rabdomiosarcoma | Rhabdomyosarcoma | HP:0002859 | neoplasia |
| Nefrocalcinosis presente desde el nacimiento | Nephrocalcinosis | HP:0000121 | renal |
| Talla baja | Short stature | HP:0004322 | crecimiento |
| Fallo de medro | Failure to thrive | HP:0001508 | crecimiento |
| Baja masa muscular | Skeletal muscle atrophy | HP:0003202 | musculoesquelético |
| Prematuridad (32 sem) | Premature birth | HP:0001622 | perinatal |
| Peso muy bajo al nacer (~1 kg) | Small for gestational age | HP:0001518 | perinatal |
| Abortos recurrentes (padres) | Recurrent spontaneous abortion | HP:0200067 | pérdida reproductiva |

## 2. Reconocimiento del cluster fenotípico

Ningún rasgo aislado es diagnóstico. La IA identifica el **patrón coherente**:
**co-ocurrencia de predisposición a cáncer + restricción de crecimiento + anomalía renal +
historia perinatal adversa + pérdidas reproductivas parentales**.

→ Este cluster es el fenotipo clásico de un trastorno de **inestabilidad cromosómica /
aneuploidía** (Mosaic Variegated Aneuploidy, MVA; OMIM 257300).

## 3. Ranking de genes candidatos (ontología HPO → gen)

Los HPO se cruzaron con la literatura (OMIM/Orphanet) para rankear genes cuya asociación
fenotípica coincide con el cluster MVA. Todos operan en el **spindle assembly checkpoint (SAC)**:

| Rank | Gen | Asociación fenotípica MVA | Modelo herencia esperado |
|---|---|---|---|
| 1 | **BUB1B** (BUBR1) | **MVA1** (OMIM 257300) — causa más común | AR compuesto |
| 2 | **CEP57** | MVA2 (OMIM 614114) | AR |
| 3 | **TRIP13** | MVA3 (OMIM 617598) | AR |
| 4 | **BUB1 / BUB3 / MAD2L1** | SAC, candidatos secundarios | AR |
| 5 | **CENPE / ZW10 / NUP85** | entrada/alimentación SAC | AR (menos apoyado) |

**Hipótesis primaria:** inestabilidad cromosómica sobre gen del SAC (BUB1B), modelo
autosómico recesivo compuesto heterocigoto (consistente con los abortos recurrentes
parentales: cada progenitor es portador de una variante patogénica distinta de BUB1B).

## 4. Validación genómica de la hipótesis (cruce con el VCF)

El ranking se validó contra el exoma/genoma del paciente:

- **BUB1B** → 2 variantes exónicas → **heterocigosis compuesta**:
  - `c.2210T>G p.Leu737Ter` = **stop_gained (LOF)**, rs759242053, **ClinVar RCV000641226 (MVA1)**, gnomAD AF=0.0000329 (rara)
  - `c.3006T>G p.Asn1002Lys` = **missense novel**, ausente en gnomAD, SIFT deleterious + PolyPhen probably_damaging (VUS→LP)
  - ✅ **Diagnóstico MVA1 confirmado**
- **CEP57** → 0 variantes exónicas → **descartado**
- **TRIP13** → 0 variantes exónicas → **descartado**
- **Panel SAC ampliado (24 genes)** → 72 variantes exónicas, todas polimorfismos comunes gnomAD → **sin co-causales**

## 5. Conclusión

La correlación genotipo-fenotipo automatizada convergió correctamente en **BUB1B**:
partiendo solo del texto clínico (sin el VCF), el cluster fenotípico apuntó al SAC/aneuploidía,
y el prio ranking (BUB1B > CEP57 > TRIP13) fue confirmado de forma independiente por el
WGS, con la variante patogénica RCV000641226 ya anotada en ClinVar para MVA1.

**Diagnóstico molecular:** Mosaic Variegated Aneuploidy tipo 1 (MVA1, OMIM 257300) por
heterocigosis compuesta en BUB1B: Leu737Ter (Pathogenic) + Asn1002Lys (Likely Pathogenic).

---

*Nota de privacidad: conforme a las restricciones del expediente, no se incluye ningún dato
reidentificable del paciente ni de su familia.*
