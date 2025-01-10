from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Hardcoded credentials for demonstration
VALID_USERNAME = "admin"
VALID_PASSWORD = "password"

# In-memory storage for sessions and connected PCs
sessions = {}
connected_pcs = {}

# Login route
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if username == VALID_USERNAME and password == VALID_PASSWORD:
        # Generate a session token (for demonstration purposes)
        session_token = "session_" + username
        sessions[session_token] = username
        return jsonify({"success": True, "session_token": session_token})
    else:
        return jsonify({"success": False}), 401

# Route for PCs to register themselves
@app.route("/register_pc", methods=["POST"])
def register_pc():
    data = request.get_json()
    session_token = data.get("session_token")
    pc_id = data.get("pc_id")  # Unique identifier for the PC

    if session_token in sessions:
        connected_pcs[session_token] = pc_id
        return jsonify({"success": True})
    else:
        return jsonify({"success": False}), 401

# Route to send commands to the PC
@app.route("/send_command", methods=["POST"])
def send_command():
    data = request.get_json()
    session_token = data.get("session_token")
    command = data.get("command")

    if session_token in sessions:
        pc_id = connected_pcs.get(session_token)
        if pc_id:
            # Send the command to the PC (implementation depends on how PCs are identified)
            print(f"Sending command '{command}' to PC {pc_id}")
            return jsonify({"success": True, "message": f"Command '{command}' sent to PC {pc_id}"})
        else:
            return jsonify({"success": False, "message": "PC not connected"}), 404
    else:
        return jsonify({"success": False}), 401

# Route to serve the login page
@app.route("/")
def index():
    return render_template("login.html")

# Route to serve the program page
@app.route("/program")
def program():
    return render_template("program.html")

# Run the Flask app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
