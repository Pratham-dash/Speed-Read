export function calculateOrpIndex(word) {
  const clean = (word || "").replace(/[^a-z0-9]/gi, "");
  const len = clean.length;
  if (len <= 1) return 0;
  if (len <= 5) return 1;
  if (len <= 9) return 2;
  if (len <= 13) return 3;
  return Math.min(len - 1, Math.round(len * 0.35));
}
