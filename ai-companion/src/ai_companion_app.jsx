import React, { useState } from 'react';

function App() {
  const [status, setStatus] = useState("Ready to chat");

  return (
    <div style={{ padding: '20px', textAlign: 'center', fontFamily: 'sans-serif' }}>
      <h1>AI Companion</h1>
      <p>Status: {status}</p>
      <button 
        onClick={() => setStatus("Connecting to Simli...")}
        style={{ padding: '10px 20px', borderRadius: '8px', backgroundColor: '#007AFF', color: 'white', border: 'none' }}
      >
        Start Session
      </button>
    </div>
  );
}

export default App;
