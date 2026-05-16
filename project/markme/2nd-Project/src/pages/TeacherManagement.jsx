import React, { useMemo, useState } from 'react'
import { Plus, Search, Trash2, UserCog, Mail, Phone, BookOpen, Lock, RefreshCw, AlertTriangle } from 'lucide-react'
import { motion, AnimatePresence } from 'framer-motion'
import toast from 'react-hot-toast'
import { useStore } from '../store/store'

export default function TeacherManagement() {
  const { teachers, students, addTeacher, removeTeacher, fetchTeachers, globalSearch, setGlobalSearch } = useStore()

  const [formData, setFormData] = useState({
    name: '', subject: '', email: '', phone: '', password: ''
  })
  const [saving, setSaving] = useState(false)
  const [deleteTarget, setDeleteTarget] = useState(null)

  const filteredTeachers = useMemo(() => {
    if (!globalSearch.trim()) return teachers
    const q = globalSearch.toLowerCase()
    return teachers.filter((t) =>
      t.name?.toLowerCase().includes(q) ||
      t.subject?.toLowerCase().includes(q) ||
      t.email?.toLowerCase().includes(q)
    )
  }, [teachers, globalSearch])

  const handleCreate = async () => {
    if (!formData.name.trim()) { toast.error('Full name is required'); return }
    if (!formData.email.trim()) { toast.error('Email is required'); return }
    if (!formData.subject.trim()) { toast.error('Subject is required'); return }

    setSaving(true)
    try {
      await addTeacher(formData)
      setFormData({ name: '', subject: '', email: '', phone: '', password: '' })
      toast.success(`${formData.name} added as teacher! ✅`)
    } catch (err) {
      const msg = err.data?.email?.[0] || err.data?.non_field_errors?.[0] || err.message || 'Failed to add teacher'
      toast.error(msg)
    } finally {
      setSaving(false)
    }
  }

  const handleDelete = (teacherId, name) => {
    setDeleteTarget({ id: teacherId, name })
  }

  const confirmDelete = async () => {
    if (!deleteTarget) return
    await removeTeacher(deleteTarget.id)
    toast.success(`${deleteTarget.name} removed.`)
    setDeleteTarget(null)
  }

  const field = (key, placeholder, icon, type = 'text') => (
    <div className="relative">
      <div className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400">{icon}</div>
      <input
        type={type}
        value={formData[key]}
        onChange={(e) => setFormData({ ...formData, [key]: e.target.value })}
        placeholder={placeholder}
        className="w-full bg-gray-50 dark:bg-dark-900 border border-gray-200 dark:border-white/10 text-gray-800 dark:text-white text-sm rounded-xl pl-10 pr-4 py-3 outline-none focus:ring-2 focus:ring-primary-500/20 focus:border-primary-500 transition-all"
      />
    </div>
  )

  return (
    <div className="max-w-6xl mx-auto pb-12 w-full space-y-8">
      {/* Header */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white tracking-tight">Teacher Management</h1>
          <p className="text-gray-500 dark:text-gray-400 mt-1 text-sm">
            Add teachers who can run the live scanner and mark attendance.
          </p>
        </div>
        <div className="flex items-center gap-3 w-full md:w-auto">
          <button onClick={fetchTeachers} className="p-2.5 rounded-xl border border-gray-200 dark:border-white/10 hover:bg-gray-50 dark:hover:bg-dark-800 text-gray-500 transition-colors">
            <RefreshCw className="w-4 h-4" />
          </button>
          <div className="relative flex-1 md:w-64">
            <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" />
            <input
              value={globalSearch}
              onChange={(e) => setGlobalSearch(e.target.value)}
              placeholder="Search teachers..."
              className="w-full bg-white dark:bg-dark-800 border border-gray-200 dark:border-white/10 text-gray-800 dark:text-white pl-10 pr-4 py-2.5 rounded-xl text-sm outline-none focus:border-primary-500 transition-all shadow-sm"
            />
          </div>
        </div>
      </div>

      {/* Add Teacher Form */}
      <div className="bg-white dark:bg-dark-800 border border-gray-100 dark:border-white/10 rounded-3xl p-7 shadow-sm">
        <h2 className="text-lg font-bold text-gray-900 dark:text-white mb-5">Add New Teacher</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {field('name',     'Full name *',             <UserCog className="w-4 h-4" />)}
          {field('subject',  'Subject taught *',        <BookOpen className="w-4 h-4" />)}
          {field('email',    'Email address *',         <Mail     className="w-4 h-4" />, 'email')}
          {field('phone',    'Phone (optional)',         <Phone    className="w-4 h-4" />, 'tel')}
          {field('password', 'Password (default: hajri@2026)', <Lock className="w-4 h-4" />, 'text')}
        </div>
        <div className="mt-5 flex items-center gap-3">
          <button
            onClick={handleCreate}
            disabled={saving}
            className="bg-primary-600 hover:bg-primary-700 disabled:opacity-60 text-white px-6 py-2.5 rounded-xl text-sm font-semibold flex items-center gap-2 shadow-lg shadow-primary-500/20 transition-all"
          >
            {saving
              ? <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
              : <Plus className="w-4 h-4" />}
            {saving ? 'Saving…' : 'Add Teacher'}
          </button>
          <p className="text-xs text-gray-400">
            Teacher will be able to log in at <span className="font-mono text-primary-500">localhost:5173</span> with their email + password.
          </p>
        </div>
      </div>

      {/* Teacher Cards */}
      {teachers.length === 0 ? (
        <div className="bg-white dark:bg-dark-800 border border-gray-100 dark:border-white/10 border-dashed rounded-3xl p-16 text-center shadow-sm">
          <div className="w-16 h-16 bg-primary-50 dark:bg-primary-900/20 rounded-full flex items-center justify-center mx-auto mb-4">
            <UserCog className="w-8 h-8 text-primary-400" />
          </div>
          <h3 className="text-lg font-bold text-gray-900 dark:text-white mb-1">No Teachers Yet</h3>
          <p className="text-gray-500 dark:text-gray-400 text-sm">Add your first teacher using the form above.</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-5">
          {filteredTeachers.map((teacher) => {
            const assignedStudents = students.filter((s) => s.teacherId === teacher.id)
            return (
              <motion.div
                key={teacher.id}
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                className="bg-white dark:bg-dark-800 border border-gray-100 dark:border-white/10 rounded-2xl p-5 shadow-sm group hover:shadow-md transition-shadow"
              >
                <div className="flex justify-between items-start gap-3">
                  <div className="flex gap-3 items-center">
                    <div className="w-12 h-12 rounded-2xl bg-primary-50 dark:bg-primary-500/10 flex items-center justify-center shrink-0">
                      <UserCog className="w-6 h-6 text-primary-600 dark:text-primary-400" />
                    </div>
                    <div>
                      <h3 className="font-bold text-gray-900 dark:text-white">{teacher.name}</h3>
                      <span className="text-xs font-semibold text-primary-600 dark:text-primary-400 bg-primary-50 dark:bg-primary-500/10 px-2 py-0.5 rounded-full">
                        {teacher.subject || 'No subject'}
                      </span>
                    </div>
                  </div>
                  <button
                    onClick={() => handleDelete(teacher.id, teacher.name)}
                    className="p-2 rounded-xl text-gray-400 hover:text-red-500 hover:bg-red-50 dark:hover:bg-red-500/10 opacity-0 group-hover:opacity-100 transition-all"
                  >
                    <Trash2 className="w-4 h-4" />
                  </button>
                </div>

                <div className="mt-4 space-y-2 text-sm">
                  <p className="flex items-center gap-2 text-gray-500 dark:text-gray-400">
                    <Mail className="w-3.5 h-3.5 shrink-0" />
                    <span className="truncate">{teacher.email || 'No email'}</span>
                  </p>
                  {teacher.phone && (
                    <p className="flex items-center gap-2 text-gray-500 dark:text-gray-400">
                      <Phone className="w-3.5 h-3.5 shrink-0" />
                      {teacher.phone}
                    </p>
                  )}
                </div>

                <div className="mt-4 pt-4 border-t border-gray-100 dark:border-white/10 flex items-center justify-between">
                  <p className="text-xs text-gray-500 dark:text-gray-400">Assigned Students</p>
                  <span className="text-sm font-bold text-primary-600 dark:text-primary-400">
                    {assignedStudents.length}
                  </span>
                </div>
              </motion.div>
            )
          })}
        </div>
      )}

      {/* How-to box */}
      <div className="bg-primary-50 dark:bg-primary-900/20 border border-primary-100 dark:border-primary-500/20 rounded-2xl p-5">
        <h3 className="text-sm font-bold text-primary-800 dark:text-primary-300 mb-2">📋 To add an Admin account</h3>
        <p className="text-xs text-primary-700 dark:text-primary-400 leading-relaxed">
          Admins are created via the Django admin panel or terminal only (for security). Go to{' '}
          <a href="http://127.0.0.1:8000/admin/accounts/user/add/" target="_blank" rel="noreferrer"
            className="underline font-semibold">
            http://127.0.0.1:8000/admin/accounts/user/add/
          </a>{' '}
          → set Role to <strong>Admin</strong> + check <strong>Staff status</strong> + <strong>Superuser status</strong>.
        </p>
      </div>

      {/* Delete confirm modal */}
      <AnimatePresence>
        {deleteTarget && (
          <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-gray-900/70 backdrop-blur-sm">
            <motion.div
              initial={{ opacity: 0, scale: 0.93 }} animate={{ opacity: 1, scale: 1 }} exit={{ opacity: 0, scale: 0.93 }}
              className="bg-white dark:bg-dark-800 w-full max-w-sm rounded-3xl shadow-2xl border border-gray-100 dark:border-white/10 p-7 text-center"
            >
              <div className="w-14 h-14 bg-red-100 dark:bg-red-500/20 rounded-2xl flex items-center justify-center mx-auto mb-4">
                <AlertTriangle className="w-7 h-7 text-red-600 dark:text-red-400" />
              </div>
              <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-2">Remove Teacher?</h3>
              <p className="text-sm text-gray-500 dark:text-gray-400 mb-6">
                <span className="font-semibold text-gray-700 dark:text-gray-200">{deleteTarget.name}</span> will be removed.
                Students assigned to them will become unassigned.
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
    </div>
  )
}
