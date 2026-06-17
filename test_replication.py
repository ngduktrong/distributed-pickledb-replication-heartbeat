import pytest

from pickledb import PickleDB
from replica_manager import ReplicaManager


class FakeReplicaManager:
    def __init__(self):
        self.calls = []

    async def replicate(self, key, value):
        self.calls.append((key, value))
        return {"fake": True}


def test_pickledb_does_not_replicate_by_default(tmp_path):
    db = PickleDB(str(tmp_path / "test.json"))

    assert db.set("name", "Trong") is True
    assert db.replica_manager is None


@pytest.mark.asyncio
async def test_pickledb_replicates_when_manager_is_configured(tmp_path):
    replica_manager = FakeReplicaManager()
    db = PickleDB(
        str(tmp_path / "test.json"),
        replica_manager=replica_manager,
    )

    assert await db.set("name", "Trong") is True

    assert replica_manager.calls == [("name", "Trong")]


@pytest.mark.asyncio
async def test_replica_manager_reports_success_for_http_2xx():
    manager = ReplicaManager([])
    session = FakeSession(status=200)

    replica, success = await manager._replicate_one(
        session,
        "http://worker",
        "course",
        "distributed systems",
    )

    assert replica == "http://worker"
    assert success is True
    assert session.requests == [
        (
            "http://worker/replicate",
            {
                "key": "course",
                "value": "distributed systems",
            },
        )
    ]


@pytest.mark.asyncio
async def test_replica_manager_reports_failure_for_http_error():
    manager = ReplicaManager([])
    session = FakeSession(status=500)

    replica, success = await manager._replicate_one(
        session,
        "http://worker",
        "course",
        "distributed systems",
    )

    assert replica == "http://worker"
    assert success is False


@pytest.mark.asyncio
async def test_replica_manager_reports_failure_for_connection_error():
    manager = ReplicaManager([])
    session = FakeSession(error=RuntimeError("connection failed"))

    replica, success = await manager._replicate_one(
        session,
        "http://worker",
        "course",
        "distributed systems",
    )

    assert replica == "http://worker"
    assert success is False


class FakeResponse:
    def __init__(self, status):
        self.status = status

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, traceback):
        return False


class FakeSession:
    def __init__(self, status=200, error=None):
        self.status = status
        self.error = error
        self.requests = []

    def post(self, url, json):
        self.requests.append((url, json))

        if self.error is not None:
            raise self.error

        return FakeResponse(self.status)
