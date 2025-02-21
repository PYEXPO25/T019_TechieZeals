from flask import Flask, jsonify
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)  


def generate_data():
    ph_value = round(random.uniform(6.5, 8.5), 2)
    ph_percentage = round(((ph_value - 6.5) / (8.5 - 6.5)) * 100, 2)  
    tds_level = round(random.uniform(100, 500), 2)  
    water_flow = round(random.uniform(1.0, 10.0), 2) 
    
    return {
        "pH_percentage": ph_percentage,
        "TDS": tds_level,
        "Water_Flow": water_flow
    }

@app.route("/api/water-quality", methods=["GET"])
def get_water_quality():
    return jsonify(generate_data())

if __name__ == "__main__":
    app.run(debug=True, port=5000)
