from openai import OpenAI
from dotenv import load_dotenv
import os


# Membaca file .env
load_dotenv()


# Membuat client NotispaceAI
client = OpenAI(
    api_key=os.getenv("NOTISPACE_API_KEY"),
    base_url="https://api.notispaces.cloud/v1"
)


def create_embedding(text):
    """
    Membuat embedding dari sebuah text.
    """

    response = client.embeddings.create(
        model="notispace-embedding",
        input=text
    )

    return response.data[0].embedding