from flask import Flask, request, jsonify
from flask_cors import CORS
import database
from pymongo import MongoClient
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, InvalidHash

app = Flask(__name__)
CORS(app)
ph = PasswordHasher()
cluster = database.setup_database()
db = database.access_db(cluster)
users = database.access_users(db)

project_db = database.access_projects_db(cluster)
projects = database.access_projects(project_db)

# USER AUTHENTICATION
@app.route("/api/signup", methods=["POST"])
def signup():
    # TODO: replace with real database insertion
    data = request.json
    userId = data.get("userId")
    password = data.get("password")

    if not userId or not password:
        return jsonify(error="Missing fields"), 400

    if users.find_one({"username": userId}):
        return jsonify(error="User already exists"), 409
    
    hashed_password = ph.hash(password)

    users.insert_one({"username": userId, "password": hashed_password})
    return jsonify(message="User created"), 201

@app.route("/api/signin", methods=["POST"])
def signin():
    data = request.json
    userId = data.get("userId")
    password = data.get("password")


    # TODO: replace with real database lookup
    user = users.find_one({"username": userId})
    stored_password_hash = user["password"] if user else None
    
    if not stored_password_hash:
        return jsonify(error="User not found"), 404
    
    try:
        ph.verify(stored_password_hash, password)
    except VerifyMismatchError:
        return jsonify(error="Incorrect password"), 401 
    except InvalidHash:
        return jsonify(error= "Incorrect Hash"), 401

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

    if projects.find_one({"project_id": p_id}):
        return jsonify(error="Project ID already exists"), 409

    # Save to our mock project database
    # TODO: replace with real database insertion
    projects.insert_one({"project_id": p_id, "project_name": p_name, "project_description": p_desc})
    
    return jsonify(message="Project created successfully", projectID=p_id), 201

@app.route("/api/projects/login", methods=["POST"])
def login_project():
    """Allows a user to 'enter' a project by its ID"""
    data = request.json
    p_id = data.get("projectID")


    # TODO: replace with real database lookup
    project = projects.find_one({"project_id": p_id})
    
    if not project:
        return jsonify(error="Project not found"), 404

    # Return the project details to the user
    return jsonify(
        message="Logged into project",
        projectID=p_id,
    ), 200

# RESOURCE MANAGEMENT

@app.route("/api/hardware/<project_id>", methods=["GET"])
def get_hardware(project_id):
    """Fetches the current hardware status for a given project."""
    project = projects.find_one({"project_id": project_id})
    
    if not project:
        return jsonify(error="Project not found"), 404
        
    hardware = project.get("hardware", {
        "HWSet1": {"capacity": 100, "available": 100},
        "HWSet2": {"capacity": 100, "available": 100},
        "HWSet3": {"capacity": 100, "available": 100},
        "HWSet4": {"capacity": 100, "available": 100},
        "HWSet5": {"capacity": 100, "available": 100}
    })
    
    return jsonify(hardware=hardware), 200

@app.route("/api/hardware/checkout", methods=["POST"])
def checkout_hardware():
    data = request.json
    p_id = data.get("projectID")
    hw_set = data.get("hwSet")
    amount = int(data.get("amount", 0))

    if amount <= 0:
        return jsonify(error="Amount must be greater than 0"), 400

    #check current availability
    project = projects.find_one({"project_id": p_id})
    if not project:
        return jsonify(error="Project not found"), 404

    #current available amount
    current_available = project.get("hardware", {}).get(hw_set, {}).get("available", 100)

    if amount > current_available:
        return jsonify(error=f"Not enough {hw_set} available. Only {current_available} left."), 400

    #adjust the available amount in the database
    update_query = {
        "$inc": {f"hardware.{hw_set}.available": -amount}
    }
    #ensure capacity
    projects.update_one({"project_id": p_id}, update_query)

    return jsonify(message=f"Successfully checked out {amount} of {hw_set}"), 200

@app.route("/api/hardware/checkin", methods=["POST"])
def checkin_hardware():
    data = request.json
    p_id = data.get("projectID")
    hw_set = data.get("hwSet")
    amount = int(data.get("amount", 0))

    if amount <= 0:
        return jsonify(error="Amount must be greater than 0"), 400

    project = projects.find_one({"project_id": p_id})
    if not project:
        return jsonify(error="Project not found"), 404

    current_data = project.get("hardware", {}).get(hw_set, {"capacity": 100, "available": 100})
    current_available = current_data.get("available")
    capacity = current_data.get("capacity")

    if (current_available + amount) > capacity:
        return jsonify(error=f"Cannot return more than capacity ({capacity})."), 400

    #increment available amount in the database
    update_query = {
        "$inc": {f"hardware.{hw_set}.available": amount}
    }
    projects.update_one({"project_id": p_id}, update_query)

    return jsonify(message=f"Successfully checked in {amount} of {hw_set}"), 200
if __name__ == "__main__":
    print("Running with mock database for Users and Projects")
    app.run(port=5000, debug=True)