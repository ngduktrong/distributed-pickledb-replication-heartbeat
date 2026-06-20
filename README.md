Link Demo : [OneDirve_Account Phenikaa can View Demo](https://daihocphenikaa-my.sharepoint.com/:v:/g/personal/23010594_st_phenikaa-uni_edu_vn/IQBjfjSYy_HHS4EhVBR-Km0VAQW4CcRrf7McSrriUvPWQGc?nav=eyJyZWZlcnJhbEluZm8iOnsicmVmZXJyYWxBcHAiOiJPbmVEcml2ZUZvckJ1c2luZXNzIiwicmVmZXJyYWxBcHBQbGF0Zm9ybSI6IldlYiIsInJlZmVycmFsTW9kZSI6InZpZXciLCJyZWZlcnJhbFZpZXciOiJNeUZpbGVzTGlua0NvcHkifX0&e=qe51wr)
# Distributed PickleDB with Replication and Heartbeat
[![Logo](https://patx.github.io/pickledb/logo.png)](https://patx.github.io/pickledb)

[pickleDB](https://patx.github.io/pickledb) is a fast, easy to use, in-memory Python 
key-value store with first class asynchronous support. It is built with the `orjson` 
module for extremely high performance. It is licensed under the BSD three-clause 
license. [Check out the website](https://patx.github.io/pickledb) for installation 
instructions, API docs, advanced examples, benchmarks, and more.

```python
from pickledb import PickleDB

db = PickleDB("example.json").load()
db.set("key", "value")

db.get("key")  # return "value"
```

A demo fork of PickleDB that adds simple distributed replication and worker
heartbeat monitoring on top of the original async/sync JSON-backed key-value
store.

## What this repository includes

- `pickledb.py`: the core PickleDB key-value store using `orjson` and `aiofiles`.
- `replica_manager.py`: asynchronous replication support for forwarding writes to
  replica nodes.
- `heartbeat_manager.py`: worker health checks using periodic heartbeat requests.
- `dashboard.py`: primary node UI and API for saving data, viewing replicas, and
  checking worker status.
- `worker1.py`, `worker2.py`: replica nodes that accept replication requests and
  expose their stored data and heartbeat endpoints.
- `templates/index.html`: dashboard frontend for status, replica snapshots, and
  write operations.

## Features

- Fast in-memory key-value storage with optional persistence to a JSON file.
- Primary-replica write replication from dashboard to worker nodes.
- Heartbeat-based worker liveness detection.
- Simple browser dashboard for status and replica inspection.

## Requirements

- Python 3.10+
- `pip`

Optional dependencies are defined in `pyproject.toml`:

- `distributed`: `aiohttp`, `fastapi`, `jinja2`, `pydantic`, `uvicorn`
- `test`: `aiohttp`, `aiosqlite`, `pytest`, `pytest-asyncio`

## Installation

Install the package with distributed dependencies:

```bash
pip install -e '.[distributed]'
```

Install test dependencies separately when needed:

```bash
pip install -e '.[test]'
```

## Run the demo

Start the dashboard and worker nodes in separate terminals:

```bash
uvicorn dashboard:app --port 9000
uvicorn worker1:app --port 8001
uvicorn worker2:app --port 8002
```

Open the dashboard at:

```text
http://127.0.0.1:9000
```

The dashboard writes data into `dashboard.json` and replicates each key/value to
`worker1.json` and `worker2.json` via `/replicate`. The dashboard also polls
worker heartbeat and replica snapshots through its API.

## Demo behavior

- Add a key/value pair in the dashboard form.
- The dashboard persists the data locally and sends it to both worker nodes.
- The dashboard fetches replica snapshots from each worker using `/all`.
- If you stop a worker, the dashboard will show that node as `OFFLINE`.
- Restart the worker to restore its `ONLINE` status.

## Testing

Run the test suite with:

```bash
python -m pytest -q
```

To enable longer stress tests explicitly:

```bash
RUN_STRESS_TESTS=1 python -m pytest -m stress
```

## Notes

- The repository is based on the original PickleDB project and extends it with
  a minimal distributed demo.
- The dashboard and workers use local HTTP endpoints on ports `8000`, `8001`,
  and `8002` by default.
