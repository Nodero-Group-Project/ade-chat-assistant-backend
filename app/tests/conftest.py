"""
Shared test setup.

Tests marked 'live' call the real Groq and StatsNZ APIs and are skipped unless pytest is run with --live. Every other tests runs with the APIs blocked, so they are fast and give the same results consistently.
"""

import os 
import urllib.request
from pathlib import Path
from unittest.mock import MagicMock

import pytest
from dotenv import load_dotenv

# Load real keys first (for live tests), then fall back to a dummy so the Groq clients can be created at import time without a .env file
load_dotenv(Path(__file__).parents[1] / ".env")
os.environ.setdefault("GROQ_API_KEY", "test-key")

from app import intent_classification, llm_query
from app.tests.fakes import make_completion

def pytest_addoption(parser):
    parser.addoption("--live", action="store_true", help="Run tests that call the real Groq and StatsNZ APIs")
    
def pytest_collection_modifyitems(config, items):
    if config.getoption("--live"):
        return
    skip_live = pytest.mark.skip(reason="calls real APIs; run with --live")
    for item in items:
        if "live" in item.keywords:
            item.add_marker(skip_live)
            
@pytest.fixture(autouse=True)
def block_real_apis(request, monkeypatch):
    """ Fail loudly if a non-live test tries to reach Groq or StatsNZ """
    if "live" in request.keywords:
        return
    
    blocked_client = MagicMock()
    blocked_client.chat.completions.create.side_effect = AssertionError("test tried to call the real Groq API")
    monkeypatch.setattr(llm_query, "client", blocked_client)
    monkeypatch.setattr(intent_classification, "client", blocked_client)
    
    def blocked_urlopen(*args, **kwargs):
        raise AssertionError("test tried to make a real HTTP request")
    monkeypatch.setattr(urllib.request, "urlopen", blocked_urlopen)
    
    
@pytest.fixture
def fake_groq(monkeypatch):
    """
    Replace a module's Groq client with one that returns the given reply.
    Returns the mock so tests can check what was sent, e.g. which model was used.
    """
    def install(module, content, **completion_kwargs):
        client = MagicMock()
        client.chat.completions.create.return_value = make_completion(content, **completion_kwargs)
        monkeypatch.setattr(module, "client", client)
        return client

    return install
    