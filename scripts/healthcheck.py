import asyncio
import aiohttp


async def healthcheck():
    async with aiohttp.ClientSession(raise_for_status=True) as session:
        resp = await session.get("http://127.0.0.1:8000/v1/health")
        health: dict[str, int] = await resp.json()
        if health["total"] == 0 or health["online"] < health["total"] - 1:
            raise RuntimeError


if __name__ == "__main__":
    asyncio.run(healthcheck())
