# Fase 6 — Verificación de los Criterios Zhang (Specificity / Efficiency / PAM) para la terapia génica BUB1B

**Fuentes:** secuencia de referencia **GRCh38/hg38** (UCSC REST API) · VCF real `data/results/vcf_exonic_variants.txt` ·
`deliverables/consorcio/VERIFICACION_MANEJO_CLINICO.md` · `docs/fase6_zhang_influence.md`.

Los **criterios de Feng Zhang** para diseños CRISPR-Cas9 terapéuticos se verifican sitio a sitio:
**(1) Especificidad** (off-target), **(2) Eficiencia** (on-target), **(3) PAM** (SpCas9 `5'-NGG-3'`).

## Verificación sitio a sitio (secuencia hg38 real)

| Sitio (VCF) | Ref vérif. hg38 | PAM NGG | Strand | Eficiencia heurística | Alelo-específico (seed/PAM) | Especificidad off-target |
|---|---|---|---|---|---|---|
| `chr15:40209701` (p.Leu737Ter) | ✅ T | ✅ `CC`→NGG (opuesto) | `-` | ALTA (gc 45-60%, sin poly-T) | ❌ fuera de seed | ⏳ PENDIENTE CRISPOR |
| `chr15:40220612` (p.Asn1002Lys) | ✅ T | ✅ `CC`→NGG (opuesto) | `-` | ALTA (gc 45-60%, sin poly-T) | ❌ fuera de seed | ⏳ PENDIENTE CRISPOR |

**Espaciadores candidatos (calidad declarada, PAM NGG):**
- gRNA-L2: `CACTTAACTCTGGTAGGGAC` (chr15:40209701)
- gRNA-N1002K: `CCTCATCATTGGCATTCAGA` (chr15:40220612)

> El puntaje de eficiencia es **heurístico preliminar** (subset de rasgos Doench/DeepCRISPR: GC 40-65%,
> ausencia de poly-T U6, homopolímeros, seed G). Debe reemplazarse por el puntaje oficial CRISPOR/Doench 2016.

## Estado por criterio

### 3) Criterio PAM — ✅ VERIFICADO
Ambos sitios tienen PAM `NGG` utilizable a distancia de corte funcional (3 nt 5' del PAM), en el strand opuesto.
Los espaciadores reclutables cubren la posición de la variante dentro del protoespaciador.

### 2) Criterio Eficiencia (on-target) — ⚠️ ESTIMADO (preliminar)
Heurística ALTA para ambos espaciadores, pero pendiente puntaje oficial (CRISPOR/IDT/DeepCRISPR).
`Eficiencia esperada` de Fase 6 (HDR ~10-30%/alelo) aplica al método, no al gRNA.

### 1) Criterio Especificidad (off-target) — ⏳ PENDIENTE (plan definido)
El barrido off-target genoma-completo (CRISPOR/CasOFFinder) requiere el índice GRCh38 (~751 MB),
no disponible en el entorno del hackathon. Plan para producción:
1. CRISPOR v4 / CasOFFinder (GRCh38) con ambos espaciadores + PAM NGG.
2. Aceptar solo gRNAs con ≤3 mismatches canónicos fuera de BUB1B.
3. **Excluir cortes en oncogenes y genes del SAC** (BUB1, MAD2L1, TTK, CDC20, …) → evita aneuploidía inducida
   (crítico dado la predisposición oncológica del MVA1, Verificación A2 y corrección #2 del Consorcio).
4. **Discriminación alélica**: la variante queda fuera del seed en la ventana natural → ninguna
   dependencia exclusiva de discriminar WT vs mutante; mitigar con:
   - **HDR con donor alélico** (plantilla = secuencia WT que repara al alelo mutado) + selección post-edición,
   - o **prime editing (PE3) / SpRY-NG** para reposicionar el PAM y acercar la edición al seed,
   - o **base editing** solo para el valor agregado de N1002K (la transversión T>G no es editable con CBE/ABE directo).

## Cobertura de la verificación clínica del Consorcio por la terapia génica

| # Consorcio | Afirmación/corrección clínica | ¿Lo cubre la propuesta de terapia génica? | Detalle |
|---|---|---|---|
| A1 | No existe terapia curativa disponible | ✅ Coherente | Fase 6 es propuesta **traslacional/preclínica** (I/II en 2-3 años); la corrección génica candidata no contradice el estado actual |
| A2 + #2 | Espectro tumoral (Wilms, RMS, **MDS**, neuroblastoma, gónadas, GI) | ⚠️ PARCIAL | Edición HSC reduce riesgo hematológico/oncogénico hematopoyético; los tumores sólidos requieren además vigilancia activa (plan clínico) y **terapia sistémica** (LNP-TfR1/AAV9 en Fase 6) |
| #1 | Confirmación citogenética del mosaico (PCS/FISH) | ✅ Cubierto | Fase 6 `calibrated by mosaicism (FISH/karyotype required)` para dosis y go/no-go |
| #3 | Vigilancia hematológica (citopenias/MDS) | ✅ Cubierto | Monitor de eficacia post-HSC editadas (hemograma + quimerismo) y de seguridad del ensayo |
| #4 | Vigilancia oftalmológica | ⚠️ PARCIAL | Solo como monitor de seguridad del ensayo; el manejo base oftalmológico sigue siendo del plan clínico |
| #5 | Quistes/malformaciones renales | ⚠️ PARCIAL | La edición sistémica preserva función renal a futuro; la nefrocalcinosis ya establecida no es reversible → manejo nefrológico paralelo |
| #6 | Malformaciones SNC (Dandy-Walker, cuerpo calloso) | ⚠️ PARCIAL | Objetivo LNP-TfR1 (cerebro) contempla SNC; defectos estructurales no son corregibles → RMN + neurodesarrollo del plan clínico |
| #7 | Inicio de vigilancia al diagnóstico | ✅ Cubierto | La ventana pediátrica (E7 en `fase6_elegibilidad.json`) y el diseño gRNA no dependen de la edad → aplicable desde el diagnóstico |
| A5 | GH individualizada | ⚠️ Independiente | La edición génica no reemplaza el manejo endocrino; se mantiene individualización según respuesta |

## Conclusión

La propuesta de terapia génica de Fase 6 **cumple el criterio PAM (verificado en secuencia hg38 real),**
estima **eficiencia on-target alta preliminar** y **deja el criterio de especificidad off-target como pendiente
de orquestación (CRISPOR/CasOFFinder)** — sin el cual no debe avanzar a la etapa clínica. El diseño actual incorpora
las salvaguardas dictadas por la verificación del Consorcio: requerir FISH/cariotipo (mosaico) para dosis, no
editar oncogenes genes SAC y vigilar el espectro tumoral ampliado durante el ensayo.

*Módulo Fase 6 — anclado a la secuencia de referencia hg38 descargada (UCSC) y a los resultados verificados del pipeline.*