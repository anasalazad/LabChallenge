# Lab 3 screenshots go here

Save each one with the name below (only the number at the start has to be exact; .png or .jpg; a long one can be split into `3.xa_…` + `3.xb_…`). Then, from the repo folder:

```bash
python _tools/insert_screenshots.py 3
```

**Never let an API key / token show in a screenshot.**

| File name | What to capture |
|---|---|
| `3.1_pinecone_index.png` | **Pinecone – my index** – the Pinecone console page of your index showing dimension 1024, metric cosine, type dense. |
| `3.2_make_ingestion.png` | **Make – RAG Ingestion after Run once** – the RAG Ingestion scenario canvas after *Run once* – all 5 modules with green ticks and the little bubbles showing how many operations each did. |
| `3.3_make_pinecone_record.png` | **Pinecone – a record stored by Make (DELIVERABLE)** – Pinecone console → your index → Browser → namespace `week3-lab` → one record opened, showing its ID and the `text` + `source` metadata. |
| `3.4_make_query_answer.png` | **Make – RAG Query run with the final answer (DELIVERABLE)** – the RAG Query scenario after *Run once* with 'What is a learning agent?' – click the bubble on the last module so the answer is visible (like the last picture in the sheet). |
| `3.5_make_out_of_scope.png` | **Make – out-of-scope question** – same as 3.4 but with 'What's the weather in Melbourne?' – the answer saying it doesn't have enough information. |
| `3.6_make_limit_change.png` | **Make – after changing Limit** – the Pinecone 'Search with a query' module settings with Limit changed (1 or 5) + the answer bubble after running again. Two shots are fine: `3.6a_…` + `3.6b_…`. |
| `3.7_concept_demo.png` | **Terminal – concept_demo.py** – the output of `python concept_demo.py` – the answer with NO context and WITH the chunk. |
| `3.8_ingest.png` | **Terminal – ingest.py** – the output of `python ingest.py` (Loaded…, Characters…, Created 9 chunks, Processing chunk 1/9 … 9/9, Ingestion complete). |
| `3.9_python_pinecone_record.png` | **Pinecone – a record from Python (DELIVERABLE)** – Pinecone console → namespace `week3-code-lab` → one record opened with `text`, `source` and `chunk_number` metadata. |
| `3.10_query_learning_agent.png` | **Terminal – query.py with chunks + answer (DELIVERABLE)** – `python query.py`, type 'What is a learning agent?' – the retrieved chunks (rank, ID, score, text) and the FINAL ANSWER. Two shots are fine: `3.10a_…` + `3.10b_…`. |
| `3.11_query_out_of_scope.png` | **Terminal – out-of-scope question (DELIVERABLE)** – `python query.py "What's the weather in Melbourne?"` – the low scores and the 'not enough information' answer. |
| `3.12_experiments.png` | **Terminal – experiments.py (DELIVERABLE)** – the output of `python experiments.py` – the Experiment A part (TOP_K = 1 / 3 / 5) and the Experiment B part (chunk size 100 / 200 / 400). Two shots are fine: `3.12a_…` + `3.12b_…`. |

Step-by-step: `START_HERE_Labs1-4_click_by_click.pdf` in the top folder.
