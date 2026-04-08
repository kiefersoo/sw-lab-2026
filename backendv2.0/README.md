# Flask API Documentation

This Flask server handles User Authentication and Project Management. 
Note: The server currently uses an in-memory Mock Database. Data will reset on server restart.

## Getting Started

- Base URL: http://localhost:5000
- Content-Type: All requests must include header: {"Content-Type": "application/json"}
- Body Format: All data must be sent as a JSON string (JSON.stringify(data))

## User Authentication

### Sign Up (New User)
Registers a new user ID and password.
- Endpoint: /api/signup
- Method: POST
- Payload: 
  {
    "userId": "string",
    "password": "string"
  }
- Success (201): {"message": "User created"}
- Error (409): {"error": "User already exists"}

### Sign In
Authenticates user and returns a dummy session token.
- Endpoint: /api/signin
- Method: POST
- Payload: 
  {
    "userId": "string",
    "password": "string"
  }
- Success (200): {"userId": "string", "token": "string"}
- Error (401/404): {"error": "string"}

## Project Management

### Create New Project
Adds a new project to the system.
- Endpoint: /api/projects/create
- Method: POST
- Payload: 
  {
    "projectID": "string",
    "name": "string",
    "description": "string"
  }
- Success (201): {"message": "Project created successfully", "projectID": "string"}
- Error (409): {"error": "Project ID already exists"}

### Login to Project
Retrieves existing project data by ID.
- Endpoint: /api/projects/login
- Method: POST
- Payload: 
  {
    "projectID": "string"
  }
- Success (200): 
  {
    "message": "Logged into project",
    "projectID": "string",
    "details": { "name": "string", "description": "string" }
  }
- Error (404): {"error": "Project not found"}

## Developer TODOs (Database, Backend)
- Replace mock_users dictionary with MongoDB users collection.
- Replace mock_projects dictionary with MongoDB projects collection.
- Implement bcrypt for password hashing.