import React from 'react';
import { Container, Card, Button } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';
import { getUserId, clearAuth } from './api';

function Projects() {
  const navigate = useNavigate();
  const userId = getUserId();

  const handleSignOut = () => {
    clearAuth();
    navigate('/');
  };

  return (
    <Container className="py-4">
      <div className="d-flex justify-content-between align-items-center mb-4">
        <h2>Projects</h2>
        <div className="d-flex align-items-center gap-2">
          <span className="text-muted">Signed in as {userId}</span>
          <Button variant="outline-secondary" size="sm" onClick={handleSignOut}>
            Sign Out
          </Button>
        </div>
      </div>

      <div className="row g-3">
        <div className="col-md-6">
          <Card className="h-100 shadow-sm">
            <Card.Body>
              <Card.Title>Create New Project</Card.Title>
              <Card.Text className="text-muted">
                Add a new project with name, description, and project ID. Use the API client in this app to call <code>POST /api/projects/create</code>.
              </Card.Text>
              <Button variant="primary" disabled>
                Create Project (wire up form next)
              </Button>
            </Card.Body>
          </Card>
        </div>
        <div className="col-md-6">
          <Card className="h-100 shadow-sm">
            <Card.Body>
              <Card.Title>Login to Existing Project</Card.Title>
              <Card.Text className="text-muted">
                Enter a project ID to open an existing project. Use <code>POST /api/projects/login</code> with the API client.
              </Card.Text>
              <Button variant="secondary" disabled>
                Enter Project (wire up form next)
              </Button>
            </Card.Body>
          </Card>
        </div>
      </div>
    </Container>
  );
}

export default Projects;
