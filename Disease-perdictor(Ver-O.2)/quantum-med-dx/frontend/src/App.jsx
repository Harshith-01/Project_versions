import React, { useState } from "react";
import SymptomForm from "./components/SymptomForm.jsx";
import Results from "./components/Results.jsx";
import axios from "axios";

const API = "http://127.0.0.1:8000/api";

export default function App() {
  const [res, setRes] = useState(null);
  const [loading, setLoading] = useState(false);

  async function onSubmit({ text, boxes, quantum }) {
    setLoading(true);
    try {
      const { data } = await axios.post(`${API}/diagnose`, {
        free_text: text,
        checkboxes: boxes,
        quantum_mode: quantum,
      });
      setRes(data);
    } catch (e) {
      alert("API error: " + e.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="max-w-3xl mx-auto p-6 space-y-6">
      <h1 className="text-3xl font-bold">Quantum-Enhanced Triage (Demo)</h1>
      <SymptomForm onSubmit={onSubmit} loading={loading} />
      {res && <Results data={res} />}
      <p className="text-xs text-slate-500">
        Disclaimer: Educational demo. Not a medical device.
      </p>
    </div>
  );
}
