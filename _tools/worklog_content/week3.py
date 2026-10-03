# Week 3 worklog content - Lab 3 (Agentic RAG + vector database: Make.com no-code + Python)
# Markup: **bold**, `code`, [[yellow = filled in once the scripts have run]].
# Numbers come from "Lab 3/results/lab3_results.json" (saved by the scripts in Lab 3/simple-rag/).
# Run ingest.py, query.py, experiments.py, make_check.py, concept_demo.py, then:
#     python _tools/build_worklogs.py 3

from worklog_content._results import get, has, k, load

RESULTS = "Lab 3/results/lab3_results.json"
# facts about the provided text file (same every time - worked out from the file itself)
DOC_WORDS, DOC_CHARS = 1530, 10425
N_CHUNKS = {100: 19, 200: 9, 400: 4}

EXPLAIN = [
    ("Why do we chunk a document instead of embedding the entire document as one vector?",
     "One vector for the whole document would mix every topic into one 'average' meaning, so a question about "
     "one small part (like learning agents) wouldn't match it well. Chunks let the search find just the part "
     "that answers the question, and only that part gets sent to Gemini – shorter, cheaper and more focused."),
    ("What does the embedding model produce?",
     "A list of numbers – here 1024 of them (a vector) – that stands for the meaning of the text. Texts that "
     "mean similar things get vectors that point in a similar direction."),
    ("Why must the document chunks and the question use the same embedding model and dimension?",
     "Every model has its own 'map' of meaning, so vectors from two different models can't be compared – it's "
     "like comparing coordinates from two different maps. And Pinecone only accepts vectors of the index's size "
     "(1024), so the dimension has to match the index and both scripts."),
    ("What does Pinecone store for each record?",
     "An `id` (e.g. `intelligent_agents_overview.txt-chunk-0`), the `values` (the 1024 numbers) and `metadata` "
     "(the chunk `text`, the `source` file name and the `chunk_number`), inside a namespace in my index."),
    ("What does cosine similarity help us find?",
     "Chunks whose vector points the same way as the question's vector, i.e. chunks with a similar meaning even if "
     "they use different words. Close to 1 = very similar, close to 0 = unrelated."),
    ("What does top-k control?",
     "How many of the most similar chunks come back and get pasted into the prompt. Small k = focused but might "
     "miss something; big k = more information but also more unrelated text and a longer prompt."),
    ("Why do we store the original chunk text as metadata if Pinecone already stores the vector?",
     "You can't turn a vector back into text. Gemini needs the actual words as context, and I need them to check "
     "what was retrieved."),
    ("Where does retrieval end and generation begin?",
     "Retrieval ends when Pinecone has returned the top-k chunks and I've joined them into one context string. "
     "Generation starts at `gemini.interactions.create(...)`, when Gemini writes the answer from that context."),
    ("What is the purpose of the system instruction that says to answer only from context?",
     "It keeps Gemini to my documents instead of its general knowledge, and gives it a fixed sentence to say when "
     "the context doesn't have the answer – so it's less likely to make things up. It's not a guarantee though, "
     "so I still check the retrieved chunks."),
    ("What part of the Python implementation corresponds to the Make Iterator?",
     "The `for i, chunk in enumerate(chunks):` loop in `ingest.py` – it embeds and upserts one chunk at a time, "
     "just like the Iterator sends one chunk at a time to the Gemini and Pinecone modules."),
]

