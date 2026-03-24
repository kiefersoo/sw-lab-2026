import React, { useState, useEffect } from 'react';
import { Container, Card, Button, Form, Row, Col } from 'react-bootstrap';
import { useNavigate, useParams } from 'react-router-dom';
import { getUserId, clearAuth, post, get } from './api';

function HardwareManager() {
    const { projId } = useParams();
    const navigate = useNavigate();
    const userId = getUserId();
    
    const [HW1, setHW1] = useState({ capacity: 100, available: 100});
    const [HW2, setHW2] = useState({ capacity: 100, available: 100});
    const [HW3, setHW3] = useState({ capacity: 100, available: 100});
    const [HW4, setHW4] = useState({ capacity: 100, available: 100});
    const [HW5, setHW5] = useState({ capacity: 100, available: 100});

    const [reqHW1, setReqHW1] = useState(0);
    const [reqHW2, setReqHW2] = useState(0);
    const [reqHW3, setReqHW3] = useState(0);
    const [reqHW4, setReqHW4] = useState(0);
    const [reqHW5, setReqHW5] = useState(0);

    const handleCheckout = async (HWSet, amnt) => {
        //flask here?
        alert(`Checking out ${amnt} of HW${HWSet}`);
    };
    const handleReturn = async (HWSet, amnt) => {
        //flask here?
        alert(`Returning ${amnt} of HW${HWSet}`);
    };

return (
    <Container className="py-4">
      <div className="d-flex justify-content-between align-items-center mb-4">
        <h2>Resource Management: {projId}</h2>
        <Button variant="outline-primary" size="sm" onClick={() => navigate('/projects')}>
          Back to Projects
        </Button>
      </div>

      <Card className="shadow-sm">
        <Card.Body>
          <Row className="mb-3 fw-bold border-bottom pb-2">
            <Col>Hardware Set</Col>
            <Col>Capacity</Col>
            <Col>Available</Col>
            <Col>Request Amount</Col>
            <Col>Actions</Col>
          </Row>

          {/* HWSet1 Row */}
          <Row className="align-items-center mb-3">
            <Col>HWSet1</Col>
            <Col>{HW1.capacity}</Col>
            <Col>{HW1.available}</Col>
            <Col>
              <Form.Control 
                type="number" min="0" value={reqHW1} 
                onChange={(e) => setReqHW1(e.target.value)} 
              />
            </Col>
            <Col className="d-flex gap-2">
              <Button variant="success" size="sm" onClick={() => handleReturn('HWSet1', reqHW1)}>Check In</Button>
              <Button variant="warning" size="sm" onClick={() => handleCheckout('HWSet1', reqHW1)}>Check Out</Button>
            </Col>
          </Row>

          {/* HWSet2 Row */}
          <Row className="align-items-center">
            <Col>HWSet2</Col>
            <Col>{HW2.capacity}</Col>
            <Col>{HW2.available}</Col>
            <Col>
              <Form.Control 
                type="number" min="0" value={reqHW2} 
                onChange={(e) => setReqHW2(e.target.value)} 
              />
            </Col>
            <Col className="d-flex gap-2">
              <Button variant="success" size="sm" onClick={() => handleReturn('HWSet2', reqHW2)}>Check In</Button>
              <Button variant="warning" size="sm" onClick={() => handleCheckout('HWSet2', reqHW2)}>Check Out</Button>
            </Col>
          </Row>

        </Card.Body>
      </Card>
    </Container>
  );
}

export default HardwareManager;