# Comparativa de Participantes — MVA Hackathon 2026 (Track 1 & Track 2)

**Equipo:** byronzunigao (nosotros)
**Fuente de datos:** repos públicos de GitHub de participantes + nuestro workspace.
**Cadencia:** actualización diaria automática (hasta el cierre del leaderboard, 24 oct 2026).
**Última actualización:** (fecha automática al correr el monitor)

> **Aviso importante sobre la métrica (confirmado por participante MikeRecognex, 2026-08-27):**
> *"39 of 39 entries score 100.0 rank points and F-max 1.000"* — el leaderboard **automático de Track 1
> está saturado**. Todo equipo que acierta el par BUB1B en rank 1 obtiene **100/100 pts y F-max 1.0**.
> Por tanto, la métrica automática **no diferencia modelos**; la diferenciación real está en el
> **Track 2 (panel de expertos)** y en la calidad/rigor del método documentado.

---

## 1. Convergencia en el diagnóstico (Track 1)

Cinco pipelines **independientes** (100% de consenso) convergen en el **mismo par causal**:

| | Alelo 1 (BUB1B) | Alelo 2 (BUB1B) | Score declarado |
|---|---|---|---|
| **byronzunigao (nosotros)** | chr15:40209701 T>G · p.Leu737Ter | chr15:40220612 T>G · p.Asn1002Lys | 100 / F-max 1.0 |
| michalbutkiewicz0000 | chr15:40209701 T>G · p.Leu737Ter | chr15:40220612 T>G · p.Asn1002Lys | 100/100 · F-max 1.0 |
| bralewild | chr15:40209701 T>G · p.Leu737Ter | chr15:40220612 T>G · p.Asn1002Lys | 100/100 · F-max 1.0 (epcr 0.95) |
| MikeRecognex | BUB1B (posición no revelada) | BUB1B | 100.0 / F-max 1.000 |
| tfius (texdata) | BUB1B | BUB1B | 100/100 · full match rank 1 |

**Interpretación:** el diagnóstico **MVA1 (OMIM 257300) por compound-heterocigosis BUB1B** se
confirma de forma **robusta y reproducible**. La variante nonsense p.Leu737Ter (ClinVar
Pathogenic) + el missense novel p.Asn1002Lys (AlphaMissense 0.923) en el dominio quinasa son el
par molecular canónico de MVA1.

---

## 2. Tabla comparativa de métodos y modelos

### Track 1 — Variant prediction

| Participante | Herramientas / "modelos" | Enfoque | Fortaleza |
|---|---|---|---|
| **byronzunigao (nosotros)** | Claude LLM (HPO) + Ensembl VEP + gnomAD v4 GraphQL + ClinVar + AlphaMissense + ACMG | Fenotipo→HPO→genes (MVA) → escaneo de exones tabix → anotación → ACMG | Evidencia-first determinista; LLM nunca toca coordenadas; exclusión con paneles SAC + cancer/renal |
| michalbutkiewicz0000 | gnomAD r4 GraphQL + CADD + PhyloP + SpliceAI + SIFT/PolyPhen | Streaming VCF → hard QC → priorización impacto×rareza → compound-het pairing | Barrido de 106 genes SAC/cohesión/DDR/centrosoma; re-verificación live contra gnomAD/ClinVar/dbSNP |
| bralewild | SnpEff + HPO semantic similarity + herencia/frecuencia | **Blind** genome-wide (5,012,204 vars, 140 genes, sin pistas) | Método "ciego" sin nombres de enfermedad; margen 22.8% sobre ZFP57 rank2 |
| MikeRecognex | Hard-filter (QD/MQ/FS, no VQSR) + ClinVar join + depth scan 47 bins + IGV manual | Triage + **revisión de fase cis/trans** + exclusión de deleción grande | Máxima transparencia de discard ledger; mejor manejo de fase y falsos positivos |
| tfius (texdata) | **Exomiser** (fenotipo-gen) + ClinVar scan + SV/coverage + align + phasing | 10 pasos: ref→normalize→clinvar→deepdive→phanerode→SV→phase | Usa gold-standard clínico (Exomiser); manejo de SV/aneuploidía |

### Track 2 — Drug repurposing

| Participante | Herramientas / "modelos" | Mecanismo | Candidatos | Resultado clave |
|---|---|---|---|---|
| **byronzunigao (nosotros)** | Razonamiento mecanístico + literatura + análisis de vías | Hypomorph BubR1 residual; checkpoint roto | **NMN/NAD+ (vía SIRT2)**, **senolíticos**, **GH** | Anti-mitóticos **contraindicados** |
| tfius (texdata) | **TxGNN** (GNN zero-shot) + **PrimeKG/OptimusKG** + ChEMBL | "Más BubR1" por 3 vías independientes | NMN/nicotinamide riboside (SIRT2), inhibidores CREBBP/EP300, readthrough | **Los grafos recomiendan anti-mitóticos (contraindicados)** — el GNN no sabe que el checkpoint está roto; valida nuestra vía NAD⁺/SIRT2 (*Baker NCB 2013*) |
| bralewild | Screen unbiased readthrough (~1,600 fármacos) + filtro HPO | Readthrough del alelo nulo p.Leu737Ter | **Escina** (readthrough), gentamicina, ataluren, amlexanox | Escina gana por estar comercializada y sin conflicto con nefrocalcinosis |

---

## 3. ¿Ventaja competitiva?

**Track 1 (automático):** NO hay diferenciación — leaderboard saturado en 100/1.0. Nuestra
ventaja es **defensiva/rigor**: caveat de fase in-trans declarado, exclusión de co-causa con
paneles ampliados (equivalente al cis/trans de MikeRecognex).

**Track 2 (panel de expertos — donde sí puntúa):** nuestras hipótesis (NAD⁺/SIRT2 + readthrough +
senolíticos) están **alineadas con la evidencia de mayor respaldo biológico** (ver tfius/Baker).
A diferencia de la IA de grafos (TxGNN), nosotros **integramos la biología del variant**
(checkpoint roto), evitando el error de recomendar anti-mitóticos.

---

## 4. Registro de monitoreo (nuevos participantes)

| Fecha | Participante | Repo | Método resumido | Estado |
|---|---|---|---|---|
| 2026-08-31 | byronzunigao | (local) | Pipeline HPO+genómico determinista ACMG | Analizado |
| 2026-08-31 | michalbutkiewicz0000 | github.com/michalbutkiewicz0000/mva-hackathon-2026 | VCF streaming + gnomAD r4 + compound-het | Analizado |
| 2026-08-31 | bralewild | github.com/bralewild/mva-hackathon-2026 | Blind WGS triage + HPO semantic rank | Analizado |
| 2026-08-31 | MikeRecognex | github.com/MikeRecognex/mva-hackathon-2026 | Triage + hard-filter + fase + discard ledger | Analizado |
| 2026-08-31 | tfius (texdata) | github.com/tfius/mva-hackathon-2026 | Exomiser + TxGNN/PrimeKG track2 | Analizado |

*(El monitor agrega filas aquí conforme detecta repos nuevos.)*
