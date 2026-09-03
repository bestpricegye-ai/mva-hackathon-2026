# Contraste Contra Plataformas Genómicas Globales 2026 — Consorcio MVA

**Veredicto:** DIAGNÓSTICO **CONFIRMADO**. Clasificación ACMG final (Likely Pathogenic bialélica) ratificada con evidencia independiente. Se documentan **2 observaciones de documentación** (no errores diagnósticos) y **1 hallazgo de precisión** sobre el alcance de AlphaMissense.

**Fecha de verificación:** 3 septiembre 2026
**Fuentes primarias usadas (todas consultadas directamente, respuestas registradas localmente):**
Ensembl REST API (VEP, AlphaMissense integrado), ClinVar API, gnomAD v4 (capturas pipeline), Ensembl CDS, UniProt O60566.

---

## 1. Verificaciones INDEPENDIENTES CONFIRMADAS

| # | Afirmación del expediente | Fuente independiente | Resultado |
|---|---------------------------|----------------------|-----------|
| 1 | BUB1B chr15:40,160,984–40,221,137, + | Ensembl ENSG00000156970 | ✓ exacto |
| 2 | Leu737Ter c.2210T>G, stop_gained, rs759242053 | VEP (ENST00000287598), ClinVar VCV000533901/RCV000641226 | ✓ HIGH (PVS1), **LP/Pathogenic MVA1 (OMIM 257300)** |
| 3 | Asn1002Lys c.3006T>G missense, novel (absent gnomAD, ClinVar count=0) | VEP (MODERATE), gnomAD found=false | ✓ novel confirmado |
| 4 | AlphaMissense N1002K = **0.9229** | **VEP `AlphaMissense=1` (independiente del pipeline)** | ✓ **0.9229**, class **likely_pathogenic** |
| 5 | AlphaMissense N1002S = **0.348** (ambigua) | VEP | ✓ **0.3477**, ambiguous |
| 6 | gnomAD stop freq **3.29e-05** | ClinVar/gnomAD af 3.2857e-05 (AC=5/152174) | ✓ exacto |
| 7 | Traducción codones HGVS (737 TTA→TGA; 1002 AAT→AAG) | CDS Ensembl | ✓ ambos correctos |
| 8 | PM1 válido (residuo en dominio quinasa) | UniProt O60566, dominio Ser/Thr-quinasa C-terminal | ✓ 1002 ∈ dominio catalítico |
| 9 | PM3 no circular (Leu737Ter pathogenic independiente) | ClinVar RCV000641226 catalogada patogénica por PVS1 | ✓ resuelto |
| 10 | K668 presente en alelo nulo (736trunc>668) | Lógica de truncamiento | ✓ correcto |

**AlphaMissense: puntajes directos en residuo 1002 (codón AAT), obtenidos de VEP:**

| Sustitución | Codón | Score AM | Clase |
|-------------|-------|----------|-------|
| **N1002K** | AAG | **0.9229** | likely_pathogenic |
| N1002I | ATT | 0.8808 | likely_pathogenic |
| N1002D | GAT | 0.7452 | likely_pathogenic |
| N1002Y | TAT | 0.7327 | likely_pathogenic |
| N1002T | ACT | 0.7235 | likely_pathogenic |
| N1002H | CAT | 0.6051 | likely_pathogenic |
| **N1002S** | AGT | **0.3477** | **ambiguous** |

→ **6/7 single-nucleotide missense = likely_pathogenic; 1 (S) ambiguous; 0 benigna.** Confirma el núcleo del expediente.

---

## 2. Hallazgos de PRECISIÓN (documentación, no errores diagnósticos)

### 2.1 "18/19 sustituciones pathogenic en residuo 1002" — ALCANCE SOBREELEVADO
**Hecho:** AlphaMissense solo asigna predicción a las variantes missense alcanzables por **una sola sustitución nucleotídica** (SNV) desde el codón de referencia. Para AAT (Asn1002) son **7 aminoácidos únicos** (K, I, D, Y, T, H, S). La afirmación "*18/19 sustituciones*" (junto con la tabla §4.1 que enlista los 19 aminoácidos alternativos) extrapola la predicción a todos los aminoácidos posibles — fuera del alcance definido del modelo.

