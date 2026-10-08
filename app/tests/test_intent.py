import pytest
from unittest.mock import patch

from app.db import Intent
from app.main import intent_add,intent_remove,intent_get

@pytest.mark.asyncio
@patch("app.main.intent_add")
async def test_intent_add(mock):

    intent = Intent(Description="INTENT_FOR_TEST")

    result = await intent_add(intent)

    assert result == {
        "success": True,
        "message": 'The intent added successfully.'
    }

@pytest.mark.asyncio
@patch("app.main.intent_add")
async def test_intent_exists(mock):

    intent = Intent(Description="INTENT_FOR_TEST")

    result = await intent_add(intent)

    assert result == {
        "success": False,
        "message": 'The intent already exists.'
    }

@pytest.mark.asyncio
@patch("app.main.intent_get")
async def test_intent_exists(mock):

    result = await intent_get()

    assert result[0] is not None

@pytest.mark.asyncio
@patch("app.main.intent_remove")
async def test_intent_remove(mock):

    result = await intent_remove("INTENT_FOR_TEST")

    assert result == {
        "success": True,
        "message": "Intent removed successfully."
    }
