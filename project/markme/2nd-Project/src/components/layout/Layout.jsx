import React, { useEffect } from 'react'
import { Outlet } from 'react-router-dom'
import Sidebar from './Sidebar'
import Header from './Header'

export default function Layout() {
  // Always dark mode — permanently applied
  useEffect(() => {
    document.documentElement.classList.add('dark')
  }, [])

  return (
    <div className="flex h-screen bg-dark-900 transition-colors duration-300 overflow-hidden text-gray-100">
      <Sidebar />
      <div className="flex-1 flex flex-col relative w-full overflow-hidden">
        <Header />
        <main className="flex-1 overflow-y-auto p-8 z-10 w-full relative">
          <Outlet />
        </main>
      </div>
    </div>
  )
}
