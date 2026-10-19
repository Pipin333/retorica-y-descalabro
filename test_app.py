"""
Tests automatizados para validar los endpoints y motores de enriquecimiento y teléfono descompuesto.
"""
import pytest
from fastapi.testclient import TestClient
from main import app
from enricher import enrich_text_heuristic
from whispers import CHAOS_PRESETS

client = TestClient(app)

def test_enrich_heuristic_unit():
    """Valida la sustitución léxica de canciones conocidas en modo heurístico."""
    original = "Sigue tu camino que sin ti me va mejor, ahora tengo otras que me lo hacen mejor"
    enriched = enrich_text_heuristic(original, formality_level=2)
    assert "continúa con tu sendero" in enriched
    assert "calidad de mi" in enriched
    assert "entidades femeninas" in enriched

def test_api_languages_endpoint():
    """Valida que el endpoint de metadatos de idiomas funcione."""
    response = client.get("/api/languages")
    assert response.status_code == 200
    data = response.json()
    assert "languages" in data
    assert "presets" in data
    assert "es" in data["languages"]
    assert "clasico" in data["presets"]

def test_api_enrich_endpoint():
    """Valida la petición POST de enriquecimiento por API."""
    payload = {
        "text": "hola amigo, tengo hambre",
        "mode": "heuristic",
        "formality_level": 2
    }
    response = client.post("/api/enrich", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["mode"] == "heuristic"
    assert "salutaciones" in data["result"].lower() or "inanición" in data["result"].lower()

def test_api_whispers_mocked_chain(monkeypatch):
    """Valida el endpoint de teléfono descompuesto simulando saltos."""
    def mock_run_whispers(text, chain=None, delay_between_hops=0.3, acoustic_distortion=True):
        return {
            "original": text,
            "final": "Texto distorsionado",
            "chain": chain or ["es", "en", "es"],
            "steps": [
                {"step": 0, "lang_name": "Español", "text": text},
                {"step": 1, "lang_name": "Inglés", "text": "Distorted text"},
                {"step": 2, "lang_name": "Español", "text": "Texto distorsionado"}
            ]
        }

    import main
    monkeypatch.setattr(main, "run_whispers_chain", mock_run_whispers)

    payload = {
        "text": "No necesito un GPS",
        "mode": "chain",
        "preset": "ligero",
        "acoustic_distortion": True
    }
    response = client.post("/api/whispers", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["final"] == "Texto distorsionado"
    assert len(data["steps"]) == 3

def test_acoustic_layer_unit():
    """Valida la distorsión acústica de jerga y confusiones fonéticas."""
    from acoustic import apply_acoustic_layer
    lyrics = "Rudeboyz Ajá Me has vuelto un mare, mamacita Dice Hoy pienso que ella me ama"
    distorted, changes = apply_acoustic_layer(lyrics)
    assert "mujer" in distorted.lower()
    assert "burro" in distorted.lower()
    assert "ahora me amas" in distorted.lower()
    assert len(changes) >= 3
