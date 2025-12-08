export function runJavaScript(code) {
  // very small wrapper around eval for testability
  // In production this should be sandboxed.
  // eslint-disable-next-line no-eval
  return eval(code)
}
