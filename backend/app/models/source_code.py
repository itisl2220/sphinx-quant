"""
策略代码模型
"""
from sqlalchemy import Column, Text
from app.models.base import BaseModel


class SourceCode(BaseModel):
    """策略代码模型"""
    __tablename__ = "source_codes"
    
    code_text = Column(Text, nullable=True)

