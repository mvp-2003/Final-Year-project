import { useState, useRef } from 'react';
import './Chatsection.css'
import User from './User.jsx'
import axios from 'axios';
import Chatbubble from './Chatbubble.jsx';

function ChatSection(){
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState('');
    const inputRef = useRef(null);

    const handleSubmit = async () => {
        if (input.trim()) {
            const userMessage = { id: Date.now(), sender: 'user', text: input };
            setMessages([...messages, userMessage]);

            try {
                const response = await axios.post('/api/chat', { message: input });
                const botMessage = { id: Date.now() + 1, sender: 'bot', text: response.data.reply };
                setMessages((prevMessages) => [...prevMessages, botMessage]);
            } catch (error) {
                console.error('Error sending message:', error);
            }

            setInput('');
            adjustTextareaHeight();
        }
    };

    const handleKeyDown = (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSubmit();
        }
    };

    const adjustTextareaHeight = () => {
        const textarea = inputRef.current;
        textarea.style.height = 'auto';
        textarea.style.height = `${Math.min(textarea.scrollHeight, 60)}px`;
    };

    return(
        <div className="background-space">
            <User/>
            <div className="chat-messages">
                {messages.map((msg) => (
                    <Chatbubble key={msg.id} sender={msg.sender} text={msg.text} />
                ))}
            </div>
            <textarea
                ref={inputRef}
                className="user-input"
                value={input}
                onChange={(e) => {
                    setInput(e.target.value);
                    adjustTextareaHeight();
                }}
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