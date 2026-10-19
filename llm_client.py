"""
Cliente universal para proveedores de LLM bajo esquema BYOK (Bring Your Own Key).
Soporta proveedores compatibles con OpenAI/Groq/OpenRouter y Google Gemini (generativelanguage).
"""
from typing import Optional, Dict, Any, List
import requests

# Prompts refinados con ejemplos (Few-Shot) para calidad garantizada sin importar el texto
SYSTEM_PROMPTS = {
    "enricher_1": """Eres un maestro de la diplomacia, la redacción institucional y la elegancia formal.
Transforma el texto del usuario a un registro formal impecable, propio de correspondencia diplomática o un comunicado oficial solemne.
Conserva el significado nuclear del mensaje pero con exquisita cortesía y vocablo culto.
Responde ÚNICAMENTE con el texto transformado.""",

    "enricher_2": """Eres un catedrático erudito de filosofía y sociología del siglo XIX.
Transforma el texto del usuario (que puede ser jerga, reggaetón, modismos o frases cotidianas) a un tratado académico ultra-rimbombante, formal y denso.
Utiliza perífrasis complejas, sinónimos latinizados y descripciones antropológicas, biológicas o pseudocientíficas para cualquier concepto callejero o carnal.
Ejemplo de referencia:
Entrada: "Sigue tu camino que sin ti me va mejor, ahora tengo otras que me lo hacen mejor"
Salida: "Continúa con tu sendero porque en tu ausencia la calidad de mi vida ha aumentado; actualmente poseo a otras entidades femeninas que copulan más satisfactoriamente con mi persona."
Conserva con precisión quirúrgica el mensaje nuclear pero enmascarado en la más pomposa pedantería académica.
Responde ÚNICAMENTE con el texto resultante.""",

    "enricher_3": """Eres un poeta del Siglo de Oro español, discípulo extremo de Luis de Góngora y el culteranismo barroco.
Transforma el texto del usuario a un estilo rococó, barroco y conceptualmente hiperbólico al límite de lo absurdo.
Usa hipérbaton, metáforas mitológicas, perífrasis interminables y vocabulario barroco grandilocuente.
Responde ÚNICAMENTE con el texto resultante.""",

    "whispers": """Eres un simulador de 'Teléfono Descompuesto' (Chinese Whispers) multilingüe y malentendido auditivo (mondegreens).
Tu labor es tomar el texto de entrada (letras de canciones urbanas, modismos, mensajes hablados) y devolver lo que resultaría de:
1. Malentendidos acústicos propios de canciones oída a la rápida (interpretar sonidos por palabras absurdas parecidas).
2. Traducción literal sin modismos a través de varios idiomas exóticos y vuelta al español tosco.
3. Desmoronamiento de frases hechas en conceptos cómicos y literales.
Ejemplo de referencia:
Entrada:
"Rudeboyz. Ajá. Yo, esto es una historia real, mi amor. Tú sabes que te estoy hablando a ti. Me has vuelto un mare, mamacita. Dice. Hoy pienso que ella me ama porque amanezco en su cama. Van varias noche de eso, creo que la matan mis besos. Siento que puedo nadar, flotando entre sus piernas pongo dulce el mar. Yo no necesito un GPS pa' llegarte siempre donde estés, sólo vine a darte hasta las seis."
Salida:
"Mujer. AHA. Esta es mi historia y mi amor. Te digo: Él me trajo un burro y una madre. Él dijo: Ahora me amas, ¿por qué debería dejar mi cama? Come otra noche, esperé antes de que me mataran. Quiero soportar, en mis piernas dormí sin dormir, quiero lavar. Estoy en la playa y no quiero morir. No tengo GPS, serás tu lugar. Estoy diciendo que no lo necesitas, te daré seis horas."
Aplica este mismo fenómeno al texto que te proporcione el usuario, respetando su estructura estrófica o en párrafos.
Responde ÚNICAMENTE con la versión descompuesta."""
}

PROVIDER_DEFAULTS = {
    "groq": {
        "name": "Groq (Gratis, ultra-rápido)",
        "base_url": "https://api.groq.com/openai/v1",
        "default_model": "llama-3.3-70b-versatile",
        "key_hint": "Obtén tu API Key gratis en console.groq.com"
    },
    "openrouter": {
        "name": "OpenRouter (Modelos gratis y de pago)",
        "base_url": "https://openrouter.ai/api/v1",
        "default_model": "meta-llama/llama-3.2-3b-instruct:free",
        "key_hint": "Obtén tu API Key en openrouter.ai/keys"
    },
    "openai": {
        "name": "OpenAI",
        "base_url": "https://api.openai.com/v1",
        "default_model": "gpt-4o-mini",
        "key_hint": "Obtén tu API Key en platform.openai.com"
    },
    "gemini": {
        "name": "Google Gemini (OpenAI Compatible)",
        "base_url": "https://generativelanguage.googleapis.com/v1beta/openai",
        "default_model": "gemini-1.5-flash",
        "key_hint": "Obtén tu API Key gratis en aistudio.google.com"
    },
    "ollama": {
        "name": "Ollama Local",
        "base_url": "http://localhost:11434/v1",
        "default_model": "llama3.1",
        "key_hint": "Asegúrate de tener Ollama corriendo localmente"
    }
}

class LLMClient:
    """Cliente universal compatible con OpenAI API para LLMs bajo BYOK."""

    def __init__(
        self,
        base_url: str = "https://api.groq.com/openai/v1",
        api_key: Optional[str] = None,
        model: str = "llama-3.3-70b-versatile"
    ):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.model = model

    def is_configured(self) -> bool:
        """Determina si cuenta con la configuración para hacer llamadas."""
        if "localhost" in self.base_url or "127.0.0.1" in self.base_url:
            return True
        return bool(self.api_key and self.api_key.strip())

    def generate(self, prompt: str, system_prompt: str, temperature: float = 0.7) -> str:
        """
        Envía la petición a la API de inferencia.
        """
        if not self.is_configured():
            raise ValueError(
                "Falta configurar tu API Key (BYOK). Abre el modal de configuración en la esquina superior derecha."
            )

        url = f"{self.base_url}/chat/completions"
        headers: Dict[str, str] = {
            "Content-Type": "application/json"
        }
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key.strip()}"

        payload: Dict[str, Any] = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            "temperature": temperature,
            "max_tokens": 2048
        }

        try:
            response = requests.post(url, json=payload, headers=headers, timeout=25)
            if response.status_code != 200:
                raise RuntimeError(
                    f"Error de proveedor ({response.status_code}): {response.text[:300]}"
                )
            data = response.json()
            return data["choices"][0]["message"]["content"].strip()
        except requests.RequestException as exc:
            raise RuntimeError(f"Error de conexión con el proveedor de IA: {str(exc)}") from exc
