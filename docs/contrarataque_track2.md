# Contrataque Track 2 — Mejorar lo nuestro, no copiar al rival

**Equipo:** byronzunigao
**Fecha:** 2026-09-02
**Propósito:** análisis adversarial de las dos propuestas de Track 2 más fuertes (tfius/texdata y
bralewild) para REFUTAR sus debilidades y REFORZAR nuestro diferencial, respetando el lema
"mejora lo nuestro sin copiar su trabajo".
**Criterio de rigor:** todo lo que se afirma del rival está tomado de sus repos públicos
(`github.com/tfius/mva-hackathon-2026`, `github.com/bralewild/mva-hackathon-2026`) y es verificable.

---

## 0. Estado del tablero

| Participante | Enfoque Track 2 | Candidato final | Diferencial declarado |
|---|---|---|---|
| **byronzunigao (nosotros)** | Mecanismo → "más BubR1" + **guardrail anti-mitótico explícito** + **ruta de reemplazo génico (mRNA-LNP)** | **NMN/NAD+ (SIRT2)** + senolíticos + GH + readthrough (PTC) 4º | Integra la biología del variant; auditoría de toxicidad Fase 5; **roadmap preclínico** |
| **tfius (texdata)** | Knowledge-graph (PrimeKG/OptimusKG) + TxGNN + GraphMask | 6 candidatos → "más BubR1" (NAD+/SIRT2, CBP/p300, PTC) | Audita los sesgos del GNN; detecta que BubR1 es "undrugged" |
| **bralewild** | Screen DGIdb/OpenTargets + dirección-de-efecto + readthrough PTC | **Escina (escin)** — el único comercializado no conflictivo | Control positivo (CFTR/PAH) y negativo (AURKB); pipeline de 2 min |

