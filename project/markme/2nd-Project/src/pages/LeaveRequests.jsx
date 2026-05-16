import React, { useState, useEffect, useCallback } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { useStore } from '../store/store'
import toast from 'react-hot-toast'
import {
  FileText, Clock, CheckCircle2, XCircle, ChevronDown,
  CalendarDays, User, RefreshCw, Search, SlidersHorizontal,
  Paperclip, MessageSquare, X, AlertTriangle,
} from 'lucide-react'
import clsx from 'clsx'

const REASON_LABELS = {
  MEDICAL:  { label: 'Medical / Health',    iconBg: 'bg-red-500/10',      iconText: 'text-red-400'      },
  FAMILY:   { label: 'Family Emergency',    iconBg: 'bg-amber-500/10',    iconText: 'text-amber-400'    },
  PERSONAL: { label: 'Personal Reason',     iconBg: 'bg-primary-500/10',  iconText: 'text-primary-400'  },
  TRAVEL:   { label: 'Travel / Outstation', iconBg: 'bg-primary-500/10',  iconText: 'text-primary-400'  },
  OTHER:    { label: 'Other',               iconBg: 'bg-gray-500/10',     iconText: 'text-gray-400'     },
}

const STATUS_META = {
  PENDING:  { label: 'Pending',  icon: Clock,         cls: 'bg-amber-50  border-amber-200  text-amber-700  dark:bg-amber-500/10  dark:border-amber-500/30  dark:text-amber-400'  },
  APPROVED: { label: 'Approved', icon: CheckCircle2,  cls: 'bg-green-50  border-green-200  text-green-700  dark:bg-green-500/10  dark:border-green-500/30  dark:text-green-400'  },
  REJECTED: { label: 'Rejected', icon: XCircle,       cls: 'bg-red-50    border-red-200    text-red-700    dark:bg-red-500/10    dark:border-red-500/30    dark:text-red-400'    },
}

async function apiCall(path, options = {}, token = null) {
  const headers = { ...(options.headers || {}) }
  if (token) headers['Authorization'] = `Bearer ${token}`
  if (!(options.body instanceof FormData)) headers['Content-Type'] = 'application/json'
  const res = await fetch(`/api${path}`, { ...options, headers })
  const data = await res.json().catch(() => ({}))
  if (!res.ok) throw Object.assign(new Error(data.detail || JSON.stringify(data)), { data })
  return data
}

