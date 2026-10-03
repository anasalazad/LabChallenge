"""Check what my Make.com scenarios stored in Pinecone (my addition).

Run this AFTER "RAG Ingestion" has run once in Make (and ideally after "RAG Query" too):

    python make_check.py

It (1) counts the records Make stored in namespace "week3-lab" and prints one of them (text + source
metadata), (2) compares Make's chunks with my Python chunks, and (3) repeats the Make query
pipeline step by step (same embedding model, 1024 dims, same namespace, Limit = 1 / 3 / 5, same
"---" text aggregator, same system prompt + model as the blueprint) so I can see exactly which chunks
Make's Pinecone module gets, whether they're relevant, and how the answer changes with the Limit.
Results go to ../results/lab3_results.json ("make_check") for my worklog.
"""
import json
import time
from pathlib import Path

from google.genai import types

from ingest import gemini, INDEX_NAME, chunk_text, embed_text, index, save_result, TEXT_FILE
from experiments import CHECKS

MAKE_NAMESPACE = "week3-lab"
QUESTION = "What is a learning agent?"
OUT_OF_SCOPE = "What's the weather in Melbourne?"
BLUEPRINT = Path(__file__).resolve().parent.parent / "RAG Query.blueprint.json"


def make_generate_settings():
    """Read the model, system prompt and user template straight out of the tutor's Make blueprint."""
    bp = json.loads(BLUEPRINT.read_text(encoding="utf-8"))
    module = next(m for m in bp["flow"] if m["module"].startswith("gemini-ai:createACompletion"))
    mapper = module["mapper"]
    system = mapper["system_instruction"]["parts"][0]["text"].replace("\r\n", "\n")
    template = mapper["contents"][0]["parts"][0]["text"]
    return mapper["model"], system, template


def make_answer(question, texts):
    """Make's steps 4-5: Text aggregator (---) + Gemini 'Generate a response' with the blueprint's prompts."""
    model, system, template = make_generate_settings()
    context = "\n\n---\n\n".join(texts)
    user = template.replace("{{`10`}}", context).replace("{{7.question}}", question)
    response = gemini.models.generate_content(
        model=model, contents=user, config=types.GenerateContentConfig(system_instruction=system))
    return model, (response.text or "").strip()


def list_ids(namespace):
    ids = []
    for page in index.list(namespace=namespace):
        if hasattr(page, "vectors"):              # pinecone 8+ gives pages
            ids += [v.id for v in page.vectors]
        elif isinstance(page, (list, tuple)):     # older versions give lists of ids
            ids += list(page)
        else:
            ids.append(str(page))
    return ids


def chunk_no(record_id):
    try:
        return int(record_id.rsplit("-chunk-", 1)[1])
    except (IndexError, ValueError):
        return 10 ** 6


def main():
    stats = index.describe_index_stats()
    if MAKE_NAMESPACE not in stats.namespaces:
        print(f"No records in namespace '{MAKE_NAMESPACE}' of index '{INDEX_NAME}' yet - run the Make "
              "'RAG Ingestion' scenario first (Run once).")
        return
    ids = sorted(list_ids(MAKE_NAMESPACE), key=chunk_no)
    print(f"Make stored {len(ids)} records in namespace '{MAKE_NAMESPACE}':")
    for i in ids:
        print("  ", i)

    fetched = index.fetch(ids=ids, namespace=MAKE_NAMESPACE).vectors
    words = [len((fetched[i].metadata or {}).get("text", "").split()) for i in ids if i in fetched]
    first = fetched[ids[0]]
    md = first.metadata or {}
    print(f"\nOne record ({ids[0]}):")
    print("  metadata fields:", sorted(md.keys()))
    print("  source:", md.get("source"))
    print("  text:", md.get("text", "")[:300], "...")
    print(f"  vector length: {len(first.values)}")

    py_chunks = chunk_text(TEXT_FILE.read_text(encoding="utf-8"), 200, 20)
    print(f"\nMake made {len(ids)} chunks of {min(words)}-{max(words)} words (avg {sum(words) / len(words):.0f}); "
          f"my Python chunker made {len(py_chunks)} chunks of up to 200 words.")

    print(f"\nRe-running Make's query pipeline for: {QUESTION!r}")
    qv = embed_text(QUESTION)
    searches = {}
    for k in (1, 3, 5):
        res = index.query(namespace=MAKE_NAMESPACE, vector=qv, top_k=k, include_metadata=True)
        found = [{"id": m.id, "score": round(m.score, 4),
                  "relevant": any(p in (m.metadata or {}).get("text", "").lower() for p in CHECKS[QUESTION])}
                 for m in res.matches]
        model, ans = make_answer(QUESTION, [(m.metadata or {}).get("text", "") for m in res.matches])
        searches[str(k)] = {"chunks": found, "answer": ans, "answer_words": len(ans.split()), "model": model}
        print(f"\n  Limit {k}: " + ", ".join(f"{f['id'].split('-chunk-')[-1]} ({f['score']}, "
                                              f"{'relevant' if f['relevant'] else 'not relevant'})" for f in found))
        print(f"  answer ({len(ans.split())} words): {ans[:300]}")

    res = index.query(namespace=MAKE_NAMESPACE, vector=embed_text(OUT_OF_SCOPE), top_k=3, include_metadata=True)
    model, ans = make_answer(OUT_OF_SCOPE, [(m.metadata or {}).get("text", "") for m in res.matches])
    oos = {"question": OUT_OF_SCOPE, "scores": [round(m.score, 4) for m in res.matches], "answer": ans,
           "says_not_enough": "enough information" in ans.lower()}
    print(f"\n  Out of scope ({OUT_OF_SCOPE}) - scores {oos['scores']}\n  answer: {ans[:300]}")

    save_result("make_check", {"namespace": MAKE_NAMESPACE, "n_records": len(ids), "ids": ids,
                               "words_min": min(words), "words_max": max(words),
                               "words_avg": round(sum(words) / len(words)), "metadata_fields": sorted(md.keys()),
                               "example_id": ids[0], "example_source": md.get("source"),
                               "example_text": md.get("text", "")[:300], "vector_length": len(first.values),
                               "python_chunks": len(py_chunks), "question": QUESTION, "searches": searches,
                               "out_of_scope": oos,
                               "run_at": time.strftime("%Y-%m-%d %H:%M")})
    print("\nsaved to results/lab3_results.json")


if __name__ == "__main__":
    main()
