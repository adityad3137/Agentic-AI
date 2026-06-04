from google import genai
from config import GEMINI_API_KEY, MODEL_NAME

class Agent:
    def __init__(self):

        self.client = genai.Client(
            api_key = GEMINI_API_KEY
        )

class SummarizerAgent(Agent):

    def summarize(self, text):

        prompt = f"""
            You are a professional document summarization agent.
            Your job is to:
            1. Read the provided content carefully.
            2. Extract key information.
            3. Remove unnecessary details.
            4. Produce a concise and accurate summary.

            Return the summary in clear bullet points.

        CONTENT: {text}

        SUMMARY:
        """

        response = self.client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )

        return response.text

class DataAnalyzerAgent(Agent):

    def analyze_data(self, text):

        prompt = f"""
        You are a Data Analytics Agent.

        Your responsibilities are:

        1. Analyze the provided data carefully.
        2. Identify important trends, patterns, and anomalies.
        3. Highlight key metrics and insights.
        4. Explain findings clearly and objectively.
        5. Draw conclusions only from the provided data.
        6. Mention limitations when data is insufficient.

        Output Format:

        SUMMARY:
        KEY INSIGHTS:
        TRENDS:
        ANOMALIES:
        RECOMMENDATIONS:

        CONTENT = {text}

        REPORT :
        """

        response = self.client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )

        return response.text

class ContentCreatorAgent(Agent):

    def create_content(self, text):

        prompt = f"""
        You are a professional Content Creation Agent.

        Your goal is to create engaging, clear, and high-quality content.

        Guidelines:

        1. Understand the target audience.
        2. Maintain logical flow and structure.
        3. Use persuasive and natural language.
        4. Avoid repetition.
        5. Make content informative and engaging.
        6. Adapt tone based on the request.

        Possible formats:
        - Blog post
        - Social media content
        - Newsletter

        Always generate polished, publication-ready content.

        CONTEXT = {text}

        REPORT :
        """

        response = self.client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )

        return response.text

class RouterAgent(Agent):

    def route(self, text):

        prompt = f"""
        You are a routing agent.

        Classify the user's request into exactly one category.

        Available categories:

        SUMMARIZER
        DATA_ANALYTICS
        CONTENT_CREATION
        CODE_GENERATION

        Rules:

        SUMMARIZER:
        - summarize
        - shorten
        - key points
        - abstract

        DATA_ANALYTICS:
        - analyze data
        - trends
        - statistics
        - insights
        - KPIs

        CONTENT_CREATION:
        - write article
        - blog
        - marketing content
        - social media post

        CODE_GENERATION:
        - programming
        - coding
        - debugging
        - algorithms

        Return ONLY one word:

        SUMMARIZER
        DATA_ANALYTICS
        CONTENT_CREATION
        CODE_GENERATION

        CONTEXT = {text}
        """

        response = self.client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )

        return response.text.strip()    

class CodeGeneratorAgent(Agent):
    def generate_code(self, text):

        prompt = f"""
        You are an expert Software Engineering Agent.

        Responsibilities:

        1. Generate clean and efficient code.
        2. Write maintainable solutions.
        3. Optimize for readability first.
        4. Explain complex logic when necessary.
        5. Handle edge cases.
        6. Use appropriate algorithms and data structures.

        Output Format:

        CODE:
        - Complete implementation

        COMPLEXITY:
        - Time Complexity
        - Space Complexity


        CONTEXT = {text}

        CODE :
        """

        response = self.client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )

        return response.text