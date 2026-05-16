import React from 'react'
import { Users, Camera, ShieldAlert, CheckCircle2, AlertCircle } from 'lucide-react'
import { useStore } from '../store/store'
import { motion } from 'framer-motion'
import clsx from 'clsx'
import { getLocalDateKey } from '../utils/date'

export default function Dashboard() {
  const students = useStore(state => state.students)
  const attendanceLogs = useStore(state => state.attendanceLogs)
  const todayKey = getLocalDateKey()
  const scansToday = attendanceLogs.filter((log) => (log.dateKey || getLocalDateKey(log.timestamp)) === todayKey).length
  const studentsWithoutBiometric = students.filter((student) => !student.descriptor || Object.keys(student.descriptor).length === 0).length

  // Sort logs by time desc
  const sortedLogs = [...attendanceLogs].sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp))
  const recentLogs = sortedLogs.slice(0, 5) // top 5

  const stats = [
    { name: 'Total Students',    value: students.length,           icon: Users,      color: 'text-primary-400', bg: 'bg-primary-500/10' },
    { name: 'Total Scans Today', value: scansToday,                icon: Camera,     color: 'text-primary-400', bg: 'bg-primary-500/10' },
    { name: 'Security Alerts',   value: studentsWithoutBiometric,  icon: ShieldAlert, color: 'text-red-400',     bg: 'bg-red-500/10'     },
  ]

  return (
    <div className="max-w-6xl mx-auto space-y-8 pb-12">
      <div>
        <h1 className="text-3xl font-bold text-white font-display tracking-tight">System Activity Logs</h1>
        <p className="text-gray-400 mt-2 text-sm max-w-2xl">Monitoring all real-time interactions, security events, and biometric validations. Ensure all models and cameras operate correctly.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {stats.map((stat, i) => (
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: i * 0.1 }}
            key={stat.name} 
            className="bg-dark-800 border border-white/10 rounded-2xl p-6 flex items-center gap-5 hover:border-primary-500/30 transition-all"
          >
            <div className={clsx("w-14 h-14 rounded-full flex items-center justify-center", stat.bg)}>
              <stat.icon className={clsx("w-7 h-7", stat.color)} />
            </div>
            <div>
              <p className="text-sm font-medium text-gray-400">{stat.name}</p>
              <h3 className="text-2xl font-bold text-white mt-1">{stat.value}</h3>
            </div>
          </motion.div>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 ">
        <div className="lg:col-span-2 bg-dark-800 border border-white/10 rounded-2xl p-6 max-h-[600px] overflow-y-auto">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-lg font-bold text-white border-b border-white/10 pb-4 w-full">Recent Biometric Events</h2>
          </div>
          
          <div className="space-y-6">
            {recentLogs.length === 0 ? (
              <p className="text-gray-400 text-sm text-center py-8">No recent activity found today.</p>
            ) : (
              recentLogs.map((log, i) => {
                const student = students.find(s => s.id === log.studentId)
                return (
                  <motion.div 
                    initial={{ opacity: 0, x: -10 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: i * 0.1 }}
                    key={log.id} 
                    className="flex gap-4 items-start relative group"
                  >
                    <div className="w-10 h-10 rounded-full bg-dark-900 flex items-center justify-center shrink-0 z-10 border-2 border-dark-800 overflow-hidden shadow-lg">
                      {student?.profilePic ? (
                        <img src={student.profilePic} alt="" className="w-full h-full object-cover"/>
                      ) : (
                        <CheckCircle2 className="w-5 h-5 text-primary-500" />
                      )}
                    </div>
                    <div className="bg-dark-900/50 rounded-xl p-4 flex-1 border border-white/5 group-hover:border-primary-500/30 transition-colors">
                      <div className="flex justify-between items-start">
                        <div>
                          <p className="text-sm text-gray-300">
                            <span className="font-bold text-primary-400">{student?.name || 'Unknown'}</span> successfully identified via biometrics.
                          </p>
                          <p className="text-xs text-gray-500 mt-1">Status: {log.status}</p>
                        </div>
                        <span className="text-xs font-semibold text-gray-400 bg-dark-800 px-2 py-1 rounded-md border border-white/10 shadow-sm">
                          {new Date(log.timestamp).toLocaleTimeString([], { hour: '2-digit', minute:'2-digit' })}
                        </span>
                      </div>
                    </div>
                  </motion.div>
                )
              })
            )}
          </div>
        </div>

        <div className="bg-dark-800 border border-white/10 rounded-2xl p-6 overflow-hidden">
          <div className="flex items-center gap-3 mb-6">
            <div className="p-2 bg-primary-500/10 text-primary-400 rounded-lg"><AlertCircle className="w-5 h-5" /></div>
            <h2 className="text-lg font-bold text-white">System Activity</h2>
          </div>
          <div className="space-y-4">
            <div className="flex justify-between items-center bg-dark-900 p-3 rounded-lg border border-white/5">
               <div>
                  <p className="text-sm font-medium text-gray-300">AI Model Status</p>
                  <p className="text-xs text-gray-500">tiny_face_detector</p>
               </div>
               <span className="text-xs font-bold bg-primary-500/10 text-primary-400 px-2 py-1 rounded-full border border-primary-500/20">LOADED</span>
            </div>
            <div className="flex justify-between items-center bg-dark-900 p-3 rounded-lg border border-white/5">
               <div>
                  <p className="text-sm font-medium text-gray-300">Face Match Status</p>
                  <p className="text-xs text-gray-500">recognition_net</p>
               </div>
               <span className="text-xs font-bold bg-primary-500/10 text-primary-400 px-2 py-1 rounded-full border border-primary-500/20">LOADED</span>
            </div>
            <div className="flex justify-between items-center p-3">
              <span className="text-sm text-gray-500">Background Sync</span>
              <span className="text-sm font-semibold text-gray-300">Active</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
