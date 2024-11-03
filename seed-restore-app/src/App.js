import React, { useState } from 'react';
import Layout from './components/Layout';
import ChatBox from './components/ChatBox';
import './App.css'; // Add any global styles here
import './img/sun-thing.png'; // Add styles for chat box
import CloudsAndSun from './components/CloudsAndSun';
import Grass from './components/Grass';
import Chatbot from './components/Chatbot';

function App() {
  const [isFirstMessageSent, setIsFirstMessageSent] = useState(false);
  const handleFirstMessage = () => {
    setIsFirstMessageSent(true);
  };

  return (
    // Sun and clouds
      <Chatbot />
  );
}

export default App;