# 📜 Retórica & Descalabro
> **Enriquecedor de Párrafos Barroco** & **Traductor de Teléfono Descompuesto (Back-Translation)**

Una aplicación web interactiva híbrida desarrollada con **FastAPI**, **Deep-Translator** / **MyMemory API**, heurísticas léxicas barrocas y soporte opcional para **LLMs gratuitos** (Groq / OpenRouter / Ollama).

---

## 🚀 Características

1. **✨ Enriquecedor de Párrafos (Poshifier / Barroquizador)**:
   - Toma frases cotidianas, modismos o canciones urbanas (ej. *Bad Bunny*) y las transforma en tratados filosóficos solemnes y rimbombantes del siglo XIX.
   - **Tres niveles de rimbombancia**: Carta Formal, Tratado Académico y Barroco Rococó Absurdo.
   - Funciona instantáneamente de manera local mediante un analizador heurístico sin depender obligatoriamente de claves de pago.

2. **📞 Teléfono Descompuesto Multilingüe (Back-Translation Simulator)**:
   - Pasa un texto por una secuencia de traducciones sucesivas a través de idiomas variados (Español ➔ Inglés ➔ Alemán ➔ Italiano ➔ Español, o rutas con Árabe, Japonés, Ruso y Finés).
   - Muestra el **timeline interactivo de saltos** paso a paso para ver cómo las metáforas se desmoronan cómicamente en traducciones literales.

3. **🧠 Enfoque Híbrido con Modelos de Lenguaje**:
   - Incluye un panel desplegable de configuración opcional para conectar modelos OpenAI-compatibles gratuitos (como **Groq con Llama 3**, OpenRouter, o tu instancia local de **Ollama**).

---

## 🛠️ Instalación y Ejecución Local

### Prerrequisitos
- Python 3.10 o superior

### 1. Clonar o acceder a la carpeta del proyecto
```bash
cd telefono-descompuesto-poshifier
```

### 2. Crear y activar el entorno virtual
```bash
python -m venv .venv

# En Windows PowerShell:
.\.venv\Scripts\Activate.ps1

# En Linux/macOS:
source .venv/bin/activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Iniciar el servidor web
```bash
uvicorn main:app --reload --port 8000
```

Abre tu navegador en: **`http://localhost:8000`**

---

## 🧪 Pruebas Automatizadas

Para correr la suite de pruebas unitarias y de integración:
```bash
pytest -v
```

---

## 🐳 Ejecución con Docker (Opcional)

Si cuentas con Docker instalado:
```bash
docker compose up --build
```
La aplicación quedará disponible en `http://localhost:8000`.
