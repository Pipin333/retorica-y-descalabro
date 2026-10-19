"""
Tests automatizados para la arquitectura BYOK y el motor de traducción multilingüe puro.
"""
import pytest
from fastapi.testclient import TestClient
from main import app
from whispers import CHAOS_PRESETS, generate_random_chain
from llm_client import LLMClient, SYSTEM_PROMPTS

client = TestClient(app)

def test_api_providers_endpoint():
    """Valida que el endpoint entregue los metadatos de proveedores y presets."""
    response = client.get("/api/providers")
    assert response.status_code == 200
    data = response.json()
    assert "providers" in data
    assert "groq" in data["providers"]
    assert "gemini" in data["providers"]
    assert "languages" in data
    assert "es" in data["languages"]

def test_llm_client_unconfigured():
    """Valida que un cliente sin API key rechace llamadas no locales."""
    client_llm = LLMClient(api_key=None, base_url="https://api.groq.com/openai/v1")
    assert not client_llm.is_configured()
    with pytest.raises(ValueError):
        client_llm.generate("hola", "prompt")

def test_generate_random_chain():
    """Valida la generación de saltos aleatorios sin hardcoding."""
    chain = generate_random_chain(hops=5)
    assert chain[0] == "es"
    assert chain[-1] == "es"
    assert len(chain) == 7

def test_api_enrich_requires_key():
    """Valida que el endpoint de enriquecimiento requiera API Key."""
    payload = {
        "text": "Sigue tu camino",
        "formality_level": 2,
        "llm": {
            "base_url": "https://api.groq.com/openai/v1",
            "api_key": None,
            "model": "llama-3.3-70b-versatile"
        }
    }
    response = client.post("/api/enrich", json=payload)
    assert response.status_code == 400
    assert "Falta configurar la API Key" in response.json()["detail"]

def test_api_whispers_mocked_llm(monkeypatch):
    """Valida la llamada a simulación LLM en teléfono descompuesto usando mock."""
    def mock_generate(self, prompt, system_prompt, temperature=0.7):
        return "Simulación de teléfono descompuesto sin hardcoding"

    monkeypatch.setattr(LLMClient, "generate", mock_generate)

    payload = {
        "text": "Canción arbitraria cualquiera",
        "mode": "llm",
        "llm": {
            "base_url": "https://api.groq.com/openai/v1",
            "api_key": "dummy_test_key",
            "model": "llama-3.3-70b-versatile"
        }
    }
    response = client.post("/api/whispers", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["final"] == "Simulación de teléfono descompuesto sin hardcoding"
    assert data["mode"] == "llm"

def test_api_whispers_chain_mode(monkeypatch):
    """Valida la traducción real pura en modo chain."""
    def mock_run_whispers(text, chain=None, delay_between_hops=0.3, acoustic_distortion=False):
        return {
            "original": text,
            "final": "Texto degradado por idiomas",
            "chain": chain or ["es", "en", "es"],
            "steps": [
                {"step": 0, "lang_name": "Texto Original", "text": text},
                {"step": 1, "lang_name": "Inglés", "text": "Degraded text"},
                {"step": 2, "lang_name": "Español", "text": "Texto degradado por idiomas"}
            ]
        }

    import main
    monkeypatch.setattr(main, "run_whispers_chain", mock_run_whispers)

    payload = {
        "text": "Hola mundo",
        "mode": "chain",
        "preset": "ligero",
        "llm": {
            "base_url": "https://api.groq.com/openai/v1",
            "api_key": None,
            "model": "llama-3.3-70b-versatile"
        }
    }
    response = client.post("/api/whispers", json=payload)
    assert response.status_code == 200
    assert response.json()["final"] == "Texto degradado por idiomas"
