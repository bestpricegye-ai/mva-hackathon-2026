# FASE 6 - Zhang_Influence: analisis de aplicabilidad terapeutica
# Evalua los 4 metodos de Zhang_Influence para la enfermedad MVA1 (BUB1B compound-het).
# Salida: data/results/fase6_zhang_influence.json
import json, os

DISEASE = {
    "nombre": "Mosaic Variegated Anueploidy Syndrome 1 (MVA1)",
    "omim": "OMIM #257300",
    "gen": "BUB1B (BubR1, HGNC:1149)",
    "cromosoma": "chr15:40.2 Mb (GRCh38)",
    "herencia": "Autosomal recesivo",
    "fenotipo": "Disregulacion mitotica (aneuploidia variegada, predisposicion a cancer, "
               "retraso del crecimiento, alteraciones renales y perinatales)",
}

VARIANTES = [
    {"pos": "chr15:40209701", "ref": "T", "alt": "G", "hgvs": "c.2210T>G",
     "prot": "p.(Leu737Ter)", "consequence": "stop_gained", "impact": "HIGH",
     "genotipo": "Alele 1", "gnomad": "absente", "clinvar": "Pathogenic (RCV000641226)"},
    {"pos": "chr15:40220612", "ref": "T", "alt": "G", "hgvs": "c.3006T>G",
     "prot": "p.(Asn1002Lys)", "consequence": "missense_variant", "impact": "MODERATE",
     "genotipo": "Alele 2", "gnomad": "absente", "clinvar": "novel",
     "alphamissense": 0.9229},
]

# Evaluacion de cada metodo Zhang_Influence para MVA1
METODOS = {
    "crispr_cas9": {
        "nombre": "Edicion Genetica de Precisión (CRISPR-Cas9)",
        "aplicable": True,
        "justificacion": "MVA1 es monogenica con mutaciones puntuales (ideales para HDR/ABE). "
                         "La correccion restaura funcion (no silencia), por lo que NO es oncogenica.",
        "objetivo": "Corregir ambos alelos BUB1B via HDR con donor sintetico o ABE (A->G para revertir N1002K).",
        "gRNAs": ["chr15:40209701 (±20 nt, PAM NGG)", "chr15:40220612 (±20 nt, PAM NGG)"],
        "estrategia": "Correccion ex vivo de HSC del paciente + trasplante autologo.",
        "complejidad": "Alta", "eficiencia_esperada": "HDR ~10-30% por alele",
        "seguridad": "Media (edicion permanente)", "reversibilidad": "No",
        "listo_clinica": "Ensayos Fase I/II (2-3 anos)",
    },
    "crispr_cas13": {
        "nombre": "Edicion Transitoria de ARN (CRISPR-Cas13)",
        "aplicable": True,
        "justificacion": "Puente terapeutico: corrige el ARNm mutado sin alterar el genoma. "
                         "Ideal para pacientes jovenes o como puente a terapia definitiva.",
        "objetivo": "Degradacion selectiva del ARNm mutado p.Leu737Ter o edicion ADAR transitoria.",
        "gRNAs": ["gRNA anti-mRNA Leu737Ter", "gRNA anti-mRNA Asn1002Lys"],
        "estrategia": "VLP-SEND con Cas13 + gRNA -> correccion transitoria en progenitores hematopoyeticos.",
        "complejidad": "Media", "eficiencia_esperada": "knockdown >80% (transitorio 2-4 semanas)",
        "seguridad": "Alta (transitorio)", "reversibilidad": "Si",
        "listo_clinica": "Pre-clinico (1-2 anos)",
    },
    "crispr_screening": {
        "nombre": "Cribado Genomico CRISPR (CRISPR Screening)",
        "aplicable": True,
        "justificacion": "MVA1 es poco comun; screening identifica modificadores del fenotipo y nuevas dianas.",
        "objetivo": "Identificar supresores sinteticos y rutas compensatorias de la perdida de BUB1B.",
        "pantallas": ["knockout screen (supresores)", "CRISPRa (sobre-expresion)", "sensibilidad aneuploidia"],
        "candidatos": ["BUB1 (paralogo)", "MAD2L1/MAD1L1 (clientes directos)", "TTK, AURKB, PLK1",
                       "genes DDR (convergencia con checkpoint)"],
        "complejidad": "Media", "eficiencia_esperada": "Alta",
        "seguridad": "Alta", "reversibilidad": "N/A",
        "listo_clinica": "Investigacion (1-2 anos)",
    },
    "send": {
        "nombre": "Nuevos Sistemas de Entrega Molecular (Plataforma SEND)",
        "aplicable": True,
        "justificacion": "PEG10 humano empaqueta CRISPR en VLPs sin inmunogenicidad; re-dosis segura.",
        "objetivo": "Entregar Cas9/gRNA/donor a HSC del paciente para correccion in vivo o ex vivo.",
        "componentes": ["mRNA Cas9", "gRNA BUB1B", "donor HDR", "peg10-VLP"],
        "ventaja": "Componentes propios del cuerpo -> menor rechazo -> re-administracion posible (pacientes pediatricos).",
        "complejidad": "Alta", "eficiencia_esperada": "Pre-clinico",
        "seguridad": "Alta (natural PEG10)", "reversibilidad": "Si (si no integra)",
        "listo_clinica": "Pre-clinico (2-3 anos)",
    },
}

PROPUESTA_TERAPEUTICA = {
    "enfermedad": DISEASE["nombre"],
    "gen_causal": DISEASE["gen"],
    "variantes": VARIANTES,
    "estrategia_escalonada": [
        {
            "fase": "6A - Puente terapeutico",
            "metodo": "CRISPR-Cas13 (transitorio)",
            "descripcion": "Correccion del ARNm mutado BUB1B en progenitores hematopoyeticos -> "
                           "restauracion temporal de BubR1 funcional -> reducion de aneuploidia.",
            "complejidad": "Baja", "tiempo_estimado": "1-2 anos",
        },
        {
            "fase": "6B - Correccion genesica definitiva",
            "metodo": "CRISPR-Cas9/ABE + plataforma SEND",
            "descripcion": "Edicion ex vivo de HSC (HDR de ambos alelos BUB1B) + trasplante autologo -> "
                           "restauracion permanente de la funcion BUB1B en hematopoyesis.",
            "complejidad": "Alta", "tiempo_estimado": "2-3 anos",
        },
        {
            "fase": "6C - Optimizacion de seguridad",
            "metodo": "CRISPR Screening",
            "descripcion": "Identificacion de modificadores geneticos y dianas de resistencia para "
                           "optimizar la terapia y estratificar riesgo.",
            "complejidad": "Media", "tiempo_estimado": "1-2 anos",
        },
    ],
    "conclusion": "MVA1 es una diana excelente para Zhang_Influence. BUB1B es un gen monogenico, "
                  "puntual, con mecanismo claro (checkpoint mitotico). La correcion genica (restaurar "
                  "funcion, no silenciar) es beneficiosa y NO oncogenica. La terapia mas prometedora es "
                  "CRISPR-Cas9/ABE + SEND con correccion ex vivo de HSC.",
}

def main():
    out = {
        "enfermedad": DISEASE,
        "variantes_candidatas": VARIANTES,
        "metodos_analizados": METODOS,
        "propuesta_terapeutica": PROPUESTA_TERAPEUTICA,
    }
    os.makedirs("data/results", exist_ok=True)
    with open("data/results/fase6_zhang_influence.json", "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print(json.dumps(out, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()