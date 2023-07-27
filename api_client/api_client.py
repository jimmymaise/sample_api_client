from typing import Optional, AsyncGenerator, Union
from pydantic import BaseModel, Field
from utils.common import Common
from models.document import Document
from models.note import Note
from typing import List, Any
from httpx import AsyncClient
from typing import List, Optional, Generator
from typing import TypeVar, Generic, List
import httpx
import asyncio


class ApiClient:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session = httpx.AsyncClient(base_url=base_url)

    async def get(self, path: str, params: dict = None):
        response = await self.session.get(path, params=params)
        response.raise_for_status()
        return response.json()

    async def post(self, path: str, data: dict = None):
        response = await self.session.post(path, json=data)
        response.raise_for_status()
        return response.json()

    async def close(self):
        await self.session.aclose()
