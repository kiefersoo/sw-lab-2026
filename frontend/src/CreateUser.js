import React, { useState } from 'react';
import { Card, Container, Form, Button } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';
import { post } from './api';

function CreateUser() {
    const [userId, setUserId] = useState('');
    const [password, setPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();

        if (password !== confirmPassword) {
            alert("Passwords do not match!");
            return;
        }

        try {
            const { ok, data } = await post("/api/signup", { userId, password });

            if (ok) {
                alert("Account created successfully!");
                navigate("/");
            } else {
                alert(data.error ? `Error: ${data.error}` : 'Signup failed');
            }
        } catch (err) {
            console.error("Connection error:", err);
            alert("Could not connect to the server.");
        }
    };

    return (
        <Container className="d-flex justify-content-center align-items-center" style={{ height: '100vh' }}>
            <Card style={{ width: '400px', padding: '20px' }} className="shadow">
                <h2 className="text-center mb-4">Create Account</h2>

                <Form onSubmit={handleSubmit}>

                    <Form.Group className="mb-3" controlId="formUserId">
                        <Form.Label>User ID</Form.Label>
                        <Form.Control
                            type="text"
                            placeholder="Choose a User ID"
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

                    <Form.Group className="mb-3" controlId="formConfirmPassword">
                        <Form.Label>Confirm Password</Form.Label>
                        <Form.Control
                            type="password"
                            placeholder="Confirm Password"
                            value={confirmPassword}
                            onChange={(e) => setConfirmPassword(e.target.value)}
                            required
                        />
                    </Form.Group>

                    <Button variant="success" type="submit" className="w-100">
                        Create Account
                    </Button>

                    <div className="text-center mt-3">
                        <span>Already have an account?</span>
                        <Button
                            variant="link"
                            className="p-0 ms-2"
                            onClick={() => navigate("/")}
                        >
                            Sign In
                        </Button>
                    </div>
                </Form>
            </Card>
        </Container>
    );
}

export default CreateUser;