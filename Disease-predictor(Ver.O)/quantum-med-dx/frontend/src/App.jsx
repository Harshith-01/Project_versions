import React, { useState } from 'react'

const API_BASE = 'http://localhost:8000'

export default function App() {
  const [freeText, setFreeText] = useState("")
  const [checkbox, setCheckbox] = useState({ fever:false, headache:false, cough:false, rash:false })
  const [quantumMode, setQuantumMode] = useState(false)
  const [loading, setLoading] = useState(false)
  const [response, setResponse] = useState(null)
  const [followup, setFollowup] = useState(null)
  const [answer, setAnswer] = useState("yes")
  const [sessionId] = useState(() => crypto.randomUUID())

  const submit = async () => {
    setLoading(true)
    setResponse(null)
    setFollowup(null)
    const checkbox_symptoms = Object.keys(checkbox).filter(k => checkbox[k])
    const payload = { session_id: sessionId, free_text: freeText, checkbox_symptoms, quantum_mode: quantumMode }
    const res = await fetch(`${API_BASE}/diagnose`, {
      method: 'POST',
      headers: { 'Content-Type':'application/json' },
      body: JSON.stringify(payload)
    })
    const data = await res.json()
    setLoading(false)
    if (data.status === 'clarify') setFollowup(data)
    else setResponse(data)
  }

  const sendClarify = async () => {
    if (!followup) return
    setLoading(true)
    const payload = {
      session_id: sessionId,
      answer,
      chosen_question: followup.question,
      quantum_mode: quantumMode,
      previous_trace_id: followup.trace_id
    }
    const res = await fetch(`${API_BASE}/clarify`, {
      method: 'POST',
      headers: { 'Content-Type':'application/json' },
      body: JSON.stringify(payload)
    })
    const data = await res.json()
    setLoading(false)
    setFollowup(null)
    setResponse(data)
  }

  return (
    <div className="max-w-3xl mx-auto p-6">
      <h1 className="text-2xl font-bold mb-4">Quantum-Enhanced Medical Diagnosis (Demo)</h1>
      <p className="text-sm text-gray-600 mb-6">Not a medical device. For educational purposes only.</p>

      <div className="bg-white rounded-xl shadow p-4 mb-4">
        <label className="block font-medium mb-2">Describe your symptoms</label>
        <textarea
          className="w-full border rounded p-2"
          rows={4}
          value={freeText}
          onChange={e=>setFreeText(e.target.value)}
          placeholder="e.g., fever for 3 days, no cough, mild headache"
        />
        <div className="mt-4">
          <label className="block font-medium mb-2">Or select common symptoms</label>
          <div className="flex gap-4">
            {Object.keys(checkbox).map(k => (
              <label key={k} className="flex items-center gap-2">
                <input type="checkbox" checked={checkbox[k]} onChange={()=>setCheckbox({...checkbox, [k]:!checkbox[k]})}/>
                <span className="capitalize">{k}</span>
              </label>
            ))}
          </div>
        </div>
        <div className="mt-4 flex items-center gap-2">
          <input type="checkbox" id="qm" checked={quantumMode} onChange={()=>setQuantumMode(!quantumMode)} />
          <label htmlFor="qm">Use Quantum Randomness for follow-up</label>
        </div>
        <button
          onClick={submit}
          className="mt-4 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
          disabled={loading}
        >
          {loading ? "Working..." : "Diagnose"}
        </button>
      </div>

      {followup && (
        <div className="bg-white rounded-xl shadow p-4 mb-4">
          <h2 className="font-semibold">Clarifying question</h2>
          <p className="mt-2">{followup.question}</p>
          <div className="mt-3 flex gap-3">
            {["yes","no","unsure"].map(a=>(
              <label key={a} className="flex items-center gap-2">
                <input type="radio" name="ans" checked={answer===a} onChange={()=>setAnswer(a)} />
                <span className="capitalize">{a}</span>
              </label>
            ))}
          </div>
          <button onClick={sendClarify} className="mt-3 px-4 py-2 bg-emerald-600 text-white rounded">Submit</button>
          <div className="mt-3">
            <h3 className="font-medium">Citations:</h3>
            <ul className="list-disc ml-6">
              {followup.citations?.map(c=>(
                <li key={c.ctx_id}><span className="text-sm">{c.ctx_id}</span> – <a className="text-blue-700 underline" href={c.url} target="_blank">{c.section}</a></li>
              ))}
            </ul>
          </div>
        </div>
      )}

      {response && (
        <div className="bg-white rounded-xl shadow p-4">
          <h2 className="font-semibold mb-2">Results</h2>
          <p className="text-sm text-gray-600 mb-3">{response.disclaimer}</p>
          <ol className="list-decimal ml-6">
            {response.top_diagnoses?.map((d,i)=>(
              <li key={i} className="mb-1">{d.name} — {(d.prob*100).toFixed(1)}%</li>
            ))}
          </ol>
          {response.recommended_tests?.length>0 && (
            <>
              <h3 className="font-medium mt-3">Recommended tests</h3>
              <ul className="list-disc ml-6">
                {response.recommended_tests.map((t,i)=><li key={i}>{t}</li>)}
              </ul>
            </>
          )}
          {response.red_flags?.length>0 && (
            <>
              <h3 className="font-medium mt-3 text-red-700">Red flags</h3>
              <ul className="list-disc ml-6 text-red-700">
                {response.red_flags.map((t,i)=><li key={i}>{t}</li>)}
              </ul>
            </>
          )}
          <h3 className="font-medium mt-3">Citations</h3>
          <ul className="list-disc ml-6">
            {response.citations?.map(c=>(
              <li key={c.ctx_id}><span className="text-sm">{c.ctx_id}</span> – <a className="text-blue-700 underline" href={c.url} target="_blank">{c.section}</a></li>
            ))}
          </ul>
          <p className="mt-3 text-sm">Quantum mode: <b>{String(response.quantum_mode)}</b></p>
        </div>
      )}
    </div>
  )
}
