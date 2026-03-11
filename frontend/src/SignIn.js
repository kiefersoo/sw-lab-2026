import React, { useState } from 'react';
import { Card, Container, Form, Button } from 'react-bootstrap';
import { useNavigate } from "react-router-dom";
import { post, setAuth } from "./api";

function SignIn() {
    const [userId, setUserId] = useState('');
    const [password, setPassword] = useState('');

    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();

        try {
            const { ok, data } = await post("/api/signin", { userId, password });

            if (ok) {
                setAuth(data.userId, data.token);
                navigate('/projects');
            } else {
                alert(data.error ? `Error: ${data.error}` : 'Sign in failed');
            }
        } catch (err) {
            console.error("Connection error:", err);
            alert("Could not connect to the server.");
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
                        <Button 
                            variant="link" 
                            className="p-0 ms-2"
                            onClick={() => navigate("/create-user")}
                        >
                            you should make one..
                        </Button>
                    </div>
                </Form>
            </Card>
        </Container>
    );
}

export default SignIn;
