from src.pipeline import run_wifi_clients_pipeline, run_speed_test_pipeline
from src.utils import generate_wifi_clients_dataset
import json


if __name__ == "__main__":
    # run_wifi_clients_pipeline(interval_s=30, runtime_min=60, target_id="Router-0100000000000000014FCF3B")

    # generate_wifi_clients_dataset()
    run_speed_test_pipeline(interval_s=60, runtime_min=60)
