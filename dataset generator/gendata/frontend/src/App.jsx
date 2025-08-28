import React, { useState, useEffect } from 'react'
import { ingestUrl, uploadCsvFile, downloadCsv, getColumns } from './api'

export default function App(){
  const [url, setUrl] = useState('')
  const [disease, setDisease] = useState('')
  const [busy, setBusy] = useState(false)
  const [preview, setPreview] = useState([])
  const [message, setMessage] = useState('')
  const [columns, setColumns] = useState([])

  useEffect(()=>{ loadColumns() }, [])
  async function loadColumns(){
    try{ const data = await getColumns(); setColumns(data.columns || []) }catch(e){console.warn(e)}
  }

  async function handleIngest(){
    if(!url||!disease) return setMessage('Provide disease name and URL')
    setBusy(true); setMessage('')
    try{
      const data = await ingestUrl(url, disease)
      setPreview(data.preview || [])
      setMessage(`Added ${data.added} rows. Total rows: ${data.total_rows || 'unknown'}`)
    }catch(e){ setMessage('Error: '+String(e)) }
    setBusy(false)
  }

  async function handleUpload(ev){
    const file = ev.target.files?.[0]
    if(!file) return
    setBusy(true); setMessage('')
    try{
      const data = await uploadCsvFile(file)
      setMessage(`Merged ${data.merged_rows} rows. Total: ${data.total_rows}`)
    }catch(e){ setMessage('Error: '+String(e)) }
    setBusy(false)
  }

  async function handleDownload(){
    const data = await downloadCsv()
    if(data.content){
      const blob = new Blob([data.content], {type:'text/csv'})
      const u = URL.createObjectURL(blob)
      const a = document.createElement('a'); a.href=u; a.download=data.filename||'dataset.csv'; a.click(); URL.revokeObjectURL(u)
    }
  }

  return (
    <div className="container">
      <h1>Disease Dataset Builder</h1>
      <p className="small-muted">Ingest trusted medical URLs to auto-generate multiple probabilistic symptom rows per disease.</p>

      <div style={{display:'grid', gap:10}}>
        <input placeholder="Disease name (e.g., Dengue)" value={disease} onChange={e=>setDisease(e.target.value)} />
        <input placeholder="Trusted medical URL" value={url} onChange={e=>setUrl(e.target.value)} />
        <div style={{display:'flex', gap:8}}>
          <button onClick={handleIngest} disabled={busy} style={{padding:'10px 14px'}}> {busy? 'Working…' : 'Ingest URL and Append Rows'} </button>
          <button onClick={handleDownload} style={{padding:'10px 14px'}}>Download CSV</button>
          <label style={{padding:'10px 14px', border:'1px solid #eee', cursor:'pointer'}}>Upload CSV
            <input type="file" accept=".csv" onChange={handleUpload} style={{display:'none'}} />
          </label>
        </div>

        {message && <div style={{padding:10, background:'#f5f8ff', borderRadius:8}}>{message}</div>}

        {preview.length>0 && (
          <div>
            <h3>Preview (rows added)</h3>
            <div className="preview-wrap">
              <table className="table-preview">
                <thead>
                  <tr>{Object.keys(preview[0]).map(k=> <th key={k}>{k}</th>)}</tr>
                </thead>
                <tbody>
                  {preview.map((row,i)=> (
                    <tr key={i}>{Object.keys(preview[0]).map(k=> <td key={k}>{String(row[k] ?? '')}</td>)}</tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

      </div>
    </div>
  )
}
