"""
Author: sg.kim
Date: 2025-04-25
Description:
"""
import pytest

from app.dependencies import get_async_session


@pytest.mark.asyncio
async def test_database_connection():

    get_async_session()
