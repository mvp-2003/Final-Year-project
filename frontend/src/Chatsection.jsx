import { useState, useRef } from 'react';
import './Chatsection.css'
import axios from 'axios';
import ChatBubbleUser from './ChatBubbleUser.jsx';
import ChatBubbleBot from './ChatBubbleBot.jsx';

function ChatSection() {
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState('');
    const inputRef = useRef(null);

    const handleSubmit = async () => {
        if (input.trim()) {
            const userMessage = { id: Date.now(), sender: 'user', text: input };
            setMessages([...messages, userMessage]);

            try {
                const response = await axios.post('/api/chat', { message: input });
                const botMessage = { id: Date.now() + 1, sender: 'bot', text: response.data.response };
                setMessages((prevMessages) => [...prevMessages, botMessage]);
            } catch (error) {
                console.error('Error sending message:', error);
            }

            setInput('');
        }
    };

    const handleKeyDown = (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSubmit();
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
                        <ChatBubbleBot 
                            key={msg.id} 
                            text={msg.text} 
                        />
                    )
                ))}
            </div>
            <textarea
                ref={inputRef}
                className="user-input"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={handleKeyDown}
                placeholder="Type your message..."
                rows={1}
                style={{ resize: 'none', overflowY: 'auto' }}
            />
            <button className="submit-prompt" onClick={handleSubmit}></button>
        </div>
    );
}

export default ChatSection