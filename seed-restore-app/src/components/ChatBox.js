// src/components/ChatBox.js
import React, { useState } from 'react';
import ScrollableFeed from 'react-scrollable-feed';
import './ChatBox.css';

const ChatBox = () => {
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState('');
    const [isFirstMessageSent, setIsFirstMessageSent] = useState(false);

    const handleSendMessage = () => {
        if (input.trim()) {
        setMessages([...messages, input]);
        setInput('');
        if (!isFirstMessageSent) setIsFirstMessageSent(true);
        }
    };
 
    return (
      <div className={`chat-box-container ${isFirstMessageSent ? 'shifted' : ''}`}>
      <ScrollableFeed className="message-list">
        {messages.map((msg, idx) => (
          <div key={idx} className="message">{msg}</div>
        ))}
      </ScrollableFeed>
      <input 
        type="text" 
        value={input} 
        onChange={(e) => setInput(e.target.value)} 
        placeholder="Type your message..."
      />
      <button onClick={handleSendMessage}>Send</button>
    </div>
  );
};

export default ChatBox;