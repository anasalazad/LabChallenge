# Lab 2 screenshots go here

Save each one with the name below (only the number at the start has to be exact; .png or .jpg; a long one can be split into `2.xa_…` + `2.xb_…`). Then, from the repo folder:

```bash
python _tools/insert_screenshots.py 2
```

**Never let an API key / token show in a screenshot.**

| File name | What to capture |
|---|---|
| `2.1_hf_token.png` | **Hugging Face – my access token** – huggingface.co → Settings → Access Tokens with your token in the list (the value is hidden – good). Don't screenshot the pop-up that shows the full token. |
| `2.2_pip_install.png` | **Terminal – installing smolagents** – the end of `pip install "smolagents[toolkit]" "smolagents[transformers]"` ('Successfully installed …'). |
| `2.3_no_tools.png` | **Notebook – cloud agent, no tools** – the step 2 output: the 'New run' box, Step 1 / Step 2 with the code, 'Final answer: 1275' and the small step table. |
| `2.4_web_search.png` | **Notebook – web search, two steps** – the step 3 log: Step 1 with `web_search(...)` + its Execution logs, and Step 2 with the 15% maths + 'Final answer'. Two shots are fine: `2.4a_…` + `2.4b_…`. |
| `2.5_memory.png` | **Notebook – agent.memory.steps** – the step 4 output (TaskStep / ActionStep lines + the 'what smolagents records' line) and the follow-up's last line ('searched again: False …'). |
| `2.6_local_model.png` | **Notebook – local model (TransformersModel)** – the step 5 output: 'loaded Qwen/… in … s', the steps and the final answer (or the error if it failed). |
| `2.7_cloud_vs_local.png` | **Notebook – cloud vs local** – the step 6 'Cloud: …s' / 'Local: …s' lines and the comparison table under them. |
| `2.8_gradio_ui.png` | **GradioUI chat in the browser** – http://127.0.0.1:7860 (or the link the notebook printed) after asking the agent something that needs a search – the steps and the final answer should be visible. |

Step-by-step: `START_HERE_Labs1-4_click_by_click.pdf` in the top folder.
