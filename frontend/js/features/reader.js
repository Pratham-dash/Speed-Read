import { renderWord } from "../ui/display.js";
import { updateProgress } from "../ui/progress.js";
import { store } from "../state/store.js";

export function setWords(words) {
  store.words = words || [];
  store.index = 0;
}

export function stop() {
  store.playing = false;
  if (store.timer) clearTimeout(store.timer);
  store.timer = null;
}

export function restart(ui) {
  stop();
  store.index = 0;
  tick(ui);
}

export function seek(delta, ui) {
  store.index = Math.min(Math.max(store.index + delta, 0), Math.max(store.words.length - 1, 0));
  tick(ui);
}

export function play(ui) {
  if (store.playing) return;
  store.playing = true;
  loop(ui);
}

function loop(ui) {
  if (!store.playing) return;
  const current = store.words[store.index];
  tick(ui);
  if (!current) {
    stop();
    return;
  }
  store.index += 1;
  store.timer = setTimeout(() => loop(ui), current.delay_ms || 150);
}

export function tick({ wordDisplay, progress, progressLabel }) {
  const current = store.words[store.index];
  renderWord(wordDisplay, current?.word, current?.orp_index ?? 0);
  updateProgress(progress, progressLabel, store.index, store.words.length);
}
