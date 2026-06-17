import pytest

from heartbeat_manager import HeartbeatManager


@pytest.mark.asyncio
async def test_check_all_returns_empty_status_when_no_replicas():
    manager = HeartbeatManager([])

    assert await manager.check_all() == {}
    assert manager.status == {}


@pytest.mark.asyncio
async def test_check_node_returns_online_for_http_200():
    manager = HeartbeatManager([])
    session = FakeSession(status=200)

    node, state = await manager._check_node(session, "http://worker")

    assert node == "http://worker"
    assert state == "ONLINE"
    assert session.requests == ["http://worker/heartbeat"]


@pytest.mark.asyncio
async def test_check_node_returns_offline_for_http_error():
    manager = HeartbeatManager([])
    session = FakeSession(status=500)

    node, state = await manager._check_node(session, "http://worker")

    assert node == "http://worker"
    assert state == "OFFLINE"


@pytest.mark.asyncio
async def test_check_node_returns_offline_for_connection_error():
    manager = HeartbeatManager([])
    session = FakeSession(error=RuntimeError("connection failed"))

    node, state = await manager._check_node(session, "http://worker")

    assert node == "http://worker"
    assert state == "OFFLINE"


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

    def get(self, url):
        self.requests.append(url)

        if self.error is not None:
            raise self.error

        return FakeResponse(self.status)
