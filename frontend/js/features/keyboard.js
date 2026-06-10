export function setupKeyboard({ onTogglePlay, onRestart, onSeek }) {
  document.addEventListener("keydown", (e) => {
    if (e.target && ["INPUT", "TEXTAREA", "SELECT"].includes(e.target.tagName)) return;
    if (e.code === "Space") {
      e.preventDefault();
      onTogglePlay();
    }
    if (e.key.toLowerCase() === "r") onRestart();
    if (e.key === "ArrowRight") onSeek(1);
    if (e.key === "ArrowLeft") onSeek(-1);
  });
}
