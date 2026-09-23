from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer


BASE_DIR = Path(__file__).resolve().parent

DOCS_DIR = BASE_DIR / "docs"

CHROMA_DIR = BASE_DIR / "chroma_db"

COLLECTION_NAME = "zepto_policies"

EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"


def load_documents():
    documents = []

    for file_path in sorted(DOCS_DIR.glob("*.txt")):

        text = file_path.read_text(
            encoding="utf-8"
        ).strip()

        if not text:
            continue

        documents.append(
            {
                "id": file_path.stem,
                "text": text,
                "source": file_path.name,
            }
        )

    return documents


def chunk_text(
    text,
    chunk_size=500,
    overlap=50
):
    chunks = []

    start = 0

    while start < len(text):

        end = start + chunk_size

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        if end >= len(text):
            break

        start = end - overlap

    return chunks


def build_vector_database():

    documents = load_documents()

    if not documents:

        raise RuntimeError(
            "No documents found inside docs folder."
        )

    print("Loading embedding model...")

    model = SentenceTransformer(
        EMBEDDING_MODEL_NAME
    )

    client = chromadb.PersistentClient(
        path=str(CHROMA_DIR)
    )

    # Delete old collection if it already exists
    try:

        client.delete_collection(
            COLLECTION_NAME
        )

    except Exception:

        pass

    collection = client.create_collection(
        name=COLLECTION_NAME,
        metadata={
            "hnsw:space": "cosine"
        },
    )

    ids = []

    texts = []

    metadatas = []

    for document in documents:

        chunks = chunk_text(
            document["text"]
        )

        for index, chunk in enumerate(chunks):

            ids.append(
                f"{document['id']}_{index}"
            )

            texts.append(chunk)

            metadatas.append(
                {
                    "source": document["source"],
                    "document_id": document["id"],
                }
            )

    print("Creating embeddings...")

    embeddings = model.encode(
        texts,
        normalize_embeddings=True,
    ).tolist()

    collection.add(
        ids=ids,
        documents=texts,
        embeddings=embeddings,
        metadatas=metadatas,
    )

    print()
    print("Ingestion completed successfully.")
    print(f"Documents loaded : {len(documents)}")
    print(f"Chunks stored    : {len(texts)}")
    print(f"Database location: {CHROMA_DIR}")


if __name__ == "__main__":

    build_vector_database()