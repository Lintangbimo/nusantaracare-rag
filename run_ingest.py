import chromadb
from chromadb.utils.embedding_functions import DefaultEmbeddingFunction
from app.services.ingest import create_documents


# =========================
# 1. Load embedding function
# =========================
print("Loading embedding function...")

embedding_function = DefaultEmbeddingFunction()

print("Embedding function loaded.")


# =========================
# 2. Load documents
# =========================
print("Loading documents...")

documents = create_documents()

print(f"Jumlah dokumen/section: {len(documents)}")


# =========================
# 3. Connect ChromaDB
# =========================
chroma_client = chromadb.PersistentClient(
    path="./chroma_db"
)

collection = chroma_client.get_or_create_collection(
    name="nusantaracare_knowledge",
    embedding_function=embedding_function
)


# =========================
# 4. Ambil text
# =========================
texts = [
    document["text"]
    for document in documents
]


# =========================
# 5. Metadata
# =========================
metadatas = [
    document["metadata"]
    for document in documents
]

ids = [
    document["chunk_id"]
    for document in documents
]


# =========================
# 6. Masukkan ke ChromaDB
# =========================
print("Adding documents to ChromaDB...")

collection.upsert(
    ids=ids,
    documents=texts,
    metadatas=metadatas
)

print("Ingest selesai!")
print(f"Total data di ChromaDB: {collection.count()}")