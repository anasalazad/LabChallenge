# COS30018 Intelligent Systems – Labs 1–9

Lab challenge: complete the labs and document each week in the Lab Work Log template.

| Lab | Topic | Worklog | Main work |
|---|---|---|---|
| [Lab 1](Lab%201) | LLM access: local (Ollama) + cloud (Gemini) | `Lab1_Worklog_Week1.docx` | `Lab1_LLM_Access.ipynb` |
| [Lab 2](Lab%202) | Agent with tools and memory (smolagents) | `Lab2_Worklog_Week2.docx` | `Lab2_smolagents_agent.ipynb` |
| [Lab 3](Lab%203) | Agentic RAG + vector DB (Make.com + Python + Pinecone) | `Lab3_Worklog_Week3.docx` | Make blueprints, `simple-rag/` (`ingest.py`, `query.py`, `experiments.py`) |
| [Lab 4](Lab%204) | Multi-agent conversation (Microsoft AutoGen) | `Lab4_Worklog_Week4.docx` | `Multiagent/` (fixed app, `run_examples.py`, `groupchat_demo.py`) |
| [Lab 5](Lab%205) | Python intro, Google Colab, scikit-learn, Linear Regression | `Lab5_Worklog_Week5.docx` | `python_basics_practice.ipynb`, `colab_walkthrough.ipynb`, `linear_regression_extras.ipynb` |
| [Lab 6](Lab%206) | Naïve Bayes, PCA | `Lab6_Worklog_Week6.docx` | `Naive_Bayes.ipynb`, `PCA.ipynb`, `naive_bayes_extras.ipynb`, `pca_extras.ipynb` |
| [Lab 7](Lab%207) | TensorFlow & PyTorch, neural networks, MNIST | `Lab7_Worklog_Week7.docx` | `neural_net.ipynb` (fixed for Keras 3), `nn_experiments.ipynb`, `nn_pytorch.ipynb` |
| [Lab 8](Lab%208) | RNN, LSTM/GRU, attention (+ one-page summary deliverable) | `Lab8_Worklog_Week8.docx` | `Lab8_RNN_LSTM_Attention.ipynb`, `Lab8_Summary.pdf` |
| [Lab 9](Lab%209) | Reinforcement learning with Gymnasium (Q-learning) | `Lab9_Worklog_Week9.docx` | `Lab_Week 9.ipynb` (completed) |

- **Beginner, step by step:** Labs 1–4 → [`START_HERE_Labs1-4_click_by_click.pdf`](START_HERE_Labs1-4_click_by_click.pdf), Labs 5–9 → [`START_HERE_click_by_click_guide.pdf`](START_HERE_click_by_click_guide.pdf)
- **Keys (Labs 1–4):** copy `.env.example` to `.env` and fill it in – `.env` is git-ignored
- **What's left / how to finish:** [`Anas.md`](Anas.md) (and `Lab N/Anas.md` in each folder)
- **Run everything locally:** `pip install -r requirements.txt` (Python 3.10–3.12); Lab 4 needs its own Python 3.12 venv with `Lab 4/Multiagent/requirements.txt`
- **Worklog tools:** `_tools/` – build worklogs, insert screenshots, tick checklists (see `CLAUDE.md`)
