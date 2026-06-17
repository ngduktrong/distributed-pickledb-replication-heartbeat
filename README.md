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

## Distributed features

This fork adds two distributed-systems features on top of PickleDB:

- Data Replication: writes on the dashboard node are replicated to worker nodes.
- Heartbeat and Failure Detection: the dashboard periodically checks worker
  nodes and marks them as `ONLINE` or `OFFLINE`.

The demo uses a primary-replica model:

```text
Dashboard / Primary Node :8000
  |-- Worker 1 / Replica :8001
  `-- Worker 2 / Replica :8002
```

Install the optional dashboard dependencies:

```bash
pip install -e ".[distributed]"
```

Run the dashboard and two replicas in separate terminals:

```bash
uvicorn dashboard:app --port 8000
uvicorn worker1:app --port 8001
uvicorn worker2:app --port 8002
```

Open `http://127.0.0.1:8000` to view node health and replicated data. If port
8000 is busy, use another dashboard port, for example:

```bash
uvicorn dashboard:app --port 9000
```

Use the form in the dashboard to save a key-value pair. The dashboard writes to
`dashboard.json`, then PickleDB's replica manager sends the write to worker
nodes through `/replicate`. The dashboard reads each worker's `/all` endpoint
through `/replica-data` so each replica snapshot is visible in the browser.

To demo failure detection, stop one worker process. Within a few seconds, the
dashboard should mark that worker as `OFFLINE`. Start it again and the status
should return to `ONLINE`.

## Tests

Install test dependencies and run the unit tests:

```bash
pip install -e ".[test]"
python -m pytest -q
```

The million-entry stress test is disabled by default. Enable it explicitly with
`RUN_STRESS_TESTS=1 python -m pytest -m stress`.
