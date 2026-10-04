"""
Queries Groq to convert a user's question into a StatsNZ API URL,
routing to a model tier based on the intent classification result.
"""

import os
from groq import Groq
from app.prompts import cigarette_smoking,household_income,telecommunication_system,education,activity_limitations
from app.heuristic_router import heuristic_tier
from app.llm_usage import log_usage

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


MODELS = {
    "expert": "openai/gpt-oss-120b",
    "faster": "openai/gpt-oss-20b",
    "vision": "qwen/qwen3.8-27b"
}

def select_model(user_query: str, dataset: dict) -> str:
    """ Route to a Groq model using the heuristic router """
    tier = heuristic_tier(user_query, dataset)
    model = MODELS[tier]
    print(f"[routing] tier={tier} model={model} query={user_query!r}")
    return tier,model
    
# Query the LLM to convert a user query into an API URL
def query_llm(user_query: str, dataset: dict):
    # select an appropriate prompt depends on selected dataset
    match dataset["id"]:
        case "CEN23_HAD_020":
            prompt = cigarette_smoking.prompt()
        case "CEN23_HOU_001":
            prompt = household_income.prompt()
        case "CEN23_FHH_017":
            prompt = telecommunication_system.prompt()
        case "CEN23_EDU_003":
            prompt = education.prompt()
        case "CEN23_HAD_014":
            prompt = activity_limitations.prompt()
        case _:
            return {"success": False, "message": f"No prompt configured for dataset {dataset['id']}", "model": None, "tier": None}

    tier, model = select_model(user_query, dataset)

    # Ask the LLM to create a URL for the selected dataset
    completion = client.chat.completions.create(
        # model="qwen/qwen3.8-27b",
        model=model,
        reasoning_format="hidden",
        # Mapping a question to codes is simple; low effort cuts billed reasoning tokens
        reasoning_effort="low",
        max_completion_tokens=4096,
        # Static system prompt first so Groq can reuse the cached prefix
        messages=[
            {"role": "system", "content": prompt },
            {"role": "user", "content": user_query},
        ],

    )

    usage = log_usage("query_llm", model, completion)

    result = (completion.choices[0].message.content or "").strip()

    print(result)

    # if LLM generates URL
    if result.startswith("API_URL"):
        return {
            "success": True,
            "URL": result.replace("API_URL:", ""),
            "model": model,
            "tier": tier,
            "usage": usage
        }
    # if LLM generates ERROR
    elif result.startswith("ERROR"):
        return {
            "success": False,
            "message":result.replace("ERROR:", ""),
            "model": model,
            "tier": tier,
            "usage": usage
        }
    # here is where the LLM generate nothing. Neither URL nor ERROR
    # because of token limitation, or any other unknown reason.
    else:
        return {
            "success": False,
            "message":"No data found. Please try again later.",
            "model": model,
            "tier": tier,
            "usage": usage
        }

