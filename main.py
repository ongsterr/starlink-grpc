from src.client import get_grpc_response
from src.api import get_all_user_terminals

import json


if __name__ == "__main__":
    ### example grpc request to router server
    router_id = "0100000000000000014FB585"
    get_grpc_response(router_id, "get_device_info")
