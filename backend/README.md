# Flask API Documentation

This Flask server handles User Authentication, Project Management, and Hardware Resource Management.
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

## Hardware Resource Management

### View Hardware Status
Returns the capacity and available hardware units for all hardware sets.
- Endpoint: /api/hardware/status
- Method: GET
- Success (200): 
  {
    "HWSet1": { "capacity": "number", "available": "number" },
    "HWSet2": { "capacity": "number", "available": "number" }
  }

### Request Hardware
Checks whether the requested hardware is available.
- Endpoint: /api/hardware/request
- Method: POST
- Payload:
  {
    "hardware": "string",
    "quantity": "number"
  }
- Success (200):
  {
    "message": "Hardware available",
    "requested": "number",
    "available": "number"
  }
- Error (409): {"error": "Not enough hardware available"}

### Checkout Hardware
Allocates hardware units to a project.
- Endpoint: /api/hardware/checkout
- Method: POST
- Payload:
  {
    "projectID": "string",
    "hardware": "string",
    "quantity": "number"
  }
- Success (200):
  {
    "message": "Hardware checked out",
    "projectID": "string",
    "hardware": "string",
    "quantity": "number"
  }
- Error (409): {"error": "Not enough hardware available"}

### Check In Hardware
Returns hardware units back to the system.
- Endpoint: /api/hardware/checkin
- Method: POST
- Payload:
  {
    "projectID": "string",
    "hardware": "string",
    "quantity": "number"
  }
- Success (200):
  {
    "message": "Hardware checked in",
    "projectID": "string",
    "hardware": "string",
    "quantity": "number"
  }
- Error (400): {"error": "Trying to return more than allocated"}

### View Project Hardware Allocations
Returns the hardware currently allocated to a project.
- Endpoint: /api/hardware/allocations/<projectID>
- Method: GET
- Success (200):
  {
    "projectID": "string",
    "allocations": {
      "HWSet1": "number",
      "HWSet2": "number"
    }
  }

## Developer TODOs (Database, Backend)
- Replace mock_users dictionary with MongoDB users collection.
- Replace mock_projects dictionary with MongoDB projects collection.
- Replace mock_hardware dictionary with MongoDB hardware collection.
- Replace mock_allocations dictionary with MongoDB allocation records.
- Implement bcrypt for password hashing.