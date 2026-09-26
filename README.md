NusantaraCare RAG API

Backend service berbasis FastAPI yang menerapkan Retrieval-Augmented Generation (RAG) untuk menjawab pertanyaan berdasarkan knowledge base operasional internal NusantaraCare.

1. Project Overview

NusantaraCare RAG API dibuat untuk menyediakan layanan tanya jawab berbasis knowledge base internal.

Sistem menggunakan pendekatan RAG agar jawaban yang diberikan oleh Large Language Model (LLM) didasarkan pada informasi yang terdapat dalam knowledge base.

Teknologi utama yang digunakan:

FastAPI — backend API

ChromaDB — vector database

Sentence Transformers — text embedding

NotispaceAI — LLM untuk menghasilkan jawaban

Python — bahasa pemrograman

2. Architecture

Alur utama sistem:

User
  │
  ▼
FastAPI /chat
  │
  ▼
Agent
  │
  ▼
RAG Pipeline
  │
  ├── Query Embedding
  │       │
  │       ▼
  │   ChromaDB
  │       │
  │       ▼
  │   Retrieved Context
  │
  ▼
NotispaceAI LLM
  │
  ▼
Generated Answer

Secara sederhana, sistem bekerja dengan tahapan:

User mengirim pertanyaan melalui endpoint /chat.

Pertanyaan diubah menjadi embedding menggunakan Sentence Transformers.

ChromaDB mencari dokumen yang paling relevan.

Dokumen hasil retrieval digunakan sebagai context.

Context dan pertanyaan dikirim ke NotispaceAI.

LLM menghasilkan jawaban berdasarkan context.

Jawaban dikembalikan melalui API.

3. Project Structure

nusantaracare-rag/
│
├── README.md
├── requirements.txt
├── .env.example
├── .gitignore
│
├── data/
│   └── raw_docs/
│       └── nusantaracare_panduan_operasional_internal_v2.md
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── schemas.py
│   │
│   └── services/
│       ├── __init__.py
│       ├── ingest.py
│       ├── rag.py
│       └── agent.py
│
└── chroma_db/

4. Installation

Clone repository kemudian masuk ke folder project:

git clone <repository-url>
cd nusantaracare-rag

Buat virtual environment:

py -m venv .venv

Aktifkan virtual environment pada Windows:

.venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt

5. Environment Variables

Buat file .env pada folder utama project.

Isi dengan API key NotispaceAI:

NOTISPACE_API_KEY=your_notispace_api_key

API key tidak disimpan langsung di source code.

File .env juga tidak dimasukkan ke repository karena sudah dimasukkan ke .gitignore.

6. Knowledge Base

Knowledge base berada pada:

data/raw_docs/nusantaracare_panduan_operasional_internal_v2.md

Dokumen diproses berdasarkan struktur section Markdown.

Setiap section akan menjadi sebuah chunk yang memiliki:

chunk_id

teks dokumen

doc_id

doc_title

category

doc_version

effective_date

last_updated

is_active

owner

section_title

Embedding dibuat menggunakan:

sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2

Embedding kemudian disimpan ke ChromaDB.

7. Ingestion

Proses ingestion dilakukan menggunakan:

app/services/ingest.py

Dokumen diproses menjadi beberapa section dan metadata sebelum dimasukkan ke vector database.

ChromaDB menggunakan persistent storage pada:

chroma_db/

Collection yang digunakan:

nusantaracare_knowledge

8. Running the API

Jalankan FastAPI menggunakan:

py -m uvicorn app.main:app --reload

API akan berjalan pada:

http://127.0.0.1:8000

9. API Documentation

FastAPI menyediakan Swagger UI pada:

http://127.0.0.1:8000/docs

Endpoint yang tersedia:

Method

Endpoint

Description

GET

/

Mengecek status API

POST

/chat

Mengirim pertanyaan ke RAG

10. Chat Endpoint

Request

Endpoint:

POST /chat

Request body:

{
  "question": "Bagaimana prosedur penanganan keluhan pelanggan?"
}

Response

Jika layanan LLM tersedia, API mengembalikan:

{
  "answer": "Jawaban berdasarkan knowledge base NusantaraCare."
}

11. Error Handling

API menangani beberapa kondisi seperti:

pertanyaan kosong

kegagalan layanan LLM

error pada server

Jika layanan LLM tidak tersedia, API memberikan pesan bahwa layanan AI sedang tidak tersedia daripada mengembalikan error mentah kepada pengguna.

12. RAG Pipeline

Pipeline utama berada pada:

app/services/rag.py

Fungsi utama:

search_knowledge()

digunakan untuk mencari informasi relevan dari ChromaDB.

Kemudian:

generate_answer()

mengirimkan context dan pertanyaan pengguna kepada NotispaceAI.

Pipeline lengkap:

Question
   │
   ▼
Embedding
   │
   ▼
ChromaDB Similarity Search
   │
   ▼
Relevant Documents
   │
   ▼
Context
   │
   ▼
NotispaceAI
   │
   ▼
Answer

13. Security

API key tidak ditulis langsung di source code.

Gunakan environment variable:

NOTISPACE_API_KEY=...

File berikut tidak disimpan di repository:

.env
.venv/
chroma_db/
__pycache__/

14. Limitations

Kualitas jawaban bergantung pada:

kualitas dan kelengkapan knowledge base

hasil retrieval ChromaDB

kemampuan model LLM

ketersediaan API dan quota NotispaceAI

Sistem dirancang agar jawaban berdasarkan informasi yang ditemukan pada knowledge base dan tidak mengarang informasi ketika context yang relevan tidak ditemukan.

15. Future Improvements

Pengembangan berikutnya dapat mencakup:

peningkatan strategi chunking

evaluasi retrieval menggunakan dataset pertanyaan

pengaturan similarity threshold

penambahan citation/source pada response

authentication untuk endpoint API

monitoring penggunaan API

deployment pada cloud infrastructure