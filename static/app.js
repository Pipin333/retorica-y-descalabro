// Lógica de interacción frontend para Retórica & Descalabro

// Muestras predeterminadas para enriquecedor
const ENRICHER_SAMPLES = {
  1: "Sigue tu camino que sin ti me va mejor, ahora tengo otras que me lo hacen mejor",
  2: "Hola amigo, hoy no tengo plata para salir a comer, pero la noche está linda para ir a la playa",
  3: "Me rompiste el corazón y me engañaste, no te creo nada de lo que dices, callate ya"
};

// Muestras predeterminadas para teléfono descompuesto
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
  2: "No me vuelvas a llamar porque ya no me importa nada de lo que hagas con tu vida"
};

// Navegación entre pestañas
document.addEventListener("DOMContentLoaded", () => {
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

  // Cargar muestra 1 por defecto en el enriquecedor
  loadEnricherSample(1);
});

function loadEnricherSample(id) {
  const input = document.getElementById("enricher-input");
  if (ENRICHER_SAMPLES[id]) {
    input.value = ENRICHER_SAMPLES[id];
  }
}

function loadWhispersSample(id) {
  const input = document.getElementById("whispers-input");
  if (WHISPERS_SAMPLES[id]) {
    input.value = WHISPERS_SAMPLES[id];
  }
}

function getLLMConfig() {
  return {
    llm_base_url: document.getElementById("llm-base-url").value.trim(),
    llm_api_key: document.getElementById("llm-api-key").value.trim() || null,
    llm_model: document.getElementById("llm-model").value.trim()
  };
}

// Handler de Enriquecimiento
async function handleEnrich() {
  const text = document.getElementById("enricher-input").value.trim();
  const engine = document.getElementById("enricher-engine").value;
  const level = parseInt(document.getElementById("enricher-level").value, 10);
  const outputContainer = document.getElementById("enricher-output-container");
  const btn = document.getElementById("btn-run-enricher");

  if (!text) {
    alert("Por favor introduce una frase o texto para enriquecer.");
    return;
  }

  btn.disabled = true;
  outputContainer.className = "output-box";
  outputContainer.innerHTML = `
    <div class="loading-indicator">
      <div class="spinner"></div>
      <span>Destilando elocuencia y rebuscamiento barroco...</span>
    </div>
  `;

  try {
    const payload = {
      text,
      mode: engine,
      formality_level: level,
      ...getLLMConfig()
    };

    const res = await fetch("/api/enrich", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    const data = await res.json();
    if (!res.ok) {
      throw new Error(data.detail || "Error en el servidor al enriquecer el texto.");
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

// Handler de Teléfono Descompuesto
async function handleWhispers() {
  const text = document.getElementById("whispers-input").value.trim();
  const engine = document.getElementById("whispers-engine").value;
  const preset = document.getElementById("whispers-preset").value;
  const acoustic = document.getElementById("whispers-acoustic").value === "true";
  const outputContainer = document.getElementById("whispers-output-container");
  const stepsSection = document.getElementById("whispers-steps-section");
  const stepsTimeline = document.getElementById("steps-timeline");
  const btn = document.getElementById("btn-run-whispers");

  if (!text) {
    alert("Por favor introduce un texto para someter al teléfono descompuesto.");
    return;
  }

  btn.disabled = true;
  outputContainer.innerHTML = `
    <div class="loading-indicator">
      <div class="spinner"></div>
      <span>Haciendo saltos de idioma por el mundo...</span>
    </div>
  `;
  stepsSection.style.display = "none";
  stepsTimeline.innerHTML = "";

  try {
    const payload = {
      text,
      mode: engine,
      preset: preset,
      acoustic_distortion: acoustic,
      ...getLLMConfig()
    };

    const res = await fetch("/api/whispers", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    const data = await res.json();
    if (!res.ok) {
      throw new Error(data.detail || "Error al procesar teléfono descompuesto.");
    }

    outputContainer.innerHTML = `<div id="whispers-final-text"><strong>${escapeHtml(data.final)}</strong></div>`;

    // Renderizar pasos
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

function toggleWhispersMode() {
  const engine = document.getElementById("whispers-engine").value;
  const presetContainer = document.getElementById("whispers-preset-container");
  if (engine === "llm") {
    presetContainer.style.opacity = "0.5";
    presetContainer.style.pointerEvents = "none";
  } else {
    presetContainer.style.opacity = "1";
    presetContainer.style.pointerEvents = "auto";
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
