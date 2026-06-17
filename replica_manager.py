import asyncio

import aiohttp


class ReplicaManager:
    def __init__(self, replicas=None, timeout=3):
        self.replicas = list(replicas or [])
        self.timeout = timeout

    async def replicate(self, key, value):
        if not self.replicas:
            return {}

        timeout = aiohttp.ClientTimeout(total=self.timeout)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            results = await asyncio.gather(
                *(
                    self._replicate_one(session, replica, key, value)
                    for replica in self.replicas
                )
            )

        return dict(results)

    async def _replicate_one(self, session, replica, key, value):
        try:
            async with session.post(
                f"{replica}/replicate",
                json={
                    "key": key,
                    "value": value,
                },
            ) as response:
                return replica, response.status < 400

        except Exception:
            return replica, False