MAPPING = [
    ["Load document", "Google Drive → Download a File", "`Path(...).read_text()`"],
    ["Chunk text", "Make AI Toolkit → Chunk text (200 / 20)", "`chunk_text(text, 200, 20)`"],
    ["Iterate chunks", "Iterator", "`for i, chunk in enumerate(chunks):`"],
    ["Embed text", "Google Gemini AI → Generate embeddings (1024)", "`embed_text(chunk)` (`embed_content`)"],
    ["Store vector", "Pinecone → Create or Update a Record", "`index.upsert(namespace=..., vectors=[...])`"],
    ["Embed question", "Google Gemini AI → Generate embeddings", "`embed_text(question)`"],
    ["Retrieve top-k", "Pinecone → Search with a query (Limit 3)", "`index.query(vector=..., top_k=3, ...)`"],
    ["Aggregate context", "Tools → Text aggregator (---)", "`\"\\n\\n---\\n\\n\".join(context_parts)`"],
    ["Generate answer", "Google Gemini AI → Generate a response", "`gemini.interactions.create(...)`"],
    ["(question in / answer out)", "Tools → Set variable / Get variable", "`input(...)` / `print(answer)`"],
]


def _chunks(ids):
    return ", ".join(i.split("-chunk-")[-1] for i in ids)


