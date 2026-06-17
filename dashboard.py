import asyncio
from typing import Any

import aiohttp
from fastapi import FastAPI, HTTPException, Request
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

from heartbeat_manager import HeartbeatManager
from pickledb import PickleDB


REPLICAS = [
    "http://127.0.0.1:8001",
    "http://127.0.0.1:8002",
]

app = FastAPI()
templates = Jinja2Templates(directory="templates")

manager = HeartbeatManager(REPLICAS)
db = PickleDB("dashboard.json", replicas=REPLICAS)
db.load()


class SetDataRequest(BaseModel):
    key: str = Field(min_length=1)
    value: Any


@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={},
    )


@app.get("/status")
async def get_status():
    return await manager.check_all()


@app.post("/set")
async def set_data(data: SetDataRequest):
    key = data.key.strip()
    if not key:
        raise HTTPException(status_code=400, detail="Key cannot be blank.")

    await db.set(key, data.value)
    await db.save()

    return {
        "status": "success",
    }


@app.get("/data")
async def get_data():
    return await db.dump()


@app.get("/replica-data")
async def get_replica_data():
    timeout = aiohttp.ClientTimeout(total=3)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        results = await asyncio.gather(
            *(fetch_replica_data(session, replica) for replica in REPLICAS)
        )

    return dict(results)


async def fetch_replica_data(session, replica):
    try:
        async with session.get(f"{replica}/all") as response:
            if response.status == 200:
                return replica, {
                    "status": "ok",
                    "data": await response.json(),
                }

            return replica, {
                "status": "error",
                "error": f"HTTP {response.status}",
            }

    except Exception:
        return replica, {
            "status": "error",
            "error": "UNREACHABLE",
        }
