export function bindControls({ playBtn, pauseBtn, restartBtn, onPlay, onPause, onRestart }) {
  playBtn.addEventListener("click", onPlay);
  pauseBtn.addEventListener("click", onPause);
  restartBtn.addEventListener("click", onRestart);
}
