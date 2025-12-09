import apiClient from './index'
import type { User } from '@/types/user'

export async function getCurrentUser(): Promise<User> {
  return apiClient.get('/users/me')
}

