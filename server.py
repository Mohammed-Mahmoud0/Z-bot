from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import os
import requests
import base64
from io import BytesIO
from openai import OpenAI

app = Flask(__name__)
CORS(app)

GEMINI_API_KEY = "AIzaSyBas_C8_moPbGqtJytKySyMZyWrVz-Gwkw"
genai.configure(api_key=GEMINI_API_KEY)

OPENAI_API_KEY = "sk-abcdqrstefgh5678abcdqrstefgh5678abcdqrst"
openai_client = OpenAI(api_key=OPENAI_API_KEY)

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
            messages = [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": message
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": image
                            }
                        }
                    ]
                }
            ]
            
            response = openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                max_tokens=500
            )
            
            response_text = response.choices[0].message.content
        else:
            model = genai.GenerativeModel('gemini-2.5-flash')
            response = model.generate_content(message)
            
            if hasattr(response, 'text'):
                response_text = response.text
            elif hasattr(response, 'candidates') and len(response.candidates) > 0:
                response_text = response.candidates[0].content.parts[0].text
            else:
                response_text = "I apologize, but I couldn't generate a response."
        
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
        models = genai.list_models()
        model_list = []
        for model in models:
            if 'generateContent' in model.supported_generation_methods:
                model_list.append({
                    'name': model.name,
                    'display_name': model.display_name,
                    'description': model.description
                })
        return jsonify({
            'success': True,
            'models': model_list
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
