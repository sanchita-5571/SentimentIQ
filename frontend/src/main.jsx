import React from 'react'
import ReactDOM from 'react-dom/client'
import { BrowserRouter } from 'react-router-dom'
import App from './App'
import './index.css'
import { useUIStore } from './stores/uiStore'

import { useEffect } from 'react'

function InitFreshState() {
  const initTheme = useUIStore((state) => state.initTheme)

  useEffect(() => {
    initTheme()
  }, [initTheme])

  return null
}

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <BrowserRouter future={{ v7_startTransition: true, v7_relativeSplatPath: true }}>
      <InitFreshState />
      <App />
    </BrowserRouter>
  </React.StrictMode>,
)
