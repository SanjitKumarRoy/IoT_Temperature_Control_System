from flask import Flask, render_template_string

# This is the user-facing web application.
# It provides a dashboard to see the current state and control the target temperature.
# It runs on the default Flask port, 5000.

app = Flask(__name__)

# The entire front-end is contained in this single HTML string.
# It uses Tailwind CSS for styling and vanilla JavaScript for interactivity.
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>IoT Temperature Control</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body { font-family: 'Inter', sans-serif; }
        @import url('https://rsms.me/inter/inter.css');
        .temp-display { font-size: 5rem; line-height: 1; font-weight: 700; }
        .status-dot { width: 12px; height: 12px; }
    </style>
</head>
<body class="bg-gray-100 text-gray-800">

    <div class="container mx-auto p-4 md:p-8 max-w-4xl">
        <header class="mb-8">
            <h1 class="text-3xl font-bold text-gray-900">IoT Temperature Control Panel</h1>
            <p class="text-gray-600">Remotely monitor and manage your room's climate.</p>
        </header>

        <main class="grid grid-cols-1 md:grid-cols-3 gap-6">
            <!-- Main Control Panel -->
            <div class="md:col-span-2 bg-white rounded-xl shadow-md p-6">
                <h2 class="text-xl font-semibold mb-4">Live Status</h2>
                <div class="flex flex-col md:flex-row items-center justify-around gap-8 text-center">
                    <!-- Current Temperature -->
                    <div>
                        <p class="text-gray-500 mb-2">CURRENT ROOM TEMP</p>
                        <div id="current-temp" class="temp-display text-blue-600">--.- °C</div>
                        <div class="flex items-center justify-center mt-2">
                            <div id="status-dot" class="status-dot bg-gray-400 rounded-full mr-2"></div>
                            <span id="status-text" class="text-gray-500">Waiting for data...</span>
                        </div>
                    </div>
                    <!-- Target Temperature -->
                    <div>
                        <p class="text-gray-500 mb-2">TARGET TEMP</p>
                        <div id="target-temp" class="temp-display text-green-600">--.- °C</div>
                    </div>
                </div>

                <!-- Control Interface -->
                <div class="mt-8 pt-6 border-t">
                    <h3 class="font-semibold mb-3">Set New Target Temperature</h3>
                    <div class="flex flex-col sm:flex-row gap-2">
                        <input type="number" id="new-temp-input" class="flex-grow p-2 border rounded-md focus:ring-2 focus:ring-blue-500 focus:outline-none" placeholder="e.g., 22.5">
                        <button onclick="setTemperature()" class="bg-blue-600 text-white font-bold py-2 px-4 rounded-md hover:bg-blue-700 transition-colors">Set Temperature</button>
                    </div>
                    <p id="error-message" class="text-red-500 text-sm mt-2"></p>
                </div>
            </div>

            <!-- Historical Data -->
            <div class="bg-white rounded-xl shadow-md p-6">
                <div class="flex justify-between items-center mb-4">
                    <h2 class="text-xl font-semibold">History</h2>
                    <button onclick="fetchHistory()" class="text-sm text-blue-600 hover:underline">Refresh</button>
                </div>
                <div id="history-container" class="space-y-2 max-h-80 overflow-y-auto pr-2">
                    <p class="text-gray-500">No historical data loaded.</p>
                </div>
            </div>
        </main>
    </div>

    <script>
        const CONTROL_API_URL = 'http://127.0.0.1:5002';
        const DATA_API_URL = 'http://127.0.0.1:5001';

        const currentTempEl = document.getElementById('current-temp');
        const targetTempEl = document.getElementById('target-temp');
        const statusDotEl = document.getElementById('status-dot');
        const statusTextEl = document.getElementById('status-text');
        const historyContainerEl = document.getElementById('history-container');
        const errorMessageEl = document.getElementById('error-message');

        // Fetch the current state from the control service
        async function fetchCurrentState() {
            try {
                const response = await fetch(`${CONTROL_API_URL}/state`);
                if (!response.ok) throw new Error('Network response was not ok');
                const data = await response.json();

                // Update current temperature display
                if (data.current_temperature !== null) {
                    currentTempEl.textContent = `${data.current_temperature.toFixed(1)} °C`;
                    statusDotEl.classList.remove('bg-gray-400', 'bg-red-500');
                    statusDotEl.classList.add('bg-green-500');
                    statusTextEl.textContent = 'Connected';
                } else {
                    currentTempEl.textContent = '--.- °C';
                    statusDotEl.classList.remove('bg-green-500');
                    statusDotEl.classList.add('bg-red-500');
                    statusTextEl.textContent = 'No sensor data';
                }

                // Update target temperature display
                if (data.target_temperature !== null) {
                    targetTempEl.textContent = `${data.target_temperature.toFixed(1)} °C`;
                }

                errorMessageEl.textContent = ''; // Clear previous errors
            } catch (error) {
                console.error('Failed to fetch state:', error);
                statusDotEl.classList.remove('bg-green-500');
                statusDotEl.classList.add('bg-red-500');
                statusTextEl.textContent = 'Service Unreachable';
                errorMessageEl.textContent = 'Error: Could not connect to services. Are they running?';
            }
        }
        
        // Set a new target temperature
        async function setTemperature() {
            const input = document.getElementById('new-temp-input');
            const newTemp = parseFloat(input.value);

            if (isNaN(newTemp)) {
                alert('Please enter a valid number.');
                return;
            }

            try {
                const response = await fetch(`${CONTROL_API_URL}/setpoint`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ temperature: newTemp })
                });
                if (!response.ok) throw new Error('Failed to set temperature');
                
                await response.json();
                input.value = ''; // Clear input on success
                fetchCurrentState(); // Refresh state immediately
            } catch (error) {
                console.error('Error setting temperature:', error);
                alert('Failed to set new temperature.');
            }
        }
        
        // Fetch historical data from the data service
        async function fetchHistory() {
            historyContainerEl.innerHTML = '<p class="text-gray-500">Loading history...</p>';
            try {
                const response = await fetch(`${DATA_API_URL}/data`);
                 if (!response.ok) throw new Error('Network response was not ok');
                const data = await response.json();

                if (data.length === 0) {
                     historyContainerEl.innerHTML = '<p class="text-gray-500">No historical data found.</p>';
                     return;
                }

                let historyHtml = '';
                data.forEach(record => {
                    const date = new Date(record.timestamp);
                    historyHtml += `
                        <div class="flex justify-between text-sm p-1 rounded">
                            <span>${record.temperature.toFixed(1)} °C</span>
                            <span class="text-gray-500">${date.toLocaleTimeString()}</span>
                        </div>
                    `;
                });
                historyContainerEl.innerHTML = historyHtml;
            } catch (error) {
                console.error('Failed to fetch history:', error);
                historyContainerEl.innerHTML = '<p class="text-red-500">Could not load history.</p>';
            }
        }
        
        // On page load, fetch initial data and set up polling
        document.addEventListener('DOMContentLoaded', () => {
            fetchCurrentState();
            fetchHistory();
            setInterval(fetchCurrentState, 5000); // Poll for new state every 5 seconds
        });
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

if __name__ == '__main__':
    # This service runs on port 5000
    app.run(host='0.0.0.0', port=5000, debug=True)

