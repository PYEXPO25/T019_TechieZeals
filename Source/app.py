import os
import smtplib
import firebase_admin
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from firebase_admin import credentials, db
from flask import Flask, jsonify, render_template

app = Flask(__name__)

# Initialize Firebase
cred = credentials.Certificate('aqua-sentinel-357b7-firebase-adminsdk-fbsvc-15495f90d8.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://aqua-sentinel-357b7-default-rtdb.asia-southeast1.firebasedatabase.app/'
})

# Email Configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_ADDRESS = "sanjayjeya2006@gmail.com"
EMAIL_PASSWORD = "ixht vwtj jsov dfox"
RECIPIENT_EMAIL = "vijayadhanush07@gmail.com"

def send_email(subject, body):
    """Sends an email notification."""
    try:
        msg = MIMEMultipart()
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = RECIPIENT_EMAIL
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, RECIPIENT_EMAIL, msg.as_string())

        print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")

@app.route('/')
def home():
    return render_template('authentication.html')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/logout')
def logout():
    return render_template('authentication.html')

@app.route('/get_data', methods=['GET'])
def get_data():
    """Fetch sensor data from Firebase and send alerts if conditions are met."""
    try:
        ref = db.reference('/')
        data = ref.get()

        if not data:
            return jsonify({"message": "No data found"}), 404

        ph_value = data["sensor"]["ph"]
        flow_rate = data["sensor"]["flowRate"]

        if ph_value < 6.5 or ph_value > 8.0:
            send_email(
                "Aqua Sentinel Alert: pH Level Out of Range",
                f"Warning! Water pH level is {ph_value}, outside the safe range (6.5 - 8.0)."
            )

        if flow_rate == 0:
            send_email(
                "Aqua Sentinel Alert: Water Flow Stopped",
                "Warning! The water flow rate has dropped to 0. Immediate action required."
            )

        return jsonify(data), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
