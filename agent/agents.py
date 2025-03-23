import json
from typing import Optional
from agent.parser import func_to_json
import logging
import google.generativeai as genai

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

sys_msg = """Our Assistant is an advanced software system powered by Google's Gemini AI.

The Assistant is specifically designed to assist with tasks related to health, fitness, and nutrition. It provides valuable calculations related to health metrics such as Basal Metabolic Rate (BMR) and Total Daily Energy Expenditure (TDEE) using recognized equations like Harris-Benedict and Mifflin-St Jeor. Additionally, it can fetch nutritional information of various food items using an external API.

Its capabilities allow it to engage in meaningful conversations and provide helpful responses related to health and nutrition. Based on the input it receives, the Assistant can calculate and provide critical health metric values, allowing users to better understand their energy expenditure and nutritional intake.

This Assistant is constantly evolving and improving its abilities to provide more accurate and informative responses. Its capabilities include understanding and processing large amounts of text, generating human-like responses, and providing detailed explanations about complex health metrics.

Whether you are looking to understand more about your daily energy expenditure, need help calculating your BMR, or want to fetch nutritional information about your meals, our Assistant is here to assist you. The ultimate goal is to support and contribute to a healthier lifestyle by making nutritional and metabolic information more accessible.
"""


class Agent:
    def __init__(
        self,
        gemini_api_key: str,
        model_name: str = 'models/gemini-2.0-flash-lite-preview',
        functions: Optional[list] = None
    ):
        genai.configure(api_key=gemini_api_key)
        self.model = genai.GenerativeModel(model_name)
        self.chat = self.model.start_chat(history=[])
        self.chat.send_message(sys_msg)
        self.functions = self._parse_functions(functions)
        self.func_mapping = self._create_func_mapping(functions)
        self.chat_history = [{'role': 'system', 'content': sys_msg}]

    def _parse_functions(self, functions: Optional[list]) -> Optional[list]:
        if functions is None:
            return None
        return [func_to_json(func) for func in functions]

    def _create_func_mapping(self, functions: Optional[list]) -> dict:
        if functions is None:
            return {}
        return {func.__name__: func for func in functions}

    def _generate_response(self, query: str) -> str:
        try:
            response = self.chat.send_message(query)
            return response.text
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return "I apologize, but I encountered an error. Please try again."

    def ask(self, query: str) -> dict:
        self.chat_history.append({'role': 'user', 'content': query})
        response_text = self._generate_response(query)
        self.chat_history.append({'role': 'assistant', 'content': response_text})
        return {'choices': [{'message': {'content': response_text}}]}