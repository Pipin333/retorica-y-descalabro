"""
Servidor principal FastAPI para la aplicación de Teléfono Descompuesto y Enriquecedor de Párrafos.
Ofrece endpoints REST y sirve la interfaz web frontend.
"""
from typing import List, Optional
import os
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

from enricher import enrich_text_heuristic
from whispers import run_whispers_chain, generate_random_chain, CHAOS_PRESETS, SUPPORTED_LANGUAGES
from llm_client import LLMClient, DEFAULT_SYSTEM_ENRICHER, DEFAULT_SYSTEM_WHISPERS

app = FastAPI(
    title="Traductor Teléfono Descompuesto & Enriquecedor Barroco",
    description="Aplicación web interactiva híbrida (heurística/APIs de traducción y LLM opcional).",
    version="1.0.0"
)

# Servir archivos estáticos
STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# Modelos Pydantic para validación de entrada
class EnrichRequest(BaseModel):
    text: str = Field(..., min_length=1, description="Texto de entrada a enriquecer")
    mode: str = Field("heuristic", description="'heuristic' o 'llm'")
    formality_level: int = Field(2, ge=1, le=3, description="Nivel de formalidad (1 a 3)")
    llm_base_url: Optional[str] = Field("https://api.groq.com/openai/v1")
    llm_api_key: Optional[str] = Field(None)
    llm_model: Optional[str] = Field("llama-3.1-8b-instant")

class WhispersRequest(BaseModel):
    text: str = Field(..., min_length=1, description="Texto original a distorsionar")
    mode: str = Field("chain", description="'chain' (traducción real encadenada) o 'llm'")
    preset: Optional[str] = Field("clasico", description="Nombre del preset: ligero, clasico, exotico, maximo_caos, personalizado")
    custom_chain: Optional[List[str]] = Field(None, description="Cadena personalizada de códigos de idioma")
    custom_hops: Optional[int] = Field(None, ge=1, le=12, description="Número de saltos aleatorios si el preset es 'personalizado'")
    acoustic_distortion: Optional[bool] = Field(True, description="Si True, añade capa previa de malentendidos fonéticos/mondegreens")
    llm_base_url: Optional[str] = Field("https://api.groq.com/openai/v1")
    llm_api_key: Optional[str] = Field(None)
    llm_model: Optional[str] = Field("llama-3.1-8b-instant")

@app.get("/")
def serve_index():
    """Entrega la página web principal."""
    index_path = os.path.join(STATIC_DIR, "index.html")
    if not os.path.exists(index_path):
        raise HTTPException(status_code=404, detail="Frontend index.html no encontrado")
    return FileResponse(index_path)

@app.get("/api/languages")
def get_languages():
    """Retorna los idiomas soportados y los presets de cadenas de teléfono descompuesto."""
    return {
        "languages": SUPPORTED_LANGUAGES,
        "presets": CHAOS_PRESETS
    }

@app.post("/api/enrich")
def enrich_text_endpoint(req: EnrichRequest):
    """
    Enriquece un párrafo coloquial/urbano a lenguaje barroco o académico rimbombante.
    """
    if req.mode == "llm":
        client = LLMClient(
            base_url=req.llm_base_url or "https://api.groq.com/openai/v1",
            api_key=req.llm_api_key,
            model=req.llm_model or "llama-3.1-8b-instant"
        )
        if not client.is_configured():
            raise HTTPException(
                status_code=400,
                detail="El modo LLM requiere una API Key válida (ej. de Groq u OpenRouter) o un host local como Ollama."
            )
        try:
            result = client.generate(req.text, DEFAULT_SYSTEM_ENRICHER)
            return {"original": req.text, "result": result, "mode": "llm"}
        except RuntimeError as exc:
            raise HTTPException(status_code=502, detail=str(exc))
    
    # Modo heurístico de alta velocidad (sin costo de API)
    result = enrich_text_heuristic(req.text, req.formality_level)
    return {"original": req.text, "result": result, "mode": "heuristic"}

@app.post("/api/whispers")
def whispers_endpoint(req: WhispersRequest):
    """
    Simula el 'teléfono descompuesto' mediante saltos idiomáticos o simulación con LLM.
    """
    if req.mode == "llm":
        client = LLMClient(
            base_url=req.llm_base_url or "https://api.groq.com/openai/v1",
            api_key=req.llm_api_key,
            model=req.llm_model or "llama-3.1-8b-instant"
        )
        if not client.is_configured():
            raise HTTPException(
                status_code=400,
                detail="El modo LLM requiere una API Key válida o servicio local (Ollama)."
            )
        try:
            result = client.generate(req.text, DEFAULT_SYSTEM_WHISPERS)
            return {
                "original": req.text,
                "final": result,
                "chain": ["es", "llm-chaos", "es"],
                "steps": [
                    {"step": 0, "lang_name": "Español Original", "text": req.text},
                    {"step": 1, "lang_name": "Traducción Cruda Descompuesta", "text": result}
                ],
                "mode": "llm"
            }
        except RuntimeError as exc:
            raise HTTPException(status_code=502, detail=str(exc))

    # Modo cadena de traducción real
    chain = req.custom_chain
    if not chain:
        if req.preset == "personalizado":
            hops = req.custom_hops or 4
            chain = generate_random_chain(hops)
        else:
            chain = CHAOS_PRESETS.get(req.preset or "clasico", CHAOS_PRESETS["clasico"])

    res = run_whispers_chain(
        req.text,
        chain=chain,
        acoustic_distortion=req.acoustic_distortion if req.acoustic_distortion is not None else True
    )
    res["mode"] = "chain"
    return res
