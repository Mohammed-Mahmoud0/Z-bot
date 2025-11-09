import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import './ChatBot.css';

function ChatBot() {
  const [messages, setMessages] = useState([
    { role: 'bot', content: 'Hello! I\'m your AI assistant. How can I help you today? You can also attach images and ask me about them!' }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [selectedImage, setSelectedImage] = useState(null);
  const [imagePreview, setImagePreview] = useState(null);
  const messagesEndRef = useRef(null);
  const fileInputRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async () => {
    if ((!input.trim() && !selectedImage) || loading) return;

    const userMessage = input.trim();
    const userImage = imagePreview;
    
    setInput('');
    setSelectedImage(null);
    setImagePreview(null);
    
    // Add user message with image if present
    setMessages(prev => [...prev, { 
      role: 'user', 
      content: userMessage || 'What is in this image?',
      image: userImage 
    }]);
    setLoading(true);

    try {
      const response = await axios.post('http://localhost:5000/api/chat', {
        message: userMessage || 'What is in this image?',
        image: selectedImage // Send base64 image
      });

      if (response.data.success) {
        setMessages(prev => [...prev, {
          role: 'bot',
          content: response.data.response
        }]);
      } else {
        setMessages(prev => [...prev, {
          role: 'bot',
          content: 'Sorry, I encountered an error. Please try again.'
        }]);
      }
    } catch (error) {
      setMessages(prev => [...prev, {
        role: 'bot',
        content: 'Sorry, I couldn\'t connect to the server. Please make sure the server is running.'
      }]);
    } finally {
      setLoading(false);
    }
  };

  const handleImageSelect = (e) => {
    const file = e.target.files[0];
    if (file && file.type.startsWith('image/')) {
      const reader = new FileReader();
      reader.onloadend = () => {
        setSelectedImage(reader.result); // base64 string
        setImagePreview(reader.result);
      };
      reader.readAsDataURL(file);
    }
  };

  const removeImage = () => {
    setSelectedImage(null);
    setImagePreview(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="chatbot-container">
      <div className="messages-container">
        {messages.map((msg, index) => (
          <div key={index} className={`message ${msg.role}`}>
            <div className="message-content">
              {msg.image && (
                <img src={msg.image} alt="Uploaded" className="message-image" />
              )}
              {msg.content}
            </div>
          </div>
        ))}
        {loading && (
          <div className="message bot">
            <div className="message-content">
              <div className="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <div className="input-container">
        {imagePreview && (
          <div className="image-preview">
            <img src={imagePreview} alt="Preview" />
            <button className="remove-image" onClick={removeImage}>×</button>
          </div>
        )}
        <div className="input-row">
          <input
            type="file"
            ref={fileInputRef}
            accept="image/*"
            onChange={handleImageSelect}
            style={{ display: 'none' }}
          />
          <button 
            className="attach-button" 
            onClick={() => fileInputRef.current?.click()}
            disabled={loading}
            title="Attach image"
          >
            📎
          </button>
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Type your message or attach an image..."
            rows="1"
            disabled={loading}
          />
          <button 
            onClick={handleSend} 
            disabled={loading || (!input.trim() && !selectedImage)}
            className="send-button"
          >
            Send
          </button>
        </div>
      </div>
    </div>
  );
}

export default ChatBot;
