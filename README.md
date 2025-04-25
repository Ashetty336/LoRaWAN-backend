

ME check
# 🌐 LoRaWAN Network Optimization & Real-Time Dashboard

A full-stack platform to simulate, monitor, and optimize LoRaWAN network parameters in real time using ChirpStack, Socket.IO, FastAPI, and Supabase. Visualize live sensor data and dynamically tune Adaptive Data Rate (ADR) settings via a modern web interface.

---

## 🧠 Project Overview

This project simulates and processes real-time LoRa sensor data through ChirpStack, enabling visual monitoring and dynamic ADR control from a web-based dashboard. Whether using physical sensors or simulated data, it empowers experimentation with data rate strategies and live tuning.

---

## 📡 System Architecture

```text
LoRa Sensors
    ↓
ChirpStack → MQTT Broker (Mosquitto)
    ↓
FastAPI Backend
  • Subscribes to MQTT topics (via paho-mqtt)
  • Runs ADR logic (custom module)
  • Broadcasts real-time data via Socket.IO
  • Accepts ADR tuning commands from frontend via Socket.IO
  • Writes data to Supabase/PostgreSQL for history
    ↓                        ↕
Frontend (Next.js + shadcn/ui) ←→ Socket.IO Client
```

---

## 🚀 Features

- 📶 Real-time data ingestion from ChirpStack via MQTT
- 🔄 Full-duplex live communication using Socket.IO
- 🎛️ Interactive ADR tuning (Spreading Factor, Tx Power, etc.)
- 📈 Live dashboard with signal + environmental data (RSSI, SNR, Temp, etc.)
- 💾 Historical data storage in Supabase for analytics
- 🧠 Modular ADR algorithm logic (easily swappable)

---

## 🧰 Tech Stack

### 📦 Backend

- **FastAPI** – Async Python backend framework
- **paho-mqtt** – MQTT client for real-time data from ChirpStack
- **python-socketio** – Enables real-time event-based communication
- **Supabase** – PostgreSQL cloud database for storing historical sensor data
- **ADR Logic Module** – Custom Python module for dynamic data rate adjustment

### 💻 Frontend

- **Next.js** – Full-featured React framework
- **shadcn/ui** – Modern and accessible UI components built on TailwindCSS
- **socket.io-client** – Socket.IO frontend integration for live updates

### 🔧 Infrastructure

- **ChirpStack** – LoRaWAN Network Server stack
- **Mosquitto** – Lightweight MQTT broker
- **Docker** (optional) – For containerized setup and deployment

---

## 📁 Folder Structure

```
/backend
  ├── main.py              # FastAPI app with MQTT and Socket.IO integration
  ├── adr_logic.py         # Pluggable ADR decision logic
  └── requirements.txt     # Backend dependencies

/frontend
  ├── pages/               # Next.js route files
  ├── components/          # shadcn/ui-based components
  └── utils/               # Socket.IO connection logic

/simulators
  └── fake_mqtt_sensor.py  # Simulates MQTT uplinks from LoRa sensors

/docs
  └── ADR.md               # Explanation of ADR algorithm used
```

---

## 🧪 Simulating Without Hardware

If you don't have actual LoRa sensors, simulate MQTT uplinks to test the full stack.

```bash
# Run MQTT simulation script
python simulators/fake_mqtt_sensor.py
```

This will mimic sensor uplinks via MQTT, trigger ADR logic, and push data to the frontend via Socket.IO.

---

## ⚙️ Getting Started

### Clone the repository

```bash
git clone https://github.com/yourusername/lorawan-adr-dashboard.git
cd lorawan-adr-dashboard
```

### Start Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

### Start Frontend

```bash
cd frontend
npm install
npm run dev
```

### Optional: Run MQTT Sensor Simulator

```bash
python simulators/fake_mqtt_sensor.py
```

---

## 📈 Roadmap

- [ ] Multi-sensor support and device registration
- [ ] ADR optimization comparison (visual SF vs RSSI/SNR graphs)
- [ ] Alerts for anomalous sensor values or network dropouts
- [ ] Role-based user access and authentication (Supabase Auth)
- [ ] Docker Compose integration

---

## 📄 License

Licensed under the MIT License.

---

## 🤝 Contributing

Fork,create new branch and create a pull request when done.

---


