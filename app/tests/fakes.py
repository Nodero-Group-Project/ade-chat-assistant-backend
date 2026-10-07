"""
Fake objects shared by the tests.
"""

from types import SimpleNamespace

def make_completion(content, prompt_tokens=100, completion_tokens=20, cached_tokens=0, reasoning_tokens=10, finish_reason="stop", with_usage=True):
    """ Build an object shaped like a Groq chat completion """
    usage = SimpleNamespace(
        prompt_tokens=prompt_tokens,
        completion_tokens=completion_tokens,
        prompt_tokens_details=SimpleNamespace(cached_tokens=cached_tokens),
        completion_tokens_details=SimpleNamespace(reasoning_tokens=reasoning_tokens),
    )
    return SimpleNamespace(
        choices=[SimpleNamespace(message=SimpleNamespace(content=content),
        finish_reason=finish_reason)],
        usage=usage if with_usage else None
    )
