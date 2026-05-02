import { Navigate } from 'react-router-dom'

// Login page is no longer needed - redirect to dashboard
export default function LoginPage() {
  return <Navigate to="/" replace />
}
