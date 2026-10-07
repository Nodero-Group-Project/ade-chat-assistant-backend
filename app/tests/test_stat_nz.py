"""
Tests for the StatsNZ client, with urllib's urlopen replaced by fakes.
"""

import io
import json
import urllib.error
import urllib.request

from app.services import stat_nz

URL = "https://api.data.stats.govt.nz/rest/data/STATSNZ,CEN23_HOU_001,1.0/2023.16.99.8.001?dimensionAtObservation=AllDimensions"


class FakeResponse(io.BytesIO):
    """ urlopen's response is used as a context manager that returns bytes """


def test_missing_api_key_skips_request(monkeypatch):
    monkeypatch.delenv("STAT_NZ_API_KEY", raising=False)
    calls = []
    monkeypatch.setattr(urllib.request, "urlopen", lambda *args, **kwargs: calls.append(args))

    assert stat_nz.get(URL) is None
    assert calls == []


def test_successful_response_is_parsed(monkeypatch):
    monkeypatch.setenv("STAT_NZ_API_KEY", "test-stats-key")
    sent = {}

    def fake_urlopen(request, *args, **kwargs):
        sent["request"] = request
        return FakeResponse(json.dumps({"data": {"dataSets": []}}).encode("utf-8"))

    monkeypatch.setattr(urllib.request, "urlopen", fake_urlopen)

    assert stat_nz.get(URL) == {"data": {"dataSets": []}}
    assert sent["request"].full_url == URL
    assert sent["request"].get_header("Ocp-apim-subscription-key") == "test-stats-key"


def test_http_error_returns_none(monkeypatch):
    monkeypatch.setenv("STAT_NZ_API_KEY", "test-stats-key")

    def fake_urlopen(request, *args, **kwargs):
        raise urllib.error.HTTPError(URL, 401, "Unauthorized", hdrs=None, fp=io.BytesIO(b"bad key"))

    monkeypatch.setattr(urllib.request, "urlopen", fake_urlopen)

    assert stat_nz.get(URL) is None


def test_connection_error_returns_none(monkeypatch):
    monkeypatch.setenv("STAT_NZ_API_KEY", "test-stats-key")

    def fake_urlopen(request, *args, **kwargs):
        raise urllib.error.URLError("no network")

    monkeypatch.setattr(urllib.request, "urlopen", fake_urlopen)

    assert stat_nz.get(URL) is None