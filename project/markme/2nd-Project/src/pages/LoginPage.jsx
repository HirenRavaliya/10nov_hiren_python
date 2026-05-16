import React, { useState } from 'react'
import { motion } from 'framer-motion'
import { useStore } from '../store/store'
import toast from 'react-hot-toast'
import { LogIn, Eye, EyeOff } from 'lucide-react'

export default function LoginPage() {
  const login = useStore((s) => s.login)
  const [form, setForm] = useState({ email: '', password: '' })
  const [showPass, setShowPass] = useState(false)
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!form.email || !form.password) return toast.error('Enter email and password')
    setLoading(true)
    try {
      await login(form.email, form.password)
      toast.success('Logged in successfully!')
    } catch (err) {
      toast.error(err.data?.detail || 'Invalid credentials')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center p-6 relative overflow-hidden"
      style={{ background: 'linear-gradient(135deg, #040804 0%, #0d1f07 50%, #040804 100%)' }}
    >
      {/* Background glow — matches visitor site atmosphere */}
      <div className="absolute inset-0 pointer-events-none">
        <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-[#82bc4a]/10 rounded-full blur-[120px]" />
        <div className="absolute bottom-1/4 right-1/4 w-80 h-80 bg-[#82bc4a]/8 rounded-full blur-[100px]" />
        {/* Subtle grid overlay */}
        <div className="absolute inset-0 opacity-5"
          style={{
            backgroundImage: 'repeating-linear-gradient(0deg, #82bc4a 0px, #82bc4a 1px, transparent 1px, transparent 40px), repeating-linear-gradient(90deg, #82bc4a 0px, #82bc4a 1px, transparent 1px, transparent 40px)'
          }}
        />
      </div>

      <motion.div
        initial={{ opacity: 0, y: 24 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="w-full max-w-md relative z-10"
      >
        {/* Logo */}
        <div className="text-center mb-10">
          <div className="inline-flex items-center justify-center mb-6">
            <img src="/hajrihub-logo.png" alt="Hajri Hub" className="h-16 object-contain" />
          </div>
          <p className="text-gray-400 mt-1 text-sm tracking-wide">AI Attendance Management System</p>
        </div>

        {/* Card */}
        <div
          className="rounded-3xl shadow-2xl p-8 border"
          style={{
            background: 'rgba(130, 188, 74, 0.04)',
            backdropFilter: 'blur(20px)',
            borderColor: 'rgba(130, 188, 74, 0.2)',
          }}
        >
          <h2 className="text-xl font-bold text-white mb-6 font-display">Sign in to continue</h2>

          <form onSubmit={handleSubmit} className="space-y-5">
            <div>
              <label className="block text-sm font-semibold text-gray-300 mb-1.5">
                Email Address
              </label>
              <input
                type="email"
                autoComplete="email"
                value={form.email}
                onChange={(e) => setForm({ ...form, email: e.target.value })}
                placeholder="admin@hajrihub.ai"
                className="w-full text-white text-sm rounded-xl p-3 outline-none transition-all placeholder-gray-600"
                style={{
                  background: 'rgba(255,255,255,0.03)',
                  border: '1px solid rgba(130,188,74,0.2)',
                }}
                onFocus={e => e.target.style.borderColor = 'rgba(130,188,74,0.6)'}
                onBlur={e => e.target.style.borderColor = 'rgba(130,188,74,0.2)'}
              />
            </div>

            <div>
              <label className="block text-sm font-semibold text-gray-300 mb-1.5">
                Password
              </label>
              <div className="relative">
                <input
                  type={showPass ? 'text' : 'password'}
                  autoComplete="current-password"
                  value={form.password}
                  onChange={(e) => setForm({ ...form, password: e.target.value })}
                  placeholder="••••••••"
                  className="w-full text-white text-sm rounded-xl p-3 pr-10 outline-none transition-all placeholder-gray-600"
                  style={{
                    background: 'rgba(255,255,255,0.03)',
                    border: '1px solid rgba(130,188,74,0.2)',
                  }}
                  onFocus={e => e.target.style.borderColor = 'rgba(130,188,74,0.6)'}
                  onBlur={e => e.target.style.borderColor = 'rgba(130,188,74,0.2)'}
                />
                <button
                  type="button"
                  onClick={() => setShowPass(!showPass)}
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-500 hover:text-gray-300 transition-colors"
                >
                  {showPass ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                </button>
              </div>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full font-bold py-3 rounded-xl transition-all flex items-center justify-center gap-2 disabled:opacity-60 disabled:cursor-not-allowed font-display text-black"
              style={{
                background: loading ? '#5a8f2a' : 'linear-gradient(135deg, #82bc4a 0%, #5a8f2a 100%)',
                boxShadow: '0 10px 30px -10px rgba(130,188,65,0.5)',
              }}
            >
              {loading ? (
                <div className="w-5 h-5 border-2 border-black/40 border-t-black rounded-full animate-spin" />
              ) : (
                <>
                  <LogIn className="w-5 h-5" />
                  Sign In
                </>
              )}
            </button>
          </form>

          {/* Default credentials hint */}
          <div className="mt-6 p-4 rounded-xl border"
            style={{
              background: 'rgba(130,188,74,0.08)',
              borderColor: 'rgba(130,188,74,0.2)',
            }}
          >
            <p className="text-xs font-semibold text-[#82bc4a] mb-1">Default credentials</p>
            <p className="text-xs text-gray-400 font-mono">admin@hajrihub.ai / admin1234</p>
          </div>
        </div>

        <p className="text-center text-xs text-gray-600 mt-6">
          © 2026 Hajri Hub AI · All rights reserved
        </p>
      </motion.div>
    </div>
  )
}
