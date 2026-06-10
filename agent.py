from google import genai
from config import GEMINI_API_KEY, MODEL_NAME
from utils import *

class Agent:
    def __init__(self):

        self.client = genai.Client(
            api_key = GEMINI_API_KEY
        )

    def run(self, route, query, document, prev_conversation):

        System_Prompt = f"""
        INSTRUCTIONS :
        {prompt[route]}


        DOCUMENT :
        {document}


        PREVIOUS CONVERSATION : 
        {prev_conv_to_string(prev_conversation)}
        

        CURRENT QUERY :
        {query}
        """
        
        response = self.client.models.generate_content(
            model = MODEL_NAME,
            contents = System_Prompt
        )

        return response.text