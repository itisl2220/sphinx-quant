"""
回测模式
"""
from typing import Optional
from pydantic import BaseModel
from uuid import UUID
from datetime import date, datetime
from app.schemas.source_code import SourceCode


class BacktestBase(BaseModel):
    name: str
    description: Optional[str] = None
    start_date: date
    end_date: date
    bar_type: str  # TICK, MINUTE, DAY


class BacktestCreate(BacktestBase):
    strategy_id: UUID
    source_code_id: UUID


class BacktestUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    logs: Optional[str] = None
    total_profit_percent: Optional[float] = None
    year_profit_percent: Optional[float] = None
    max_dropdown_percent: Optional[float] = None


class Backtest(BacktestBase):
    id: UUID
    status: str
    logs: Optional[str] = None
    total_profit_percent: Optional[float] = None
    year_profit_percent: Optional[float] = None
    max_dropdown_percent: Optional[float] = None
    strategy_id: UUID
    source_code_id: UUID
    source_code: SourceCode
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

