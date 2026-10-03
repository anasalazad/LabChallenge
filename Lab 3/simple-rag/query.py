"""Part 2 - Query pipeline: question -> embed -> Pinecone search -> top-k chunks -> Gemini answer.

This is Appendix B of the lab sheet. My additions (marked "my addition"):
  * the main code is inside ask() so experiments.py can reuse it,
  * you can pass the question on the command line (otherwise it asks, like the sheet),
  * --top-k / --namespace for the experiments,
  * if Google has renamed/retired the model it tries the next one, and it retries on 429,
  * every run is saved to ../results/lab3_results.json for my worklog.

    python query.py                                   # asks "Ask a question:" like the sheet
    python query.py "What is a learning agent?"       # same, question given straight away
    python query.py "What is a learning agent?" --top-k 5

Make.com equivalent: Set variable -> Gemini embeddings -> Pinecone search -> Text aggregator
-> Gemini generate a response -> Get variable.
"""
import argparse
import json
import os
import time

from dotenv import load_dotenv
from google import genai
from pinecone import Pinecone

from ingest import RESULTS_FILE, embed_text   # same embedding model + dimension as ingestion

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
INDEX_NAME = os.getenv("PINECONE_INDEX")

NAMESPACE = "week3-code-lab"
# EMBEDDING_MODEL ("gemini-embedding-2") and EMBEDDING_DIMENSION (1024) come from ingest.py together with
# embed_text(), so the question is always embedded exactly like the chunks were
GENERATION_MODEL = "gemini-3.6-flash"
FALLBACK_MODELS = ["gemini-3.5-flash", "gemini-3-flash", "gemini-2.5-flash"]   # (my addition)
TOP_K = 3

SYSTEM_INSTRUCTION = (
    "Answer the user's question using only the supplied context. "
    "If the context does not contain enough information, say: "
    "'I don't have enough information in the provided documents.'"
)

if not all([GEMINI_API_KEY, PINECONE_API_KEY, INDEX_NAME]):
    raise ValueError("Missing GEMINI_API_KEY, PINECONE_API_KEY, or PINECONE_INDEX in .env")

gemini = genai.Client(api_key=GEMINI_API_KEY)
pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index(INDEX_NAME)


def generate(question, context):
    """gemini.interactions.create(...) like the sheet + (my addition) model fallback and 429 retry."""
    global GENERATION_MODEL
    for attempt in range(8):
        try:
            interaction = gemini.interactions.create(
                model=GENERATION_MODEL,
                system_instruction=SYSTEM_INSTRUCTION,
                input=f"CONTEXT:\n{context}\n\nQUESTION:\n{question}",
            )
            return interaction.output_text
        except Exception as e:
            status = getattr(e, "status_code", None) or getattr(e, "code", None)
            if status == 404 and FALLBACK_MODELS:
                print(f"  ({GENERATION_MODEL} not available - trying {FALLBACK_MODELS[0]})")
                GENERATION_MODEL = FALLBACK_MODELS.pop(0)
            elif status == 429 and attempt < 7:
                print("  (Gemini rate limit - waiting 20 s)")
                time.sleep(20)
            else:
                raise


def ask(question, top_k=TOP_K, namespace=NAMESPACE, show=True, save=True):
    query_vector = embed_text(question)
    if show:
        print(f"Query embedding dimensions: {len(query_vector)}")

    results = index.query(
        namespace=namespace,
        vector=query_vector,
        top_k=top_k,
        include_metadata=True,
        include_values=False,
    )

    if show:
        print("\nRetrieved chunks:")
    context_parts = []
    matches = []

    for rank, match in enumerate(results.matches, start=1):
        text = match.metadata.get("text", "")
        source = match.metadata.get("source", "unknown")
        matches.append({"rank": rank, "id": match.id, "score": round(match.score, 4),
                        "chunk_number": match.metadata.get("chunk_number"), "words": len(text.split()),
                        "text": text})

        if show:
            print("\n--------------------")
            print(f"Rank: {rank}")
            print(f"ID: {match.id}")
            print(f"Score: {match.score:.4f}")
            print(f"Source: {source}")
            print(f"Text: {text[:300]}")

        if text:
            context_parts.append(text)

    if not context_parts:
        print("\nNo context was retrieved from Pinecone.")
        raise SystemExit(1)

    context = "\n\n---\n\n".join(context_parts)

    answer = generate(question, context)

    if show:
        print("\n====================")
        print("FINAL ANSWER")
        print("====================")
        print(answer)

    run = {"question": question, "namespace": namespace, "top_k": top_k, "model": GENERATION_MODEL,
           "matches": matches, "context_words": len(context.split()), "answer": answer,
           "says_not_enough": "enough information" in answer.lower(), "run_at": time.strftime("%Y-%m-%d %H:%M")}
    if save:                                  # (my addition) keep a log of my runs for the worklog
        data = json.loads(RESULTS_FILE.read_text()) if RESULTS_FILE.exists() else {}
        data.setdefault("query_runs", []).append(run)
        RESULTS_FILE.parent.mkdir(exist_ok=True)
        RESULTS_FILE.write_text(json.dumps(data, indent=2))
    return run


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="RAG Part 2 - query")
    parser.add_argument("question", nargs="?", help="leave out to be asked, like in the lab sheet")
    parser.add_argument("--top-k", type=int, default=TOP_K)
    parser.add_argument("--namespace", default=NAMESPACE)
    args = parser.parse_args()

    question = args.question or input("Ask a question: ").strip()
    if not question:
        raise ValueError("Question cannot be empty")
    ask(question, top_k=args.top_k, namespace=args.namespace)
