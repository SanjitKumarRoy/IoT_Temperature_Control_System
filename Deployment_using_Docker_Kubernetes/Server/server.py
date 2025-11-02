from flask import Flask, request, jsonify
import requests
app = Flask(__name__)

TARGET_TEMPERATURE = 20.0
DATA_SERVICE_ADDRESS = "http://127.0.0.1:5001/history"

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<h1>IoT based Room Temperature Controller</h1>
<body><h2>Here we can see the current temperature <br> and also can reset the temperature</h2></body>
</html>
"""


@app.route('/')
def get_index_page():
    return HTML_TEMPLATE

@app.route('/sensor_log')
def get_sensor_log():
    try:
        number_or_items = 10
        response = requests.get(DATA_SERVICE_ADDRESS, params={"number_of_items": number_or_items})
        data = response.json()
        return jsonify({"Status":"Success", "data":data})
    except requests.exceptions.RequestException as e:
        print(f"Could not connect to {DATA_SERVICE_ADDRESS}: {e}")
    return {"Status":"Failed", "Message":"Could not retrieve sensor log"}

@app.route('/status')
def send_status():
    return jsonify({"target_value":TARGET_TEMPERATURE})

@app.route('/target_temperature', methods=['PATCH'])
def get_target_temperature():
    global TARGET_TEMPERATURE
    value = request.get_json()
    if value is None:
        return jsonify({"Status":"Error!"})
    else:
        key = list(value.keys())[0]
        TARGET_TEMPERATURE = float(value[key])
    return jsonify({"Status":"Success"})

if __name__ == '__main__':
    app.run(debug=True, host="127.0.0.1", port=5000)
