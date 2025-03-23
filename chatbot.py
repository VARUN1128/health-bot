import os
import logging
import gradio as gr
from fitness_agent import FitnessAgent
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# load environment variables from .env.list
load_dotenv('.env.list')

# Now you can access the variables using os.environ
gemini_api_key = os.getenv('GEMINI_API_KEY')
nut_api_key = os.getenv('NUT_API_KEY')

# WhatsApp-style CSS
whatsapp_css = """
.gradio-container {
    background-color: #efeae2 !important;
}

.chat-message {
    padding: 10px 15px !important;
    border-radius: 10px !important;
    margin: 5px 0 !important;
    max-width: 70% !important;
    white-space: pre-wrap !important;
}

.chat-message.user {
    background-color: #dcf8c6 !important;
    margin-left: auto !important;
}

.chat-message.assistant {
    background-color: white !important;
    margin-right: auto !important;
}

.message-wrap {
    display: flex !important;
    flex-direction: column !important;
    gap: 10px !important;
}

.input-row {
    background-color: #f0f0f0 !important;
    padding: 10px !important;
    border-top: 1px solid #d1d7db !important;
    position: fixed !important;
    bottom: 0 !important;
    width: 100% !important;
}

.textbox {
    border-radius: 20px !important;
    padding: 12px 20px !important;
    background: white !important;
    border: none !important;
}

.send-btn {
    background-color: #128C7E !important;
    border-radius: 50% !important;
    width: 40px !important;
    height: 40px !important;
    padding: 0 !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
}
"""

# Custom CSS for animations and styling
custom_css = """
@keyframes gradient {
    0% {background-position: 0% 50%;}
    50% {background-position: 100% 50%;}
    100% {background-position: 0% 50%;}
}

@keyframes float {
    0% {transform: translateY(0px);}
    50% {transform: translateY(-10px);}
    100% {transform: translateY(0px);}
}

.gradio-container {
    background: linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab);
    background-size: 400% 400%;
    animation: gradient 15s ease infinite;
}

.title-container {
    text-align: center;
    margin-bottom: 2em;
    animation: float 3s ease-in-out infinite;
}

.title {
    font-size: 2.5em;
    color: white;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    margin-bottom: 0.5em;
}

.subtitle {
    font-size: 1.2em;
    color: white;
    opacity: 0.9;
}

.chatbot {
    border-radius: 15px;
    box-shadow: 0 10px 20px rgba(0,0,0,0.2);
    background: rgba(255,255,255,0.1);
    backdrop-filter: blur(10px);
}

.message {
    padding: 1em;
    margin: 0.5em;
    border-radius: 10px;
    background: rgba(255,255,255,0.9);
    transition: all 0.3s ease;
}

.message:hover {
    transform: scale(1.02);
}

.input-container {
    margin-top: 1em;
    background: rgba(255,255,255,0.1);
    border-radius: 10px;
    padding: 1em;
}
"""

# Instantiate FitnessAgent here so it remains open
fitness_agent = FitnessAgent(gemini_api_key, nut_api_key)

def get_response(message, history):
    logger.info(f'Chat history: {history}')

    formatted_chat_history = [
        {
            'role': 'system',
            'content': '''You are a health and fitness assistant that specializes in:
            1. Providing personalized fitness advice and workout plans
            2. Offering nutrition guidance and meal planning
            3. Explaining health concepts and wellness practices
            4. Suggesting healthy lifestyle modifications
            5. Answering questions about exercise techniques and form
            6. Providing motivation and support for health goals
            
            Always prioritize safety and recommend consulting healthcare professionals for medical advice.
            Be friendly, encouraging, and focus on sustainable health practices.'''
        }
    ]

    if history:
        for i, chat in enumerate(history[0]):
            formatted_chat_history.append({
                'role': 'user' if i % 2 == 0 else 'assistant',
                'content': chat
            })

        logger.info(formatted_chat_history)
        fitness_agent.chat_history = formatted_chat_history
        logger.info(fitness_agent.chat_history)

    try:
        # Get raw chat response
        res = fitness_agent.ask(message)
        chat_response = res['choices'][0]['message']['content']
        return chat_response
    except Exception as e:
        logger.error(f"Error getting response: {e}")
        return "I apologize, but I encountered an error. Please try again."

def main():
    chat_interface = gr.ChatInterface(
        fn=get_response,
        title="Health & Fitness Assistant",
        description="Your personal health and fitness companion. Ask me about workouts, nutrition, and healthy living!",
    )

    chat_interface.launch(share=False)

if __name__ == "__main__":
    main()