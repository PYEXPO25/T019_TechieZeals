import os
import firebase_admin
from firebase_admin import credentials, db
from flask import Flask, jsonify, render_template

app = Flask(__name__)

# Path to your Firebase key.json file
cred = credentials.Certificate('key.json')

# Initialize Firebase Admin SDK with the credentials
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://aqua-sentinel-357b7-default-rtdb.asia-southeast1.firebasedatabase.app/'
})

@app.route('/')
def home():
    return render_template('authentication.html')  # Serve the index.html file

@app.route('/index')
def index():
    return render_template('index.html')  # Serve the index.html file

@app.route('/logout')
def logout():
    return render_template('authentication.html')


# Serve the index.html file
@app.route('/get_data', methods=['GET'])
def get_data():
    try:
        # Reference your Firebase Realtime Database (root reference in this case)
        ref = db.reference('/')
        
        # Get data from Firebase
        data = ref.get()

        # If data is None, return a message
        if not data:
            return jsonify({"message": "No data found"}), 404
        
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Ensure the static files are served correctly in Flask
    app.run(debug=True)
