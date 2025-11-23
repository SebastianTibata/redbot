async function fetchLogs() {
  const token = localStorage.getItem('token');
  const res = await fetch('/api/logs', {
    headers: { 'Authorization': `Bearer ${token}` }
  });
  const logs = await res.json();
  const container = document.getElementById('logs');
  container.innerHTML = logs.map(log => `<div>${log.timestamp}: ${log.message}</div>`).join('');
}
fetchLogs();
