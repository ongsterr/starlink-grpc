from src.client import get_grpc_response
from src.api import get_accounts


if __name__ == "__main__":
    ### example grpc request to router server
    router_id = "0100000000000000014FB585"
    get_grpc_response(req_type="get_device_info", target_id=router_id)

    ### example api request
    accounts = get_accounts()
    print(accounts)