export default function LeaveRequests() {
  const { token } = useStore()

  const [leaves, setLeaves]         = useState([])
  const [loading, setLoading]       = useState(true)
  const [filterStatus, setFilterStatus] = useState('ALL')
  const [search, setSearch]         = useState('')
  const [selected, setSelected]     = useState(null)   // detail modal
  const [reviewing, setReviewing]   = useState(null)   // {id, action}
  const [reviewNote, setReviewNote] = useState('')
  const [submitting, setSubmitting] = useState(false)
  const [deleteTarget, setDeleteTarget] = useState(null) // {id}

  const fetchLeaves = useCallback(async () => {
    setLoading(true)
    try {
      const data = await apiCall('/attendance/leave-requests/?page_size=200', {}, token)
      setLeaves(data.results || data)
    } catch (e) {
      toast.error('Failed to load leave requests')
    } finally {
      setLoading(false)
    }
  }, [token])

  useEffect(() => { fetchLeaves() }, [fetchLeaves])

  // ── Filter & search ────────────────────────────────────────────────────────
  const filtered = leaves.filter((l) => {
    if (filterStatus !== 'ALL' && l.status !== filterStatus) return false
    if (search.trim()) {
      const q = search.toLowerCase()
      return (
        l.student_name?.toLowerCase().includes(q) ||
        l.reason_display?.toLowerCase().includes(q) ||
        l.description?.toLowerCase().includes(q)
      )
    }
    return true
  })

  const counts = {
    ALL: leaves.length,
    PENDING:  leaves.filter(l => l.status === 'PENDING').length,
    APPROVED: leaves.filter(l => l.status === 'APPROVED').length,
    REJECTED: leaves.filter(l => l.status === 'REJECTED').length,
  }

  // ── Review (approve/reject) ────────────────────────────────────────────────
  const handleReview = async () => {
    if (!reviewing) return
    setSubmitting(true)
    try {
      const updated = await apiCall(
        `/attendance/leave-requests/${reviewing.id}/review/`,
        { method: 'POST', body: JSON.stringify({ action: reviewing.action, review_note: reviewNote }) },
        token
      )
      setLeaves(prev => prev.map(l => l.id === updated.id ? updated : l))
      if (selected?.id === updated.id) setSelected(updated)
      toast.success(`Leave request ${reviewing.action === 'approve' ? 'approved ✅' : 'rejected ❌'}`)
      setReviewing(null)
      setReviewNote('')
    } catch (e) {
      toast.error(e.message || 'Review failed')
    } finally {
      setSubmitting(false)
    }
  }

  const handleDelete = (id) => {
    setDeleteTarget({ id })
  }

  const confirmDelete = async () => {
    if (!deleteTarget) return
    try {
      await apiCall(`/attendance/leave-requests/${deleteTarget.id}/`, { method: 'DELETE' }, token)
      setLeaves(prev => prev.filter(l => l.id !== deleteTarget.id))
      if (selected?.id === deleteTarget.id) setSelected(null)
      toast.success('Deleted.')
    } catch (e) {
      toast.error('Delete failed')
    } finally {
      setDeleteTarget(null)
    }
  }

  return (
    <div className="max-w-6xl mx-auto pb-12 w-full">
      {/* Header */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-8 gap-4">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white tracking-tight">Leave Requests</h1>
          <p className="text-gray-500 dark:text-gray-400 mt-1 text-sm">
            Review and approve leave requests submitted by students & parents.
          </p>
        </div>
        <div className="flex items-center gap-3">
          <button onClick={fetchLeaves} className="p-2.5 rounded-xl border border-gray-200 dark:border-white/10 hover:bg-gray-50 dark:hover:bg-dark-800 text-gray-500 transition-colors">
            <RefreshCw className={clsx('w-4 h-4', loading && 'animate-spin')} />
          </button>
          <div className="relative">
            <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" />
            <input
              type="text" placeholder="Search student or reason…" value={search}
              onChange={e => setSearch(e.target.value)}
              className="bg-white dark:bg-dark-800 border border-gray-200 dark:border-white/10 text-sm rounded-xl pl-9 pr-4 py-2.5 outline-none focus:border-primary-500 transition-all w-60 shadow-sm"
            />
          </div>
        </div>
      </div>

      {/* Status filter tabs */}
      <div className="flex gap-2 mb-6 flex-wrap">
        {['ALL', 'PENDING', 'APPROVED', 'REJECTED'].map(s => (
          <button
            key={s}
            onClick={() => setFilterStatus(s)}
            className={clsx(
              'px-4 py-2 rounded-full text-sm font-semibold border transition-all',
              filterStatus === s
                ? 'bg-primary-600 border-primary-600 text-white shadow-md shadow-primary-500/20'
                : 'bg-white dark:bg-dark-800 border-gray-200 dark:border-white/10 text-gray-600 dark:text-gray-400 hover:border-primary-400'
            )}
          >
            {s === 'ALL' ? 'All' : STATUS_META[s].label}
            <span className={clsx(
              'ml-2 px-1.5 py-0.5 rounded-full text-xs',
              filterStatus === s ? 'bg-white/20' : 'bg-gray-100 dark:bg-dark-900 text-gray-500'
            )}>
              {counts[s]}
            </span>
          </button>
        ))}
      </div>

      {/* List */}
      {loading ? (
        <div className="flex justify-center items-center h-52">
          <div className="w-10 h-10 border-4 border-primary-200 dark:border-primary-900 border-t-primary-600 rounded-full animate-spin" />
        </div>
      ) : filtered.length === 0 ? (
        <div className="bg-white dark:bg-dark-800 rounded-3xl border border-gray-100 dark:border-white/10 border-dashed p-16 text-center shadow-sm">
          <FileText className="w-12 h-12 text-gray-300 dark:text-gray-600 mx-auto mb-4" />
          <h3 className="text-lg font-bold text-gray-900 dark:text-white mb-1">No Leave Requests</h3>
          <p className="text-gray-500 dark:text-gray-400 text-sm">
            {filterStatus !== 'ALL' ? `No ${filterStatus.toLowerCase()} requests.` : 'Students haven\'t submitted any requests yet.'}
          </p>
        </div>
      ) : (
        <div className="space-y-3">
          {filtered.map(leave => {
            const reasonMeta = REASON_LABELS[leave.reason] || REASON_LABELS.OTHER
            const statusMeta = STATUS_META[leave.status]
            const StatusIcon = statusMeta.icon
            return (
              <motion.div
                key={leave.id}
                initial={{ opacity: 0, y: 8 }}
                animate={{ opacity: 1, y: 0 }}
                className="bg-white dark:bg-dark-800 rounded-2xl border border-gray-100 dark:border-white/10 shadow-sm hover:shadow-md transition-shadow cursor-pointer"
                onClick={() => setSelected(leave)}
              >
                <div className="p-5 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                  {/* Left info */}
                  <div className="flex items-center gap-4">
                    <div className={`w-12 h-12 rounded-2xl ${reasonMeta.iconBg} flex items-center justify-center shrink-0`}>
                      <FileText className={`w-6 h-6 ${reasonMeta.iconText}`} />
                    </div>
                    <div>
                      <div className="flex items-center gap-2 flex-wrap">
                        <p className="font-bold text-gray-900 dark:text-white">{leave.student_name}</p>
                        <span className="text-xs font-semibold bg-gray-100 dark:bg-dark-900 text-gray-500 dark:text-gray-400 px-2 py-0.5 rounded-full">
                          {leave.reason_display}
                        </span>
                      </div>
                      <div className="flex items-center gap-3 mt-1 text-sm text-gray-500 dark:text-gray-400">
                        <span className="flex items-center gap-1">
                          <CalendarDays className="w-3.5 h-3.5" />
                          {leave.start_date} → {leave.end_date}
                        </span>
                        <span className="font-semibold text-gray-700 dark:text-gray-300">
                          {leave.duration_days} day{leave.duration_days > 1 ? 's' : ''}
                        </span>
                        {leave.proof_doc_url && (
                          <span className="flex items-center gap-1 text-primary-500">
                            <Paperclip className="w-3.5 h-3.5" /> Proof attached
                          </span>
                        )}
                      </div>
                      {leave.description && (
                        <p className="text-xs text-gray-400 mt-1 line-clamp-1">{leave.description}</p>
                      )}
                    </div>
                  </div>

                  {/* Right: status + actions */}
                  <div className="flex items-center gap-3 ml-auto shrink-0" onClick={e => e.stopPropagation()}>
                    <span className={`flex items-center gap-1.5 px-3 py-1.5 rounded-full border text-xs font-semibold ${statusMeta.cls}`}>
                      <StatusIcon className="w-3.5 h-3.5" />
                      {statusMeta.label}
                    </span>
                    {leave.status === 'PENDING' && (
                      <>
                        <button
                          onClick={() => { setReviewing({ id: leave.id, action: 'approve' }); setReviewNote('') }}
                          className="px-3 py-1.5 bg-green-600 hover:bg-green-700 text-white text-xs font-semibold rounded-lg transition-colors shadow-sm"
                        >
                          Approve
                        </button>
                        <button
                          onClick={() => { setReviewing({ id: leave.id, action: 'reject' }); setReviewNote('') }}
                          className="px-3 py-1.5 bg-red-600 hover:bg-red-700 text-white text-xs font-semibold rounded-lg transition-colors shadow-sm"
                        >
                          Reject
                        </button>
                      </>
                    )}
                  </div>
                </div>
              </motion.div>
            )
          })}
        </div>
      )}

      {/* ── Detail Modal ───────────────────────────────────────────────────────── */}
      <AnimatePresence>
        {selected && (
          <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-gray-900/60 backdrop-blur-sm">
            <motion.div
              initial={{ opacity: 0, scale: 0.95 }} animate={{ opacity: 1, scale: 1 }} exit={{ opacity: 0, scale: 0.95 }}
              className="bg-white dark:bg-dark-800 w-full max-w-lg rounded-3xl shadow-2xl border border-gray-100 dark:border-white/10 overflow-auto max-h-[90vh]"
            >
              <div className="p-7">
                {/* Modal header */}
                <div className="flex justify-between items-start mb-6">
                  <h2 className="text-xl font-bold text-gray-900 dark:text-white">Leave Request Detail</h2>
                  <button onClick={() => setSelected(null)} className="p-1.5 hover:bg-gray-100 dark:hover:bg-dark-900 rounded-full text-gray-400">
                    <X className="w-5 h-5" />
                  </button>
                </div>

                {/* Student */}
                <div className="flex items-center gap-3 mb-6 p-4 bg-gray-50 dark:bg-dark-900 rounded-2xl border border-gray-100 dark:border-white/10">
                  <div className="w-10 h-10 rounded-full bg-primary-100 dark:bg-primary-900/30 flex items-center justify-center">
                    <User className="w-5 h-5 text-primary-600 dark:text-primary-400" />
                  </div>
                  <div>
                    <p className="font-bold text-gray-900 dark:text-white">{selected.student_name}</p>
                    <p className="text-xs text-gray-500">{selected.student_email}</p>
                  </div>
                  <span className={`ml-auto flex items-center gap-1.5 px-3 py-1 rounded-full border text-xs font-semibold ${STATUS_META[selected.status].cls}`}>
                    {STATUS_META[selected.status].label}
                  </span>
                </div>

                {/* Details grid */}
                <div className="grid grid-cols-2 gap-4 mb-6">
                  {[
                    { label: 'Reason',     value: selected.reason_display },
                    { label: 'Duration',   value: `${selected.duration_days} day${selected.duration_days > 1 ? 's' : ''}` },
                    { label: 'From',       value: selected.start_date },
                    { label: 'To',         value: selected.end_date },
                    { label: 'Submitted',  value: new Date(selected.created_at).toLocaleDateString('en-IN', { day: 'numeric', month: 'short', year: 'numeric' }) },
                    { label: 'Reviewed by',value: selected.reviewed_by_name || '—' },
                  ].map(({ label, value }) => (
                    <div key={label} className="bg-gray-50 dark:bg-dark-900 rounded-xl p-3 border border-gray-100 dark:border-white/5">
                      <p className="text-xs text-gray-400 font-semibold uppercase tracking-wide mb-0.5">{label}</p>
                      <p className="text-sm font-bold text-gray-800 dark:text-gray-200">{value}</p>
                    </div>
                  ))}
                </div>

                {/* Description */}
                {selected.description && (
                  <div className="mb-4 p-4 bg-gray-50 dark:bg-dark-900 rounded-xl border border-gray-100 dark:border-white/10">
                    <p className="text-xs text-gray-400 font-semibold uppercase tracking-wide mb-1">Student Note</p>
                    <p className="text-sm text-gray-700 dark:text-gray-300">{selected.description}</p>
                  </div>
                )}

                {/* Review note */}
                {selected.review_note && (
                  <div className="mb-4 p-4 bg-primary-50 dark:bg-primary-500/10 rounded-xl border border-primary-100 dark:border-primary-500/20">
                    <p className="text-xs text-primary-600 dark:text-primary-400 font-semibold uppercase tracking-wide mb-1 flex items-center gap-1"><MessageSquare className="w-3.5 h-3.5" />Admin Note</p>
                    <p className="text-sm text-primary-700 dark:text-primary-300">{selected.review_note}</p>
                  </div>
                )}

                {/* Proof document */}
                {selected.proof_doc_url && (
                  <a
                    href={selected.proof_doc_url}
                    target="_blank"
                    rel="noreferrer"
                    className="flex items-center gap-2 text-sm text-primary-600 dark:text-primary-400 font-semibold hover:underline mb-6"
                  >
                    <Paperclip className="w-4 h-4" /> View Proof Document
                  </a>
                )}

                {/* Actions */}
                {selected.status === 'PENDING' && (
                  <div className="flex gap-3">
                    <button
                      onClick={() => { setReviewing({ id: selected.id, action: 'approve' }); setReviewNote('') }}
                      className="flex-1 bg-green-600 hover:bg-green-700 text-white py-2.5 rounded-xl text-sm font-semibold flex items-center justify-center gap-2 transition-all shadow-lg shadow-green-500/20"
                    >
                      <CheckCircle2 className="w-4 h-4" /> Approve
                    </button>
                    <button
                      onClick={() => { setReviewing({ id: selected.id, action: 'reject' }); setReviewNote('') }}
                      className="flex-1 bg-red-600 hover:bg-red-700 text-white py-2.5 rounded-xl text-sm font-semibold flex items-center justify-center gap-2 transition-all shadow-lg shadow-red-500/20"
                    >
                      <XCircle className="w-4 h-4" /> Reject
                    </button>
                    <button
                      onClick={() => handleDelete(selected.id)}
                      className="p-2.5 border border-gray-200 dark:border-white/10 hover:bg-red-50 dark:hover:bg-red-500/10 hover:border-red-200 text-gray-400 hover:text-red-500 rounded-xl transition-all"
                      title="Delete request"
                    >
                      <X className="w-5 h-5" />
                    </button>
                  </div>
                )}
              </div>
            </motion.div>
          </div>
        )}
      </AnimatePresence>

      {/* ── Review Confirm Modal ──────────────────────────────────────────────── */}
      <AnimatePresence>
        {reviewing && (
          <div className="fixed inset-0 z-[60] flex items-center justify-center p-4 bg-gray-900/70 backdrop-blur-sm">
            <motion.div
              initial={{ opacity: 0, scale: 0.93 }} animate={{ opacity: 1, scale: 1 }} exit={{ opacity: 0, scale: 0.93 }}
              className="bg-white dark:bg-dark-800 w-full max-w-md rounded-3xl shadow-2xl border border-gray-100 dark:border-white/10 p-7"
            >
              <div className={clsx(
                'w-14 h-14 rounded-2xl mx-auto mb-5 flex items-center justify-center',
                reviewing.action === 'approve' ? 'bg-green-100 dark:bg-green-500/20' : 'bg-red-100 dark:bg-red-500/20'
              )}>
                {reviewing.action === 'approve'
                  ? <CheckCircle2 className="w-7 h-7 text-green-600 dark:text-green-400" />
                  : <AlertTriangle className="w-7 h-7 text-red-600 dark:text-red-400" />
                }
              </div>
              <h3 className="text-xl font-bold text-center text-gray-900 dark:text-white mb-1">
                {reviewing.action === 'approve' ? 'Approve Leave?' : 'Reject Leave?'}
              </h3>
              <p className="text-sm text-center text-gray-500 dark:text-gray-400 mb-5">
                {reviewing.action === 'approve'
                  ? 'The student will be notified that their request was approved.'
                  : 'The student will be notified that their request was rejected.'}
              </p>
              <div className="mb-5">
                <label className="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-1.5">
                  Note to student <span className="text-gray-400 font-normal">(optional)</span>
                </label>
                <textarea
                  rows={3}
                  value={reviewNote}
                  onChange={e => setReviewNote(e.target.value)}
                  placeholder={reviewing.action === 'approve'
                    ? 'e.g. Please bring a medical certificate when you return.'
                    : 'e.g. Insufficient proof provided, please reapply.'}
                  className="w-full bg-gray-50 dark:bg-dark-900 border border-gray-200 dark:border-white/10 text-sm rounded-xl p-3 outline-none focus:border-primary-500 resize-none transition-all"
                />
              </div>
              <div className="flex gap-3">
                <button
                  onClick={() => setReviewing(null)}
                  disabled={submitting}
                  className="flex-1 border border-gray-200 dark:border-white/10 py-2.5 rounded-xl text-sm font-semibold text-gray-600 dark:text-gray-400 hover:bg-gray-50 dark:hover:bg-dark-900 transition-all"
                >
                  Cancel
                </button>
                <button
                  onClick={handleReview}
                  disabled={submitting}
                  className={clsx(
                    'flex-1 py-2.5 rounded-xl text-sm font-semibold text-white transition-all shadow-lg flex items-center justify-center gap-2',
                    reviewing.action === 'approve'
                      ? 'bg-green-600 hover:bg-green-700 shadow-green-500/20 disabled:opacity-60'
                      : 'bg-red-600 hover:bg-red-700 shadow-red-500/20 disabled:opacity-60'
                  )}
                >
                  {submitting
                    ? <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
                    : (reviewing.action === 'approve' ? 'Confirm Approve' : 'Confirm Reject')
                  }
                </button>
              </div>
            </motion.div>
          </div>
        )}\n      </AnimatePresence>

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
              <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-2">Delete Request?</h3>
              <p className="text-sm text-gray-500 dark:text-gray-400 mb-6">
                This leave request will be permanently deleted. This cannot be undone.
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
                  className="flex-1 bg-red-600 hover:bg-red-700 text-white py-2.5 rounded-xl text-sm font-semibold shadow-lg shadow-red-500/20 transition-all"
                >
                  Yes, Delete
                </button>
              </div>
            </motion.div>
          </div>
        )}
      </AnimatePresence>
    </div>
  )
}
