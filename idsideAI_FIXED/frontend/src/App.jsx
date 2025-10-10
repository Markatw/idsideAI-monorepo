import React from 'react'

export default function App() {
  const apiBase = import.meta?.env?.VITE_API_BASE || 'http://127.0.0.1:8013';

  async function ping() {
    try {
      const r = await fetch(`${apiBase}/healthz`);
      const t = await r.text();
      alert(t);
    } catch (e) {
      alert(String(e));
    }
  }

  return (
    <div style={{ fontFamily: 'system-ui, sans-serif', padding: 16 }}>
      <h1>idsideAI Frontend</h1>
      <p>VITE_API_BASE = {apiBase}</p>
      <button onClick={ping}>Test /healthz</button>
    </div>
  );
}
