from src.client import get_grpc_response


if __name__ == "__main__":
    ### example grpc request to router server
    router_id = "0100000000000000014FB585"
    get_grpc_response(router_id, "get_device_info")
