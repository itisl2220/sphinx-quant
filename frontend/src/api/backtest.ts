import apiClient from './index'
import type { Backtest, BacktestCreate, BacktestUpdate } from '@/types/backtest'

export async function getBacktests(): Promise<Backtest[]> {
  return apiClient.get('/backtests/')
}

export async function getBacktest(id: string): Promise<Backtest> {
  return apiClient.get(`/backtests/${id}`)
}

export async function createBacktest(data: BacktestCreate): Promise<Backtest> {
  return apiClient.post('/backtests/', data)
}

export async function updateBacktest(id: string, data: BacktestUpdate): Promise<Backtest> {
  return apiClient.put(`/backtests/${id}`, data)
}

export async function deleteBacktest(id: string): Promise<void> {
  return apiClient.delete(`/backtests/${id}`)
}

