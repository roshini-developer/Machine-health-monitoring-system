# Python MQTT Subscriber — MHMS V1

## Overview
This module is responsible for receiving machine temperature readings from the MQTT broker, processing the incoming data as JSON records, and storing the readings in a local SQLite database.

## Working Process
1. Connects to the HiveMQ public MQTT broker.
2. Subscribes to the MHMS temperature topic.
3. Receives temperature readings published by the ESP32.
4. Processes the readings into JSON records containing device information, temperature, and timestamp.
5. Stores the received records in an SQLite database.

## Technologies Used
- Python
- MQTT (Paho MQTT Client)
- JSON
- SQLite

## MQTT Configuration
- Broker: broker.hivemq.com
- Port: 1883
- Topic: `mhms/roshini/real/temperature`

## JSON Data Structure

Each received reading is processed with the following information:

- `device` — Device identifier
- `temperature` — Measured temperature in °C
- `timestamp` — Reading timestamp in UTC

## Database
Temperature readings are stored locally in SQLite in the `temperature_readings` table.

The live database file is excluded from the GitHub repository.

## Execution

Install the required Python package:

```bash
pip install paho-mqtt
```

Run the subscriber:

```bash
python mhms_subscriber.py
```

Ensure that the ESP32 is publishing data to the configured MQTT topic before running the subscriber.
