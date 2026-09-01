# Registro de Decisión — Reads FASTQ/BAM no analizables en el proyecto

**Fecha:** 2026-09-01
**Participante:** byronzunigao
**Estado:** Decisión tomada — sin análisis a nivel de reads
**Relacionado:** `docs/verificacion_dirigida_vcf.md` (verificación dirigida desde VCF)

## Contexto

El dataset del challenge incluye reads crudos (FASTQ/BAM, ~85 GB). En la fase de
adquisición de datos solo se descargaron el VCF (`WGS_EX2312012_HGWCNDSX7.vcf.gz`,
315 MB) y su índice `.tbi`; los reads quedaron fuera por tamaño (desviación
documentada del plan de datos).

Se evaluó la alternativa de procesar los reads **sin descargarlos al disco local**,
usando cómputo en la nube (AWS / Hugging Face).

## Evaluación técnica

### AWS (cuenta del proyecto, profile `hackathon`, región `us-east-1`)

Pruebas directas con la CLI (2026-09-01):

| Servicio | Resultado |
|---|---|
| `freetier get-account-plan-state` | `ResourceNotFoundException` (sin datos de plan) |
| S3 `list-buckets` | `NotSignedUp` — el servicio no está habilitado |
| EC2 `describe-regions` | `OptInRequired` — sin suscripción al servicio |
| AWS Batch `describe-job-queues` | `SubscriptionRequiredException` |
| Amazon Omics `list-workflows` | `SubscriptionRequiredException` |
| ECR `describe-repositories` | OK (repositorio vacío) — sin cómputo asociado |

**Conclusión:** la cuenta del proyecto (nueva experiencia AWS) no tiene habilitados
S3 ni cómputo (EC2/Batch/Omics). ECR solo no habilita pipelines. La única vía sería
activar servicios avanzados (AWS Settings), con costo estimado de US$10-30 solo en
transferencia (85 GB inbound) + cómputo de alineamiento/llamado, sujeto a las
políticas de control del proyecto (SCP/RCP) y al spend limit.

### Hugging Face

Hugging Face no es una plataforma de cómputo genómico: los Spaces no están
diseñados para depósitos WGS de ~85 GB ni para pipelines bwa/GATK/manifold/mosdepth.
Hub solo aloja datos/modelos; subir 85 GB no habilita procesamiento. **Descartada.**

## Valor esperado vs. riesgo

- Información adicional obtenible solo desde reads: llamada de SV/CNV y cuantificación
  de aneuploidía en mosaico (fenotipo MVA), verificación a nivel de read (strand bias,
  artefactos de mapeo), variantes de baja VAF.
- El diagnóstico ya está confirmado por el VCF (BUB1B compound-het,
  `chr15:40209701 T>G` + `chr15:40220612 T>G`, ambas GT=0/1 PASS, VAF balanceada
  ~0.46-0.54), sin variantes adicionales deletéreas en el locus (16 variantes
  regionales, ver `docs/verificacion_dirigida_vcf.md`).
- Riesgo: costo + tiempo sin impacto en el diagnóstico ni en el scoring del Track 1.

## Decisión

**NO se procesan los reads.** El pipeline completo se sustenta en el VCF real
(5,012,204 variantes), con fases 1-6 cerradas y reproducibles (scripts parametrizados
en `src/config.py`). La cuantificación de aneuploidía en mosaico queda documentada
como trabajo futuro (requiere el BAM y cómputo dedicado).

## Alternativa futura

Si se requiere análisis de reads: (1) activar servicios avanzados en AWS Settings,
(2) solicitar al staff del challenge un bucket público del dataset o re-descargar a
disco local, (3) correr alineación + llamada de SV/CNV (MANTA, cnvkit, MosaicForecast)
en instancia efímera, descartándola al finalizar.