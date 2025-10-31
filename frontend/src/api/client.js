const API_BASE = 'http://localhost:8765'

export const api = {
  async getFileTree(projectId, maxDepth = 3, showHidden = false) {
    const params = new URLSearchParams({
      max_depth: maxDepth,
      show_hidden: showHidden
    })
    const response = await fetch(`${API_BASE}/projects/${projectId}/tree?${params}`)
    if (!response.ok) {
      throw new Error(`Failed to fetch file tree: ${response.statusText}`)
    }
    return response.json()
  },

  async readFile(projectId, filePath) {
    const response = await fetch(`${API_BASE}/projects/${projectId}/files/${filePath}`)
    if (!response.ok) {
      throw new Error(`Failed to read file: ${response.statusText}`)
    }
    return response.json()
  },

  async writeFile(projectId, filePath, content) {
    const response = await fetch(`${API_BASE}/projects/${projectId}/files/${filePath}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ content })
    })
    if (!response.ok) {
      throw new Error(`Failed to write file: ${response.statusText}`)
    }
    return response.json()
  }
}