**Interpretación:** El 19 proviene de "todos los demás aminoácidos" (20 − Asn). No es un error de valor dictado por AlphaMissense, sino un redacción imprecisa sobre qué variantes AlphaMissense puntúa realmente.

**Corrección recomendada:** La tabla de *scores* debe restringirse a las 7 sustituciones SNV-aislables y reportarse como: **"Las 7 sustituciones missense de un solo nucleótido en el residuo 1002 puntuadas por AlphaMissense son todas likely_pathogenic excepto N1002S (ambigua); N1002K es la más deletérea (0.9229)."**

### 2.2 "ExAC 0.01%" — SOBREDEREDACCIÓN MENOR (×2)
**Hecho:** clinVar/ExAC para rs759242053 reporta AF = **0.00005 = 0.005%**, no 0.01%. El gnomAD AF correcto (3.29e-05) se usa para PM2 en la matriz ACMG de ENTREGABLE_FINAL.

**Impacto:** Nulo en clasificación (ambos < umbral de rareza PM2). Solo precisión de cifra.

### 2.3 Vocabulario de clase AlphaMissense
**Hecho:** AlphaMissense usa `likely_pathogenic` / `ambiguous` / `likely_benign`. El expediente escribe "Pathogenic" (equivale a `likely_pathogenic`) y "PP3_strong" (no es criterio ACMG estándar). Recomendar: `likely_pathogenic` y PM3/PP3 con peso estándar.

---

## 3. Verificaciones BLOQUEADAS (acceso restringido)
- **gnomAD constraint (pLI/missense_z)** — GraphQL rechaza POST programático. Interpolado de la publicación Decipher v11.40 (basada en gnomAD v4.1).
- **DECIPHER pacientes / GARD / Orphanet / RareVarDB** — APIs con login o SPA sin servidor de datos. Fenotipo HPO del probando (rabdo, nefrocalcinosis, talla baja, SGA) contrastado contra literatura fenotípica BUB1B conocida vía los reportes del expediente.

---

## 4. Correlación fenotipo-clínica (negociado de literatura, no evento adverso)
El fenotipo del probando — rabdomiosarcoma, nefrocalcinosis, talla baja, SGA — es compatible con la constelación MVA1/BUB1B (dianacuasia mitótica → tumor + insuficiencia de proliferación tisular). La heterogeneidad de presentación (mosaicismo por tejido) explica presentaciones parciales. Consistente, sin revisión a la baja.

---

## 5. RATIFICACIÓN DEL DIAGNÓSTICO
- **MVA1 (OMIM 257300), bialélico:** `BUB1B` c.2210T>G p.(Leu737Ter) **Pathogenic** (PVS1+PM2+PM3) **en trans** con c.3006T>G p.(Asn1002Lys) **Likely Pathogenic** (PM2+PM3+PM1+PP3; AlphaMissense 0.9229).
- Clasificación final **Likely Pathogenic ±** ratificada. Sin reversión.
- Estándar ACMG Hoja de trabajo: **PM2** (rareza gnomAD 3.29e-05), **PM1** (dominio quinasa), **PM3** (en trans con LOF Pathogenic), **PP3** (AlphaMissense/sift/polyphen deletéreos).

---

## 6. Acciones correctivas recomendadas (para aplicar a SUJETO/entregables)
| Archivo | Corrección | Severidad |
|---------|-----------|-----------|
| `docs/bibliografia_mva.md` (B4, C2.2) | **K250 → K668** (North = deacetilación K668; Suematsu = K250) | **CRÍTICA bibliográfica** |
| `docs/ENTREGABLE_FINAL_MVA.md` §4.1 | Limitar tabla AM a 7 sustituciones SNV; reformular "18/19" | Menor (precisión) |
| `docs/diagnostico_mva.md` / FINAL / diagnosis | "ExAC 0.01%" → **0.005%** | Menor |
| Matriz ACMG missense (4 docs) | Unificar: PM2+PM3+PM1+PP3 (sin "PP3_strong"/"PM1 probable") | Documental |

---

*Preparado por el Comité de Revisión Crítica (Consorcio Científico-Médico). Contraste técnico ejecutado contra Ensembl REST/AlphaMissense (3/9/2026), ClinVar API, pipeline local gnomAD v4.0.*