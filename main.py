"""
Servidor principal FastAPI para la aplicación de Teléfono Descompuesto y Enriquecedor de Párrafos.
Opera con LLM bajo esquema BYOK (Bring Your Own Key) y preserva la cadena de traducción real multilingüe.
"""
from typing import List, Optional
import os
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

from llm_client import LLMClient, SYSTEM_PROMPTS, PROVIDER_DEFAULTS
from whispers import run_whispers_chain, generate_random_chain, CHAOS_PRESETS, SUPPORTED_LANGUAGES

app = FastAPI(
    title="Retórica & Descalabro",
    description="Transformador de jerga a prosa barroca y simulador de teléfono descompuesto con LLM BYOK y traducción multilingüe.",
    version="2.0.0"
)

# Servir frontend estático
STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

class LLMConfig(BaseModel):
    base_url: str = Field("https://api.groq.com/openai/v1")
    api_key: Optional[str] = Field(None)
    model: str = Field("llama-3.3-70b-versatile")

class EnrichRequest(BaseModel):
    text: str = Field(..., min_length=1, description="Texto de entrada a enriquecer")
    formality_level: int = Field(2, ge=1, le=3, description="Nivel de formalidad (1: Formal, 2: Académico, 3: Rococó)")
    llm: LLMConfig

class WhispersRequest(BaseModel):
    text: str = Field(..., min_length=1, description="Texto original a distorsionar")
    mode: str = Field("llm", description="'llm' (simulación realista de mondegreens/slang) o 'chain' (traducción real por idiomas)")
    preset: Optional[str] = Field("clasico")
    custom_chain: Optional[List[str]] = Field(None)
    custom_hops: Optional[int] = Field(None, ge=1, le=12)
    llm: LLMConfig

@app.get("/")
def serve_index():
    """Entrega la página web principal."""
    index_path = os.path.join(STATIC_DIR, "index.html")
    if not os.path.exists(index_path):
        raise HTTPException(status_code=404, detail="index.html no encontrado")
    return FileResponse(index_path)

@app.get("/api/providers")
def get_providers_metadata():
    """Retorna los metadatos de configuración de proveedores LLM y lenguajes soportados."""
    return {
        "providers": PROVIDER_DEFAULTS,
        "languages": SUPPORTED_LANGUAGES,
        "presets": CHAOS_PRESETS
    }

@app.post("/api/enrich")
def enrich_endpoint(req: EnrichRequest):
    """
    Enriquece un texto mediante el LLM configurado por el usuario.
    """
    client = LLMClient(
        base_url=req.llm.base_url,
        api_key=req.llm.api_key,
        model=req.llm.model
    )
    if not client.is_configured():
        raise HTTPException(
            status_code=400,
            detail="Falta configurar la API Key. Por favor añade tu clave en el modal de configuración (esquina superior derecha)."
        )

    sys_key = f"enricher_{req.formality_level}"
    system_prompt = SYSTEM_PROMPTS.get(sys_key, SYSTEM_PROMPTS["enricher_2"])

    try:
        result = client.generate(req.text, system_prompt, temperature=0.7)
        return {"original": req.text, "result": result, "mode": "llm"}
    except (ValueError, RuntimeError) as exc:
        raise HTTPException(status_code=502, detail=str(exc))

@app.post("/api/whispers")
def whispers_endpoint(req: WhispersRequest):
    """
    Ejecuta el teléfono descompuesto a través de LLM contextual o por cadena de idiomas.
    """
    if req.mode == "llm":
        client = LLMClient(
            base_url=req.llm.base_url,
            api_key=req.llm.api_key,
            model=req.llm.model
        )
        if not client.is_configured():
            raise HTTPException(
                status_code=400,
                detail="Falta configurar la API Key en el modal de configuración."
            )
        try:
            result = client.generate(req.text, SYSTEM_PROMPTS["whispers"], temperature=0.85)
            return {
                "original": req.text,
                "final": result,
                "chain": ["es", "llm-mondegreen-translation", "es"],
                "steps": [
                    {"step": 0, "lang_name": "Texto Original", "text": req.text},
                    {"step": 1, "lang_name": "👂 Simulación Acústica & Back-Translation", "text": result}
                ],
                "mode": "llm"
            }
        except (ValueError, RuntimeError) as exc:
            raise HTTPException(status_code=502, detail=str(exc))

    # Modo Traducción Encadenada Real
    chain = req.custom_chain
    if not chain:
        if req.preset == "personalizado":
            hops = req.custom_hops or 4
            chain = generate_random_chain(hops)
        else:
            chain = CHAOS_PRESETS.get(req.preset or "clasico", CHAOS_PRESETS["clasico"])

    # En cadena pura, pasamos acoustic_distortion=False para no alterar artificialmente el texto con diccionarios
    res = run_whispers_chain(req.text, chain=chain, acoustic_distortion=False)
    res["mode"] = "chain"
    return res
