import type { SourceCode } from './sourceCode'

export interface Backtest {
  id: string
  name: string
  description?: string
  start_date: string
  end_date: string
  status: string
  bar_type: string
  logs?: string
  total_profit_percent?: number
  year_profit_percent?: number
  max_dropdown_percent?: number
  strategy_id: string
  source_code_id: string
  source_code: SourceCode
  created_at: string
  updated_at: string
}

export interface BacktestCreate {
  name: string
  description?: string
  start_date: string
  end_date: string
  bar_type: string
  strategy_id: string
  source_code_id: string
}

export interface BacktestUpdate {
  name?: string
  description?: string
  status?: string
  logs?: string
  total_profit_percent?: number
  year_profit_percent?: number
  max_dropdown_percent?: number
}

