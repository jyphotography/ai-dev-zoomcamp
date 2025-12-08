import React, { useEffect, useState, useRef } from 'react'
import { io } from 'socket.io-client'
import { runJavaScript } from './utils'

const SERVER = import.meta.env.VITE_SERVER || window.location.origin

export default function App() {
  const [sessionId, setSessionId] = useState('')
  const [code, setCode] = useState('// start coding')
  const [language, setLanguage] = useState('javascript')
  const socketRef = useRef(null)

  useEffect(() => {
    socketRef.current = io(SERVER)
    const s = socketRef.current
    s.on('init', ({ code, language: lang }) => {
      if (code !== undefined) setCode(code)
      if (lang) setLanguage(lang)
    })
    s.on('code:update', ({ code }) => setCode(code))
    s.on('language:update', ({ language }) => setLanguage(language))
    return () => s.disconnect()
  }, [])

  function createSession() {
    fetch(`${SERVER}/session`, { method: 'POST' })
      .then(r => r.json())
      .then(data => {
        setSessionId(data.id)
        socketRef.current.emit('join', { sessionId: data.id })
      })
  }

  function joinSession() {
    if (!sessionId) return alert('Enter session id')
    socketRef.current.emit('join', { sessionId })
  }

  function updateCode(v) {
    setCode(v)
    if (sessionId) socketRef.current.emit('code:update', { sessionId, code: v })
  }

  function changeLanguage(l) {
    setLanguage(l)
    if (sessionId) socketRef.current.emit('language:update', { sessionId, language: l })
  }

  async function runCode() {
    if (language === 'javascript') {
      try {
        const result = runJavaScript(code)
        alert(String(result))
      } catch (e) {
        alert(String(e))
      }
    } else if (language === 'python') {
      try {
        // dynamic loader
        const { loadPyodideIfNeeded } = await import('./pyodide-loader')
        await loadPyodideIfNeeded()
        const res = await window.pyodide.runPythonAsync(code)
        alert(String(res))
      } catch (e) {
        alert(String(e))
      }
    }
  }

  return (
    <div style={{ padding: 20, fontFamily: 'sans-serif' }}>
      <h2>Collaborative Editor</h2>
      <div style={{ marginBottom: 8 }}>
        <button onClick={createSession}>Create Session</button>
        <input value={sessionId} onChange={e => setSessionId(e.target.value)} placeholder="session id" style={{ marginLeft: 8 }} />
        <button onClick={joinSession} style={{ marginLeft: 8 }}>Join</button>
      </div>

      <div style={{ marginBottom: 8 }}>
        <label>Language: </label>
        <select value={language} onChange={e => changeLanguage(e.target.value)}>
          <option value="javascript">JavaScript</option>
          <option value="python">Python</option>
        </select>
        <button onClick={runCode} style={{ marginLeft: 8 }}>Run</button>
      </div>

      <textarea
        value={code}
        onChange={e => updateCode(e.target.value)}
        style={{ width: '100%', height: 400, fontFamily: 'monospace', fontSize: 14 }}
      />
    </div>
  )
}
