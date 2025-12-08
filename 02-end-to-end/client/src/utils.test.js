import { describe, it, expect } from 'vitest'
import { runJavaScript } from './utils'

describe('runJavaScript', () => {
  it('evaluates expressions', () => {
    expect(runJavaScript('1+2')).toBe(3)
  })

  it('returns string results', () => {
    expect(runJavaScript("'a'.toUpperCase()")).toBe('A')
  })
})
