import { useState } from 'react'

function ReviewData({ data, onBack, onGenerate, loading }) {
  const [selectedDepts, setSelectedDepts] = useState(data.departments.map(d => d.id))
  const [confirmed, setConfirmed] = useState(false)

  const handleGenerate = () => {
    if (confirmed) {
      onGenerate(selectedDepts)
    } else {
      alert('Please confirm that all data is correct before generating timetable')
    }
  }

  return (
    <div className="review-container">
      <div className="review-header">
        <h2>Step 2: Review & Verify Data</h2>
        <p>Please review all entered data carefully before proceeding</p>
      </div>

      <div className="review-sections">
        <div className="review-section">
          <h3>Departments ({data.departments.length})</h3>
          <div className="review-table">
            <table>
              <thead>
                <tr>
                  <th>Name</th>
                  <th>Code</th>
                </tr>
              </thead>
              <tbody>
                {data.departments.map(d => (
                  <tr key={d.id}>
                    <td>{d.name}</td>
                    <td><span className="badge">{d.code}</span></td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        <div className="review-section">
          <h3>Subjects ({data.subjects.length})</h3>
          <div className="review-table">
            <table>
              <thead>
                <tr>
                  <th>Name</th>
                  <th>Code</th>
                  <th>Hours/Week</th>
                  <th>Type</th>
                </tr>
              </thead>
              <tbody>
                {data.subjects.map(s => (
                  <tr key={s.id}>
                    <td>{s.name}</td>
                    <td><span className="badge">{s.code}</span></td>
                    <td>{s.hours_per_week}</td>
                    <td>{s.is_lab ? <span className="badge lab">LAB</span> : <span className="badge">THEORY</span>}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        <div className="review-section">
          <h3>Rooms ({data.rooms.length})</h3>
          <div className="review-table">
            <table>
              <thead>
                <tr>
                  <th>Room No.</th>
                  <th>Floor</th>
                  <th>Capacity</th>
                  <th>Benches</th>
                  <th>Type</th>
                </tr>
              </thead>
              <tbody>
                {data.rooms.map(r => (
                  <tr key={r.id}>
                    <td><strong>{r.room_number}</strong></td>
                    <td>{r.floor}</td>
                    <td>{r.capacity}</td>
                    <td>{r.bench_count}</td>
                    <td>{r.is_lab ? <span className="badge lab">LAB</span> : <span className="badge">CLASSROOM</span>}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        <div className="review-section">
          <h3>Faculty ({data.faculty.length})</h3>
          <div className="review-table">
            <table>
              <thead>
                <tr>
                  <th>Name</th>
                  <th>Employee ID</th>
                </tr>
              </thead>
              <tbody>
                {data.faculty.map(f => (
                  <tr key={f.id}>
                    <td>{f.name}</td>
                    <td><span className="badge">{f.employee_id}</span></td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        <div className="review-section">
          <h3>Divisions ({data.divisions.length})</h3>
          <div className="review-table">
            <table>
              <thead>
                <tr>
                  <th>Name</th>
                  <th>Year</th>
                  <th>Students</th>
                </tr>
              </thead>
              <tbody>
                {data.divisions.map(d => (
                  <tr key={d.id}>
                    <td><strong>{d.name}</strong></td>
                    <td>{d.year}</td>
                    <td>{d.student_count}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <div className="verification-box">
        <label className="checkbox-label">
          <input 
            type="checkbox" 
            checked={confirmed}
            onChange={(e) => setConfirmed(e.target.checked)}
          />
          <span>I confirm that all the above data is correct and complete</span>
        </label>
      </div>

      <div className="action-bar">
        <button className="btn-secondary" onClick={onBack}>
          Back to Edit
        </button>
        <button 
          className="btn-primary" 
          onClick={handleGenerate}
          disabled={!confirmed || loading}
        >
          {loading ? 'Generating...' : 'Generate Timetable'}
        </button>
      </div>
    </div>
  )
}

export default ReviewData
