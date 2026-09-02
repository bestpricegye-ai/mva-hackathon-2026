# Video pitch — Track 2 (MVA Hackathon 2026) · byronzunigao

Guion del pitch (3:00) a **nivel científico (formato paper)**, con citas primarias y la localización
de la evidencia de cada dato. La narración reconstruida es la fuente única del video; render con
`src/hacer_video.py` → `pitch_byronzunigao.mp4`.

---

## Escena 1 · Caso: MVA1 (OMIM #257300) — WGS real GRCh38

**Narración:**
> Hola, soy Byron Zúñiga, del equipo byronzunigao. Presentamos un caso real de aneuploidía variegada en
> mosaico, MVA tipo 1, OMIM 257300: una enfermedad ultra rara. La entrada del análisis es un exoma
> completo en GRCh38 y el fenotipo clínico del probando. Las células pierden y ganan cromosomas por un
> punto de control mitótico deficiente, y el paciente desarrolló un rabdomiosarcoma. Malumbres, en Nature
> Reviews Genetics, confirma que hoy no existe tratamiento aprobado. Proponemos un reposicionamiento
> mecanismo-primero, anclado a la proteína causal.

**Bullets:**
- PROBAND01 · WGS GRCh38 + HPO clínica (8 rasgos)
- CIN: aneuploidía variegada en mosaico
- Rabdomiosarcoma en la infancia
- Sin tratamiento aprobado (Malumbres 2024)

**Footer:** Fuente: VCF `WGS_EX2312012` + `clinical_history.json` · OMIM #257300 · Orphanet #1052

**Evidencia de cada dato (dónde):**
| Dato | Dónde se obtuvo |
|---|---|
| Genotipo/GRCh38 | `data/results/vcf_exonic_variants.txt` (VCF provisto, FILTER=PASS) |
| Fenotipo HPO (8 rasgos) | `data/results/clinical_history.json` (texto clínico del reto) |
| No hay tratamiento aprobado | Malumbres & Villarroya-Beltri, **Nat Rev Genet 2024;25:864** (PMID 39169218) |

---

## Escena 2 · Diagnóstico molecular: BUB1B compound-het

**Narración:**
> El diagnóstico se ancla al genotipo. El probando es heterocigoto compuesto en BUB1B: p.Leu737Ter,
> stop-gain que trunca la proteína, criterio PVS1; y p.Asn1002Lys, missense novel en el dominio quinasa,
> con puntaje AlphaMissense 0.923. Hanks, en Nature Genetics de 2004, estableció que las mutaciones
> bialélicas de BUB1B predisponen a aneuploidía y cáncer. El resultado es BUBR1 haploinsuficiente:
> punto de control del huso debilitado. El defecto es de pérdida de función: lo que pide la biología
> es más BUBR1 funcional.

**Bullets:**
- p.Leu737Ter — stop-gain, PVS1 (trunca BUBR1)
- p.Asn1002Lys — novel, dominio quinasa · AlphaMissense 0.923
- BUBR1 haploinsuficiente → SAC débil
- Hanks 2004 (Nat Genet): bialélicas BUB1B → MVA1

**Footer:** GRCh38: chr15:40209701 T>G + chr15:40220612 T>G · PASS QUAL 708.77 · gnomAD 3.29e-5 / novel

**Evidencia:**
| Dato | Evidencia / dónde |
|---|---|
| Coordenadas, QUAL, AD (VAF 0.54/0.46) | `vcf_exonic_variants.txt` + `verificacion_dirigida_vcf.py` (chr15:40.19–40.23) |
| p.Leu737Ter Pathogenic | ClinVar **RCV000641226**; genotipo VCF |
| 1.000Gen./gnomAD AF | gnomAD v2.1.1 → `fase2_gnomad_completo.json` |
| Bialélicas BUB1B → MVA1 | Hanks et al., **Nat Genet 2004;36:1159** (PMID 15475955) |
| AlphaMissense 0.923 | Cheng et al., **Nature 2023;625:321** |

---

## Escena 3 · Restauración de BUBR1: eje SIRT2/NAD+

**Narración:**
> La literatura aporta una diana con datos in vivo. Baker, en Nature Cell Biology de 2013, demostró que
> aumentar BUBR1 protege de aneuploidía, de cáncer y prolonga la vida sana en ratones hipomorfos. North,
> en EMBO Journal de 2014, precisó el mecanismo: la deacetilación de la lisina 668 de BUBR1, mediada por
> SIRT2, una deacetilasa dependiente de NAD. Su precursor, NMN, eleva NAD y vía SIRT2 incrementa BUBR1.
> Es la única estrategia publicada que sube directamente la proteína afectada.

**Bullets:**
- ↑BUBR1 protege de aneuploidía/cáncer · Baker, NCB 2013
- BUBR1 se deacetila en K668 por SIRT2 (in vivo) · North, EMBO J 2014
- SIRT2 = deacetilasa NAD+-dependiente
- NMN → NAD+ → SIRT2 → estabiliza BUBR1

**Footer:** Ratón progeroide BubR1^H/H · ↑BUBR1 = única vía publicada que sube la proteína causal

