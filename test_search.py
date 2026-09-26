from app.services.rag import search_knowledge


question = "Bagaimana prosedur penanganan keluhan pelanggan?"

documents = search_knowledge(question)

print("\nHasil pencarian:\n")

for i, document in enumerate(documents, start=1):
    print("=" * 60)
    print(f"Dokumen {i}")
    print("=" * 60)
    print(document)