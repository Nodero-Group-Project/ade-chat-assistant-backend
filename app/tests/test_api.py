"""
HTTP-level tests for the FastAPI endpoints, with the LLM steps and StatsNZ mocked out.
"""

import pytest
from fastapi.testclient import TestClient

from app import main

URL = "https://api.data.stats.govt.nz/rest/data/STATSNZ,CEN23_HOU_001,1.0/2023.16.99.8.001?dimensionAtObservation=AllDimensions"
CLASSIFIER_USAGE = {"input": 580, "cached": 0, "output": 60, "reasoning": 30}
QUERY_USAGE = {"input": 700, "cached": 100, "output": 150, "reasoning": 100}

client = TestClient(main.web)


@pytest.fixture
def pipeline(monkeypatch):
    """
    Mock both LLM steps and StatsNZ. Tests change the returned values as needed;
    `calls` records what StatsNZ and query_llm were called with.
    """
    state = {
        "analysis": {"selected_dataset_id": "CEN23_HOU_001", "selection_confidence": 0.9, "usage": CLASSIFIER_USAGE},
        "query_result": {"success": True, "URL": URL, "model": "openai/gpt-oss-20b", "tier": "faster", "usage": QUERY_USAGE},
        "statistic_data": {"data": {"dataSets": [{"observations": {"0:0:0:0:0": [1290]}}]}},
        "calls": {"query_llm": [], "stat_nz": []},
    }

    def fake_query_llm(user_query, dataset):
        state["calls"]["query_llm"].append((user_query, dataset["id"]))
        return state["query_result"]

    def fake_stat_nz_get(url):
        state["calls"]["stat_nz"].append(url)
        return state["statistic_data"]

    monkeypatch.setattr(main, "analyse_query", lambda q: state["analysis"])
    monkeypatch.setattr(main, "query_llm", fake_query_llm)
    monkeypatch.setattr(main.stat_nz, "get", fake_stat_nz_get)
    return state


def test_report_requires_a_question():
    response = client.get("/report")

    assert response.status_code == 422


def test_report_success(pipeline):
    response = client.get("/report", params={"q": "house owners in Tasman"})
    body = response.json()

    assert response.status_code == 200
    assert body["success"] is True
    assert body["question"] == "house owners in Tasman"
    assert body["selected_dataset"]["id"] == "CEN23_HOU_001"
    assert body["data"] == pipeline["statistic_data"]
    assert body["model"] == "openai/gpt-oss-20b"
    assert body["tier"] == "faster"
    assert pipeline["calls"]["query_llm"] == [("house owners in Tasman", "CEN23_HOU_001")]
    assert pipeline["calls"]["stat_nz"] == [URL + "&format=jsondata"]


def test_report_returns_token_totals(pipeline):
    tokens = client.get("/report", params={"q": "house owners in Tasman"}).json()["tokens"]

    assert tokens["input"] == 580 + 700
    assert tokens["output"] == 60 + 150
    assert tokens["cached"] == 100
    assert tokens["reasoning"] == 130
    assert tokens["steps"] == {"analyse_query": CLASSIFIER_USAGE, "query_llm": QUERY_USAGE}


def test_low_confidence_stops_before_url_step(pipeline):
    pipeline["analysis"] = {"selected_dataset_id": "CEN23_HOU_001", "selection_confidence": 0.3, "usage": CLASSIFIER_USAGE}

    body = client.get("/report", params={"q": "black holes"}).json()

    assert body["success"] is False
    assert body["selected_dataset"] == ""
    assert body["message"] == "Unfortunately we can't provide any data for your question."
    assert body["tokens"]["input"] == 580
    assert pipeline["calls"]["query_llm"] == []
    assert pipeline["calls"]["stat_nz"] == []


def test_no_dataset_stops_before_url_step(pipeline):
    pipeline["analysis"] = {"selected_dataset_id": None, "selection_confidence": 0.0, "usage": CLASSIFIER_USAGE}

    body = client.get("/report", params={"q": "black holes"}).json()

    assert body["success"] is False
    assert pipeline["calls"]["query_llm"] == []


def test_llm_error_is_passed_to_user(pipeline):
    pipeline["query_result"] = {"success": False, "message": "Year 1990 is not available",
                                "model": "openai/gpt-oss-20b", "tier": "faster", "usage": QUERY_USAGE}

    body = client.get("/report", params={"q": "house owners in 1990"}).json()

    assert body["success"] is False
    assert body["message"] == "Year 1990 is not available"
    assert pipeline["calls"]["stat_nz"] == []


def test_statsnz_failure(pipeline):
    pipeline["statistic_data"] = None

    body = client.get("/report", params={"q": "house owners in Tasman"}).json()

    assert body["success"] is False
    assert body["message"] == "No data retrieved. Please try again later."
    assert body["URL"] == URL


@pytest.fixture
def report_dir(tmp_path, monkeypatch):
    """ A temporary exports folder with one report, and a secret file next to it """
    exports = tmp_path / "exports"
    exports.mkdir()
    (exports / "report.csv").write_text("region,count\nTasman,1290\n")
    (tmp_path / ".env").write_text("STAT_NZ_API_KEY=secret")
    monkeypatch.setattr(main, "REPORT_DIR", str(exports))
    return exports


def test_download_existing_report(report_dir):
    response = client.get("/download", params={"filename": "report.csv"})

    assert response.status_code == 200
    assert "Tasman,1290" in response.text


def test_download_missing_report(report_dir):
    response = client.get("/download", params={"filename": "nope.csv"})

    assert response.status_code == 404


@pytest.mark.parametrize("filename", ["../.env", "..\\.env", "../exports/../.env"])
def test_download_cannot_escape_report_folder(report_dir, filename):
    response = client.get("/download", params={"filename": filename})

    assert response.status_code == 404
    assert "secret" not in response.text