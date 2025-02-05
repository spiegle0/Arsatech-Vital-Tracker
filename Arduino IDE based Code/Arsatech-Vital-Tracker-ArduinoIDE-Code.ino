#include <Wire.h>
#include <Adafruit_MLX90614.h>
#include "MAX30105.h"
#include "spo2_algorithm.h"

// MLX90614 object
Adafruit_MLX90614 mlx = Adafruit_MLX90614();

// MAX30102 object
MAX30105 particleSensor;

// Constants for SpO2 and heart rate
#define BUFFER_SIZE 100
uint32_t irBuffer[BUFFER_SIZE];  // Infrared LED sensor data
uint32_t redBuffer[BUFFER_SIZE]; // Red LED sensor data
int32_t spo2 = 0;                // SpO2 value
int8_t validSPO2 = 0;            // SpO2 validity
int32_t heartRate = 0;           // Heart rate value
int8_t validHeartRate = 0;       // Heart rate validity

// TCRT5000 sensor
const int tcrtPin = 13;  // GPIO 13 as input for TCRT5000

void setup() {
  Serial.begin(115200);
  Wire.begin();

  // Initialize MLX90614
  if (!mlx.begin()) {
    Serial.println("Error: Could not find MLX90614 sensor!");
  } else {
    Serial.println("MLX90614 initialized successfully.");
  }

  // Initialize MAX30102
  if (!particleSensor.begin()) {
    Serial.println("MAX30102 not detected. Check wiring.");
    while (1);
  }
  Serial.println("Place your finger on the MAX30102 sensor.");

  // Configure MAX30102
  particleSensor.setup(50, 1, 2, 100, 411, 4096); // LED brightness, averaging, LED mode, sample rate, pulse width, ADC range

  // Configure TCRT5000 sensor pin
  pinMode(tcrtPin, INPUT);  // Set GPIO 13 as input
}

void loop() {
  // Read MLX90614 data
  if (mlx.begin()) {
    double objectTemp = mlx.readObjectTempC();
    double ambientTemp = mlx.readAmbientTempC();

    Serial.print("MLX90614 - Object Temperature: ");
    Serial.print(objectTemp);
    Serial.println(" °C");

    Serial.print("MLX90614 - Ambient Temperature: ");
    Serial.print(ambientTemp);
    Serial.println(" °C");
  }

  // Collect MAX30102 data
  for (int i = 0; i < BUFFER_SIZE; i++) {
    while (!particleSensor.available()) {
      particleSensor.check();
    }
    redBuffer[i] = particleSensor.getRed();
    irBuffer[i] = particleSensor.getIR();
    particleSensor.nextSample();
  }

  // Calculate SpO2 and heart rate
  maxim_heart_rate_and_oxygen_saturation(irBuffer, BUFFER_SIZE, redBuffer, &spo2, &validSPO2, &heartRate, &validHeartRate);

  // Display MAX30102 results
  if (validHeartRate && validSPO2) {
    Serial.print("MAX30102 - Heart Rate: ");
    Serial.print(heartRate);
    Serial.print(" bpm, SpO2: ");
    Serial.print(spo2);
    Serial.println(" %");
  } else {
    Serial.println("MAX30102 - Reading not valid. Please adjust your finger.");
  }

  // Read TCRT5000 sensor data
  int tcrtValue = digitalRead(tcrtPin);  // Read digital input (HIGH or LOW)

  // Display TCRT5000 status
  if (tcrtValue == HIGH) {
    Serial.println("TCRT5000 - Object Detected");
  } else {
    Serial.println("TCRT5000 - No Object Detected");
  }

  Serial.println("------------------------------------");
  delay(1000); // Wait before the next loop
}