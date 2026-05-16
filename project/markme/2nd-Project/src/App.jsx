import React, { useEffect } from 'react'
import { Routes, Route, Navigate } from 'react-router-dom'
import Layout from './components/layout/Layout'
import Dashboard from './pages/Dashboard'
import LiveScanner from './pages/LiveScanner'
import Analytics from './pages/Analytics'
import StudentManagement from './pages/StudentManagement'
import NotificationLogs from './pages/NotificationLogs'
import TeacherManagement from './pages/TeacherManagement'
import LeaveRequests from './pages/LeaveRequests'
import LoginPage from './pages/LoginPage'
import { Toaster } from 'react-hot-toast'
import { useStore } from './store/store'

export default function App() {
  const token = useStore((s) => s.token)
  const orgType = useStore((s) => s.orgType)
  const fetchStudents = useStore((s) => s.fetchStudents)
  const fetchTeachers = useStore((s) => s.fetchTeachers)
  const fetchAttendanceLogs = useStore((s) => s.fetchAttendanceLogs)
  const fetchNotifications = useStore((s) => s.fetchNotifications)

  const isEducational = orgType === 'educational'

  // Fetch all data when logged in
  useEffect(() => {
    if (token) {
      fetchStudents()
      fetchTeachers()
      fetchAttendanceLogs()
      fetchNotifications()
    }
  }, [token])

  if (!token) {
    return (
      <>
        <LoginPage />
        <Toaster position="top-right" />
      </>
    )
  }

  return (
    <>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Dashboard />} />
          <Route path="scanner" element={<LiveScanner />} />
          <Route path="analytics" element={<Analytics />} />
          <Route path="students" element={<StudentManagement />} />
          <Route path="teachers" element={<TeacherManagement />} />
          {/* Leave Requests: educational institutions only */}
          {isEducational && (
            <Route path="leaves" element={<LeaveRequests />} />
          )}
          <Route path="notifications" element={<NotificationLogs />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Route>
      </Routes>
      <Toaster position="top-right" />
    </>
  )
}
