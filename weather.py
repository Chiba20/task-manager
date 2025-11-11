from flask import Flask, jsonify, request

app = Flask(__name__)

# ------------------------------
# Mock Weather Data
# ------------------------------
weather_data = {
    "London": {
        "temperature": "15°C",
        "condition": "Cloudy",
        "humidity": "70%"
    },
    "Paris": {
        "forecast": [
            {"day": 1, "temperature": "18°C", "condition": "Sunny"},
            {"day": 2, "temperature": "17°C", "condition": "Partly Cloudy"},
            {"day": 3, "temperature": "16°C", "condition": "Rain"}
        ]
    }
}


# ------------------------------------------------------------
# Endpoint 1:
# /api/weather/current?city=London
# Returns: temperature, condition, humidity
# ------------------------------------------------------------
@app.route("/api/weather/current", methods=["GET"])
def get_current_weather():
    city = request.args.get("city")

    if not city:
        return jsonify({"error": "city parameter is required"}), 400

    city = city.capitalize()

    if city not in weather_data:
        return jsonify({"error": "City not found"}), 404

    return jsonify(weather_data[city])


# ------------------------------------------------------------
# Endpoint 2:
# /api/weather/forecast?city=Paris&days=3
# Returns: 3-day forecast data
# ------------------------------------------------------------
@app.route("/api/weather/forecast", methods=["GET"])
def get_weather_forecast():
    city = request.args.get("city")
    days = request.args.get("days", default=3, type=int)

    if not city:
        return jsonify({"error": "city parameter is required"}), 400

    city = city.capitalize()

    if city not in weather_data or "forecast" not in weather_data[city]:
        return jsonify({"error": "Forecast not available for this city"}), 404

    return jsonify(weather_data[city]["forecast"][:days])


# ------------------------------------------------------------
# Run Flask App
# ------------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5001)
