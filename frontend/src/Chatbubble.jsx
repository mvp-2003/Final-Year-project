import './Chatbubble.css'
import PropTypes from 'prop-types';

function Chatbubble({ sender, text }) {
    return (
        <div className={`chat-bubble ${sender}`}>
            {text}
        </div>
    );
}

Chatbubble.propTypes = {
    sender: PropTypes.string.isRequired,
    text: PropTypes.string.isRequired,
};

export default Chatbubble
