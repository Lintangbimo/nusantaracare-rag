import chromadb
from sentence_transformers import SentenceTransformer
from app.services.ingest import create_documents


# =========================
# 1. Load embedding model
# =========================
print("Loading embedding model...")

embedding_model = SentenceTransformer(
    "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)

print("Embedding model loaded.")


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
    name="nusantaracare_knowledge"
)


# =========================
# 4. Ambil text
# =========================
texts = [
    document["text"]
    for document in documents
]


# =========================
# 5. Buat embedding
# =========================
print("Creating embeddings...")

embeddings = embedding_model.encode(
    texts
).tolist()

print("Embeddings created.")


# =========================
# 6. Metadata
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
# 7. Masukkan ke ChromaDB
# =========================
print("Adding documents to ChromaDB...")

collection.upsert(
    ids=ids,
    documents=texts,
    embeddings=embeddings,
    metadatas=metadatas
)

print("Ingest selesai!")
print(f"Total data di ChromaDB: {collection.count()}")