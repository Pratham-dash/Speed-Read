export function renderWord(container, word, orpIndex) {
  if (!word) {
    container.textContent = "Done";
    return;
  }
  const idx = Math.min(Math.max(0, orpIndex), word.length - 1);
  container.innerHTML = `${word.slice(0, idx)}<span class="pivot">${word[idx] || ""}</span>${word.slice(idx + 1)}`;
}
