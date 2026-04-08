from flask import Flask, request, jsonify
from flask_cors import CORS
import database
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, InvalidHash

import subprocess
import base64
import tempfile

from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

# 🔐 Session key (temporary storage)
SESSION_KEY = None

app = Flask(__name__)
CORS(app)

# 🔐 Password hasher
ph = PasswordHasher()

# ✅ DB CONNECTION (ONLY ONCE)
cluster = database.setup_database()

# user DB
db = database.access_db(cluster)
users = database.access_users(db)

# project DB
project_db = database.access_projects_db(cluster)
projects = database.access_projects(project_db)

# hardware DB
hardware_collection = db["hardware"]
allocations_collection = db["allocations"]


# =========================
# RSA DECRYPT (OpenSSL)
# =========================
def decrypt_with_openssl(encrypted_b64):
    encrypted_bytes = base64.b64decode(encrypted_b64)

    with tempfile.NamedTemporaryFile(delete=False) as enc_file:
        enc_file.write(encrypted_bytes)
        enc_path = enc_file.name

    with tempfile.NamedTemporaryFile(delete=False) as out_file:
        out_path = out_file.name

    cmd = [
        "openssl", "pkeyutl",
        "-decrypt",
        "-inkey", "private.pem",
        "-in", enc_path,
        "-out", out_path,
        "-pkeyopt", "rsa_padding_mode:oaep"
    ]

    subprocess.run(cmd, check=True)

    with open(out_path, "rb") as f:
        return f.read().decode()


# =========================
# AES DECRYPT (SESSION KEY)
# =========================
def decrypt_with_aes(encrypted_b64, key):
    encrypted_bytes = base64.b64decode(encrypted_b64)

    iv = encrypted_bytes[:16]
    ciphertext = encrypted_bytes[16:]

    cipher = AES.new(key.encode(), AES.MODE_CBC, iv)
    decrypted = unpad(cipher.decrypt(ciphertext), AES.block_size)

    return decrypted.decode()


# =========================
# PUBLIC KEY
# =========================
@app.route("/api/public-key", methods=["GET"])
def get_public_key():
    with open("public.pem", "r") as f:
        return jsonify(public_key=f.read())


# =========================
# KEY EXCHANGE (RSA → AES)
# =========================
@app.route("/api/key-exchange", methods=["POST"])
def key_exchange():
    global SESSION_KEY

    data = request.json
    encrypted_key = data.get("key")

    if not encrypted_key:
        return jsonify(error="Missing key"), 400

    try:
        session_key = decrypt_with_openssl(encrypted_key)
    except:
        return jsonify(error="Key decryption failed"), 500

    # Ensure valid AES key length (32 bytes)
    SESSION_KEY = session_key[:32]

    return jsonify(message="Key exchange successful"), 200


# =========================
# USER AUTHENTICATION
# =========================
@app.route("/api/signup", methods=["POST"])
def signup():
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
    global SESSION_KEY

    data = request.json
    userId = data.get("userId")
    encrypted_password = data.get("password")

    if not userId or not encrypted_password:
        return jsonify(error="Missing fields"), 400

    if not SESSION_KEY:
        return jsonify(error="Session key not established"), 400

    try:
        password = decrypt_with_aes(encrypted_password, SESSION_KEY)
    except:
        return jsonify(error="AES decryption failed"), 500

    user = users.find_one({"username": userId})
    stored_password_hash = user["password"] if user else None

    if not stored_password_hash:
        return jsonify(error="User not found"), 404

    try:
        ph.verify(stored_password_hash, password)
    except VerifyMismatchError:
        return jsonify(error="Incorrect password"), 401
    except InvalidHash:
        return jsonify(error="Invalid hash"), 500

    return jsonify(userId=userId, token="demo-token-" + userId), 200


# =========================
# PROJECT MANAGEMENT
# =========================
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

    projects.insert_one({
        "project_id": p_id,
        "project_name": p_name,
        "project_description": p_desc
    })

    return jsonify(message="Project created successfully", projectID=p_id), 201


@app.route("/api/projects/login", methods=["POST"])
def login_project():
    data = request.json
    p_id = data.get("projectID")

    project = projects.find_one({"project_id": p_id})

    if not project:
        return jsonify(error="Project not found"), 404

    return jsonify(
        message="Logged into project",
        projectID=p_id
    ), 200


# =========================
# HARDWARE MANAGEMENT
# =========================
def parse_request(data):
    project_id = data.get("projectID")
    hw = data.get("hardware")
    qty = data.get("quantity", 0)

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


@app.route("/api/hardware/status", methods=["GET"])
def hardware_status():
    hardware = list(hardware_collection.find({}, {"_id": 0}))
    return jsonify(hardware=hardware), 200


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


@app.route("/api/hardware/checkout", methods=["POST"])
def checkout_hardware():
    data = request.json
    project_id, hw, qty, err, code = parse_request(data)
    if err:
        return err, code

    proj_check = validate_project(project_id)
    if proj_check:
        return proj_check

    hw_doc = hardware_collection.find_one({"hardware_set": hw})

    if not hw_doc:
        return jsonify(error="Hardware not found"), 404

    if hw_doc["availability"] < qty:
        return jsonify(error="Not enough hardware"), 409

    hardware_collection.update_one(
        {"hardware_set": hw, "availability": {"$gte": qty}},
        {"$inc": {"availability": -qty}}
    )

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


@app.route("/api/hardware/checkin", methods=["POST"])
def checkin_hardware():
    data = request.json
    project_id, hw, qty, err, code = parse_request(data)
    if err:
        return err, code

    alloc_doc = allocations_collection.find_one({"project_id": project_id})

    if not alloc_doc or alloc_doc.get("hardware", {}).get(hw, 0) < qty:
        return jsonify(error="Returning more than allocated"), 400

    allocations_collection.update_one(
        {"project_id": project_id},
        {"$inc": {f"hardware.{hw}": -qty}}
    )

    hardware_collection.update_one(
        {"hardware_set": hw},
        {"$inc": {"availability": qty}}
    )

    return jsonify(
        message="Checked in",
        projectID=project_id,
        hardware=hw,
        quantity=qty
    ), 200


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


if __name__ == "__main__":
    print("Running server...")
    app.run(port=5000, debug=True)