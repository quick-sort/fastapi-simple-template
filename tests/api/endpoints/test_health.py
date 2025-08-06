import logging

import pytest
from httpx import AsyncClient

logger = logging.getLogger(__name__)


@pytest.mark.asyncio
async def test_ping(client: AsyncClient):
    logger.info("Testing ping")
    resp = await client.get("/api/v1/health/ping")
    assert resp.json()["ping"] == "pong"
