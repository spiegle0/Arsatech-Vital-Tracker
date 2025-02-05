# 🏥 Arsatech-Vital-Tracker

**Real-time Health Monitoring System using ESP32 & Python Visualization**  

🚀 Developed as part of an internship at **Arsatechnology**, this system collects and visualizes real-time biometric sensor data using an **ESP32 Wroom DA**. It includes two implementations:  

- **ESP32 (Arduino IDE)** – Reads sensor data and transmits it via serial communication.  
- **Python (PC Visualization)** – Processes and displays the data in a **medical-style live graph** using **Matplotlib**.  

---

## 📌 Features  

✅ **Body & Ambient Temperature Monitoring**  
- Uses **MLX90614** to measure object & ambient temperature (0-100°C).  

✅ **Heart Rate & SpO₂ Tracking**  
- Uses **MAX30102** to detect heart rate (40-180 BPM) and oxygen saturation (80-100%).  

✅ **Object Detection**  
- Uses **TCRT5000** to detect object presence (0 = No object, 1 = Object detected).  

✅ **Real-Time Medical Graph Visualization**  
- Displays sensor data dynamically using **Matplotlib** in Python.  

---

## 🛠️ Hardware Requirements  

- **ESP32 Wroom DA**  
- **MLX90614** (Infrared Temperature Sensor)  
- **MAX30102** (Pulse Oximeter & Heart Rate Sensor)  
- **TCRT5000** (Object Detection Sensor)  





