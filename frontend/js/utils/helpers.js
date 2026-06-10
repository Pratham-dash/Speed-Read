export function debounce(fn, wait = 100) {
  let t;
  return (...args) => {
    clearTimeout(t);
    t = setTimeout(() => fn(...args), wait);
  };
}

export function sanitizeText(input) {
  return (input || "").replace(/[<>]/g, "").trim();
}
