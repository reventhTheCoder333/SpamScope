const messageEl = document.getElementById("message");
const analyzeBtn = document.getElementById("analyze-btn");
const clearBtn = document.getElementById("clear-btn");
const resultEl = document.getElementById("result");
const resultLabel = document.getElementById("result-label");
const resultSummary = document.getElementById("result-summary");
const meterFill = document.getElementById("meter-fill");
const meterMarker = document.getElementById("meter-marker");
const spamPercent = document.getElementById("spam-percent");
const errorEl = document.getElementById("error");

function hideError() {
  errorEl.classList.add("hidden");
  errorEl.textContent = "";
}

function showError(message) {
  errorEl.textContent = message;
  errorEl.classList.remove("hidden");
  resultEl.classList.add("hidden");
}

function formatPercent(value) {
  return `${(value * 100).toFixed(1)}%`;
}

function showResult(data) {
  hideError();
  resultEl.classList.remove("hidden");

  const isSpam = data.label === "spam";
  resultLabel.textContent = isSpam ? "Spam" : "Not spam";
  resultLabel.className = `badge ${data.label}`;

  resultSummary.textContent = isSpam
    ? "This message looks like spam."
    : "This message looks legitimate.";

  const spamPct = data.spam_probability * 100;
  meterFill.style.width = `${100 - spamPct}%`;
  meterMarker.style.left = `${spamPct}%`;
  spamPercent.textContent = `${formatPercent(data.spam_probability)} spam probability`;
  spamPercent.style.color = isSpam ? "var(--spam)" : "var(--ham)";
}

async function analyze() {
  const text = messageEl.value.trim();
  if (!text) {
    showError("Please enter a message to analyze.");
    return;
  }

  hideError();
  analyzeBtn.disabled = true;
  analyzeBtn.textContent = "Analyzing…";

  try {
    const response = await fetch("/api/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text }),
    });

    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.detail || "Analysis failed.");
    }

    showResult(data);
  } catch (err) {
    showError(err.message || "Something went wrong. Please try again.");
  } finally {
    analyzeBtn.disabled = false;
    analyzeBtn.textContent = "Analyze";
  }
}

function clearAll() {
  messageEl.value = "";
  resultEl.classList.add("hidden");
  hideError();
  messageEl.focus();
}

analyzeBtn.addEventListener("click", analyze);
clearBtn.addEventListener("click", clearAll);

messageEl.addEventListener("keydown", (event) => {
  if ((event.ctrlKey || event.metaKey) && event.key === "Enter") {
    event.preventDefault();
    analyze();
  }
});
