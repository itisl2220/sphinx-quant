"""
策略模型
"""
from sqlalchemy import Column, String, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.models.base import BaseModel


class Strategy(BaseModel):
    """策略模型"""
    __tablename__ = "strategies"
    
    name = Column(String(100), nullable=False, index=True)
    description = Column(Text, nullable=True)
    type = Column(String(127), nullable=False)  # STOCK, FUTURES, CRYPTO_CURRENCY, OTHER
    source_code_id = Column(UUID(as_uuid=True), ForeignKey("source_codes.id"), nullable=False)
    
    # 关系
    source_code = relationship("SourceCode", backref="strategies")
    backtests = relationship("Backtest", back_populates="strategy", cascade="all, delete-orphan")

