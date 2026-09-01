# RESUMEN DE PRESENTACIÓN — MVA CLINICAL PHENOTYPE

**Título:** *Biallelic BUB1B compound heterozygosity (c.2210T>G p.Leu737Ter / c.3006T>G p.Asn1002Lys) causes Mosaic Variegated Aneuploidy Syndrome 1 with rhabdomyosarcoma risk*

**TL;DR:** El probando es portador de dos mutaciones recesivas en el gen **BUB1B** que juntas causan **MVA1 (OMIM 257300)**: una variante truncante (stop-gained, asociada formalmente a MVA1 en ClinVar) y una missense novel en el dominio C-terminal, cada una en un alelo distinto (heterocigosis compuesta).

---

## 1. Antecedentes
- Mosaic Variegated Aneuploidy (MVA) syndrome: aneuploidía cromosómica mosaica debida a falla del *spindle assembly checkpoint*.
- Causa genética principal: mutaciones **bialélicas en BUB1B** (MVA1, ~75% riesgo de cáncer, sobre todo sarcomas).

## 2. Caso (fenotipo clínico)
- Rabdomiosarcoma (cáncer), talla baja, fallo de medrar, nefrocalcinosis, atrofia muscular, parto prematuro (32 sem), bajo peso (1 kg).
- Antecedente familiar: abortos recurrentes.

## 3. Método
- VCF de genoma completo (GRCh38) filtrado a exones de genes MVA (BUB1B, CEP57, TRIP13) + panel ampliado de 24 genes SAC.
- Anotación con Ensembl VEP; validación en ClinVar/gnomAD/ExAC.
- Priorizados variantes raras/LoF con genotipo bialélico.

## 4. Resultados
- **CEP57 y TRIP13: sin variantes exónicas → descartados.**
- **Panel SAC: 72 variantes, todas polimórficas benignas → sin co-causales.**
- **BUB1B: 2 variantes exónicas patogénicas en trans:**
  1. `c.2210T>G, p.(Leu737Ter)` — **stop_gained** (truncante). ExAC 0.01%. **ClinVar RCV000641226: asociada a MVA1.**
  2. `c.3006T>G, p.(Asn1002Lys)` — **missense** novel en el exón terminal.
- **Diagnóstico: MVA1 por compuesto heterocigoto (bialélico) en BUB1B.**

## 5. Correlación clínica
- El riesgo de rabdomiosarcoma y el espectro MVA completo son consistentes con el genotipo BUB1B.
- Los abortos recurrentes parentales son compatibles con el estado portador de variantes BUB1B severas.

## 6. Clasificación ACMG
- p.Leu737Ter: **Pathogenic** (PVS1+PM2+PM3)
- p.Asn1002Lys: **Likely Pathogenic** (PM2+PM3, PM1 probable)
- Estado final: **Patogénico (compuesto heterocigoto)**

## 7. Recomendaciones / Próximos pasos
- **Vigilancia oncológica cada 3 meses** + consejo genético familiar.
- **Investigación terapéutica:** rescue *read-through* (ataluren) de la variante nonsense; refuerzo de sirtuinas/NAD+; evaluación del mosaicismo por cariotipo+PCS.

---

**Figuras aportadas (archivos):** `clinvar_rcv000641226.png` (opcional), `vcf_exonic_variants.txt`, `vcf_sac_panel_variants.txt`, `diagnostico_mva.md`, `PROPUESTA_TERAPEUTICA.md`.

**× Nota:** Todos los archivos de análisis están en `C:\starquake\hackathonmva\`. Datos con restricciones priva-cíclicas (CC-BY 4.0, borrar tras evento, no reidentificar).
