"""
Servicio cliente para proveedores de LLM gratuitos o de bajo coste (OpenAI-compatible, Groq, OpenRouter, Ollama, etc.).
Permite invocar modelos para enriquecer texto o simular teléfono descompuesto con gran precisión semántica.
"""
from typing import Optional, Dict, Any
import requests

DEFAULT_SYSTEM_ENRICHER = """Eres un maestro de la retórica barroca, culteranismo, hiper-formalidad y lenguaje académico del siglo XIX.
Tu única labor es transformar la frase o párrafo que te entregue el usuario a una versión cómica, absurdamente elevada, rimbombante, pomposa y pedante, usando perífrasis complejas, sinónimos latinizados y descripciones anatómicas o pseudocientíficas para conceptos callejeros.
Conserva el significado nuclear exacto pero enmascarado en la más pomposa pedantería.
Responde ÚNICAMENTE con el texto transformado, sin introducciones ni explicaciones."""

DEFAULT_SYSTEM_WHISPERS = """Eres un motor de traducción literal ultra-estricto y desprovisto de sentido común o contexto idiomático ('teléfono descompuesto').
Tu tarea es simular lo que le ocurre a un texto popular tras ser traducido toscamente a través de múltiples idiomas extraños y devuelto al español.
Rompe las frases hechas y metáforas traduciéndolas a palabras literales, crea falsos cognados cómicos, altera ligeramente los tiempos verbales y genera ese estilo absurdo pero misteriosamente reconocible (ejemplo: 'te tengo ganas' -> 'poseo deseos carnales en tu dirección', 'me mareas' -> 'me has vuelto un mare').
Responde ÚNICAMENTE con el texto resultante, sin explicaciones ni comillas."""

class LLMClient:
    """Cliente ligero para interactuar con APIs de lenguaje compatibles con OpenAI/Groq/Ollama."""

    def __init__(
        self,
        base_url: str = "https://api.groq.com/openai/v1",
        api_key: Optional[str] = None,
        model: str = "llama-3.1-8b-instant"
    ):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.model = model

    def is_configured(self) -> bool:
        """Indica si el cliente cuenta con los parámetros mínimos para intentar llamada."""
        if "localhost" in self.base_url or "127.0.0.1" in self.base_url:
            return True
        return bool(self.api_key and self.api_key.strip())

    def generate(self, prompt: str, system_prompt: str, temperature: float = 0.8) -> str:
        """
        Envía un prompt a la API de LLM configurada.
        
        Args:
            prompt: Texto de entrada.
            system_prompt: Instrucción de sistema rectora.
            temperature: Variabilidad estocástica.
            
        Returns:
            Texto generado por el modelo.
            
        Raises:
            RuntimeError: Si la llamada a la API falla o arroja un código de error HTTP.
        """
        url = f"{self.base_url}/chat/completions"
        headers: Dict[str, str] = {
            "Content-Type": "application/json"
        }
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        payload: Dict[str, Any] = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            "temperature": temperature,
            "max_tokens": 1024
        }

        try:
            response = requests.post(url, json=payload, headers=headers, timeout=20)
            if response.status_code != 200:
                raise RuntimeError(
                    f"Error de API LLM (Código {response.status_code}): {response.text[:300]}"
                )
            data = response.json()
            return data["choices"][0]["message"]["content"].strip()
        except requests.RequestException as exc:
            raise RuntimeError(f"Error de red al conectar con el LLM: {str(exc)}") from exc
