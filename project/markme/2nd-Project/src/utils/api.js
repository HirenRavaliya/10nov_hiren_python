/**
 * Hajri Hub API Client
 * Connects the React admin dashboard to the Django backend REST API.
 */

const BASE_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000/api'

// ── Token management ─────────────────────────────────────────────────────────
export const getToken = () => localStorage.getItem('access_token')
export const setTokens = (access, refresh) => {
  localStorage.setItem('access_token', access)
  localStorage.setItem('refresh_token', refresh)
}
export const clearTokens = () => {
  localStorage.removeItem('access_token')
  localStorage.removeItem('refresh_token')
}

// ── Base fetch with JWT ───────────────────────────────────────────────────────
async function apiFetch(path, options = {}) {
  const token = getToken()
  const headers = {
    ...(options.headers || {}),
  }
  if (token) headers['Authorization'] = `Bearer ${token}`

  // Don't set Content-Type for FormData (browser sets it with boundary)
  if (!(options.body instanceof FormData)) {
    headers['Content-Type'] = headers['Content-Type'] || 'application/json'
  }

  const res = await fetch(`${BASE_URL}${path}`, { ...options, headers })

  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }))
    throw new Error(err.detail || JSON.stringify(err))
  }

  if (res.status === 204) return null
  return res.json()
}

// ── Auth ──────────────────────────────────────────────────────────────────────
export const authAPI = {
  login: (email, password) =>
    apiFetch('/auth/login/', { method: 'POST', body: JSON.stringify({ email, password }) }),
  logout: (refresh) =>
    apiFetch('/auth/logout/', { method: 'POST', body: JSON.stringify({ refresh }) }),
  refresh: (refresh) =>
    apiFetch('/auth/refresh/', { method: 'POST', body: JSON.stringify({ refresh }) }),
  me: () => apiFetch('/accounts/me/'),
  updateFCMToken: (fcm_token) =>
    apiFetch('/accounts/me/fcm-token/', { method: 'POST', body: JSON.stringify({ fcm_token }) }),
}

// ── Students ──────────────────────────────────────────────────────────────────
export const studentsAPI = {
  list: (params = '') => apiFetch(`/accounts/students/${params}`),
  get: (id) => apiFetch(`/accounts/students/${id}/`),
  create: (data) => apiFetch('/accounts/students/', { method: 'POST', body: JSON.stringify(data) }),
  update: (id, data) => apiFetch(`/accounts/students/${id}/`, { method: 'PATCH', body: JSON.stringify(data) }),
  delete: (id) => apiFetch(`/accounts/students/${id}/`, { method: 'DELETE' }),
  attendanceHistory: (id) => apiFetch(`/accounts/students/${id}/attendance_history/`),
  enrollFace: (id, formData) =>
    apiFetch(`/accounts/students/${id}/enroll-face/`, {
      method: 'POST',
      body: formData,
      headers: {}, // Let browser set Content-Type for FormData
    }),
}

// ── Teachers ──────────────────────────────────────────────────────────────────
export const teachersAPI = {
  list: () => apiFetch('/accounts/teachers/'),
  create: (data) => apiFetch('/accounts/teachers/', { method: 'POST', body: JSON.stringify(data) }),
  delete: (id) => apiFetch(`/accounts/teachers/${id}/`, { method: 'DELETE' }),
}

// ── Attendance ────────────────────────────────────────────────────────────────
export const attendanceAPI = {
  scan: (formData) =>
    apiFetch('/attendance/scan/', {
      method: 'POST',
      body: formData,
      headers: {},
    }),
  scanBase64: (image_base64, tolerance) =>
    apiFetch('/attendance/scan/', {
      method: 'POST',
      body: JSON.stringify({ image_base64, tolerance }),
    }),
  manual: (student_id, status = 'PRESENT', notes = '') =>
    apiFetch('/attendance/manual/', {
      method: 'POST',
      body: JSON.stringify({ student_id, status, notes }),
    }),
  logs: (params = '') => apiFetch(`/attendance/logs/${params}`),
  dashboard: () => apiFetch('/attendance/dashboard/'),
  analytics: (days = 30, student_id = null) => {
    const params = new URLSearchParams({ days })
    if (student_id) params.set('student_id', student_id)
    return apiFetch(`/attendance/analytics/?${params}`)
  },
  notifications: (params = '') => apiFetch(`/attendance/notifications/${params}`),
  // Mobile
  myHistory: () => apiFetch('/attendance/my-history/'),
  myNotifications: () => apiFetch('/attendance/my-notifications/'),
}

export default {
  auth: authAPI,
  students: studentsAPI,
  teachers: teachersAPI,
  attendance: attendanceAPI,
}
