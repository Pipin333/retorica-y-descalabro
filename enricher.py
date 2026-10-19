"""
Diccionario léxico y transformador heurístico de enriquecimiento barroco / rimbombante.
Permite enriquecer frases cotidianas a un registro ultra-académico y barroco.
"""
from typing import Dict, List, Tuple
import re

# Reglas de sustitución contextual por frases o modismos completos
PHRASE_RULES: List[Tuple[str, str]] = [
    (r"\bsigue tu camino\b", "continúa con tu sendero"),
    (r"\bsiga su camino\b", "continúe con su sendero"),
    (r"\bque sin ti me va mejor\b", "porque en tu ausencia la calidad de mi vida ha aumentado"),
    (r"\bsin ti me va mejor\b", "en tu ausencia la calidad de mi vida ha aumentado"),
    (r"\bme va mejor\b", "mi bienestar holístico experimenta una cúspide notable"),
    (r"\bme lo hacen mejor\b", "copulan más satisfactoriamente con mi persona"),
    (r"\bahora tengo otras\b", "actualmente poseo a otras entidades femeninas"),
    (r"\btengo otras\b", "poseo a otras entidades femeninas"),
    (r"\blo hacen mejor\b", "ejecutan el acto carnal con mayor satisfacción"),
    (r"\bla paso bien\b", "disfruto de un deleite dionisíaco inconmensurable"),
    (r"\bno me importa\b", "resulta totalmente irrelevante para mis facultades cognitivas"),
    (r"\bte quiero\b", "profeso por tu individuo un afecto químicamente desmesurado"),
    (r"\bte amo\b", "albergo una vehemente devoción epistémica y visceral hacia tu ser"),
    (r"\bno tengo plata\b", "adolezco de solvencia y liquidez monetaria en mis arcas"),
    (r"\bestoy cansado\b", "mi fisiología se encuentra en un estado de letargo y fatiga extrema"),
    (r"\btengo hambre\b", "mi sistema digestivo emite señales ostensibles de inanición calórica"),
    (r"\bvamos de fiesta\b", "procedamos a congregarnos en un festín de jolgorio y regocijo"),
    (r"\bme rompiste el corazón\b", "provocaste una disrupción traumática en mi ventrículo emocional"),
    (r"\bme engañaste\b", "incurriste en una vileza de deslealtad y perfidia sentimental"),
    (r"\bno te creo nada\b", "concedo nulo valor de verosimilitud a tus enunciados"),
    (r"\bcallate\b", "abstente de emitir perturbaciones acústicas articuladas"),
    (r"\bcállate\b", "abstente de emitir perturbaciones acústicas articuladas"),
]

