import apiClient from './index'
import type { Token } from '@/types/auth'

export async function login(username: string, password: string): Promise<Token> {
  const formData = new FormData()
  formData.append('username', username)
  formData.append('password', password)
  
  return apiClient.post('/auth/login', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  })
}

