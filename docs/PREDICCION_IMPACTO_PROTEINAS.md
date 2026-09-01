# PREDICCIÓN DEL IMPACTO FUNCIONAL DE PROTEÍNAS (Track 3)
## Resolución del VUS p.Asn1002Lys en BUB1B mediante modelo de lenguaje de proteínas (AlphaMissense)

**Caso:** Proband Clinical Phenotype 1 (WGS_EX2312012_HGWCNDSX7)
**Variante en estudio (VUS):** `chr15:40220612 G>T` → `c.3006T>G` → **p.Asn1002Lys** en BUB1B/BUBR1 (ENST00000287598, UniProt O60566, 1050 aa)

---

## 1. Contexto: ¿por qué era un VUS?

Sin precedentes clínicos ni validación funcional, la missense `Asn1002Lys` era de **Significado Incierto**:
- Ausente en gnomAD (genome:null) y en ClinVar (novel).
- Predictores evolutivos clásicos la señalaban: SIFT = deleterious (0.01), PolyPhen = probably_damaging (0.997), pero de forma aislada no alcanzaban la clasificación patogénica definitiva.

## 2. Enfoque de modelo de lenguaje de proteínas (pLM) basado en estructura

**AlphaMissense** (DeepMind, Jumper et al. 2023, Science) es un pLM que integra:
- **Embeddings de lenguaje de secuencia** (de ESM/traductor genético proteico).
- **Estructura tridimensional** derivada de AlphaFold (folds de BUB1B disponibles: O60566-F1).
- Alineamientos multi-secuencia (evolución cruzada de especies).

Produce un score `am_pathogenicity ∈ [0,1]` que mide la probabilidad de que una sustitución sea patogénica **por su efecto estructural/funcional**, imitando la señal que daría una simulación biofísica sin su costo computacional.

## 3. Resultado para Asn1002Lys

| Criterio | Valor | Interpretación |
|---|---|---|
| **am_pathogenicity (N1002K)** | **0.9229 / 1.0** | **Pathogenic** (umbral AM: ≥0.564) |
| clasificación AlphaMissense | **pathogenic** | patogénica predicha |

## 4. Análisis del residuo 1002: hotspot funcional restringido

Se consultaron **todos los cambios posibles en el residuo 1002** de BUB1B (19 sustituciones):

| Clase | Sustituciones | Score AM |
|---|---|---|
| **Pathogenic** | A, C, D, E, F, G, H, I, **K**, L, M, P, Q, R, T, V, W, Y (18) | 0.60 – 0.98 |
| **Ambiguous** | S | 0.348 |
| Benign | — | 0 |

- **18 de 19 sustituciones en la posición 1002 son patogénicas.** Solo N1002S es "ambiguous" (0.35) y ninguna es benigna.
- Un residuo tan **intolerante a la sustitución** indica fuerte presión selectiva: la posición 1002 es **funcionalmente crítica**.
- Mean de patogenicidad del residuo = **0.819** (promedio sobre todas las sustituciones), muy por encima del umbral.

## 5. Contexto estructural

El residuo **N1002 se ubica en el extremo distal del dominio quinasa serina/treonina C-terminal de BUBR1** (dominio que fosforila a CDC20 y es esencial para la inhibición del APC/C en el spindle assembly checkpoint). Una Asn→Lys introduce una **carga básica positiva adicional (+1)** y mayor volumen de cadena lateral en una región estructuralmente restringida de catálisis — consistente con error de plegado/unión de sustrato.

## 6. Integración con la clasificación ACMG

La evidencia de pLM actúa como soporte **PP3** (in silico concordante múltiple). Al combinarse en la red de evidencias (ver `diagnostico_mva.md`):

- **PM2** (ausente en control poblacional) — estricto
- **PP3** (SIFT deleterious + PolyPhen probably_damaging + **AlphaMissense pathogenic 0.92**) — múltiple concordante
- **PM3** (en trans con la LOF patogénica Leu737Ter, heterocigosis compuesta)

→ **Likely Pathogenic** (VUS resuelto).

## 7. Conclusión del Track

El modelo de lenguaje de proteínas resolvió el dilema VUS de forma independiente y más concluyente que los predictores evolutivos clásicos: con un score AM de **0.92 (pathogenic)** y una posición-1002 que es un **hotspot donde 18/19 sustituciones son deletéreas**, la variante Asn1002Lys se comporta como una mutación funcionalmente dañina, no como un cambio neutro. Esto cierra el diagnóstico de **heterocigosis compuesta en BUB1B (MVA1)**.

---

*Los scores AlphaMissense son predicciones computacionales de patogenicidad, no clasificaciones clínicas ACMG finales; se usan aquí como soporte dentro del marco ACMG/AMP junto con los demás criterios.*
