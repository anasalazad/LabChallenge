# Lab 4 screenshots go here

Save each one with the name below (only the number at the start has to be exact; .png or .jpg; a long one can be split into `4.xa_…` + `4.xb_…`). Then, from the repo folder:

```bash
python _tools/insert_screenshots.py 4
```

**Never let an API key / token show in a screenshot.**

| File name | What to capture |
|---|---|
| `4.1_venv_install.png` | **Terminal – Python 3.12 environment + install** – the terminal showing `python --version` (3.12.x) inside `.venv-autogen` and the end of `pip install -r requirements.txt yfinance` ('Successfully installed …'). |
| `4.2_config_fix.png` | **My fix – CONFIG_LIST.json + agent.py** – VS Code with `CONFIG_LIST.json` (the `base_url` line, key still 'Your API Key') and the `(my fix)` lines in `agent.py`. Two shots are fine: `4.2a_…` + `4.2b_…`. |
| `4.3_app_running.png` | **Terminal – python app.py** – the terminal after `python app.py`: 'Running on local URL: http://0.0.0.0:7868'. |
| `4.4_example_sum.png` | **Browser – example 1 (sum of two numbers)** – http://127.0.0.1:7868 after clicking the first example: the assistant's code, the userproxy's 'exitcode: 0' and the final answer. |
| `4.5_example_product.png` | **Browser – example 2 (follow-up)** – the reply to 'what if the production of two numbers?' (it should use multiplication). |
| `4.6_example_stock_chart.png` | **Browser – example 3 + 4 (stock chart)** – the reply to the stock-price example and then 'show file: stock_price.png' with the chart shown in the chat. Two shots are fine: `4.6a_…` + `4.6b_…`. |
| `4.7_run_examples.png` | **Terminal – run_examples.py** – the end of `python run_examples.py`: the '--> … s \| … messages \| code run …' line of each example and 'saved …'. |
| `4.8_groupchat.png` | **Terminal – groupchat_demo.py (extension)** – the output of `python groupchat_demo.py`: 'Next speaker: critic', the critic's APPROVED (or its comments), the executor's exit code and the summary line at the end. |

Step-by-step: `START_HERE_Labs1-4_click_by_click.pdf` in the top folder.
