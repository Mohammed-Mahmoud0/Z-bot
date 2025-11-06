import React, { useState } from 'react';
import axios from 'axios';
import './ImageGenerator.css';

function ImageGenerator() {
  const [prompt, setPrompt] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleGenerate = async () => {
    if (!prompt.trim() || loading) return;

    setLoading(true);
    setResult(null);

    try {
      const response = await axios.post('http://localhost:5000/api/generate-image', {
        prompt: prompt.trim()
      });

      if (response.data.success) {
        setResult({
          image: response.data.image,
          imageUrl: response.data.imageUrl,
          message: response.data.message
        });
      } else {
        setResult({
          error: 'Failed to generate image. Please try again.'
        });
      }
    } catch (error) {
      setResult({
        error: 'Could not connect to the server. Please make sure the server is running.'
      });
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleGenerate();
    }
  };

  return (
    <div className="image-generator-container">
      <div className="generator-content">
        <div className="prompt-section">
          <h2>🎨 Image Generator</h2>
          <p className="description">
            Describe the image you want to generate
          </p>
          
          <textarea
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="E.g., A beautiful sunset over mountains with a lake..."
            rows="4"
            disabled={loading}
          />
          
          <button 
            onClick={handleGenerate} 
            disabled={loading || !prompt.trim()}
            className="generate-button"
          >
            {loading ? 'Generating...' : 'Generate'}
          </button>
        </div>

        {result && (
          <div className="result-section">
            {result.error ? (
              <div className="error-message">
                ❌ {result.error}
              </div>
            ) : (
              <>
                <div className="success-message">
                  ✅ {result.message}
                </div>
                {result.image && (
                  <div className="image-box">
                    <h3>Generated Image:</h3>
                    <img src={result.image} alt="Generated" className="generated-image" />
                  </div>
                )}
              </>
            )}
          </div>
        )}

        {loading && (
          <div className="loading-indicator">
            <div className="spinner"></div>
            <p>Generating description...</p>
          </div>
        )}
      </div>
    </div>
  );
}

export default ImageGenerator;
