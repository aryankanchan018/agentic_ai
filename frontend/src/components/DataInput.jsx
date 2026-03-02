import { useState } from 'react'

function DataInput({ onGenerate, loading }) {
  const [activeTab, setActiveTab] = useState('departments')
  const [formData, setFormData] = useState({
    departments: [],
    subjects: [],
    rooms: [],
    faculty: [],
    divisions: []
  })

  const addDepartment = () => {
    const name = prompt('Department Name:')
    const code = prompt('Department Code:')
    if (name && code) {
      setFormData(prev => ({
        ...prev,
        departments: [...prev.departments, { name, code, id: Date.now() }]
      }))
    }
  }

  const addSubject = () => {
    const name = prompt('Subject Name:')
    const code = prompt('Subject Code:')
    const hours = parseInt(prompt('Hours per week:', '4'))
    const isLab = confirm('Is this a lab subject?')
    const deptId = formData.departments[0]?.id
    if (name && code && deptId) {
      setFormData(prev => ({
        ...prev,
        subjects: [...prev.subjects, { name, code, hours_per_week: hours, is_lab: isLab, department_id: deptId, id: Date.now() }]
      }))
    }
  }

  const addRoom = () => {
    const roomNumber = prompt('Room Number:')
    const floor = parseInt(prompt('Floor:', '1'))
    const capacity = parseInt(prompt('Capacity:', '60'))
    const benchCount = parseInt(prompt('Bench Count:', '30'))
    const isLab = confirm('Is this a lab?')
    if (roomNumber) {
      setFormData(prev => ({
        ...prev,
        rooms: [...prev.rooms, { room_number: roomNumber, floor, capacity, bench_count: benchCount, is_lab: isLab, room_type: isLab ? 'Lab' : 'Classroom', id: Date.now() }]
      }))
    }
  }

  const addFaculty = () => {
    const name = prompt('Faculty Name:')
    const empId = prompt('Employee ID:')
    const deptId = formData.departments[0]?.id
    if (name && empId && deptId) {
      setFormData(prev => ({
        ...prev,
        faculty: [...prev.faculty, { name, employee_id: empId, department_id: deptId, id: Date.now() }]
      }))
    }
  }

  const addDivision = () => {
    const name = prompt('Division Name (e.g., CS-A):')
    const year = parseInt(prompt('Year:', '2'))
    const studentCount = parseInt(prompt('Student Count:', '50'))
    const deptId = formData.departments[0]?.id
    if (name && deptId) {
      setFormData(prev => ({
        ...prev,
        divisions: [...prev.divisions, { name, year, student_count: studentCount, department_id: deptId, id: Date.now() }]
      }))
    }
  }

  const handleGenerate = async () => {
    try {
      const deptIds = []
      for (const dept of formData.departments) {
        const res = await fetch('/api/departments/', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(dept)
        })
        const saved = await res.json()
        deptIds.push(saved.id)
      }

      for (const subj of formData.subjects) {
        await fetch('/api/subjects/', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(subj)
        })
      }

      for (const room of formData.rooms) {
        await fetch('/api/rooms/', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(room)
        })
      }

      for (const fac of formData.faculty) {
        await fetch('/api/faculty/', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(fac)
        })
      }

      for (const div of formData.divisions) {
        await fetch('/api/divisions/', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(div)
        })
      }

      onGenerate({ department_ids: deptIds })
    } catch (error) {
      console.error('Error saving data:', error)
    }
  }

  const canGenerate = formData.departments.length > 0 && 
                      formData.subjects.length > 0 && 
                      formData.rooms.length > 0 && 
                      formData.faculty.length > 0 && 
                      formData.divisions.length > 0

  return (
    <div className="data-input-modern">
      <div className="input-header">
        <h2>Input Your University Data</h2>
        <p>Add your departments, subjects, rooms, faculty, and divisions</p>
      </div>

      <div className="tabs">
        <button className={activeTab === 'departments' ? 'active' : ''} onClick={() => setActiveTab('departments')}>Departments ({formData.departments.length})</button>
        <button className={activeTab === 'subjects' ? 'active' : ''} onClick={() => setActiveTab('subjects')}>Subjects ({formData.subjects.length})</button>
        <button className={activeTab === 'rooms' ? 'active' : ''} onClick={() => setActiveTab('rooms')}>Rooms ({formData.rooms.length})</button>
        <button className={activeTab === 'faculty' ? 'active' : ''} onClick={() => setActiveTab('faculty')}>Faculty ({formData.faculty.length})</button>
        <button className={activeTab === 'divisions' ? 'active' : ''} onClick={() => setActiveTab('divisions')}>Divisions ({formData.divisions.length})</button>
      </div>

      <div className="tab-content">
        {activeTab === 'departments' && (
          <div className="tab-panel">
            <button className="add-btn" onClick={addDepartment}>+ Add Department</button>
            <div className="items-list">
              {formData.departments.map(d => (
                <div key={d.id} className="item-card">
                  <strong>{d.name}</strong>
                  <span className="badge">{d.code}</span>
                </div>
              ))}
            </div>
          </div>
        )}

        {activeTab === 'subjects' && (
          <div className="tab-panel">
            <button className="add-btn" onClick={addSubject}>+ Add Subject</button>
            <div className="items-list">
              {formData.subjects.map(s => (
                <div key={s.id} className="item-card">
                  <strong>{s.name}</strong>
                  <span className="badge">{s.code}</span>
                  <span className="info">{s.hours_per_week}h/week</span>
                  {s.is_lab && <span className="badge lab">LAB</span>}
                </div>
              ))}
            </div>
          </div>
        )}

        {activeTab === 'rooms' && (
          <div className="tab-panel">
            <button className="add-btn" onClick={addRoom}>+ Add Room</button>
            <div className="items-list">
              {formData.rooms.map(r => (
                <div key={r.id} className="item-card">
                  <strong>Room {r.room_number}</strong>
                  <span className="info">Floor {r.floor}</span>
                  <span className="info">Capacity: {r.capacity}</span>
                  <span className="info">Benches: {r.bench_count}</span>
                  {r.is_lab && <span className="badge lab">LAB</span>}
                </div>
              ))}
            </div>
          </div>
        )}

        {activeTab === 'faculty' && (
          <div className="tab-panel">
            <button className="add-btn" onClick={addFaculty}>+ Add Faculty</button>
            <div className="items-list">
              {formData.faculty.map(f => (
                <div key={f.id} className="item-card">
                  <strong>{f.name}</strong>
                  <span className="badge">{f.employee_id}</span>
                </div>
              ))}
            </div>
          </div>
        )}

        {activeTab === 'divisions' && (
          <div className="tab-panel">
            <button className="add-btn" onClick={addDivision}>+ Add Division</button>
            <div className="items-list">
              {formData.divisions.map(d => (
                <div key={d.id} className="item-card">
                  <strong>{d.name}</strong>
                  <span className="info">Year {d.year}</span>
                  <span className="info">{d.student_count} students</span>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>

      <div className="generate-section">
        <button 
          className="generate-btn" 
          onClick={handleGenerate} 
          disabled={!canGenerate || loading}
        >
          {loading ? 'Generating Timetable...' : 'Generate Timetable'}
        </button>
        {!canGenerate && <p className="hint">Add at least one item in each category to generate</p>}
      </div>
    </div>
  )
}

export default DataInput
