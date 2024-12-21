import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import ChatSection from './Chatsection.jsx'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <ChatSection />
  </StrictMode>
)