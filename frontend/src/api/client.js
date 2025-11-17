/**
 * API client using native fetch
 */

const API_BASE_URL = '/api';

async function handleResponse(response) {
  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Unknown error' }));
    throw new Error(error.detail || `HTTP ${response.status}`);
  }
  return response.json();
}

export const api = {
  async listProjects() {
    const response = await fetch(`${API_BASE_URL}/projects`);
    return handleResponse(response);
  }
};