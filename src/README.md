## IoT Temperature Control System using Microservices
This project demonstrates a simple IoT system for monitoring and controlling room temperature using a microservice architecture with Flask.

### Architecture
The system is composed of four independent components:

**1. Data Service** (`data_service.py`):
The backend service responsible for receiving and storing all temperature readings.
It runs on port `5001`.

**2. Control Service** (`control_service.py`):
Manages the system's state, specifically the target temperature.
It fetches the latest reading from the Data Service to provide a complete system status. It runs on port `5002`.

**3, Client Application** (`client_app.py`):
The user-facing web dashboard.
It communicates with the other two services to display data and allow the user to set a new target temperature.
It runs on port `5000`.

**4. IoT Device Simulator** (`iot_device_simulator.py`):
A script that mimics a real-world IoT sensor.
It periodically sends simulated temperature readings to the Data Service.

### How to Run

You need to have Python and the `Flask`, `requests`, and `Flask-Cors` libraries installed.
```bash
pip install Flask requests Flask-Cors
```
You will need to open four separate terminal windows or tabs to run each component simultaneously.

#### Step 1: Start the Data Service
In your first terminal, run:
```bash
python data_service.py
```
You should see output indicating that the Flask server is running on `http://127.0.0.1:5001`.

#### Step 2: Start the Control Service
In your second terminal, run:
```bash
python control_service.py
```
This will start the control server on `http://127.0.0.1:5002`.

#### Step 3: Start the Client Web Application
In your third terminal, run:
```bash
python client_app.py
```
This will start the main web application on `http://127.0.0.1:5000`.

#### Step 4: Start the IoT Device Simulator
In your fourth terminal, run:
```bash
python iot_device_simulator.py
```
This script will start sending data immediately.
You will see log messages in this terminal and in the Data Service terminal.

#### Step 5: View the Control Panel
Open your web browser and navigate to:

https://www.google.com/search?q=http://127.0.0.1:5000

You should now see the control panel.
It will automatically update every 5 seconds with new data from the simulator.
You can set a new target temperature and watch as the simulator's ''current temperature'' slowly adjusts to meet the new target.
You can also refresh the history panel to see all the data points that have been logged.