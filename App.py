from flask import Flask, request, jsonify
from flask_cors import CORS
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, InvalidHash

app = Flask(__name__)
CORS(app)

# Initialize Argon2 password hasher
ph = PasswordHasher()

# Mock Databases - These reset when the server restarts
mock_users = {}

# Key: projectID, Value: {name, description}
mock_projects = {
    "proj101": {
        "name": "Alpha",
        "description": "First test project"}
}

# USER AUTHENTICATION
@app.route("/api/signup", methods=["POST"])
def signup():
    # TODO: replace with real database insertion
    data = request.json
    userId = data.get("userId")
    password = data.get("password")

    if not userId or not password:
        return jsonify(error="Missing fields"), 400

    if userId in mock_users:
        return jsonify(error="User already exists"), 409

    # Hash password using Argon2 before storing
    hashed_password = ph.hash(password)
    mock_users[userId] = hashed_password
    return jsonify(message="User created"), 201

@app.route("/api/signin", methods=["POST"])
def signin():
    data = request.json
    userId = data.get("userId")
    password = data.get("password")

    # TODO: replace with real database lookup
    stored_password_hash = mock_users.get(userId)
    
    if not stored_password_hash:
        return jsonify(error="User not found"), 404

    # Verify password using Argon2
    try:
        ph.verify(stored_password_hash, password)
    except VerifyMismatchError:
        return jsonify(error="Incorrect password"), 401
    except InvalidHash:
        return jsonify(error="Invalid password hash"), 500

    token = "demo-token-" + userId
    return jsonify(userId=userId, token=token), 200

# PROJECT MANAGEMENT
@app.route("/api/projects/create", methods=["POST"])
def create_project():
    data = request.json
    p_id = data.get("projectID")
    p_name = data.get("name")
    p_desc = data.get("description")

    if not p_id or not p_name:
        return jsonify(error="Project ID and Name are required"), 400

    if p_id in mock_projects:
        return jsonify(error="Project ID already exists"), 409

    # Save to our mock project database
    # TODO: replace with real database insertion
    mock_projects[p_id] = {
        "name": p_name,
        "description": p_desc
    }
    
    return jsonify(message="Project created successfully", projectID=p_id), 201

@app.route("/api/projects/login", methods=["POST"])
def login_project():
    """Allows a user to 'enter' a project by its ID"""
    data = request.json
    p_id = data.get("projectID")

    # TODO: replace with real database lookup
    project = mock_projects.get(p_id)
    
    if not project:
        return jsonify(error="Project not found"), 404

    # Return the project details to the user
    return jsonify(
        message="Logged into project",
        projectID=p_id,
        details=project
    ), 200

if __name__ == "__main__":
    print("Running with mock database for Users and Projects")
    app.run(port=5000, debug=True)