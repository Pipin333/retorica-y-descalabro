// Controlador frontend con soporte BYOK y gestión en LocalStorage

// Proveedores predeterminados
const PROVIDERS_INFO = {
  groq: {
    base_url: "https://api.groq.com/openai/v1",
    model: "llama-3.3-70b-versatile",
    hint: "💡 Obtén tu API Key gratis en <strong>console.groq.com</strong>. Solo toma 30 segundos."
  },
  gemini: {
    base_url: "https://generativelanguage.googleapis.com/v1beta/openai",
    model: "gemini-1.5-flash",
    hint: "💡 Obtén tu API Key gratis en <strong>aistudio.google.com</strong> con tu cuenta de Google."
  },
  openrouter: {
    base_url: "https://openrouter.ai/api/v1",
    model: "meta-llama/llama-3.2-3b-instruct:free",
    hint: "💡 Obtén tu API Key en <strong>openrouter.ai/keys</strong> (modelos :free disponibles)."
  },
  openai: {
    base_url: "https://api.openai.com/v1",
    model: "gpt-4o-mini",
    hint: "💡 Requiere API Key con saldo en <strong>platform.openai.com</strong>."
  },
  ollama: {
    base_url: "http://localhost:11434/v1",
    model: "llama3.1",
    hint: "💡 No requiere API Key. Requiere tener Ollama ejecutándose en tu máquina local."
  },
  custom: {
    base_url: "https://api.openai.com/v1",
    model: "custom-model",
    hint: "💡 Introduce la URL base y modelo compatible con la especificación de OpenAI."
  }
};

const ENRICHER_SAMPLES = {
  1: "Sigue tu camino que sin ti me va mejor, ahora tengo otras que me lo hacen mejor",
  2: "Hola amigo, hoy no tengo plata para salir a comer, pero la noche está linda para ir a la playa",
  3: "Me rompiste el corazón y me engañaste, no te creo nada de lo que dices, cállate ya"
};

const WHISPERS_SAMPLES = {
  1: `Rudeboyz
Ajá
Yo, esto es una historia real, mi amor
Tú sabes que te estoy hablando a ti
Me has vuelto un mare, mamacita
Dice
Hoy pienso que ella me ama
Porque amanezco en su cama
Van varias noche de eso
Creo que la matan mis besos
Siento que puedo nadar
Flotando entre sus piernas pongo dulce el mar
Siento que en sus aguas puedo navegar
Ya llegue a la orilla y no me voy a ahogar
Yo no necesito un GPS
Pa' llegarte siempre donde estés
Déjame contarte, yo no vine a amarte
Sólo vine a darte hasta las seis`,
  2: "No me vuelvas a llamar porque ya no me importa nada de lo que hagas con tu vida, te deseo lo peor"
};

// Inicialización de la aplicación
document.addEventListener("DOMContentLoaded", () => {
  setupTabs();
  setupCharCounters();
  loadStoredConfig();
  checkFirstVisitAndModal();
  loadEnricherSample(1);
});

function setupCharCounters() {
  const enricherInput = document.getElementById("enricher-input");
  const enricherCounter = document.getElementById("enricher-char-counter");
  const whispersInput = document.getElementById("whispers-input");
  const whispersCounter = document.getElementById("whispers-char-counter");

  const updateCounter = (inputEl, counterEl) => {
    const len = inputEl.value.length;
    counterEl.innerText = `${len.toLocaleString()} / 10.000`;
    if (len >= 9900) {
      counterEl.className = "char-counter limit";
    } else if (len >= 8000) {
      counterEl.className = "char-counter warning";
    } else {
      counterEl.className = "char-counter";
    }
  };

  enricherInput.addEventListener("input", () => updateCounter(enricherInput, enricherCounter));
  whispersInput.addEventListener("input", () => updateCounter(whispersInput, whispersCounter));

  // Exponer para actualización tras cargar muestras
  window.updateAllCounters = () => {
    updateCounter(enricherInput, enricherCounter);
    updateCounter(whispersInput, whispersCounter);
  };
}

function setupTabs() {
  const tabEnricher = document.getElementById("tab-enricher");
  const tabWhispers = document.getElementById("tab-whispers");
  const panelEnricher = document.getElementById("panel-enricher");
  const panelWhispers = document.getElementById("panel-whispers");

  tabEnricher.addEventListener("click", () => {
    tabEnricher.classList.add("active");
    tabEnricher.setAttribute("aria-selected", "true");
    tabWhispers.classList.remove("active");
    tabWhispers.setAttribute("aria-selected", "false");

    panelEnricher.classList.add("active");
    panelEnricher.removeAttribute("hidden");
    panelWhispers.classList.remove("active");
    panelWhispers.setAttribute("hidden", "true");
  });

  tabWhispers.addEventListener("click", () => {
    tabWhispers.classList.add("active");
    tabWhispers.setAttribute("aria-selected", "true");
    tabEnricher.classList.remove("active");
    tabEnricher.setAttribute("aria-selected", "false");

    panelWhispers.classList.add("active");
    panelWhispers.removeAttribute("hidden");
    panelEnricher.classList.remove("active");
    panelEnricher.setAttribute("hidden", "true");
  });
}

