from src.client import get_grpc_response
from src.speedtest import run_ookla_speedtest

import json
from datetime import datetime
import time


def get_device_status():
    device_status_resp = get_grpc_response(req_type="get_device_status")
    device_status = device_status_resp["wifiGetStatus"]
    return device_status


def run_wifi_clients_pipeline(interval_s: int = 30, runtime_min: int = 60, target_id: str = "Router-0100000000000000014FB585"):
    runtime_seconds = 0
    wifi_clients = get_grpc_response(req_type="get_wifi_clients")
    speed_test = run_ookla_speedtest()

    clients_data = []
    while runtime_seconds < runtime_min * 60:
        wifi_clients = get_grpc_response(req_type="get_wifi_clients", target_id=target_id)
        wifi_clients["extracted_at"] = datetime.now().strftime("%d-%m-%Y_%H:%M:%S")
        device_status = get_device_status()
        wifi_clients["device_status"] = device_status
        wifi_clients["speed_test"] = speed_test

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


def run_speed_test_pipeline(interval_s: int = 300, runtime_min: int = 60):

    data = []
    runtime_seconds = 0
    while runtime_seconds < runtime_min * 60:
        res = run_ookla_speedtest()
        res["extracted_at"] = datetime.now().strftime("%d-%m-%Y_%H:%M:%S")
        data.append(res)

        with open(f"./data/speedtest/speedtest_{datetime.now().strftime("%d%m%Y_%H%M%S")}.json", "w") as f:
            json.dump(res, f, indent=4)
        print(f"Extracted speed test data for {runtime_seconds}/{runtime_min*60}")

        time.sleep(interval_s)
        runtime_seconds += interval_s

        if runtime_seconds >= runtime_min * 60:
            print("Runtime reached, stopping pipeline.")
            break

    return data
