import React, { useState, useEffect } from 'react'
import { api } from '../api/client'
import './FileTree.css'

function FileTree({ projectId, onFileSelect, selectedFile }) {
  const [tree, setTree] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [expanded, setExpanded] = useState(new Set())

  useEffect(() => {
    loadTree()
  }, [projectId])

  const loadTree = async () => {
    setLoading(true)
    setError(null)
    try {
      const data = await api.getFileTree(projectId)
      setTree(data.tree)
      // Auto-expand root level
      const rootPaths = data.tree
        .filter(node => node.type === 'directory')
        .map(node => node.path)
      setExpanded(new Set(rootPaths))
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  const toggleExpand = (path) => {
    setExpanded(prev => {
      const next = new Set(prev)
      if (next.has(path)) {
        next.delete(path)
      } else {
        next.add(path)
      }
      return next
    })
  }

  if (loading) {
    return (
      <div className="file-tree">
        <div className="file-tree-header">
          <h3>📁 Files</h3>
        </div>
        <div className="file-tree-loading">Loading files...</div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="file-tree">
        <div className="file-tree-header">
          <h3>📁 Files</h3>
          <button onClick={loadTree} className="refresh-btn" title="Refresh">
            ↻
          </button>
        </div>
        <div className="file-tree-error">
          Error: {error}
          <button onClick={loadTree} className="retry-btn">Retry</button>
        </div>
      </div>
    )
  }

  return (
    <div className="file-tree">
      <div className="file-tree-header">
        <h3>📁 Files</h3>
        <button onClick={loadTree} className="refresh-btn" title="Refresh">
          ↻
        </button>
      </div>
      <div className="file-tree-content">
        {tree && tree.length > 0 ? (
          <TreeNode
            items={tree}
            expanded={expanded}
            onToggle={toggleExpand}
            onFileSelect={onFileSelect}
            selectedFile={selectedFile}
            level={0}
          />
        ) : (
          <div className="file-tree-empty">No files found</div>
        )}
      </div>
    </div>
  )
}

function TreeNode({ items, expanded, onToggle, onFileSelect, selectedFile, level }) {
  return (
    <ul className="tree-list" style={{ paddingLeft: level === 0 ? 0 : 16 }}>
      {items.map((item) => (
        <li key={item.path} className="tree-item">
          {item.type === 'directory' ? (
            <>
              <div
                className="tree-node-label directory"
                onClick={() => onToggle(item.path)}
              >
                <span className="tree-icon">
                  {expanded.has(item.path) ? '📂' : '📁'}
                </span>
                <span className="tree-name">{item.name}</span>
              </div>
              {expanded.has(item.path) && item.children && item.children.length > 0 && (
                <TreeNode
                  items={item.children}
                  expanded={expanded}
                  onToggle={onToggle}
                  onFileSelect={onFileSelect}
                  selectedFile={selectedFile}
                  level={level + 1}
                />
              )}
            </>
          ) : (
            <div
              className={`tree-node-label file ${selectedFile === item.path ? 'selected' : ''}`}
              onClick={() => onFileSelect(item.path)}
            >
              <span className="tree-icon">📄</span>
              <span className="tree-name">{item.name}</span>
            </div>
          )}
        </li>
      ))}
    </ul>
  )
}

export default FileTree