Fasts test:
uv run pytest

Add -v to see each test's name and result:
uv run pytest -v

Run one file:
uv run pytest app/tests/test_api.py

Run one test:
uv run pytest app/tests/test_api.py::test_report_success

Run tests whose names match a keyword:
uv run pytest -k download

Include the live end-to-end tests:
uv run pytest --live

Show print output such as the [usage] and [routing] lines:
uv run pytest -s