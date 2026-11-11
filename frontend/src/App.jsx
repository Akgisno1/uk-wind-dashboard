import { useEffect, useState } from 'react'

// Trailing slashes in VITE_API_URL would produce '//api/health', which Vercel
// answers with a 308 redirect that carries no CORS headers. Strip them.
const API = (import.meta.env.VITE_API_URL || '').replace(/\/+$/, '')

function App() {
  const [status, setStatus] = useState('loading...')

  useEffect(() => {
    fetch(`${API}/api/health`)
      .then((res) => {
        if (!res.ok) throw new Error(`HTTP ${res.status}`)
        return res.json()
      })
      .then((data) => setStatus(data.status))
      .catch((err) => {
        console.error('Health check failed:', err)
        setStatus('backend not reachable')
      })
  }, [])

  return (
    <main style={{ padding: '2rem' }}>
      <h1>UK Wind Forecast Portal</h1>
      <p>Backend status: {status}</p>
    </main>
  )
}

export default App
