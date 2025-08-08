# NodeSPL
Distributed framework to Sample, Process and Learn from multi-source signal data

## Overview
Goal:
A modular framework that allows multiple embedded nodes to send sensor data to a centralized server (especially medical domain). The server processes this data using configurable signal processing and regression algorithms and provides real-time visualization and API access.

## High-Level Architecture
+-----------------+          +------------------+          +---------------------+ \n
|  Sensor Nodes   |  -->     |  Communication   |  -->     |    Server Backend   |
|  (RPi Pico W)   |  POST    |  (MQTT or HTTP)  |          | (Flask + ML/Signal) |
+-----------------+          +------------------+          +----------+----------+
                                                                       |
                                                                       v
                                                            +----------+----------+
                                                            |  Visualization/API  |
                                                            |  (Dashboard + REST) |
                                                            +---------------------+

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
| Receive endpoint w/ auth	|✅|
|In-memory data buffer per device	|✅|
|Configurable signal + ML pipeline	|✅|
|Web dashboard (polling)	|✅|
|Configuration API	|✅|
|MicroPython node script	|✅|
