export function notify(container, message, timeout = 3000) {
  const node = document.createElement("div");
  node.className = "toast";
  node.textContent = message;
  container.appendChild(node);
  setTimeout(() => node.remove(), timeout);
}
