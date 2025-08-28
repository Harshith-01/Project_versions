// /frontend/src/App.js
import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import { v4 as uuidv4 } from 'uuid';
import './App.css';

const API_URL = 'http://localhost:5000/diagnose';

function App() {
  const [sessionId, setSessionId] = useState('');
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [quantumMode, setQuantumMode] = useState(true);
  const [symptomHistory, setSymptomHistory] = useState([]);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    setSessionId(uuidv4());
    setMessages([{ 
      sender: 'ai', 
      text: 'Welcome! Please describe your symptoms. This tool is for informational purposes only and is not a substitute for professional medical advice.' 
    }]);
  }, []);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSendMessage = async (text, isFollowUp = false) => {
    const userMessage = text.trim();
    if (!userMessage) return;

    setMessages(prev => [...prev, { sender: 'user', text: userMessage }]);
    setInput('');
    setIsLoading(true);

    // Update symptom history based on user's response
    let updatedHistory = [...symptomHistory];
    if (isFollowUp) {
      const lastQuestion = messages.find(m => m.sender === 'ai' && m.isFollowUp)?.text;
      if(lastQuestion) {
        if (userMessage.toLowerCase() === 'yes') {
            updatedHistory.push({ type: 'present', symptoms: [lastQuestion]});
        } else {
            updatedHistory.push({ type: 'absent', symptoms: [lastQuestion]});
        }
      }
    }
    setSymptomHistory(updatedHistory);

    try {
      const response = await axios.post(API_URL, {
        session_id: sessionId,
        free_text: userMessage,
        quantum_mode: quantumMode,
        symptom_history: updatedHistory,
      });

      const aiResponse = response.data;
      let aiMessages = [];

      if (aiResponse.error) {
        aiMessages.push({ sender: 'ai', text: `An error occurred: ${aiResponse.error}` });
      } else {
        if (aiResponse.diagnoses && aiResponse.diagnoses.length > 0) {
          const diagnosesText = aiResponse.diagnoses
            .map(d => `${d.name} (${(d.prob * 100).toFixed(1)}%)`)
            .join(', ');
          aiMessages.push({ sender: 'ai', text: `Possible conditions: ${diagnosesText}` });
        }
        if (aiResponse.red_flags && aiResponse.red_flags.length > 0) {
          aiMessages.push({ sender: 'ai', text: `🚨 Red Flags Identified: ${aiResponse.red_flags.join(', ')}. Please consider seeking medical attention.` });
        }
        if (aiResponse.citations && aiResponse.citations.length > 0) {
          const citationText = aiResponse.citations.map(c => `${c.disease} (${c.id})`).join('; ');
          aiMessages.push({ sender: 'ai', text: `Citations: ${citationText}` });
        }

        if (!aiResponse.final_diagnosis && aiResponse.follow_up_question) {
          aiMessages.push({ sender: 'ai', text: aiResponse.follow_up_question, isFollowUp: true });
        } else {
          aiMessages.push({ sender: 'ai', text: "This concludes the preliminary analysis. Please consult a healthcare professional for an accurate diagnosis." });
        }
      }
      setMessages(prev => [...prev, ...aiMessages]);

    } catch (error) {
      console.error("API call failed:", error);
      setMessages(prev => [...prev, { sender: 'ai', text: 'Sorry, I am having trouble connecting to the server.' }]);
    } finally {
      setIsLoading(false);
    }
  };

  const lastMessageIsFollowUp = messages[messages.length - 1]?.isFollowUp;

  return (
    <div className="bg-gray-900 text-white min-h-screen flex flex-col items-center p-4 font-sans">
      <div className="w-full max-w-3xl flex flex-col h-[95vh] bg-gray-800 rounded-lg shadow-xl">
        <header className="p-4 border-b border-gray-700 flex justify-between items-center">
          <h1 className="text-xl font-bold">AI Medical Diagnosis Assistant</h1>
          <div className="flex items-center space-x-2">
            <label htmlFor="quantum-toggle" className="text-sm">Quantum Clarifier</label>
            <button
              id="quantum-toggle"
              onClick={() => setQuantumMode(!quantumMode)}
              className={`relative inline-flex items-center h-6 rounded-full w-11 transition-colors ${quantumMode ? 'bg-purple-600' : 'bg-gray-600'}`}
            >
              <span className={`inline-block w-4 h-4 transform bg-white rounded-full transition-transform ${quantumMode ? 'translate-x-6' : 'translate-x-1'}`} />
            </button>
          </div>
        </header>

        <main className="flex-1 p-4 overflow-y-auto">
          <div className="space-y-4">
            {messages.map((msg, index) => (
              <div key={index} className={`flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}>
                <div className={`max-w-md p-3 rounded-lg ${msg.sender === 'user' ? 'bg-blue-600' : 'bg-gray-700'}`}>
                  <p>{msg.text}</p>
                </div>
              </div>
            ))}
            {isLoading && (
              <div className="flex justify-start">
                <div className="max-w-md p-3 rounded-lg bg-gray-700">
                  <div className="animate-pulse">Thinking...</div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>
        </main>

        <footer className="p-4 border-t border-gray-700">
          {lastMessageIsFollowUp ? (
            <div className="flex justify-center space-x-4">
              <button onClick={() => handleSendMessage('Yes', true)} className="px-6 py-2 bg-green-600 rounded-lg hover:bg-green-700 transition">Yes</button>
              <button onClick={() => handleSendMessage('No', true)} className="px-6 py-2 bg-red-600 rounded-lg hover:bg-red-700 transition">No</button>
            </div>
          ) : (
            <form onSubmit={(e) => { e.preventDefault(); handleSendMessage(input); }} className="flex space-x-2">
              <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder="Type your symptoms here..."
                className="flex-1 p-2 bg-gray-700 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
                disabled={isLoading}
              />
              <button type="submit" className="px-4 py-2 bg-purple-600 rounded-lg hover:bg-purple-700 disabled:bg-gray-500 transition" disabled={isLoading}>
                Send
              </button>
            </form>
          )}
        </footer>
      </div>
    </div>
  );
}

export default App;