#Arsatech-Vital-Tracker

🚀 ESP32-based real-time health monitoring system

#Overview
Arsatech-Vital-Tracker is a real-time health monitoring system based on ESP32 Wroom DA, developed during an internship at #Arsatechnology. This system collects and visualizes biometric sensor data, displaying it in a medical-style graphical #interface for real-time monitoring.

#Code Versions
This project includes two versions of code:

1.ESP32 (Arduino IDE) – The firmware that runs on the ESP32 to read data from sensors and send it via Serial communication.
2.Python (PC Visualization) – A Python script that reads the serial data from ESP32 and visualizes it using Matplotlib in a medical-style graph.
#Features :
✅ Body & Ambient Temperature Monitoring – Uses MLX90614 to measure object and ambient temperature (0-100°C).
✅ Heart Rate & SpO2 Tracking – Uses MAX30102 to detect heart rate (40-180 BPM) and oxygen saturation (80-100%).
✅ Object Detection – Uses TCRT5000 to detect object presence with a binary output (0 = no object, 1 = object detected).
✅ Real-Time Visualization – Displays sensor data in a live medical-style graph using Python & Matplotlib.

#Hardware Requirements
-ESP32 Wroom DA
-MLX90614 (Infrared Temperature Sensor)
-MAX30102 (Pulse Oximeter & Heart Rate Sensor)
-TCRT5000 (Optical Sensor for Object Detection)

#Software Requirements
-Arduino IDE (for ESP32 programming)
-Python 3.x with required libraries:
-pyserial – for serial communication
-matplotlib – for data visualization
-threading – for handling serial data asynchronously




