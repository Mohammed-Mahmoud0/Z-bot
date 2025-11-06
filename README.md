# Gemini AI Chat & Image Generator

A simple web app with a Python Flask backend and React frontend. Users can chat with an AI bot (Gemini API) or generate images from text prompts using Pollinations.ai. Clean UI, easy setup, and free to use.

## Features
- Chat with Gemini AI
- Generate images from text prompts
- Simple, modern interface

## Tech Stack
- Python, Flask
- React
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
4. Start interacting with the AI!

## Note
The Image Generator now creates real images using Pollinations.ai. No API key required for image generation.
