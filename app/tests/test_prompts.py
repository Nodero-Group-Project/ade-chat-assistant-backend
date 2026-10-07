"""
Sanity checks on the dataset prompts, to catch copy-paste mistakes between datasets.
"""

import re
import pytest
from app import llm_query
from app.datasets import datasets

DATASET_IDS = [dataset.id for dataset in datasets()]

def prompt_for(dataset_id, fake_groq):
    """ Run query_llm with a fake Groq client and return the system prompt it sent """
    client = fake_groq(llm_query, "ERROR:test")
    result = llm_query.query_llm("test question", {"id": dataset_id})
    
    assert not result["message"].startswith("No prompt configured"), f"no prompt for {dataset_id}"
    return client.chat.completions.create.call_args.kwargs["messages"][0]["content"]

@pytest.mark.parametrize("dataset_id", DATASET_IDS)
def test_prompt_url_template_uses_its_own_dataset(dataset_id, fake_groq):
    prompt = prompt_for(dataset_id, fake_groq)
    
    template_ids = re.findall(r"STATSNZ,([A-Z0-9_]+),1\.0/", prompt)
    assert template_ids == [dataset_id]
    

@pytest.mark.parametrize("dataset_id", DATASET_IDS)
def test_prompt_defines_the_output_format(dataset_id, fake_groq):
    prompt = prompt_for(dataset_id, fake_groq)
    
    assert "API_URL:" in prompt
    assert "ERROR:" in prompt
    

@pytest.mark.parametrize("dataset_id", DATASET_IDS)
def test_prompt_has_no_duplicate_codes_within_a_dimension(dataset_id, fake_groq):
    prompt = prompt_for(dataset_id, fake_groq)
    
    section, codes, duplicates = None, {}, []
    for line in prompt.splitlines():
        heading = re.match(r"^([A-Za-z][^:=]*):\s*$", line.strip())
        if heading:
            section, codes = heading.group(1), {}
            continue
        code = re.match(r"^(\S+) = ", line.strip())
        if code and section:
            if code.group(1) in codes:
                duplicates.append(f"{section}: {code.group(1)}")
            codes[code.group(1)] = True
    
    assert duplicates == []
