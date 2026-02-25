import React, { useState } from 'react';
import { Card, Container, Form, Button } from 'react-bootstrap';

function SignIn() {
    const [userId, setUserId] = useState('');
    const [password, setPassword] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault(); 
        
        const creds = {userId, password};

        try {
            const response = await fetch("http://localhost:5000/api/signin", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(creds),
            });

            const data = await response.json();

            if (response.ok) {
                alert(`Welcome, ${data.userId}! Token: ${data.token}`);
                console.log("Sign in successful:", data);
                // You could redirect here, e.g., window.location.href = '/dashboard';
            } else {
                alert(`Error: ${data.error}`);
            }
        } catch (error) {
            console.error("Connection error:", error);
            alert("Could not connect to the Flask server.");
        }
    };

    return (
        <Container className="d-flex justify-content-center align-items-center" style={{ height: '100vh' }}>
            <Card style={{ width: '400px' , padding: '20px' }} className="shadow">
                <h2 className="text-center mb-4">Team 7 Sign In</h2>
                <Form onSubmit={handleSubmit}>

                    <Form.Group className="mb-3" controlId="formUserId">
                        <Form.Label>User ID</Form.Label>
                        <Form.Control 
                            type="text" 
                            placeholder="Enter User ID"
                            value={userId}
                            onChange={(e) => setUserId(e.target.value)}
                            required
                        />
                    </Form.Group>

                    <Form.Group className="mb-3" controlId="formPassword">
                        <Form.Label>Password</Form.Label>
                        <Form.Control 
                            type="password" 
                            placeholder="Enter Password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            required
                        />
                    </Form.Group>

                    <Button variant="primary" type="submit" className="w-100">
                        Sign In
                    </Button>

                    <div className="text-center mt-3">
                        <span>No Account??</span>
                        {/* You can point this to your SignUp component later */}
                        <Button variant="link" className="p-0 ms-2">
                            you should make one..
                        </Button>
                    </div>
                </Form>
            </Card>
        </Container>
    );
}

export default SignIn;
