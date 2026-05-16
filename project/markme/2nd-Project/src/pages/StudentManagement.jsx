import React, { useState, useRef, useMemo, useCallback, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { useStore } from '../store/store'
import Webcam from 'react-webcam'
import toast from 'react-hot-toast'
import { Users, Plus, X, Camera, Save, Search, Trash2, Eye, RefreshCw, CheckCircle2, AlertCircle, AlertTriangle } from 'lucide-react'
import { getLocalDateKey } from '../utils/date'

// Convert base64 data URL → Blob
function dataURLtoBlob(dataURL) {
  const [header, b64] = dataURL.split(',')
  const mime = header.match(/:(.*?);/)[1]
  const binary = atob(b64)
  const arr = new Uint8Array(binary.length)
  for (let i = 0; i < binary.length; i++) arr[i] = binary.charCodeAt(i)
  return new Blob([arr], { type: mime })
}

export default function StudentManagement() {
  const { students, teachers, addStudent, removeStudent, fetchStudents, attendanceLogs, globalSearch, setGlobalSearch } = useStore()

  // ── Modal state ────────────────────────────────────────────────────────────
  const [isAdding, setIsAdding] = useState(false)
  const [selectedStudent, setSelectedStudent] = useState(null)
  const [deleteTarget, setDeleteTarget] = useState(null) // { id, name }

  // ── Form state ─────────────────────────────────────────────────────────────
  const [formData, setFormData] = useState({
    name: '', email: '', password: '', phone: '',
    guardianPhone: '', guardianName: '', guardianEmail: '',
    rollNumber: '', teacherId: '',
  })

  // ── Webcam / capture state ─────────────────────────────────────────────────
  const webcamRef = useRef(null)
  const [capturedImg, setCapturedImg] = useState(null)   // base64 preview
  const [capturedBlob, setCapturedBlob] = useState(null) // blob for API
  const [cameraReady, setCameraReady] = useState(false)
  const [saving, setSaving] = useState(false)
  const [step, setStep] = useState(1) // 1=form, 2=camera

  // ── Reset form ─────────────────────────────────────────────────────────────
  const resetForm = () => {
    setFormData({ name: '', email: '', password: '', phone: '', guardianPhone: '', guardianName: '', guardianEmail: '', rollNumber: '', teacherId: '' })
    setCapturedImg(null)
    setCapturedBlob(null)
    setCameraReady(false)
    setStep(1)
  }

  const handleClose = () => { setIsAdding(false); resetForm() }

  // ── Capture from webcam ────────────────────────────────────────────────────
  const handleCapture = useCallback(() => {
    if (!webcamRef.current) return
    const imgSrc = webcamRef.current.getScreenshot({ width: 640, height: 480 })
    if (!imgSrc) { toast.error('Could not capture frame. Allow camera access.'); return }
    const blob = dataURLtoBlob(imgSrc)
    setCapturedImg(imgSrc)
    setCapturedBlob(blob)
    toast.success('Photo captured! Review and save.')
  }, [])

  const handleRetake = () => { setCapturedImg(null); setCapturedBlob(null) }

  // ── Save student ───────────────────────────────────────────────────────────
  const handleSave = async () => {
    if (!formData.name.trim()) { toast.error('Full name is required'); return }
    if (!formData.email.trim()) { toast.error('Email is required'); return }
    if (!formData.guardianPhone.trim()) { toast.error('Guardian phone is required'); return }
    if (!capturedBlob) { toast.error('Please capture the student\'s face photo'); return }

    setSaving(true)
    try {
      await addStudent(formData, capturedBlob)
      toast.success(`${formData.name} enrolled with face recognition! ✅`)
      handleClose()
      fetchStudents()
    } catch (err) {
      if (err.studentCreated) {
        toast.error('Student created but face enrollment failed. Re-enroll from student profile.')
        handleClose()
        fetchStudents()
      } else {
        const msg = err.data?.email?.[0] || err.message || 'Failed to enroll student'
        toast.error(msg)
      }
    } finally {
      setSaving(false)
    }
  }

  const handleDelete = (id, name, e) => {
    if (e) e.stopPropagation()
    setDeleteTarget({ id, name })
  }

  const confirmDelete = async () => {
    if (!deleteTarget) return
    await removeStudent(deleteTarget.id)
    toast.success(`${deleteTarget.name} removed.`)
    setDeleteTarget(null)
    if (selectedStudent?.id === deleteTarget.id) setSelectedStudent(null)
  }

  // ── Filtered list ──────────────────────────────────────────────────────────
  const filteredStudents = useMemo(() => {
    if (!globalSearch.trim()) return students
    const q = globalSearch.toLowerCase()
    return students.filter((s) =>
      s.name?.toLowerCase().includes(q) ||
      s.guardianPhone?.includes(q) ||
      s.email?.toLowerCase().includes(q)
    )
  }, [students, globalSearch])

  const teacherById = useMemo(() =>
    teachers.reduce((acc, t) => ({ ...acc, [t.id]: t }), {}), [teachers])

  // ── Calendar helper ────────────────────────────────────────────────────────
  const renderCalendar = (studentId) => {
    const today = new Date()
    const days = Array.from({ length: 35 }, (_, i) => {
      const d = new Date(today); d.setDate(d.getDate() - (34 - i)); return d
    })
    return (
      <div className="grid grid-cols-7 gap-1.5 mt-4">
        {['S','M','T','W','T','F','S'].map((d, i) => (
          <div key={i} className="text-center text-xs font-semibold text-gray-400 py-1">{d}</div>
        ))}
        {days.map((date, i) => {
          const dateStr = date.toISOString().split('T')[0]
          const log = attendanceLogs.find((l) =>
            l.studentId === studentId && (l.dateKey ? l.dateKey === getLocalDateKey(date) : l.timestamp?.startsWith(dateStr))
          )
          let bg = 'bg-gray-100 dark:bg-dark-900 text-gray-400 border-gray-200 dark:border-white/10'
          if (log) {
            bg = log.status === 'PRESENT'
              ? 'bg-green-500 text-white border-green-600 shadow-sm'
              : 'bg-red-500 text-white border-red-600 shadow-sm'
          } else if (date > today) {
            bg = 'bg-transparent border-dashed border-gray-200 dark:border-white/10 text-gray-300 dark:text-gray-600'
          }
          return (
            <div key={i} className={`aspect-square flex items-center justify-center rounded-lg text-xs font-medium border ${bg}`} title={date.toDateString()}>
              {date.getDate()}
            </div>
          )
        })}
      </div>
    )
  }

  return (
    <div className="max-w-6xl mx-auto pb-12 w-full">
      {/* Header */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-8 gap-4">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white tracking-tight">Access Management</h1>
          <p className="text-gray-500 dark:text-gray-400 mt-2 text-sm">Enroll students with live face capture for AI recognition.</p>
        </div>
        <div className="flex items-center gap-3 w-full md:w-auto">
          <button onClick={fetchStudents} className="p-2.5 rounded-xl border border-gray-200 dark:border-white/10 hover:bg-gray-50 dark:hover:bg-dark-800 text-gray-500 transition-colors" title="Refresh">
            <RefreshCw className="w-4 h-4" />
          </button>
          <div className="relative flex-1 md:w-64">
            <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" />
            <input
              type="text" placeholder="Search profiles..." value={globalSearch}
              onChange={(e) => setGlobalSearch(e.target.value)}
              className="w-full bg-white dark:bg-dark-800 border border-gray-200 dark:border-white/10 text-gray-800 dark:text-white pl-10 pr-4 py-2.5 rounded-xl text-sm outline-none focus:border-primary-500 transition-all shadow-sm"
            />
          </div>
          <button onClick={() => setIsAdding(true)} className="bg-primary-600 hover:bg-primary-700 text-white px-5 py-2.5 rounded-xl text-sm font-semibold flex items-center gap-2 shadow-lg shadow-primary-500/20 transition-all shrink-0">
            <Plus className="w-5 h-5" /> Enroll
          </button>
        </div>
      </div>

      {/* Student Grid */}
      {students.length === 0 ? (
        <div className="bg-white dark:bg-dark-800 border text-center p-16 rounded-3xl shadow-sm border-gray-100 dark:border-white/10 border-dashed">
          <div className="bg-primary-50 dark:bg-primary-900/20 w-20 h-20 rounded-full flex items-center justify-center mx-auto mb-4">
            <Users className="w-10 h-10 text-primary-400" />
          </div>
          <h3 className="text-lg font-bold text-gray-900 dark:text-white mb-1">No Profiles Enrolled</h3>
          <p className="text-gray-500 dark:text-gray-400 text-sm">Click Enroll to add students with live face capture.</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredStudents.map((st) => (
            <motion.div key={st.id} initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="bg-white dark:bg-dark-800 rounded-2xl shadow-sm border border-gray-100 dark:border-white/10 overflow-hidden group">
              <div className="h-32 bg-gradient-to-r from-primary-500 to-primary-700 relative">
                <div className="absolute top-4 right-4 flex gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
                  <button onClick={(e) => { e.stopPropagation(); setSelectedStudent(st) }} className="p-2 bg-white/20 hover:bg-white/30 backdrop-blur-md rounded-full text-white"><Eye className="w-4 h-4" /></button>
                  <button onClick={(e) => handleDelete(st.id, st.name, e)} className="p-2 bg-red-500/80 hover:bg-red-500 backdrop-blur-md rounded-full text-white"><Trash2 className="w-4 h-4" /></button>
                </div>
                <div className="absolute -bottom-10 left-6">
                  <div className="w-20 h-20 rounded-2xl border-4 border-white dark:border-dark-800 bg-gray-100 dark:bg-dark-900 overflow-hidden shadow-lg group-hover:scale-105 transition-transform">
                    {st.profilePic ? (
                      <img src={st.profilePic} alt={st.name} className="w-full h-full object-cover" />
                    ) : (
                      <Users className="w-full h-full p-4 text-gray-300 dark:text-gray-600" />
                    )}
                  </div>
                </div>
              </div>
              <div className="pt-14 pb-6 px-6">
                <div className="flex items-start justify-between">
                  <h3 className="text-lg font-bold text-gray-900 dark:text-white">{st.name}</h3>
                  {st.face_registered
                    ? <span className="flex items-center gap-1 text-xs font-semibold text-green-600 bg-green-50 dark:bg-green-500/10 px-2 py-0.5 rounded-full border border-green-100 dark:border-green-500/20"><CheckCircle2 className="w-3 h-3" />AI Ready</span>
                    : <span className="flex items-center gap-1 text-xs font-semibold text-amber-600 bg-amber-50 px-2 py-0.5 rounded-full border border-amber-100"><AlertCircle className="w-3 h-3" />No Face</span>
                  }
                </div>
                <div className="mt-4 space-y-2">
                  <p className="text-sm text-gray-500 flex justify-between"><span className="font-medium text-gray-400">Guardian</span><span className="text-gray-800 dark:text-gray-200">{st.guardianPhone}</span></p>
                  <p className="text-sm text-gray-500 flex justify-between"><span className="font-medium text-gray-400">Teacher</span><span className="text-gray-800 dark:text-gray-200">{teacherById[st.teacherId]?.name || 'Unassigned'}</span></p>
                </div>
              </div>
            </motion.div>
          ))}
        </div>
      )}

      {/* ── View Details Modal ─────────────────────────────────────────────── */}
      <AnimatePresence>
        {selectedStudent && (
          <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-gray-900/60 backdrop-blur-sm">
            <motion.div initial={{ opacity: 0, scale: 0.95 }} animate={{ opacity: 1, scale: 1 }} exit={{ opacity: 0, scale: 0.95 }}
              className="bg-white dark:bg-dark-800 w-full max-w-lg rounded-3xl shadow-2xl border border-gray-100 dark:border-white/10 overflow-auto max-h-[90vh]">
              <div className="p-6 md:p-8">
                <div className="flex justify-between items-start mb-6">
                  <div className="flex gap-4 items-center">
                    <div className="w-16 h-16 rounded-2xl overflow-hidden border-2 border-primary-100 dark:border-primary-900/50">
                      {selectedStudent.profilePic
                        ? <img src={selectedStudent.profilePic} className="w-full h-full object-cover" />
                        : <Users className="w-full h-full p-3 text-gray-300 dark:text-gray-600 bg-gray-50 dark:bg-dark-900" />}
                    </div>
                    <div>
                      <h2 className="text-2xl font-bold text-gray-900 dark:text-white">{selectedStudent.name}</h2>
                      <p className="text-sm text-gray-500 dark:text-gray-400">{selectedStudent.email || 'No email'}</p>
                    </div>
                  </div>
                  <button onClick={() => setSelectedStudent(null)} className="p-2 hover:bg-gray-100 dark:hover:bg-dark-900 rounded-full text-gray-400">
                    <X className="w-6 h-6" />
                  </button>
                </div>
                {(() => {
                  const logs = attendanceLogs.filter((l) => l.studentId === selectedStudent.id)
                  const present = logs.filter((l) => l.status === 'PRESENT').length
                  return (
                    <>
                      <div className="grid grid-cols-2 gap-4 mb-8">
                        <div className="bg-gray-50 dark:bg-dark-900 p-4 rounded-2xl border border-gray-100 dark:border-white/5">
                          <p className="text-xs text-gray-500 font-semibold uppercase tracking-wider mb-1">Total Logs</p>
                          <p className="text-3xl font-bold text-gray-900 dark:text-white">{logs.length}</p>
                        </div>
                        <div className="bg-primary-50 dark:bg-primary-500/10 p-4 rounded-2xl border border-primary-100 dark:border-primary-500/20">
                          <p className="text-xs text-primary-600 dark:text-primary-400 font-semibold uppercase tracking-wider mb-1">Present</p>
                          <p className="text-3xl font-bold text-primary-700 dark:text-primary-300">{present}</p>
                        </div>
                      </div>
                      <h3 className="text-lg font-bold text-gray-900 dark:text-white mb-3">Last 35 Days</h3>
                      <div className="bg-gray-50 dark:bg-dark-900 p-4 rounded-2xl border border-gray-100 dark:border-white/5">
                        {renderCalendar(selectedStudent.id)}
                      </div>
                    </>
                  )
                })()}
              </div>
            </motion.div>
          </div>
        )}
      </AnimatePresence>

      {/* ── Delete Confirm Modal ──────────────────────────────────────────────── */}
      <AnimatePresence>
        {deleteTarget && (
          <div className="fixed inset-0 z-[70] flex items-center justify-center p-4 bg-gray-900/70 backdrop-blur-sm">
            <motion.div
              initial={{ opacity: 0, scale: 0.93 }} animate={{ opacity: 1, scale: 1 }} exit={{ opacity: 0, scale: 0.93 }}
              className="bg-white dark:bg-dark-800 w-full max-w-sm rounded-3xl shadow-2xl border border-gray-100 dark:border-white/10 p-7 text-center"
            >
              <div className="w-14 h-14 bg-red-100 dark:bg-red-500/20 rounded-2xl flex items-center justify-center mx-auto mb-4">
                <AlertTriangle className="w-7 h-7 text-red-600 dark:text-red-400" />
              </div>
              <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-2">Remove Student?</h3>
              <p className="text-sm text-gray-500 dark:text-gray-400 mb-6">
                <span className="font-semibold text-gray-700 dark:text-gray-200">{deleteTarget.name}</span> will be permanently removed
                along with all their attendance records. This cannot be undone.
              </p>
              <div className="flex gap-3">
                <button
                  onClick={() => setDeleteTarget(null)}
                  className="flex-1 border border-gray-200 dark:border-white/10 py-2.5 rounded-xl text-sm font-semibold text-gray-600 dark:text-gray-400 hover:bg-gray-50 dark:hover:bg-dark-900 transition-all"
                >
                  Cancel
                </button>
                <button
                  onClick={confirmDelete}
                  className="flex-1 bg-red-600 hover:bg-red-700 text-white py-2.5 rounded-xl text-sm font-semibold shadow-lg shadow-red-500/20 transition-all flex items-center justify-center gap-2"
                >
                  <Trash2 className="w-4 h-4" /> Yes, Remove
                </button>
              </div>
            </motion.div>
          </div>
        )}
      </AnimatePresence>

      {/* ── Enroll Modal ───────────────────────────────────────────────────── */}
      <AnimatePresence>
        {isAdding && (
          <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-gray-900/70 backdrop-blur-sm">
            <motion.div initial={{ opacity: 0, scale: 0.95 }} animate={{ opacity: 1, scale: 1 }} exit={{ opacity: 0, scale: 0.95 }}
              className="bg-white dark:bg-dark-800 w-full max-w-4xl rounded-3xl shadow-2xl border border-gray-100 dark:border-white/10 flex flex-col md:flex-row max-h-[90vh]">

              {/* LEFT: Camera Panel */}
              <div className="w-full md:w-1/2 bg-dark-900 relative flex flex-col items-center justify-center min-h-[320px] rounded-t-3xl md:rounded-l-3xl md:rounded-tr-none overflow-hidden">
                {capturedImg ? (
                  /* Preview captured image */
                  <div className="w-full h-full flex flex-col items-center justify-center p-6 gap-4">
                    <div className="relative">
                      <img src={capturedImg} alt="Captured" className="w-56 h-56 object-cover rounded-2xl border-4 border-green-400 shadow-2xl shadow-green-500/30" />
                      <div className="absolute -top-2 -right-2 bg-green-500 rounded-full p-1.5 shadow-lg">
                        <CheckCircle2 className="w-4 h-4 text-white" />
                      </div>
                    </div>
                    <p className="text-green-400 text-sm font-semibold">Face captured successfully</p>
                    <button onClick={handleRetake} className="flex items-center gap-2 bg-white/10 hover:bg-white/20 text-white text-sm px-4 py-2 rounded-full transition-colors">
                      <RefreshCw className="w-4 h-4" /> Retake
                    </button>
                  </div>
                ) : (
                  /* Live webcam feed */
                  <div className="w-full h-full flex flex-col items-center justify-center relative">
                    <Webcam
                      ref={webcamRef}
                      screenshotFormat="image/jpeg"
                      screenshotQuality={0.92}
                      videoConstraints={{ facingMode: 'user', width: 640, height: 480 }}
                      onUserMedia={() => setCameraReady(true)}
                      onUserMediaError={() => { toast.error('Camera access denied'); setCameraReady(false) }}
                      className="w-full h-full object-cover absolute inset-0 opacity-70"
                      mirrored
                    />
                    {/* Face guide overlay */}
                    <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
                      <div className="w-44 h-56 border-2 border-dashed border-primary-400/70 rounded-full opacity-60" />
                    </div>
                    {/* Scanning line animation */}
                    {cameraReady && (
                      <div className="absolute inset-0 overflow-hidden pointer-events-none">
                        <div className="w-full h-0.5 bg-gradient-to-r from-transparent via-primary-400 to-transparent animate-scan-line" />
                      </div>
                    )}
                    {/* Capture button */}
                    <div className="absolute bottom-6 flex flex-col items-center gap-2">
                      <button
                        onClick={handleCapture}
                        disabled={!cameraReady}
                        className="w-16 h-16 rounded-full bg-white border-4 border-primary-500 hover:scale-105 active:scale-95 transition-all shadow-xl shadow-primary-500/40 flex items-center justify-center disabled:opacity-40 disabled:cursor-not-allowed"
                        title="Capture face"
                      >
                        <Camera className="w-7 h-7 text-primary-600" />
                      </button>
                      <p className="text-white/70 text-xs">{cameraReady ? 'Position face & tap to capture' : 'Starting camera…'}</p>
                    </div>
                  </div>
                )}
              </div>

              {/* RIGHT: Form Panel */}
              <div className="w-full md:w-1/2 p-7 flex flex-col overflow-y-auto">
                <div className="flex justify-between items-center mb-6">
                  <div>
                    <h2 className="text-2xl font-bold text-gray-900 dark:text-white tracking-tight">Enroll Student</h2>
                    <p className="text-sm text-gray-500 dark:text-gray-400 mt-0.5">Capture live face + fill details</p>
                  </div>
                  <button onClick={handleClose} className="p-2 hover:bg-gray-100 dark:hover:bg-dark-900 rounded-full text-gray-400">
                    <X className="w-6 h-6" />
                  </button>
                </div>

                <div className="space-y-4 flex-1">
                  {[
                    { label: 'Full Name *', key: 'name', placeholder: 'John Doe', type: 'text' },
                    { label: 'Email Address *', key: 'email', placeholder: 'student@example.com', type: 'email' },
                    { label: 'Login Password', key: 'password', placeholder: 'Min 6 chars (default: hajri@2026)', type: 'text' },
                    { label: 'Guardian Phone *', key: 'guardianPhone', placeholder: '+91 9876543210', type: 'tel' },
                    { label: 'Guardian Name', key: 'guardianName', placeholder: "Parent's name", type: 'text' },
                    { label: 'Guardian Email', key: 'guardianEmail', placeholder: 'parent@example.com', type: 'email' },
                    { label: 'Roll Number', key: 'rollNumber', placeholder: 'STU-001', type: 'text' },
                  ].map(({ label, key, placeholder, type }) => (
                    <div key={key}>
                      <label className="block text-xs font-semibold text-gray-600 dark:text-gray-400 mb-1">{label}</label>
                      <input
                        type={type} placeholder={placeholder} value={formData[key]}
                        onChange={(e) => setFormData({ ...formData, [key]: e.target.value })}
                        className="w-full bg-gray-50 dark:bg-dark-900 border border-gray-200 dark:border-white/10 text-gray-800 dark:text-white text-sm rounded-xl focus:ring-2 focus:ring-primary-500/30 focus:border-primary-500 px-3 py-2.5 outline-none transition-all placeholder-gray-400"
                      />
                    </div>
                  ))}

                  <div>
                    <label className="block text-xs font-semibold text-gray-600 dark:text-gray-400 mb-1">Assigned Teacher</label>
                    <select
                      value={formData.teacherId}
                      onChange={(e) => setFormData({ ...formData, teacherId: e.target.value })}
                      className="w-full bg-gray-50 dark:bg-dark-900 border border-gray-200 dark:border-white/10 text-gray-800 dark:text-white text-sm rounded-xl focus:ring-2 focus:ring-primary-500/30 focus:border-primary-500 px-3 py-2.5 outline-none transition-all"
                    >
                      <option value="">Unassigned</option>
                      {teachers.map((t) => (
                        <option key={t.id} value={t.id}>{t.name} – {t.subject}</option>
                      ))}
                    </select>
                  </div>
                </div>

                {/* Status bar */}
                <div className={`mt-5 flex items-center gap-2 px-4 py-2.5 rounded-xl text-sm font-medium border ${capturedImg ? 'bg-green-50 border-green-200 text-green-700 dark:bg-green-500/10 dark:border-green-500/30 dark:text-green-400' : 'bg-amber-50 border-amber-200 text-amber-700 dark:bg-amber-500/10 dark:border-amber-500/30 dark:text-amber-400'}`}>
                  {capturedImg
                    ? <><CheckCircle2 className="w-4 h-4 shrink-0" /> Face captured — ready to save</>
                    : <><Camera className="w-4 h-4 shrink-0" /> Capture face from camera on the left</>
                  }
                </div>

                <button
                  onClick={handleSave}
                  disabled={saving || !capturedBlob}
                  className="mt-4 w-full bg-primary-600 hover:bg-primary-700 disabled:opacity-50 disabled:cursor-not-allowed text-white font-semibold rounded-xl py-3.5 flex items-center justify-center gap-2 shadow-lg shadow-primary-500/20 transition-all"
                >
                  {saving
                    ? <><div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" /> Enrolling…</>
                    : <><Save className="w-5 h-5" /> Save & Enroll Face</>
                  }
                </button>
              </div>
            </motion.div>
          </div>
        )}
      </AnimatePresence>
    </div>
  )
}
