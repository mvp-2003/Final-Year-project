import { useState, useEffect } from 'react';
import './Chatsection.css';
import axios from 'axios';
import ChatBubbleUser from './ChatBubbleUser.jsx';
import ChatBubbleBot from './ChatBubbleBot.jsx';

function ChatSection() {
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState('');
    const [sessionId] = useState(Date.now().toString());

    useEffect(() => {
        const getInitialGreeting = async () => {
            try {
                const response = await axios.post('/api/chat', { 
                    message: "Hi",
                    session_id: sessionId
                });
                const botMessage = { id: Date.now(), sender: 'bot', text: response.data.response.text, imageUrl: response.data.response.image_url };
                setMessages([botMessage]);
            } catch (error) {
                console.error('Error getting initial greeting:', error);
            }
        };

        getInitialGreeting();
    }, [sessionId]);

    const handleSubmit = async () => {
        if (input.trim()) {
            const userMessage = { id: Date.now(), sender: 'user', text: input };
            setMessages([...messages, userMessage]);

            try {
                const response = await axios.post('/api/chat', { 
                    message: input,
                    session_id: sessionId
                });
                const botMessage = { 
                    id: Date.now() + 1, 
                    sender: 'bot', 
                    text: response.data.response.text, 
                    imageUrl: response.data.response.image_url
                };
                setMessages((prevMessages) => [...prevMessages, botMessage]);
            } catch (error) {
                console.error('Error sending message:', error);
            }

            setInput('');
        }
    };

    return (
        <div className="background-space">
            <div className="chat-messages">
                {messages.map((msg) => (
                    msg.sender === 'user' ? (
                        <ChatBubbleUser 
                            key={msg.id} 
                            text={msg.text} 
                        />
                    ) : (
                        <div key={msg.id}>
                            <ChatBubbleBot 
                                text={msg.text} 
                            />
                            {msg.imageUrl && <img src={msg.imageUrl} alt="Generated" />}
                        </div>
                    )
                ))}
            </div>
            <div className="input-container">
                <input
                    placeholder="Enter your message..."
                    type="text"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    onKeyDown={(e) => e.key === 'Enter' && handleSubmit()}
                />
            </div>
            <button className="submit-prompt" onClick={handleSubmit}></button>
        </div>
    );
}

export default ChatSection;