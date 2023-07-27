from typing import Optional

from pydantic import BaseModel, Field
from utils.common import Common


class Note(BaseModel):
    candidate_id: int = Field()
    note: str
    note_type: int = Field()
    note_type_name: Optional[str] = Field(None)
    entered_by: Optional[int] = Field(None, alias='enteredby')
    note_id: int = Field()
    entered_time: Optional[int] = Field(None)

    class Config:
        allow_population_by_field_name = True
        alias_generator = Common.to_camel
