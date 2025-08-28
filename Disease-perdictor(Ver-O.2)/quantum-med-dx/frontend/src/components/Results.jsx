export default function Results({ data }) {
  if (data.ask_followup) {
    return (
      <div className="p-4 bg-yellow-50 border border-yellow-200 rounded-xl">
        <div className="font-semibold">Follow-up needed ({data.clarifier_mode})</div>
        <p className="mt-2">{data.ask_followup}</p>
        <p className="mt-2 text-sm text-slate-600">Answer in the text box and run again.</p>
      </div>
    );
  }
  const f = data.final || {};
  return (
    <div className="p-4 bg-green-50 border border-green-200 rounded-xl space-y-3">
      <div className="font-semibold">Differential diagnoses</div>
      <ul className="list-disc ml-5">
        {(f.differential_diagnoses || []).map((d,i)=>(
          <li key={i}>{d.name} — {(d.prob*100).toFixed(1)}%</li>
        ))}
      </ul>
      {!!(f.recommended_tests||[]).length && (
        <>
          <div className="font-semibold">Recommended next steps/tests</div>
          <ul className="list-disc ml-5">
            {f.recommended_tests.map((t,i)=>(<li key={i}>{t}</li>))}
          </ul>
        </>
      )}
      {!!(f.red_flags||[]).length && (
        <>
          <div className="font-semibold text-red-700">Red flags</div>
          <ul className="list-disc ml-5 text-red-700">
            {f.red_flags.map((t,i)=>(<li key={i}>{t}</li>))}
          </ul>
        </>
      )}
      <div className="text-xs text-slate-600">{f.disclaimer}</div>
      <div className="text-xs">
        <span className="font-semibold">Citations: </span>
        {data.citations.map((c,i)=>(
          <a key={i} href={c.url} target="_blank" className="underline mr-2" rel="noreferrer">{c.ctx_id}</a>
        ))}
      </div>
    </div>
  );
}
