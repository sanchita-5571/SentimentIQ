import { Route, Routes } from 'react-router-dom'
import { Toaster } from 'react-hot-toast'
import Layout from './components/Layout/Layout'
import ErrorBoundary from './components/UI/ErrorBoundary'
import DashboardPage from './pages/DashboardPage'
import TrendsPage from './pages/TrendsPage'
import RootCausePage from './pages/RootCausePage'
import VerbatimsPage from './pages/VerbatimsPage'
import ReportsPage from './pages/ReportsPage'

export default function App() {
  return (
    <ErrorBoundary>
      <Toaster position="top-right" />
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<DashboardPage />} />
          <Route path="trends" element={<TrendsPage />} />
          <Route path="root-causes" element={<RootCausePage />} />
          <Route path="verbatims" element={<VerbatimsPage />} />
          <Route path="reports" element={<ReportsPage />} />
        </Route>
      </Routes>
    </ErrorBoundary>
  )
}