**Evidencia:**
| Dato | Evidencia / dónde |
|---|---|
| ↑BUBR1 → menos aneuploidía/cáncer, +vida sana | Baker et al., **Nat Cell Biol 2013;15:96** (ncb2643) |
| BUBR1 hipomorfo → progeria + aneuploidía | Baker et al., **Nat Genet 2004;36:744** |
| SIRT2 desacetila/estabiliza BUBR1 (NAD+ dep.) | North et al., **EMBO J 2014;33:1438** (PMC4194088) |
| NMN precursor NAD+, diana farmacológica | Blanco `fase4_mapeo_blancos.json` (ChEMBL/Open Targets) |

---

## Escena 4 · Seguridad: salvaguarda explícita + candidatos secundarios

**Narración:**
> Encerramos la hipótesis en una salvaguarda de seguridad: cualquier fármaco que debilite más el punto
> de control mitótico está contraindicado: taxanos, vincristina, inhibidores de MPS1 o de TTK. Validamos
> este resultado negativo en ChEMBL, Open Targets y PubMed. Los candidatos secundarios atacan las
> consecuencias: senolíticos, como dasatinib con quercetina, eliminan la senescencia inflamatoria,
> solo bajo oncología por el sarcoma; y la hormona de crecimiento, de respuesta limitada en MVA,
> se individualiza.

**Bullets:**
- Contraindicado: taxanos · vincristina · MPS1/TTK (debilitan el SAC)
- Validado: ChEMBL + Open Targets + PubMed
- Senolíticos (dasatinib+quercetina) → solo oncología
- GH → individualizada (respuesta limitada en MVA)

**Footer:** Resultado negativo clínicamente accionable (guardrail) · Liu & Suson 2020

**Evidencia:**
| Dato | Evidencia / dónde |
|---|---|
| Contraindicación anti-mitóticos | ChEMBL/Open Targets/PubMed (blancos MPS1/TTK) · `fase4_validacion_farmacos.json` |
| Riesgo de quimio/radio en MVA | Liu & Suson 2020 (PMC7658145) |
| Senescencia en insuficiencia BUBR1 | Malumbres & Villarroya-Beltri 2024 (PMID 39169218) |
| GH de respuesta limitada | Pellicer Viudes et al. 2026 (PMID 41700350) |

---

## Escena 5 · Plan integral y marco escalable

**Narración:**
> El manejo fue auditado por un panel médico. Vigilancia oncológica cada tres meses hasta los siete años,
> según Orphanet y SIOP-Europe de 2021; hemograma seriado para mielodisplasia, como documentó Laberko;
> régimen estándar de rabdomiosarcoma; rescate experimental monitoreado con NMN y NAD; senolíticos bajo
> oncología; y genotipado parental para cerrar el diagnóstico en trans y el riesgo de recurrencia del
> 25 % por embarazo. Este marco se generaliza a otros síndromes de insuficiencia e inestabilidad
> cromosómica.

**Bullets:**
- Vigilancia oncológica c/3 meses hasta 7 años (Orphanet · SIOP-Europe 2021)
- Hemograma → MDS (Laberko 2019)
- Régimen pediátrico de rabdomiosarcoma
- Genotipado parental → riesgo de recurrencia 25 %

**Footer:** Consorcio: `VERIFICACION_MANEJO_CLINICO.md` (A1–A8 + 7 correcciones)

**Evidencia:**
| Dato | Evidencia / dónde |
|---|---|
| Vigilancia ECO renal c/3 meses→7 años | Orphanet #1052 · Hol et al., **Eur J Cancer 2021;153:51** (SIOP-Europe) |
| MDS/hemograma | Laberko et al., **Orphanet J Rare Dis 2019** (PMID 31040233) |
| Inicio al diagnóstico, espectro tumoral | Nakano et al., **Clin Cancer Res 2024;30:5009** (AACR) |
| Segregación parental / riesgo 25 % | Verificación Consorcio · OMIM #257300 (AR) |

---

## Escena 6 · Cierre

**Narración:**
> A este paciente no podemos reconstruirle el punto de control hoy. Pero sí ofrecer una vía traslacional,
> honesta y accionable, que restaura la dosis de su proteína causal con apoyo de evidencia primaria.
> Reposicionar no es hallar una droga nueva para una enfermedad vieja: es escuchar qué necesita la
> biología de ese paciente y buscar un fármaco aprobado que ya sabe hacerlo. Gracias.

**Bullets:**
- Vía traslacional, honesta y accionable
- Restaura la dosis de la proteína causal
- Pipeline reproducible F1→F6, salidas versionadas
- Gracias

**Footer:** byronzunigao · MVA Hackathon 2026 · Track 1+2 · github.com/bestpricegye-ai/mva-hackathon-2026

---

## Nota de transcripción (LLM disclosure)

Narración y guión curados por Anthropic API (Claude, términos comerciales); todas las afirmaciones son
contrastadas contra la literatura primaria citada; sin datos de identificación del paciente (PROBAND01,
procesado y anonimizado en `clinical_history.json`).