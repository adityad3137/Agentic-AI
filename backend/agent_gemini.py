from google import genai
from config import GEMINI_API_KEY, GEMINI_MODEL_NAME
from utils import *

class Agent:
    def __init__(self):
        self.client = genai.Client(api_key = GEMINI_API_KEY)

    def run(self, route, query, document = None, prev_conversation = None):

        document_info = ""
        if document != None :
            document_info = f"""
            **REFERENCE_MATERIAL** :
            {document}
            """
        
        prev_conv = ""
        if prev_conversation != None:
            prev_conv = f"""
            PREVIOUS CONVERSATION : 
            {prev_conv_to_string(prev_conversation)}
            """
        
        System_Prompt = f"""
        INSTRUCTIONS :
        {prompt[route]}

        {document_info}

        {prev_conv}
        
        CURRENT QUERY :
        {query}
        """
        
        print(System_Prompt)

        response = self.client.models.generate_content(
            model = GEMINI_MODEL_NAME,
            contents = System_Prompt
        )

        return response.text