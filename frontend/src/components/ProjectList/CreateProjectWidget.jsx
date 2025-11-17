/**
 * Create new project widget
 */
import React from 'react';

function CreateProjectWidget({ onCreate }) {
  return (
    <div className="create-project-widget" onClick={onCreate}>
      <span className="create-icon">[+]</span>
      <span className="create-text">Create New Project</span>
    </div>
  );
}

export default CreateProjectWidget;