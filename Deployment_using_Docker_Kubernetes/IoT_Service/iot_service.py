import random
import time
from datetime import datetime
import requests
from flask import Flask

app = Flask(__name__)

SERVER_SERVICE_ADDRESS = "http://127.0.0.1:5000/status"
DATA_SERVICE_ADDRESS = "http://127.0.0.1:5001/sensor_data"
DEFAULT_TARGET_TEMPERATURE = 20.0

def get_status():
    try:
        response = requests.get(SERVER_SERVICE_ADDRESS)
        data = response.json()
        key = list(data.keys())[0]
        target_temperature = float(data[key])
        return target_temperature
    except requests.exceptions.RequestException as e:
        print(f"Could not connect to {SERVER_SERVICE_ADDRESS}: {e}")
    except Exception as e:
        print(f"Failed to parse status: {e}")
    return DEFAULT_TARGET_TEMPERATURE

def gen_sensor_data(target_temperature, current_temperature):
    random_number = random.uniform(0,0.4)
    drift = round(random_number, 2)
    if current_temperature > target_temperature:
        current_temperature -= drift
    else:
        current_temperature += drift
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return timestamp, current_temperature

def send_sensor_data(sensor_data):
    try:
        response = requests.patch(DATA_SERVICE_ADDRESS, json=sensor_data)
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Could not connect to {DATA_SERVICE_ADDRESS}: {e}")
    except Exception as e:
        print(f"Failed to send sensor data: {e}")
    return {"Status":"Failed", "Message":"Data not sent"}

@app.route('/sensor')
def get_sensor_data():
    current_temperature = 8.3

    while True:
        target_temperature = get_status()
        time_stamp, current_temperature = gen_sensor_data(target_temperature, current_temperature)
        sensor_data = {str(time_stamp): current_temperature}
        status = send_sensor_data(sensor_data)
        print(status, sensor_data, target_temperature)
        time.sleep(1)

if __name__ == "__main__":
    get_sensor_data()
    app.run(debug=True, host="127.0.0.1", port=5002)