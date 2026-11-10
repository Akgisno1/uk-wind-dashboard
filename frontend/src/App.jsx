import { useEffect, useState } from 'react'

const API = import.meta.env.VITE_API_URL || ''

function App() {
  const [status, setStatus] = useState('loading...')

  useEffect(() => {
    fetch(`${API}/api/health`)
      .then((res) => res.json())
      .then((data) => setStatus(data.status))
      .catch(() => setStatus('backend not reachable'))
  }, [])

  return (
    <main style={{ padding: '2rem' }}>
      <h1>UK Wind Forecast Portal</h1>
      <p>Backend status: {status}</p>
    </main>
  )
}

export default App
