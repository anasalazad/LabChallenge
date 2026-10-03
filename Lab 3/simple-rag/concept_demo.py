"""The "Concept" part of the Make.com sheet (my addition): why do we need a vector database at all?

Asks Gemini the same question twice - once with no context, once with the right chunk of the
document pasted in by hand. The vector DB's job is to find and paste that chunk automatically.

    python concept_demo.py
"""
import os
import time

from dotenv import load_dotenv
from google import genai

from ingest import TEXT_FILE, save_result

load_dotenv()
gemini = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
MODEL = "gemini-3.5-flash"     # same model as the Make "RAG Query" blueprint

QUESTION = ("In our course notes on intelligent agents, at what temperature does the thermostat example "
            "turn the heating on, and what type of agent is it?")

# the paragraph I'd have to find and paste in myself without a vector DB
text = TEXT_FILE.read_text(encoding="utf-8")
start = text.index("Simple Reflex Agents")
CHUNK = text[start:text.index("Model-Based Reflex Agents")].strip()


def answer(prompt):
    t = time.time()
    response = gemini.models.generate_content(model=MODEL, contents=prompt)
    return (response.text or "").strip(), round(time.time() - t, 1)


no_ctx, t1 = answer(QUESTION)
with_ctx, t2 = answer(f"Context:\n{CHUNK}\n\nQuestion:\n{QUESTION}\n\nAnswer using only the context above.")

print("QUESTION:", QUESTION)
print("\n--- 1) NO context -------------------------------------------")
print(no_ctx)
print(f"({t1} s)")
print("\n--- 2) WITH the right chunk pasted in --------------------------")
print(with_ctx)
print(f"({t2} s)")

save_result("concept_demo", {"model": MODEL, "question": QUESTION, "chunk_words": len(CHUNK.split()),
                             "no_context": no_ctx, "with_context": with_ctx,
                             "no_context_mentions_18": "18" in no_ctx or "eighteen" in no_ctx.lower(),
                             "with_context_mentions_18": "18" in with_ctx or "eighteen" in with_ctx.lower()})
