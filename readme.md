# Starlink API

Simple utilities to query:

- Starlink Management & Telemetry HTTP APIs (public / enterprise)
- Local device gRPC API (router device)

## Quick links

- HTTP API code: [`src/api.py`](src/api.py) — main helpers like [`src.api.get_token`](src/api.py), [`src.api.get_all_user_terminals`](src/api.py), and [`src.api.generate_telemetry_stream`](src/api.py).
- API endpoints config: [`src/config.py`](src/config.py) — the `starlink_api_config` mapping.
- Local gRPC client: [`src/client.py`](src/client.py) — functions [`src.client.get_grpc_response`](src/client.py) and [`src.client.get_routers_clients`](src/client.py).
- Utilities: [`src/utils.py`](src/utils.py) — small helpers like [`src.utils.get_routers_list`](src/utils.py).
- Example runner: [main.py](main.py)
- Example data/ metadata: [data/metadata/routers.json](data/metadata/routers.json)
- Project deps: [pyproject.toml](pyproject.toml)

## Requirements

- Python 3.12 (see [pyproject.toml](pyproject.toml))
- Install dependencies with your preferred tool (poetry/pip).

## Configuration

- Add secrets to a `.env` (or environment) — `CLIENT_ID_PROD` and `CLIENT_SECRET_PROD` are used by [`src.api.get_token`](src/api.py).
- Files saved/used by the code live under `data/` (and are gitignored).

## Usage examples

1. Query Starlink HTTP APIs / telemetry

- Get all user terminals: call [`src.api.get_all_user_terminals`](src/api.py).
- Produce telemetry CSVs & parsed results: call [`src.api.generate_telemetry_stream`](src/api.py). Results are saved in `./data/`.

2. Query local device gRPC server

- Use [`src.client.get_grpc_response`](src/client.py) to run requests against the local router gRPC server (see [main.py](main.py) for an example call).
- Use [`src.client.get_routers_clients`](src/client.py) to fetch Wi‑Fi clients across routers returned by the HTTP API.

## Notes

- Some requests in [`src/api.py`](src/api.py) disable SSL verification (verify=False) — adjust for production.
- Output files (JSON/CSV) are written into `./data/` for easy inspection.

## Usage examples

1. Query Starlink HTTP APIs / telemetry

- Get all user terminals: call [`src.api.get_all_user_terminals`](src/api.py).
- Produce telemetry CSVs & parsed results: call [`src.api.generate_telemetry_stream`](src/api.py). Results are saved in `./data/`.

2. Query local device gRPC server

- Use [`src.client.get_grpc_response`](src/client.py) to run requests against the local router gRPC server (see [main.py](main.py) for an example call).
- Use [`src.client.get_routers_clients`](src/client.py) to fetch Wi‑Fi clients across routers returned by the HTTP API.

## Quick start (examples)

1. Setup a virtual environment and install deps (example using pip)

   ```
   poetry init
   poetry install
   ```

2. Set required secrets (example .env)

- CLIENT_ID_PROD=...
- CLIENT_SECRET_PROD=...

3. Run some example scripts provided in `main.py`.

   ```
   poetry run python main.py
   ```