# Sustitución de palabras individuales por sus análogos barrocos/académicos
WORD_MAP: Dict[str, str] = {
    "hola": "salutaciones cordiales",
    "chau": "hasta el próximo solsticio",
    "adios": "hasta que el hado vuelva a converger",
    "adiós": "hasta que el hado vuelva a converger",
    "amigo": "fraterno camarada",
    "amiga": "fraterna camarada",
    "casa": "residencia habitacional",
    "auto": "vehículo autopropulsado",
    "coche": "carruaje de combustión",
    "trabajo": "labor prolectaria indispensable",
    "dormir": "sucumbir a los brazos de Morfeo",
    "comer": "ingerir sustento biológico",
    "dinero": "recursos fiduciarios",
    "plata": "recursos fiduciarios",
    "mujer": "entidad femenina",
    "mujeres": "entidades femeninas",
    "hombre": "espécimen masculino",
    "hombres": "especímenes masculinos",
    "persona": "ente biopsicosocial",
    "gente": "colectividad de conciencias",
    "cuerpo": "anatomía somática",
    "ojos": "órganos fotorreceptores",
    "boca": "cavidad bucal oratoria",
    "beso": "ósculo conmovedor",
    "besos": "ósculos conmovedores",
    "noche": "período nocturno y umbrío",
    "día": "intervalo heliocéntrico diurno",
    "dia": "intervalo heliocéntrico diurno",
    "cama": "lecho voluptuoso de reposo",
    "playa": "litoral marítimo arenoso",
    "mar": "masa acuífera oceánica",
    "tiempo": "continuo espacio-temporal",
    "vida": "existencia orgánica consciente",
    "muerte": "cese definitivo de las constantes biológicas",
    "feliz": "imbuido en una dicha platónica",
    "triste": "sumido en un pozo de melancolía inconsolable",
    "loco": "desprovisto de coherencia heurística",
    "loca": "desprovista de coherencia heurística",
    "lindo": "dotado de una estética armoniosa y excelsa",
    "linda": "dotada de una estética armoniosa y excelsa",
    "feo": "carente de proporción áurea tangible",
    "fea": "carente de proporción áurea tangible",
    "malo": "nocivo y pernicioso",
    "bueno": "benéfico y laudable",
    "grande": "monumental y ciclópeo",
    "chico": "diminuto y microscópico",
    "rápido": "con una celeridad vertiginosa",
    "despacio": "con una lentitud solemne y pausada",
    "fiesta": "jolgorio bacanal",
    "música": "composición armónica sonora",
    "canción": "oda melódica contemporánea",
    "amor": "afecto neuroquímico sublime",
    "problema": "dilema ontológico inextricable",
    "verdad": "certeza epistemológica irrefutable",
    "mentira": "falacia retórica artificiosa",
}

# Prefijos y sufijos ornamentales para dar textura solemne
ORNAMENTS_START = [
    "Haciendo un exhaustivo análisis hermenéutico, procede manifestar que: ",
    "A la luz de los postulados ético-filosóficos imperantes, se colige que: ",
    "Conviene aseverar con meridiana lucidez que: ",
    "Resulta palmario e incontrovertible colegir que: ",
]

def enrich_text_heuristic(text: str, formality_level: int = 2) -> str:
    """
    Enriquece un texto aplicando reglas fonético-léxicas y frases académicas/barrocas.
    
    Args:
        text: Texto original en español.
        formality_level: Nivel de 1 a 3 (1: Formal, 2: Ultra-académico, 3: Rococó / Rimbombante).
        
    Returns:
        Texto enriquecido con retórica rimbombante.
    """
    if not text or not text.strip():
        return ""

    processed = text.strip()

    # 1. Aplicar reglas de frases complejas (case insensitive)
    for pattern, replacement in PHRASE_RULES:
        processed = re.sub(pattern, replacement, processed, flags=re.IGNORECASE)

    # 2. Aplicar mapeo de palabras
    words = processed.split(" ")
    enriched_words = []
    for word in words:
        clean_word = re.sub(r"[^\wáéíóúüñÁÉÍÓÚÜÑ]", "", word).lower()
        punctuation_before = ""
        punctuation_after = ""
        m_start = re.match(r"^[^\wáéíóúüñÁÉÍÓÚÜÑ]+", word)
        m_end = re.search(r"[^\wáéíóúüñÁÉÍÓÚÜÑ]+$", word)
        if m_start:
            punctuation_before = m_start.group(0)
        if m_end:
            punctuation_after = m_end.group(0)

        if clean_word in WORD_MAP:
            replacement = WORD_MAP[clean_word]
            # Preservar mayúscula inicial si la tenía
            if word and word[0].isupper():
                replacement = replacement.capitalize()
            enriched_words.append(f"{punctuation_before}{replacement}{punctuation_after}")
        else:
            enriched_words.append(word)

    enriched = " ".join(enriched_words)

    # 3. Nivel de formalidad: añadir preludio ornamental si es nivel 3
    if formality_level >= 3:
        prefix = ORNAMENTS_START[len(text) % len(ORNAMENTS_START)]
        enriched = f"{prefix}{enriched} Por ende, la premisa queda fáctica e irrebatiblemente sentada."

    return enriched
