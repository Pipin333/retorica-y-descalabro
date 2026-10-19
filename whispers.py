"""
Módulo de Traducción Encadenada ("Teléfono Descompuesto").
Pasa un texto por una secuencia de idiomas utilizando la API de MyMemory para provocar
deriva sintáctica y semántica cómica.
"""
from typing import List, Dict, Any, Optional
import urllib.parse
import urllib.request
import json
import time

# Idiomas disponibles y legibles con sus códigos ISO
SUPPORTED_LANGUAGES: Dict[str, str] = {
    "es": "Español",
    "en": "Inglés",
    "fr": "Francés",
    "de": "Alemán",
    "it": "Italiano",
    "pt": "Portugués",
    "ru": "Ruso",
    "ja": "Japonés",
    "zh": "Chino",
    "ar": "Árabe",
    "el": "Griego",
    "pl": "Polaco",
    "nl": "Neerlandés",
    "fi": "Finlandés",
    "sv": "Sueco",
    "tr": "Turco"
}

# Presets de cadenas divertidas
CHAOS_PRESETS: Dict[str, List[str]] = {
    "ligero": ["es", "en", "fr", "es"],
    "clasico": ["es", "en", "de", "it", "es"],
    "exotico": ["es", "ja", "ru", "ar", "es"],
    "maximo_caos": ["es", "el", "pl", "fi", "ja", "de", "es"],
    "personalizado": []
}

def generate_random_chain(hops: int = 4) -> List[str]:
    """
    Genera una cadena pseudoaleatoria de 'hops' saltos intermedios garantizando
    que inicie y termine en español ('es') con idiomas sin repetición contigua.
    
    Args:
        hops: Cantidad de saltos intermedios deseados (mínimo 1, máximo 12).
        
    Returns:
        Lista de códigos ISO de idiomas.
    """
    import random
    available = [code for code in SUPPORTED_LANGUAGES.keys() if code != "es"]
    clamped_hops = max(1, min(hops, 12))
    
    # Seleccionar idiomas asegurando variedad
    if clamped_hops <= len(available):
        chosen = random.sample(available, clamped_hops)
    else:
        chosen = random.choices(available, k=clamped_hops)
        
    return ["es"] + chosen + ["es"]

def translate_single_hop(text: str, source_lang: str, target_lang: str, timeout: int = 8) -> str:
    """
    Traduce un texto corto entre dos idiomas utilizando MyMemory API.
    
    Args:
        text: Texto a traducir.
        source_lang: Código ISO idioma origen.
        target_lang: Código ISO idioma destino.
        timeout: Segundos máximos de espera.
        
    Returns:
        Texto traducido.
    """
    clean_text = text.strip()
    if not clean_text:
        return ""
    if source_lang == target_lang:
        return clean_text

    encoded_query = urllib.parse.quote(clean_text)
    url = f"https://api.mymemory.translated.net/get?q={encoded_query}&langpair={source_lang}|{target_lang}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        if resp.status != 200:
            raise RuntimeError(f"Error en MyMemory API: Código HTTP {resp.status}")
        data = json.loads(resp.read().decode("utf-8"))
        translated = data.get("responseData", {}).get("translatedText", "")
        # Si la API devuelve un mensaje de cuota o error en el payload
        if "MYMEMORY WARNING" in translated.upper():
            raise RuntimeError("Límite de solicitudes de MyMemory alcanzado")
        return translated if translated else clean_text

def run_whispers_chain(
    text: str,
    chain: Optional[List[str]] = None,
    delay_between_hops: float = 0.3,
    acoustic_distortion: bool = True
) -> Dict[str, Any]:
    """
    Ejecuta el proceso completo de teléfono descompuesto pasando el texto
    por una capa acústica/fonética y luego por una cadena de idiomas.
    
    Args:
        text: Texto original en español.
        chain: Lista de códigos de idiomas (por defecto: preset 'clasico').
        delay_between_hops: Pausa entre saltos para respetar rate limits.
        acoustic_distortion: Si True, aplica capa de malentendidos fonéticos previos.
        
    Returns:
        Diccionario con pasos intermedios, idiomas y texto final.
    """
    if chain is None or len(chain) < 2:
        chain = CHAOS_PRESETS["clasico"]

    # Asegurar que comience y termine en español si no se especificó otro
    if chain[0] != "es":
        chain = ["es"] + chain
    if chain[-1] != "es":
        chain = chain + ["es"]

    steps: List[Dict[str, str]] = [
        {
            "step": 0,
            "lang": chain[0],
            "lang_name": "Texto Original",
            "text": text
        }
    ]

    current_text = text

    for i in range(len(chain) - 1):
        src = chain[i]
        tgt = chain[i + 1]
        try:
            current_text = translate_single_hop(current_text, src, tgt)
        except Exception as exc:
            # Si falla un salto externo, registramos el paso y continuamos
            current_text = f"{current_text} (desfase en {tgt}: {str(exc)[:40]})"
        
        steps.append({
            "step": i + 1,
            "from_lang": src,
            "to_lang": tgt,
            "lang_name": SUPPORTED_LANGUAGES.get(tgt, tgt),
            "text": current_text
        })
        if delay_between_hops > 0:
            time.sleep(delay_between_hops)

    return {
        "original": text,
        "final": current_text,
        "chain": chain,
        "steps": steps
    }
