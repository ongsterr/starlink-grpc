import grpc
from google.protobuf.json_format import MessageToJson, MessageToDict

from protobuf.spacex.api.device import service_pb2_grpc, device_pb2

from protobuf.spacex.api.device.device_pb2 import (
    GetStatusRequest,
    SpeedTestRequest,
    PingHostRequest,
    GetDeviceInfoRequest,
    GetHistoryRequest,
)
from protobuf.spacex.api.device.wifi_pb2 import WifiGetClientsRequest, WifiGetDiagnosticsRequest, WifiGetConfigRequest
from src.api import get_all_user_terminals


def get_grpc_response(req_type: str, target_id=None):
    """
    Available req_types:
    - get_device_status
    - get_speed_test
    - get_ping_host
    - get_device_info
    - get_ping_history
    - get_wifi_clients
    - get_wifi_diagnostics
    - get_wifi_configs
    """

    # Connect to the server
    channel = grpc.insecure_channel("192.168.1.1:9000")
    stub = service_pb2_grpc.DeviceStub(channel)

    if req_type == "get_device_status":
        request = device_pb2.Request(target_id=target_id, get_status=GetStatusRequest())
    elif req_type == "get_speed_test":
        request = device_pb2.Request(target_id=target_id, speed_test=SpeedTestRequest())
    elif req_type == "get_ping_host":
        request = device_pb2.Request(target_id=target_id, ping_host=PingHostRequest())
    elif req_type == "get_device_info":
        request = device_pb2.Request(target_id=target_id, get_device_info=GetDeviceInfoRequest())
    elif req_type == "get_ping_history":
        request = device_pb2.Request(target_id=target_id, get_history=GetHistoryRequest())
    elif req_type == "get_wifi_clients":
        request = device_pb2.Request(target_id=target_id, wifi_get_clients=WifiGetClientsRequest())
    elif req_type == "get_wifi_diagnostics":
        request = device_pb2.Request(target_id=target_id, wifi_get_diagnostics=WifiGetDiagnosticsRequest())
    elif req_type == "get_wifi_configs":
        request = device_pb2.Request(target_id=target_id, wifi_get_config=WifiGetConfigRequest())
    else:
        print("Request not set up yet.")
        return

    response = stub.Handle(request)
    response_dict = MessageToDict(response)
    response_json = MessageToJson(response)

    return response_dict


def get_routers_clients():
    user_terminals_resp = get_all_user_terminals()
    router_ids = [
        {"terminal_id": terminal["id"], "router_id": router["routerId"]}
        for terminal in user_terminals_resp["content"]["results"]
        for router in terminal["routers"]
    ]

    clients_usage = []

    for router in router_ids:
        router_id = router["router_id"]
        clients = get_grpc_response(router_id, "get_wifi_clients")
        clients_usage.append(clients)

    return clients_usage
