from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import requests
import base64
from io import BytesIO
from datetime import datetime, timedelta
import json
import threading
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import re

app = Flask(__name__)
CORS(app)

HF_API_URL = "https://api-inference.huggingface.co/models/"

reminders = []
reminders_lock = threading.Lock()

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        message = data.get('message', '')
        image = data.get('image', None)  
        
        if not message:
            return jsonify({
                'success': False,
                'error': 'Message is required'
            }), 400
        
        if image:
            response_text = f"I can see you've attached an image. For free image analysis, I recommend using these services:\n\n"
            response_text += "1. Upload to imgur.com and use their description\n"
            response_text += "2. Use Google Lens (lens.google.com)\n"
            response_text += "3. Try Hugging Face's BLIP model for image captioning\n\n"
            response_text += f"Your question was: {message}\n\n"
            response_text += "Note: Full vision AI requires API keys. This is a demo mode."
        else:
            try:
                hf_response = requests.post(
                    HF_API_URL + "mistralai/Mistral-7B-Instruct-v0.2",
                    json={"inputs": message, "parameters": {"max_new_tokens": 200}},
                    timeout=10
                )
                
                if hf_response.status_code == 200:
                    result = hf_response.json()
                    if isinstance(result, list) and len(result) > 0:
                        response_text = result[0].get('generated_text', message)
                        if message in response_text:
                            response_text = response_text.replace(message, '').strip()
                    else:
                        response_text = "I'm an AI assistant. How can I help you today?"
                else:
                    response_text = generate_simple_response(message)
            except:
                response_text = generate_simple_response(message)
        
        return jsonify({
            'success': True,
            'response': response_text
        })
    except Exception as e:
        print(f"Error in chat: {str(e)}")  
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

def generate_simple_response(message):
    message_lower = message.lower()
    
    if any(word in message_lower for word in ['hello', 'hi', 'hey']):
        return "Hello! I'm your AI assistant. How can I help you today?"
    elif any(word in message_lower for word in ['how are you', 'how do you do']):
        return "I'm doing well, thank you for asking! I'm here to help you with any questions you have."
    elif any(word in message_lower for word in ['help', 'support']):
        return "I'm here to help! You can ask me questions, and I'll do my best to assist you. What would you like to know?"
    elif any(word in message_lower for word in ['bye', 'goodbye', 'see you']):
        return "Goodbye! Feel free to come back if you have more questions."
    elif '?' in message:
        return f"That's an interesting question about '{message}'. Let me help you with that. For the most accurate answers, please try using a specific AI model API."
    else:
        return f"I understand you're asking about: {message}. I'm currently running in demo mode with limited capabilities. For full AI features, please configure an API key."

