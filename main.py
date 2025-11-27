from src.pipeline import run_wifi_clients_pipeline
from src.utils import generate_wifi_clients_dataset


if __name__ == "__main__":
    # run_wifi_clients_pipeline(interval_s=30, runtime_min=60)

    generate_wifi_clients_dataset()
