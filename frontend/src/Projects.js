import React from 'react';
import { Container, Card, Button, Form } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';
import { getUserId, clearAuth, post } from './api';

function Projects() {
  const navigate = useNavigate();
  const userId = getUserId();
  //project creation
  const [newProjName, setNewProjName] = React.useState('');
  const [newProjDesc, setNewProjDesc] = React.useState('');
  const [newProjId, setNewProjId] = React.useState('');
  //project joinage
  const [joinProjId, setJoinProjId] = React.useState('');

  const handleSignOut = () => {
    clearAuth();
    navigate('/');
  };

  const handleCreateProject = async (e) => {
    e.preventDefault();
    try {
      const { ok, data } = await post('/api/projects/create', {
        projectID: newProjId,
        name: newProjName,
        description: newProjDesc,
      });
      if (ok) {
        alert('you made it big dog');
        navigate(`/hardware/${newProjId}`);
      }
      else {
        alert('SIKE!!! NO PROJECT:: ' + data.error);
      }
    } catch (err) {
      console.error('Error creating project:', err);
      alert('An error occurred while creating the project (it is your fault)');
    }
  };

  const handleJoinProject = async (e) => {
    e.preventDefault();
    try {
      const { ok, data } = await post('/api/projects/login', {
        projectID: joinProjId,
      });
      if (ok) {
        navigate(`/hardware/${joinProjId}`);
      }
      else {
        alert('this doesnt exist...' + data.error);
      }
    } catch (err) {
      console.error('Error joining project:', err);
      alert('An error occurred while joining the project (it is your fault)');
    }
  };


  return (
    <Container className="py-4">
      <div className="d-flex justify-content-between align-items-center mb-4">
        <h2>Projects Dashboard</h2>
        <div className="d-flex align-items-center gap-2">
          <span className="text-muted">Signed in as {userId}</span>
          <Button variant="outline-secondary" size="sm" onClick={handleSignOut}>
            Sign Out
          </Button>
        </div>
      </div>

      <div className="row g-3">
        {/* CREATE PROJECT CARD */}
        <div className="col-md-6">
          <Card className="h-100 shadow-sm">
            <Card.Body>
              <Card.Title>Create New Project</Card.Title>
              <Form onSubmit={handleCreateProject} className="mt-3">
                <Form.Group className="mb-2">
                  <Form.Control 
                    type="text" placeholder="Project Name" required
                    value={newProjName} onChange={(e) => setNewProjName(e.target.value)}
                  />
                </Form.Group>
                <Form.Group className="mb-2">
                  <Form.Control 
                    type="text" placeholder="Description" required
                    value={newProjDesc} onChange={(e) => setNewProjDesc(e.target.value)}
                  />
                </Form.Group>
                <Form.Group className="mb-3">
                  <Form.Control 
                    type="text" placeholder="Project ID" required
                    value={newProjId} onChange={(e) => setNewProjId(e.target.value)}
                  />
                </Form.Group>
                <Button variant="primary" type="submit" className="w-100">
                  Create Project
                </Button>
              </Form>
            </Card.Body>
          </Card>
        </div>

        {/* JOIN PROJECT CARD */}
        <div className="col-md-6">
          <Card className="h-100 shadow-sm">
            <Card.Body>
              <Card.Title>Login to Existing Project</Card.Title>
              <Form onSubmit={handleJoinProject} className="mt-3">
                <Form.Group className="mb-3">
                  <Form.Control 
                    type="text" placeholder="Project ID" required
                    value={joinProjId} onChange={(e) => setJoinProjId(e.target.value)}
                  />
                </Form.Group>
                <Button variant="secondary" type="submit" className="w-100 mt-auto">
                  Enter Project
                </Button>
              </Form>
            </Card.Body>
          </Card>
        </div>
      </div>
    </Container>
  );
}
export default Projects;