# Gemini AI Chat & Image Generator

A simple web app with a Python Flask backend and React frontend. Users can chat with an AI bot (Gemini API) or generate images from text prompts using Pollinations.ai. **NEW: Vision capability - attach images and ask questions about them!**

## Features
- Chat with Gemini AI
- **Vision capability - Upload images and ask questions about them (uses OpenAI GPT-4o-mini)**
- Generate images from text prompts
- Simple, modern interface

## Tech Stack
- Python, Flask
- React
- OpenAI GPT-4o-mini (vision)
- Pollinations.ai (image generation)
- Gemini API (chat)

## Setup

### Backend
1. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the Flask server:
   ```bash
   python server.py
   ```
   The server will start at `http://localhost:5000`

### Frontend
1. Install Node.js dependencies:
   ```bash
   npm install
   ```
2. Start the React development server:
   ```bash
   npm start
   ```
   The app will open at `http://localhost:3000`

## Usage
1. Make sure both the Flask backend (port 5000) and React frontend (port 3000) are running
2. Open your browser to `http://localhost:3000`
3. Choose between Chat or Image Generator tabs
4. **In Chat:** Type a message or click the 📎 button to attach an image and ask questions about it
5. **In Image Generator:** Describe what you want and get AI-generated images

## Features Demo
- **Text Chat:** Ask any question and get AI responses
- **Vision Chat:** Upload an image (click 📎) and ask "What's in this image?" or any related question
- **Image Generation:** Type a prompt like "A sunset over mountains" and get a generated image

## Note
- The Image Generator creates real images using Pollinations.ai. No API key required for image generation.
- Vision capability uses OpenAI GPT-4o-mini to analyze uploaded images.
- Text-only chat uses Gemini API for fast responses.
