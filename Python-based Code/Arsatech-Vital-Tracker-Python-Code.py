import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import deque
import threading
import re  # For regex-based parsing

# Serial Configuration
SERIAL_PORT = "COM5"  # Replace with your ESP32's serial port
BAUD_RATE = 115200

# Data Buffers
max_length = 300  # Number of data points to display
object_temp = deque([0] * max_length, maxlen=max_length)
ambient_temp = deque([0] * max_length, maxlen=max_length)
heart_rate = deque([40] * max_length, maxlen=max_length)
spo2 = deque([80] * max_length, maxlen=max_length)
tcrt5000 = deque([0] * max_length, maxlen=max_length)

# Function to check serial connection
def check_serial_connection():
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        if ser.is_open:
            print(f"[INFO] Connected to {SERIAL_PORT}")
            ser.close()
        else:
            print(f"[ERROR] Unable to connect to {SERIAL_PORT}")
    except serial.SerialException as e:
        print(f"[ERROR] Serial connection failed: {e}")

# Function to read serial data
def read_serial_data():
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        print("[INFO] Serial connection established on", SERIAL_PORT)
        while True:
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8').strip()
                print("[DEBUG] Raw Line:", line)  # Debugging: Print raw serial data

                # Parse SpO2 Data
                match = re.search(r'SpO2[^0-9]*(\d+)', line)
                if match:
                    ox = int(match.group(1))
                    ox = max(80, min(ox, 100))  # Clamp to 80-100%
                    spo2.append(ox)

                # Parse Object Temperature
                match = re.search(r'Object Temperature:\s*([0-9.]+)', line)
                if match:
                    temp = float(match.group(1))
                    temp = max(0, min(temp, 100))
                    object_temp.append(temp)

                # Parse Ambient Temperature
                match = re.search(r'Ambient Temperature:\s*([0-9.]+)', line)
                if match:
                    temp = float(match.group(1))
                    temp = max(0, min(temp, 100))
                    ambient_temp.append(temp)

                # Parse Heart Rate
                match = re.search(r'Heart Rate:\s*(\d+)', line)
                if match:
                    hr = int(match.group(1))
                    hr = max(40, min(hr, 180))  # Clamp between 40-180 bpm
                    heart_rate.append(hr)

                # Parse TCRT5000 Sensor (Object Detection)
                if "Object Detected" in line:
                    tcrt5000.append(1)
                elif "No Object Detected" in line:
                    tcrt5000.append(0)

    except serial.SerialException as e:
        print("Serial Error:", e)

# Function to update the plot
def update_plot(frame):
    ax1.clear()
    ax2.clear()
    ax3.clear()
    ax4.clear()
    ax5.clear()

    ax1.plot(object_temp, label=f"Object Temp: {object_temp[-1]}°C", color='r', linewidth=2)
    ax1.set_ylim(0, 100)
    ax1.legend()
    ax1.grid(True, linestyle='--', alpha=0.6)
    ax1.set_xlim(0, max_length)

    ax2.plot(ambient_temp, label=f"Ambient Temp: {ambient_temp[-1]}°C", color='b', linewidth=2)
    ax2.set_ylim(0, 100)
    ax2.legend()
    ax2.grid(True, linestyle='--', alpha=0.6)
    ax2.set_xlim(0, max_length)

    ax3.plot(heart_rate, label=f"Heart Rate: {heart_rate[-1]} BPM", color='g', linewidth=2)
    ax3.set_ylim(40, 180)
    ax3.legend()
    ax3.grid(True, linestyle='--', alpha=0.6)
    ax3.set_xlim(0, max_length)

    ax4.plot(spo2, label=f"SpO2: {spo2[-1]}%", color='m', linewidth=2)
    ax4.set_ylim(80, 100)
    ax4.legend()
    ax4.grid(True, linestyle='--', alpha=0.6)
    ax4.set_xlim(0, max_length)

    ax5.plot(tcrt5000, label=f"TCRT5000 Detection: {'Detected' if tcrt5000[-1] == 1 else 'No Object'}", color='k', linewidth=2)
    ax5.set_ylim(-0.5, 1.5)
    ax5.legend()
    ax5.grid(True, linestyle='--', alpha=0.6)
    ax5.set_xlim(0, max_length)

# Check serial connection before starting
check_serial_connection()

# Create the plot
fig, (ax1, ax2, ax3, ax4, ax5) = plt.subplots(5, 1, figsize=(10, 12), sharex=True)
ani = animation.FuncAnimation(fig, update_plot, interval=500)

# Start serial data reading in a separate thread
thread = threading.Thread(target=read_serial_data, daemon=True)
thread.start()

# Show the plot
plt.show()
