# Lab 9 (Week 9) – what's left for you, Anas

**Topic:** Reinforcement learning with Gymnasium – Q-learning (Taxi, CartPole) + my extra: Expected Value SARSA on CliffWalking
**Task 1 (in class):** complete the notebook ✅ done · **Task 2 (at home):** install the libraries on your own laptop and run it there ⬜ yours
**Worklog:** `Lab 9/Lab9_Worklog_Week9.docx` (7/11 checklist items done)
**Time you still need:** about 40 min

---

## ✅ Already done for you

| What | File |
|---|---|
| **Task 1:** every `<YOUR CODE HERE>` filled in (`get_value`, `update`, `get_best_action`, `get_action`, `play_and_train`, the `Discretizer`, ε decay) and the whole notebook run: Taxi passes the assert (7.78 ≥ 4.5), CartPole ewma 135.9 (target ≥ 50) | `Lab_Week 9.ipynb` |
| Extras in the same notebook (cells marked *(my addition)*): watch the trained taxi, greedy CartPole test, **EV-SARSA vs Q-learning on CliffWalking** | `Lab_Week 9.ipynb` |
| Task 2 helper: one-screen local check (versions + the 3 envs + trains a Taxi agent in ~1 s) | `screenshot_demo_gym_check.py` |
| Plots for the worklog | `figures/9_*.png` |
| The worklog | `Lab9_Worklog_Week9.docx` |

## ⬜ What you need to do

### Step 1 – Task 1 in Google Colab (≈10 min) → screenshots 9.1–9.4
1. <https://colab.research.google.com> → **File → Upload notebook** → `Lab 9/Lab_Week 9.ipynb`.
2. **Runtime → Run all.** The first cell installs gymnasium + Colab display stuff (~1 min); the whole thing takes a few minutes (CartPole's 10,000 episodes are the slow bit).
3. Take:
   - 📸 **9.1** – the `QLearningAgent` cell, scrolled so my filled-in `<YOUR CODE HERE>` blocks are visible. It's long, so two shots are fine: `9.1a_…` (`get_value` + `update`) and `9.1b_…` (`get_best_action` + `get_action`).
   - 📸 **9.2** – the Taxi training cell (reward plot, **no AssertionError** under it) + the next cell's output (`mean reward of the last 100 episodes: 7.78 …`).
   - 📸 **9.3** – the `Discretizer` cell (my per-dimension digits) + the CartPole training plot + the *"How did it go?"* output (`ewma@100 at the end: 135.9`).
   - 📸 **9.4** – the CliffWalking benchmark plot + the two `Q-learning … / EV-SARSA …` lines + the greedy-path picture.

   *(Colab may give slightly different numbers than mine if its gymnasium version differs – that's fine, the checks just need to pass.)*

### Step 2 – Task 2 at home: run it on your laptop (≈20 min) → screenshots 9.5, 9.6
Open a terminal in the repo folder (activate your `.venv` if you made one – see the main `Anas.md`):
```bash
pip install "gymnasium[classic-control,toy-text]" numpy pandas matplotlib tqdm notebook
cd "Lab 9"
python screenshot_demo_gym_check.py
```
📸 **9.5** – the end of the pip install + the whole output of the check script, down to *"Gymnasium works locally - ready for Lab 9!"*.

Then run the notebook locally:
```bash
jupyter notebook
```
→ open `Lab_Week 9.ipynb` → **Kernel → Restart & Run All**.
- On Windows/Mac the first cell may print something like *"bash: ../xvfb: No such file or directory"* or *"'bash' is not recognized"* – **ignore it**, it's a Colab-only display trick and isn't needed (the notebook renders to images).

📸 **9.6** – the notebook in your browser with the address bar showing `localhost:8888`, scrolled to the finished Taxi training cell.

### Step 3 – screenshots into the worklog + final touches
1. Save screenshots in **`Lab 9/screenshots/`** with the names below.
2. `python _tools/insert_screenshots.py 9`
3. Tick the checklist: click the boxes in Word or `python _tools/tick_checklist.py 9 8 9 10 11`
4. In Word: **Student ID**, check the **dates** (8–14 Oct 2026), adjust **TIME SPENT**.

---

## 📸 Screenshot list (Lab 9)

| # | Where | Exactly what to capture | Save as |
|---|---|---|---|
| 9.1 | `Lab_Week 9.ipynb` – `QLearningAgent` cell | my `<YOUR CODE HERE>` blocks (can be 9.1a + 9.1b) | `screenshots/9.1_qlearning_code.png` |
| 9.2 | Taxi training cell + next cell | reward plot, no AssertionError, mean reward 7.78 | `screenshots/9.2_taxi_training.png` |
| 9.3 | Discretizer + CartPole training + "How did it go?" | my discretizer, the plot, ewma 135.9 | `screenshots/9.3_cartpole_training.png` |
| 9.4 | the last 3 cells (CliffWalking) | benchmark plot, the 2 reward lines, greedy paths | `screenshots/9.4_evsarsa_vs_qlearning.png` |
| 9.5 | your terminal | pip install + `python screenshot_demo_gym_check.py` output | `screenshots/9.5_local_gym_check.png` |
| 9.6 | Jupyter on your laptop | notebook at `localhost:8888`, Taxi cell finished | `screenshots/9.6_local_jupyter_run.png` |

---

## 🧠 Know your stuff (2-minute revision)
- **RL loop:** the agent picks an action → the environment returns the next observation + reward → repeat. Gymnasium API: `env = gym.make(...)`, `obs, info = env.reset()`, `obs, reward, terminated, truncated, info = env.step(action)`. *terminated* = the task really ended, *truncated* = time limit.
- **Q-learning update:** `Q(s,a) ← (1−α)·Q(s,a) + α·(r + γ·max_a' Q(s',a'))`. α = learning rate, γ = discount (how much future reward counts).
- **ε-greedy:** with probability ε take a random action (explore), otherwise the best one (exploit); decay ε over time.
- **Taxi:** 500 discrete states → a table works directly (7.78 mean reward, delivers the passenger in 10 steps).
- **CartPole:** continuous observations → round them into bins (discretize) so a table works. Too fine = too many states, too coarse = can't tell states apart. I used digits `[0, 1, 2, 1]` (pole angle needs more detail) → ewma 135.9.
- **Off- vs on-policy (my extra):** Q-learning learns the optimal path (along the cliff edge) but falls off while exploring (−104.6); EV-SARSA learns the value of the policy it actually follows → safer path, better online reward (−30.5).

> Heads-up: a lot of this was prepared with an AI assistant. Make sure you can explain the code you're handing in (especially the 5 filled-in functions) in your own words, and check your unit's rules on AI use (add an acknowledgement if they ask for one).
