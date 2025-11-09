import React, { useState } from "react";
import "./App.css";
import ChatBot from "./components/ChatBot";
import ImageGenerator from "./components/ImageGenerator";

function App() {
  const [activeTab, setActiveTab] = useState("chat");

  return (
    <div className="App">
      <header className="App-header">
        <h1>🤖 Gemini AI Assistant</h1>
        <p>Chat with AI or Generate Image Descriptions</p>
      </header>

      <div className="tab-container">
        <button
          className={`tab-button ${activeTab === "chat" ? "active" : ""}`}
          onClick={() => setActiveTab("chat")}
        >
          💬 Chat
        </button>
        <button
          className={`tab-button ${activeTab === "image" ? "active" : ""}`}
          onClick={() => setActiveTab("image")}
        >
          🎨 Image Generator
        </button>
      </div>

      <div className="content-container">
        {activeTab === "chat" ? <ChatBot /> : <ImageGenerator />}
      </div>
    </div>
  );
}

export default App;
