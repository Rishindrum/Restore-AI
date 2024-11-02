import React, { useState } from 'react';
import Layout from './components/Layout';
import ChatBox from './components/ChatBox';
import './App.css'; // Add any global styles here

function App() {
  const [isFirstMessageSent, setIsFirstMessageSent] = useState(false);

  const handleFirstMessage = () => {
    setIsFirstMessageSent(true);
  };

  return (
    <Layout>
      <div className={`app-container ${isFirstMessageSent ? 'centered-chat' : ''}`}>
        {/* Main content with chat box */}
        <div className="content">
          <h1>How can I help with your land?</h1>
        </div>

        {/* Chat Box */}
        <ChatBox onFirstMessage={handleFirstMessage} />
      </div>
    </Layout>
  );
}

export default App;