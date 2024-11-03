// src/components/Chatbot.js
import React, { useState } from 'react';
import { Box, TextField, Button } from '@mui/material';
import './Chatbot.css';
import ChatBox from './ChatBox';

const Chatbot = () => {
    const [message, setMessage] = useState('');
    const [isFirstMessageSent, setIsFirstMessageSent] = useState(false);

    const handleFirstMessage = () => {
        setIsFirstMessageSent(true);
    };
    
    const handleSendMessage = () => {
        console.log("Message sent:", message);
        setMessage('');
    };

    return (
    
        <Box className={`app-container ${isFirstMessageSent ? 'centered-chat' : ''}`}>
        {/* Main content with chat box */}
        <Box className="content">
          <h1>How can I help with your land?</h1>
        </Box>
        {/* Chat Box */}
        <Box className="scrollable-text">
        <ChatBox onFirstMessage={handleFirstMessage} />
        </Box>
      </Box>
    );
};

export default Chatbot;