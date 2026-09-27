```python
import chromadb
from chromadb.utils.embedding_functions import DefaultEmbeddingFunction
from openai import OpenAI
from dotenv import load_dotenv
import os

from services.ingest import create_documents

load_dotenv()


# =========================
# LLM NotispaceAI
# =========================

llm_client = OpenAI(
    api_key=os.getenv("NOTISPACE_API_KEY"),
    base_url="https://api.notispaces.cloud/v1"
)

LLM_MODEL = "notispace-v1"


# =========================
# Embedding Model
# =========================

embedding_function = DefaultEmbeddingFunction()


# =========================
# ChromaDB
# =========================

chroma_client = chromadb.PersistentClient(
    path="./chroma_db"
)

collection = chroma_client.get_or_create_collection(
    name="nusantaracare_knowledge",
    embedding_function=embedding_function
)


# =========================
# Auto Ingest Knowledge Base
# =========================

def initialize_knowledge_base():
    """
    Jika ChromaDB masih kosong, masukkan dokumen
    dari knowledge base ke ChromaDB.
    """

    current_count = collection.count()

    print(f"Jumlah data ChromaDB saat ini: {current_count}")

    if current_count > 0:
        print("Knowledge base sudah tersedia.")
        return

    print("ChromaDB kosong. Memulai ingest knowledge base...")

    documents = create_documents()

    texts = [
        document["text"]
        for document in documents
    ]

    metadatas = [
        document["metadata"]
        for document in documents
    ]

    ids = [
        document["chunk_id"]
        for document in documents
    ]

    collection.upsert(
        ids=ids,
        documents=texts,
        metadatas=metadatas
    )

    print(
        f"Ingest selesai. Total data ChromaDB: "
        f"{collection.count()}"
    )


# Jalankan saat aplikasi pertama kali menggunakan RAG
initialize_knowledge_base()


# =========================
# Search Knowledge
# =========================

def search_knowledge(query, top_k=3):
    """
    Mencari informasi paling relevan dari ChromaDB.
    """

    results = collection.query(
        query_texts=[query],
        n_results=top_k
    )

    documents = results["documents"][0]

    return documents


# =========================
# Generate Answer
# =========================

def generate_answer(query, context):

    prompt = f"""
Anda adalah asisten NusantaraCare.

Jawablah pertanyaan pengguna hanya berdasarkan
informasi yang diberikan pada context.

Jika informasi tidak ditemukan dalam context,
katakan bahwa informasi tersebut tidak ditemukan
dalam knowledge base.

Jangan mengarang informasi.

Context:
{context}

Pertanyaan:
{query}
"""

    try:
        response = llm_client.chat.completions.create(
            model=LLM_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "Anda adalah asisten RAG NusantaraCare."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response.choices[0].message.content

    except Exception as e:
        print(f"LLM Error: {e}")

        return (
            "Maaf, layanan AI sedang tidak tersedia. "
            "Silakan coba lagi nanti."
        )


# =========================
# RAG Pipeline
# =========================

def ask_rag(query):
    """
    Pipeline utama RAG.
    """

    documents = search_knowledge(query)

    if not documents:
        return "Informasi tidak ditemukan dalam knowledge base."

    context = "\n\n".join(documents)

    answer = generate_answer(
        query=query,
        context=context
    )

    return answer
```