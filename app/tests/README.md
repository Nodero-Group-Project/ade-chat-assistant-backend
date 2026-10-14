# Backend tests
 
The test suite for the ADE Chat Assistant backend. It currently has **84 tests in 9 files**.:

- **Unit and HTTP tests**  run by default. Groq and StatsNZ are blocked and replaced byt fakes, so these are fast, free, and give the same results every run.
- **Live tests** ('test_report.py') call the real Groq and StatsNZ APIs end to end. They cost tokens, and becasue LLM output can vary between runs they only run when asked for '--live'.

## Running the tests

All commands run from the backend root ('ade-chat-assistant-backend/').

| Command | What it does |
|---|---|
| `uv run pytest` | Run every non-live test |
| `uv run pytest -v` | Show each test's name and result |
| `uv run pytest app/tests/test_api.py` | Run one file |
| `uv run pytest app/tests/test_api.py::test_report_success` | Run one test |
| `uv run pytest -k router` | Run tests whose names match a keyword |
| `uv run pytest --live` | Include the live end-to-end tests |
| `uv run pytest -s` | Show print output, such as the `[usage]` and `[routing]` lines |
| `uv run pytest --cov=app --cov-report=term-missing` | Show code coverage, including which lines aren't tested |
| `uv run pytest --cov=app --cov-report=html` | Write a coverage report to `htmlcov/index.html` |

pytest settings live in 'pyproject.toml' under the `[tool.pytest.ini_options]` section.

### Requirements

- **'app/.env' with 'CONNECTION_STRING':** needed even for the non-live tests. 'intent_classification.py' builds its dataset list from the database when it's imported and 'test_prompt.py' reads the dataset IDs from the database to parametrize its tests.
- **'GROQ_API_KEY' and 'STAT_NZ_API_KEY':** only needed for '--live'. 'conftest.py' sets a dummy Groq key so the clients can be created without one

## Shared setup

### 'conftest.py'

| Item | Purpose |
|---|---|
| `--live` option | Adds the `--live` flag. Without it, every test marked `@pytest.mark.live` is skipped. |
| `block_real_apis` (autouse fixture) | For every non-live test, replaces both Groq clients and `urllib.request.urlopen` with versions that raise `AssertionError`. A test that accidentally reaches a real API fails loudly instead of quietly costing tokens. |
| `fake_groq` fixture | `fake_groq(module, content, **kwargs)` swaps a module's Groq client for a mock that returns `content`. It returns the mock, so tests can check what was sent, e.g. which model was used. |

### `fakes.py`

`make_completion(content, prompt_tokens=100, completion_tokens=20, cached_tokens=0, reasoning_tokens=10, finish_reason="stop", with_usage=True)` builds an object shaped like a Groq chat completion, including token usage.

## Test files

### `test_intent_classification.py` – dataset selection (10 tests)

Tests `analyse_query`, the first LLM step that picks a dataset for the question.

| Test | Checks that |
|---|---|
| `test_valid_dataset_is_selected` | A valid dataset ID and confidence are returned along with token usage |
| `test_null_dataset_means_no_match` | `null` from the LLM means no dataset and 0 confidence |
| `test_invented_dataset_id_is_rejected` | An ID that isn't in the database is ignored, even with high confidence |
| `test_invalid_json_returns_error` | Non-JSON replies return an error, the finish reason and usage, with no dataset |
| `test_empty_reply_returns_error` | An empty reply returns an error |
| `test_missing_confidence_counts_as_zero` | No confidence means 0 |
| `test_numeric_string_confidence_is_parsed` | `"0.8"` is read as 0.8 |
| `test_non_numeric_confidence_counts_as_zero` | `"high"` counts as 0 instead of crashing |
| `test_request_uses_json_mode_and_small_model` | The call uses `gpt-oss-20b`, JSON mode, low reasoning effort and the cached system prompt |
| `test_system_prompt_lists_every_dataset` | Every dataset in the database appears in the system prompt |

### `test_model_router.py` – model routing (15 tests)

One parametrized test, `test_heuristic_tier`, runs `heuristic_tier` against 15 questions:

| Signal | Example | Tier |
|---|---|---|
| Empty or blank question | `""`, `"   "` | expert |
| Comparison words (case-insensitive) | `compare smoking rates in Auckland`, `smokers vs non smokers in Otago` | expert |
| Two or more "and"s | `smokers in Auckland and Otago and Canterbury` | expert |
| One "and" | `smokers in Auckland and Otago` | faster |
| "and" inside a word isn't counted | `smokers in Auckland, Rotorua` | faster |
| More than 25 words | 26 words | expert (25 words → faster) |
| Several questions | `How many smokers? Where?` | expert |
| Simple lookup | `How many smokers in Otago` | faster |

### `test_llm_query.py` – URL generation (9 tests)

Tests `query_llm`, the second LLM step that turns the question into a StatsNZ URL.

| Test | Checks that |
|---|---|
| `test_url_reply_is_returned` | `API_URL: <url>` returns success, the URL and token usage |
| `test_url_reply_with_space_after_prefix` | Extra spaces after `API_URL:` are removed |
| `test_error_reply_results_reason` | `ERROR: <reason>` returns the reason as the message |
| `test_unexpected_reply_returns_fallback_message` | Any other reply returns `No data found. Please try again later.` |
| `test_empty_reply_returns_fallback_message` | An empty reply returns the same fallback message |
| `test_unknown_dataset_does_not_call_groq` | An unknown dataset doesn't call Groq (**out of date**, see [Known failures](#known-failures)) |
| `test_simple_question_uses_faster_model` | Simple questions use the `faster` model |
| `test_comparison_question_uses_expert_model` | Comparison questions use the `expert` model |
| `test_request_keeps_token_saving_settings` | Low reasoning effort, with the system prompt first (cacheable) and the question second |

