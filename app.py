from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Hardcoded credentials for demonstration
VALID_USERNAME = "admin"
VALID_PASSWORD = "password"

# In-memory storage for sessions, connected PCs, and serial_info
sessions = {}
connected_pcs = {}
pc_serial_info = {}  # Store serial_info for each PC

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
        return jsonify({"success": True, "session_token": session_token, "username": username})
    else:
        return jsonify({"success": False}), 401

# Route for PCs to register themselves
@app.route("/register_pc", methods=["POST"])
def register_pc():
    data = request.get_json()
    session_token = data.get("session_token")
    pc_id = data.get("pc_id")  # Unique identifier for the PC
    serial_info = data.get("serial_info")  # Get serial_info from the request

    if session_token in sessions:
        connected_pcs[session_token] = pc_id
        pc_serial_info[pc_id] = serial_info  # Store serial_info for the PC
        return jsonify({"success": True})
    else:
        return jsonify({"success": False}), 401

# Route to send commands to the PC
@app.route("/send_command", methods=["POST"])
def send_command():
    data = request.get_json()
    session_token = data.get("session_token")
    command = data.get("command")

    # Check if the session token is valid
    if session_token not in sessions:
        return jsonify({"success": False, "message": "Unauthorized: Invalid session token"}), 401

    # Get the PC ID associated with the session token
    pc_id = connected_pcs.get(session_token)
    if not pc_id:
        return jsonify({"success": False, "message": "PC not connected"}), 404

    # Send the command to the PC (implementation depends on how PCs are identified)
    print(f"Sending command '{command}' to PC {pc_id}")
    return jsonify({"success": True, "message": f"Command '{command}' sent to PC {pc_id}"})

# Route to check for commands
@app.route("/check_commands", methods=["POST"])
def check_commands():
    data = request.get_json()
    session_token = data.get("session_token")
    pc_id = data.get("pc_id")

    # Validate session token
    if session_token not in sessions:
        return jsonify({"success": False, "message": "Unauthorized: Invalid session token"}), 401

    # Simulate a command (replace with your logic)
    command = None  # Replace with logic to fetch a command for the PC
    return jsonify({"success": True, "command": command})

# Route to serve the login page
@app.route("/")
def index():
    return render_template("login.html")

# Route to serve the program page
@app.route("/program")
def program():
    # Retrieve session token from query parameters
    session_token = request.args.get("session_token")
    if session_token in sessions:
        username = sessions[session_token]  # Get username from sessions
        pc_id = connected_pcs.get(session_token)  # Get PC ID
        serial_info = pc_serial_info.get(pc_id, {})  # Get serial_info for the PC
        return render_template("program.html", username=username, serial_info=serial_info)
    else:
        return redirect(url_for("index"))  # Redirect to login if session is invalid

# Run the Flask app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
