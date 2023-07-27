from typing import AsyncGenerator, Union, Any, Optional, TypeVar, Generic, List
from pydantic import BaseModel, Field
from utils.common import Common
from models.document import Document
from models.note import Note
from api_client.api_client import ApiClient

T = TypeVar('T')


class PageResponse(BaseModel, Generic[T]):
    page_number: int
    total_count: int
    data: List[T]

    class Config:
        populate_by_name = True
        alias_generator = Common.to_camel
        arbitrary_types_allowed = True


class NoteInsertRequestInput(BaseModel):
    candidate_id: int
    note: str
    note_type: int

    class Config:
        populate_by_name = True
        alias_generator = Common.to_camel
        arbitrary_types_allowed = True


class Candidate(BaseModel):
    candidate_id: Optional[int] = Field(default=None)
    first_name: str
    last_name: str
    email: Optional[str] = Field(default=None)
    phone_number: Optional[str] = Field(default=None)
    address1: Optional[str] = Field(default=None)
    address2: Optional[str] = Field(default=None)
    city: Optional[str] = Field(default=None)
    state: Optional[str] = Field(default=None)
    zip_code: Optional[str] = Field(default=None)
    status: Optional[str] = Field(default=None)
    hot_candidate: Optional[int] = Field(default=None)
    warm_candidate: Optional[int] = Field(default=None)
    skills: Optional[any] = Field(default=None)
    longname: Optional[any] = Field(default=None)
    shifts: Optional[any] = Field(default=None)
    lic_states: Optional[any] = Field(default=None)
    req_regions: Optional[any] = Field(default=None)
    rec_first_name: Optional[str] = Field(default=None)
    rec_last_name: Optional[str] = Field(default=None)
    rec_email: Optional[str] = Field(default=None)
    rec_phone: Optional[str] = Field(default=None)
    rec_title: Optional[str] = Field(default=None)
    time_created: Optional[int] = Field(default=None)
    time_last_note: Optional[int] = Field(default=None)
    external_note_id: Optional[int] = Field(default=None)
    recent_note: Optional[int] = Field(default=None)
    no_call: Optional[int] = Field(default=None)
    no_email: Optional[int] = Field(default=None)
    no_text: Optional[int] = Field(default=None)
    earliest_start_date: Optional[int] = Field(default=None)
    desired_weekly_pay: Optional[int] = Field(default=None)
    desired_hourly_pay: Optional[int] = Field(default=None)
    phone_verified: Optional[int] = Field(default=None)
    registration_status: Optional[str] = Field(default=None)
    registration_email_type: Optional[str] = Field(default=None)
    email_queue_id: Optional[int] = Field(default=None)

    is_alumni: Optional[int] = Field(default=None)
    has_resume: Optional[int] = Field(default=None)
    has_checklist: Optional[int] = Field(default=None)
    references: Optional[int] = Field(default=None)
    profile_complete: Optional[int] = Field(default=None)
    type: Optional[str] = Field(default=None)

    class Config:
        populate_by_name = True
        alias_generator = Common.to_camel
        arbitrary_types_allowed = True

    manager: Any = None  # will be set to an instance of CandidateManager

    # Add the following fields:
    api_client: 'ApiClient' = Field(default=None)

    async def get_notes(self) -> AsyncGenerator[Note, None]:
        return self._get_paged_objects('note')

    async def get_documents(self) -> AsyncGenerator[Document, None]:
        return self._get_paged_objects('document')

    async def insert_note(self, note: str, note_type: int) -> Note:
        # Define the data to be sent with the request
        data = NoteInsertRequestInput(candidate_id=self.candidate_id,
                                      note=note,
                                      note_type=note_type).model_dump(by_alias=True)

        # Make the request
        response = await self.api_client.post('candidate/insertnote', data=data)

        # Parse the response
        return Note(**response)

    async def _get_paged_objects(self, object_type: str) -> AsyncGenerator[Union[Note, Document], None]:
        page_number = 0
        page_size = 10
        total_items = None
        while total_items is None or page_number * page_size < total_items:
            params = {"page": page_number}
            response = await self.api_client.get(f'/candidate/{self.candidate_id}/{object_type}', params=params)
            model_cls = globals()[object_type.capitalize()]
            page_response = PageResponse[model_cls](**response)

            if total_items is None:
                total_items = page_response.total_count

            if not page_response.data:
                break

            for obj in page_response.data:
                yield obj

            page_number += 1

    async def save(self):
        if self.candidate_id is not None:
            # Update existing candidate
            await self.manager.update(self)
        else:
            # Create new candidate
            await self.manager.create(self)


class CandidateManager:
    def __init__(self, api_client):
        self.api_client = api_client

    async def get(self, candidate_id: int) -> Candidate:
        response = await self.api_client.get(f'/candidate/{candidate_id}')
        return Candidate(api_client=self.api_client, **response)

    async def create(self, candidate: Candidate):
        await self._upsert(candidate)

    async def update(self, candidate: Candidate):
        await self._upsert(candidate)

    async def _upsert(self, candidate: Candidate):
        response = await self.api_client.post(f'/candidate',
                                              data=candidate.model_dump(by_alias=True,
                                                                        exclude={"manager", "api_client"}
                                                                        ))
        for attr, value in response.items():
            setattr(candidate, Common.to_snake(attr), value)
