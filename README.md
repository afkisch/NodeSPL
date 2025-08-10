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
git clone https://github.com/yourusername/nodespl.git
cd nodespl
pip install -r requirements.txt
```

# NodeSPL
Distributed framework to Sample, Process and Learn from multi-source signal data

## Overview
Goal:
A modular framework that allows multiple embedded nodes to send sensor data to a centralized server (especially medical domain). The server processes this data using configurable signal processing and regression algorithms and provides real-time visualization and API access.

## High-Level Architecture
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
## Components
### Sensor Node (Device Layer)
Hardware: Raspberry Pi Pico W

Language: MicroPython

Function:
- Read analog ECG signal
- Normalize or compress data if needed
- Send to server via HTTP POST

### Communication Layer
Mode: HTTP (MVP), MQTT (future option)
API endpoint: POST /receive
Optional: X-API-KEY auth header

### Server Backend
Language: Python 3
Framework: Flask (or FastAPI)

Functionality:
- Receive and validate incoming data
- Route to appropriate processing pipeline
- Store in-memory (via deque) or buffer
- Expose API endpoints: /data, /configure, /health

### Processing Pipeline
Defined per device

Chain of transformations:
- Signal smoothing
- Feature extraction (optional)
- Regression (linear, logistic, ...)

## API Design
|API|Method|Description|
|-------|----|------------------------------------------|
| /receive	| POST |	Accepts incoming data ({ "device": "id", "value": 1234 }) |
| /data	| GET	| Returns recent N samples per device |
| /configure|	POST | Sets processing pipeline for a device |
| /health	| GET	| Health check, device status, API key check |

## File Structure
```bash
spl_framework/
├── server/
│   ├── app.py             # Flask app
│   ├── pipeline.py        # Signal processing functions
│   ├── config.py          # Per-device pipeline config
│   ├── buffer.py          # Stores recent data in memory
│   ├── auth.py            # API key validation
│   └── templates/
│       └── index.html     # Live dashboard
├── node/
│   └── pico_send.py       # MicroPython script
├── requirements.txt
└── README.md
```
### Visualization Layer
Frontend: <PENDING>

Function:
- Visualize latest ECG signal
- Show processed version (e.g., regression overlay)

## Design Principles

Modular: Processing pipeline can be changed per device

Stateless nodes: Devices don’t run ML, just publish

Configurable: Server can dynamically reconfigure pipelines

Open-source friendly: Lightweight, readable, easy to extend

Hardware-agnostic: Works with any sensor node supporting HTTP/MQTT

## MVP Checklist
| Feature |	Status |
| ----- | -----|
| Receive endpoint w/ auth	|TBD|
|In-memory data buffer per device	|TBD|
|Configurable signal + ML pipeline	|TBD|
|Web dashboard (polling)	|TBD|
|Configuration API	|TBD|
|MicroPython node script	|TBD|
