from pydantic import BaseModel
from typing import List, Optional

class DataSource(BaseModel):
    name: str
    type: str
    url: str
    credentials: Optional[dict]

class Document(BaseModel):
    title: str
    content: str
    source: DataSource

class User(BaseModel):
    id: int
    name: str
    email: str

class Query(BaseModel):
    user_id: int
    query_text: str
    results: List[Document]