"""
策略相关 API
"""
from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.api.v1.endpoints.users import get_current_user
from app.models.user import User
from app.models.strategy import Strategy
from app.models.source_code import SourceCode
from app.models.backtest import Backtest
from app.schemas.strategy import (
    Strategy as StrategySchema,
    StrategyCreate,
    StrategyUpdate,
    StrategyDetail,
)

router = APIRouter()


@router.get("/", response_model=List[StrategySchema])
async def list_strategies(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """获取策略列表"""
    strategies = db.query(Strategy).offset(skip).limit(limit).all()
    return strategies


@router.get("/{strategy_id}", response_model=StrategyDetail)
async def get_strategy(
    strategy_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """获取策略详情"""
    strategy = db.query(Strategy).filter(Strategy.id == strategy_id).first()
    if not strategy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="策略不存在",
        )
    
    # 计算回测数量
    bt_count = db.query(Backtest).filter(Backtest.strategy_id == strategy_id).count()
    
    result = StrategyDetail.model_validate(strategy)
    result.bt_length = bt_count
    return result


@router.post("/", response_model=StrategyDetail, status_code=status.HTTP_201_CREATED)
async def create_strategy(
    strategy: StrategyCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """创建策略"""
    # 创建源代码
    source_code_data = strategy.source_code
    source_code = SourceCode(code_text=source_code_data.get("code_text", ""))
    db.add(source_code)
    db.flush()
    
    # 创建策略
    db_strategy = Strategy(
        name=strategy.name,
        description=strategy.description,
        type=strategy.type,
        source_code_id=source_code.id,
    )
    db.add(db_strategy)
    db.commit()
    db.refresh(db_strategy)
    
    result = StrategyDetail.model_validate(db_strategy)
    result.bt_length = 0
    return result


@router.put("/{strategy_id}", response_model=StrategyDetail)
async def update_strategy(
    strategy_id: UUID,
    strategy_update: StrategyUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """更新策略"""
    strategy = db.query(Strategy).filter(Strategy.id == strategy_id).first()
    if not strategy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="策略不存在",
        )
    
    # 更新策略字段
    if strategy_update.name is not None:
        strategy.name = strategy_update.name
    if strategy_update.description is not None:
        strategy.description = strategy_update.description
    if strategy_update.type is not None:
        strategy.type = strategy_update.type
    
    # 更新源代码
    if strategy_update.source_code is not None:
        source_code = db.query(SourceCode).filter(
            SourceCode.id == strategy.source_code_id
        ).first()
        if source_code:
            source_code.code_text = strategy_update.source_code.get("code_text", "")
    
    db.commit()
    db.refresh(strategy)
    
    # 计算回测数量
    bt_count = db.query(Backtest).filter(Backtest.strategy_id == strategy_id).count()
    
    result = StrategyDetail.model_validate(strategy)
    result.bt_length = bt_count
    return result


@router.delete("/{strategy_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_strategy(
    strategy_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """删除策略"""
    strategy = db.query(Strategy).filter(Strategy.id == strategy_id).first()
    if not strategy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="策略不存在",
        )
    
    db.delete(strategy)
    db.commit()
    return None

