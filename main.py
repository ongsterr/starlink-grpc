from src.pipeline import run_wifi_clients_pipeline, run_speed_test_pipeline
from src.utils import generate_wifi_clients_dataset
from src.client import get_grpc_response


if __name__ == "__main__":
    # run_wifi_clients_pipeline(interval_s=30, runtime_min=300, target_id="Router-0100000000000000014FCF3B")

    generate_wifi_clients_dataset()
    # run_speed_test_pipeline(interval_s=60, runtime_min=60)

    # result = get_grpc_response(req_type="get_dish_emc", target_id="ut01000000-00000000-00c5ebae")
    # print(result)
