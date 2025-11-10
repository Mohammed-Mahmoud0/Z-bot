# AI Assistant Suite - Free & Open Source Edition

A comprehensive web app with Python Flask backend and React frontend featuring chat, image generation, AI-powered reminders, and fine-tuning examples. **Now runs completely FREE without API keys!**

## Features
- **Chat with AI** - Text conversations using free Hugging Face models
- **Vision capability** - Image upload with guidance for free analysis tools
- **Image Generation** - Generate images from text prompts (Pollinations.ai - FREE!)
- **AI Reminder Agent** - Set reminders using natural language parsing
- **Fine-Tuning Example** - Interactive demo showing how fine-tuning works
- Simple, modern interface
- **100% FREE** - No API keys required!

## Tech Stack
- Python, Flask
- React
- Hugging Face API (free tier - no key needed)
- Pollinations.ai (free image generation)
- Rule-based NLP for reminders and fine-tuning demo

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
3. Choose between Chat, Images, Reminders, or Fine-Tuning tabs
4. **Chat Tab:** Type messages or click 📎 to attach images and ask questions about them
5. **Images Tab:** Describe what you want and get AI-generated images
6. **Reminders Tab:** Set reminders using natural language like "Remind me to call John tomorrow at 3 PM"
7. **Fine-Tuning Tab:** Interactive tutorial on preparing training data and testing fine-tuned models

## Features Demo

### Lab 1: Chat & Image Generation
- **Text Chat:** Ask any question and get AI responses
- **Image Generation:** Type a prompt like "A sunset over mountains" and get a generated image

### Lab 2: Vision Capability
- **Vision Chat:** Upload an image (click 📎) and ask "What's in this image?" or any related question

### Lab 3: AI Reminder Agent
- **Natural Language Reminders:** Say "Remind me to buy groceries on December 15 at 10 AM"
- **AI Parsing:** OpenAI GPT-4o-mini intelligently extracts task and datetime
- **Email Notifications:** Get reminded via email at the specified time
- **Active Reminders View:** See all your pending reminders

### Lab 4: Fine-Tuning Example
- **Step-by-Step Tutorial:** Learn how fine-tuning works with real examples
- **Sample Training Data:** See example customer support training data
- **Data Validation:** Prepare and validate data in JSONL format
- **Model Comparison:** Compare base model vs fine-tuned model responses
- **Interactive Testing:** Test the models with your own questions

## Note
- **100% FREE** - All features work without any API keys!
- Image Generator uses Pollinations.ai (completely free)
- Chat uses Hugging Face's free inference API (Mistral-7B model)
- Vision feature provides guidance for free alternatives
- Reminders use regex-based natural language parsing (no AI needed)
- Fine-tuning demo uses rule-based responses to show the concept

## How It Works (Free Edition)

### Chat Bot
- Uses Hugging Face's free inference API
- Falls back to rule-based responses if API is busy
- No API key required for basic use

### Image Generation  
- Pollinations.ai generates real AI images
- Completely free, no rate limits
- No account needed

### Reminder Agent
- Smart regex-based date/time parsing
- Understands: "tomorrow at 3 PM", "next Monday", etc.
- Email notifications (console logging by default)

### Fine-Tuning Demo
- Shows concept with rule-based examples
- Compares generic vs specialized responses
- Educational demonstration of fine-tuning benefits

## Example Fine-Tuning Use Cases
- Customer support chatbots with specific company knowledge
- Code generation for specific frameworks or styles
- Content writing with particular tone or format
- Data extraction with custom schemas
- Translation with domain-specific terminology

## Example Reminder Phrases
- "Remind me to call John tomorrow at 3 PM"
- "Meeting reminder on December 20 at 2:30 PM"
- "Remind me to submit report next Monday at 9 AM"
- "Doctor appointment on Jan 5 at 10:00 AM"
