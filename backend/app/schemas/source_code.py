"""
策略代码模式
"""
from typing import Optional
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class SourceCodeBase(BaseModel):
    code_text: Optional[str] = None


class SourceCodeCreate(SourceCodeBase):
    pass


class SourceCodeUpdate(SourceCodeBase):
    pass


class SourceCode(SourceCodeBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

