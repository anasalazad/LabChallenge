"""Helpers for weeks 1-4: fill the worklog text from the results file a notebook/script saved.

If the result isn't there yet (notebook not run), the text gets a yellow [[placeholder]] instead,
so it's obvious what's still missing. Re-run the notebook, then rebuild the worklog.
"""
import json
import os

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def load(rel_path):
    """Load Lab N/results/....json -> dict (empty dict if it doesn't exist yet)."""
    path = os.path.join(REPO_ROOT, rel_path)
    if not os.path.exists(path):
        return {}
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def get(data, dotted, default=None):
    """get(r, "sentiment.ollama.avg_s") -> value or default."""
    cur = data
    for key in dotted.split("."):
        if isinstance(cur, dict) and key in cur:
            cur = cur[key]
        elif isinstance(cur, list) and key.isdigit() and int(key) < len(cur):
            cur = cur[int(key)]
        else:
            return default
    return cur


def v(data, dotted, fmt="{}", placeholder="?"):
    """Formatted value, or a yellow [[placeholder]] if the notebook hasn't produced it yet."""
    val = get(data, dotted)
    if val is None:
        return f"[[{placeholder}]]"
    try:
        return fmt.format(val)
    except (ValueError, TypeError):
        return str(val)


def has(data, *dotted):
    return all(get(data, d) is not None for d in dotted)


def pct(x):
    return f"{x:.0%}"


def fig(rel_path, caption, width=6.0):
    """Optional figure - only added if the notebook already made it."""
    return {"path": rel_path, "caption": caption, "width": width, "optional": True}


def k(data, dotted, known, fmt="{}"):
    """Like v(), but for facts we already know for sure (e.g. the dataset size) - no yellow."""
    val = get(data, dotted)
    if val is None:
        return str(known)
    try:
        return fmt.format(val)
    except (ValueError, TypeError):
        return str(val)
