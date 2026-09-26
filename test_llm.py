from openai import OpenAI
from dotenv import load_dotenv
import os

# Membaca file .env
load_dotenv()

# Membuat koneksi ke NotispaceAI
client = OpenAI(
    api_key=os.getenv("NOTISPACE_API_KEY"),
    base_url="https://api.notispaces.cloud/v1"
)

# Mengirim pertanyaan sederhana
response = client.chat.completions.create(
    model="notispace-v1",
    messages=[
        {
            "role": "user",
            "content": "Halo, jawab singkat: apakah API berhasil terhubung?"
        }
    ]
)

# Menampilkan jawaban
print(response.choices[0].message.content)