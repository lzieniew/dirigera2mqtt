import dirigera
from typing import Any
import json
import os


ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
dirigera_hub = dirigera.Hub(token=ACCESS_TOKEN, ip_address="192.168.1.161")


def on_message(ws: Any, message: str):
    message_dict = json.loads(message)
    print(message_dict)


def on_error(ws: Any, message: str):
    print(message)


dirigera_hub.create_event_listener(on_message=on_message, on_error=on_error)
