"""Part 1 - Ingestion pipeline: text file -> chunks -> Gemini embeddings -> Pinecone.

This is Appendix A of the lab sheet. My additions (marked "my addition") are small:
  * the main code is inside ingest() so experiments.py can reuse it,
  * optional command-line settings for the chunk-size experiment,
  * a retry when Gemini's free tier says "too many requests" (error 429),
  * the numbers are saved to ../results/lab3_results.json for my worklog.

    python ingest.py                                              # the normal run (200 / 20)
    python ingest.py --chunk-size 100 --namespace week3-code-100  # experiment B

Make.com equivalent: Google Drive -> Chunk text -> Iterator -> Gemini embeddings -> Pinecone upsert.
"""
import argparse
import json
import os
import re
import time
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import errors, types
from pinecone import Pinecone

load_dotenv()   # reads .env from this folder or any folder above it (I keep one .env in the repo root)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
INDEX_NAME = os.getenv("PINECONE_INDEX")

NAMESPACE = "week3-code-lab"
EMBEDDING_MODEL = "gemini-embedding-2"
EMBEDDING_DIMENSION = 1024

HERE = Path(__file__).resolve().parent
TEXT_FILE = HERE / "data" / "intelligent_agents_overview.txt"    # (my change) works from any folder
RESULTS_FILE = HERE.parent / "results" / "lab3_results.json"

if not all([GEMINI_API_KEY, PINECONE_API_KEY, INDEX_NAME]):
    raise ValueError("Missing GEMINI_API_KEY, PINECONE_API_KEY, or PINECONE_INDEX in .env")

gemini = genai.Client(api_key=GEMINI_API_KEY)
pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index(INDEX_NAME)


def chunk_text(text: str, chunk_size: int = 200, overlap: int = 20) -> list[str]:
    """Split text into overlapping word-based chunks."""
    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than 0")
    if overlap < 0 or overlap >= chunk_size:
        raise ValueError("overlap must be >= 0 and smaller than chunk_size")

    words = text.split()
    chunks = []
    step = chunk_size - overlap

    for start in range(0, len(words), step):
        end = start + chunk_size
        chunk_words = words[start:end]

        if not chunk_words:
            break

        chunks.append(" ".join(chunk_words))

        if end >= len(words):
            break

    return chunks


def embed_text(text: str) -> list[float]:
    for attempt in range(6):          # (my addition) wait and retry on the free tier's "429 too many requests"
        try:
            result = gemini.models.embed_content(
                model=EMBEDDING_MODEL,
                contents=text,
                config=types.EmbedContentConfig(
                    output_dimensionality=EMBEDDING_DIMENSION
                ),
            )
            return result.embeddings[0].values
        except errors.ClientError as e:
            if e.code != 429 or attempt == 5:
                raise
            found = re.search(r"retry in ([\d.]+)s", str(e))
            wait = float(found.group(1)) + 1 if found else 10 * (attempt + 1)
            print(f"  (Gemini rate limit - waiting {wait:.0f} s)")
            time.sleep(wait)


def save_result(key, value):
    """(my addition) keep every script's numbers in one JSON file for the worklog."""
    RESULTS_FILE.parent.mkdir(exist_ok=True)
    data = json.loads(RESULTS_FILE.read_text()) if RESULTS_FILE.exists() else {}
    data[key] = value
    RESULTS_FILE.write_text(json.dumps(data, indent=2))


def wait_until_stored(namespace, expected, timeout=60):
    """(my addition) Pinecone is 'eventually consistent' - new records can take a few seconds to show up."""
    start = time.time()
    while time.time() - start < timeout:
        ns = index.describe_index_stats().namespaces.get(namespace)
        if ns and ns.vector_count >= expected:
            return ns.vector_count
        time.sleep(2)
    return None


def ingest(file_path=TEXT_FILE, chunk_size=200, overlap=20, namespace=NAMESPACE):
    file_path = Path(file_path)
    if not file_path.exists():
        raise FileNotFoundError(f"Cannot find {file_path}. Put the lab text file inside the data folder.")

    text = file_path.read_text(encoding="utf-8")
    print(f"Loaded: {file_path.name}")
    print(f"Characters: {len(text)}")

    chunks = chunk_text(text, chunk_size=chunk_size, overlap=overlap)
    print(f"Created {len(chunks)} chunks")

    start = time.time()
    for i, chunk in enumerate(chunks):
        print(f"Processing chunk {i + 1}/{len(chunks)}")
        vector = embed_text(chunk)

        index.upsert(
            namespace=namespace,
            vectors=[
                {
                    "id": f"{file_path.name}-chunk-{i}",
                    "values": vector,
                    "metadata": {
                        "text": chunk,
                        "source": file_path.name,
                        "chunk_number": i,
                    },
                }
            ],
        )

    print("Ingestion complete.")
    stored = wait_until_stored(namespace, len(chunks))
    print(f"Pinecone now has {stored} records in namespace '{namespace}' (index '{INDEX_NAME}')")

    stats = {"file": file_path.name, "characters": len(text), "words": len(text.split()),
             "chunk_size": chunk_size, "overlap": overlap, "namespace": namespace, "index": INDEX_NAME,
             "n_chunks": len(chunks), "words_per_chunk": [len(c.split()) for c in chunks],
             "embedding_dims": len(vector), "stored": stored, "seconds": round(time.time() - start, 1),
             "first_id": f"{file_path.name}-chunk-0", "run_at": time.strftime("%Y-%m-%d %H:%M")}
    save_result(f"ingest_{namespace}", stats)
    return stats


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="RAG Part 1 - ingestion")
    parser.add_argument("--chunk-size", type=int, default=200)
    parser.add_argument("--overlap", type=int, default=20)
    parser.add_argument("--namespace", default=NAMESPACE)
    args = parser.parse_args()
    ingest(chunk_size=args.chunk_size, overlap=args.overlap, namespace=args.namespace)
