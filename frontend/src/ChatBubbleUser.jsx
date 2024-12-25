import './ChatBubbleUser.css'
import PropTypes from 'prop-types';

function ChatBubbleUser({ text }) {
    return (
        <div className="chat-bubble-user">
            {text}
        </div>
    );
}

ChatBubbleUser.propTypes = {
    text: PropTypes.string.isRequired,
};

export default ChatBubbleUser;