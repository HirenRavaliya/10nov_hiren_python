import React from 'react'
import { Bell, Search, Filter, Calendar, Download, Menu, LogOut } from 'lucide-react'
import { useStore } from '../../store/store'

export default function Header() {
  const { globalSearch, setGlobalSearch, toggleMobileMenu, currentUser, logout } = useStore()

  // Generate initials from name
  const initials = (currentUser?.full_name || 'A')
    .split(' ')
    .map(w => w[0])
    .slice(0, 2)
    .join('')
    .toUpperCase()

  return (
    <header className="h-20 bg-dark-800 border-b border-white/10 flex items-center justify-between px-4 md:px-8 z-20 shadow-sm shrink-0">
      <div className="flex items-center gap-4 flex-1">
        <button onClick={toggleMobileMenu} className="md:hidden p-2 text-gray-400 hover:text-white transition-colors">
          <Menu className="w-6 h-6" />
        </button>
        
        <div className="flex-1 max-w-xl">
          <div className="relative flex items-center hidden sm:flex">
            <Search className="w-5 h-5 text-gray-500 absolute left-4" />
            <input 
              type="text" 
              value={globalSearch}
              onChange={(e) => setGlobalSearch(e.target.value)}
              placeholder="Search profiles, events..." 
              className="w-full bg-dark-900 pl-11 pr-16 md:pr-24 py-2.5 rounded-full text-sm outline-none border border-white/10 focus:border-primary-500/60 transition-all text-gray-200 placeholder-gray-600"
            />
            <div className="absolute right-4 flex items-center gap-2 text-gray-600 hidden md:flex">
              <Filter className="w-4 h-4 cursor-pointer hover:text-gray-300 transition-colors" />
              <Calendar className="w-4 h-4 cursor-pointer hover:text-gray-300 transition-colors" />
            </div>
          </div>
        </div>
      </div>

      <div className="flex items-center gap-3 md:gap-6">
        <button className="relative p-2 text-gray-500 hover:text-gray-300 transition-colors hidden sm:block">
          <Bell className="w-5 h-5" />
          <span className="absolute top-1.5 right-1.5 w-2 h-2 bg-red-500 rounded-full border border-dark-800"></span>
        </button>

        <button className="bg-primary-500 hover:bg-primary-600 text-black px-4 md:px-5 py-2 md:py-2.5 rounded-full text-sm font-bold flex items-center gap-2 shadow-md shadow-primary-500/30 transition-all hidden md:flex font-display">
          <Download className="w-4 h-4" />
          Export
        </button>

        <div className="h-8 w-px bg-white/10 hidden sm:block"></div>

        <div className="flex items-center gap-3 cursor-pointer group">
          <div className="text-right hidden md:block">
            <p className="text-sm font-semibold text-white leading-tight">{currentUser?.full_name || 'Admin'}</p>
            <p className="text-xs text-gray-500">{currentUser?.role || 'Administrator'}</p>
          </div>
          <div className="w-9 h-9 md:w-10 md:h-10 rounded-full bg-primary-500 overflow-hidden ring-2 ring-transparent group-hover:ring-primary-400 transition-all flex items-center justify-center">
            <span className="text-black font-bold text-sm select-none font-display">{initials}</span>
          </div>
        </div>

        <button
          onClick={() => logout()}
          className="p-2 text-gray-500 hover:text-red-400 transition-colors"
          title="Logout"
        >
          <LogOut className="w-5 h-5" />
        </button>
      </div>
    </header>
  )
}
