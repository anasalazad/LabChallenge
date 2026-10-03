# Lab 2 screenshots go here

Save each one with the name below (only the number at the start has to be exact; .png or .jpg; a long one can be split into `2.xa_…` + `2.xb_…`). Then, from the repo folder:

```bash
python _tools/insert_screenshots.py 2
```

**Never let a token show in a screenshot** – take the notebook shots from `Lab2_completed.ipynb` (the copy without the HF token).

| File name | What to capture |
|---|---|
| `2.1_hf_token.png` | **Hugging Face – my access token** – huggingface.co → Settings → Access Tokens with your (new) token in the list – the value is hidden. Not the pop-up that shows the full token. |
| `2.2_no_tools.png` | **Notebook – cloud agent, no tools** – the sum of 1 to 50 run: the 'New run' box, Step 1 (the formula code + 1275.0), Step 2 (final_answer) and the 1275.0 printed at the end. |
| `2.3_web_search.png` | **Notebook – web search, 3 cycles** – the Melbourne run: Step 1 with `web_search(...)` + the start of its search results, then Steps 2 and 3 with 795000. Two shots are fine: `2.3a_…` + `2.3b_…`. |
| `2.4_memory.png` | **Notebook – agent.memory.steps** – the memory cell: the `TaskStep(...)` line and the start of the `ActionStep(step_number=1, timing=…` lines. |
| `2.5_local_model.png` | **Notebook – local model stuck** – the local run: Step 1 (105 s) and a couple of the 'Error in code parsing' steps with their durations. Two shots are fine: `2.5a_…` + `2.5b_…`. |
| `2.6_cloud_vs_local_402.png` | **Notebook – cloud vs local, 402 error** – the `run_and_time` cell and its '402 Payment Required … depleted your monthly included credits' error. |
| `2.7_gradio_ui.png` | **GradioUI chat** – the GradioUI page at http://127.0.0.1:7860 with your message (and the reply or the error). |
| `2.8_checkpoint.png` | **Notebook – checkpoint answers** – the 'Checkpoint questions' cell at the end of the notebook. |
