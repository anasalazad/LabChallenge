# Week 9 worklog content - Lab 9 (Reinforcement learning with Gymnasium, Q-learning)
# Markup: **bold**, `code`. Edit text here, then: python _tools/build_worklogs.py 9

SPEC = {
    "week": 9,
    "dates": "8-14 October 2026",
    "student_name": "Anas Al Azad",
    "student_id": "",
    "title": "Week 9 – Reinforcement learning with Gymnasium (Q-learning)",
    "intro": "My checklist for this week – ticked = done (the completed notebook, plots and scripts are "
             "in the **Lab 9** folder of my repo), unticked = still on my to-do list.",
    "checklist": [
        ("Read the Week 9 tutorial (Gymnasium API: `make` / `reset` / `step`, terminated vs truncated, "
         "built-in environments)", True),
        ("Task 1: filled in `QLearningAgent` – `get_value`, `update`, `get_best_action`, "
         "`get_action` (ε-greedy)", True),
        ("Task 1: filled in `play_and_train`, trained on Taxi-v4 – passes the notebook's check "
         "(mean reward **7.78** ≥ 4.5)", True),
        ("Watched my trained taxi pick up and drop off the passenger (10 steps, reward 11)", True),
        ("CartPole: per-dimension discretizer + ε decay → ewma **135.9** (target ≥ 50)", True),
        ("Extra: Expected Value SARSA vs Q-learning on CliffWalking (with the notebook's "
         "`benchmark_agents` helper)", True),
        ("Task 2 prep: `requirements.txt` + `screenshot_demo_gym_check.py` for my laptop", True),
        ("Task 2: install gymnasium + friends on my laptop and run the check script", False),
        ("Task 2: run `Lab_Week 9.ipynb` locally in Jupyter (not Colab)", False),
        ("Task 1 (in class): run the notebook in Google Colab too", False),
        ("Add my screenshots (yellow boxes below)", False),
    ],
    "rows": [
        {
            "task": "RL + Gymnasium basics",
            "task_note": "Week 9 tutorial sheet",
            "did": [
                "Read about the agent / environment / reward loop and Gymnasium's standard API: "
                "`gym.make()`, `env.reset()`, `env.step(action)` → observation, reward, "
                "**terminated**, **truncated**, info.",
                "Looked at the 3 environments I used: Taxi-v4 (500 discrete states, 6 actions), "
                "CartPole (4 continuous numbers, 2 actions), CliffWalking (48 states, 4 actions).",
            ],
            "time": "1 h",
            "learning": [
                "Gymnasium is the maintained successor of OpenAI Gym – same API for every environment, "
                "so one agent works on all of them.",
                "terminated = the task really ended, truncated = cut off by a time limit.",
            ],
            "problems": [
                "The notebook text still says Taxi-v3 / OpenAI gym, but current Gymnasium only has "
                "**Taxi-v4**; CartPole-v0 also prints a “v0 is out of date” warning.",
            ],
        },
        {
            "task": "Task 1 – Q-learning agent",
            "task_note": "`Lab_Week 9.ipynb`, all the `<YOUR CODE HERE>` blocks",
            "did": [
                "`get_value`: V(s) = max over actions of Q(s, a).",
                "`update`: Q(s,a) ← (1 − α)·Q(s,a) + α·(r + γ·V(s')).",
                "`get_best_action`: the action with the highest Q(s, a).",
                "`get_action`: ε-greedy – random action with probability ε, otherwise the best one.",
                "`play_and_train`: `a = agent.get_action(s)` then `agent.update(s, a, r, next_s)`.",
            ],
            "time": "1.5 h",
            "learning": [
                "Q-learning is a temporal-difference method: it updates its guess from its own next "
                "guess (bootstrapping), no model of the environment needed.",
                "ε balances exploring vs exploiting.",
            ],
            "problems": [
                "The hint warns that Q-values can be negative – starting a manual max at 0 would "
                "give a wrong V(s), so I used `max()` over the actual Q-values.",
                "Used `self.env.np_random` (as the tip says) instead of `random.random()`, otherwise "
                "`seed_everything` can't make the runs reproducible.",
            ],
        },
        {
            "task": "Taxi-v4",
            "task_note": "Task 1",
            "did": [
                "α = 0.5, γ = 0.99, ε = 0.25 shrinking ×0.99 per episode, 1000 episodes: "
                "mean reward of the last 100 = **7.78**, so the notebook's assert (≥ 4.5) passes; "
                "visited 404 of the 500 states (Fig 9.1).",
                "Watched the greedy agent with `visualize_agent`: drives to the passenger, picks them up "
                "and drops them off in **10 steps, total reward 11** (Fig 9.2).",
            ],
            "time": "0.5 h",
            "learning": [
                "Rewards: −1 per step, +20 for a correct drop-off, −10 for illegal pick-up/drop-off "
                "– so it learns the shortest route.",
            ],
            "problems": [
                "`visualize_agent` clears its cell's output while animating, so my print in the same cell "
                "disappeared – moved the print to its own cell.",
                "The setup cell's `!bash ../xvfb start` fails outside Colab (*No such file or directory*) "
                "– harmless, rendering uses `rgb_array` so no screen is needed.",
            ],
        },
        {
            "task": "CartPole (continuous → discrete)",
            "task_note": "Discretizer + training",
            "did": [
                "Plotted the observation histograms from 100k random steps, then changed the "
                "`Discretizer` so each dimension can have its own number of digits.",
                "Tried 6 settings: everything at 1 digit already beats 50 (ewma ≈ 103), too coarse "
                "`[0, 0, 1, 0]` only ≈ 20. Picked **`[0, 1, 2, 1]`** (pole angle only spans "
                "±0.2 so it needs 2 digits, cart position is fine as whole numbers) + ε ×0.999 "
                "per episode (min 0.01).",
                "Result: 4,696 states (inside the tip's 10³–10⁴), last-100 mean 105.1, "
                "**ewma 135.9** (target ≥ 50), best episode 7,664 steps; greedy test over 20 "
                "episodes: mean 755 steps (Fig 9.3).",
            ],
            "time": "1.5 h",
            "learning": [
                "Too fine = too many states to ever learn, too coarse = can't tell good states from bad.",
                "Decaying ε lets it exploit what it learned without stopping exploration completely.",
            ],
            "problems": [
                "Rewards are super noisy (episodes from ~10 to 7,000+ steps), so I judged by the ewma.",
                "The env is unwrapped (no 200-step limit), so training gets slower as the agent gets "
                "better – long episodes.",
            ],
        },
        {
            "task": "Extra – EV-SARSA vs Q-learning",
            "task_note": "CliffWalking-v1",
            "did": [
                "Wrote `EVSarsaAgent` (only `get_value` changes: expected Q under the ε-greedy policy "
                "instead of the max) and compared it with Q-learning using the notebook's unused "
                "`benchmark_agents` helper (3 seeds × 500 episodes).",
                "Average reward over the last 100 episodes: **Q-learning −104.6 vs EV-SARSA −30.5** "
                "(Fig 9.4).",
                "Greedy paths: Q-learning walks **right along the cliff edge** (13 steps), EV-SARSA one row "
                "further away (15 steps) (Fig 9.5).",
            ],
            "time": "1.5 h",
            "learning": [
                "Q-learning is **off-policy** (learns the optimal path but keeps falling off while still "
                "exploring); EV-SARSA is **on-policy** (learns the safer path for the policy it actually "
                "follows).",
            ],
            "problems": [
                "CliffWalking has no time limit, and the first episodes with an untrained agent wander for "
                "a long time (rewards around −2000), so the start of the plot is squashed.",
            ],
        },
        {
            "task": "Task 2 – at home",
            "task_note": "local install",
            "did": [
                "Made `requirements.txt` for the whole repo and `screenshot_demo_gym_check.py`: prints "
                "the versions, creates Taxi / CartPole / CliffWalking and trains a numpy Q-table on Taxi "
                "(≈ 1 s, mean reward 8.0).",
                "Still to do: install everything on my laptop, run the check script and the notebook "
                "in local Jupyter (screenshots 9.5, 9.6).",
            ],
            "time": "0.5 h",
            "learning": [
                "`pip install \"gymnasium[classic-control,toy-text]\"` pulls in pygame for rendering.",
            ],
            "problems": [],
        },
    ],
    "total_time": "6.5 h",
    "total_note": "+ ~40 min local install & screenshots",
    "screenshots_intro": "Figures 9.1–9.5 come straight out of my completed `Lab_Week 9.ipynb`. The yellow "
                         "boxes are screenshots I still need to add (9.1–9.4 from the notebook, 9.5–9.6 "
                         "from my laptop for Task 2).",
    "figures": [
        {"path": "Lab 9/figures/9_1_taxi_training.png", "width": 3.9,
         "caption": "Taxi-v4 training rewards (blue) and moving average (orange)"},
        {"path": "Lab 9/figures/9_2_taxi_trained_agent.png", "width": 3.6,
         "caption": "my trained taxi after dropping off the passenger – 10 steps, reward 11"},
        {"path": "Lab 9/figures/9_3_cartpole_training.png", "width": 3.9,
         "caption": "CartPole training with my discretizer (the notebook redraws every 1000 episodes – "
                    "final ewma 135.9)"},
        {"path": "Lab 9/figures/9_4_cliffwalking_benchmark.png", "width": 5.0,
         "caption": "Q-learning vs Expected Value SARSA on CliffWalking (mean of 3 seeds ± std)"},
        {"path": "Lab 9/figures/9_5_cliff_paths.png", "width": 6.2,
         "caption": "greedy paths: Q-learning hugs the cliff (red), EV-SARSA keeps one row away"},
    ],
    "screenshots": [
        {"id": "9.1", "title": "My completed Q-learning code",
         "what": "the `QLearningAgent` cell scrolled to my `<YOUR CODE HERE>` blocks (`get_value`, "
                 "`update`, `get_best_action`, `get_action`) – two shots 9.1a / 9.1b is fine.",
         "file": "Lab 9/screenshots/9.1_qlearning_code.png"},
        {"id": "9.2", "title": "Taxi training (Task 1)",
         "what": "the Taxi training cell with its reward plot and no AssertionError, plus the next cell's "
                 "output (mean reward of the last 100 episodes ≈ 7.78).",
         "file": "Lab 9/screenshots/9.2_taxi_training.png"},
        {"id": "9.3", "title": "CartPole with my discretizer",
         "what": "my `Discretizer` code + the training plot, and the “How did it go?” output "
                 "(ewma ≈ 135.9).",
         "file": "Lab 9/screenshots/9.3_cartpole_training.png"},
        {"id": "9.4", "title": "Extra – EV-SARSA vs Q-learning",
         "what": "the CliffWalking benchmark plot, the two average-reward lines and the greedy-path picture.",
         "file": "Lab 9/screenshots/9.4_evsarsa_vs_qlearning.png"},
        {"id": "9.5", "title": "Task 2 – libraries installed on my laptop",
         "what": "terminal: the end of the pip install + full output of "
                 "`python screenshot_demo_gym_check.py` down to “Gymnasium works locally”.",
         "file": "Lab 9/screenshots/9.5_local_gym_check.png"},
        {"id": "9.6", "title": "Task 2 – the notebook running locally",
         "what": "the notebook open in Jupyter on your laptop (address bar shows `localhost:8888`) with "
                 "the Taxi training cell finished.",
         "file": "Lab 9/screenshots/9.6_local_jupyter_run.png"},
    ],
}
