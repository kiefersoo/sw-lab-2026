import React, { useState, useEffect } from 'react';
import { Container, Card, Button, Form, Row, Col, Alert } from 'react-bootstrap';
import { useNavigate, useParams } from 'react-router-dom';
import { getUserId, post, get } from './api';

function HardwareManager() {
    const { projId } = useParams();
    const navigate = useNavigate();
    //state for hardware list fetched from backend
    const [hardwareList, setHardwareList] = useState([]);

    //input field states keyed by hardware name for easy access
    const [inputs, setInputs] = useState({});
    const [error, setError] = useState(null);

    const fetchHardwareData = async () => {
        try {
            const response = await get('/api/hardware/status');
            if (response && response.hardware) {
                setHardwareList(response.hardware);
                setError(null);
            }
        } catch (err) {
            console.error("Failed to fetch hardware data:", err);
            setError("Could not load hardware status.");
        }
    };

    useEffect(() => {
        fetchHardwareData();
    }, [projId]);

    const handleInputChange = (name, value) => {
        setInputs(prev => ({ ...prev, [name]: value }));
    };

    const handleAction = async (actionType, hwName) => {
        const amount = parseInt(inputs[hwName], 10);
        
        if (!amount || amount <= 0) {
            alert("Please enter a valid amount greater than 0.");
            return;
        }

        const endpoint = actionType === 'checkout' ? '/api/hardware/checkout' : '/api/hardware/checkin';

        try {
            const response = await post(endpoint, {
                projectID: projId,
                hardware: hwName, // Backend expects "hardware" key based on parse_request()
                quantity: amount   // Backend expects "quantity" key
            });

            if (response.error) {
                alert(response.error);
            } else {
                // Refresh data and clear specific input
                fetchHardwareData();
                handleInputChange(hwName, ""); 
            }
        } catch (err) {
            console.error(`${actionType} failed:`, err);
            alert("Transaction failed. Check console.");
        }
    };

    return (
        <Container className="py-4">
            <div className="d-flex justify-content-between align-items-center mb-4">
                <h2>Project: {projId}</h2>
                <Button variant="outline-primary" size="sm" onClick={() => navigate('/projects')}>
                    Back to Projects
                </Button>
            </div>

            {error && <Alert variant="danger">{error}</Alert>}

            <Card className="shadow-sm">
                <Card.Body>
                    <Row className="mb-3 fw-bold border-bottom pb-2">
                        <Col xs={3}>Hardware Set</Col>
                        <Col>Capacity</Col>
                        <Col>Available</Col>
                        <Col xs={3}>Request Amount</Col>
                        <Col xs={3}>Actions</Col>
                    </Row>

                    {hardwareList.map((hw) => (
                        <Row key={hw.name} className="align-items-center mb-3 border-bottom pb-3">
                            <Col xs={3}><strong>{hw.name}</strong></Col>
                            <Col>{hw.capacity || (hw.available + hw.checked_out)}</Col>
                            <Col>{hw.available}</Col>
                            <Col xs={3}>
                                <Form.Control 
                                    type="number" 
                                    placeholder="0"
                                    value={inputs[hw.name] || ""} 
                                    onChange={(e) => handleInputChange(hw.name, e.target.value)} 
                                />
                            </Col>
                            <Col xs={3} className="d-flex gap-2">
                                <Button 
                                    variant="success" 
                                    className="flex-grow-1"
                                    onClick={() => handleAction('checkin', hw.name)}
                                >
                                    Check In
                                </Button>
                                <Button 
                                    variant="warning" 
                                    className="flex-grow-1"
                                    onClick={() => handleAction('checkout', hw.name)}
                                >
                                    Check Out
                                </Button>
                            </Col>
                        </Row>
                    ))}

                    {hardwareList.length === 0 && !error && (
                        <div className="text-center py-3">No hardware sets found in database.</div>
                    )}
                </Card.Body>
            </Card>
        </Container>
    );
}

export default HardwareManager;