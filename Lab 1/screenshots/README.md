# Lab 1 screenshots go here

Save each one with the name below (only the number at the start has to be exact; .png or .jpg; a long one can be split into `1.xa_…` + `1.xb_…`). Then, from the repo folder:

```bash
python _tools/insert_screenshots.py 1
```

**Never let an API key / token show in a screenshot.**

| File name | What to capture |
|---|---|
| `1.1_ollama_cli.png` | **Terminal – `ollama run llama3.2:1b`** – the terminal after `ollama run llama3.2:1b`: the 'pulling … success' lines and the model's reply after you type `hello`. |
| `1.2_ollama_notebook.png` | **Notebook – local model + under the hood** – the step 3 cell (`ollama.chat`) with its answer and the '--- llama3.2:1b: … s' line, and the step 4 output (HTTP status 200, the JSON keys, 'loaded in memory'). Two shots are fine: `1.2a_…` + `1.2b_…`. |
| `1.3_ai_studio_key.png` | **Google AI Studio – my API key** – aistudio.google.com/app/api-keys with your key in the list (it only shows the last few characters – that's fine). Never screenshot the full key. |
| `1.4_gemini_notebook.png` | **Notebook – Gemini call** – the step 5 output: Gemini's answer, the '--- gemini… s \| prompt … tokens' line and the 'Same question: local … vs cloud …' line. |
| `1.5_sentiment_results.png` | **Notebook – sentiment on both models** – the step 7 results table (avg seconds, correct, one-word answers, predictions) and the 'agreed on …' lines under it. |
| `1.6_reasoning.png` | **Notebook – step by step vs direct** – the bottom of the step 8 cell: one or two answers + the small summary table (right / avg seconds / avg words). |
| `1.7_gradio_chat.png` | **Gradio chat in the browser** – http://127.0.0.1:7860 with one question answered by the local model and one by Gemini (switch the 'Which model answers?' button in between) – the '(model, x s)' line under each answer should show. |
| `1.8_comparison_table.png` | **Notebook – comparison table** – the 'Deliverable – comparison table' output and the checkpoint question 2 answer under it. |

Step-by-step: `START_HERE_Labs1-4_click_by_click.pdf` in the top folder.
