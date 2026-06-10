import { config } from "../config.js";
import { calculateOrpIndex } from "../utils/orp.js";
import { calculateDelayMs } from "../utils/timing.js";

export async function processText(text, wpm) {
  const payload = { text, wpm };
  try {
    const response = await fetch(`${config.apiBaseUrl}/api/process-text`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    return await response.json();
  } catch (_e) {
    return localProcess(text, wpm);
  }
}

export async function processFile(file, wpm) {
  const form = new FormData();
  form.append("file", file);
  form.append("wpm", String(wpm));

  try {
    const response = await fetch(`${config.apiBaseUrl}/api/process-pdf`, {
      method: "POST",
      body: form,
    });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    return await response.json();
  } catch (_e) {
    const text = await file.text();
    return localProcess(text, wpm);
  }
}

function localProcess(text, wpm) {
  const words = String(text || "")
    .split(/\s+/)
    .filter(Boolean)
    .map((word, index) => ({
      index,
      word,
      orp_index: calculateOrpIndex(word),
      delay_ms: calculateDelayMs(word, wpm, false),
      is_heading: false,
    }));

  return {
    wpm,
    total_words: words.length,
    estimated_read_seconds: Math.round((words.reduce((acc, w) => acc + w.delay_ms, 0) / 1000) * 100) / 100,
    words,
  };
}
