import type { SourceCode } from './sourceCode'

export interface Strategy {
  id: string
  name: string
  description?: string
  type: string
  source_code_id: string
  created_at: string
  updated_at: string
}

export interface StrategyCreate {
  name: string
  description?: string
  type: string
  source_code: {
    code_text?: string
  }
}

export interface StrategyUpdate {
  name?: string
  description?: string
  type?: string
  source_code?: {
    code_text?: string
  }
}

export interface StrategyDetail extends Strategy {
  source_code: SourceCode
  bt_length: number
}

