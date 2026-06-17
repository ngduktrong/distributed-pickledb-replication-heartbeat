import asyncio

from heartbeat_manager import HeartbeatManager

manager = HeartbeatManager(
    [
        "http://127.0.0.1:8001",
        "http://127.0.0.1:8002"
    ]
)

asyncio.run(
    manager.monitor()
)