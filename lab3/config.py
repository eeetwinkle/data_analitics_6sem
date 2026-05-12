import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GITHUB_TOKEN")
BASE_URL = "https://models.inference.ai.azure.com"
MODEL = "gpt-4o-mini"
MAX_ITER = 4