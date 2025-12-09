"""
策略模式
"""
from typing import Optional
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from app.schemas.source_code import SourceCode


class StrategyBase(BaseModel):
    name: str
    description: Optional[str] = None
    type: str  # STOCK, FUTURES, CRYPTO_CURRENCY, OTHER


class StrategyCreate(StrategyBase):
    source_code: dict  # {"code_text": "..."}


class StrategyUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    type: Optional[str] = None
    source_code: Optional[dict] = None


class Strategy(StrategyBase):
    id: UUID
    source_code_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class StrategyDetail(StrategyBase):
    id: UUID
    source_code: SourceCode
    created_at: datetime
    updated_at: datetime
    bt_length: Optional[int] = 0  # 回测数量

    class Config:
        from_attributes = True

