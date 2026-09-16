import asyncio
from unittest.mock import patch

from sqlalchemy import create_engine, inspect

import app.main as main_module


def test_lifespan_creates_tables(monkeypatch):
    test_engine = create_engine("sqlite:///:memory:")
    monkeypatch.setattr(main_module, "engine", test_engine)

    async def drive_lifespan():
        async with main_module.lifespan(main_module.app):
            pass

    asyncio.run(drive_lifespan())

    assert "items" in inspect(test_engine).get_table_names()


def test_lifespan_starts_and_stops_scheduler():
    async def drive_lifespan():
        async with main_module.lifespan(main_module.app):
            pass

    with patch("app.main.AsyncIOScheduler") as mock_scheduler_class:
        asyncio.run(drive_lifespan())

        scheduler = mock_scheduler_class.return_value

        scheduler.add_job.assert_called_once()
        scheduler.start.assert_called_once()
        scheduler.shutdown.assert_called_once()
