import dirigera
from typing import Any
import json
import os
from dotenv import load_dotenv
import time
import paho.mqtt.publish as publish

# Load environment variables
load_dotenv()

# MQTT Configuration
MQTT_BROKER = os.getenv("MQTT_BROKER")
MQTT_PORT = int(os.getenv("MQTT_PORT", 1883))  # Default MQTT port is 1883
MQTT_TOPIC = os.getenv("MQTT_TOPIC")

# Dirigera Configuration
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
DIRIGERA_HUB_IP_ADDR = os.getenv("DIRIGERA_HUB_IP_ADDR")

# Print configurations for verification
print(DIRIGERA_HUB_IP_ADDR)
print(ACCESS_TOKEN)
print(MQTT_TOPIC)
print(MQTT_BROKER)
print(MQTT_PORT)

# Initialize Dirigera hub
dirigera_hub = dirigera.Hub(token=ACCESS_TOKEN, ip_address=DIRIGERA_HUB_IP_ADDR)

# Time-off tracker
last_trigger_time = {}


def send_mqtt_message(topic, payload):
    try:
        publish.single(topic, payload, hostname=MQTT_BROKER, port=MQTT_PORT)
        print(f"MQTT Message sent: Topic={topic}, Payload={payload}")
    except Exception as e:
        print(f"Failed to send MQTT message: {e}")


def on_message(ws: Any, message: str):
    message_dict = json.loads(message)
    if message_dict["type"] == "sceneUpdated":
        scene_name = message_dict["data"]["info"]["name"]
        print(scene_name)

        # Check for time-off condition
        current_time = time.time()
        if (
            scene_name not in last_trigger_time
            or (current_time - last_trigger_time[scene_name]) > 2
        ):
            last_trigger_time[scene_name] = current_time
            send_mqtt_message(MQTT_TOPIC, scene_name)


def on_error(ws: Any, message: str):
    print(message)


dirigera_hub.create_event_listener(on_message=on_message, on_error=on_error)
