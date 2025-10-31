import React, { useState, useEffect } from 'react'
import { api } from '../api/client'
import './CodeDisplay.css'

function CodeDisplay({ projectId, filePath }) {
  const [content, setContent] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  useEffect(() => {
    if (filePath) {
      loadFile()
    } else {
      setContent('')
      setError(null)
    }
  }, [projectId, filePath])

  const loadFile = async () => {
    setLoading(true)
    setError(null)
    try {
      const data = await api.readFile(projectId, filePath)
      setContent(data.content)
    } catch (err) {
      setError(err.message)
      setContent('')
    } finally {
      setLoading(false)
    }
  }

  if (!filePath) {
    return (
      <div className="code-display-empty">
        <div className="empty-state">
          <span className="empty-icon">📄</span>
          <p>Select a file to view its contents</p>
        </div>
      </div>
    )
  }

  if (loading) {
    return (
      <div className="code-display">
        <div className="code-display-header">
          <span className="file-path">📄 {filePath}</span>
        </div>
        <div className="code-display-loading">Loading file...</div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="code-display">
        <div className="code-display-header">
          <span className="file-path">📄 {filePath}</span>
          <button onClick={loadFile} className="reload-btn" title="Reload">
            ↻
          </button>
        </div>
        <div className="code-display-error">
          <span className="error-icon">⚠️</span>
          <p>Error: {error}</p>
          <button onClick={loadFile} className="retry-btn">Retry</button>
        </div>
      </div>
    )
  }

  return (
    <div className="code-display">
      <div className="code-display-header">
        <span className="file-path">📄 {filePath}</span>
        <button onClick={loadFile} className="reload-btn" title="Reload">
          ↻
        </button>
      </div>
      <div className="code-display-content">
        <pre className="code-pre">
          <code className="code-text">
            {content.split('\n').map((line, i) => (
              <div key={i} className="code-line">
                <span className="line-number">{i + 1}</span>
                <span className="line-content">{line || ' '}</span>
              </div>
            ))}
          </code>
        </pre>
      </div>
    </div>
  )
}

export default CodeDisplay