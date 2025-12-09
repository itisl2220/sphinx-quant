"""
API 路由汇总
"""
from fastapi import APIRouter
from app.api.v1.endpoints import auth, strategies, backtests, users

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["认证"])
api_router.include_router(users.router, prefix="/users", tags=["用户"])
api_router.include_router(strategies.router, prefix="/strategies", tags=["策略"])
api_router.include_router(backtests.router, prefix="/backtests", tags=["回测"])

