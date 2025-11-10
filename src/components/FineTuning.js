import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './FineTuning.css';

function FineTuning() {
  const [trainingData, setTrainingData] = useState([]);
  const [loading, setLoading] = useState(false);
  const [activeStep, setActiveStep] = useState(1);
  const [prepareResult, setPrepareResult] = useState(null);
  const [testMessage, setTestMessage] = useState('');
  const [testResult, setTestResult] = useState(null);
  const [testLoading, setTestLoading] = useState(false);

  useEffect(() => {
    loadExampleData();
  }, []);

  const loadExampleData = async () => {
    setLoading(true);
    try {
      const response = await axios.get('http://localhost:5000/api/finetune/example-data');
      if (response.data.success) {
        setTrainingData(response.data.training_data);
      }
    } catch (error) {
      console.error('Error loading example data:', error);
    } finally {
      setLoading(false);
    }
  };

  const prepareData = async () => {
    setLoading(true);
    setPrepareResult(null);
    try {
      const response = await axios.post('http://localhost:5000/api/finetune/prepare', {
        training_data: trainingData
      });
      if (response.data.success) {
        setPrepareResult(response.data);
        setActiveStep(3);
      }
    } catch (error) {
      setPrepareResult({
        success: false,
        error: error.response?.data?.error || 'Failed to prepare data'
      });
    } finally {
      setLoading(false);
    }
  };

  const testModels = async () => {
    if (!testMessage.trim()) return;
    
    setTestLoading(true);
    setTestResult(null);
    try {
      const response = await axios.post('http://localhost:5000/api/finetune/test', {
        message: testMessage
      });
      if (response.data.success) {
        setTestResult(response.data);
      }
    } catch (error) {
      setTestResult({
        success: false,
        error: error.response?.data?.error || 'Failed to test models'
      });
    } finally {
      setTestLoading(false);
    }
  };

  return (
    <div className="finetune-container">
      <div className="finetune-header">
        <h2>🎓 Fine-Tuning Example</h2>
        <p>Learn how to fine-tune an AI model with custom training data</p>
      </div>

      <div className="steps-indicator">
        <div className={`step ${activeStep >= 1 ? 'active' : ''}`}>
          <div className="step-number">1</div>
          <div className="step-label">Training Data</div>
        </div>
        <div className="step-line"></div>
        <div className={`step ${activeStep >= 2 ? 'active' : ''}`}>
          <div className="step-number">2</div>
          <div className="step-label">Prepare & Validate</div>
        </div>
        <div className="step-line"></div>
        <div className={`step ${activeStep >= 3 ? 'active' : ''}`}>
          <div className="step-number">3</div>
          <div className="step-label">Test Results</div>
        </div>
      </div>

      {/* Step 1: Training Data */}
      {activeStep >= 1 && (
        <div className="step-content">
          <h3>📚 Step 1: Training Data</h3>
          <p className="step-description">
            This is sample training data for a customer support chatbot. Each example shows how the model should respond.
          </p>
          
          <div className="training-data-list">
            {trainingData.map((item, idx) => (
              <div key={idx} className="training-example">
                <div className="example-header">Example {idx + 1}</div>
                {item.messages.map((msg, msgIdx) => (
                  <div key={msgIdx} className={`message-item ${msg.role}`}>
                    <strong>{msg.role}:</strong> {msg.content}
                  </div>
                ))}
              </div>
            ))}
          </div>

          <button 
            className="action-button"
            onClick={() => setActiveStep(2)}
            disabled={loading || trainingData.length === 0}
          >
            Next: Prepare Data →
          </button>
        </div>
      )}

      {/* Step 2: Prepare & Validate */}
      {activeStep >= 2 && (
        <div className="step-content">
          <h3>⚙️ Step 2: Prepare & Validate</h3>
          <p className="step-description">
            Validate the training data format and prepare it for fine-tuning.
          </p>

          <div className="info-box">
            <strong>📊 Dataset Info:</strong>
            <ul>
              <li>Total Examples: {trainingData.length}</li>
              <li>Format: Chat completion (messages)</li>
              <li>Use Case: Customer Support Chatbot</li>
            </ul>
          </div>

          {prepareResult && (
            <div className={`result-box ${prepareResult.success ? 'success' : 'error'}`}>
              {prepareResult.success ? (
                <>
                  <h4>✅ Data Validated Successfully!</h4>
                  <p>{prepareResult.message}</p>
                  <div className="code-preview">
                    <strong>JSONL Preview:</strong>
                    <pre>{prepareResult.jsonl_preview}</pre>
                  </div>
                  <p className="info-text">{prepareResult.info}</p>
                </>
              ) : (
                <>
                  <h4>❌ Validation Failed</h4>
                  <p>{prepareResult.error}</p>
                </>
              )}
            </div>
          )}

          <div className="button-group">
            <button 
              className="action-button secondary"
              onClick={() => setActiveStep(1)}
            >
              ← Back
            </button>
            <button 
              className="action-button"
              onClick={prepareData}
              disabled={loading}
            >
              {loading ? 'Validating...' : 'Validate Data'}
            </button>
            {prepareResult?.success && (
              <button 
                className="action-button"
                onClick={() => setActiveStep(3)}
              >
                Next: Test Models →
              </button>
            )}
          </div>
        </div>
      )}

      {/* Step 3: Test Results */}
      {activeStep >= 3 && (
        <div className="step-content">
          <h3>🧪 Step 3: Test Base vs Fine-Tuned Model</h3>
          <p className="step-description">
            Compare responses from a base model vs a fine-tuned model (simulated with system prompt).
          </p>

          <div className="test-section">
            <label>Ask a customer support question:</label>
            <textarea
              value={testMessage}
              onChange={(e) => setTestMessage(e.target.value)}
              placeholder="E.g., How do I reset my password?"
              rows="3"
              disabled={testLoading}
            />
            <button 
              className="action-button"
              onClick={testModels}
              disabled={testLoading || !testMessage.trim()}
            >
              {testLoading ? 'Testing...' : 'Compare Models'}
            </button>
          </div>

          {testResult && testResult.success && (
            <div className="comparison-results">
              <div className="model-response base">
                <h4>🤖 Base Model</h4>
                <p className="model-name">{testResult.base_model.model}</p>
                <div className="response-text">{testResult.base_model.response}</div>
              </div>

              <div className="vs-divider">VS</div>

              <div className="model-response finetuned">
                <h4>✨ Fine-Tuned Model (Simulated)</h4>
                <p className="model-name">{testResult.finetuned_model.model}</p>
                <div className="response-text">{testResult.finetuned_model.response}</div>
              </div>

              <div className="info-box">
                <strong>ℹ️ Note:</strong> {testResult.info}
              </div>
            </div>
          )}

          <div className="button-group">
            <button 
              className="action-button secondary"
              onClick={() => setActiveStep(2)}
            >
              ← Back
            </button>
          </div>
        </div>
      )}

      <div className="finetune-info">
        <h3>📖 About Fine-Tuning</h3>
        <p>
          Fine-tuning adapts a pre-trained model to your specific use case by training it on custom examples.
          This improves accuracy and makes responses more consistent with your needs.
        </p>
        <ul>
          <li><strong>Use Cases:</strong> Customer support, code generation, content writing, data extraction</li>
          <li><strong>Benefits:</strong> Better accuracy, consistent tone, reduced prompt engineering</li>
          <li><strong>Requirements:</strong> Quality training data (10+ examples), validation set, testing</li>
        </ul>
      </div>
    </div>
  );
}

export default FineTuning;
