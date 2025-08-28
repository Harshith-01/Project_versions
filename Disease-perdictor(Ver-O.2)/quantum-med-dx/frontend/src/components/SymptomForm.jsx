import React, { useState } from "react";
import Toggle from "./Toggle.jsx";

export default function SymptomForm({ onSubmit, loading }) {
  const [text, setText] = useState("");
  const [quantum, setQuantum] = useState(true);
  const [boxes, setBoxes] = useState([]);

  const known = [
    "fever",
    "cough",
    "headache",
    "fatigue",
    "nausea",
    "chest pain",
    "shortness of breath",
  ];

  const toggleBox = (symptom) => {
    setBoxes((prev) =>
      prev.includes(symptom)
        ? prev.filter((s) => s !== symptom)
        : [...prev, symptom]
    );
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit({ text, boxes, quantum });
  };

  return (
    <form
      onSubmit={handleSubmit}
      className="bg-white rounded-2xl shadow p-5 space-y-4"
    >
      {/* Symptom text input */}
      <textarea
        className="w-full border rounded-lg p-3 focus:ring-2 focus:ring-blue-500 outline-none"
        rows="4"
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="Describe your symptoms, duration, and negatives (e.g., 'no cough')"
      />

      {/* Predefined symptoms checkboxes */}
      <div className="flex flex-wrap gap-3">
        {known.map((symptom) => (
          <label
            key={symptom}
            className="flex items-center px-3 py-1 border rounded-full text-sm cursor-pointer select-none hover:bg-gray-100"
          >
            <input
              type="checkbox"
              className="mr-2 accent-blue-600"
              checked={boxes.includes(symptom)}
              onChange={() => toggleBox(symptom)}
            />
            {symptom}
          </label>
        ))}
      </div>

      {/* Quantum toggle */}
      <Toggle
        checked={quantum}
        onChange={setQuantum}
        label="Use quantum randomness for follow-ups"
      />

      {/* Submit button */}
      <button
        type="submit"
        disabled={loading}
        className={`px-4 py-2 rounded-lg transition-colors ${
          loading
            ? "bg-gray-400 cursor-not-allowed"
            : "bg-black hover:bg-gray-800 text-white"
        }`}
      >
        {loading ? "Thinking..." : "Diagnose"}
      </button>
    </form>
  );
}
