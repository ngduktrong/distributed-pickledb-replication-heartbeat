from typing import Any

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from heartbeat_manager import HeartbeatManager
from pickledb import PickleDB


NODE_NAME = "worker1"
DB_FILE = "worker1.json"
REPLICAS = [
    "http://127.0.0.1:8001",
    "http://127.0.0.1:8002",
]

app = FastAPI()
db = PickleDB(DB_FILE).load()
manager = HeartbeatManager(REPLICAS)


class ReplicateRequest(BaseModel):
    key: str = Field(min_length=1)
    value: Any


@app.post("/replicate")
async def replicate(data: ReplicateRequest):
    key = data.key.strip()
    if not key:
        raise HTTPException(status_code=400, detail="Key cannot be blank.")

    await db.set(key, data.value)
    await db.save()

    return {
        "status": "ok",
        "worker": NODE_NAME,
        "key": key,
    }


@app.get("/all")
async def all_data():
    return await db.dump()


@app.get("/heartbeat")
async def heartbeat():
    return {
        "status": "alive",
        "node": NODE_NAME,
    }


@app.get("/status")
async def get_status():
    return await manager.check_all()
