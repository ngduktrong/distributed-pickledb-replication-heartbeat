import asyncio

import aiohttp


class HeartbeatManager:
    def __init__(self, replicas, timeout=3):
        self.replicas = list(replicas)
        self.timeout = timeout
        self.status = {}

    async def check_node(self, node):
        timeout = aiohttp.ClientTimeout(total=self.timeout)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            replica, state = await self._check_node(session, node)
            self.status[replica] = state
            return state

    async def check_all(self):
        if not self.replicas:
            self.status = {}
            return {}

        timeout = aiohttp.ClientTimeout(total=self.timeout)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            results = await asyncio.gather(
                *(self._check_node(session, node) for node in self.replicas)
            )

        self.status = dict(results)
        return dict(self.status)

    async def _check_node(self, session, node):
        try:
            async with session.get(f"{node}/heartbeat") as response:
                if response.status == 200:
                    return node, "ONLINE"
                return node, "OFFLINE"

        except Exception:
            return node, "OFFLINE"

    async def monitor(self):
        while True:
            await self.check_all()

            print("\n========== NODE STATUS ==========")
            for node, state in self.status.items():
                print(f"{node} ---> {state}")

            await asyncio.sleep(5)
