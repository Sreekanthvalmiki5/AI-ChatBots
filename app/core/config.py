from dotenv import load_dotenv
import os

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
DATA_GOV_API_KEY = os.getenv("DATA_GOV_API_KEY")
DATA_GOV_API_URL=  os.getenv("DATA_GOV_API_URL")
OPEN_ROUTER_API_URL=os.getenv("OPEN_ROUTER_API_URL")