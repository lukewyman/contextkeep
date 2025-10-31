import React, { useState } from 'react'
import FileTree from './components/FileTree'
import CodeDisplay from './components/CodeDisplay'
import './App.css'

function App() {
  const [projectId] = useState('test-project')
  const [selectedFile, setSelectedFile] = useState(null)
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false)

  return (
    <div className="app">
      <header className="app-header">
        <div className="header-left">
          <button 
            className="toggle-sidebar-btn"
            onClick={() => setSidebarCollapsed(!sidebarCollapsed)}
            title={sidebarCollapsed ? "Show sidebar" : "Hide sidebar"}
          >
            {sidebarCollapsed ? '→' : '←'}
          </button>
          <h1 className="app-title">ContextKeep</h1>
          <span className="project-name">{projectId}</span>
        </div>
      </header>

      <div className="app-content">
        {!sidebarCollapsed && (
          <aside className="sidebar">
            <FileTree 
              projectId={projectId} 
              onFileSelect={setSelectedFile}
              selectedFile={selectedFile}
            />
          </aside>
        )}

        <main className="main-content">
          <CodeDisplay 
            projectId={projectId} 
            filePath={selectedFile}
          />
        </main>
      </div>
    </div>
  )
}

export default App