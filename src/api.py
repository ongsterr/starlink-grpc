import requests
import os
import json
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv

from src.config import starlink_api_config


load_dotenv()


def get_token():
    client_id = os.getenv("CLIENT_ID_PROD")
    client_secret = os.getenv("CLIENT_SECRET_PROD")
    url = "https://www.starlink.com/api/auth/connect/token"
    payload = {"grant_type": "client_credentials", "client_id": client_id, "client_secret": client_secret}
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post(url, data=payload, headers=headers, verify=False)

    result = response.json()
    access_token = result.get("access_token")
    return access_token


def get_accounts(version: str = "v2"):
    token = get_token()
    url = starlink_api_config[version]["get_accounts"]()["url"]
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers, verify=False)
    try:
        resp_json = response.json()
        with open(f"./data/accounts_{datetime.now().strftime("%d-%m-%Y_%H%M%S")}.json", "w") as f:
            json.dump(resp_json, f, indent=4)
        return resp_json
    except Exception as e:
        print(f"Response: {response.status_code} - {response.text}")


def get_all_addresses(account_number=None, version="v2"):
    token = get_token()
    url = starlink_api_config[version]["get_all_addresses"](account_number)["url"]
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers, verify=False)
    return response.json()


def get_all_router_configs(account_number=None, version="v2"):
    token = get_token()
    url = starlink_api_config[version]["get_all_router_configs"](account_number)["url"]
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers, verify=False)

    resp_json = response.json()

    with open(f"./data/router_configs_{datetime.now().strftime("%d-%m-%Y_%H%M%S")}.json", "w") as f:
        json.dump(resp_json, f, indent=4)

    return resp_json


def get_router_details(account_number=None, router_id=None, version="v2"):
    token = get_token()
    url = starlink_api_config[version]["get_router_details"](account_number, router_id)["url"]
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers, verify=False)
    try:
        return response.json()
    except Exception as e:
        print(f"Response: {response.status_code} - {response.text}")
        print(f"Error parsing JSON response: {e}")
        return None


def get_tls_configs(account_number=None, version="v2"):
    token = get_token()
    url = starlink_api_config[version]["get_tls_configs"](account_number)["url"]
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers, verify=False)
    return response.json()


def get_router_local_content(account_number=None):
    token = get_token()
    url = f"https://web-api.starlink.com/enterprise/v1/accounts/{account_number}/router-local-content"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers, verify=False)
    return response.json()


def get_all_service_lines(account_number=None, version="v2"):
    token = get_token()
    url = starlink_api_config[version]["get_all_service_lines"](account_number)["url"]
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers, verify=False)
    resp_json = response.json()

    with open(f"./data/service_lines_{datetime.now().strftime("%d-%m-%Y_%H%M%S")}.json", "w") as f:
        json.dump(resp_json, f, indent=4)

    return resp_json


def get_service_line(account_number=None, service_line_no=None, version="v2"):
    token = get_token()
    url = starlink_api_config[version]["get_service_line"](account_number, service_line_no)["url"]
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers, verify=False)
    return response.json()


def get_products(account_number=None, version="v2"):
    token = get_token()
    url = starlink_api_config[version]["get_products"](account_number)["url"]
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers, verify=False)
    return response.json()


def get_all_user_terminals(account_number=None, version="v2"):
    token = get_token()
    url = starlink_api_config[version]["get_all_user_terminals"](account_number)["url"]
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers, verify=False)
    resp_json = response.json()

    with open(f"./data/user_terminals_{datetime.now().strftime("%d-%m-%Y_%H%M%S")}.json", "w") as f:
        json.dump(resp_json, f, indent=4)

    return resp_json


def get_account_data_usage(
    account_number=None,
    previous_billing_cycle: int = 1,
):
    token = get_token()
    url = f"https://web-api.starlink.com/enterprise/v1/accounts/{account_number}/billing-cycles/query"
    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "previousBillingCycles": previous_billing_cycle,
        "activeServiceLinesOnly": True,
    }
    response = requests.post(url, headers=headers, json=payload, verify=False)
    return response.json()


def get_sandbox_clients(account_number=None):
    token = get_token()
    url = f"https://web-api.starlink.com/enterprise/v1/account/{account_number}/routers/sandbox/clients"
    headers = {"Authorization": f"Bearer {token}"}
    query_params = {"sandboxId": "11"}
    response = requests.get(url, headers=headers, verify=False, params=query_params)
    return response.json()


def reboot_user_terminal(account_number: str, device_id: str):
    token = get_token()
    url = f"https://web-api.starlink.com/enterprise/v1/account/{account_number}/user-terminals/{device_id}/reboot"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(url, headers=headers, verify=False)
    return response.json()


def get_telemetry_cached(account_number=None, include_user_terminals=True, include_routers=True, version="v2"):
    token = get_token()
    url = starlink_api_config[version]["get_telemetry_cached"](account_number, include_user_terminals, include_routers)[
        "url"
    ]
    headers = {"Authorization": f"Bearer {token}"}
    payload = starlink_api_config[version]["get_telemetry_cached"](
        account_number, include_user_terminals, include_routers
    )["payload"]
    response = requests.post(url, headers=headers, verify=False, json=payload)
    resp_json = response.json()

    return resp_json


