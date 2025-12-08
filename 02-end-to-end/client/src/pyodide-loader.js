export async function loadPyodideIfNeeded() {
  if (window.pyodide) return window.pyodide
  // load from CDN
  const script = document.createElement('script')
  script.src = 'https://cdn.jsdelivr.net/pyodide/v0.24.0/full/pyodide.js'
  document.head.appendChild(script)
  await new Promise((res, rej) => {
    script.onload = res
    script.onerror = () => rej(new Error('Failed to load pyodide'))
  })
  // eslint-disable-next-line no-undef
  window.pyodide = await loadPyodide({ indexURL: 'https://cdn.jsdelivr.net/pyodide/v0.24.0/full/' })
  return window.pyodide
}