**Lectura honesta:** somos los tres convergiendo en la misma conclusión de fondo ("BubR1 no tiene
fármaco que lo suba directo; hay que restaurar niveles/actividad"), pero desde **tres metodologías
distintas**. La competición no es por el "qué" (todos decimos más BubR1) sino por el **cómo lo
demuestras** y por **qué entregable clínico más completo aportas**.

---

## 1. Análisis de la amenaza tfius (texdata) — refutación

### Qué hace fuerte a tfius (FACTOS de su repo)
1. **Análisis de knowledge-graph de primer nivel**: detectó que *BUB1B tiene 464 edges en PrimeKG y
   CERO drug edges* — "BubR1 is undrugged". Reproducido con OptimusKG (4× más denso). Es un hallazgo
   **genuino y bien demostrado**.
2. **Autocrítica documentada**: encontraron 5 errores propios (el "K668 deleted en el alelo nulo",
   vincristina mal clasificada, LZTR1 invertido, ACMG mal calculado) vía revisores IA independientes.
   Esta honestidad es atractiva para el panel.
3. **Sesgo del GNN expuesto**: TxGNN recomendaba paclitaxel/vinblastina (anti-mitóticos) y ellos lo
   corrigen por mecanismo.

### Debilidades de tfius que PODEMOS REFUTAR
1. **El GNN recomendó anti-mitóticos EN SU PROPIO pipeline** — aunque lo autocrítican, el entregable
   central ("TxGNN zero-shot repurposing") produjo el error que nosotros evitamos desde el diseño.
   Es un **hallazgo negativo elegante, pero no una propuesta terapéutica**. Da "éxito de auditoría",
   no "candidato accionable".
2. **Sus 6 candidatos → ningún candidato único final con peso clínico concreto.** Es "más BubR1"
   desglosado, pero **no entrega un plan clínico integrado** (vigilancia oncológica + GH + consejo
   reproductivo) como nosotros.
3. **CBP/p300 inhibition**: proponen inhibir el "writer" de la marca acetilo desestabilizadora
   (CREBBP/EP300). Esto es **más especulativo** que la vía NAD+/SIRT2 porque:
   - Inhibir CBP/p300 es **epigenéticamente promiscuo** (acetilan miles de dianas, no solo BUBR1).
   - Riesgo de toxicidad acético global/HAT. Tanpamisu/curcumin breadth issues.
   - No tiene datos in-vivo de que específicamente suba BubR1. Nosotros tenemos Baker 2013/2017
     (in-vivo real).
4. **No ofrece opción de reemplazo génico / mRNA-LNP** — se quedan en farmacología química.
   Nosotros tenemos la **Fase 6** (mRNA-LNP 72/100, jerarquía de opciones SNV).

### Nuestra contra (lo que ya tenemos y le falta a tfius)
- **Candidato accionable con mayor peso de evidencia in-vivo**: la vía NAD+/SIRT2 (nuestra top) está
  **respaldada por datos en ratones hipomórficos** (Baker NCB 2013). La CBP/p300 de tfius **no**.
- **Plan clínico integral** (onco-vigilancia + GH + reproducción) frente a su lista de 6 mecanismos.
- **Auditoría de toxicidad severa** (Fase 5) en contexto pediátrico oncológico, no solo un "guard".
- **Opción de reemplazo génico (mRNA-LNP)** para cuando la química no baste.

---

## 2. Análisis de la amenaza bralewild — refutación

### Qué hace fuerte a bralewild (FACTOS)
1. **Control positivo y negativo impecable**: su pipeline admitió ivacaftor (CFTR) y sapropterin (PAH)
   y rechazó AURKB — prueba que el filtro no es demasiado estricto. Método de validación robusto.
2. **Filtro de dirección de-efecto**: descarta inhibidores que empeorarían un LoF. Elegante y reutilizable.
3. **Candidato concreto y comercializado**: Escina (escin), con reordenamiento por fenotipo HPO.
4. **Pipeline de 2 min** y transparente.

### Debilidades de bralewild que PODEMOS REFUTAR
1. **Escina tiene efecto esperado PEQUEÑO y ellos mismos lo admiten** ("Expected effect size is small").
   Es una apuesta de readthrough de bajo retorno biológico.
2. **Readthrough (PTC) es la vía MÁS CONTROVERTIDA** — exactamente donde nosotros la pusimos en 4º
   lugar con pro/con documentado (PTC124/ataluren sin readthrough reproducible en ensayos
   independientes; McElroy 2013). bralewild la hace su **único** candidato accionable. Eso es una
   **debilidad estructural**: concentran todo el peso clínico en el mecanismo más incierto.
3. **Ignoran el alelo missense p.Asn1002Lys**: el readthrough solo ataca el alelo nulo (PTC); no
   resuelve el defecto de la quinasa del missense. **No restauran la dosis completa del par**. Nosotros
   sí: nuestra vía NAD+/SIRT2 sube BubR1 globalmente (ambos alelos) y además tenemos mRNA-LNP.
4. **No manejan el contexto oncológico activo** con la profundidad nuestra: solo cruzan HPO para
   "liability", nosotros hacemos gestión de vigilancia GH/sarcoma/NAD+ en malignidad activa.

### Nuestra contra (lo que ya tenemos y le falta a bralewild)
- **Readthrough como hipótesis de seguimiento, NO como candidato principal** — diferente priorización
  con el mismo respeto a la evidencia. Ellos lo ponen al frente; nosotros lo ponemos en 4º con pro/con.
- **Abarcamos ambos alelos** (nulo + missense) con NMN/SIRT2 y con mRNA-LNP de reemplazo total.
- **Peso en evidencia in-vivo (Baker/North)** frente a screen in-silico de DGIdb.

---

## 3. Plan de contratataque — 7 acciones concretas (mejorar lo nuestro)

> Principio: NO copiamos su metodología (graphs, screens de fábrica). Reforzamos lo que ya tenemos
> y cerramos los huecos que su análisis evidencia en común.

### Acción 1 — Blindar el readthrough como #4 (ya hecho, reforzar pro/con)
Ambos rivales convergen en PTC-readthrough como salida. Añadir a nuestro reporte una frase explícita
que **cite que la evidencia independiente falló** (PTC124/ataluren, CF trials contradictorios, McElroy
PMC3692445) con peso suficiente para que el panel vea que NO lo eludimos por ignorancia sino por rigor.

### Acción 2 — Blindar el anti-mitótico como guardrail (ya hecho, ampliar)
Nosotros y bralewild coincidimos en que los anti-mitóticos (taxanos/vincristina/TTK) están
contraindicados. Nuestra ventaja: la **dicotomía vincristina (SOC obligado) vs TTK/MPS1 (sabotaje
deliberado)**. Reforzar que esta distinción es **clínicamente operativa** (monitorización de aneuploidía
durante VAC) — bralewild solo los descarta por "dirección". Nosotros damos un plan de manejo del
riesgo, no solo una bandera roja.

### Acción 3 — Convertir nuestro diferencial de reemplazo génico (mRNA-LNP) en sección del Track 2
Es lo que NI tfius NI bralewild tienen. Ya vivimos en `docs/fase6_zhang_influence.md` y
`deliverables/track2` (roadmap preclínico E1: payload ARNm-BUBR1, delivery LNP multiorgánico,
reversibilidad 48h, cero genotoxicidad). **Exponerlo como candidato de resolución definitiva de dosis**
(jerarquía: NAD+/SIRT2 puente → chaperona N1002K → reemplazo mRNA-LNP → CRISPR). Esto nos distingue:
los rivales se quedan en qui��mica; nosotros cerramos con ingeniería génica.

### Acción 4 — Añadir el control de direccionalidad (prestar A SU metodología es copiar; mejor citarla)
NO copiamos control positivos iguales. En su lugar, **añadimos nuestro propio control de positivo
adicional**: mostrar que la vía NAD+/SIRT2 también admite un agente aprobado (NMN es suplemento OTC),
lo que da "auditable" sin usar sus CFTR/PAH. (Nada impide mencionar que la validación de un filtro
por controles es buena práctica estándar — sin detallar la suya.)

### Acción 5 — Reforzar el plan clínico integral (lo que ninguno tiene)
Ambos se centran en el mecanismo/fármaco. Nosotros ya integramos: vigilancia oncológica q3m,
monitorización de mielodisplasia (Laberko), régimen sarcoma estándar, GH con sign-off onco, senolíticos
under oncology, y consejo reproductivo 25%. **Hacer que esto sea la tesis de cierre del Track 2**:
"el mejor fármaco sin un plan clínico no es medicina; nosotros entregamos el plan."

### Acción 6 — Refinar la Fase 5 (toxicidad/oncogénesis) para el caso concreto
Seguir el rigor del Consorcio (our técnico): una tabla explícita de **riesgos oncogénicos de cada
candidato en contexto de sarcoma activo** (NAD+ fueling tumoral Nacarelli 2019, GH/IGF-1 oncogenic,
senolíticos antiproliferativos) con conclusiones por candidato. Esto es un entregable que ni sus repos
tienen con esa severidad pediátrica.

### Acción 7 — Un "titular" diferenciador para el panel en 1 frase
Nuestro gancho: **"Los repos de fármacos no pueden ayudarte aquí porque BubR1 es undrugged — así
que redescubrimos una vía aprobada y lista para cruzar a clínica, añadimos un respiratorio de
seguridad oncológica, y tenemos lista la llave de reemplazo génico para cuando la química no baste."**

---

## 4. Conclusión de posición competitiva

| Dimensión | tfius | bralewild | byronzunigao (nosotros) |
|---|---|---|---|
| Innovación algorítmica | ★★★★★ (GNN) | ★★★★ (directional filter) | ★★★ (mecanismo + ingeniería) |
| Rotundidad del candidato | Baja (6 opciones, ninguna con in-vivo) | Baja-Media (Escina, efecto pequeño) | **Alta (NMN/SIRT2 con in-vivo real)** |
| Cobertura de ambos alelos | Parcial | **Solo alelo nulo** | **Completa (nulo + missense + reemplazo)** |
| Plan clínico integral | No | Parcial (HPO liability) | **Sí (vigilancia+GH+repro+onco)** |
| Seguridad/tóxico en malignidad activa | Media | Media | **Alta (Fase 5 severa)** |
| Salida de reemplazo génico | No | No | **Sí (mRNA-LNP)** |

**Veredicto:** el panel que valora backup clínico y evidencia in-vivo nos favorece. El panel que
valora la innovación algorítmica favorece a tfius. Nuestro contratataque: **cerrar el debate sobre
evidencia clínica y entrega integral**, donde somos inalcanzables dentro de estas dos propuestas.

**Lema operativo:** no competimos por tener el método más impresionante; competimos por entregar la
propuesta más **activable y más segura para este niño**, con una ruta de resolución definitiva.