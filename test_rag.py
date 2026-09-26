from app.services.rag import ask_rag


question = "Bagaimana prosedur penanganan keluhan pelanggan?"

answer = ask_rag(question)

print("\nJawaban:")
print(answer)