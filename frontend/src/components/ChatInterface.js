import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import './ChatInterface.css';

const API_BASE_URL = 'http://localhost:8000/api/v1';

function ChatInterface() {
  const [messages, setMessages] = useState([
    {
      type: 'bot',
      text: 'Hello! I\'m an AI assistant with real-time content moderation. How can I help you today?',
      timestamp: new Date()
    }
  ]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [region, setRegion] = useState('global');
  const [sessionId] = useState(() => `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async (e) => {
    e.preventDefault();

    if (!inputMessage.trim() || isLoading) {
      return;
    }

    const userMessage = inputMessage.trim();
    setInputMessage('');

    // Add user message to chat
    const newUserMessage = {
      type: 'user',
      text: userMessage,
      timestamp: new Date()
    };
    setMessages(prev => [...prev, newUserMessage]);

    setIsLoading(true);

    try {
      const response = await axios.post(`${API_BASE_URL}/chat`, {
        message: userMessage,
        region: region,
        session_id: sessionId
      });

      const botMessage = {
        type: 'bot',
        text: response.data.response,
        timestamp: new Date(),
        isModerated: response.data.is_moderated,
        moderationInfo: response.data.moderation_info
      };

      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      console.error('Error sending message:', error);
      const errorMessage = {
        type: 'bot',
        text: 'Sorry, I encountered an error. Please try again.',
        timestamp: new Date(),
        isError: true
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const formatTime = (date) => {
    return date.toLocaleTimeString('en-US', {
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  return (
    <div className="chat-interface">
      <div className="chat-header">
        <div className="chat-info">
          <h2>Chat Session</h2>
          <span className="session-id">Session: {sessionId.substring(0, 20)}...</span>
        </div>
        <div className="region-selector">
          <label htmlFor="region">Region:</label>
          <select
            id="region"
            value={region}
            onChange={(e) => setRegion(e.target.value)}
          >
            <option value="global">Global</option>
            <option value="us">United States (HIPAA)</option>
            <option value="eu">European Union (GDPR)</option>
            <option value="uk">United Kingdom</option>
            <option value="apac">Asia Pacific</option>
          </select>
        </div>
      </div>

      <div className="messages-container">
        {messages.map((message, index) => (
          <div key={index} className={`message ${message.type}`}>
            <div className="message-content">
              <p>{message.text}</p>
              {message.isModerated && (
                <div className="moderation-badge">
                  <span className="badge-icon">🛡️</span>
                  <span>Moderated</span>
                  {message.moderationInfo && (
                    <div className="moderation-details">
                      {message.moderationInfo.blocked && (
                        <span className="blocked">Content Blocked</span>
                      )}
                      <span>Latency: {message.moderationInfo.latency_ms?.toFixed(2)}ms</span>
                      <span>Rules: {message.moderationInfo.rules_triggered}</span>
                    </div>
                  )}
                </div>
              )}
            </div>
            <span className="message-time">{formatTime(message.timestamp)}</span>
          </div>
        ))}
        {isLoading && (
          <div className="message bot loading">
            <div className="message-content">
              <div className="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <form className="message-input-container" onSubmit={handleSendMessage}>
        <input
          type="text"
          value={inputMessage}
          onChange={(e) => setInputMessage(e.target.value)}
          placeholder="Type your message..."
          disabled={isLoading}
          className="message-input"
        />
        <button
          type="submit"
          disabled={isLoading || !inputMessage.trim()}
          className="send-button"
        >
          Send
        </button>
      </form>
    </div>
  );
}

export default ChatInterface;
