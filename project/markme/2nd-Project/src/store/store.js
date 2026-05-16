import { create } from 'zustand'
import { persist } from 'zustand/middleware'
import { getLocalDateKey } from '../utils/date'

// ── API helper ────────────────────────────────────────────────────────────────
async function apiCall(path, options = {}, token = null) {
  const headers = { ...(options.headers || {}) }
  if (token) headers['Authorization'] = `Bearer ${token}`
  if (!(options.body instanceof FormData)) {
    headers['Content-Type'] = headers['Content-Type'] || 'application/json'
  }
  const res = await fetch(`/api${path}`, { ...options, headers })
  if (res.status === 204) return null
  const data = await res.json().catch(() => ({}))
  if (!res.ok) throw Object.assign(new Error(data.detail || JSON.stringify(data)), { status: res.status, data })
  return data
}

export const useStore = create(
  persist(
    (set, get) => ({
      // ── Theme ──────────────────────────────────────────────────────────────
      theme: 'light',
      toggleTheme: () => set((s) => ({ theme: s.theme === 'light' ? 'dark' : 'light' })),

      // ── UI ─────────────────────────────────────────────────────────────────
      globalSearch: '',
      setGlobalSearch: (q) => set({ globalSearch: q }),
      mobileMenuOpen: false,
      toggleMobileMenu: () => set((s) => ({ mobileMenuOpen: !s.mobileMenuOpen })),
      setMobileMenuOpen: (v) => set({ mobileMenuOpen: v }),

      // ── Auth ───────────────────────────────────────────────────────────────
      token: null,
      refreshToken: null,
      currentUser: null,
      // 'educational' = full feature set (leave requests visible)
      // 'company'     = general org version (leave requests hidden)
      orgType: 'educational',

      login: async (email, password) => {
        const data = await apiCall('/auth/login/', {
          method: 'POST',
          body: JSON.stringify({ email, password }),
        })
        set({ token: data.access, refreshToken: data.refresh, orgType: data.org_type || 'educational' })
        // Fetch own profile
        try {
          const profile = await apiCall('/accounts/me/', {}, data.access)
          set({ currentUser: profile })
        } catch (_) {}
        return data
      },

      logout: async () => {
        const { refreshToken, token } = get()
        try {
          if (refreshToken)
            await apiCall('/auth/logout/', { method: 'POST', body: JSON.stringify({ refresh: refreshToken }) }, token)
        } catch (_) {}
        set({ token: null, refreshToken: null, currentUser: null, orgType: 'educational', students: [], teachers: [], attendanceLogs: [], notificationLogs: [] })
      },

      // ── Backend-connected students ──────────────────────────────────────────
      students: [],
      fetchStudents: async () => {
        const { token } = get()
        if (!token) return
        try {
          const data = await apiCall('/accounts/students/?page_size=200', {}, token)
          const list = data.results || data
          // Normalise to match existing store shape
          const normalised = list.map((s) => ({
            id: s.id,
            name: s.user.full_name,
            email: s.user.email,
            phone: s.user.phone,
            guardianPhone: s.guardian_phone,
            guardianName: s.guardian_name,
            guardianEmail: s.guardian_email,
            teacherId: s.assigned_teacher || '',
            face_registered: s.face_registered,
            profilePic: s.profile_photo || null,
            attendancePercentage: s.attendance_percentage,
            totalPresent: s.total_present,
            descriptor: {},  // encoding lives on backend now
            _backendId: s.id,
          }))
          set({ students: normalised })
        } catch (e) {
          console.error('fetchStudents failed', e)
        }
      },

      // ── Backend-connected teachers ──────────────────────────────────────────
      teachers: [],
      fetchTeachers: async () => {
        const { token } = get()
        if (!token) return
        try {
          const data = await apiCall('/accounts/teachers/?page_size=200', {}, token)
          const list = data.results || data
          const normalised = list.map((t) => ({
            id: t.id,
            name: t.user.full_name,
            subject: t.subject,
            email: t.user.email,
            phone: t.user.phone,
          }))
          set({ teachers: normalised })
        } catch (e) {
          console.error('fetchTeachers failed', e)
        }
      },

      addStudent: async (studentData, faceImageBlob = null) => {
        const { token } = get()

        // 1. Create student account on backend
        const created = await apiCall('/accounts/students/', {
          method: 'POST',
          body: JSON.stringify({
            email: studentData.email,
            full_name: studentData.name,
            password: studentData.password || 'hajri@2026',
            phone: studentData.phone || '',
            guardian_phone: studentData.guardianPhone,
            guardian_name: studentData.guardianName || '',
            guardian_email: studentData.guardianEmail || '',
            roll_number: studentData.rollNumber || '',
            assigned_teacher: studentData.teacherId || null,
          }),
        }, token)

        // 2. Enroll face if webcam image provided
        let faceEnrolled = false
        if (faceImageBlob) {
          const formData = new FormData()
          formData.append('photo', faceImageBlob, 'capture.jpg')
          try {
            await apiCall(`/accounts/students/${created.id}/enroll-face/`, {
              method: 'POST',
              body: formData,
              headers: {},
            }, token)
            faceEnrolled = true
          } catch (err) {
            console.warn('Face enrollment error:', err.message)
            throw Object.assign(new Error('Student created but face enrollment failed: ' + err.message), { studentCreated: true, created })
          }
        }

        // 3. Add to local store
        const newStudent = {
          id: created.id,
          name: created.user?.full_name || studentData.name,
          email: created.user?.email || studentData.email,
          guardianPhone: created.guardian_phone || studentData.guardianPhone,
          teacherId: created.assigned_teacher || studentData.teacherId || '',
          face_registered: faceEnrolled,
          profilePic: created.profile_photo || null,
          descriptor: {},
          _backendId: created.id,
        }
        set((s) => ({ students: [...s.students, newStudent] }))
        return newStudent
      },

      removeStudent: async (studentId) => {
        const { token } = get()
        try {
          await apiCall(`/accounts/students/${studentId}/`, { method: 'DELETE' }, token)
        } catch (e) {
          console.error('Delete student failed', e)
        }
        set((s) => ({
          students: s.students.filter((x) => x.id !== studentId),
          attendanceLogs: s.attendanceLogs.filter((l) => l.studentId !== studentId),
          notificationLogs: s.notificationLogs.filter((n) => n.studentId !== studentId),
        }))
      },

      updateStudent: (studentId, updates) =>
        set((s) => ({
          students: s.students.map((st) => (st.id === studentId ? { ...st, ...updates } : st)),
        })),

      addTeacher: async (teacherData) => {
        const { token } = get()
        const created = await apiCall('/accounts/teachers/', {
          method: 'POST',
          body: JSON.stringify({
            email: teacherData.email,
            full_name: teacherData.name,
            password: teacherData.password || 'hajri@2026',
            phone: teacherData.phone || '',
            subject: teacherData.subject || '',
          }),
        }, token)
        const newTeacher = {
          id: created.id,
          name: created.user?.full_name || teacherData.name,
          subject: created.subject || teacherData.subject || '',
          email: created.user?.email || teacherData.email,
          phone: created.user?.phone || teacherData.phone || '',
        }
        set((s) => ({ teachers: [...s.teachers, newTeacher] }))
        return newTeacher
      },

      removeTeacher: async (teacherId) => {
        const { token } = get()
        try {
          await apiCall(`/accounts/teachers/${teacherId}/`, { method: 'DELETE' }, token)
        } catch (e) {
          console.error('Delete teacher failed', e)
        }
        set((s) => ({
          teachers: s.teachers.filter((t) => t.id !== teacherId),
          students: s.students.map((st) =>
            st.teacherId === teacherId ? { ...st, teacherId: '' } : st
          ),
        }))
      },

      // ── Attendance (local + backend) ────────────────────────────────────────
      attendanceLogs: [],
      notificationLogs: [],

      fetchAttendanceLogs: async () => {
        const { token } = get()
        if (!token) return
        try {
          const data = await apiCall('/attendance/logs/?page_size=200', {}, token)
          const list = data.results || data
          const normalised = list.map((l) => ({
            id: l.id,
            studentId: l.student_id,
            timestamp: l.timestamp,
            dateKey: l.date,
            status: l.status,
            method: l.method,
            confidence: l.confidence,
          }))
          set({ attendanceLogs: normalised })
        } catch (e) {
          console.error('fetchAttendanceLogs failed', e)
        }
      },

      fetchNotifications: async () => {
        const { token } = get()
        if (!token) return
        try {
          const data = await apiCall('/attendance/notifications/?page_size=200', {}, token)
          const list = data.results || data
          const normalised = list.map((n) => ({
            id: n.id,
            studentId: n.student_id,
            message: n.message,
            timestamp: n.created_at,
            status: n.status,
          }))
          set({ notificationLogs: normalised })
        } catch (e) {
          console.error('fetchNotifications failed', e)
        }
      },

      logAttendance: async (studentId) => {
        const { token } = get()
        try {
          const result = await apiCall('/attendance/manual/', {
            method: 'POST',
            body: JSON.stringify({ student_id: studentId, status: 'PRESENT' }),
          }, token)
          const log = result.attendance
          const newLog = {
            id: log.id,
            studentId: log.student_id,
            timestamp: log.timestamp,
            dateKey: log.date,
            status: log.status,
            method: log.method,
          }
          const newNotif = {
            id: log.id + '-notif',
            studentId: log.student_id,
            message: `Attendance logged at ${new Date(log.timestamp).toLocaleTimeString()}`,
            timestamp: log.timestamp,
            status: 'SENT',
          }
          const dateKey = getLocalDateKey()
          set((s) => {
            if (s.attendanceLogs.some((l) => l.studentId === studentId && l.dateKey === dateKey)) return s
            return {
              attendanceLogs: [...s.attendanceLogs, newLog],
              notificationLogs: [...s.notificationLogs, newNotif],
            }
          })
        } catch (e) {
          console.error('logAttendance failed', e)
        }
      },

      clearLogs: () => set({ attendanceLogs: [], notificationLogs: [] }),
    }),
    {
      name: 'attendance-storage',
      partialize: (state) => ({
        theme: state.theme,
        token: state.token,
        refreshToken: state.refreshToken,
        currentUser: state.currentUser,
        orgType: state.orgType,
        // Don't persist data arrays — always fetch fresh from backend
      }),
    }
  )
)
