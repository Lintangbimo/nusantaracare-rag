import chromadb
from sentence_transformers import SentenceTransformer
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()


# =========================
# LLM NotispaceAI
# =========================

llm_client = OpenAI(
    api_key=os.getenv("NOTISPACE_API_KEY"),
    base_url="https://api.notispaces.cloud/v1"
)


# =========================
# Embedding Model
# =========================

embedding_model = SentenceTransformer(
    "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)


# =========================
# ChromaDB
# =========================

chroma_client = chromadb.PersistentClient(
    path="./chroma_db"
)

collection = chroma_client.get_or_create_collection(
    name="nusantaracare_knowledge"
)


# =========================
# Search Knowledge
# =========================

def search_knowledge(query, top_k=3):
    """
    Mencari informasi paling relevan dari ChromaDB.
    """

    query_embedding = embedding_model.encode(
        [query]
    ).tolist()

    results = collection.query(
        query_embeddings=query_embedding,
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