"""
Logs Groq token usage so we can see where input/output token costs come from.
"""


def log_usage(label: str, model: str, completion) -> None:
    """ Print prompt, cached, completion and reasoning token counts for a Groq completion """
    usage = completion.usage
    if usage is None:
        print(f"[usage] {label} model={model} usage=unavailable")
        return

    cached = usage.prompt_tokens_details.cached_tokens if usage.prompt_tokens_details else 0
    reasoning = usage.completion_tokens_details.reasoning_tokens if usage.completion_tokens_details else 0

    print(
        f"[usage] {label} model={model} "
        f"prompt={usage.prompt_tokens} cached={cached} "
        f"completion={usage.completion_tokens} reasoning={reasoning} "
        f"total={usage.total_tokens}"
    )
