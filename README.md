# NodeSPL: Distributed Signal Processing & Machine Learning Framework
**Sample. Process. Learn.**  

🚧 *Ongoing MVP project* 🚧

**NodeSPL** is a lightweight, configurable framework for **distributed signal acquisition, preprocessing, and server-side analytics**.  
It’s designed for scenarios where **multiple nodes** (e.g., medical devices, industrial sensors, IoT endpoints) send data to a central server for **signal processing, anomaly detection, and machine learning**.

---

## ✨ Features (MVP Progress)

- ✅ **Node → Server transport layer** using HTTP POST (JSON envelopes)
- ✅ **Configurable preprocessing on nodes**  
  - Baseline correction  
  - Z-score normalization  
  - Filtering (basic low/high-pass)
- ✅ **Server-side pipelines** defined in JSON/YAML
- 🚧 **Flexible data envelope**  
  - Works with scalars, arrays, dicts, or booleans  
- ✅ **REST APIs** for data ingest, node health, and configs
- 🚧 **Web UI** under development (node health, live signal data, pipeline editor)

---

## 📦 Example Data Envelope

```json
{
  "node_id": "node-001",
  "timestamp": "2025-08-25T12:00:00Z",
  "sensor_type": "ecg",
  "step": "filtered_signal",
  "output_type": "array",
  "output": [0.1, 0.2, 0.3, 0.4]
}

```

---

## 🛠️ Getting Started

Clone the repository:

```bash
git clone https://github.com/afkisch/nodespl
cd nodespl
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the server:

```bash
python src/app.py
```

Nodes can POST sensor data to:

```http
POST /api/v1/nodes/{node_id}/data
```

---

## 📚 API Overview

- ``` POST /api/v1/nodes/{node_id}/data ``` → ingest new sensor data  
- ``` GET /api/v1/nodes/{node_id}/latest ``` → fetch last reported data  
- ``` GET /api/v1/nodes/{node_id}/config ``` → get current pipeline config  
- ``` POST /api/v1/nodes/{node_id}/heartbeat ``` → send node heartbeat  

All endpoints support **API key authentication** using `x-api-key` header.

---

## 🏗️ High-Level Architecture
``` bash
+-----------------+          +------------------+          +---------------------+ 
|  Sensor Nodes   |  -->     |  Communication   |  -->     |    Server Backend   |
|  (RPi Pico W)   |  POST    |  (MQTT or HTTP)  |          |   (Flask + DSP&ML)  |
+-----------------+          +------------------+          +----------+----------+
                                                                       |
                                                                       v
                                                            +----------+----------+
                                                            |  Visualization/API  |
                                                            |  (Dashboard + REST) |
                                                            +---------------------+
```
---

## 🚀 Roadmap

- [ ] Web UI with dynamic rendering (node cards, health indicators, charts)  
- [ ] Configurable pipeline editor (UI-based)  
- [ ] MQTT support for scalability (20+ devices)  
- [ ] Cloud deployment (Docker + AWS / GCP)  
- [ ] More DSP blocks (FFT, HRV analysis, anomaly detection)  
- [ ] Support for multiple sensor types (ECG, temp, industrial signals)  

---

## 📌 Changelog

### [0.1.0] – 2025-08-25
- Initial MVP:
  - Data ingest API  
  - Node preprocessing configs  
  - Server pipeline executor  
  - REST APIs for data & health  
  - Automated testing setup



# NodeSPL
**Sample. Process. Learn.**  
A distributed signal processing & machine learning framework for IoT and edge devices.

NodeSPL lets you connect multiple lightweight nodes (e.g., Raspberry Pi Pico, ESP32) to a Python-based server for real-time data collection, preprocessing, and advanced analytics.

## 🚀 Features
- Modular **node-side preprocessing** (conditioning, outlier detection, normalization, filtering)
- Centralized **server-side analytics** (FFT, ML models, anomaly detection)
- Supports **YAML/JSON pipeline definitions** for easy configuration
- Works with biomedical, environmental, and industrial sensors
- Scales from **local deployments** to **cloud hosting**

## 📦 Quick Start
```bash
git clone https://github.com/YOURNAME/nodespl.git
cd nodespl
pip install -r requirements.txt
```

## MVP Checklist
| Feature |	Status |
| ----- | -----|
| Receive endpoint w/ auth	|✅|
|In-memory data buffer per device	|✅|
|Configurable signal + ML pipeline	|🚧|
|DSP + ML functions	|TBD|
|Web dashboard (polling)	|🚧|
|Configuration API	|✅|
|MicroPython node script	|🚧|
