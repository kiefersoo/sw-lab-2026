from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Mock Databases - These reset when the server restarts
mock_users = {
    "user1": "password1",
    "user2": "password2"
}

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

    mock_users[userId] = password
    return jsonify(message="User created"), 201

@app.route("/api/signin", methods=["POST"])
def signin():
    data = request.json
    userId = data.get("userId")
    password = data.get("password")

    # TODO: replace with real database lookup
    stored_password = mock_users.get(userId)
    
    if not stored_password:
        return jsonify(error="User not found"), 404

    if password != stored_password:
        return jsonify(error="Incorrect password"), 401

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


# HARDWARE RESOURCE MANAGEMENT

# Mock hardware database
# capacity = total hardware in system
# available = currently unused hardware

mock_hardware = {
    "HWSet1": {
        "capacity": 10,
        "available": 10
    },
    "HWSet2": {
        "capacity": 8,
        "available": 8
    }
}

# Track allocations per project
# { projectID : {HWSet1: qty, HWSet2: qty}}
mock_allocations = {}


# Get Hardware Status
@app.route("/api/hardware/status", methods=["GET"])
def hardware_status():
    """Return capacity and availability of all hardware sets"""
    return jsonify(mock_hardware), 200


# Request Hardware (Check Availability)
@app.route("/api/hardware/request", methods=["POST"])
def request_hardware():
    data = request.json
    hw_name = data.get("hardware")
    quantity = data.get("quantity", 0)

    hw = mock_hardware.get(hw_name)

    if not hw:
        return jsonify(error="Hardware set not found"), 404

    if quantity <= 0:
        return jsonify(error="Invalid quantity"), 400

    if hw["available"] >= quantity:
        return jsonify(
            message="Hardware available",
            requested=quantity,
            available=hw["available"]
        ), 200

    return jsonify(
        error="Not enough hardware available",
        available=hw["available"]
    ), 409


# Checkout Hardware
@app.route("/api/hardware/checkout", methods=["POST"])
def checkout_hardware():
    data = request.json
    project_id = data.get("projectID")
    hw_name = data.get("hardware")
    quantity = data.get("quantity", 0)

    hw = mock_hardware.get(hw_name)

    if not hw:
        return jsonify(error="Hardware set not found"), 404

    if quantity <= 0:
        return jsonify(error="Invalid quantity"), 400

    if hw["available"] < quantity:
        return jsonify(error="Not enough hardware available"), 409

    # reduce availability
    hw["available"] -= quantity

    # track allocation
    if project_id not in mock_allocations:
        mock_allocations[project_id] = {}

    mock_allocations[project_id][hw_name] = \
        mock_allocations[project_id].get(hw_name, 0) + quantity

    return jsonify(
        message="Hardware checked out",
        projectID=project_id,
        hardware=hw_name,
        quantity=quantity
    ), 200


# Check-in Hardware
@app.route("/api/hardware/checkin", methods=["POST"])
def checkin_hardware():
    data = request.json
    project_id = data.get("projectID")
    hw_name = data.get("hardware")
    quantity = data.get("quantity", 0)

    if project_id not in mock_allocations:
        return jsonify(error="Project has no allocations"), 404

    allocated = mock_allocations[project_id].get(hw_name, 0)

    if quantity <= 0:
        return jsonify(error="Invalid quantity"), 400

    if allocated < quantity:
        return jsonify(error="Trying to return more than allocated"), 400

    # update allocation
    mock_allocations[project_id][hw_name] -= quantity

    # update hardware availability
    mock_hardware[hw_name]["available"] += quantity

    return jsonify(
        message="Hardware checked in",
        projectID=project_id,
        hardware=hw_name,
        quantity=quantity
    ), 200


# View Project Allocations
@app.route("/api/hardware/allocations/<project_id>", methods=["GET"])
def get_allocations(project_id):
    allocations = mock_allocations.get(project_id, {})
    return jsonify(projectID=project_id, allocations=allocations), 200


if __name__ == "__main__":
    print("Running with mock database for Users and Projects")
    app.run(port=5000, debug=True)