from app.db import dataset_get_all, intent_get_all

def datasets():
    return [
        {
            "id": dataset.Id,
            "name": dataset.Name,
            "description": dataset.Description
        }
        for dataset in dataset_get_all()
    ]


def intents():
    return [
        intent.Description

        for intent in intent_get_all()
    ]