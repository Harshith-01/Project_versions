const API_BASE = '/api'

export async function ingestUrl(url, disease) {
  const res = await fetch(`${API_BASE}/ingest-url`, {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({url, disease})
  })
  return res.json()
}

export async function uploadCsvFile(file) {
  const form = new FormData()
  form.append('file', file)
  const res = await fetch(`${API_BASE}/upload-csv`, { method: 'POST', body: form })
  return res.json()
}

export async function downloadCsv() {
  const res = await fetch(`${API_BASE}/download-csv`)
  return res.json()
}

export async function getColumns() {
  const res = await fetch(`${API_BASE}/columns`)
  return res.json()
}
