import chromadb
from app.services.embedding import create_embedding
from pathlib import Path
import re


# Lokasi file knowledge base
DATA_PATH = Path(
    "data/raw_docs/nusantaracare_panduan_operasional_internal_v2.md"
)


def load_document():
    """
    Membaca dokumen Markdown NusantaraCare.
    """

    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"File tidak ditemukan: {DATA_PATH}"
        )

    text = DATA_PATH.read_text(encoding="utf-8")

    return text


def extract_metadata(text):
    """
    Mengambil metadata utama dari bagian Metadata dokumen.
    """
    metadata = {}

    patterns = {
        "doc_id": r"doc_id\s*:\s*(.+)",
        "doc_title": r"doc_title\s*:\s*(.+)",
        "category": r"category\s*:\s*(.+)",
        "doc_version": r"doc_version\s*:\s*(.+)",
        "effective_date": r"effective_date\s*:\s*(.+)",
        "last_updated": r"last_updated\s*:\s*(.+)",
        "is_active": r"is_active\s*:\s*(.+)",
        "owner": r"owner\s*:\s*(.+)",
        "source_path": r"source_path\s*:\s*(.+)",
    }

    for key, pattern in patterns.items():
        match = re.search(pattern, text)
        if match:
            value = match.group(1).strip()

            if key == "is_active":
                value = value.lower() == "true"

            metadata[key] = value

    return metadata


def split_into_sections(text):
    """
    Memecah dokumen berdasarkan heading Markdown level 2 (##).

    Setiap section akan menjadi satu bagian yang nantinya
    dapat diproses lebih lanjut menjadi chunks.
    """

    sections = []

    # Cari semua heading ## ...
    matches = list(
        re.finditer(
            r"^## (.+)$",
            text,
            re.MULTILINE
        )
    )

    for i, match in enumerate(matches):

        section_title = match.group(1).strip()

        start = match.end()

        if i + 1 < len(matches):
            end = matches[i + 1].start()
        else:
            end = len(text)

        section_text = text[start:end].strip()

        if section_text:
            sections.append(
                {
                    "section_title": section_title,
                    "text": section_text,
                }
            )

    return sections


def create_documents():
    """
    Membaca dokumen dan menghasilkan data terstruktur
    yang siap digunakan untuk proses chunking dan embedding.
    """

    text = load_document()

    metadata = extract_metadata(text)

    sections = split_into_sections(text)

    documents = []

    for index, section in enumerate(sections, start=1):

        document = {
            "chunk_id": f"{metadata['doc_id']}-{index:03d}",
            "text": section["text"],
            "metadata": {
                "doc_id": metadata.get("doc_id"),
                "doc_title": metadata.get("doc_title"),
                "category": metadata.get("category"),
                "doc_version": metadata.get("doc_version"),
                "effective_date": metadata.get("effective_date"),
                "last_updated": metadata.get("last_updated"),
                "is_active": metadata.get("is_active"),
                "owner": metadata.get("owner"),
                "section_title": section["section_title"],
            },
        }

        documents.append(document)

    return documents

def save_to_chromadb(documents):
    """
    Menyimpan dokumen beserta embedding ke ChromaDB.
    """

    client = chromadb.PersistentClient(
        path="./chroma_db"
    )

    collection = client.get_or_create_collection(
        name="nusantaracare_knowledge"
    )

    ids = []
    texts = []
    embeddings = []
    metadatas = []

    for document in documents:

        ids.append(document["chunk_id"])
        texts.append(document["text"])

        embedding = create_embedding(
            document["text"]
        )

        embeddings.append(embedding)
        metadatas.append(document["metadata"])

    collection.upsert(
        ids=ids,
        documents=texts,
        embeddings=embeddings,
        metadatas=metadatas
    )

    print("Data berhasil disimpan ke ChromaDB!")
    print("Jumlah data:", collection.count())

if __name__ == "__main__":

    documents = create_documents()

    print(f"Jumlah section: {len(documents)}")

    save_to_chromadb(documents)

    documents = create_documents()

    print(f"Jumlah section: {len(documents)}")
    print()

    for document in documents[:5]:

        print("=" * 60)

        print("Chunk ID:")
        print(document["chunk_id"])

        print("\nSection:")
        print(document["metadata"]["section_title"])

        print("\nMetadata:")
        print(document["metadata"])

        print("\nText:")
        print(document["text"][:500])