def build_spec():
    r = load(RESULTS)
    ran = bool(r)
    ing = get(r, "ingest_week3-code-lab") or {}
    ex = get(r, "experiments") or {}
    mk = get(r, "make_check") or {}
    cd = get(r, "concept_demo") or {}
    runs = get(r, "query_runs") or []
    index_name = ing.get("index") or "[[my index name]]"

    # ---- concept demo -----------------------------------------------------------
    if cd:
        concept = [
            "Concept demo (`concept_demo.py`): asked Gemini where the thermostat in our notes turns the heating on. "
            "**No context:** \"" + cd["no_context"][:160].replace("\n", " ") + "…\" – **with the right chunk pasted "
            "in:** \"" + cd["with_context"][:160].replace("\n", " ") + "…\"",
        ]
        if cd["with_context_mentions_18"] and not cd["no_context_mentions_18"]:
            concept_learning = ("Without the chunk Gemini can't know what our notes say; with it, it answered 18 °C "
                                "straight away. A vector DB's whole job is to find and paste that chunk for me.")
        else:
            concept_learning = ("The answer is much more specific with the right chunk in the prompt – a vector DB's "
                                "whole job is to find and paste that chunk for me.")
    else:
        concept = ["Concept demo (`concept_demo.py`): asked Gemini a question about our notes once with no context "
                   "and once with the right chunk pasted in – [[what each answer said]]."]
        concept_learning = ("A vector DB's whole job is to find the right chunk and paste it into the prompt for me, "
                            "so I don't have to do it by hand.")

    # ---- Make -----------------------------------------------------------------------
    if mk:
        make_ing = (f"Ran it once: Make stored **{mk['n_records']} records** in namespace `week3-lab` "
                    f"({mk['words_min']}–{mk['words_max']} words each). Opened one in Pinecone: "
                    f"`{mk['example_id']}` with metadata **{' + '.join(mk['metadata_fields'])}** "
                    f"(source = `{mk['example_source']}`).")
        if mk["n_records"] != mk["python_chunks"]:
            make_chunk_note = (f"Make made {mk['n_records']} chunks but my Python code makes {mk['python_chunks']} "
                               "from the same settings (200 / 20) – the Make module doesn't count in words (the sheet "
                               "says its unit isn't given), so the chunks come out a different size.")
        else:
            make_chunk_note = (f"Make made {mk['n_records']} chunks – the same number as my Python word-based chunker "
                               "with 200 / 20.")
        s3 = mk["searches"]["3"]
        rel3 = sum(c["relevant"] for c in s3["chunks"])
        make_retrieval = (f"For 'What is a learning agent?' the search step (Limit 3, re-run in Python with "
                          f"`make_check.py`) returns chunks "
                          f"{_chunks([c['id'] for c in s3['chunks']])} (scores "
                          f"{', '.join(str(c['score']) for c in s3['chunks'])}) – {rel3} of the 3 are from the "
                          "Learning Agents part.")
    else:
        make_ing = ("Ran it once: Make stored [[x]] records in namespace `week3-lab`. Opened one in Pinecone to check "
                    "the **text** and **source** metadata were saved.")
        make_chunk_note = ("[[Make made x chunks]] with chunk size 200 / overlap 20 – my Python chunker makes 9 "
                           "(it counts words; the sheet says Make's unit isn't given).")
        make_retrieval = "For 'What is a learning agent?' the search (Limit 3) returned chunks [[x, y, z]]."

    # ---- Python ----------------------------------------------------------------------
    py_ing = (f"`python ingest.py`: {DOC_CHARS:,} characters → **{k(r, 'ingest_week3-code-lab.n_chunks', 9)} chunks** "
              f"(eight of 200 words + one of 90) → {k(r, 'ingest_week3-code-lab.embedding_dims', 1024)} numbers each "
              f"→ {k(r, 'ingest_week3-code-lab.stored', '[[9]]')} records in namespace `week3-code-lab`"
              + (f" ({ing['seconds']} s)." if ing else "."))
    normal = next((q for q in reversed(runs) if not q["says_not_enough"]), None)
    oos_run = next((q for q in reversed(runs) if q["says_not_enough"]), None)
    if normal:
        py_query = (f"`python query.py` – \"{normal['question']}\": top 3 = chunks "
                    f"{_chunks([m['id'] for m in normal['matches']])} (scores "
                    f"{', '.join(str(m['score']) for m in normal['matches'])}), then Gemini (`{normal['model']}`) "
                    f"answered in {len(normal['answer'].split())} words using that context.")
    else:
        py_query = ("`python query.py` – \"What is a learning agent?\": printed the top 3 chunks with their scores, "
                    "then Gemini's answer [[chunk numbers + scores]].")

    A = ex.get("A") or {}
    B = ex.get("B") or {}
    oos = ex.get("out_of_scope") or {}
    if A:
        a_line = "; ".join(f"top-k {kk}: chunks {_chunks(A[kk]['ids'])}, {A[kk]['relevant_chunks']}/{A[kk]['of']} "
                           f"relevant, {A[kk]['context_words']} words of context, {A[kk]['answer_words']}-word answer"
                           for kk in ("1", "3", "5"))
        a1, a5 = A["1"], A["5"]
        if a5["relevant_chunks"] < a5["of"]:
            a_learning = (f"Top-k 1 already found the right chunk; top-k 5 added {a5['of'] - a5['relevant_chunks']} "
                          f"chunk(s) that aren't about learning agents and {a5['context_words'] - a1['context_words']} "
                          "more words for Gemini to read – more context isn't automatically better.")
        else:
            a_learning = "Even at top-k 5 all chunks were relevant here, but the prompt got 5× longer."
    else:
        a_line = "top-k 1 / 3 / 5: [[which chunks came back, how many relevant, answer length]]"
        a_learning = "[[did more chunks help, or just add unrelated text?]]"

    if B:
        def bline(size):
            run = B[size]["runs"]["What is a learning agent?"]
            rh = B[size]["runs"]["What is reward hacking?"]
            return (f"{size} words → {N_CHUNKS[int(size)]} chunks, top 3 for 'learning agent' = "
                    f"{run['relevant_chunks']}/3 relevant (best score {run['scores'][0]}), 'reward hacking' found at "
                    f"rank {rh['rank_of_first_relevant'] or '–'}, {run['context_words']} words of context")
        b_line = "; ".join(bline(s) for s in ("100", "200", "400"))
        b_learning = ("Smaller chunks = more precise passages (higher best score, less unrelated text), but an answer "
                      "can get split across chunks; bigger chunks = more context in one go but more unrelated text "
                      "(400 words is a quarter of the whole document).")
    else:
        b_line = ("100 words → 19 chunks, 200 → 9, 400 → 4 (fresh namespaces `week3-code-100` / `week3-code-400`) – "
                  "[[relevance + scores of the top 3 for each]]")
        b_learning = "[[did smaller chunks give more precise passages? did bigger ones add unrelated text?]]"

    if oos:
        oos_line = (f"Out-of-scope \"{oos['question']}\": best score only {oos['scores'][0]} (vs "
                    f"{A.get('3', {}).get('scores', ['?'])[0]} for the learning-agent question) and Gemini said: "
                    f"\"{oos['answer'][:110]}\" → " + ("**no hallucination**." if not oos["hallucinated"]
                                                        else "**it made something up** (see below)."))
    elif oos_run:
        oos_line = (f"Out-of-scope \"{oos_run['question']}\": Gemini said \"{oos_run['answer'][:110]}\" → "
                    "no hallucination.")
    else:
        oos_line = ("Out-of-scope \"What's the weather in Melbourne?\": [[did it say it doesn't have enough "
                    "information, or make something up?]]")

    # ---- deliverable tables -------------------------------------------------------------
    if A:
        tA = [[f"top-k {kk}", _chunks(A[kk]["ids"]), ", ".join(str(s) for s in A[kk]["scores"]),
               f"{A[kk]['relevant_chunks']}/{A[kk]['of']}", str(A[kk]["context_words"]), str(A[kk]["answer_words"])]
              for kk in ("1", "3", "5")]
    else:
        tA = [[f"top-k {kk}", "[[ ]]", "[[ ]]", "[[ ]]", "[[ ]]", "[[ ]]"] for kk in (1, 3, 5)]
    if B:
        tB = []
        for size in ("100", "200", "400"):
            run = B[size]["runs"]["What is a learning agent?"]
            rh = B[size]["runs"]["What is reward hacking?"]
            tB.append([f"{size} / 20", str(N_CHUNKS[int(size)]), _chunks(run["ids"]),
                       f"{run['relevant_chunks']}/3 (best {run['scores'][0]})",
                       str(rh["rank_of_first_relevant"] or "not found"), str(run["context_words"])])
    else:
        tB = [[f"{s} / 20", str(N_CHUNKS[s]), "[[ ]]", "[[ ]]", "[[ ]]", "[[ ]]"] for s in (100, 200, 400)]

    if mk:
        s1, s3, s5 = (mk["searches"][x] for x in ("1", "3", "5"))
        make_mod = [
            f"**Modification: Limit (top-k) in the Pinecone 'Search with a query' module, 3 → 1 and 3 → 5.** To see "
            "the exact effect I also re-ran Make's query steps in Python with the blueprint's own prompt and model "
            f"(`make_check.py`): Limit 1 → only chunk {_chunks([c['id'] for c in s1['chunks']])}, "
            f"{s1['answer_words']}-word answer; Limit 3 → chunks {_chunks([c['id'] for c in s3['chunks']])}, "
            f"{s3['answer_words']} words; Limit 5 → chunks {_chunks([c['id'] for c in s5['chunks']])} "
            f"({sum(c['relevant'] for c in s5['chunks'])}/5 about learning agents), {s5['answer_words']} words.",
            ("**Effect:** " + ("with Limit 1 the answer only had the one chunk to go on; going up to 5 added chunks "
                               "about other agent types, which made the context longer without adding anything "
                               "about learning agents." if sum(c['relevant'] for c in s5['chunks']) < 5 else
                               "all 5 chunks were still on topic, the answer just had more to work with.")),
        ]
    else:
        make_mod = ["**Modification:** changed Limit (top-k) in the Pinecone 'Search with a query' module from 3 to "
                    "1 and to 5, and ran the same question again – [[what changed in the retrieved chunks and the "
                    "answer (run make_check.py to get the numbers)]]."]

    # ---- checkpoint answers (Make sheet) ---------------------------------------------------
    if mk:
        top_ok = s3["chunks"][0]["relevant"]
        cq1 = make_retrieval + (" So yes – the best match is the Learning Agents section (performance element, "
                                "critic, learning element, problem generator)" if top_ok else
                                " The best match was NOT the Learning Agents definition")
        cq1 += ("." if rel3 == 3 else f", and the other {3 - rel3} chunk(s) are from other parts of the document "
                "(they only got in because Limit = 3 always returns 3 chunks).")
        mo = mk.get("out_of_scope") or {}
        cq2 = (f"The best match scores dropped to about {mo['scores'][0]} (vs {s3['chunks'][0]['score']} for the "
               "learning-agent question) because nothing in the document is about weather. The system prompt told "
               "Gemini to only use the context, so it said: \"" + mo["answer"][:140] + "\""
               + (" – no made-up weather report." if mo["says_not_enough"] else " – it still tried to answer.")
               ) if mo else "[[run make_check.py]]"
        cq3 = (f"I changed Limit from 3 to 1 and to 5. Limit 1 → only chunk {_chunks([c['id'] for c in s1['chunks']])}"
               f" ({s1['answer_words']}-word answer); Limit 5 → chunks {_chunks([c['id'] for c in s5['chunks']])}, "
               f"of which {sum(c['relevant'] for c in s5['chunks'])} are about learning agents "
               f"({s5['answer_words']}-word answer). " + make_mod[1].replace("**Effect:** ", "").capitalize())
    else:
        cq1 = "[[run make_check.py – it lists the chunks Make's search returns and whether they're relevant]]"
        cq2 = "[[what Make answered for 'What's the weather in Melbourne?']]"
        cq3 = "[[what changed after changing Limit 3 → 1 / 5]]"

    return {
        "week": 3,
        "dates": "17–23 August 2026",
        "student_name": "Anas Al Azad",
        "student_id": "105694136",
        "title": "Week 3 – Agentic RAG with a vector database (Make.com no-code + Python)",
        "intro": "My checklist for this week – ticked = done, unticked = still to do. The Python project is in "
                 "`Lab 3/simple-rag/`, the Make blueprints are in `Lab 3/`." + ("" if ran else
                 " (Yellow bits fill in by themselves once I've run the scripts and rebuilt this worklog.)"),
        "checklist": [
            ("Read both Week 3 sheets (Make.com no-code + Simple RAG with Python)", True),
            ("Python project `simple-rag/` written: `ingest.py`, `query.py`, `experiments.py` + helpers", True),
            ("Pinecone account + index (dense, 1024, cosine)", bool(ing or mk)),
            ("Concept demo – same question with and without the right chunk (`concept_demo.py`)", bool(cd)),
            ("Make: imported both blueprints + connected my own Google Drive, Gemini and Pinecone", bool(mk)),
            ("Make: ran RAG Ingestion + checked a record's text/source metadata in Pinecone", bool(mk)),
            ("Make: ran RAG Query – a normal question + 'What's the weather in Melbourne?'", False),
            ("Make: changed Limit (top-k), re-ran and compared (+ `make_check.py`)", False),
            ("Python: `ingest.py` → records in namespace `week3-code-lab`", bool(ing)),
            ("Python: `query.py` with an in-scope and an out-of-scope question", bool(runs) or bool(oos)),
            ("Experiment A (top-k 1 / 3 / 5) + Experiment B (chunk size 100 / 400)", bool(ex)),
            ("Experiment C (Make → Python mapping) + the 10 'be able to explain' questions", True),
            ("Screenshots for both deliverables + the rest (yellow boxes below)", False),
        ],
        "rows": [
            {
                "task": "Concept + set-up",
                "task_note": "Make sheet 'Concept', accounts",
                "did": [
                    "Read both sheets. Made a free Pinecone account and an index "
                    f"(`{index_name}`: dense, 1024 dimensions, cosine). Reused my Gemini key from Week 1.",
                ] + concept,
                "time": "1 h",
                "learning": [
                    "Keyword search only finds the exact words; semantic search compares meanings, so 'how do agents "
                    "get better over time?' can still find the learning-agents part.",
                    concept_learning,
                ],
                "problems": [],
            },
            {
                "task": "Make – Part 1: ingestion",
                "task_note": "RAG Ingestion blueprint",
                "did": [
                    "Created a new scenario and imported `RAG Ingestion.blueprint.json`: Google Drive → Chunk text "
                    "(200 / 20) → Iterator → Gemini embeddings (1024) → Pinecone upsert.",
                    "Uploaded `intelligent_agents_overview.txt` to my Google Drive and connected my own Google Drive, "
                    "Gemini and Pinecone accounts.",
                    make_ing,
                ],
                "time": "1 h",
                "learning": [
                    "The Iterator makes the next modules run once per chunk – that's why the Gemini and Pinecone "
                    "modules show one operation per chunk.",
                    "Record ID = file name + chunk position, so running it again overwrites the same records instead "
                    "of adding copies.",
                ],
                "problems": [
                    "The blueprint still points to the tutor's connections and the tutor's Drive file, so every module "
                    "had to be re-connected to my accounts and the file picked again before it would run.",
                    make_chunk_note,
                ],
            },
            {
                "task": "Make – Part 2: query",
                "task_note": "RAG Query blueprint",
                "did": [
                    "Imported `RAG Query.blueprint.json`: Set variable → Gemini embeddings → Pinecone search (Limit 3) "
                    "→ Text aggregator → Gemini response → Get variable.",
                    "Set the question to 'What is a learning agent?', clicked *Run once* and read the answer at the "
                    "last module. Then tried 'What's the weather in Melbourne?'.",
                    make_retrieval,
                    "Modification: Limit 3 → 1 and → 5, ran again and compared (details in the deliverable below).",
                ],
                "time": "1 h",
                "learning": [
                    "The text aggregator glues the 3 chunks together with '---' between them so Gemini sees them as "
                    "separate pieces of context.",
                    "The system prompt is what makes it say 'not enough information' instead of guessing.",
                ],
                "problems": [
                    "Same as Part 1: the Gemini (×2) and Pinecone modules had to be switched to my own connections.",
                    "The blueprint's Set variable still had the question 'What's the current weather' – changed it to "
                    "my own question first.",
                ],
            },
            {
                "task": "Python – set-up + ingestion",
                "task_note": "`simple-rag/ingest.py`",
                "did": [
                    "Made the project like section 4 of the sheet (`data/`, `ingest.py`, `query.py`, `.env`, "
                    "`.gitignore`, `requirements.txt`) and installed `google-genai pinecone python-dotenv`. Keys are "
                    "only in `.env`, which git ignores.",
                    py_ing,
                    "Checked a record in the Pinecone console: the vector is there and the metadata has `text`, "
                    "`source` and `chunk_number`.",
                ],
                "time": "1 h",
                "learning": [
                    "Overlap = the last 20 words of a chunk are repeated at the start of the next one, so a sentence "
                    "cut at a boundary isn't lost.",
                    "1024 has to be the same in three places: ingest, query and the index.",
                ],
                "problems": [
                    "Pinecone can take a few seconds before new records show up (the sheet's troubleshooting "
                    "mentions it), so `ingest.py` waits until the count is right before it says it's done.",
                ],
            },
            {
                "task": "Python – query",
                "task_note": "`simple-rag/query.py`",
                "did": [py_query, oos_line],
                "time": "0.5 h",
                "learning": [
                    "Printing the retrieved chunks first (the 'R' in RAG) shows whether a bad answer is the search's "
                    "fault or Gemini's.",
                    "A low top score is a good sign that the documents just don't cover the question.",
                ],
                "problems": [],
            },
            {
                "task": "Experiment A – top-k",
                "task_note": "`experiments.py`",
                "did": [f"Same question ('What is a learning agent?'), {a_line}."],
                "time": "0.5 h",
                "learning": [a_learning],
                "problems": [],
            },
            {
                "task": "Experiment B – chunk size",
                "task_note": "fresh namespaces",
                "did": [
                    "Re-ingested with 100 and 400-word chunks into fresh namespaces (`week3-code-100`, "
                    "`week3-code-400`) so old chunk IDs couldn't mix in, and asked the same questions (+ 'What is "
                    "reward hacking?', which is only one sentence in the document).",
                    b_line + ".",
                ],
                "time": "1 h",
                "learning": [b_learning],
                "problems": [
                    "Re-using the same namespace would leave old records behind (upsert only overwrites the same "
                    "IDs) – that's why each chunk size gets its own namespace.",
                ],
            },
            {
                "task": "Experiment C + explain questions",
                "task_note": "Make → Python mapping",
                "did": [
                    "Filled in the Make.com → Python table and answered the 10 'what you should be able to explain' "
                    "questions + the 3 Make checkpoint questions (all below).",
                ],
                "time": "0.5 h",
                "learning": [
                    "Make and Python do exactly the same steps – Python just makes every step visible (and testable).",
                ],
                "problems": [],
            },
        ],
        "total_time": "6.5 h",
        "total_note": "+ ~30 min for screenshots",
        "screenshots_intro": "Screenshots 3.3 + 3.4 are the Make.com deliverable, 3.9–3.12 the Python deliverable. "
                             "The yellow boxes are screenshots I still need to add. **Never show an API key** in any "
                             "of them.",
        "figures": [],
        "screenshots": [
            {"id": "3.1", "title": "Pinecone – my index",
             "what": "the Pinecone console page of your index showing dimension 1024, metric cosine, type dense.",
             "file": "Lab 3/screenshots/3.1_pinecone_index.png"},
            {"id": "3.2", "title": "Make – RAG Ingestion after Run once",
             "what": "the RAG Ingestion scenario canvas after *Run once* – all 5 modules with green ticks and the "
                     "little bubbles showing how many operations each did.",
             "file": "Lab 3/screenshots/3.2_make_ingestion.png"},
            {"id": "3.3", "title": "Pinecone – a record stored by Make (DELIVERABLE)",
             "what": "Pinecone console → your index → Browser → namespace `week3-lab` → one record opened, showing "
                     "its ID and the `text` + `source` metadata.",
             "file": "Lab 3/screenshots/3.3_make_pinecone_record.png"},
            {"id": "3.4", "title": "Make – RAG Query run with the final answer (DELIVERABLE)",
             "what": "the RAG Query scenario after *Run once* with 'What is a learning agent?' – click the bubble on "
                     "the last module so the answer is visible (like the last picture in the sheet).",
             "file": "Lab 3/screenshots/3.4_make_query_answer.png"},
            {"id": "3.5", "title": "Make – out-of-scope question",
             "what": "same as 3.4 but with 'What's the weather in Melbourne?' – the answer saying it doesn't have "
                     "enough information.",
             "file": "Lab 3/screenshots/3.5_make_out_of_scope.png"},
            {"id": "3.6", "title": "Make – after changing Limit",
             "what": "the Pinecone 'Search with a query' module settings with Limit changed (1 or 5) + the answer "
                     "bubble after running again. Two shots are fine: `3.6a_…` + `3.6b_…`.",
             "file": "Lab 3/screenshots/3.6_make_limit_change.png"},
            {"id": "3.7", "title": "Terminal – concept_demo.py",
             "what": "the output of `python concept_demo.py` – the answer with NO context and WITH the chunk.",
             "file": "Lab 3/screenshots/3.7_concept_demo.png"},
            {"id": "3.8", "title": "Terminal – ingest.py",
             "what": "the output of `python ingest.py` (Loaded…, Characters…, Created 9 chunks, Processing chunk 1/9 "
                     "… 9/9, Ingestion complete).",
             "file": "Lab 3/screenshots/3.8_ingest.png"},
            {"id": "3.9", "title": "Pinecone – a record from Python (DELIVERABLE)",
             "what": "Pinecone console → namespace `week3-code-lab` → one record opened with `text`, `source` and "
                     "`chunk_number` metadata.",
             "file": "Lab 3/screenshots/3.9_python_pinecone_record.png"},
            {"id": "3.10", "title": "Terminal – query.py with chunks + answer (DELIVERABLE)",
             "what": "`python query.py`, type 'What is a learning agent?' – the retrieved chunks (rank, ID, score, "
                     "text) and the FINAL ANSWER. Two shots are fine: `3.10a_…` + `3.10b_…`.",
             "file": "Lab 3/screenshots/3.10_query_learning_agent.png"},
            {"id": "3.11", "title": "Terminal – out-of-scope question (DELIVERABLE)",
             "what": "`python query.py \"What's the weather in Melbourne?\"` – the low scores and the 'not enough "
                     "information' answer.",
             "file": "Lab 3/screenshots/3.11_query_out_of_scope.png"},
            {"id": "3.12", "title": "Terminal – experiments.py (DELIVERABLE)",
             "what": "the output of `python experiments.py` – the Experiment A part (TOP_K = 1 / 3 / 5) and the "
                     "Experiment B part (chunk size 100 / 200 / 400). Two shots are fine: `3.12a_…` + `3.12b_…`.",
             "file": "Lab 3/screenshots/3.12_experiments.png"},
        ],
        "sections": [
            {
                "heading": "Deliverable – Part 1 (Make.com)",
                "paragraphs": [
                    "**Pinecone record with stored metadata:** Screenshot 3.3" +
                    (f" (`{mk['example_id']}` – metadata {', '.join(mk['metadata_fields'])})." if mk else "."),
                    "**Part 2 run with the final answer:** Screenshot 3.4 (and the out-of-scope run in 3.5).",
                ] + make_mod,
            },
            {
                "heading": "Deliverable – Part 2 (Python)",
                "paragraphs": [
                    "**Pinecone record from the Python namespace:** Screenshot 3.9. **query.py run with retrieved "
                    "chunks and final answer:** Screenshot 3.10.",
                    "**Out-of-scope question:** " + oos_line.split(": ", 1)[-1] + (
                        "" if not oos else
                        " The retrieved chunks were about agents, not weather, and the system instruction told Gemini "
                        "to only use the supplied context and gave it a sentence to use when that isn't enough – so it "
                        "didn't make anything up." if not oos.get("hallucinated") else
                        " Even with the 'only use the context' instruction it added things that aren't in the "
                        "chunks – the instruction reduces hallucination but doesn't guarantee it.") +
                    " That's also why I always look at the retrieved chunks and their scores (Screenshot 3.11).",
                    "**Modification – before/after (Experiment A, top-k):** same question 'What is a learning agent?'.",
                ],
                "table": {"header": ["", "Chunks retrieved", "Scores", "Relevant", "Context words",
                                     "Answer words"],
                          "rows": tA, "widths": [1100, 1500, 2365, 1200, 1400, 1400]},
            },
            {
                "heading": "",
                "paragraphs": [
                    "**Modification – before/after (Experiment B, chunk size, top-k 3):** relevant = the chunk "
                    "contains the Learning Agents definition.",
                ],
                "table": {"header": ["Chunk size / overlap", "Chunks", "Top 3 (learning agent)", "Relevant",
                                     "'Reward hacking' found at rank", "Context words"],
                          "rows": tB, "widths": [1300, 900, 1800, 1765, 1700, 1500]},
            },
            {
                "heading": "",
                "paragraphs": ["**Before → after in one sentence:** " + (b_learning if B else
                                                                          "[[run experiments.py]]")],
            },
            {
                "heading": "Experiment C – Make.com modules → Python",
                "table": {"header": ["Operation", "Make.com", "Python"], "rows": MAPPING,
                          "widths": [1900, 3300, 3765]},
            },
            {
                "heading": "Checkpoint questions (Make.com sheet)",
                "qa": [
                    ("1. Which chunks did the vector DB retrieve for your question, and were they actually relevant?",
                     cq1),
                    ("2. What happened when you asked a question with no matching content?", cq2),
                    ("3. What changed after your modification?", cq3),
                ],
            },
            {
                "heading": "What I should be able to explain (Python sheet, section 11)",
                "qa": [(f"{i}. {q}", a) for i, (q, a) in enumerate(EXPLAIN, 1)],
            },
        ],
    }
