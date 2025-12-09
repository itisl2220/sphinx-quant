"""
回测相关 API
"""
from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.api.v1.endpoints.users import get_current_user
from app.models.user import User
from app.models.backtest import Backtest
from app.models.strategy import Strategy
from app.models.source_code import SourceCode
from app.schemas.backtest import (
    Backtest as BacktestSchema,
    BacktestCreate,
    BacktestUpdate,
)

router = APIRouter()


@router.get("/", response_model=List[BacktestSchema])
async def list_backtests(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """获取回测列表"""
    backtests = db.query(Backtest).offset(skip).limit(limit).all()
    return backtests


@router.get("/{backtest_id}", response_model=BacktestSchema)
async def get_backtest(
    backtest_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """获取回测详情"""
    backtest = db.query(Backtest).filter(Backtest.id == backtest_id).first()
    if not backtest:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="回测不存在",
        )
    return backtest


@router.post("/", response_model=BacktestSchema, status_code=status.HTTP_201_CREATED)
async def create_backtest(
    backtest: BacktestCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """创建回测"""
    # 验证策略和源代码是否存在
    strategy = db.query(Strategy).filter(Strategy.id == backtest.strategy_id).first()
    if not strategy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="策略不存在",
        )
    
    source_code = db.query(SourceCode).filter(
        SourceCode.id == backtest.source_code_id
    ).first()
    if not source_code:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="源代码不存在",
        )
    
    db_backtest = Backtest(
        name=backtest.name,
        description=backtest.description,
        start_date=backtest.start_date,
        end_date=backtest.end_date,
        bar_type=backtest.bar_type,
        status="START",
        strategy_id=backtest.strategy_id,
        source_code_id=backtest.source_code_id,
    )
    db.add(db_backtest)
    db.commit()
    db.refresh(db_backtest)
    return db_backtest


@router.put("/{backtest_id}", response_model=BacktestSchema)
async def update_backtest(
    backtest_id: UUID,
    backtest_update: BacktestUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """更新回测"""
    backtest = db.query(Backtest).filter(Backtest.id == backtest_id).first()
    if not backtest:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="回测不存在",
        )
    
    if backtest_update.name is not None:
        backtest.name = backtest_update.name
    if backtest_update.description is not None:
        backtest.description = backtest_update.description
    if backtest_update.status is not None:
        backtest.status = backtest_update.status
    if backtest_update.logs is not None:
        backtest.logs = backtest_update.logs
    if backtest_update.total_profit_percent is not None:
        backtest.total_profit_percent = backtest_update.total_profit_percent
    if backtest_update.year_profit_percent is not None:
        backtest.year_profit_percent = backtest_update.year_profit_percent
    if backtest_update.max_dropdown_percent is not None:
        backtest.max_dropdown_percent = backtest_update.max_dropdown_percent
    
    db.commit()
    db.refresh(backtest)
    return backtest


@router.delete("/{backtest_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_backtest(
    backtest_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """删除回测"""
    backtest = db.query(Backtest).filter(Backtest.id == backtest_id).first()
    if not backtest:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="回测不存在",
        )
    
    db.delete(backtest)
    db.commit()
    return None


@router.post("/{strategy_id}/test", status_code=status.HTTP_202_ACCEPTED)
async def start_backtest(
    strategy_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """启动回测任务（异步）"""
    strategy = db.query(Strategy).filter(Strategy.id == strategy_id).first()
    if not strategy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="策略不存在",
        )
    
    # TODO: 这里应该调用 Celery 任务
    # from app.tasks import backtest_task
    # backtest_task.delay(strategy_id=str(strategy_id), ...)
    
    return {"status": "Process", "message": "回测任务已启动"}

