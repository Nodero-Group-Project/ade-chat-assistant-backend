from types import SimpleNamespace

from app.llm_usage import EMPTY_USAGE, combine_usage, log_usage
from app.tests.fakes import make_completion

def test_log_usage_reads_all_counts():
    completion = make_completion("x", prompt_tokens=500, completion_tokens=80, cached_tokens=300, reasoning_tokens=50)
    
    assert log_usage("step", "model", completion) == {"input": 500, "cached": 300, "output": 80, "reasoning": 50}
    
def test_log_usage_without_token_details():
    completion = make_completion("x", prompt_tokens=500, completion_tokens=80)
    completion.usage = SimpleNamespace(
        prompt_tokens=500, completion_tokens=80,
        prompt_tokens_details=None, completion_tokens_details=None,
    )
    
    assert log_usage("step", "model", completion) == {"input": 500, "cached": 0, "output": 80, "reasoning": 0}
    
def test_log_usage_without_returns_zeros():
    completion = make_completion("x", with_usage=False)
    
    assert log_usage("step", "model", completion) == EMPTY_USAGE
    
def test_log_usage_does_not_share_the_empty_dict():
    tokens = log_usage("step", "model", make_completion("x", with_usage=False))
    tokens["input"] = 999
    
    assert EMPTY_USAGE["input"] == 0
    
def test_combine_usage_sums_steps():
    first = {"input": 500, "cached": 100, "output": 50, "reasoning": 30}
    second = {"input": 700, "cached": 0, "output": 150, "reasoning": 100}
    
    combined = combine_usage(analyse_query=first, query_llm=second)
    
    assert combined["input"] == 1200
    assert combined["cached"] == 100
    assert combined["output"] == 200
    assert combined["reasoning"] == 130
    assert combined["steps"] == {"analyse_query": first, "query_llm": second}
    
def test_combine_usage_skips_missing_steps():
    first = {"input": 500, "cached": 0, "output": 50, "reasoning": 30}
    
    combined = combine_usage(analyse_query=first, query_llm=None)
    
    assert combined["input"] == 500
    assert list(combined["steps"].keys()) == ["analyse_query"]
    
def test_combine_usage_with_nothing():
    assert combine_usage() == {**EMPTY_USAGE, "steps": {}}
    
    