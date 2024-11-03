// src/Message.js
import React from 'react';
import './Message.css';

const Message = ({ message, sender }) => {
    return (
        <div className={`message ${sender}`}>
            <div className="message-bubble">{message}</div>
        </div>
    );
};

export default Message;
