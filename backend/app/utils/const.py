"""
常量定义
"""
from enum import Enum


class BacktestStatusType(str, Enum):
    """回测状态"""
    START = "START"
    PROCESS = "PROCESS"
    DONE = "DONE"
    ERROR = "ERROR"
    ABORT = "ABORT"


class StrategyType(str, Enum):
    """策略类型"""
    STOCK = "STOCK"
    FUTURES = "FUTURES"
    CRYPTO_CURRENCY = "CRYPTO_CURRENCY"
    OTHER = "OTHER"


class BarType(str, Enum):
    """Bar类型"""
    TICK = "TICK"
    MINUTE = "MINUTE"
    DAY = "DAY"

