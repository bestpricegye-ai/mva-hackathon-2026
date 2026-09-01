# FASE 6 — Zhang_Influence: Terapia Génica Programable para MVA1
## Biología de síntesis + ingeniería genética programable para corregir BUB1B

**Enfermedad objetivo:** Mosaic Variegated Anueploidy Syndrome 1 (MVA1, OMIM #257300)
**Gen causal:** BUB1B (BubR1, HGNC:1149, chr15:40.2 Mb, GRCh38)
**Genotipo paciente:** compound-heterocigoto BUB1B
  - Alele 1: chr15:40209701 T>G → c.2210T>G p.(Leu737Ter) — stop_gained (LoF)
  - Alele 2: chr15:40220612 T>G → c.3006T>G p.(Asn1002Lys) — missense (AlphaMissense 0.923)
**Herencia:** Autosomal recesivo
**Fenotipo:** Disregulación mitótica (aneuploidía variegada, predisposición a cáncer, retraso del crecimiento, alteraciones renales y perinatales)

---

## 1. Aplicación de los 4 métodos de Zhang_Influence a MVA1

### 1.1 Edición Génica de Precisión CRISPR-Cas9 (corrección definitiva)

**Objetivo:** Corregir ambos alelos BUB1B en células del paciente para restaurar la función completa de BubR1.

**Estrategia propuesta — corrección de exones:**

| Alele | Variante | Estrategia CRISPR-Cas9 |
|---|---|---|
| **Leu737Ter** (T>G chr15:40209701) | stop_gained en c.2210 | Corrección por HDR con plantilla sintética que restaure T>G → T (o ablación del sitio de corte para eliminar el stop premature) |
| **Asn1002Lys** (T>G chr15:40220612) | missense en quinasa C-term | Corrección por HDR: restablecer T>G → T para recuperar Asn1002, o edición base (adenina base editor) para convertir el Lys en Asn |

**Diseño de guías RNA (prototipo):**
- **gRNA-L737Ter:** dirigida a chr15:40209701 (±20 nt flanqueo), PAM NGG → corta a ~3 bp del error
- **gRNA-N1002K:** dirigida a chr15:40220612 (±20 nt), PAM NGG → corta cerca del codón 1002

**Vectores de reparación (donor):**
- Plantillas ssDNA con secuencia corregida + homologías laterales (500–800 bp)
- Para N1002K: ABE (adenine base editor) → A→G en el ADN complementario para revertir el Lys a Asn sin doble cadena

**Modelo celular de validación:**
- Fibroblastos del paciente (biopsia cutánea) → reprogramación a iPSC → diferenciación a progenitores hematopoyéticos
- Correción ex vivo + trasplante autólogo de células madre hematopoyéticas (HSC) corregidas

**Viabilidad:** ALTA — MVA1 es monogénico, las mutaciones son puntuales (ideales para HDR/ABE), y el fenotipo requiere restauración de función (no supresión, por lo que la corrección es beneficiosa y no oncogénica).

**Limitación:** BUB1B es grande (~30 exones). La corrección de ambos aleles requiere doble golpe en el mismo locus, lo que reduce eficiencia de HDR. Estrategia alternativa: **corrección alélica individual con donor específico por mutación**.

---

### 1.2 Edición Transitoria de ARN con CRISPR-Cas13 (puente terapéutico)

**Objetivo:** Corregir transitoriamente el ARNm mutado de BUB1B para restaurar temporalmente la proteína BubR1 funcional, mientras se desarrolla la terapia génica permanente.

**Mecanismo:**
- **Cas13** (dirigida a ARN, no ADN) + gRNA específica del transcrito mutado
- Modificación temporal de la traducción:
  - Para el transcrito p.Leu737Ter: Cas13 puede dirigirse al ARNm mutado y degradarlo selectivamente (RNA editing / RNA knockdown del alelo mutado) + expresión del alelo salvaje restante (si hay nivel residual)
  - Alternativa: **RNA base editing (ADAR)** → conversión temporal del codón mutado

**Ventaja médica para MVA1:**
- MVA1 requiere función BUB1B en células **dividiéndose** (mielopoiesis, embriogénesis). Una corrección transitoria en progenitores hematopoyéticos podría ser suficiente para un episodio terapéutico.
- **Sin alteración permanente del genoma** → seguridad en pacientes jóvenes (riesgo oncológico reducido).
- Ideal para pacientes que no son candidatos inmediatos a edición génica de ADN.

**Limitación:** Efecto transitorio (semafora 2–4 semanas) → requiere re-dosis o combinación con terapia génica permanente.

---

### 1.3 Cribado Genómico CRISPR (identificación de dianas y resistencia)

**Objetivo:** Descubrir modificadores genéticos y rutas compensatorias que mitiguen el fenotipo de pérdida de BUB1B.

**Pantallas propuestas:**

| Pantalla | Propósito | Modelo |
|---|---|---|
| **Knockout screen** (ko-CRISPR) | Identificar genes cuya pérdida compensa la deficiencia de BubR1 (supresores sintéticos) | iPSC del paciente → diferenciación a progenitores con BUB1B KO |
| **CRISPR activation (CRISPRa)** | Sobre-expresores que restauren el checkpoint mitótico | Línea celular con BUB1B bajo expresión inducible |
| **Screen de sensibilidad a aneuploidía** | Identificar genes que agravan o suprimen la aneuploidía en ausencia de BUB1B | Líneas con BUB1B haploinsuficiente |

**Candidatos a identificar (hipótesis basada en la red del checkpoint):**
- **BUB1** (paralogo): sobre-expresión podría compensar parcialmente la pérdida de BUB1B
- **MAD2L1 / MAD1L1** (clientes directos de BubR1): amplificación podría estabilizar el complejo mitótico
- **TTK (Mps1)** / **AURKB** / **PLK1**: kinases del checkpoint que podrían modular la severidad del fenotipo
- Genes de la vía de **respuesta al daño del ADN (DDR)** que convergen con el checkpoint

**Resultado esperado:** Identificar un "cocktail genético" de modificadores que reduzcan la severidad del fenotipo MVA1, permitiendo (a) una estratificación de riesgo más precisa y (b) nuevas dianas farmacológicas.

---

### 1.4 Plataforma SEND (Entrega Segura de Terapia Génica)

**Objetivo:** Empaquetar los componentes CRISPR-Cas9 o Cas13 para entrega segura y re-administrable en pacientes con MVA1.

**Aplicación a MVA1:**
- **Proteína PEG10** (humana, natural) → empaqueta mRNA de Cas9 + gRNA en partículas similares a virus (VLPs)
- **Ventaja para MVA1:**
  - BUB1B se expresa en células madre hematopoyéticas (HSC) y progenitoras → entrega in vivo a médula ósea
  - PEG10 evita inmunogenicidad → re-dosis posible (importante para pacientes pediátricos)
  - Componentes propios del cuerpo → menor rechazo inmune vs. AAV/LNP convencionales

**Estrategia de entrega:**
1. **Ex vivo:** Edición de HSC del paciente con Cas9 + gRNAs + donor HDR → trasplante autólogo (más control, menor riesgo inmunológico)
2. **In vivo (posterior):** VLP-SEND con Cas9/gRNA dirigidos a HSC → corrección directa en la médula ósea (sin extracción celular)

**Estado de la plataforma SEND:** Pre-clínico (publicado por Zhang Lab, 2023–2024). Aplicable a trastornos hematopoyéticos monogénicos como MVA1.

---

## 2. Propuesta terapéutica integrada para MVA1 (ruta de Fase 6)

**Estrategia escalonada ("hit-and-run" + corrección permanente):**

```
FASE 6A — Puente terapéutico (baja complejidad)
  └─ CRISPR-Cas13 (transitorio) → corrección de ARNm BUB1B en progenitores hematopoyéticos
     → restauración temporal de BubR1 funcional → reducción de aneuploidía

FASE 6B — Corrección génica definitiva (complejidad alta)
  └─ CRISPR-Cas9 / ABE + plataforma SEND
     → Edición ex vivo de HSC (corrección HDR de ambos alelos BUB1B)
     → Trasplante autólogo de HSC corregidas
     → Restauración permanente de la función BUB1B en la hematopoyesis

FASE 6C — Optimización de resistencia y seguridad
  └─ CRISPR Screening → identificación de modificadores y dianas de resistencia
     → Validación in vitro e in vivo (modelos de xenoinjerto)
```

---

## 3. Análisis de factibilidad

| Criterio | CRISPR-Cas9 (definitiva) | CRISPR-Cas13 (puente) | SEND | Screening |
|---|---|---|---|---|
| **Complejidad técnica** | Alta | Media | Alta | Media |
| **Eficiencia esperada** | Moderada (HDR ~10–30%) | Alta (knockdown >80%) | Media (pre-clínico) | Alta |
| **Seguridad** | Media (edición permanente) | Alta (transitorio) | Alta (componente humano) | Alta |
| **Reversibilidad** | No (permanente) | Sí (transitorio) | No (si es integración) | N/A |
| **Re-administración** | No | Sí | Sí | N/A |
| **Alineación con fenotipo MVA1** | ✅ (restaura BUB1B) | ✅ (restaura BubR1 transitoriamente) | ✅ (entrega segura) | ✅ (descubre mod.) |
| **Listo para traslación clínica** | Ensayos Fase I/II (2–3 años) | Pre-clínico (1–2 años) | Pre-clínico (2–3 años) | Investigación (1–2 años) |

**Conclusión:** MVA1 es una diana **excelente** para Zhang_Influence. BUB1B es un gen mono-génico, puntual, de mecanismo claro (checkpoint mitótico), y la corrección génica (restaurar función, no silenciar) es beneficiosa y no oncogénica. La terapia más prometedora es **CRISPR-Cas9/ABE + SEND** con corrección ex vivo de HSC.

---

## 4. Próximos pasos para Fase 6

1. Diseñar gRNAs específicas para cada alelo BUB1B (en silico)
2. Validar en células del paciente (fibroblastos → iPSC → progenitores)
3. Evaluar eficiencia de HDR/ABE para cada alele
4. Construir constructo SEND (peg10-mCherry reporter)
5. Screening CRISPR de modificadores del checkpoint BUB1B
6. Escribir `docs/fase6_zhang_influence.md` con propuesta completa

**Salida:** `data/results/fase6_zhang_influence.json` (análisis de factibilidad) + `docs/fase6_zhang_influence.md` (propuesta terapéutica completa)