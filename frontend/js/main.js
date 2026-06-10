import { processFile, processText } from "./api/client.js";
import { setupDragDrop } from "./features/drag-drop.js";
import { setupKeyboard } from "./features/keyboard.js";
import { bindControls } from "./ui/controls.js";
import { notify } from "./ui/notifications.js";
import { play, restart, seek, setWords, stop, tick } from "./features/reader.js";
import { store } from "./state/store.js";
import { sanitizeText } from "./utils/helpers.js";

const ui = {
  textInput: document.getElementById("text-input"),
  processTextBtn: document.getElementById("process-text"),
  wpm: document.getElementById("wpm"),
  fileInput: document.getElementById("file-input"),
  dropZone: document.getElementById("drop-zone"),
  playBtn: document.getElementById("play-btn"),
  pauseBtn: document.getElementById("pause-btn"),
  restartBtn: document.getElementById("restart-btn"),
  progress: document.getElementById("progress"),
  progressLabel: document.getElementById("progress-label"),
  wordDisplay: document.getElementById("word-display"),
  notifications: document.getElementById("notifications"),
};

function getWpm() {
  return Number(ui.wpm.value || 400);
}

async function handleTextProcess() {
  const text = sanitizeText(ui.textInput.value);
  if (!text) return notify(ui.notifications, "Please add text to process");
  const result = await processText(text, getWpm());
  setWords(result.words);
  tick(ui);
  notify(ui.notifications, `Loaded ${result.total_words} words`);
}

async function handleFile(file) {
  if (!file) return;
  if (!/\.(pdf|txt)$/i.test(file.name)) return notify(ui.notifications, "Only PDF/TXT supported");
  const result = await processFile(file, getWpm());
  setWords(result.words);
  tick(ui);
  notify(ui.notifications, `Processed ${file.name}`);
}

bindControls({
  playBtn: ui.playBtn,
  pauseBtn: ui.pauseBtn,
  restartBtn: ui.restartBtn,
  onPlay: () => play(ui),
  onPause: () => stop(),
  onRestart: () => restart(ui),
});

setupDragDrop({ zone: ui.dropZone, input: ui.fileInput, onFile: handleFile });
setupKeyboard({
  onTogglePlay: () => (store.playing ? stop() : play(ui)),
  onRestart: () => restart(ui),
  onSeek: (delta) => seek(delta, ui),
});

ui.progress.addEventListener("input", () => {
  store.index = Number(ui.progress.value || 0);
  tick(ui);
});

ui.processTextBtn.addEventListener("click", handleTextProcess);

tick(ui);
