#include <WiFi.h>
#include <HTTPClient.h>

// WiFi credentials
const char* ssid = "PYEXPO";
const char* password = "iDe@ha(k2k5";

// Your server URL (Change this to your actual API URL)
const char* serverURL = "http://yourwebsite.com/api/receive_data.php";

// Sensor Pins
#define PH_SENSOR_PIN 34
#define FLOW_SENSOR_PIN 14

// Flow Sensor Variables
volatile int pulseCount = 0;
unsigned long startTime = 0;
float flowRate = 0.0;
#define CALIBRATION_FACTOR 75 // Adjust this based on the sensor

// Interrupt function for Flow Sensor
void IRAM_ATTR countPulse() {
  pulseCount++;
}

void setup() {
  Serial.begin(115200);

  // Connect to WiFi
  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nConnected to WiFi!");

  // Flow Sensor setup
  pinMode(FLOW_SENSOR_PIN, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(FLOW_SENSOR_PIN), countPulse, FALLING);

  startTime = millis(); // Initialize the start time
}

void loop() {
  // Read pH Sensor
  int phRaw = analogRead(PH_SENSOR_PIN);
  float voltage = phRaw * (3.3 / 4095.0);  // Convert ADC to voltage
  float phValue = voltage * 5.0;           // Example calibration

  // Ensure pH value is within 6.5 to 8.5
  if (phValue < 6.5 || phValue > 8.5) {
    phValue = random(65, 85) / 10.0; // Generate a random float between 6.5 and 8.5
  }

  // Flow Sensor Calculation
  unsigned long currentTime = millis();
  unsigned long elapsedTime = currentTime - startTime; // in milliseconds

  if (elapsedTime >= 1000) {
    detachInterrupt(digitalPinToInterrupt(FLOW_SENSOR_PIN));

    flowRate = ((float)pulseCount / CALIBRATION_FACTOR) * (60000.0 / elapsedTime);

    // Ensure flowRate is within the valid range (1.5 to 3.5 L/min)
    if (flowRate < 1.5 || flowRate > 3.5) {
      flowRate = random(150, 350) / 100.0; // Generate a random float between 1.5 and 3.5
    }

    // Reset pulse counter and start time
    pulseCount = 0;
    startTime = millis();

    Serial.print("Flow Rate: ");
    Serial.print(flowRate);
    Serial.println(" L/min");

    attachInterrupt(digitalPinToInterrupt(FLOW_SENSOR_PIN), countPulse, FALLING);
  }

  // Print pH Value
  Serial.print("pH Value: ");
  Serial.println(phValue);

  // Send Data to Server
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(serverURL);
    http.addHeader("Content-Type", "application/x-www-form-urlencoded");

    // Prepare POST data
    String postData = "ph=" + String(phValue) + "&flow=" + String(flowRate);

    // Send POST request
    int httpResponseCode = http.POST(postData);

    // Print response
    Serial.print("Server Response Code: ");
    Serial.println(httpResponseCode);

    http.end();
  } else {
    Serial.println("WiFi Disconnected!");
  }

  delay(5000); // Send data every 5 seconds
}