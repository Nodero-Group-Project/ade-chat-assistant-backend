"""
Tests for query_llm's handling of LLM replies, using a fake Groq client.
"""

from app import llm_query

HOUSEHOLD = {"id": "CEN23_HOU_001"}
URL = "https://api.data.stats.govt.nz/rest/data/STATSNZ,CEN23_HOU_001,1.0/2023.16.99.8.001?dimensionAtObservation=AllDimensions"

def test_url_reply_is_returned(fake_groq):
    fake_groq(llm_query, f"API_URL: {URL}", prompt_tokens=700, completion_tokens=150)
    
    result = llm_query.query_llm("house owners in Tasman", HOUSEHOLD)
    
    assert result["success"] is True
    assert result["url"] == URL
    assert result["usage"]["input"] == 700
    assert result["usage"]["output"] == 150
    
def test_url_reply_with_space_after_prefix(fake_groq):
    fake_groq(llm_query, f"API_URL:  {URL}")
    
    result = llm_query.query_llm("house owners in Tasman", HOUSEHOLD)
    
    assert result["url"] == URL
    
def test_error_reply_results_reason(fake_groq):
    fake_groq(llm_query, "ERROR: Year 1990 is not available")
    
    result = llm_query.query_llm("house owners in 1990", HOUSEHOLD)
    
    assert result["success"] is False
    assert result["reason"] == "Year 1990 is not available"
    assert "usage" in result
    
def test_unexpected_reply_returns_fallback_message(fake_groq):
    fake_groq(llm_query, "Sure! Here is a poem about income...")
    
    result = llm_query.query_llm("write a peom", HOUSEHOLD)
    
    assert result["success"] is False
    assert result["message"] == "No data found. Please try again later."
    
def test_empty_reply_returns_fallback_message(fake_groq):
    fake_groq(llm_query, None)
    
    result = llm_query.query_llm("house owners in Tasman", HOUSEHOLD)
    
    assert result["success"] is False
    assert result["message"] == "No data found. Please try again later."
    
def test_unknown_dataset_does_not_call_groq(fake_groq):
    client = fake_groq(llm_query, f"API_URL: {URL}")
    
    result = llm_query.query_llm("anything", {"id": "NOT_A_DATASET"})
    
    assert result["success"] is False
    assert "No prompt configured" in result["message"]
    client.chat.completions.create.assert_not_called()

def test_simple_question_uses_faster_model(fake_groq):
    client = fake_groq(llm_query, f"API_URL: {URL}")
    
    result = llm_query.query_llm("how many house owners in Tasman", HOUSEHOLD)
    
    assert result["tier"] == "faster"
    assert client.chat.completions.create.call_args.kwargs["model"] == llm_query.MODELS["faster"]
    
def test_comparison_question_uses_expert_model(fake_groq):
    client = fake_groq(llm_query, f"API_URL: {URL}")
    
    result = llm_query.query_llm("compare house owners in Tasman and Nelson", HOUSEHOLD)
    
    assert result["tier"] == "expert"
    assert client.chat.completions.create.call_args.kwargs["model"] == llm_query.MODELS["expert"]
    
def test_request_keeps_token_saving_settings(fake_groq):
    client = fake_groq(llm_query, f"API_URL: {URL}")
    
    result = llm_query.query_llm("house owners in Tasman", HOUSEHOLD)
    
    kwargs = client.chat.completions.create.call_args.kwargs
    assert kwargs["reasoning_effort"] == "low"
    # Static system prompt first (cacheable), user question second (not cacheable)
    assert [message["role"] for message in kwargs["messages"]] == ["system", "user"]
    assert kwargs["messages"][1]["content"] == "house owners in Tasman"