import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './ReminderAgent.css';

function ReminderAgent() {
  const [input, setInput] = useState('');
  const [email, setEmail] = useState('');
  const [loading, setLoading] = useState(false);
  const [reminders, setReminders] = useState([]);
  const [message, setMessage] = useState(null);

  useEffect(() => {
    fetchReminders();
  }, []);

  const fetchReminders = async () => {
    try {
      const response = await axios.get('http://localhost:5000/api/reminders');
      if (response.data.success) {
        setReminders(response.data.reminders);
      }
    } catch (error) {
      console.error('Error fetching reminders:', error);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!input.trim() || !email.trim() || loading) return;

    setLoading(true);
    setMessage(null);

    try {
      const response = await axios.post('http://localhost:5000/api/create-reminder', {
        message: input,
        email: email
      });

      if (response.data.success) {
        setMessage({
          type: 'success',
          text: response.data.message
        });
        setInput('');
        fetchReminders();
      } else {
        setMessage({
          type: 'error',
          text: response.data.error || 'Failed to create reminder'
        });
      }
    } catch (error) {
      setMessage({
        type: 'error',
        text: error.response?.data?.error || 'Could not connect to server'
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="reminder-container">
      <div className="reminder-header">
        <h2>🔔 AI Reminder Agent</h2>
        <p>Tell me what to remind you about and when!</p>
      </div>

      <form className="reminder-form" onSubmit={handleSubmit}>
        <div className="form-group">
          <label>Your Email:</label>
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="your.email@example.com"
            required
            disabled={loading}
          />
        </div>

        <div className="form-group">
          <label>Reminder Request:</label>
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="E.g., Remind me to call John tomorrow at 3 PM"
            rows="3"
            required
            disabled={loading}
          />
          <small className="hint">
            💡 Examples: "Remind me to buy groceries on Dec 15 at 10 AM" or "Meeting reminder tomorrow at 2 PM"
          </small>
        </div>

        <button type="submit" disabled={loading} className="create-button">
          {loading ? 'Creating...' : 'Create Reminder'}
        </button>
      </form>

      {message && (
        <div className={`message ${message.type}`}>
          {message.type === 'success' ? '✅' : '❌'} {message.text}
        </div>
      )}

      <div className="reminders-list">
        <h3>Active Reminders ({reminders.length})</h3>
        {reminders.length === 0 ? (
          <p className="no-reminders">No active reminders</p>
        ) : (
          <div className="reminders-grid">
            {reminders.map((reminder) => (
              <div key={reminder.id} className="reminder-card">
                <div className="reminder-task">{reminder.task}</div>
                <div className="reminder-time">⏰ {reminder.datetime}</div>
                <div className="reminder-email">📧 {reminder.email}</div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default ReminderAgent;
