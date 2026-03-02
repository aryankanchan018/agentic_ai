import { useState } from 'react'
import './App.css'
import DataInput from './components/DataInput'
import TimetableView from './components/TimetableView'

function App() {
  const [timetable, setTimetable] = useState(null)
  const [loading, setLoading] = useState(false)

  const handleGenerate = async (data) => {
    setLoading(true)
    try {
      const response = await fetch('/api/generate-timetable/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      })
      const result = await response.json()
      setTimetable(result)
    } catch (error) {
      console.error('Error generating timetable:', error)
    }
    setLoading(false)
  }

  return (
    <div className="App">
      <header>
        <h1>University Timetable Management System</h1>
        <p>Powered by Agentic AI</p>
      </header>
      
      <main>
        <DataInput onGenerate={handleGenerate} loading={loading} />
        {timetable && <TimetableView data={timetable} />}
      </main>
    </div>
  )
}

export default App
