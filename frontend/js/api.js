export async function request(url, method, data) {
  const response = await fetch(url, {
    method,
    headers: {"Content-Type": "application/json"},
    body: data === undefined ? undefined : JSON.stringify(data)
  });
  const body = response.status === 204 ? null : await response.json();
  if (!response.ok) {
    const detail = body.detail;
    const message = Array.isArray(detail)
      ? detail.map(error => `${error.loc.join(" / ")}: ${error.msg}`).join("\n")
      : typeof detail === "object" ? `${(detail.path || []).join(" / ")}: ${detail.message}` : detail;
    throw new Error(message || `Ошибка HTTP ${response.status}`);
  }
  return body;
}

export function showError(container, error) {
  const box = container.querySelector(".error");
  box.textContent = error.message;
  box.hidden = false;
}
