from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Mock Database - will reset every time you restart the Flask server
mock_users = {} 

@app.route("/api/signup", methods=["POST"])
def signup():
    data = request.json
    userId = data.get("userId")
    password = data.get("password")

    if not userId or not password:
        return jsonify(error="Missing fields"), 400

    # Check if user exists in our dictionary
    if userId in mock_users:
        return jsonify(error="User already exists"), 409

    # Save to dictionary instead of MongoDB
    mock_users[userId] = password

    return jsonify(message="User created"), 201


@app.route("/api/signin", methods=["POST"])
def signin():
    data = request.json
    userId = data.get("userId")
    password = data.get("password")

    # Look up user in dictionary
    stored_password = mock_users.get(userId)
    
    if not stored_password:
        return jsonify(error="User not found"), 404

    # Simple password check, no encryption for demo purposes
    if password != stored_password:
        return jsonify(error="Incorrect password"), 401

    # Dummy token for lab demo
    token = "demo-token-" + userId
    return jsonify(userId=userId, token=token), 200


if __name__ == "__main__":
    print("Running with mock database")
    app.run(port=5000, debug=True)
