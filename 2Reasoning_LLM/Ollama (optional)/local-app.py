import os
import json
import logging
import requests
from flask import Flask, request, Response, render_template_string

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Specify the local Ollama API endpoint and model
OLLAMA_API_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "deepseek-r1:14b"

app = Flask(__name__)

@app.route('/')
def home():
    return render_template_string(r'''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Chat Stream</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; }
                #chat { max-width: 800px; margin: auto; }
                #messages { height: 400px; border: 1px solid #ccc; padding: 10px; overflow-y: auto; margin-bottom: 10px; }
                .message { margin: 5px 0; padding: 5px; border-radius: 5px; }
                .user { background-color: #e3f2fd; }
                .assistant-thinking { background-color: #fff9c4; font-style: italic; }
                .assistant { background-color: #f5f5f5; }
                #input { width: calc(100% - 80px); padding: 8px; }
                button { width: 70px; padding: 8px; }
                h1 { text-align: center; color: #333; }
            </style>
        </head>
        <body>
            <h1>© Copyright Notice 2025, Khipus.ai - All Rights Reserved</h1>
            <h1>Demo: Local model -DeepSeek - Chatbot</h1>
    
          
            <div id="chat">
                <div id="messages"></div>
                <form onsubmit="sendMessage(event)">
                    <input type="text" id="input" placeholder="Type your message...">
                    <button type="submit">Send</button>
                </form>
            </div>
            <script>
                async function sendMessage(event) {
                    event.preventDefault();
                    const input = document.getElementById('input');
                    const userMsg = input.value;
                    input.value = '';
                    appendMessage("You: " + userMsg, "user");

                    try {
                        const response = await fetch('/chat', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({ message: userMsg })
                        });

                        const reader = response.body.getReader();
                        const decoder = new TextDecoder();
                        let buffer = "";
                        let thinkingContent = "";
                        let responseContent = "";
                        let thinkingDisplayed = false;
                        let responseMessageElement = null;

                        while (true) {
                            const { done, value } = await reader.read();
                            if (done) break;

                            // Decode the current chunk
                            const chunk = decoder.decode(value, { stream: true });
                            buffer += chunk;

                            // Check if <think> tag is present
                            if (!thinkingDisplayed && buffer.includes("<think>")) {
                                const thinkEndIndex = buffer.indexOf("</think>");
                                if (thinkEndIndex !== -1) {
                                    // Extract thinking content
                                    thinkingContent = buffer.substring(
                                        buffer.indexOf("<think>") + "<think>".length,
                                        thinkEndIndex
                                    ).trim();
                                    appendMessage("Assistant Thinking: " + thinkingContent, "assistant-thinking");

                                    // Remove the processed <think> block from the buffer
                                    buffer = buffer.substring(thinkEndIndex + "</think>".length);
                                    thinkingDisplayed = true;
                                }
                            }

                            // If thinking is already displayed, treat the rest as the response
                            if (thinkingDisplayed || !buffer.includes("<think>")) {
                                responseContent += buffer;
                                buffer = "";

                                if (responseContent.trim()) {
                                    if (!responseMessageElement) {
                                        // Create a new message element for the response
                                        responseMessageElement = document.createElement('div');
                                        responseMessageElement.className = 'message assistant';
                                        document.getElementById('messages').appendChild(responseMessageElement);
                                    }
                                    // Update the response message element with the accumulated content
                                    responseMessageElement.textContent = "Assistant: " + responseContent;
                                }
                            }
                        }

                        // Handle any remaining content in the buffer
                        if (buffer.trim()) {
                            if (!responseMessageElement) {
                                responseMessageElement = document.createElement('div');
                                responseMessageElement.className = 'message assistant';
                                document.getElementById('messages').appendChild(responseMessageElement);
                            }
                            responseMessageElement.textContent = "Assistant: " + (responseContent + buffer);
                        }
                    } catch (error) {
                        console.error('Error:', error);
                        appendMessage("Assistant: Failed to get response", "assistant");
                    }
                }

                function appendMessage(content, className) {
                    const messagesDiv = document.getElementById('messages');
                    const messageDiv = document.createElement('div');
                    messageDiv.className = 'message ' + className;
                    messageDiv.textContent = content;
                    messagesDiv.appendChild(messageDiv);
                    messagesDiv.scrollTop = messagesDiv.scrollHeight;
                }
            </script>
        </body>
        </html>
    ''')

@app.route('/chat', methods=['POST'])
def chat():
    """
    Streams partial chunks from Ollama API using DeepSeek model.
    """
    try:
        data = request.get_json()
        user_message = data['message']
        logger.info(f"Received message: {user_message[:50]}...")

        # Prepare the prompt with thinking instruction
        system_message = (
            "You are a helpful assistant powered by DeepSeek. "
            "Include internal reasoning wrapped in <think>...</think> "
            "before providing the final answer."
        )
        prompt = f"{system_message}\n\nUser: {user_message}\nAssistant:"

        try:
            response = requests.post(
                OLLAMA_API_URL,
                json={
                    "model": MODEL_NAME,
                    "prompt": prompt,
                    "stream": True
                },
                stream=True,
                timeout=30
            )
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            logger.error(f"Ollama API error: {str(e)}")
            return Response(f"Error connecting to Ollama: {str(e)}", status=500)

        def generate():
            try:
                for line in response.iter_lines():
                    if line:
                        try:
                            chunk_data = json.loads(line.decode('utf-8'))
                            if 'response' in chunk_data:
                                yield chunk_data['response']
                        except json.JSONDecodeError as e:
                            logger.warning(f"JSON decode error: {str(e)}")
                            continue
            except Exception as e:
                logger.error(f"Stream processing error: {str(e)}")
                yield f"Error processing response: {str(e)}"

        return Response(generate(), mimetype='text/plain')

    except Exception as e:
        logger.error(f"Server error: {str(e)}")
        return Response(f"Server error: {str(e)}", status=500)

if __name__ == '__main__':
    try:
        # Check if Ollama server is running
        health_check = requests.get("http://localhost:11434/api/tags")
        health_check.raise_for_status()
        models = health_check.json()
        
        # Check if the required model is available
        if any(model['name'] == MODEL_NAME for model in models['models']):
            logger.info(f"✅ {MODEL_NAME} model is available")
            logger.info("Starting Flask server...")
            app.run(debug=True, host='127.0.0.1', port=5000)
        else:
            logger.error(f"❌ {MODEL_NAME} model not found")
            logger.info(f"Please pull the model first using:")
            logger.info(f"   ollama pull {MODEL_NAME}")
            exit(1)
            
    except requests.exceptions.RequestException:
        logger.error("❌ Error: Ollama server is not running")
        logger.info("Please start Ollama first")
        exit(1)