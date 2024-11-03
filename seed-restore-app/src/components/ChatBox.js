import React, { useState } from 'react';
import ScrollableFeed from 'react-scrollable-feed';
import './ChatBox.css';

const ChatBox = ({ onFirstMessage }) => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isFirstMessageSent, setIsFirstMessageSent] = useState(false);

  const handleSendMessage = () => {
    if (input.trim()) {
      setMessages([...messages, input]);
      setInput('');
      if (!isFirstMessageSent) {
        setIsFirstMessageSent(true);
        onFirstMessage(); // Notify parent component
      }
    }
  };

  return (
    <div className="chat-box-container">
      {/* Chat Messages */}
      <ScrollableFeed className="message-list">
        {messages.map((msg, idx) => (
          <div key={idx} className="message">{msg}</div>
        ))}
      </ScrollableFeed>

      {/* Input Bar */}
      <div className="input-container">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type your message..."
          className="chat-input"
        />
        <button onClick={handleSendMessage} className="send-button">Send</button>
      </div>
    </div>
  );
};

export default ChatBox;