import os
from dotenv import load_dotenv
import openai


class Config:
    def __init__(self):
        # Load environment variables from .env file
        load_dotenv()

        # Load the OpenAI API key
        self.OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

        # Set up OpenAI API key
        openai.api_key = self.OPENAI_API_KEY

        # Add any other environment variables you need for your project
        # e.g., self.DATABASE_URL = os.environ["DATABASE_URL"]
