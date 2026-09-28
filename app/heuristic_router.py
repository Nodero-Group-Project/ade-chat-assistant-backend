"""
Rule-based router for choosing a groq model
"""

import re

# Words/phrases that suggest the query needs multi-field comparison
EXPERT_SIGNAL_WORDS = [
    "compare", "comparison", "versus", " vs ", "vs.",
    "difference between", "relationship between",
    "correlat", "trend over", "change over time",
    "breakdown by", "cross-tabulate", "cross tab",
    "percentage of", "proportion of",
    "by region and", "by age and", "by gender and",
]

# Words that suggest a simple, single fact lookup
SIMPLE_SIGNAL_WORDS = [
    "what is", "who is", "when is", "where is",
    "how many", "how much", "total", "number of",
    "amount of", "count of",
]

def heuristic_tier(user_query: str, dataset: dict | None = None) -> str:
    """
    Decide "faster" or "expert" purely from he text of the query
    """
    
    query = user_query.lower().strip()
    
    if not query:
        # Empty/missing query - let the expert model handle it
        return "expert"

    word_count = len(query.split())
    
    # Signal 1: explicit comparison / correlation
    if any(signal in query for signal in EXPERT_SIGNAL_WORDS):
        return "expert"
    
    # Signal 2: multiple conjunctions suggest multiple entries/filters stacked together
    conjunction_count = len(re.findall(r"\band\b", query))
    if conjunction_count >= 2:
        return "expert"
    
    # Signal 3: long queries tend to carry more clauses/conditions
    if word_count > 25:
        return "expert"
    
    # Signal 4: questions marks stacked, or multiple sentences suggest complexity
    if query.count("?") > 1 or query.count(".") > 1:
        return "expert"
    
    # Signal 5: simple lookup phrasing
    if any(signal in query for signal in SIMPLE_SIGNAL_WORDS) and word_count <= 15:
        return "faster"

    # Default
    return "faster"
    