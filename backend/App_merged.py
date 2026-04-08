from flask import Flask, request, jsonify
from flask_cors import CORS
import database
from pymongo import MongoClient
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, InvalidHash
import os
from dotenv import load_dotenv
from flask import send_from_directory

app = Flask(__name__, static_folder="build", static_url_path="/")
CORS(app)
ph = PasswordHasher()
cluster = database.setup_database()
db = database.access_db(cluster)
users = database.access_users(db)

project_db = database.access_projects_db(cluster)
projects = database.access_projects(project_db)
hardware_db = database.access_hardware_db(cluster)
hardware_collection = database.access_hardware(hardware_db)
allocations_collection = hardware_db["allocations"]
load_dotenv(".gitignore/.env")
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

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


# HARDWARE RESOURCE MANAGEMENT


# HELPERS
def parse_request(data):
    project_id = data.get("projectID")
    hw = data.get("hardware") or data.get("hwSet")
    qty = data.get("quantity", data.get("amount", 0))

    try:
        qty = int(qty)
    except:
        return None, None, None, jsonify(error="Quantity must be integer"), 400

    return project_id, hw, qty, None, None


def validate_project(project_id):
    if not project_id:
        return jsonify(error="Project ID required"), 400

    if not projects.find_one({"project_id": project_id}):
        return jsonify(error="Project not found"), 404

    return None


# STATUS (ALL HARDWARE)
@app.route("/api/hardware/status", methods=["GET"])
def hardware_status():
    hardware = list(hardware_collection.find({}, {"_id": 0}))
    return jsonify(hardware=hardware), 200


# REQUEST (CHECK ONLY)
@app.route("/api/hardware/request", methods=["POST"])
def request_hardware():
    data = request.json
    _, hw, qty, err, code = parse_request(data)
    if err:
        return err, code

    hw_doc = hardware_collection.find_one({"hardware_set": hw})
    if not hw_doc:
        return jsonify(error="Hardware not found"), 404

    if qty <= 0:
        return jsonify(error="Invalid quantity"), 400

    if hw_doc["availability"] >= qty:
        return jsonify(
            message="Available",
            requested=qty,
            available=hw_doc["availability"]
        ), 200

    return jsonify(
        error="Not enough hardware",
        available=hw_doc["availability"]
    ), 409


# CHECKOUT
@app.route("/api/hardware/checkout", methods=["POST"])
def checkout_hardware():
    data = request.json
    project_id, hw, qty, err, code = parse_request(data)
    if err:
        return err, code

    proj_check = validate_project(project_id)
    if proj_check:
        return proj_check

    if qty <= 0:
        return jsonify(error="Invalid quantity"), 400

    hw_doc = hardware_collection.find_one({"hardware_set": hw})
    if not hw_doc:
        return jsonify(error="Hardware not found"), 404

    if hw_doc["availability"] < qty:
        return jsonify(error="Not enough hardware"), 409

    # atomic update (prevents race conditions)
    result = hardware_collection.update_one(
        {"hardware_set": hw, "availability": {"$gte": qty}},
        {
            "$inc": {
                "availability": -qty,
                "checked_out": qty
            }
        }
    )

    if result.modified_count == 0:
        return jsonify(error="Concurrent update failure"), 409

    # update allocations
    allocations_collection.update_one(
        {"project_id": project_id},
        {"$inc": {f"hardware.{hw}": qty}},
        upsert=True
    )

    return jsonify(
        message="Checked out",
        projectID=project_id,
        hardware=hw,
        quantity=qty
    ), 200


# CHECKIN
@app.route("/api/hardware/checkin", methods=["POST"])
def checkin_hardware():
    data = request.json
    project_id, hw, qty, err, code = parse_request(data)
    if err:
        return err, code

    if qty <= 0:
        return jsonify(error="Invalid quantity"), 400

    alloc_doc = allocations_collection.find_one({"project_id": project_id})

    if not alloc_doc or alloc_doc.get("hardware", {}).get(hw, 0) < qty:
        return jsonify(error="Returning more than allocated"), 400

    # update allocation
    allocations_collection.update_one(
        {"project_id": project_id},
        {"$inc": {f"hardware.{hw}": -qty}}
    )

    # update hardware
    hardware_collection.update_one(
        {"hardware_set": hw},
        {
            "$inc": {
                "availability": qty,
                "checked_out": -qty
            }
        }
    )

    return jsonify(
        message="Checked in",
        projectID=project_id,
        hardware=hw,
        quantity=qty
    ), 200


# VIEW PROJECT ALLOCATIONS
@app.route("/api/hardware/allocations/<project_id>", methods=["GET"])
def get_allocations(project_id):
    alloc = allocations_collection.find_one(
        {"project_id": project_id},
        {"_id": 0}
    )

    return jsonify(
        projectID=project_id,
        allocations=alloc.get("hardware", {}) if alloc else {}
    ), 200


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_react(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, "index.html")
    

if __name__ == "__main__":
    print("Running with mock database for Users and Projects")
    print("Running locally with mock database")
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)