def get_telemetry_stream(account_number=None, batch_size=1000, max_linger_ms=15000, version="v2"):
    token = get_token()
    url = starlink_api_config[version]["get_telemetry_stream"](account_number, batch_size, max_linger_ms)["url"]
    headers = {"Authorization": f"Bearer {token}"}
    payload = starlink_api_config[version]["get_telemetry_stream"](account_number, batch_size, max_linger_ms)["payload"]
    response = requests.post(url, headers=headers, verify=False, json=payload)
    resp_json = response.json()

    return resp_json


def process_telemetry_response(resp):
    cols = resp["data"]["columnNamesByDeviceType"]
    values = resp["data"]["values"]
    device_types = resp["metadata"]["enums"]["DeviceType"]
    alerts_by_device_type = resp["metadata"]["enums"]["AlertsByDeviceType"]

    formatted_output = []
    col_types = ["u", "r", "i"]

    for row in values:
        for col_type in col_types:
            if row[0] == col_type:
                keys = cols[col_type]
                data = {keys[i]: row[i] for i in range(len(keys))}
                data["DeviceType"] = device_types.get(col_type, "Unknown")
                data["ActiveAlertsVerbose"] = (
                    [alerts_by_device_type[col_type].get(str(alert), "Unknown Alert") for alert in data["ActiveAlerts"]]
                    if data.get("ActiveAlerts")
                    else []
                )
                formatted_output.append(data)

    return formatted_output


def generate_telemetry_stream(account_number: str, batch_size: int = 10000, max_linger_ms: int = 1000, version="v2"):
    token = get_token()
    url = starlink_api_config[version]["get_telemetry_stream"](account_number, batch_size, max_linger_ms)["url"]
    headers = {"Authorization": f"Bearer {token}"}
    payload = starlink_api_config[version]["get_telemetry_stream"](account_number, batch_size, max_linger_ms)["payload"]
    response = requests.post(url, headers=headers, verify=False, json=payload)
    resp_json = response.json()
    results = process_telemetry_response(resp_json)

    with open("./data/telemetry_raw.json", "w") as f:
        json.dump(resp_json, f, indent=4)

    # model dataframe for router
    results_router = list(filter(lambda x: x["DeviceType"] == "Router", results))

    if len(results_router) > 0:
        results_router_df = pd.DataFrame(results_router)
        results_router_df["UtcDatetime"] = pd.to_datetime(
            results_router_df["UtcTimestampNs"], unit="ns", utc=True
        ).dt.strftime("%Y-%m-%d %H:%M:%S")
        results_router_df["RowKey"] = (
            results_router_df["DeviceId"].astype(str) + "-" + results_router_df["UtcTimestampNs"].astype(str)
        )
        results_router_df["AccountNumber"] = account_number

        results_router_df.to_csv(
            f"./data/router_telemetry_data_{datetime.now().strftime("%d-%m-%Y_%H%M%S")}.csv", index=False
        )
    else:
        results_router_df = pd.DataFrame()

    # model dataframe for user terminal
    results_user_terminal = list(filter(lambda x: x["DeviceType"] == "UserTerminal", results))
    if len(results_user_terminal) > 0:
        results_user_terminal_df = pd.DataFrame(results_user_terminal)
        results_user_terminal_df["UtcDatetime"] = pd.to_datetime(
            results_user_terminal_df["UtcTimestampNs"], unit="ns", utc=True
        ).dt.strftime("%Y-%m-%d %H:%M:%S")
        results_user_terminal_df["RowKey"] = (
            results_user_terminal_df["DeviceId"].astype(str)
            + "-"
            + results_user_terminal_df["UtcTimestampNs"].astype(str)
        )
        results_user_terminal_df["AccountNumber"] = account_number

        results_user_terminal_df.to_csv(
            f"./data/user_terminal_telemetry_data_{datetime.now().strftime("%d-%m-%Y_%H%M%S")}.csv", index=False
        )
    else:
        results_user_terminal_df = pd.DataFrame()

    # model dataframe for ip allocation
    results_ip_allocation = list(filter(lambda x: x["DeviceType"] == "IpAllocs", results))
    if len(results_ip_allocation) > 0:
        results_ip_allocation_df = pd.DataFrame(results_ip_allocation)
        results_ip_allocation_df["UtcDatetime"] = pd.to_datetime(
            results_ip_allocation_df["UtcTimestampNs"], unit="ns", utc=True
        ).dt.strftime("%Y-%m-%d %H:%M:%S")
        results_ip_allocation_df["RowKey"] = (
            results_ip_allocation_df["DeviceId"].astype(str)
            + "-"
            + results_ip_allocation_df["UtcTimestampNs"].astype(str)
        )
        results_ip_allocation_df["AccountNumber"] = account_number

        results_ip_allocation_df.to_csv(
            f"./data/ip_allocation_telemetry_data_{datetime.now().strftime("%d-%m-%Y_%H%M%S")}.csv", index=False
        )
    else:
        results_ip_allocation_df = pd.DataFrame()

    return {
        "raw": results,
        "router": results_router_df,
        "user_terminal": results_user_terminal_df,
        "ip_allocation": results_ip_allocation_df,
    }
