from fastapi import FastAPI

from models import (
    AskRequest,
    AskResponse,
)

from graph import ask_question


app = FastAPI(
    title="Zepto Support Assistant",
    description=(
        "A RAG-based Zepto policy "
        "support assistant."
    ),
    version="1.0.0",
)


@app.get("/")
def root():

    return {
        "message":
        "Zepto Support Assistant is running."
    }


@app.get("/health")
def health():

    return {
        "status": "ok"
    }


@app.post(
    "/ask",
    response_model=AskResponse,
)
def ask(
    request: AskRequest
):

    return ask_question(
        request.query
    )