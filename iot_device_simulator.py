import requests
import time
import random

# This script simulates an IoT device.
# It periodically checks the target temperature from the Control Service
# and sends its simulated sensor readings to the Data Service.

CONTROL_SERVICE_URL = "http://127.0.0.1:5002/state"
DATA_SERVICE_URL = "http://127.0.0.1:5001/data"

# Initial simulated temperature
current_temperature = 20.0

def get_target_temperature():
    """Fetches the target temperature from the control service."""
    try:
        response = requests.get(CONTROL_SERVICE_URL)
        response.raise_for_status()
        return response.json().get('target_temperature')
    except requests.exceptions.RequestException as e:
        print(f"SIMULATOR: Could not get target temperature: {e}")
        return None

def post_temperature_reading(temp):
    """Posts a new temperature reading to the data service."""
    try:
        payload = {"temperature": temp}
        response = requests.post(DATA_SERVICE_URL, json=payload)
        response.raise_for_status()
        print(f"SIMULATOR: Successfully sent temperature reading: {temp:.2f}°C")
    except requests.exceptions.RequestException as e:
        print(f"SIMULATOR: Could not send temperature reading: {e}")

def simulate_temperature_change(current, target):
    """
    Simulates the room temperature slowly changing to meet the target.
    Adds a little random noise to make it more realistic.
    """
    if target is None:
        # If we can't get a target, just drift randomly
        return current + random.uniform(-0.2, 0.2)
        
    # Move towards the target temperature
    if current < target:
        current += random.uniform(0.1, 0.4)
    elif current > target:
        current -= random.uniform(0.1, 0.4)
    
    # Add some random sensor noise
    current += random.uniform(-0.1, 0.1)
    
    return current

if __name__ == "__main__":
    print("--- IoT Device Simulator Started ---")
    print("Press Ctrl+C to stop.")
    while True:
        try:
            # 1. Get the current setpoint
            target_temp = get_target_temperature()

            # 2. Simulate the new temperature based on the target
            current_temperature = simulate_temperature_change(current_temperature, target_temp)

            # 3. Send the new reading to the data service
            post_temperature_reading(current_temperature)
            
            # 4. Wait for the next cycle
            time.sleep(5) # Send data every 5 seconds

        except KeyboardInterrupt:
            print("\n--- IoT Device Simulator Stopped ---")
            break
        except Exception as e:
            print(f"SIMULATOR: An unexpected error occurred: {e}")
            time.sleep(10) # Wait longer if there's a persistent error

