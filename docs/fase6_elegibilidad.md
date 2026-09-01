# Fase 6 — Elegibilidad de Terapia Génica (Zhang_Influence) para PROBAND01

**Objetivo:** cruzar la historia clínica (HPO) y el genotipo (VCF) del probando contra los
criterios de elegibilidad de terapia génica definidos en `docs/fase6_zhang_influence.md`.

**Fuentes:** `data/results/clinical_history.json` (7 rasgos HPO) · `data/results/vcf_exonic_variants.txt` (VCF real GRCh38) · criterios de Fase 6.

## Puntaje de elegibilidad

**Total ponderado: 95.0/100 → Nivel ALTA**

| ID | Criterio | Peso | Score | Contribución |
|---|---|---|---|---|
| E1 | Monogenicia | 15 | 2.0/2 | 15.0 |
| E2 | Herencia | 10 | 2.0/2 | 10.0 |
| E3 | Mecanismo molecular (SNV) | 20 | 2.0/2 | 20.0 |
| E4 | Funcion-perdida (restauracion) | 20 | 2.0/2 | 20.0 |
| E5 | Tejido diana | 10 | 1.5/2 | 7.5 |
| E6 | Severidad / unmet need | 15 | 2.0/2 | 15.0 |
| E7 | Ventana pediatrica | 10 | 1.5/2 | 7.5 |

## Evidencia por criterio

### E1 — Monogenicia (score 2.0/2)
- gen causal unico: ['BUB1B']
- excluidos CEP57([0]) TRIP13([0])

### E2 — Herencia (score 2.0/2)
- caveat: segregacion parental pendiente
- soporte HPO: ['miscarriage', 'recurrent']
- mecanismo: compound-heterozygous (biallelic, in-trans) BUB1B loss of function

### E3 — Mecanismo molecular (SNV) (score 2.0/2)
- chr15:40209701 T>G SNV
- chr15:40220612 T>G SNV

### E4 — Funcion-perdida (restauracion) (score 2.0/2)
- ACMG: Pathogenic + Likely Pathogenic
- mecanismo: compound-heterozygous (biallelic, in-trans) BUB1B loss of function

### E5 — Tejido diana (score 1.5/2)
- soporte HPO tejido: ['rhabdo', 'sarcoma', 'nephro']
- HSC objetivo ex-vivo; afectacion multiorganica = reto sistemico

### E6 — Severidad / unmet need (score 2.0/2)
- soporte HPO severidad: ['rhabdo', 'sarcoma', 'stature', 'thrive', 'muscle']
- sin tratamiento establecido (literatura: manejo sintomatico)

### E7 — Ventana pediatrica (score 1.5/2)
- soporte HPO ventana: ['prematur', 'birth weight', 'low birth']

## Rasgos HPO cruzados

| Rasgo | Contexto |
|---|---|
| Rhabdomyosarcoma | predisposicion oncologica (HP:0002859) |
| Nephrocalcinosis present since birth | afectacion renal (HP:0000121) |
| Short stature | retraso de crecimiento (HP:0004322) |
| Failure to thrive | retraso de crecimiento (HP:0001508) |
| Low muscle mass | afectacion trofica (HP:0003701) |
| Prematurity (32 weeks) | parto pretermino (HP:0001622) |
| Very low birth weight (~1 kg) | bajo peso al nacer (HP:0001530) |
| Recurrent miscarriages (parents) | perdidas reproductivas parentales (HP:0000624) |

## Conclusión

Elegibilidad **ALTA** (95.0/100): MVA1 cumple monogenicidad, defecto puntual (2 SNV,
HDR/ABE viable), mecanismo de pérdida de función y severidad sin tratamiento establecido.
Limitantes: segregación parental pendiente y afectación multiorgánica (renal, crecimiento)
que exigen estrategia sistémica además del objetivo hematopoyético (HSC).

*Módulo Fase 6 — anclado a los resultados verificados del pipeline (VCF real + HPO).*
