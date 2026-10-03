# Simple RAG with Python (Week 3, Part 2)

The two Make.com scenarios from Part 1, rebuilt in plain Python (no LangChain / LlamaIndex),
following *Lab3_Part 2_Simple_RAG_with_Python_lab.pdf*.

| File | What it does | Make.com equivalent |
|---|---|---|
| `ingest.py` | text file → word chunks (200 / 20 overlap) → Gemini `gemini-embedding-2` (1024 dims) → Pinecone (`week3-code-lab`) | RAG Ingestion scenario |
| `query.py` | question → embedding → Pinecone top-k → join chunks → Gemini answer (only from the context) | RAG Query scenario |
| `experiments.py` | Experiment A (top-k 1/3/5), Experiment B (chunk size 100/400 in fresh namespaces), out-of-scope question, relevance check | – |
| `make_check.py` | looks at what the Make scenario stored (namespace `week3-lab`) and repeats its search step | – |
| `concept_demo.py` | same question to Gemini with and without the right chunk pasted in | the "Concept" demo |
| `setup_index.py` | optional: creates the Pinecone index (dense, 1024, cosine) | – |
| `data/intelligent_agents_overview.txt` | the knowledge base from the lab materials | Google Drive file |

```bash
pip install -r requirements.txt
cp .env.example .env          # then put your own keys in it
python ingest.py
python query.py               # asks "Ask a question:"
python experiments.py
```
All numbers are saved to `../results/lab3_results.json`.
