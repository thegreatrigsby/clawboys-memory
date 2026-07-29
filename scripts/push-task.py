#!/usr/bin/env python3
"""
One-shot task pusher — push a single mini: task to GitHub immediately.
Use this to avoid race conditions with the dispatcher.
"""
import json
import os
import subprocess
import sys
from pathlib import Path
from datetime import datetime, timezone

REPO_DIR = Path(r"C:\Users\thegr\Documents\ClawBoys-Bridge\shared-memory")
TASKS_INCOMING = REPO_DIR / "tasks" / "incoming"

def git_pull():
    os.chdir(REPO_DIR)
    subprocess.run(["git", "pull", "origin", "main"], capture_output=True, timeout=30)

def git_push():
    os.chdir(REPO_DIR)
    subprocess.run(["git", "add", "."], capture_output=True, timeout=30)
    subprocess.run(["git", "commit", "-m", "Task push"], capture_output=True, timeout=30)
    subprocess.run(["git", "push", "origin", "main"], capture_output=True, timeout=30)

def push_task(task_text, task_id=None):
    git_pull()
    if task_id is None:
        task_id = f"task-{int(datetime.now(timezone.utc).timestamp())}"
    task = {
        "id": task_id,
        "agent": "mini",
        "task": task_text,
        "created_by": "desktop",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "status": "pending"
    }
    task_file = TASKS_INCOMING / f"{task_id}.json"
    task_file.parent.mkdir(parents=True, exist_ok=True)
    with open(task_file, "w", encoding="utf-8") as f:
        json.dump(task, f, indent=2)
    git_push()
    print(f"Pushed task: {task_id}")
    return task_id

if __name__ == "__main__":
    if len(sys.argv) > 1:
        task_text = sys.argv[1]
    else:
        task_text = input("Task text: ")
    push_task(task_text)
