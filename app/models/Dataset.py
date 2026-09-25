from pydantic import BaseModel

class Dataset(BaseModel):
    Id: str
    Name: str
    Description: str
    Skill: str