import json
import os

CONFIG_FILE = "config.json"

DEFAULT_CONFIG = {
    "stock_minimo": 10
}

def cargar_config():
    if not os.path.exists(CONFIG_FILE):
        guardar_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG

    with open(CONFIG_FILE, "r") as f:
        return json.load(f)


def guardar_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f)