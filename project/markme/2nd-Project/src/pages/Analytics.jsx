import React, { useMemo, useState } from 'react'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, AreaChart, Area } from 'recharts'
import { Users, CalendarDays } from 'lucide-react'
import { useStore } from '../store/store'
import { getLocalDateKey } from '../utils/date'

export default function Analytics() {
  const { students, attendanceLogs } = useStore()
  const [selectedStudent, setSelectedStudent] = useState('ALL')

  // Generate 30-day mock or real chart data
  const chartData = useMemo(() => {
    const data = []
    const today = new Date()
    today.setHours(0,0,0,0)

    for (let i = 29; i >= 0; i--) {
      const d = new Date(today)
      d.setDate(d.getDate() - i)
      
      const dateString = getLocalDateKey(d)
      
      // Filter logs for this day
      const dayLogs = attendanceLogs.filter((log) => (log.dateKey || getLocalDateKey(log.timestamp)) === dateString)
      
      let presentCount = 0
      if (selectedStudent === 'ALL') {
         // Unique students present that day
         const uniqueStudents = new Set(dayLogs.map(l => l.studentId))
         presentCount = uniqueStudents.size
      } else {
         // Did the selected student show up?
         const studentPresent = dayLogs.some(l => l.studentId === selectedStudent)
         presentCount = studentPresent ? 1 : 0
      }

      data.push({
        date: d.toLocaleDateString([], { month: 'short', day: 'numeric' }),
        attendance: presentCount
      })
    }
    return data
  }, [attendanceLogs, selectedStudent])

  const currentSelectionName = selectedStudent === 'ALL' 
    ? "All Enrolled Users" 
    : students.find(s => s.id === selectedStudent)?.name

  return (
    <div className="max-w-6xl mx-auto space-y-8 pb-12">
      <div className="flex flex-col md:flex-row md:items-end justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white font-sans tracking-tight">Student Analytics</h1>
          <p className="text-gray-500 dark:text-gray-400 mt-2 text-sm max-w-2xl">
            Detailed 30-day biometric engagement metrics. Filter by individual profiles to see monthly attendance graphs.
          </p>
        </div>
        
        <div className="bg-white dark:bg-dark-800 border border-gray-100 dark:border-white/10 p-2 rounded-xl flex items-center shadow-sm">
           <Users className="w-5 h-5 text-gray-400 ml-2" />
           <select 
             value={selectedStudent} 
             onChange={(e) => setSelectedStudent(e.target.value)}
             className="bg-transparent border-none focus:ring-0 text-sm font-semibold text-gray-700 dark:text-gray-200 p-2 outline-none cursor-pointer"
           >
              <option value="ALL">All Enrolled Base</option>
              {students.map(s => (
                 <option key={s.id} value={s.id}>{s.name}</option>
              ))}
           </select>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
         <div className="bg-gradient-to-br from-primary-500 to-primary-700 rounded-3xl p-6 text-white shadow-lg relative overflow-hidden">
            <div className="absolute top-0 right-0 p-6 opacity-30">
               <CalendarDays className="w-16 h-16" />
            </div>
            <h3 className="text-primary-100 text-sm font-semibold uppercase tracking-wider mb-2">Subject Analysed</h3>
            <p className="text-3xl font-bold">{currentSelectionName}</p>
         </div>

         <div className="bg-white dark:bg-dark-800 border border-gray-100 dark:border-white/10 rounded-3xl p-6 shadow-sm">
            <h3 className="text-gray-500 dark:text-gray-400 text-sm font-semibold uppercase tracking-wider mb-2">Overall Rate (30 Days)</h3>
            <p className="text-3xl font-bold text-gray-900 dark:text-white">
               {selectedStudent === 'ALL' 
                  ? ((chartData.reduce((acc, curr) => acc + curr.attendance, 0) / (30 * (students.length || 1))) * 100).toFixed(1) + '%' 
                  : ((chartData.reduce((acc, curr) => acc + curr.attendance, 0) / 30) * 100).toFixed(1) + '%'
               }
            </p>
         </div>
      </div>

      <div className="bg-white dark:bg-dark-800 border border-gray-100 dark:border-white/10 rounded-3xl p-8 shadow-sm">
         <div className="flex justify-between items-center mb-8 border-b border-gray-100 dark:border-white/10 pb-4">
            <h2 className="text-xl font-bold text-gray-900 dark:text-white">30-Day Activity Graph</h2>
            <div className="flex gap-2">
               <span className="flex items-center gap-2 text-xs font-semibold text-gray-500 dark:text-gray-400">
                  <span className="w-3 h-3 rounded-full bg-primary-500"></span>
                  Verified Scans
               </span>
            </div>
         </div>
         
         <div className="h-80 w-full">
            <ResponsiveContainer width="100%" height="100%">
              {selectedStudent === 'ALL' ? (
               <AreaChart data={chartData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                  <defs>
                    <linearGradient id="colorPv" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#6366f1" stopOpacity={0.3}/>
                      <stop offset="95%" stopColor="#6366f1" stopOpacity={0}/>
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#374151" opacity={0.2} />
                  <XAxis dataKey="date" tick={{fontSize: 12}} tickMargin={10} stroke="#9ca3af" />
                  <YAxis tick={{fontSize: 12}} tickMargin={10} stroke="#9ca3af" />
                  <Tooltip 
                     contentStyle={{ backgroundColor: '#1e1e2d', borderColor: '#374151', borderRadius: '8px', color: '#fff' }}
                     itemStyle={{ color: '#818cf8', fontWeight: 'bold' }}
                  />
                  <Area type="monotone" dataKey="attendance" stroke="#6366f1" strokeWidth={3} fillOpacity={1} fill="url(#colorPv)" />
               </AreaChart>
              ) : (
               <BarChart data={chartData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                  <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#374151" opacity={0.2} />
                  <XAxis dataKey="date" tick={{fontSize: 12}} tickMargin={10} stroke="#9ca3af" />
                  <YAxis allowDecimals={false} tick={{fontSize: 12}} tickMargin={10} stroke="#9ca3af" domain={[0, 1]} />
                  <Tooltip 
                     cursor={{ fill: 'rgba(99, 102, 241, 0.1)' }}
                     contentStyle={{ backgroundColor: '#1e1e2d', borderColor: '#374151', borderRadius: '8px', color: '#fff' }}
                     formatter={(value) => [value === 1 ? 'Present' : 'Absent', 'Status']}
                  />
                  <Bar dataKey="attendance" fill="#6366f1" radius={[4, 4, 0, 0]} />
               </BarChart>
              )}
            </ResponsiveContainer>
         </div>
      </div>
    </div>
  )
}
