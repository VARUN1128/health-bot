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
openai_api_key = os.getenv('OPENAI_API_KEY')
nut_api_key = os.getenv('NUT_API_KEY')

# Instantiate FitnessAgent here so it remains open
fitness_agent = FitnessAgent(openai_api_key, nut_api_key)

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

    # Get raw chat response
    res = fitness_agent.ask(message)
    chat_response = res['choices'][0]['message']['content']
    return chat_response

def main():
    chat_interface = gr.ChatInterface(
        fn=get_response,
        title="Health & Fitness Assistant",
        description="Your personal health and fitness companion. Ask me about workouts, nutrition, and healthy living!",
    )

    chat_interface.launch()

if __name__ == "__main__":
    main()