from fastapi import FastAPI, HTTPException
from .schemas import ChatRequest, ChatResponse
from .services.agent import run_agent
app = FastAPI(
    title="NusantaraCare RAG API",
    description="Backend service RAG untuk NusantaraCare",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "message": "NusantaraCare RAG API is running"
    }


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):

    if not request.question.strip():
        raise HTTPException(
            status_code=400,
            detail="Pertanyaan tidak boleh kosong."
        )

    try:
        answer = run_agent(request.question)

        return ChatResponse(
            answer=answer
        )

    except Exception as e:
        print(f"API Error: {e}")

        raise HTTPException(
            status_code=500,
            detail="Terjadi kesalahan pada server."
        )