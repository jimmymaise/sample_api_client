from pydantic import BaseModel, Field
from utils.common import Common


class Document(BaseModel):
    candidate_id: int = Field()
    file_name: str = Field()
    file_id: int = Field(alias='fileID')
    file_type: int = Field()
    file_type_name: str = Field()
    file_expiration: int = Field()
    file_created: int = Field()

    class Config:
        allow_population_by_field_name = True
        alias_generator = Common.to_camel
