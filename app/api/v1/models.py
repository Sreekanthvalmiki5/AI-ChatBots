import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv(override=True)
OPENROUTER_API_KEY = os.getenv('OPEN_ROUTER_API_KEY')
OPENROUTER_API_URL = os.getenv('OPEN_ROUTER_API_URL', 'https://openrouter.ai/api/v1')

def get_openrouter_model():
    router = OpenAI(base_url=OPENROUTER_API_URL, api_key=OPENROUTER_API_KEY)
    return router
        