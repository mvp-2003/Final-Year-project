import './ChatBubbleBot.css';
import PropTypes from 'prop-types';

function ChatBubbleBot({ text }) {
    return (
        <div className="chat-bubble-bot">
            {text}
        </div>
    );
}

ChatBubbleBot.propTypes = {
    text: PropTypes.string.isRequired,
};

export default ChatBubbleBot;