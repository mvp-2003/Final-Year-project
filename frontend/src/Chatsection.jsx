import './Chatsection.css'
import User from './User.jsx'


function ChatSection(){
    return(
        <div className="background-space">
            <User/>
            <input className="user-input">
            </input>
            <button className="submit-prompt"></button>
        </div>
    );
}

export default ChatSection