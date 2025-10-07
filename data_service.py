import datetime
from flask import Flask, jsonify, request
from flask_cors import CORS

# This service is the single source of truth for historical temperature data.
# In a real-world application, this would be connected to a time-series database.

app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing

# Use a simple in-memory list to store data for this example.
temperature_data_store = []

@app.route('/data', methods=['GET', 'POST'])
def handle_data():
    """
    Handles storing and retrieving temperature data.
    - POST: Receives a new temperature reading from the IoT device.
    - GET: Returns the entire history of temperature readings.
    """
    if request.method == 'POST':
        # Check if the request has a JSON body
        if not request.is_json:
            return jsonify({"error": "Request must be JSON"}), 400

        data = request.get_json()
        temp = data.get('temperature')

        if temp is None:
            return jsonify({"error": "Missing 'temperature' in request"}), 400

        # Create a new record with a timestamp
        record = {
            "temperature": float(temp),
            "timestamp": datetime.datetime.utcnow().isoformat() + 'Z'
        }
        temperature_data_store.append(record)
        print(f"Data Service: Received new temperature reading: {record['temperature']}°C")

        return jsonify({"message": "Data received successfully"}), 201

    elif request.method == 'GET':
        # Return all stored data, sorted with the newest first
        sorted_data = sorted(temperature_data_store, key=lambda x: x['timestamp'], reverse=True)
        return jsonify(sorted_data)

if __name__ == '__main__':
    # This service runs on port 5001
    app.run(host='0.0.0.0', port=5001, debug=True)

