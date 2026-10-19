"""
Módulo de Distorsión Acústica y Fonética ("Mondegreen" / Homófonos / Slang).
Simula la ininteligibilidad del oído humano y la jerga urbana antes y durante el
proceso de traducción, permitiendo generar derivaciones como:
- "Rudeboyz" -> "Mujer"
- "Me has vuelto un mare" -> "Él me trajo un burro y una madre"
- "Creo que la matan mis besos" -> "Esperé antes de que me mataran"
- "Pongo dulce el mar" -> "Quiero lavar"
- "Pa' llegarte" -> "Serás tu lugar"
- "Sólo vine a darte hasta las seis" -> "Te daré seis horas"
"""
from typing import List, Tuple
import re
import random

# Reglas de distorsión fonética / homófonos urbanos y malentendidos acústicos
ACOUSTIC_CONFUSIONS: List[Tuple[str, str]] = [
    # Desglose de jerga / intros
    (r"\brudeboyz\b", "mujer"),
    (r"\brudeboys\b", "mujer"),
    (r"\bmamacita\b", "una madre"),
    (r"\bme has vuelto un mare\b", "él me trajo un burro y una madre"),
    (r"\bun mare\b", "un burro"),
    (r"\bajá\b", "AHA"),
    (r"\baja\b", "AHA"),
    (r"\bhistoria real\b", "historia y mi amor"),
    (r"\btú sabes que te estoy hablando a ti\b", "te digo"),
    (r"\bte estoy hablando a ti\b", "te digo"),
    (r"\bdice\b", "él dijo"),
    
    # Confusiones de cama / amanecer
    (r"\bhoy pienso que ella me ama\b", "ahora me amas"),
    (r"\bporque amanezco en su cama\b", "¿por qué debería dejar mi cama?"),
    (r"\bvan varias noche de eso\b", "come otra noche"),
    (r"\bcreo que la matan mis besos\b", "esperé antes de que me mataran"),
    
    # Confusiones acuáticas / piernas
    (r"\bsiento que puedo nadar\b", "quiero soportar"),
    (r"\bflotando entre sus piernas pongo dulce el mar\b", "en mis piernas dormí sin dormir, quiero lavar"),
    (r"\bpongo dulce el mar\b", "quiero lavar"),
    (r"\bsiento que en sus aguas puedo navegar\b", "estoy en la playa"),
    (r"\bya llegue a la orilla y no me voy a ahogar\b", "y no quiero morir"),
    (r"\bno me voy a ahogar\b", "no quiero morir"),
    
    # GPS / Reloj
    (r"\bpa' llegarte siempre donde estés\b", "serás tu lugar"),
    (r"\bpa llegarte siempre donde estés\b", "serás tu lugar"),
    (r"\bdéjame contarte, yo no vine a amarte\b", "estoy diciendo que no lo necesitas"),
    (r"\bdejame contarte, yo no vine a amarte\b", "estoy diciendo que no lo necesitas"),
    (r"\byo no vine a amarte\b", "no lo necesitas"),
    (r"\bsólo vine a darte hasta las seis\b", "te daré seis horas"),
    (r"\bsolo vine a darte hasta las seis\b", "te daré seis horas"),
    (r"\bdarte hasta las seis\b", "darte seis horas"),

    # Homófonos generales del español callejero
    (r"\bpa'?\b", "para"),
    (r"\bta'?\b", "está"),
    (r"\bna'?\b", "nada"),
    (r"\btoy\b", "estoy"),
    (r"\btonces\b", "entonces"),
    (r"\btamo\b", "estamos"),
    (r"\bvamo\b", "vamos"),
    (r"\bhacerlo\b", "producir un objeto"),
    (r"\bpartir\b", "dividir en dos mitades"),
    (r"\bromper\b", "quebrar la estructura"),
    (r"\bbroma\b", "niebla espesa marina"),
]

# Sustituciones acústicas estocásticas leves si el texto no contiene modismos exactos
GENERIC_PHONETIC_DRIFTS: List[Tuple[str, str]] = [
    (r"\bcasa\b", "caza"),
    (r"\bvaso\b", "bazo"),
    (r"\bciento\b", "siento"),
    (r"\bves\b", "vez"),
    (r"\bhora\b", "ola"),
    (r"\btubo\b", "tuvo"),
    (r"\bhaya\b", "halla"),
]

def apply_acoustic_layer(text: str, intensity: float = 1.0) -> Tuple[str, List[str]]:
    """
    Aplica una capa de distorsión acústica previa al texto (malentendidos fonéticos,
    jerga interpretada literalmente y mondegreens).
    
    Args:
        text: Texto de entrada.
        intensity: Factor de agresividad (0.0 a 1.0).
        
    Returns:
        Tupla con (texto_distorsionado, lista_de_cambios_realizados).
    """
    if not text or not text.strip():
        return "", []

    distorted = text
    applied_changes = []

    # 1. Aplicar transformaciones de modismos y confusiones acústicas
    for pattern, replacement in ACOUSTIC_CONFUSIONS:
        if re.search(pattern, distorted, flags=re.IGNORECASE):
            distorted = re.sub(pattern, replacement, distorted, flags=re.IGNORECASE)
            applied_changes.append(f"Malentendido acústico: '{pattern}' -> '{replacement}'")

    # 2. Si intensity es alta, añadir derivas fonéticas generales
    if intensity > 0.7:
        for pattern, replacement in GENERIC_PHONETIC_DRIFTS:
            if random.random() < 0.4 and re.search(pattern, distorted, flags=re.IGNORECASE):
                distorted = re.sub(pattern, replacement, distorted, flags=re.IGNORECASE)
                applied_changes.append(f"Homófono: '{pattern}' -> '{replacement}'")

    return distorted, applied_changes
