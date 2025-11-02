from flask import Flask, request, jsonify

history = {}
app = Flask(__name__)

@app.route('/sensor_data', methods=['PATCH'])
def get_sensor_data():
    value = request.get_json()
    if value is None:
        return jsonify({"Status":"Error!"})
    else:
        keys = value.keys()
        for key in keys:
            history[key] = value[key]
    return jsonify({"Status":"Success"})

@app.route('/history', methods=['GET'])
def get_history():
    # number_of_items = 10
    number_of_items = request.args.get('number_of_items', default=10, type=int)
    items = dict(list(history.items())[-number_of_items:])
    return jsonify(items)

if __name__ == '__main__':
    app.run(debug=True, host="127.0.0.1", port=5001)

