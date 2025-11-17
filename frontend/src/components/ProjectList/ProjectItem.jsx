/**
 * Individual project item component
 */
import React, { useState } from 'react';

function ProjectItem({ project, onProjectClick }) {
  const [expanded, setExpanded] = useState(false);

  const handleToggleExpand = (e) => {
    e.stopPropagation();
    setExpanded(!expanded);
  };

  const handleProjectClick = () => {
    onProjectClick(project.repo_name);
  };

  return (
    <div className="project-item">
      <div className="project-header" onClick={handleProjectClick}>
        <span onClick={handleToggleExpand} className="expand-icon">
          {expanded ? '[-]' : '[+]'}
        </span>
        <span className="project-name">{project.project_name}</span>
      </div>
      
      {expanded && (
        <div className="project-details">
          <div className="project-detail-row">
            <span className="detail-label">Repository:</span>
            <span className="detail-value">{project.repo_name}</span>
          </div>
          <div className="project-detail-row">
            <span className="detail-label">Description:</span>
            <span className="detail-value">{project.description}</span>
          </div>
        </div>
      )}
    </div>
  );
}

export default ProjectItem;