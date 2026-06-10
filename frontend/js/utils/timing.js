export function calculateDelayMs(word, wpm, isHeading = false) {
  const base = Math.max(1, Math.floor(60000 / Number(wpm || 400)));
  const cleanLen = (word || "").replace(/[^a-z0-9]/gi, "").length;
  const mult = cleanLen <= 3 ? 0.9 : cleanLen <= 6 ? 1 : cleanLen <= 9 ? 1.2 : 1.4;
  let delay = Math.floor(base * mult);
  if (/[.!?]$/.test(word)) delay += base * 2;
  else if (/[,;:]$/.test(word)) delay += base;
  if (isHeading) delay *= 5;
  return delay;
}