### `test_prompts.py` – dataset Skill prompts (15 tests)

Three checks, each run once for every dataset in the database (5 datasets → 15 tests). They catch copy-paste mistakes between dataset prompts.

| Test | Checks that |
|---|---|
| `test_prompt_url_template_uses_its_own_dataset` | The URL template contains this dataset's ID and no other |
| `test_prompt_defines_the_output_format` | The prompt mentions both `API_URL:` and `ERROR:` |
| `test_prompt_has_no_duplicate_codes_within_a_dimension` | No code appears twice under the same dimension heading |

### `test_llm_usage.py` – token tracking (7 tests)

| Test | Checks that |
|---|---|
| `test_log_usage_reads_all_counts` | Input, cached, output and reasoning tokens are all read |
| `test_log_usage_without_token_details` | Missing cached/reasoning details count as 0 |
| `test_log_usage_without_returns_zeros` | No usage at all returns zeros |
| `test_log_usage_does_not_share_the_empty_dict` | Changing a returned dict doesn't change `EMPTY_USAGE` |
| `test_combine_usage_sums_steps` | Totals are summed across steps, with a per-step breakdown |
| `test_combine_usage_skips_missing_steps` | Steps passed as `None` are left out |
| `test_combine_usage_with_nothing` | No steps returns zeros and an empty breakdown |

### `test_stat_nz.py` – StatsNZ client (4 tests)

`urlopen` is replaced with fakes.

| Test | Checks that |
|---|---|
| `test_missing_api_key_skips_request` | No request is made without `STAT_NZ_API_KEY` |
| `test_successful_response_is_parsed` | JSON is parsed and the subscription key header is sent |
| `test_http_error_returns_none` | HTTP errors (e.g. 401) return `None` |
| `test_connection_error_returns_none` | Network errors return `None` |

### `test_api.py` – HTTP endpoints (12 tests)

Uses FastAPI's `TestClient`. The `pipeline` fixture mocks both LLM steps and StatsNZ, and records what they were called with.

| Test | Checks that |
|---|---|
| `test_report_requires_a_question` | `/report` without `q` returns 422 |
| `test_report_success` | A full success response, and that StatsNZ is called with `&format=jsondata` |
| `test_report_returns_token_totals` | Tokens are summed across both LLM steps |
| `test_low_confidence_stops_before_url_step` | Confidence < 0.5 stops before URL generation and StatsNZ |
| `test_no_dataset_stops_before_url_step` | No dataset stops before URL generation |
| `test_llm_error_is_passed_to_user` | The LLM's `ERROR:` reason reaches the user, and StatsNZ isn't called |
| `test_statsnz_failure` | A StatsNZ failure returns the message and the generated URL |
| `test_download_existing_report` | `/download` returns an existing CSV |
| `test_download_missing_report` | `/download` returns 404 for a missing file |
| `test_download_cannot_escape_report_folder` (×3) | `../.env`-style paths can't read files outside `exports/` |

### `test_dataset.py` – dataset admin endpoints (6 tests)

Calls the `/dataset` endpoint functions directly with a test dataset, `000_DATASET_FOR_TEST_ID`.

| Test | Checks that |
|---|---|
| `test_dataset_add` | A new dataset is added |
| `test_dataset_exists` | Adding the same ID again fails |
| `test_dataset_edit` | The dataset can be edited |
| `test_dataset_remove` | The dataset can be removed |
| `test_dataset_remove_not_exist` | Removing it again fails |
| `test_dataset_edit_not_exist` | Editing a missing dataset fails |

> **These tests use the real database.** `@patch` targets the endpoint names (e.g. `app.main.dataset_add`), but the tests already imported the real functions, so nothing is mocked. They insert and delete a real row, and they only pass when run in file order.

### `test_report.py` – live end-to-end tests (6 tests, `--live` only)

Each test sends a real question through `report()` and checks the selected dataset and the actual StatsNZ numbers.

| Test | Question | Expected dataset |
|---|---|---|
| `test_report_no_dataset` | Black holes near the solar system | none |
| `test_report_education_result` | Bachelor's degree holders living in Auckland, 2018 | `CEN23_EDU_003` (170,514) |
| `test_report_household_result` | Tasman house owners earning over $200k with sink, toilet and fridge | `CEN23_HOU_001` |
| `test_report_telecommunication_result` | Pacific boys in Gisborne with internet access | `CEN23_FHH_017` (408) |
| `test_report_smoking_result` | Asian men under 30 who quit smoking, 2013 | `CEN23_HAD_020` (3,207) |
| `test_report_smoking_no_two_urls` | Smokers and non-smokers in 2023, in one URL | `CEN23_HAD_020` |

> The expected numbers in `test_report_smoking_no_two_urls` were recorded while the smoking prompt mapped "smokers" to code `999`, which StatsNZ labels "Total – cigarette smoking behaviour" (everyone). Check them again after the prompt is fixed.

## Writing new tests

- **Never call real APIs from a normal test.** Use `fake_groq` for Groq and `monkeypatch` for `stat_nz.get` / `urllib.request.urlopen`. `block_real_apis` will fail the test if you forget.
- **Mock the database where it's used,** e.g. `monkeypatch.setattr(main, "dataset_get_by_id", ...)`, not the original in `app.db`, because `main` imported the function by name.
- **Use `@pytest.mark.live`** for anything that needs real Groq or StatsNZ responses, and keep those tests few, since each run costs tokens.
- **Use `@pytest.mark.asyncio`** when calling an `async` endpoint function directly. Use `TestClient` to test over HTTP.
- **Name tests after the behaviour,** e.g. `test_low_confidence_stops_before_url_step`, so a failure explains itself.