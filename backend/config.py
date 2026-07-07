import os
from dotenv import load_dotenv

load_dotenv()

SECRET_FLASK_KEY = "bf418d5bec993e7d5049f9dc3a23c755edacdf618843f5d46164d33594608ded"

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL_NAME = "gemini-2.5-flash"

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL_NAME = "gpt-4o-mini"

DIR_PATH = "/Users/adi/Documents/existing_models"