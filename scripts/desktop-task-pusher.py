#!/usr/bin/env python3
"""
Desktop PC Task Pusher — pushes mini: tasks to GitHub for Mini PC to pick up.
Runs on the Desktop PC.
"""
import json
import os
import time
import subprocess
import re
from pathlib import Path
from datetime import datetime, timezone

REPO_DIR = Path(r"C:\Users\thegr\Documents\ClawBoys-Bridge\shared-memory")
BRIDGE_DIR = Path(r"C:\Users\thegr\Documents\ClawBoys-Bridge")
TASKS_INCOMING = REPO_DIR / "tasks" / "incoming"
BRIDGE_INCOMING = BRIDGE_DIR / "incoming"

LOG_FILE = BRIDGE_DIR / "desktop-task-pusher.log"

def log(msg):
    line = f"[{datetime.now(timezone.utc).strftime('%H:%M:%S')}] [TASK-PUSHER] {msg}"
    print(line)
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except:
        pass

def git_pull():
    os.chdir(REPO_DIR)
    result = subprocess.run(
        ["git", "pull", "origin", "main"],
        capture_output=True, text=True, timeout=30
    )
    return result.returncode == 0

def git_push():
    os.chdir(REPO_DIR)
    subprocess.run(["git", "add", "."], capture_output=True, timeout=30)
    subprocess.run(
        ["git", "commit", "-m", f"Desktop task push {datetime.now(timezone.utc).isoformat()}"],
        capture_output=True, text=True, timeout=30
    )
    result = subprocess.run(
        ["git", "push", "origin", "main"],
        capture_output=True, text=True, timeout=30
    )
    return result.returncode == 0

def find_mini_tasks():
    """Find bridge files prefixed with 'mini:' in incoming/."""
    tasks = []
    for f in BRIDGE_INCOMING.glob("*.txt"):
        try:
            with open(f, "r", encoding="utf-8") as fh:
                content = fh.read().strip()
            if content.lower().startswith("mini:"):
                task_text = content[5:].strip()
                tasks.append((f, task_text))
        except:
            pass
    return tasks

def push_task_to_github(task_text, source_file):
    """Create a JSON task in GitHub repo."""
    task_id = f"{source_file.stem}-{int(time.time())}"
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
    log(f"Pushed task: {task_id}")
    return task_id

def move_to_processed(source_file):
    """Move the original bridge file to processed/."""
    processed_dir = BRIDGE_DIR / "processed"
    processed_dir.mkdir(exist_ok=True)
    dest = processed_dir / source_file.name
    source_file.rename(dest)
    log(f"Moved {source_file.name} to processed/")

def main():
    log("=" * 50)
    log("Desktop Task Pusher started")
    log("=" * 50)
    
    while True:
        try:
            # Pull latest from GitHub
            git_pull()
            
            # Find mini: tasks
            tasks = find_mini_tasks()
            if tasks:
                log(f"Found {len(tasks)} mini: task(s) to push")
                for source_file, task_text in tasks:
                    push_task_to_github(task_text, source_file)
                    move_to_processed(source_file)
                
                # Push to GitHub
                git_push()
            else:
                log("No mini: tasks found")
                
        except Exception as e:
            log(f"Error: {str(e)}")
        
        time.sleep(10)  # Check every 10 seconds

if __name__ == "__main__":
    main()
