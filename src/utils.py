from src.api import get_all_user_terminals

from pathlib import Path
import json
import pandas as pd
import duckdb


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
                "st_upload_mbps": raw["speed_test"]["upload"] / 1000000 if raw.get("speed_test") else None,
                "st_download_mbps": raw["speed_test"]["download"] / 1000000 if raw.get("speed_test") else None,
                "st_ping_ms": raw["speed_test"]["ping"] if raw.get("speed_test") else None,
                "st_server_url": raw["speed_test"]["server"].get("url") if raw.get("speed_test") else None,
                "st_server_lat": raw["speed_test"]["server"].get("lat") if raw.get("speed_test") else None,
                "st_server_lon": raw["speed_test"]["server"].get("lon") if raw.get("speed_test") else None,
                "st_server_name": raw["speed_test"]["server"].get("name") if raw.get("speed_test") else None,
                "st_server_country": raw["speed_test"]["server"].get("country") if raw.get("speed_test") else None,
                "st_server_cc": raw["speed_test"]["server"].get("cc") if raw.get("speed_test") else None,
                "st_server_sponsor": raw["speed_test"]["server"].get("sponsor") if raw.get("speed_test") else None,
                "st_server_id": raw["speed_test"]["server"].get("id") if raw.get("speed_test") else None,
                "st_server_host": raw["speed_test"]["server"].get("host") if raw.get("speed_test") else None,
                "st_server_d": raw["speed_test"]["server"].get("d") if raw.get("speed_test") else None,
                "st_server_latency": raw["speed_test"]["server"].get("latency") if raw.get("speed_test") else None,
                "st_timestamp": raw["speed_test"]["timestamp"] if raw.get("speed_test") else None,
                "st_bytes_sent": raw["speed_test"]["bytes_sent"] if raw.get("speed_test") else None,
                "st_bytes_received": raw["speed_test"]["bytes_received"] if raw.get("speed_test") else None,
                "st_share": raw["speed_test"]["share"] if raw.get("speed_test") else None,
                "st_client_ip": raw["speed_test"]["client"].get("ip") if raw.get("speed_test") else None,
                "st_client_lat": raw["speed_test"]["client"].get("lat") if raw.get("speed_test") else None,
                "st_client_lon": raw["speed_test"]["client"].get("lon") if raw.get("speed_test") else None,
                "st_client_isp": raw["speed_test"]["client"].get("isp") if raw.get("speed_test") else None,
                "st_client_isprating": raw["speed_test"]["client"].get("isprating") if raw.get("speed_test") else None,
                "st_client_rating": raw["speed_test"]["client"].get("rating") if raw.get("speed_test") else None,
                "st_client_ispdlavg": raw["speed_test"]["client"].get("ispdlavg") if raw.get("speed_test") else None,
                "st_client_ispulavg": raw["speed_test"]["client"].get("ispulavg") if raw.get("speed_test") else None,
                "st_client_loggedin": raw["speed_test"]["client"].get("loggedin") if raw.get("speed_test") else None,
                "st_client_country": raw["speed_test"]["client"].get("country") if raw.get("speed_test") else None,
            }
            for client in raw["wifiGetClients"]["clients"]
        ]

        data.extend(modelled)

    df = pd.DataFrame(data)
    df_enriched = duckdb.sql(
        """
        select
        d.*
        , case
            when coalesce(cast(d.client_rx_bytes as float), 0) - coalesce(lag(cast(d.client_rx_bytes as float)) over (partition by d.client_ip_address order by d.extracted_at), 0) < 0 then coalesce(cast(d.client_rx_bytes as float), 0)
            else coalesce(cast(d.client_rx_bytes as float), 0) - coalesce(lag(cast(d.client_rx_bytes as float)) over (partition by d.client_ip_address order by d.extracted_at), 0)
            end as client_rx_bytes_diff
        , case
            when coalesce(cast(d.client_tx_bytes as float), 0) - coalesce(lag(cast(d.client_tx_bytes as float)) over (partition by d.client_ip_address order by d.extracted_at), 0) < 0 then coalesce(cast(d.client_tx_bytes as float), 0)
            else coalesce(cast(d.client_tx_bytes as float), 0) - coalesce(lag(cast(d.client_tx_bytes as float)) over (partition by d.client_ip_address order by d.extracted_at), 0)
            end as client_tx_bytes_diff
        from df d
        """
    ).to_df()
    df_enriched.to_csv(f"data/dataset/wifi_clients_compiled.csv", index=False)
    return df_enriched
