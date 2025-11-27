from src.client import get_grpc_response

import json
from datetime import datetime
import time


def get_device_status():
    device_status_resp = get_grpc_response(req_type="get_device_status")
    device_status = device_status_resp["wifiGetStatus"]
    return device_status


def run_wifi_clients_pipeline(interval_s: int = 30, runtime_min: int = 60):
    runtime_seconds = 0
    wifi_clients = get_grpc_response(req_type="get_wifi_clients")

    clients_data = []
    while runtime_seconds < runtime_min * 60:
        wifi_clients = get_grpc_response(req_type="get_wifi_clients")
        wifi_clients["extracted_at"] = datetime.now().strftime("%d-%m-%Y_%H:%M:%S")
        device_status = get_device_status()
        wifi_clients["device_status"] = device_status

        clients_data.append(wifi_clients)

        with open(f"./data/clients/wifi_clients_{datetime.now().strftime("%d%m%Y_%H%M%S")}.json", "w") as f:
            json.dump(wifi_clients, f, indent=4)
        print(f"Extracted wifi clients data for {runtime_seconds}/{runtime_min*60}")

        time.sleep(interval_s)

        runtime_seconds += interval_s
        if runtime_seconds >= runtime_min * 60:
            print("Runtime reached, stopping pipeline.")
            break

    return clients_data
