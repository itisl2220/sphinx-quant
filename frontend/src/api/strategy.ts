import apiClient from './index'
import type { Strategy, StrategyCreate, StrategyUpdate, StrategyDetail } from '@/types/strategy'

export async function getStrategies(): Promise<Strategy[]> {
  return apiClient.get('/strategies/')
}

export async function getStrategy(id: string): Promise<StrategyDetail> {
  return apiClient.get(`/strategies/${id}`)
}

export async function createStrategy(data: StrategyCreate): Promise<StrategyDetail> {
  return apiClient.post('/strategies/', data)
}

export async function updateStrategy(id: string, data: StrategyUpdate): Promise<StrategyDetail> {
  return apiClient.put(`/strategies/${id}`, data)
}

export async function deleteStrategy(id: string): Promise<void> {
  return apiClient.delete(`/strategies/${id}`)
}

export async function startBacktest(strategyId: string): Promise<{ status: string; message: string }> {
  return apiClient.post(`/backtests/${strategyId}/test`)
}

