export function setupDragDrop({ zone, input, onFile }) {
  const activate = () => zone.classList.add("active");
  const deactivate = () => zone.classList.remove("active");

  zone.addEventListener("click", () => input.click());
  zone.addEventListener("dragover", (e) => {
    e.preventDefault();
    activate();
  });
  zone.addEventListener("dragleave", deactivate);
  zone.addEventListener("drop", (e) => {
    e.preventDefault();
    deactivate();
    const file = e.dataTransfer?.files?.[0];
    if (file) onFile(file);
  });

  input.addEventListener("change", () => {
    const file = input.files?.[0];
    if (file) onFile(file);
  });
}
