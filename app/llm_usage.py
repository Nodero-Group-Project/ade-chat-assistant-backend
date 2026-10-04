"""
Tracks Groq token usage so we can see where input/output token costs come from.
"""

EMPTY_USAGE = {"input": 0, "cached": 0, "output": 0, "reasoning": 0}


def log_usage(label: str, model: str, completion) -> dict:
    """ Print and return input, cached, output and reasoning token counts for a Groq completion """
    usage = completion.usage
    if usage is None:
        print(f"[usage] {label} model={model} usage=unavailable")
        return dict(EMPTY_USAGE)

    tokens = {
        "input": usage.prompt_tokens,
        "cached": usage.prompt_tokens_details.cached_tokens if usage.prompt_tokens_details else 0,
        "output": usage.completion_tokens,
        "reasoning": usage.completion_tokens_details.reasoning_tokens if usage.completion_tokens_details else 0,
    }

    print(
        f"[usage] {label} model={model} "
        f"input={tokens['input']} cached={tokens['cached']} "
        f"output={tokens['output']} reasoning={tokens['reasoning']}"
    )
    return tokens


def combine_usage(**steps: dict | None) -> dict:
    """ Sum token counts across LLM calls, keeping a per-step breakdown """
    steps = {name: usage for name, usage in steps.items() if usage}
    total = {key: sum(usage[key] for usage in steps.values()) for key in EMPTY_USAGE}
    return {**total, "steps": steps}
