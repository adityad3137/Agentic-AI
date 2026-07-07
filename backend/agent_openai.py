from openai import OpenAI
from config import OPENAI_API_KEY, OPENAI_MODEL_NAME
from utils import *

class Agent :

    def __init__(self) :
        self.client = OpenAI(api_key = OPENAI_API_KEY)
    
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

        response = self.client.chat.completions.create(
            model = OPENAI_MODEL_NAME,
            messages = [
                {"role" : "system", "content" : System_Prompt}
            ]
        )

        return response.choices[0].message.content