// Gestión de LocalStorage para BYOK
function getLLMConfig() {
  const provider = localStorage.getItem("byok_provider") || "groq";
  const apiKey = localStorage.getItem("byok_api_key") || "";
  const baseUrl = localStorage.getItem("byok_base_url") || PROVIDERS_INFO[provider]?.base_url || "https://api.groq.com/openai/v1";
  const model = localStorage.getItem("byok_model") || PROVIDERS_INFO[provider]?.model || "llama-3.3-70b-versatile";

  return {
    provider,
    api_key: apiKey.trim(),
    base_url: baseUrl.trim(),
    model: model.trim()
  };
}

function updateStatusIndicator() {
  const config = getLLMConfig();
  const dot = document.getElementById("api-status-dot");
  const text = document.getElementById("api-status-text");
  const banner = document.getElementById("key-warning-banner");

  const isConfigured = config.provider === "ollama" || Boolean(config.api_key);

  if (isConfigured) {
    dot.className = "status-dot dot-connected";
    text.innerText = `Conectado: ${config.provider.toUpperCase()}`;
    banner.style.display = "none";
  } else {
    dot.className = "status-dot dot-missing";
    text.innerText = "Configurar API Key";
    banner.style.display = "flex";
  }
}

function loadStoredConfig() {
  const config = getLLMConfig();
  document.getElementById("provider-select").value = config.provider;
  document.getElementById("modal-api-key").value = config.api_key;
  document.getElementById("modal-base-url").value = config.base_url;
  document.getElementById("modal-model").value = config.model;
  updateProviderHint(config.provider);
  updateStatusIndicator();
}

function checkFirstVisitAndModal() {
  const hasVisited = localStorage.getItem("byok_modal_seen");
  const config = getLLMConfig();
  const isConfigured = config.provider === "ollama" || Boolean(config.api_key);

  // Si es la primera vez que abre la página y no tiene key, abrir modal automáticamente
  if (!hasVisited && !isConfigured) {
    openKeyModal();
    localStorage.setItem("byok_modal_seen", "true");
  }
}

function openKeyModal() {
  const modal = document.getElementById("byok-modal");
  loadStoredConfig();
  if (modal.showModal) {
    modal.showModal();
  } else {
    modal.style.display = "block";
  }
}

function closeKeyModal() {
  const modal = document.getElementById("byok-modal");
  if (modal.close) {
    modal.close();
  } else {
    modal.style.display = "none";
  }
}

function handleProviderChange() {
  const provider = document.getElementById("provider-select").value;
  const info = PROVIDERS_INFO[provider] || PROVIDERS_INFO["groq"];

  document.getElementById("modal-base-url").value = info.base_url;
  document.getElementById("modal-model").value = info.model;
  updateProviderHint(provider);
}

function updateProviderHint(provider) {
  const info = PROVIDERS_INFO[provider] || PROVIDERS_INFO["groq"];
  document.getElementById("provider-hint-text").innerHTML = info.hint;
}

function saveKeyConfig() {
  const provider = document.getElementById("provider-select").value;
  const apiKey = document.getElementById("modal-api-key").value.trim();
  const baseUrl = document.getElementById("modal-base-url").value.trim();
  const model = document.getElementById("modal-model").value.trim();

  localStorage.setItem("byok_provider", provider);
  localStorage.setItem("byok_api_key", apiKey);
  localStorage.setItem("byok_base_url", baseUrl);
  localStorage.setItem("byok_model", model);
  localStorage.setItem("byok_modal_seen", "true");

  updateStatusIndicator();
  closeKeyModal();
}

// Handlers de Muestras
function loadEnricherSample(id) {
  const input = document.getElementById("enricher-input");
  if (ENRICHER_SAMPLES[id]) {
    input.value = ENRICHER_SAMPLES[id];
    if (window.updateAllCounters) window.updateAllCounters();
  }
}

function loadWhispersSample(id) {
  const input = document.getElementById("whispers-input");
  if (WHISPERS_SAMPLES[id]) {
    input.value = WHISPERS_SAMPLES[id];
    if (window.updateAllCounters) window.updateAllCounters();
  }
}

