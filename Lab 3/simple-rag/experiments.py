"""The sheet's required experiments + a few extra checks, all in one go (my addition).

  Experiment A  - the same question with TOP_K = 1, 3 and 5
  Experiment B  - chunk size 100 and 400 (each in a fresh namespace) vs the normal 200
  Out-of-scope  - "What's the weather in Melbourne?" - does it make something up?
  Extra         - 3 more questions, and a check of whether the retrieved chunks really are the right ones

Run ingest.py first. Then:   python experiments.py      (takes a few minutes on the free tier)
Everything is printed and saved to ../results/lab3_results.json (my worklog reads it from there).
"""
import time

from ingest import NAMESPACE, index, ingest, save_result
from query import ask

QUESTION = "What is a learning agent?"
OUT_OF_SCOPE = "What's the weather in Melbourne?"
# each question + phrases that only appear in the part of the document that answers it,
# so I can check automatically whether a retrieved chunk is actually relevant
CHECKS = {
    QUESTION: ["learning agents improve their performance", "performance element", "critic"],
    "What are the four components of a learning agent?": ["performance element", "problem generator"],
    "How is a utility-based agent different from a goal-based agent?": ["goal-based agents extend",
                                                                        "utility-based agents assign"],
    "What is reward hacking?": ["reward hacking"],
}


def relevance(run):
    """How many of the retrieved chunks contain the passage that answers the question."""
    phrases = CHECKS.get(run["question"], [])
    hits = [any(p in m["text"].lower() for p in phrases) for m in run["matches"]]
    covered = [p for p in phrases if any(p in m["text"].lower() for m in run["matches"])]
    return {"relevant_chunks": sum(hits), "of": len(hits), "phrases_found": covered,
            "phrases_wanted": phrases, "rank_of_first_relevant": (hits.index(True) + 1) if any(hits) else None}


def short(run):
    """Small summary of one run (no long texts) for the results file."""
    return {"question": run["question"], "namespace": run["namespace"], "top_k": run["top_k"],
            "model": run["model"], "ids": [m["id"] for m in run["matches"]],
            "scores": [m["score"] for m in run["matches"]], "chunk_words": [m["words"] for m in run["matches"]],
            "context_words": run["context_words"], "answer": run["answer"],
            "answer_words": len(run["answer"].split()), "says_not_enough": run["says_not_enough"],
            **relevance(run)}


def show(title, run):
    s = short(run)
    print(f"\n### {title}")
    print(f"retrieved: {', '.join(i.split('-chunk-')[-1] for i in s['ids'])} (chunk numbers) | scores: {s['scores']}")
    print(f"relevant chunks: {s['relevant_chunks']}/{s['of']} | context sent to Gemini: {s['context_words']} words")
    print(f"answer ({s['answer_words']} words): {s['answer'][:400]}")
    return s


def fresh_namespace(ns):
    """Experiment B needs empty namespaces, otherwise old chunk IDs stay behind (sheet, section 9)."""
    try:
        index.delete(delete_all=True, namespace=ns)
        time.sleep(3)
    except Exception:
        pass   # namespace didn't exist yet - that's fine


def main():
    start = time.time()
    out = {"question": QUESTION, "run_at": time.strftime("%Y-%m-%d %H:%M")}
    if NAMESPACE not in index.describe_index_stats().namespaces:
        print(f"Namespace '{NAMESPACE}' is empty - running ingest.py first")
        ingest()

    print("=" * 70, "\nExperiment A - change top-k\n" + "=" * 70)
    out["A"] = {str(k): show(f"TOP_K = {k}", ask(QUESTION, top_k=k, show=False, save=False)) for k in (1, 3, 5)}

    print("\n" + "=" * 70, "\nExperiment B - change chunk size (fresh namespace for each)\n" + "=" * 70)
    out["B"] = {}
    for size in (100, 200, 400):
        ns = NAMESPACE if size == 200 else f"week3-code-{size}"
        if size != 200:
            fresh_namespace(ns)
            stats = ingest(chunk_size=size, overlap=20, namespace=ns)
        else:
            print("\n(200 = the normal namespace from ingest.py)")
            stats = None
        runs = {q: show(f"chunk size {size} - {q}", ask(q, top_k=3, namespace=ns, show=False, save=False))
                for q in (QUESTION, "What is reward hacking?")}
        out["B"][str(size)] = {"namespace": ns, "ingest": stats, "runs": runs}

    print("\n" + "=" * 70, "\nOut-of-scope question\n" + "=" * 70)
    oos = show(OUT_OF_SCOPE, ask(OUT_OF_SCOPE, top_k=3, show=False, save=False))
    oos["hallucinated"] = not oos["says_not_enough"]
    out["out_of_scope"] = oos

    print("\n" + "=" * 70, "\nExtra questions (top-k 3, chunk size 200)\n" + "=" * 70)
    out["extra"] = [show(q, ask(q, top_k=3, show=False, save=False)) for q in list(CHECKS)[1:]]

    out["seconds"] = round(time.time() - start)
    save_result("experiments", out)
    print(f"\nDone in {out['seconds']} s - saved to results/lab3_results.json")


if __name__ == "__main__":
    main()
