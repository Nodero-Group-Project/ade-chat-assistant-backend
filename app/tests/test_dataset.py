import pytest
from unittest.mock import patch

from app.db import Dataset
from app.main import dataset_get,dataset_add,dataset_edit,dataset_remove

@pytest.mark.asyncio
@patch("app.main.dataset_add")
async def test_dataset_add(mock):

    dataset = Dataset(
        Id="000_DATASET_FOR_TEST_ID",
        Name="dataset_name",
        Description="dataset_description",
        Skill="dataset_skill",
        Filters="dataset_filters"
    )

    result = await dataset_add(dataset)

    assert result == {
        "success": True,
        "message": 'The dataset added successfully.'
    }

@pytest.mark.asyncio
@patch("app.main.dataset_add")
async def test_dataset_exists(mock):

    dataset = Dataset(
        Id="000_DATASET_FOR_TEST_ID",
        Name="dataset_name",
        Description="dataset_description",
        Skill="dataset_skill",
        Filters="dataset_filters"
    )

    result = await dataset_add(dataset)

    assert result == {
        "success": False,
        "message": 'The dataset already exists.'
    }

@pytest.mark.asyncio
@patch("app.main.dataset_edit")
async def test_dataset_edit(mock):

    dataset = Dataset(
        Id="000_DATASET_FOR_TEST_ID",
        Name="dataset_name_updated",
        Description="dataset_description_updated",
        Skill="dataset_skill_updated",
        Filters="dataset_filters_updated"
    )

    result = await dataset_edit(dataset)

    assert result == {
        "success": True,
        "message": "Dataset edited successfully."
    }

@pytest.mark.asyncio
@patch("app.main.dataset_remove")
async def test_dataset_remove(mock):

    result = await dataset_remove("000_DATASET_FOR_TEST_ID")

    assert result == {
        "success": True,
        "message": "Dataset removed successfully."
    }


@pytest.mark.asyncio
@patch("app.main.dataset_remove")
async def test_dataset_remove_not_exist(mock):
    result = await dataset_remove("000_DATASET_FOR_TEST_ID")

    assert result == {
        "success": False,
        "message": "Cannot remove the dataset."
    }


@pytest.mark.asyncio
@patch("app.main.dataset_edit")
async def test_dataset_edit_not_exist(mock):

    dataset = Dataset(
        Id="000_DATASET_FOR_TEST_ID",
        Name="dataset_name_updated",
        Description="dataset_description_updated",
        Skill="dataset_skill_updated",
        Filters="dataset_filters_updated"
    )

    result = await dataset_edit(dataset)

    assert result == {
        "success": False,
        "message": "Cannot edit the dataset."
    }

