import React, { useState } from 'react';
import { Card, Container, Form, Button } from 'react-bootstrap';

function CreateUser() {
    const [userId, setUserId] = useState('');
    const [password, setPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();

        // Simple frontend validation
        if (password !== confirmPassword) {
            alert("Passwords do not match!");
            return;
        }

        const newUser = { userId, password };

        try {
            const response = await fetch("http://localhost:5000/api/signup", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(newUser),
            });

            const data = await response.json();

            if (response.ok) {
                alert("Account created successfully!");
                console.log("User created:", data);

                // Optional: redirect to sign-in page
                window.location.href = "/";
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
                            onClick={() => window.location.href = "/"}
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