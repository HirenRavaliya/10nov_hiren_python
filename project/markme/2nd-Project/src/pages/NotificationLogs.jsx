import React from 'react'
import { MessageSquare, PhoneOutgoing, Clock, CheckCircle2 } from 'lucide-react'
import { useStore } from '../store/store'
import { motion } from 'framer-motion'

export default function NotificationLogs() {
  const notificationLogs = useStore(state => state.notificationLogs)
  const students = useStore(state => state.students)
  
  const sortedLogs = [...notificationLogs].sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp))

  return (
    <div className="max-w-6xl mx-auto pb-12 w-full">
      <div className="mb-8">
         <h1 className="text-3xl font-bold text-white tracking-tight">Notification Terminal</h1>
         <p className="text-gray-400 mt-2 text-sm">Real-time simulator of guardian messaging dispatch. Shows outgoing SMS notifications triggered by biometric validations.</p>
      </div>

      <div className="bg-dark-800 border border-white/10 rounded-2xl overflow-hidden">
        <div className="bg-dark-900/60 px-6 py-4 flex items-center justify-between border-b border-white/10">
           <div className="flex gap-2 items-center">
              <MessageSquare className="w-5 h-5 text-gray-400" />
              <span className="font-semibold text-gray-300 text-sm">Transmission History ({sortedLogs.length})</span>
           </div>
           
           <div className="flex items-center gap-2">
              <span className="relative flex h-3 w-3">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-primary-400 opacity-75"></span>
                <span className="relative inline-flex rounded-full h-3 w-3 bg-primary-500"></span>
              </span>
              <span className="text-xs font-semibold text-primary-400 bg-primary-500/10 px-2 py-0.5 rounded-md border border-primary-500/20">ACTIVE GATEWAY</span>
           </div>
        </div>

        {sortedLogs.length === 0 ? (
           <div className="p-16 text-center text-gray-600">
              <PhoneOutgoing className="w-12 h-12 mx-auto mb-4 opacity-20" />
              <p>No messages have been dispatched yet.</p>
           </div>
        ) : (
           <div className="divide-y divide-white/5">
             {sortedLogs.map((log, i) => {
               const student = students.find(s => s.id === log.studentId)
               return (
                  <motion.div 
                     initial={{ opacity: 0, y: 10 }}
                     animate={{ opacity: 1, y: 0 }}
                     transition={{ delay: i * 0.05 }}
                     key={log.id} 
                     className="px-6 py-4 hover:bg-primary-500/5 transition-colors flex flex-col md:flex-row md:items-center gap-4 justify-between"
                  >
                     <div className="flex items-start gap-4">
                        <div className="mt-1 bg-primary-500/10 text-primary-400 p-2 rounded-lg items-center justify-center shrink-0 border border-primary-500/20">
                           <PhoneOutgoing className="w-4 h-4" />
                        </div>
                        <div>
                           <div className="flex items-center gap-2">
                              <h4 className="text-sm font-bold text-white">SMS Outbound</h4>
                              <span className="bg-dark-900 text-gray-500 text-[10px] font-bold px-2 py-0.5 rounded-md tracking-wider border border-white/10">
                                 TO: {student?.guardianPhone || 'Unknown'}
                              </span>
                           </div>
                           
                           <div className="bg-dark-900 border-l-2 border-primary-500 p-3 mt-2 rounded-r-lg text-sm text-gray-400 italic">
                              {student?.name}&apos;s attendance was logged securely at {new Date(log.timestamp).toLocaleTimeString()}.
                           </div>
                        </div>
                     </div>
                     
                     <div className="flex items-center gap-8 md:flex-col md:items-end justify-between pl-12 md:pl-0 border-t md:border-t-0 pt-4 md:pt-0 mt-2 md:mt-0 border-white/10">
                        <div className="flex items-center gap-1.5 text-primary-400 text-xs font-semibold">
                           <CheckCircle2 className="w-4 h-4" />
                           DELIVERED
                        </div>
                        <div className="flex items-center gap-1.5 text-gray-500 text-xs font-medium">
                           <Clock className="w-3.5 h-3.5" />
                           {new Date(log.timestamp).toLocaleString([], { dateStyle: 'short', timeStyle: 'short' })}
                        </div>
                     </div>
                  </motion.div>
               )
             })}
           </div>
        )}
      </div>
    </div>
  )
}
