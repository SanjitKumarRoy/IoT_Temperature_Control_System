import requests
from flask import Flask, jsonify, request
from flask_cors import CORS

# This service manages the system's state, including the target temperature (setpoint).
# It communicates with the Data Service to get the most recent temperature reading.

app = Flask(__name__)
CORS(app)

# URL for the Data Service
DATA_SERVICE_URL = "http://127.0.0.1:5001/data"

# In-memory state for the target temperature. Default is 21°C.
system_state = {
    "target_temperature": 21.0
}

@app.route('/state', methods=['GET'])
def get_state():
    """
    Returns the complete current state of the system, including
    the latest temperature and the target temperature.
    """
    latest_temp = None
    try:
        # Fetch all data from the data service
        response = requests.get(DATA_SERVICE_URL)
        response.raise_for_status()  # Raise an exception for bad status codes
        all_data = response.json()
        # The latest temperature is the first item if the list is not empty
        if all_data:
            latest_temp = all_data[0].get('temperature')
    except requests.exceptions.RequestException as e:
        print(f"Control Service: Could not connect to Data Service: {e}")
    except (ValueError, IndexError):
        print("Control Service: Could not parse data or no data available.")
        
    # Combine the latest known temperature with the target temperature
    full_state = {
        "current_temperature": latest_temp,
        "target_temperature": system_state["target_temperature"]
    }
    return jsonify(full_state)

@app.route('/setpoint', methods=['POST'])
def set_target_temperature():
    """
    Sets a new target temperature (setpoint).
    """
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    data = request.get_json()
    new_temp = data.get('temperature')

    if new_temp is None:
        return jsonify({"error": "Missing 'temperature' in request"}), 400

    try:
        system_state["target_temperature"] = float(new_temp)
        print(f"Control Service: New target temperature set to {system_state['target_temperature']}°C")
        return jsonify({
            "message": "Target temperature updated",
            "new_target": system_state["target_temperature"]
        })
    except ValueError:
        return jsonify({"error": "Invalid temperature format"}), 400

if __name__ == '__main__':
    # This service runs on port 5002
    app.run(host='0.0.0.0', port=5002, debug=True)

