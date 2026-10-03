"""
Lab 9 - Task 2 (at home): check that the RL libraries work on MY laptop, not just in Colab.
Run from a terminal in this folder:   python screenshot_demo_gym_check.py
One screen of output = one easy screenshot for the worklog.

It checks the imports, makes the 3 environments used in the lab, then trains a quick
tabular Q-learning agent on Taxi-v4 (same update rule as my notebook) for 2000 episodes.
"""
import os
import platform
import sys
import time

os.environ.setdefault("SDL_AUDIODRIVER", "dummy")    # pygame: no sound card needed
import warnings
warnings.filterwarnings("ignore")

print("=" * 62)
print(" COS30018 Lab 9 - Task 2: local RL setup check")
print("=" * 62)
print(f"Python      : {sys.version.split()[0]}  ({platform.system()} {platform.release()})")

missing = []
for pkg, mod_name in [("gymnasium", "gymnasium"), ("numpy", "numpy"), ("pandas", "pandas"),
                      ("matplotlib", "matplotlib"), ("tqdm", "tqdm"), ("pygame", "pygame")]:
    try:
        mod = __import__(mod_name)
        print(f"{pkg:<12}: {getattr(mod, '__version__', 'ok')}")
    except ImportError:
        print(f"{pkg:<12}: NOT INSTALLED")
        missing.append(pkg)
if missing:
    print("-" * 62)
    print('fix: pip install "gymnasium[classic-control,toy-text]" numpy pandas matplotlib tqdm')
    sys.exit(1)

import numpy as np
import gymnasium as gym

print("-" * 62)
for env_id in ["Taxi-v4", "CartPole-v1", "CliffWalking-v1"]:
    env = gym.make(env_id, render_mode="rgb_array")
    obs, _ = env.reset(seed=42)
    frame = env.render()
    sp = env.observation_space
    space = f"Discrete({sp.n})" if hasattr(sp, "n") else f"Box{sp.shape} (continuous)"
    print(f"{env_id:<16} observations {space:<22} actions {env.action_space.n} | render {frame.shape}")
    env.close()

print("-" * 62)
print("Training tabular Q-learning on Taxi-v4 (2000 episodes)...")
env = gym.make("Taxi-v4")
Q = np.zeros((env.observation_space.n, env.action_space.n))
alpha, gamma, eps = 0.5, 0.99, 0.25
rng = np.random.default_rng(42)
rewards = []
t0 = time.time()
for ep in range(2000):
    s, _ = env.reset(seed=int(rng.integers(1_000_000)))
    total, done = 0.0, False
    while not done:
        a = int(rng.integers(env.action_space.n)) if rng.random() < eps else int(Q[s].argmax())
        ns, r, terminated, truncated, _ = env.step(a)
        # Q(s,a) := (1 - alpha) * Q(s,a) + alpha * (r + gamma * max_a' Q(s',a'))
        Q[s, a] = (1 - alpha) * Q[s, a] + alpha * (r + gamma * Q[ns].max() * (not terminated))
        s, total, done = ns, total + r, terminated or truncated
    rewards.append(total)
    eps *= 0.995
    if (ep + 1) % 500 == 0:
        print(f"  episode {ep + 1:>4}: mean reward of last 100 = {np.mean(rewards[-100:]):6.1f}")
print(f"done in {time.time() - t0:.1f}s - final mean reward {np.mean(rewards[-100:]):.1f} (>= 4.5 = solved)")
print("-" * 62)
print("Gymnasium works locally - ready for Lab 9!")