// Petición al Enriquecedor
async function handleEnrich() {
  const text = document.getElementById("enricher-input").value.trim();
  const level = parseInt(document.getElementById("enricher-level").value, 10);
  const outputContainer = document.getElementById("enricher-output-container");
  const btn = document.getElementById("btn-run-enricher");
  const config = getLLMConfig();

  if (!text) {
    alert("Por favor introduce una frase o texto para enriquecer.");
    return;
  }

  if (config.provider !== "ollama" && !config.api_key) {
    openKeyModal();
    return;
  }

  btn.disabled = true;
  outputContainer.className = "output-box";
  outputContainer.innerHTML = `
    <div class="loading-indicator">
      <div class="spinner"></div>
      <span>Elaborando disertación barroca con ${escapeHtml(config.model)}...</span>
    </div>
  `;

  try {
    const payload = {
      text,
      formality_level: level,
      llm: {
        base_url: config.base_url,
        api_key: config.api_key || null,
        model: config.model
      }
    };

    const res = await fetch("/api/enrich", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    const data = await res.json();
    if (!res.ok) {
      throw new Error(data.detail || "Error al procesar la solicitud.");
    }

    outputContainer.className = "output-box baroque-style";
    outputContainer.innerHTML = `<span id="enricher-output">${escapeHtml(data.result)}</span>`;
  } catch (err) {
    outputContainer.className = "output-box";
    outputContainer.innerHTML = `<p style="color: var(--danger);">⚠️ ${escapeHtml(err.message)}</p>`;
  } finally {
    btn.disabled = false;
  }
}

// Petición al Teléfono Descompuesto
async function handleWhispers() {
  const text = document.getElementById("whispers-input").value.trim();
  const mode = document.getElementById("whispers-mode").value;
  const preset = document.getElementById("whispers-preset").value;
  const outputContainer = document.getElementById("whispers-output-container");
  const stepsSection = document.getElementById("whispers-steps-section");
  const stepsTimeline = document.getElementById("steps-timeline");
  const btn = document.getElementById("btn-run-whispers");
  const config = getLLMConfig();

  if (!text) {
    alert("Por favor introduce un texto para descomponer.");
    return;
  }

  if (mode === "llm" && config.provider !== "ollama" && !config.api_key) {
    openKeyModal();
    return;
  }

  btn.disabled = true;
  outputContainer.innerHTML = `
    <div class="loading-indicator">
      <div class="spinner"></div>
      <span>${mode === "llm" ? "Generando descalabro acústico y semántico..." : "Traduciendo por la red multilingüe..."}</span>
    </div>
  `;
  stepsSection.style.display = "none";
  stepsTimeline.innerHTML = "";

  try {
    let customHops = null;
    if (preset === "personalizado") {
      const hopsVal = parseInt(document.getElementById("custom-hops-input").value, 10);
      customHops = !isNaN(hopsVal) ? hopsVal : 4;
    }

    const payload = {
      text,
      mode,
      preset,
      custom_hops: customHops,
      llm: {
        base_url: config.base_url,
        api_key: config.api_key || null,
        model: config.model
      }
    };

    const res = await fetch("/api/whispers", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    const data = await res.json();
    if (!res.ok) {
      throw new Error(data.detail || "Error en el procesamiento.");
    }

    outputContainer.innerHTML = `<div id="whispers-final-text"><strong>${escapeHtml(data.final)}</strong></div>`;

    if (data.steps && data.steps.length > 0) {
      stepsTimeline.innerHTML = data.steps.map(step => `
        <div class="timeline-step">
          <div class="timeline-step-header">
            <span>Paso ${step.step}: ${escapeHtml(step.lang_name || step.to_lang || "Traducción")}</span>
          </div>
          <div class="timeline-step-text">${escapeHtml(step.text)}</div>
        </div>
      `).join("");
      stepsSection.style.display = "block";
    }
  } catch (err) {
    outputContainer.innerHTML = `<p style="color: var(--danger);">⚠️ ${escapeHtml(err.message)}</p>`;
  } finally {
    btn.disabled = false;
  }
}

function toggleWhispersModeUI() {
  const mode = document.getElementById("whispers-mode").value;
  const chainPresetContainer = document.getElementById("chain-preset-container");
  const customConfig = document.getElementById("custom-preset-config");

  if (mode === "chain") {
    chainPresetContainer.style.display = "flex";
    togglePresetCustomOptions();
  } else {
    chainPresetContainer.style.display = "none";
    customConfig.style.display = "none";
  }
}

function togglePresetCustomOptions() {
  const preset = document.getElementById("whispers-preset").value;
  const customConfig = document.getElementById("custom-preset-config");
  if (preset === "personalizado") {
    customConfig.style.display = "flex";
  } else {
    customConfig.style.display = "none";
  }
}

function copyToClipboard(elementId, btnElement) {
  const el = document.getElementById(elementId);
  if (!el) return;
  const text = el.innerText || el.textContent;
  navigator.clipboard.writeText(text).then(() => {
    const originalText = btnElement.innerText;
    btnElement.innerText = "¡Copiado!";
    btnElement.style.color = "var(--success)";
    setTimeout(() => {
      btnElement.innerText = originalText;
      btnElement.style.color = "";
    }, 2000);
  });
}

function escapeHtml(text) {
  if (!text) return "";
  return text
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}
