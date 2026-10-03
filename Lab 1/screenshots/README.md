# Lab 1 screenshots go here

Save each one with the name below (only the number at the start has to be exact; .png or .jpg; a long one can be split into `1.xa_…` + `1.xb_…`). Then, from the repo folder:

```bash
python _tools/insert_screenshots.py 1
```

**Never let an API key / token show in a screenshot** – take the notebook shots from `Lab1_completed.ipynb` (the copy without the key).

| File name | What to capture |
|---|---|
| `1.1_ollama_cli.png` | **Terminal – ollama run llama3.2:1b** – the terminal after `ollama run llama3.2:1b` and the model's reply when you type `hello` (`/bye` to quit). |
| `1.2_ollama_notebook.png` | **Notebook – local model** – the `import ollama` + `ollama.chat(...)` cells and the start of the answer to 'What is an intelligent system?'. |
| `1.3_ai_studio_key.png` | **Google AI Studio – my API key** – aistudio.google.com/app/api-keys with your key in the list (it only shows the last few characters – that's fine). Never the full key. |
| `1.4_gemini_notebook.png` | **Notebook – Gemini call** – the `genai.Client()` + `generate_content` cells and the start of Gemini's answer – from `Lab1_completed.ipynb`, so no key is visible. |
| `1.5_count_both_models.png` | **Notebook – counting on both models** – the two counting functions' 'Latency: 1.32s' / 'Latency: 3.18s' lines and both answers. Two shots are fine: `1.5a_…` + `1.5b_…`. |
| `1.6_reasoning.png` | **Notebook – step by step vs direct** – the four apple cells with their 'Latency' lines and answers (Ollama + Gemini, reasoning + non-reasoning). Two shots are fine: `1.6a_…` + `1.6b_…`. |
| `1.7_gradio_chat.png` | **Gradio chat in the browser** – the 'Week 1: Local LLM Chat (Ollama)' page (http://127.0.0.1:7860) after asking it something. |
| `1.8_comparison_table.png` | **Notebook – checkpoint answers + comparison table** – the 'Checkpoint Questions' cell at the end of the notebook with the comparison table. |
