import { useState } from 'react';
import './Chatsection.css'
import User from './User.jsx'
import axios from 'axios';
import Chatbubble from './Chatbubble.jsx';

function ChatSection(){
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState('');

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
        }
    };

    return(
        <div className="background-space">
            <User/>
            <div className="chat-messages">
                {messages.map((msg) => (
                    <Chatbubble key={msg.id} sender={msg.sender} text={msg.text} />
                ))}
            </div>
            <input
                className="user-input"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder="Type your message..."
            />
            <button className="submit-prompt" onClick={handleSubmit}>Send</button>
        </div>
    );
}

export default ChatSection