from flask import Flask, jsonify
from flask_cors import CORS
import random

app = Flask(_name_)
CORS(app)  # Enable CORS for frontend-backend communication

# Simulating water quality data
def generate_data():
    ph_value = round(random.uniform(6.5, 8.5), 2)
    ph_percentage = round(((ph_value - 6.5) / (8.5 - 6.5)) * 100, 2)  # Convert pH to percentage
    tds_level = round(random.uniform(100, 500), 2)  # Simulated TDS level (ppm)
    
    return {
        "pH_percentage": ph_percentage,
        "TDS": tds_level
    }

@app.route("/", methods=["GET"])
def get_water_quality():
    return jsonify(generate_data())

if _name_ == "_main_":
    app.run(debug=True, port=5000)