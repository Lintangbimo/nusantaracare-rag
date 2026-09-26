from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv("NOTISPACE_API_KEY"),
    base_url="https://api.notispaces.cloud/v1"
)

models = client.models.list()

for model in models.data:
    print(model.id)