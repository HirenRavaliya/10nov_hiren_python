import React, { useEffect, useState } from 'react'
import { NavLink } from 'react-router-dom'
import { LayoutDashboard, Camera, Users, MessageSquare, Activity, BarChart3, X, UserCog, CalendarClock } from 'lucide-react'
import clsx from 'clsx'
import { useStore } from '../../store/store'

const BASE_NAV_ITEMS = [
  { name: 'Dashboard',          path: '/',              icon: LayoutDashboard },
  { name: 'Live Scanner',       path: '/scanner',       icon: Camera },
  { name: 'Student Analytics',  path: '/analytics',     icon: BarChart3 },
  { name: 'Access Management',  path: '/students',      icon: Users },
  { name: 'Teacher Management', path: '/teachers',      icon: UserCog },
  { name: 'Notification Logs',  path: '/notifications', icon: MessageSquare },
]

// Leave Requests is only available for educational institutions
const LEAVE_REQUEST_ITEM = {
  name: 'Leave Requests',
  path: '/leaves',
  icon: CalendarClock,
  badge: true,
}

export default function Sidebar() {
  const { mobileMenuOpen, setMobileMenuOpen, token, orgType } = useStore()
  const [pendingCount, setPendingCount] = useState(0)
  const isEducational = orgType === 'educational'

  // Build nav items based on org type
  const navItems = isEducational
    ? [
        ...BASE_NAV_ITEMS.slice(0, 5),
        LEAVE_REQUEST_ITEM,
        ...BASE_NAV_ITEMS.slice(5),
      ]
    : BASE_NAV_ITEMS

  useEffect(() => {
    if (!token || !isEducational) return
    fetch('/api/attendance/leave-requests/?status=PENDING&page_size=1', {
      headers: { Authorization: `Bearer ${token}` }
    })
      .then(r => r.json())
      .then(d => setPendingCount(d.count || 0))
      .catch(() => {})
  }, [token, isEducational])

  return (
    <>
      {/* Mobile Overlay */}
      {mobileMenuOpen && (
        <div 
          className="fixed inset-0 bg-gray-900/50 backdrop-blur-sm z-30 md:hidden"
          onClick={() => setMobileMenuOpen(false)}
        />
      )}
      
      <aside className={clsx(
        "w-64 bg-white dark:bg-dark-800 border-r border-gray-100 dark:border-white/10 flex flex-col h-full shadow-sm z-40 transition-transform duration-300 fixed inset-y-0 left-0 md:relative md:translate-x-0",
        mobileMenuOpen ? "translate-x-0" : "-translate-x-full"
      )}>
        {/* Logo — Hajri Hub brand */}
        <div className="h-20 flex items-center justify-between px-6 shrink-0 border-b border-gray-100 dark:border-white/10">
          <div className="flex items-center gap-3">
            <img
              src="/hajrihub-logo.png"
              alt="Hajri Hub"
              className="h-9 object-contain"
            />
          </div>
          <button 
            onClick={() => setMobileMenuOpen(false)}
            className="md:hidden text-gray-500 hover:text-gray-900 dark:text-gray-400 dark:hover:text-white"
          >
            <X className="w-6 h-6" />
          </button>
        </div>

        <div className="px-6 py-4 flex-1 overflow-y-auto">
          <p className="text-xs font-semibold text-gray-400 dark:text-gray-500 uppercase tracking-wider mb-4">Main Navigation</p>
          <nav className="flex flex-col gap-1">
            {navItems.map((item) => (
              <NavLink
                key={item.name}
                to={item.path}
                onClick={() => setMobileMenuOpen(false)}
                className={({ isActive }) => clsx(
                  "flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium transition-all duration-200",
                  isActive 
                    ? "bg-primary-500/10 dark:bg-primary-500/10 text-primary-700 dark:text-primary-400 shadow-sm border border-primary-500/20" 
                    : "text-gray-600 dark:text-gray-400 hover:bg-gray-50 dark:hover:bg-dark-900 hover:text-gray-900 dark:hover:text-gray-200 border border-transparent"
                )}
              >
                <item.icon className="w-5 h-5" />
                {item.name}
                {item.badge && pendingCount > 0 && (
                  <span className="ml-auto bg-amber-500 text-white text-xs font-bold px-1.5 py-0.5 rounded-full min-w-[20px] text-center">
                    {pendingCount}
                  </span>
                )}
              </NavLink>
            ))}
          </nav>
        </div>

        <div className="mt-auto p-6 shrink-0">
          <div className="bg-primary-500/10 dark:bg-dark-900 rounded-xl p-4 flex items-center gap-3 border border-primary-500/20 dark:border-white/10">
            <div className="bg-primary-500/20 dark:bg-primary-500/20 p-2 rounded-lg text-primary-600 dark:text-primary-400">
              <Activity className="w-5 h-5 animate-pulse" />
            </div>
            <div>
              <p className="text-sm font-semibold text-gray-800 dark:text-gray-200">System Health</p>
              <p className="text-xs text-gray-500 dark:text-gray-500">Stable • 99.9% Uptime</p>
            </div>
          </div>
        </div>
      </aside>
    </>
  )
}
