"""
回测模型
"""
from sqlalchemy import Column, String, Date, Text, Float, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.models.base import BaseModel


class Backtest(BaseModel):
    """回测模型"""
    __tablename__ = "backtests"
    
    name = Column(String(100), nullable=False, index=True)
    description = Column(Text, nullable=True)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    status = Column(String(127), nullable=False)  # START, PROCESS, DONE, ERROR, ABORT
    bar_type = Column(String(127), nullable=False)  # TICK, MINUTE, DAY
    logs = Column(Text, nullable=True)
    total_profit_percent = Column(Float, nullable=True)
    year_profit_percent = Column(Float, nullable=True)
    max_dropdown_percent = Column(Float, nullable=True)
    
    # 外键
    strategy_id = Column(UUID(as_uuid=True), ForeignKey("strategies.id"), nullable=False)
    source_code_id = Column(UUID(as_uuid=True), ForeignKey("source_codes.id"), nullable=False)
    
    # 关系
    strategy = relationship("Strategy", back_populates="backtests")
    source_code = relationship("SourceCode", backref="backtests")

