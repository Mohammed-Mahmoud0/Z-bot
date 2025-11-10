import React, { useState } from "react";
import "./App.css";
import ChatBot from "./components/ChatBot";
import ImageGenerator from "./components/ImageGenerator";
import ReminderAgent from "./components/ReminderAgent";
import FineTuning from "./components/FineTuning";

function App() {
  const [activeTab, setActiveTab] = useState("chat");

  return (
    <div className="App">
      <header className="App-header">
        <h1>🤖 AI Assistant Suite</h1>
        <p>Chat, Generate Images, Set Reminders & Learn Fine-Tuning</p>
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
          🎨 Images
        </button>
        <button
          className={`tab-button ${activeTab === "reminder" ? "active" : ""}`}
          onClick={() => setActiveTab("reminder")}
        >
          🔔 Reminders
        </button>
        <button
          className={`tab-button ${activeTab === "finetune" ? "active" : ""}`}
          onClick={() => setActiveTab("finetune")}
        >
          🎓 Fine-Tuning
        </button>
      </div>

      <div className="content-container">
        {activeTab === "chat" && <ChatBot />}
        {activeTab === "image" && <ImageGenerator />}
        {activeTab === "reminder" && <ReminderAgent />}
        {activeTab === "finetune" && <FineTuning />}
      </div>
    </div>
  );
}

export default App;
