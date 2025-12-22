import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { authApi } from '../api'
import type { User } from '../types'

const TOKEN_KEY = 'auth_token'
const TOKEN_EXPIRY_KEY = 'auth_token_expiry'

export const useAuthStore = defineStore('auth', () => {
  const user = ref<User | null>(null)
  const token = ref<string | null>(null)
  const tokenExpiry = ref<number | null>(null)

  const isAuthenticated = computed(() => {
    if (!token.value || !tokenExpiry.value) return false
    return Date.now() < tokenExpiry.value
  })

  async function login() {
    const loginUrl = await authApi.getLoginUrl()
    window.location.href = loginUrl
  }

  async function handleCallback(code: string) {
    try {
      const response = await authApi.callback(code)
      const { access_token, expires_in } = response.data

      const expiryTimestamp = Date.now() + (expires_in * 1000)

      token.value = access_token
      tokenExpiry.value = expiryTimestamp

      localStorage.setItem(TOKEN_KEY, access_token)
      localStorage.setItem(TOKEN_EXPIRY_KEY, String(expiryTimestamp))

      await fetchCurrentUser()
    } catch (e) {
      console.error('Auth callback failed:', e)
      throw e
    }
  }

  async function fetchCurrentUser() {
    try {
      const response = await authApi.getCurrentUser()
      user.value = response.data
    } catch (e) {
      console.error('Failed to fetch current user:', e)
      logout()
    }
  }

  async function logout() {
    const logoutUrl = await authApi.getLogoutUrl()
    localStorage.removeItem(TOKEN_KEY)
    localStorage.removeItem(TOKEN_EXPIRY_KEY)
    window.location.href = logoutUrl
  }

  async function initialize() {
    const storedToken = localStorage.getItem(TOKEN_KEY)
    const storedExpiry = localStorage.getItem(TOKEN_EXPIRY_KEY)

    if (!storedToken || !storedExpiry) return

    const expiryTimestamp = Number(storedExpiry)

    if (Date.now() >= expiryTimestamp) {
      localStorage.removeItem(TOKEN_KEY)
      localStorage.removeItem(TOKEN_EXPIRY_KEY)
      return
    }

    token.value = storedToken
    tokenExpiry.value = expiryTimestamp

    await fetchCurrentUser()
  }

  return {
    user,
    token,
    tokenExpiry,
    isAuthenticated,
    login,
    logout,
    handleCallback,
    initialize
  }
})
