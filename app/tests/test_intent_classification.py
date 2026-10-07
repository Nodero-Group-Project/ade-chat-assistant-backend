"""
Tests for analyse_query's handling of LLM replies, using a fake Groq client.
"""

import json

from app import intent_classification


def reply(dataset_id, confidence):
    return json.dumps({"dataset_id": dataset_id, "confidence": confidence})


def test_valid_dataset_is_selected(fake_groq):
    fake_groq(intent_classification, reply("CEN23_HOU_001", 0.9), prompt_tokens=580)

    result = intent_classification.analyse_query("house owners in Tasman")

    assert result["selected_dataset_id"] == "CEN23_HOU_001"
    assert result["selection_confidence"] == 0.9
    assert result["usage"]["input"] == 580


def test_null_dataset_means_no_match(fake_groq):
    fake_groq(intent_classification, reply(None, 0.0))

    result = intent_classification.analyse_query("black holes near the sun")

    assert result["selected_dataset_id"] is None
    assert result["selection_confidence"] == 0.0


def test_invented_dataset_id_is_rejected(fake_groq):
    fake_groq(intent_classification, reply("MADE_UP_123", 0.99))

    result = intent_classification.analyse_query("house owners in Tasman")

    assert result["selected_dataset_id"] is None
    assert result["selection_confidence"] == 0.0


def test_invalid_json_returns_error(fake_groq):
    fake_groq(intent_classification, "I think it's the household dataset", finish_reason="length")

    result = intent_classification.analyse_query("house owners in Tasman")

    assert result["selected_dataset_id"] is None
    assert result["selection_confidence"] == 0.0
    assert result["error"] == "Failed to parse JSON from LLM response."
    assert result["finish_reason"] == "length"
    assert "usage" in result


def test_empty_reply_returns_error(fake_groq):
    fake_groq(intent_classification, None)

    result = intent_classification.analyse_query("house owners in Tasman")

    assert result["selected_dataset_id"] is None
    assert "error" in result


def test_missing_confidence_counts_as_zero(fake_groq):
    fake_groq(intent_classification, json.dumps({"dataset_id": "CEN23_HOU_001"}))

    result = intent_classification.analyse_query("house owners in Tasman")

    assert result["selection_confidence"] == 0.0


def test_numeric_string_confidence_is_parsed(fake_groq):
    fake_groq(intent_classification, reply("CEN23_HOU_001", "0.8"))

    result = intent_classification.analyse_query("house owners in Tasman")

    assert result["selection_confidence"] == 0.8


def test_non_numeric_confidence_counts_as_zero(fake_groq):
    # A malformed confidence should mean "not confident", not crash the request
    fake_groq(intent_classification, reply("CEN23_HOU_001", "high"))

    result = intent_classification.analyse_query("house owners in Tasman")

    assert result["selection_confidence"] == 0.0


def test_request_uses_json_mode_and_small_model(fake_groq):
    client = fake_groq(intent_classification, reply("CEN23_HOU_001", 0.9))

    intent_classification.analyse_query("house owners in Tasman")

    kwargs = client.chat.completions.create.call_args.kwargs
    assert kwargs["model"] == "openai/gpt-oss-20b"
    assert kwargs["response_format"] == {"type": "json_object"}
    assert kwargs["reasoning_effort"] == "low"
    assert kwargs["messages"][0]["content"] == intent_classification.SYSTEM_PROMPT


def test_system_prompt_lists_every_dataset():
    from app.datasets import datasets

    for dataset in datasets():
        assert dataset["id"] in intent_classification.SYSTEM_PROMPT
