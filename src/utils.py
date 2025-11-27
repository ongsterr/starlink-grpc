from src.api import get_all_user_terminals

from pathlib import Path
import json
import pandas as pd


def get_routers_list():
    user_terminals = get_all_user_terminals()
    user_terminals = [
        {
            "ut_id": ut["userTerminalId"],
            "ut_name": ut["nickname"],
            "router_id": router["routerId"],
            "router_name": router["nickname"],
        }
        for ut in user_terminals["content"]["results"]
        for router in ut["routers"]
    ]
    return user_terminals


def generate_wifi_clients_dataset():
    directory = Path("./data/clients")
    json_files = list(directory.glob("*.json"))

    data = []
    for file in json_files:
        with open(file, "r", encoding="utf-8") as f:
            raw = json.load(f)

        modelled = [
            {
                "api_version": raw["apiVersion"],
                "extracted_at": raw["extracted_at"],
                "device_id": raw["device_status"]["deviceInfo"]["id"],
                "device_hardware_version": raw["device_status"]["deviceInfo"]["hardwareVersion"],
                "device_software_version": raw["device_status"]["deviceInfo"]["softwareVersion"],
                "device_country_code": raw["device_status"]["deviceInfo"]["countryCode"],
                "device_uptime_s": raw["device_status"]["deviceState"]["uptimeS"],
                "device_ipv4_wan_address": raw["device_status"]["ipv4WanAddress"],
                "ping_latency_ms": raw["device_status"]["pingLatencyMs"],
                "client_name": client.get("name"),
                "client_mac_address": client.get("macAddress"),
                "client_ip_address": client.get("ipAddress"),
                "client_rx_bytes": client["rxStats"].get("bytes"),
                "client_rx_nss": client["rxStats"].get("nss"),
                "client_tx_bytes": client["txStats"].get("bytes"),
                "client_tx_nss": client["txStats"].get("nss"),
                "client_iface": client.get("iface"),
                "client_associated_time_s": client.get("associatedTimeS"),
                "client_snr": client.get("snr"),
                "client_psmode": client.get("psmode"),
                "client_signal_strength": client.get("signalStrength"),
            }
            for client in raw["wifiGetClients"]["clients"]
        ]

        data.extend(modelled)

    df = pd.DataFrame(data)
    df.to_csv(f"data/dataset/wifi_clients_compiled.csv", index=False)
    return df
