/**
 * Main project list component
 */
import React, { useEffect, useState } from 'react';
import { api } from '../../api/client';
import ProjectItem from './ProjectItem';
import CreateProjectWidget from './CreateProjectWidget';
import './ProjectList.css';

function ProjectList() {
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadProjects();
  }, []);

  const loadProjects = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await api.listProjects();
      setProjects(data.projects);
    } catch (err) {
      setError('Failed to load projects');
      console.error('Error loading projects:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleProjectClick = (repoName) => {
    console.log('Project clicked:', repoName);
    // TODO: Navigate to project detail view
  };

  const handleCreateProject = () => {
    console.log('Create new project clicked');
    // TODO: Open create project dialog
  };

  if (loading) {
    return (
      <div className="project-list-container">
        <div className="project-list-header">
          <h2>ContextKeep Projects</h2>
        </div>
        <div>Loading projects...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="project-list-container">
        <div className="project-list-header">
          <h2>ContextKeep Projects</h2>
        </div>
        <div className="error">{error}</div>
      </div>
    );
  }

  return (
    <div className="project-list-container">
      <div className="project-list-header">
        <h2>ContextKeep Projects</h2>
      </div>

      <div className="project-list-content">
        {projects.length === 0 ? (
          <div className="empty-state">
            <p>No projects found.</p>
            <p>Create your first project to get started.</p>
          </div>
        ) : (
          projects.map((project) => (
            <ProjectItem
              key={project.repo_name}
              project={project}
              onProjectClick={handleProjectClick}
            />
          ))
        )}
      </div>

      <div className="project-list-footer">
        <CreateProjectWidget onCreate={handleCreateProject} />
      </div>
    </div>
  );
}

export default ProjectList;