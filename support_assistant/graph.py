import os
from typing import TypedDict

import chromadb
from sentence_transformers import SentenceTransformer
from langgraph.graph import StateGraph, END

from models import AskResponse
from prompts import MOCK_GENERAL_ANSWER

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

CHROMA_DIR = os.path.join(
    BASE_DIR,
    "chroma_db"
)

COLLECTION_NAME = "zepto_policies"

EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"

MOCK_LLM = os.getenv(
    "MOCK_LLM",
    "1"
)


class GraphState(TypedDict, total=False):

    query: str

    intent: str

    retrieved_chunks: list[str]

    retrieved_sources: list[str]

    answer: str

    confidence: float


print("Loading embedding model...")

embedding_model = SentenceTransformer(
    EMBEDDING_MODEL_NAME
)

print("Connecting to ChromaDB...")

chroma_client = chromadb.PersistentClient(
    path=CHROMA_DIR
)

collection = chroma_client.get_or_create_collection(
    name=COLLECTION_NAME,
    metadata={
        "hnsw:space": "cosine"
    },
)


def classify_intent(
    state: GraphState
):

    query = state["query"].lower()

    policy_keywords = [
        "delivery",
        "deliver",
        "return",
        "refund",
        "membership",
        "pass",
        "tracking",
        "track",
        "cancel",
        "cancellation",
        "gift card",
        "giftcard",
        "support",
        "customer service",
        "fee",
        "charge",
        "packed",
        "damaged",
        "missing",
        "spoiled",
    ]

    is_policy_question = any(
        keyword in query
        for keyword in policy_keywords
    )

    if is_policy_question:

        intent = "policy_question"

    else:

        intent = "general_question"

    return {
        "intent": intent
    }


def retrieve_and_answer(
    state: GraphState
):

    query = state["query"]

    query_embedding = embedding_model.encode(
        [query],
        normalize_embeddings=True,
    ).tolist()

    results = collection.query(
        query_embeddings=query_embedding,
        n_results=3,
        include=[
            "documents",
            "metadatas",
            "distances",
        ],
    )

    documents = results.get(
        "documents",
        [[]]
    )[0]

    metadatas = results.get(
        "metadatas",
        [[]]
    )[0]

    sources = []

    for metadata in metadatas:

        source = metadata.get(
            "source",
            "unknown"
        )

        if source not in sources:

            sources.append(
                source
            )

    if documents:

        top_chunk = documents[0]

        snippet = top_chunk[
            :500
        ].strip()

        if MOCK_LLM == "1":

            answer = (
                "Based on the retrieved context: "
                f"{snippet}"
            )

        else:

            answer = (
                "Based on the retrieved context: "
                f"{snippet}"
            )

        confidence = 1.0

    else:

        answer = (
            "I could not find relevant information "
            "in the Zepto policy knowledge base."
        )

        confidence = 0.0

    return {

        "retrieved_chunks": documents,

        "retrieved_sources": sources,

        "answer": answer,

        "confidence": confidence,
    }


def direct_answer(
    state: GraphState
):

    return {

        "answer": MOCK_GENERAL_ANSWER,

        "retrieved_chunks": [],

        "retrieved_sources": [],

        "confidence": 1.0,
    }


def route_after_classification(
    state: GraphState
):

    if state["intent"] == "policy_question":

        return "retrieve"

    return "direct"


def build_graph():

    graph_builder = StateGraph(
        GraphState
    )

    graph_builder.add_node(
        "classify_intent",
        classify_intent,
    )

    graph_builder.add_node(
        "retrieve_and_answer",
        retrieve_and_answer,
    )

    graph_builder.add_node(
        "direct_answer",
        direct_answer,
    )

    graph_builder.set_entry_point(
        "classify_intent"
    )

    graph_builder.add_conditional_edges(
        "classify_intent",
        route_after_classification,
        {
            "retrieve": "retrieve_and_answer",
            "direct": "direct_answer",
        },
    )

    graph_builder.add_edge(
        "retrieve_and_answer",
        END,
    )

    graph_builder.add_edge(
        "direct_answer",
        END,
    )

    return graph_builder.compile()


app_graph = build_graph()


def ask_question(
    query: str
) -> AskResponse:

    result = app_graph.invoke(
        {
            "query": query
        }
    )

    return AskResponse(

        answer=result.get(
            "answer",
            "No answer generated."
        ),

        sources=result.get(
            "retrieved_sources",
            []
        ),

        confidence=result.get(
            "confidence",
            0.0
        ),
    )