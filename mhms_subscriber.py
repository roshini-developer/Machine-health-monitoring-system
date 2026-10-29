
import json
import sqlite3
from datetime import datetime, timezone

import paho.mqtt.client as mqtt

BROKER = "broker.hivemq.com"
PORT = 1883
TOPIC = "mhms/roshini/real/temperature"
DATABASE = "mhms.db"


# Open the database and create the table if needed.
conn = sqlite3.connect(DATABASE)

conn.execute("""
CREATE TABLE IF NOT EXISTS temperature_readings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    device TEXT NOT NULL,
    temperature REAL NOT NULL,
    timestamp TEXT NOT NULL
)
""")
conn.commit()


def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        print("Connected to HiveMQ successfully!")
        client.subscribe(TOPIC)
        print(f"Subscribed to: {TOPIC}")
    else:
        print(f"Connection failed: {reason_code}")


def on_message(client, userdata, message):
    try:
        raw_temperature = message.payload.decode("utf-8").strip()
        temperature = float(raw_temperature)

        record = {
            "device": "ESP32",
            "temperature": temperature,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

        json_record = json.dumps(record)
        print(json_record)

        conn.execute(
            """
            INSERT INTO temperature_readings
            (device, temperature, timestamp)
            VALUES (?, ?, ?)
            """,
            (
                record["device"],
                record["temperature"],
                record["timestamp"]
            )
        )
        conn.commit()

        print("Saved to SQLite successfully!")

    except (ValueError, UnicodeDecodeError) as error:
        print(f"Invalid temperature message: {error}")


client = mqtt.Client(
    callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
    client_id="mhms_python_subscriber"
)

client.on_connect = on_connect
client.on_message = on_message

print("Connecting to HiveMQ...")
client.connect(BROKER, PORT, keepalive=60)

try:
    client.loop_forever()
except KeyboardInterrupt:
    print("\nSubscriber stopped.")
finally:
    client.disconnect()
    conn.close()
    print("Database connection closed.")
