from services.rag import ask_rag


def run_agent(query):
    """
    Menjalankan agent NusantaraCare.
    """

    if not query or not query.strip():
        return "Pertanyaan tidak boleh kosong."

    answer = ask_rag(query)

    return answer