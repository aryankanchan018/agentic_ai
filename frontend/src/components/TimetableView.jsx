function TimetableView({ data }) {
  const { status, timetable, constraints, utilization, message_log } = data

  return (
    <div className="timetable-view">
      <h2>Timetable Generation Result</h2>
      
      <div className={`status ${status}`}>
        {status === 'success' && 'SUCCESS: Timetable Generated Successfully'}
        {status === 'conflicts_detected' && 'CONFLICTS DETECTED: Review issues below'}
        {status === 'failed' && 'FAILED: Unable to generate timetable'}
      </div>

      {status === 'success' && utilization && (
        <div className="metrics">
          <h3>Utilization Metrics</h3>
          <p>Total Classes Scheduled: <strong>{utilization.total_classes}</strong></p>
          <p>Slot Utilization: <strong>{(utilization.slot_utilization * 100).toFixed(1)}%</strong></p>
        </div>
      )}

      {timetable && timetable.length > 0 && (
        <div className="timetable-grid">
          <h3>Generated Timetable</h3>
          <table>
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
              {timetable.map((entry, idx) => (
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
      )}

      {constraints && constraints.length > 0 && (
        <div className="constraints">
          <h3>Constraint Validation Results</h3>
          {constraints.map((c, idx) => (
            <div key={idx} className={c.violated ? 'violated' : 'satisfied'}>
              <strong>{c.type.replace('_', ' ').toUpperCase()}:</strong> {c.violated ? 'Violated' : 'Satisfied'}
              <br />
              <small>{c.details}</small>
            </div>
          ))}
        </div>
      )}

      {message_log && message_log.length > 0 && (
        <div className="agent-log">
          <h3>Agent Communication Log (A2A)</h3>
          <p style={{marginBottom: '15px', color: '#666'}}>Real-time multi-agent collaboration</p>
          {message_log.map((msg, idx) => (
            <div key={idx} className="log-entry">
              <strong>{msg.sender}</strong> to <strong>{msg.receiver}</strong>: {msg.message}
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

export default TimetableView
