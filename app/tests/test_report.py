from unittest import result

import pytest
from unittest.mock import patch
from app.main import report

@pytest.mark.asyncio
@patch("app.main.report")
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

@pytest.mark.asyncio
@patch("app.main.report")
async def test_report_education_result(mock_analyse_query):

    mock_analyse_query.return_value = {
        "selected_dataset_id": None
    }

    question = "how many student hold bachelor in 2018?"

    result = await report(question)

    result_success = result["success"]
    result_question = result["question"]
    result_dataset = result["selected_dataset"]["id"]
    result_data = result["data"]["data"]["dataSets"][0]["observations"]["0:0:0:0:0"][0]

    assert ((result_success == True) and
            (result_question == question) and
            (result_dataset == "CEN23_EDU_003") and
            (407571 == result_data))

@pytest.mark.asyncio
@patch("app.main.report")
async def test_report_household_result(mock_analyse_query):

    mock_analyse_query.return_value = {
        "selected_dataset_id": None
    }

    question = "how many house owners with more than 200 thousand income exists? their house should have sink, toilet and refrigerator."

    result = await report(question)

    result_success = result["success"]
    result_question = result["question"]
    result_dataset = result["selected_dataset"]["id"]
    result_data_1 = result["data"]["data"]["dataSets"][0]["observations"]["0:0:0:0:0"][0]
    result_data_2 = result["data"]["data"]["dataSets"][0]["observations"]["0:0:1:0:0"][0]
    result_data_3 = result["data"]["data"]["dataSets"][0]["observations"]["0:0:2:0:0"][0]

    assert ((result_success == True) and
            (result_question == question) and
            (result_dataset == "CEN23_HOU_001") and
            (147048 == result_data_1) and
            (147084 == result_data_2) and
            (147156 == result_data_3))

@pytest.mark.asyncio
@patch("app.main.report")
async def test_report_telecommunication_result(mock_analyse_query):

    mock_analyse_query.return_value = {
        "selected_dataset_id": None
    }

    question = "I need to know about the children boys from pacific living in southland who can access to the internet."

    result = await report(question)

    result_success = result["success"]
    result_question = result["question"]
    result_dataset = result["selected_dataset"]["id"]
    result_data = result["data"]["data"]["dataSets"][0]["observations"]["0:0:0:0:0:0"][0]

    assert ((result_success == True) and
            (result_question == question) and
            (result_dataset == "CEN23_FHH_017") and
            (459 == result_data))

@pytest.mark.asyncio
@patch("app.main.report")
async def test_report_smoking_result(mock_analyse_query):

    mock_analyse_query.return_value = {
        "selected_dataset_id": None
    }

    question = "Any information about the number of asian men under 30 which leave smoking in 2013?"

    result = await report(question)

    result_success = result["success"]
    result_question = result["question"]
    result_dataset = result["selected_dataset"]["id"]
    result_data = result["data"]["data"]["dataSets"][0]["observations"]["0:0:0:0:0:0"][0]

    assert ((result_success == True) and
            (result_question == question) and
            (result_dataset == "CEN23_HAD_020") and
            (3207 == result_data))
