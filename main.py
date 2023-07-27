import asyncio
from api_client.api_client import ApiClient
from models.candidate import CandidateManager, Candidate
from utils.constant import Constant


async def main():
    api = ApiClient(Constant.BASE_URL)
    candidates_manager = CandidateManager(api)

    candidate = await candidates_manager.get(340452)
    print(candidate.model_dump())

    await candidate.insert_note("aaa111", 77)

    notes = await candidate.get_notes()
    async for note in notes:
        print(note)
    # Create a new candidate
    new_candidate = Candidate(
        first_name='John',
        last_name='Doe',
        email='john.doe@yopmail.com',
        phone_number="2345111468",
        address1='123 Test St',
        city='Test City',
        state='TS',
        zip_code='12345',
        manager=candidates_manager
    )

    # The save method will create a new candidate because candidate_id is None
    await new_candidate.save()

    # Update the candidate
    new_candidate.first_name = 'Duyet'
    new_candidate.last_name = 'Doe'

    # The save method will update the candidate because candidate_id is not None
    await new_candidate.save()
    print(f"Candidate updated with ID {new_candidate.candidate_id}")
    print(new_candidate.model_dump())


# Run the main function
asyncio.run(main())
