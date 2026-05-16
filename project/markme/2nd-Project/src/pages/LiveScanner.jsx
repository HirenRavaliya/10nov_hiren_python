import React, { useRef, useState, useEffect, useCallback } from 'react'
import Webcam from 'react-webcam'
import { motion } from 'framer-motion'
import { useStore } from '../store/store'
import toast from 'react-hot-toast'
import { Shield, ShieldAlert, Cpu, Camera, CheckCircle2, XCircle, RefreshCw } from 'lucide-react'
import clsx from 'clsx'

function dataURLtoBlob(dataURL) {
  const [header, b64] = dataURL.split(',')
  const mime = header.match(/:(.*?);/)[1]
  const binary = atob(b64)
  const arr = new Uint8Array(binary.length)
  for (let i = 0; i < binary.length; i++) arr[i] = binary.charCodeAt(i)
  return new Blob([arr], { type: mime })
}

export default function LiveScanner() {
  const webcamRef = useRef(null)
  const { token, fetchAttendanceLogs, fetchNotifications } = useStore()

  const [scanning, setScanning] = useState(false)
  const [cameraReady, setCameraReady] = useState(false)
  const [lastResult, setLastResult] = useState(null)   // last scan result
  const [isProcessing, setIsProcessing] = useState(false)
  const lastScanTime = useRef(0)

  const scanFrame = useCallback(async () => {
    if (!webcamRef.current || !cameraReady || isProcessing) return
    const now = Date.now()
    if (now - lastScanTime.current < 2500) return   // throttle: 2.5s between scans
    lastScanTime.current = now

    const imgSrc = webcamRef.current.getScreenshot({ width: 640, height: 480 })
    if (!imgSrc) return

    setIsProcessing(true)
    try {
      const blob = dataURLtoBlob(imgSrc)
      const formData = new FormData()
      formData.append('image', blob, 'frame.jpg')

      const res = await fetch('/api/attendance/scan/', {
        method: 'POST',
        headers: { Authorization: `Bearer ${token}` },
        body: formData,
      })
      const data = await res.json()

      setLastResult({ ...data, ts: Date.now() })

      if (data.matched) {
        if (!data.already_marked) {
          toast.success(`✅ ${data.student_name} — Attendance marked!`)
          fetchAttendanceLogs()
          fetchNotifications()
        }
      }
    } catch (err) {
      console.error('Scan error', err)
    } finally {
      setIsProcessing(false)
    }
  }, [cameraReady, isProcessing, token, fetchAttendanceLogs, fetchNotifications])

  useEffect(() => {
    if (!scanning) { setLastResult(null); return }
    const interval = setInterval(scanFrame, 1500)
    return () => clearInterval(interval)
  }, [scanning, scanFrame])

  const confidence = lastResult?.confidence
  const confidencePct = confidence != null ? (confidence * 100).toFixed(1) : null

  return (
    <div className="max-w-6xl mx-auto pb-12 h-full flex flex-col">
      <div className="mb-6 flex justify-between items-end">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white tracking-tight">Live AI Scanner</h1>
          <p className="text-gray-500 dark:text-gray-400 mt-2 text-sm">Real-time face recognition using backend AI engine.</p>
        </div>
        <div className={clsx(
          'flex items-center gap-2 px-4 py-2 rounded-full border text-sm font-semibold',
          scanning
            ? 'bg-green-50 border-green-200 text-green-700 dark:bg-green-500/10 dark:border-green-500/30 dark:text-green-400'
            : 'bg-gray-50 border-gray-200 text-gray-500 dark:bg-dark-800 dark:border-white/10'
        )}>
          <Cpu className="w-4 h-4" />
          {scanning ? 'AI Scanner Active' : 'Scanner Idle'}
          {isProcessing && <div className="w-3 h-3 border-2 border-current border-t-transparent rounded-full animate-spin ml-1" />}
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 flex-1 min-h-0">
        {/* Camera feed */}
        <div className="lg:col-span-2 relative bg-dark-900 rounded-3xl overflow-hidden shadow-xl border-4 border-gray-800 flex flex-col justify-center items-center min-h-[400px]">
          <Webcam
            ref={webcamRef}
            audio={false}
            screenshotFormat="image/jpeg"
            screenshotQuality={0.85}
            videoConstraints={{ facingMode: 'user', width: 1280, height: 720 }}
            onUserMedia={() => setCameraReady(true)}
            onUserMediaError={() => toast.error('Camera access denied')}
            className="w-full h-full object-cover absolute inset-0 opacity-80"
            mirrored
          />

          {/* Face guide frame */}
          {cameraReady && (
            <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
              <div className={clsx(
                'w-52 h-64 border-2 rounded-2xl transition-all duration-500',
                scanning ? 'border-primary-400/70 shadow-[0_0_20px_rgba(99,102,241,0.3)]' : 'border-white/20 border-dashed'
              )} />
            </div>
          )}

          {/* Scan line */}
          {scanning && cameraReady && (
            <div className="absolute inset-0 overflow-hidden pointer-events-none">
              <div className="w-full h-0.5 bg-gradient-to-r from-transparent via-primary-400 to-transparent animate-scan-line opacity-70" />
            </div>
          )}

          {/* Idle overlay */}
          {!scanning && (
            <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}
              className="z-10 bg-black/60 backdrop-blur-md p-8 rounded-2xl border border-white/10 text-center max-w-sm">
              <Camera className="w-12 h-12 text-primary-400 mx-auto mb-4" />
              <h3 className="text-xl font-bold text-white mb-2">Scanner Idle</h3>
              <p className="text-gray-400 text-sm mb-6">Activate to start scanning and marking attendance automatically.</p>
              <button
                onClick={() => setScanning(true)}
                disabled={!cameraReady}
                className="bg-primary-600 hover:bg-primary-500 disabled:opacity-50 text-white w-full py-3 rounded-xl font-semibold shadow-lg shadow-primary-500/30 transition-all"
              >
                {cameraReady ? 'Start AI Scanner' : 'Starting camera…'}
              </button>
            </motion.div>
          )}

          {/* Stop button */}
          {scanning && (
            <button
              onClick={() => setScanning(false)}
              className="absolute bottom-6 right-6 z-10 bg-red-600/90 hover:bg-red-500 text-white px-5 py-2.5 rounded-full text-sm font-semibold backdrop-blur-sm transition-all shadow-xl shadow-red-900/50"
            >
              Stop Scanner
            </button>
          )}
        </div>

        {/* Analysis panel */}
        <div className="bg-white dark:bg-dark-800 dark:border-white/10 rounded-3xl border border-gray-100 shadow-sm flex flex-col overflow-hidden">
          <div className="bg-gray-50 dark:bg-dark-900 p-5 border-b border-gray-100 dark:border-white/10 flex items-center gap-3">
            <Shield className="w-5 h-5 text-primary-600" />
            <h3 className="text-base font-bold text-gray-900 dark:text-white">Recognition Output</h3>
          </div>

          <div className="p-6 flex-1 flex flex-col justify-center">
            {!scanning ? (
              <div className="text-center text-gray-400">
                <ShieldAlert className="w-10 h-10 mx-auto mb-3 opacity-30" />
                <p className="text-sm">Start the scanner to see results here.</p>
              </div>
            ) : !lastResult ? (
              <div className="text-center">
                <div className="w-14 h-14 border-4 border-gray-100 dark:border-white/10 border-t-primary-500 rounded-full animate-spin mx-auto mb-4" />
                <p className="text-gray-500 dark:text-gray-400 font-medium text-sm">Scanning for faces…</p>
              </div>
            ) : (
              <motion.div
                key={lastResult.ts}
                initial={{ opacity: 0, scale: 0.92 }}
                animate={{ opacity: 1, scale: 1 }}
                className={clsx(
                  'p-6 rounded-2xl border text-center shadow-lg',
                  lastResult.matched
                    ? 'bg-green-50 border-green-200 shadow-green-100 dark:bg-green-500/10 dark:border-green-500/30'
                    : 'bg-red-50 border-red-200 shadow-red-100 dark:bg-red-500/10 dark:border-red-500/30'
                )}
              >
                {lastResult.matched ? (
                  <CheckCircle2 className="w-10 h-10 text-green-500 mx-auto mb-3" />
                ) : (
                  <XCircle className="w-10 h-10 text-red-400 mx-auto mb-3" />
                )}
                <h4 className={clsx(
                  'text-xl font-bold mb-2',
                  lastResult.matched ? 'text-green-700 dark:text-green-400' : 'text-red-600 dark:text-red-400'
                )}>
                  {lastResult.matched ? lastResult.student_name : 'No Match'}
                </h4>
                {confidencePct && (
                  <div className="mt-3 text-sm font-mono bg-white/60 dark:bg-black/20 py-2 rounded-lg text-gray-600 dark:text-gray-300 inline-block px-4">
                    Confidence: {confidencePct}%
                  </div>
                )}
                <p className={clsx(
                  'mt-3 text-xs font-semibold uppercase tracking-wide',
                  lastResult.matched ? 'text-green-600 dark:text-green-400' : 'text-red-500'
                )}>
                  {lastResult.matched
                    ? (lastResult.already_marked ? 'Already marked today' : 'Attendance Verified ✓')
                    : (lastResult.face_found === false ? 'No face detected' : 'Unknown person')
                  }
                </p>
              </motion.div>
            )}
          </div>

          {/* Info */}
          <div className="px-5 pb-5 pt-0">
            <div className="bg-gray-50 dark:bg-dark-900 rounded-xl p-4 border border-gray-100 dark:border-white/5 space-y-2 text-xs text-gray-500 dark:text-gray-400">
              <div className="flex justify-between">
                <span>AI Engine</span>
                <span className="font-semibold text-green-600 dark:text-green-400">face_recognition (dlib)</span>
              </div>
              <div className="flex justify-between">
                <span>Scan interval</span>
                <span className="font-semibold text-gray-700 dark:text-gray-300">2.5 seconds</span>
              </div>
              <div className="flex justify-between">
                <span>Status</span>
                <span className={clsx('font-semibold', scanning ? 'text-green-600 dark:text-green-400' : 'text-gray-500')}>{scanning ? 'ACTIVE' : 'IDLE'}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
