import pytest
from unittest.mock import patch


@pytest.mark.asyncio
@patch("main.analyse_query")
async def test_report_no_dataset(mock_analyse_query):

    mock_analyse_query.return_value = {
        "selected_dataset_id": None
    }

    question = "Is there any black hole near the solar system?"

    result = await report(question)

    assert result == {
        "success": False,
        "question": question,
        "selected_dataset": "",
        "message": "Unfortunately we can't provide any data for your question."
    }
