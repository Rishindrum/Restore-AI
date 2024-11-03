// src/Chat.js
import React, { useState } from 'react';
import Message from './Message';
import './Chat.css';
// At the top of Chat.js
import '@fortawesome/fontawesome-free/css/all.min.css';


const Chat = () => {
    const [messages, setMessages] = useState([
        { sender: 'bot', message: "Hello! I'm Sycamore.AI, and my mission is to revive the Blackland Prairie and bring it back to its former glory. Once the heart of Texas, this iconic ecosystem is now critically endangered due to relentless development and overgrazing. Recent restoration efforts are helping but they are not efficient enough. If we don't act now, these precious lands will be gone within a generation." },
        { sender: 'bot', message: "My purpose is to optimize restoration efforts, helping every seed fulfill its potential. By identifying the optimal planting season—whether the warmth of spring for vibrant growth or the chill of fall for crucial cold-stratification—I ensure that each seed revitalizes the land underneath. Share your terrain details with me, and let’s restore the Blackland Prairie to its rightful glory!" }
    ]);
    const [input, setInput] = useState('');

    const sendMessage = () => {
        if (input.trim()) {
            const newMessages = [...messages, { sender: 'user', message: input }];
            setMessages(newMessages);
            setInput('');

            // Add a dummy bot response
            setTimeout(() => {
                setMessages(prevMessages => [
                    ...prevMessages,
                    { sender: 'bot', message: "This is a static response from the bot." }
                ]);
            }, 500);
        }
    };

    const handleKeyPress = (e) => {
        if (e.key === 'Enter') {
            sendMessage();
        }
    };

    return (
        <div className="chat-container">
            <div className="chat-header">Sycamore.AI</div>
            <div className="messages-container">
                {messages.map((msg, index) => (
                    <Message key={index} message={msg.message} sender={msg.sender} />
                ))}
            </div>
            <div className="input-container">
                <textarea
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    onKeyPress={handleKeyPress}
                    placeholder="Type your message..."
                    rows="1"
                    className="expandable-textarea"
                />
                <button onClick={sendMessage}>
                    <i className="fas fa-paper-plane"></i>
                </button>
            </div>
        </div>
    );
};

export default Chat;
