import React, { useState, useEffect, useRef } from 'react';
import './App.css';
import ChatInterface from './components/ChatInterface';
import AdminPanel from './components/AdminPanel';

function App() {
  const [view, setView] = useState('chat'); // 'chat' or 'admin'

  return (
    <div className="App">
      <header className="App-header">
        <h1>AI Chatbot with Real-Time Moderation</h1>
        <div className="view-toggle">
          <button
            className={view === 'chat' ? 'active' : ''}
            onClick={() => setView('chat')}
          >
            Chat
          </button>
          <button
            className={view === 'admin' ? 'active' : ''}
            onClick={() => setView('admin')}
          >
            Admin Panel
          </button>
        </div>
      </header>

      <main className="App-main">
        {view === 'chat' ? <ChatInterface /> : <AdminPanel />}
      </main>

      <footer className="App-footer">
        <p>Real-Time Moderation and Compliance Engine | Powered by FastAPI & React</p>
      </footer>
    </div>
  );
}

export default App;
