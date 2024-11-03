// src/Chat.js
import React, { useState, useRef } from 'react';
import Message from './Message';
import './Chat.css';
import { useLocation, Link } from 'react-router-dom';
import { useEffect } from 'react';
// At the top of Chat.js
import '@fortawesome/fontawesome-free/css/all.min.css';
import '@fortawesome/fontawesome-free/css/all.min.css';
import { getBotReply, sendUserMessageToDB, getFinalResult, write_to_counter, read_from_counter } from '../scripts/appwrite';


const Chat = () => {


    const location = useLocation();
    const [messages, setMessages] = useState([
        { sender: 'bot', message: "Hello! I'm RestoreAI, and my mission is to revive the Blackland Prairie and bring it back to its former glory. Once the heart of Texas, this iconic ecosystem is now critically endangered due to relentless development and overgrazing. Recent restoration efforts are helping but they are not efficient enough. If we don't act now, these precious lands will be gone within a generation." },
        { sender: 'bot', message: "My purpose is to optimize restoration efforts, helping every seed fulfill its potential. By identifying the optimal planting season—whether the warmth of spring for vibrant growth or the chill of fall for crucial cold-stratification—I ensure that each seed revitalizes the land underneath. Share your terrain details with me, and let’s restore the Blackland Prairie to its rightful glory!" },
        { sender: 'bot', message: "Please type \"yes\" to continue." }
    ]);
    const [input, setInput] = useState('');
    const [counter, setCounter] = useState(0);
    const messagesEndRef = useRef(null);

    // useEffect(() => {
    //     chatCounter = 0
    // }, []);

    useEffect(() => {
        const initializeCounter = async () => {
            const initialCounter = 0; // Replace with your async function
            setCounter(initialCounter);
        };
        initializeCounter();
    }, []); // Empty dependency array ensures this runs only once when the component mounts

    useEffect(() => {
        // Scroll to the bottom of the messages container whenever messages change
        //Ensures that the chat window is always scrolled to the bottom
        const messagesContainer = document.querySelector('.messages-container');
        if (messagesContainer) {
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
        }
    }, [messages]);

    const sendMessage = async () => {
        if (input.trim()) {
            // chatCounter = await read_from_counter();
            console.log("chatCounter at beginning", counter)
            await write_to_counter(counter);
            const newMessages = [...messages, { sender: 'user', message: input }];
            setMessages(newMessages);
            setInput('');
            if(counter !== 0){
                console.log("finally should error", counter);
                await sendUserMessageToDB(input, counter);
            }

            setCounter(prevCounter => prevCounter + 1);
            await write_to_counter(counter + 1);
            if(counter + 1 === 6){
                const finalResult = await getFinalResult();
                setMessages(prevMessages => [
                    ...prevMessages,
                    { sender: 'bot', message: finalResult}
                ]);
            }
            else{
                const botReply = await getBotReply();
                setMessages(prevMessages => [
                    ...prevMessages,
                    { sender: 'bot', message: botReply}
                ]);
            }

            console.log("chatCounter at end", counter + 1)
        }
    };

    const handleKeyPress = (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    };

    return (
        <div className="landing-page">
        <div className="chat-container">
            <div className="chat-header">
                <Link to="/">RestoreAI</Link>
            </div>
            <div className="messages-container">
                {messages.map((msg, index) => (
                    <Message key={index} message={msg.message} sender={msg.sender} />
                ))}
            </div>
            <div className="input-container">
                <div ref={messagesEndRef} />
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
        </div>
    );
};

export default Chat;
