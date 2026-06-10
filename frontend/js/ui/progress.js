export function updateProgress(progressInput, progressLabel, current, total) {
  progressInput.max = Math.max(0, total - 1);
  progressInput.value = Math.min(current, Math.max(0, total - 1));
  progressLabel.textContent = `${Math.min(current + 1, total)} / ${total}`;
}
