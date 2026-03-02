function TimetableView({ data, loading, onStartOver }) {
  if (loading) {
    return (
      <div className="loading-container">
        <div className="spinner"></div>
        <h3>Generating Timetable...</h3>
        <p>AI agents are working to create an optimal schedule</p>
        <div className="agent-status">
          <div className="agent-step">Resource Allocation Agent - Matching rooms...</div>
          <div className="agent-step">Optimization Agent - Running solver...</div>
          <div className="agent-step">Constraint Agent - Validating rules...</div>
        </div>
      </div>
    )
  }

  if (!data) return null

  const { status, timetable, constraints, utilization, message_log } = data

  const handleExport = () => {
    const csvContent = timetable.map(entry => 
      `${entry.division_id},${entry.subject_id},${entry.room_id},${entry.faculty_id},${entry.timeslot_id}`
    ).join('\n')
    
    const blob = new Blob([csvContent], { type: 'text/csv' })
    const url = window.URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = 'timetable.csv'
    a.click()
  }

  const handleApprove = () => {
    if (confirm('Are you sure you want to approve this timetable? This will finalize the schedule.')) {
      alert('Timetable approved successfully!')
    }
  }

  return (
    <div className="timetable-container">
      <div className="result-header">
        <h2>Step 3: Generated Timetable</h2>
        <div className={`status-badge ${status}`}>
          {status === 'success' && 'SUCCESS'}
          {status === 'conflicts_detected' && 'CONFLICTS DETECTED'}
          {status === 'failed' && 'GENERATION FAILED'}
        </div>
      </div>

      {status === 'success' && (
        <>
          <div className="metrics-grid">
            <div className="metric-card">
              <div className="metric-value">{utilization?.total_classes || 0}</div>
              <div className="metric-label">Total Classes Scheduled</div>
            </div>
            <div className="metric-card">
              <div className="metric-value">{((utilization?.slot_utilization || 0) * 100).toFixed(1)}%</div>
              <div className="metric-label">Slot Utilization</div>
            </div>
            <div className="metric-card">
              <div className="metric-value">{constraints?.filter(c => !c.violated).length || 0}</div>
              <div className="metric-label">Constraints Satisfied</div>
            </div>
            <div className="metric-card">
              <div className="metric-value">{constraints?.filter(c => c.violated).length || 0}</div>
              <div className="metric-label">Violations</div>
            </div>
          </div>

          <div className="timetable-section">
            <div className="section-header">
              <h3>Generated Schedule</h3>
              <div className="action-buttons">
                <button className="btn-secondary" onClick={handleExport}>Export CSV</button>
                <button className="btn-success" onClick={handleApprove}>Approve Timetable</button>
              </div>
            </div>
            <div className="table-container">
              <table className="timetable-table">
                <thead>
                  <tr>
                    <th>Division ID</th>
                    <th>Subject ID</th>
                    <th>Room ID</th>
                    <th>Faculty ID</th>
                    <th>Timeslot ID</th>
                  </tr>
                </thead>
                <tbody>
                  {timetable && timetable.map((entry, idx) => (
                    <tr key={idx}>
                      <td>{entry.division_id}</td>
                      <td>{entry.subject_id}</td>
                      <td>{entry.room_id}</td>
                      <td>{entry.faculty_id}</td>
                      <td>{entry.timeslot_id}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </>
      )}

      {constraints && constraints.length > 0 && (
        <div className="constraints-section">
          <h3>Constraint Validation Report</h3>
          <div className="constraints-grid">
            {constraints.map((c, idx) => (
              <div key={idx} className={`constraint-card ${c.violated ? 'violated' : 'satisfied'}`}>
                <div className="constraint-header">
                  <strong>{c.type.replace('_', ' ').toUpperCase()}</strong>
                  <span className={`status-icon ${c.violated ? 'error' : 'success'}`}>
                    {c.violated ? '✗' : '✓'}
                  </span>
                </div>
                <div className="constraint-details">{c.details}</div>
              </div>
            ))}
          </div>
        </div>
      )}

      {message_log && message_log.length > 0 && (
        <div className="agent-log-section">
          <h3>Agent Communication Log</h3>
          <p className="section-description">Real-time collaboration between AI agents</p>
          <div className="log-container">
            {message_log.map((msg, idx) => (
              <div key={idx} className="log-entry">
                <span className="log-sender">{msg.sender}</span>
                <span className="log-arrow">→</span>
                <span className="log-receiver">{msg.receiver}</span>
                <span className="log-message">{msg.message}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {status === 'failed' && (
        <div className="error-section">
          <h3>Generation Failed</h3>
          <p>Unable to generate a feasible timetable with the provided constraints.</p>
          <p>Please review your data and try again.</p>
        </div>
      )}

      <div className="action-bar">
        <button className="btn-secondary" onClick={onStartOver}>
          Start Over
        </button>
      </div>
    </div>
  )
}

export default TimetableView
