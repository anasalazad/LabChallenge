# Lab 9 (Week 9) – instructions for Claude (local session)

Continuing work from a cloud session. Read the repo-root `CLAUDE.md` first. This folder is **Lab 9** (reinforcement learning with Gymnasium; extract of Yandex Practical_RL week 3). Task 1 = fill in the notebook (done). **Task 2 = install the libraries on Anas's own machine and run it there – that's what's left, and you can help.**

## Files
| File | Status |
|---|---|
| `Lab_9.pdf` | lab sheet (read-only) |
| `Lab_Week 9.ipynb` | **Task 1 complete.** All `<YOUR CODE HERE>` blocks filled (QLearningAgent `get_value`/`update`/`get_best_action`/`get_action` using `self.env.np_random`, `play_and_train`, per-dimension `Discretizer`, ε decay `max(0.01, ε·0.999)`), `n_digits=[0, 1, 2, 1]`. Extra cells marked *(my addition)*: taxi stats + `visualize_agent`, CartPole greedy test, `EVSarsaAgent` + `benchmark_agents` on CliffWalking-v1 + greedy-path plot (saves `figures/9_5_cliff_paths.png`). Executed headless in the cloud (gymnasium 1.3.0). |
| `screenshot_demo_gym_check.py` | Task 2 one-screen check (versions, makes Taxi-v4/CartPole-v1/CliffWalking-v1, trains a numpy Q-table on Taxi) |
| `figures/9_1…9_5*.png` | extracted from the notebook's outputs (+ `9_3a` histograms, not used in the worklog) |
| `Lab9_Worklog_Week9.docx` | `_tools/build_worklogs.py` ← `_tools/worklog_content/week9.py`; 7/11 checklist items done |

Cloud results (deterministic, seeded through `seed_everything` + `env.np_random`): Taxi mean of last 100 = 7.78 (assert ≥ 4.5 passes), 404 states; CartPole 4,696 states, last-100 mean 105.1, ewma 135.9, best episode 7,664, greedy test mean 755.4; CliffWalking last-100 avg Q-learning −104.6 vs EV-SARSA −30.5; greedy paths 13 vs 15 steps.

## Remaining work you CAN do (Task 2)
1. Make sure the env exists (root `CLAUDE.md`): `pip install -r requirements.txt`, or just `pip install "gymnasium[classic-control,toy-text]" numpy pandas matplotlib tqdm notebook`.
2. `python "Lab 9/screenshot_demo_gym_check.py"` → should end with "Gymnasium works locally". If pygame/rendering fails on Linux without a display, set `SDL_VIDEODRIVER=dummy`.
3. Run the notebook locally to confirm Task 2: `cd "Lab 9" && jupyter nbconvert --to notebook --execute --inplace "Lab_Week 9.ipynb"` (takes ~1–2 min). Expected: no AssertionError, same numbers as above if gymnasium is 1.3.x. The first cell's `!bash ../xvfb start` prints an error outside Colab – harmless. Note `visualize_agent` uses `clear_output`, so only the final frame stays.
   - If numbers differ (different gymnasium version), update `_tools/worklog_content/week9.py` (+ the CliffWalking markdown cell in the notebook) and rebuild with `python _tools/build_worklogs.py 9` – unless the worklog was already edited by Anas (script refuses → edit the docx in place with python-docx; never `--force` over Anas's edits). Re-extract figures from the notebook outputs if you rebuild.
   - Anas still needs to run it in **their own** Jupyter for screenshot 9.6 (Task 2 evidence) – you can't take that screenshot.
4. **Screenshots:** `Lab 9/screenshots/9.1*` … `9.6*` (9.1 may be split into `9.1a_…`/`9.1b_…`) → `python _tools/insert_screenshots.py 9`.
5. **Checklist:** items 8–11 are Anas's → `python _tools/tick_checklist.py 9 <n>`.

## Only Anas can do
Running it in Google Colab and on their laptop for the screenshots, student ID, confirming dates/time spent.
