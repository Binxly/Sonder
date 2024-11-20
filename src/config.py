import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

COST_PER_TOKEN = {
    "gpt-4": {"input": 0.03 / 1000, "output": 0.06 / 1000},
    "gpt-4-turbo": {"input": 0.01 / 1000, "output": 0.03 / 1000},
    "gpt-4o": {"input": 0.0025 / 1000, "output": 0.01 / 1000},
    "gpt-4o-mini": {"input": 0.00015 / 1000, "output": 0.0006 / 1000},
    "gpt-3.5-turbo": {"input": 0.0005 / 1000, "output": 0.0015 / 1000},
    "davinci-002": {"input": 0.002 / 1000, "output": 0.002 / 1000},
}

model = "gpt-3.5-turbo"

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

MAX_HISTORY = 10  # number of messages considered in the conversation history
INITIAL_BUDGET = 0.05  # in dollars
COST_PRINT_INTERVAL = 30  # in seconds
