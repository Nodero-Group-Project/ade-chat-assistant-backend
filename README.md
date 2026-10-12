# Te Kete Aronui - ADE Chat Assistant - Backend

[![Architecture diagram](https://gitdiagram.com/diagram-badge.svg)](https://gitdiagram.com/nodero-group-project/ade-chat-assistant-backend?utm_source=readme&utm_medium=badge)

A FastAPI service that answers plain-English questions with official Aotearoa, New Zealand census data.

A user asks something like *"how many people living in Auckland held a bachelor's degree in 2018?"*. The backend interprets the question with an LLM, picks the most appropriate ADE (Aotearoa Data Explorer) datasets, works out the dimension and filter values, builds a StatsNZ API URL and returns the data.

## How it works

```
 question
    │
    ▼
┌──────────────────────────┐   Groq · gpt-oss-20b · JSON mode
│ 1. Dataset selection     │   "Which dataset can answer this?"  → dataset ID + confidence
│    intent_classification │   Confidence < 0.5 or no match      → stop, "can't provide data"
└────────────┬─────────────┘
             ▼
┌──────────────────────────┐   heuristic_router picks a tier from the question text
│ 2. Model routing         │   simple lookup → faster (gpt-oss-20b)
│    heuristic_router      │   comparison / multi-filter → expert (gpt-oss-120b)
└────────────┬─────────────┘
             ▼
┌──────────────────────────┐   The dataset's Skill prompt (stored in the database) lists every
│ 3. URL generation        │   dimension code. The LLM replies "API_URL: <url>" or "ERROR: <reason>"
│    llm_query             │
└────────────┬─────────────┘
             ▼
┌──────────────────────────┐   GET <url>&format=jsondata with the StatsNZ subscription key
│ 4. Data retrieval        │   Returns SDMX-JSON
│    services/stat_nz      │
└────────────┬─────────────┘
             ▼
      JSON response with the data, dataset info, model/tier used and token usage
```

The LLM interprets the user's intent directly; there is no fixed list of intent categories. It dynamically determines which dataset and model tier are appropriate based on the content of the question. 
Token usage for both LLM calls is logged and returned in the final JSON response.

## Architecture

How the modules depend on each other. Click a node on GitHub to open its file.

```mermaid
flowchart TD

subgraph group_api["API"]
  node_api["FastAPI endpoints<br/>[main.py]"]
end

subgraph group_catalogue["Dataset catalogue"]
  node_dataset_model["Dataset schema<br/>[Dataset.py]"]
  node_catalogue_access["Catalogue access<br/>[datasets.py]"]
  node_dataset_db["Dataset repository<br/>[db.py]"]
end

subgraph group_query["Question processing"]
  node_classification["Dataset selection<br/>[intent_classification.py]"]
  node_routing["Model tier routing<br/>[heuristic_router.py]"]
  node_url_generation["StatsNZ URL generation<br/>[llm_query.py]"]
  node_usage["Token accounting<br/>[llm_usage.py]"]
end

subgraph group_internal_services["Internal services"]
  node_stats_client["Stats NZ client<br/>[stat_nz.py]"]
end

subgraph group_services["External services"]
  node_postgres[("PostgreSQL")]
  node_groq["Groq"]
  node_statsnz["Stats NZ API"]
end

node_user(("Client"))

node_user -->|"submits requests"| node_api
node_api -->|"classifies question"| node_classification
node_classification -->|"loads candidates"| node_catalogue_access
node_catalogue_access -->|"reads datasets"| node_dataset_db
node_dataset_db -->|"reads and writes"| node_postgres
node_api -->|"loads selected dataset + Skill"| node_dataset_db
node_api -->|"manages datasets"| node_dataset_db
node_api -->|"validates dataset input"| node_dataset_model
node_api -->|"requests URL"| node_url_generation
node_url_generation -->|"selects tier"| node_routing
node_classification -->|"requests classification"| node_groq
node_url_generation -->|"requests URL"| node_groq
node_url_generation -->|"logs tokens"| node_usage
node_classification -->|"logs tokens"| node_usage
node_api -->|"combines usage"| node_usage
node_api -->|"fetches results"| node_stats_client
node_stats_client -->|"sends GET request"| node_statsnz

click node_api "https://github.com/nodero-group-project/ade-chat-assistant-backend/blob/main/app/main.py"
click node_dataset_model "https://github.com/nodero-group-project/ade-chat-assistant-backend/blob/main/app/models/Dataset.py"
click node_catalogue_access "https://github.com/nodero-group-project/ade-chat-assistant-backend/blob/main/app/datasets.py"
click node_dataset_db "https://github.com/nodero-group-project/ade-chat-assistant-backend/blob/main/app/db.py"
click node_classification "https://github.com/nodero-group-project/ade-chat-assistant-backend/blob/main/app/intent_classification.py"
click node_routing "https://github.com/nodero-group-project/ade-chat-assistant-backend/blob/main/app/heuristic_router.py"
click node_url_generation "https://github.com/nodero-group-project/ade-chat-assistant-backend/blob/main/app/llm_query.py"
click node_usage "https://github.com/nodero-group-project/ade-chat-assistant-backend/blob/main/app/llm_usage.py"
click node_stats_client "https://github.com/nodero-group-project/ade-chat-assistant-backend/blob/main/app/services/stat_nz.py"

classDef toneBlue fill:#dbeafe,stroke:#2563eb,stroke-width:1.5px,color:#172554
classDef toneAmber fill:#fef3c7,stroke:#d97706,stroke-width:1.5px,color:#78350f
classDef toneMint fill:#dcfce7,stroke:#16a34a,stroke-width:1.5px,color:#14532d
classDef toneRose fill:#ffe4e6,stroke:#e11d48,stroke-width:1.5px,color:#881337
classDef toneTeal fill:#ccfbf1,stroke:#0f766e,stroke-width:1.5px,color:#134e4a
class node_api,node_user toneBlue
class node_dataset_model,node_catalogue_access,node_dataset_db toneAmber
class node_classification,node_routing,node_url_generation,node_usage toneMint
class node_stats_client toneTeal
class node_postgres,node_groq,node_statsnz toneRose
```

| Layer | Modules | Responsibility |
|---|---|---|
| API | `main.py` | Receives requests, runs the question pipeline, and serves the dataset admin endpoints |
| Dataset catalogue | `models/Dataset.py`, `datasets.py`, `db.py` | Validates dataset input and reads/writes the `dataset` table |
| Question processing | `intent_classification.py`, `heuristic_router.py`, `llm_query.py`, `llm_usage.py` | Picks the dataset, chooses the model, builds the StatsNZ URL and tracks tokens |
| Internal services | `services/stat_nz.py` | Calls the StatsNZ API with the subscription key |
| External services | PostgreSQL, Groq, StatsNZ API | Storage, LLM inference and census data |

An interactive version of this diagram is on [GitDiagram](https://gitdiagram.com/nodero-group-project/ade-chat-assistant-backend).

## Tech Stack

| | |
|---|---|
| Language | Python 3.14 |
| Web framework | FastAPI |
| LLM provider | [Groq](https://console.groq.com) (`openai/gpt-oss-20b`, `openai/gpt-oss-120b`) |
| Data source | [StatsNZ Aotearoa Data Explorer API](https://api.data.stats.govt.nz) |
| Database | PostgreSQL (via `psycopg` 3) – stores datasets and their prompts |
| Package manager | [uv](https://docs.astral.sh/uv/) |
| Tests | pytest, pytest-asyncio, pytest-cov |

## Project Structure

```
ade-chat-assistant-backend/
├── app/
│   ├── main.py                    # FastAPI app and all endpoints
│   ├── intent_classification.py   # Step 1: picks the dataset for a question
│   ├── heuristic_router.py        # Step 2: chooses the faster or expert model
│   ├── llm_query.py               # Step 3: turns the question into a StatsNZ URL
│   ├── llm_usage.py               # Token usage logging and totals
│   ├── datasets.py                # Dataset list used by dataset selection
│   ├── db.py                      # PostgreSQL queries for the dataset table
│   ├── models/
│   │   └── Dataset.py             # Pydantic request model for the dataset endpoints
│   ├── services/
│   │   └── stat_nz.py             # Step 4: StatsNZ API client
│   ├── tests/                     # Test suite – see app/tests/README.md
│   └── .env                       # Your local secrets (not committed)
├── exports/                       # Exported CSV reports (not committed)
├── pyproject.toml                 # Dependencies and pytest configuration
├── requirements.txt
└── uv.lock
```

## Getting started