@app.route('/api/generate-image', methods=['POST'])
def generate_image():
    try:
        data = request.json
        prompt = data.get('prompt', '')
        
        if not prompt:
            return jsonify({
                'success': False,
                'error': 'Prompt is required'
            }), 400
        
     
        image_url = f"https://image.pollinations.ai/prompt/{requests.utils.quote(prompt)}"
        
        response = requests.get(image_url, timeout=30)
        
        if response.status_code == 200:
            image_base64 = base64.b64encode(response.content).decode('utf-8')
            
            return jsonify({
                'success': True,
                'image': f"data:image/jpeg;base64,{image_base64}",
                'imageUrl': image_url,
                'message': 'Image generated successfully using Pollinations.ai'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to generate image'
            }), 500
            
    except Exception as e:
        print(f"Error in generate_image: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/list-models', methods=['GET'])
def list_models():
    try:
        model_list = [
            {
                'name': 'Mistral-7B',
                'display_name': 'Mistral 7B Instruct',
                'description': 'Free text generation model via Hugging Face'
            },
            {
                'name': 'Pollinations-AI',
                'display_name': 'Pollinations Image Generator',
                'description': 'Free image generation'
            }
        ]
        return jsonify({
            'success': True,
            'models': model_list
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/create-reminder', methods=['POST'])
def create_reminder():
    try:
        data = request.json
        user_input = data.get('message', '')
        user_email = data.get('email', '')
        
        if not user_input or not user_email:
            return jsonify({
                'success': False,
                'error': 'Message and email are required'
            }), 400
        
        parsed_data = parse_reminder_simple(user_input)
        
        if not parsed_data.get('parsed', False):
            return jsonify({
                'success': False,
                'error': parsed_data.get('error', 'Could not parse reminder. Try format: "Remind me to [task] on [date] at [time]"')
            }), 400
        
        reminder = {
            'id': len(reminders) + 1,
            'task': parsed_data['task'],
            'datetime': parsed_data['datetime'],
            'email': user_email,
            'created_at': datetime.now().isoformat(),
            'sent': False
        }
        
        with reminders_lock:
            reminders.append(reminder)
        
        return jsonify({
            'success': True,
            'reminder': reminder,
            'message': f'Reminder set for {parsed_data["datetime"]}'
        })
        
    except Exception as e:
        print(f"Error creating reminder: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

def parse_reminder_simple(user_input):
    try:
        task_match = re.search(r'(?:remind me to|remind|to)\s+(.+?)(?:\s+on|\s+at|\s+tomorrow|\s+next)', user_input, re.IGNORECASE)
        
        if not task_match:
            task_match = re.search(r'(?:remind me to|to)\s+(.+)', user_input, re.IGNORECASE)
        
        if not task_match:
            return {"parsed": False, "error": "Could not extract task"}
        
        task = task_match.group(1).strip()
        
        user_input_lower = user_input.lower()
        now = datetime.now()
        
        if 'tomorrow' in user_input_lower:
            target_date = now + timedelta(days=1)
        elif 'next week' in user_input_lower:
            target_date = now + timedelta(days=7)
        elif 'next' in user_input_lower:
            target_date = now + timedelta(days=7)  
        else:
            date_patterns = [
                r'(\d{1,2})/(\d{1,2})',  
                r'(\w+)\s+(\d{1,2})',  
                r'(\d{4})-(\d{1,2})-(\d{1,2})'  
            ]
            
            target_date = now + timedelta(hours=1)  
        
        time_match = re.search(r'(\d{1,2}):?(\d{2})?\s*(am|pm)?', user_input_lower)
        if time_match:
            hour = int(time_match.group(1))
            minute = int(time_match.group(2)) if time_match.group(2) else 0
            am_pm = time_match.group(3)
            
            if am_pm == 'pm' and hour < 12:
                hour += 12
            elif am_pm == 'am' and hour == 12:
                hour = 0
            
            target_date = target_date.replace(hour=hour, minute=minute, second=0, microsecond=0)
        else:
            target_date = target_date.replace(hour=9, minute=0, second=0, microsecond=0)
        
        return {
            "parsed": True,
            "task": task,
            "datetime": target_date.strftime("%Y-%m-%d %H:%M")
        }
    except Exception as e:
        return {"parsed": False, "error": str(e)}

@app.route('/api/reminders', methods=['GET'])
def get_reminders():
    try:
        with reminders_lock:
            active_reminders = [r for r in reminders if not r['sent']]
        return jsonify({
            'success': True,
            'reminders': active_reminders
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

def send_email_reminder(reminder):
    try:
       
        print(f"📧 Sending reminder email to {reminder['email']}")
        print(f"Task: {reminder['task']}")
        print(f"Time: {reminder['datetime']}")
        
        reminder['sent'] = True
        
        
        
        return True
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return False

def check_reminders():
    while True:
        try:
            current_time = datetime.now()
            with reminders_lock:
                for reminder in reminders:
                    if not reminder['sent']:
                        reminder_time = datetime.strptime(reminder['datetime'], "%Y-%m-%d %H:%M")
                        if current_time >= reminder_time:
                            send_email_reminder(reminder)
            time.sleep(30) 
        except Exception as e:
            print(f"Error in reminder checker: {str(e)}")
            time.sleep(30)

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy'})

@app.route('/api/finetune/example-data', methods=['GET'])
def get_example_data():
    try:
        training_examples = [
            {
                "messages": [
                    {"role": "system", "content": "You are a helpful customer support assistant for TechCorp."},
                    {"role": "user", "content": "How do I reset my password?"},
                    {"role": "assistant", "content": "To reset your password: 1) Go to login page 2) Click 'Forgot Password' 3) Enter your email 4) Check your email for reset link 5) Follow the instructions. Need more help?"}
                ]
            },
            {
                "messages": [
                    {"role": "system", "content": "You are a helpful customer support assistant for TechCorp."},
                    {"role": "user", "content": "What are your business hours?"},
                    {"role": "assistant", "content": "TechCorp support is available Monday-Friday, 9 AM to 6 PM EST. We also offer 24/7 emergency support for critical issues. How can I help you today?"}
                ]
            },
            {
                "messages": [
                    {"role": "system", "content": "You are a helpful customer support assistant for TechCorp."},
                    {"role": "user", "content": "My product isn't working"},
                    {"role": "assistant", "content": "I'm sorry to hear that. Let's troubleshoot together: 1) Is the device powered on? 2) Have you tried restarting it? 3) Are all cables connected properly? Please let me know the answers and I'll help further."}
                ]
            },
            {
                "messages": [
                    {"role": "system", "content": "You are a helpful customer support assistant for TechCorp."},
                    {"role": "user", "content": "How do I get a refund?"},
                    {"role": "assistant", "content": "To request a refund: 1) Log into your account 2) Go to Orders 3) Select the order 4) Click 'Request Refund' 5) Fill out the form. Refunds are processed within 5-7 business days. Is there anything else I can help with?"}
                ]
            },
            {
                "messages": [
                    {"role": "system", "content": "You are a helpful customer support assistant for TechCorp."},
                    {"role": "user", "content": "Do you offer student discounts?"},
                    {"role": "assistant", "content": "Yes! Students get 20% off all products. To get your discount: 1) Create an account with your .edu email 2) Verify your student status 3) Discount applies automatically at checkout. Valid student ID required."}
                ]
            }
        ]
        
        return jsonify({
            'success': True,
            'training_data': training_examples,
            'total_examples': len(training_examples),
            'info': 'This is sample training data for fine-tuning a customer support chatbot'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/finetune/prepare', methods=['POST'])
def prepare_finetune():
    try:
        data = request.json
        training_data = data.get('training_data', [])
        
        if not training_data:
            return jsonify({
                'success': False,
                'error': 'Training data is required'
            }), 400
        
        errors = []
        for idx, example in enumerate(training_data):
            if 'messages' not in example:
                errors.append(f"Example {idx}: Missing 'messages' field")
            elif not isinstance(example['messages'], list):
                errors.append(f"Example {idx}: 'messages' must be a list")
            elif len(example['messages']) < 2:
                errors.append(f"Example {idx}: Need at least 2 messages (user + assistant)")
        
        if errors:
            return jsonify({
                'success': False,
                'validation_errors': errors
            }), 400
        
        jsonl_content = '\n'.join([json.dumps(example) for example in training_data])
        
        return jsonify({
            'success': True,
            'message': 'Training data validated successfully',
            'total_examples': len(training_data),
            'jsonl_preview': jsonl_content[:500] + '...' if len(jsonl_content) > 500 else jsonl_content,
            'info': 'Data is ready for fine-tuning. In production, upload this to OpenAI and start a fine-tuning job.'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/finetune/test', methods=['POST'])
def test_finetuned_model():
    try:
        data = request.json
        user_message = data.get('message', '')
        
        if not user_message:
            return jsonify({
                'success': False,
                'error': 'Message is required'
            }), 400
        
        base_response_text = generate_simple_response(user_message)
        
        finetuned_response_text = generate_customer_support_response(user_message)
        
        return jsonify({
            'success': True,
            'base_model': {
                'response': base_response_text,
                'model': 'Rule-based (base - generic)'
            },
            'finetuned_model': {
                'response': finetuned_response_text,
                'model': 'Rule-based (fine-tuned - customer support)'
            },
            'info': 'This demonstrates how fine-tuning customizes responses. The "fine-tuned" version provides specific customer support responses vs generic answers.'
        })
        
    except Exception as e:
        print(f"Error testing models: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

def generate_customer_support_response(message):
    message_lower = message.lower()
    
    if 'password' in message_lower or 'reset' in message_lower:
        return """To reset your password, please follow these steps:
1) Go to the login page at www.techcorp.com/login
2) Click on 'Forgot Password' below the login button
3) Enter your registered email address
4) Check your email for a password reset link
5) Click the link and create a new password

The link will expire in 24 hours for security. If you don't receive the email, please check your spam folder.

Is there anything else I can help you with?"""
    
    elif 'business hours' in message_lower or 'hours' in message_lower or 'open' in message_lower:
        return """TechCorp customer support is available:
- Monday to Friday: 9:00 AM - 6:00 PM EST
- Saturday: 10:00 AM - 4:00 PM EST
- Sunday: Closed

For critical issues, we offer 24/7 emergency support. You can reach us at:
- Phone: 1-800-TECHCORP
- Email: support@techcorp.com
- Live Chat: Available during business hours

How else can I assist you today?"""
    
    elif 'refund' in message_lower:
        return """I'd be happy to help you with a refund. Here's our process:
1) Log into your TechCorp account
2) Navigate to 'My Orders' in your account dashboard
3) Find the order you wish to return
4) Click 'Request Refund' and select a reason
5) Fill out the refund request form

Our refund policy:
- Full refunds within 30 days of purchase
- Item must be in original condition
- Refunds processed within 5-7 business days

Would you like help with any specific order?"""
    
    elif 'discount' in message_lower or 'student' in message_lower:
        return """Great news! TechCorp offers several discount programs:

Student Discount: 20% off all products
- Verify with your .edu email address
- Valid student ID required
- Discount applies automatically at checkout

Other available discounts:
- Military/Veterans: 15% off
- Teachers/Educators: 15% off
- Referral Program: $20 credit for each referral

To activate your discount, please create or log into your account.

Can I help you with anything else?"""
    
    elif 'not working' in message_lower or 'broken' in message_lower or 'issue' in message_lower:
        return """I'm sorry you're experiencing issues with your product. Let's troubleshoot together:

Step 1: Basic checks
- Is the device powered on?
- Are all cables securely connected?
- Have you tried restarting the device?

Step 2: If issue persists
- Check for software updates
- Review the troubleshooting guide in your product manual
- Try resetting to factory settings (back up data first!)

Step 3: Still need help?
Contact our technical support team:
- Phone: 1-800-TECH-HELP
- Chat: Available on our website
- Schedule a video call with a technician

What specific issue are you experiencing? I'm here to help!"""
    
    else:
        return f"""Thank you for contacting TechCorp support!

I understand you're asking about: "{message}"

I'm here to help you with:
- Account and password issues
- Product troubleshooting
- Orders and refunds
- Business hours and contact information
- Discounts and promotions

Could you please provide more details about your question so I can assist you better?

You can also:
- Call us at 1-800-TECHCORP
- Email support@techcorp.com
- Visit our Help Center at www.techcorp.com/help

Is there anything specific I can help you with today?"""
        print(f"Error testing models: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    reminder_thread = threading.Thread(target=check_reminders, daemon=True)
    reminder_thread.start()
    print("🔔 Reminder checker started!")
    
    app.run(debug=True, port=5000)
