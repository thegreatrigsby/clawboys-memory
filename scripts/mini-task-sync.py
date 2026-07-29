#!/usr/bin/env python3
"""
Mini PC Task Sync — polls GitHub for tasks, executes them, pushes results back.
Runs on the Mini PC. Polls every 30 seconds.
"""
import json
import os
import time
import subprocess
from pathlib import Path
from datetime import datetime, timezone

# CONFIG — adjust these for the Mini PC
REPO_DIR = Path(r"C:\Users\thegr\Documents\ClawBoys-Bridge\shared-memory")
BRIDGE_DIR = Path(r"C:\Users\thegr\Documents\ClawBoys-Bridge")
INCOMING_DIR = REPO_DIR / "tasks" / "incoming"
COMPLETED_DIR = REPO_DIR / "tasks" / "completed"
HEARTBEAT_FILE = REPO_DIR / "tasks" / "heartbeat" / "mini-pc.json"
LOCAL_INCOMING = BRIDGE_DIR / "incoming"
LOCAL_OUTGOING = BRIDGE_DIR / "outgoing"
LOCAL_PROCESSED = BRIDGE_DIR / "processed"

POLL_INTERVAL = 30  # seconds

LOG_FILE = BRIDGE_DIR / "mini-sync.log"

def log(msg):
    line = f"[{datetime.now(timezone.utc).strftime('%H:%M:%S')}] [MINI-SYNC] {msg}"
    print(line)
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except:
        pass

def git_pull():
    """Pull latest tasks from GitHub."""
    os.chdir(REPO_DIR)
    result = subprocess.run(
        ["git", "pull", "origin", "main"],
        capture_output=True, text=True, timeout=30
    )
    if result.returncode != 0:
        log(f"git pull failed: {result.stderr[:200]}")
        return False
    return True

def git_push():
    """Push results to GitHub."""
    os.chdir(REPO_DIR)
    subprocess.run(["git", "add", "."], capture_output=True, timeout=30)
    result = subprocess.run(
        ["git", "commit", "-m", f"Mini PC sync {datetime.now(timezone.utc).isoformat()}"],
        capture_output=True, text=True, timeout=30
    )
    # Commit may fail if nothing changed — that's OK
    result = subprocess.run(
        ["git", "push", "origin", "main"],
        capture_output=True, text=True, timeout=30
    )
    if result.returncode != 0:
        log(f"git push failed: {result.stderr[:200]}")
        return False
    return True

def update_heartbeat():
    """Write heartbeat to show Mini PC is alive."""
    data = {
        "agent": "mini",
        "status": "alive",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "version": "1.0"
    }
    HEARTBEAT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(HEARTBEAT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def find_new_tasks():
    """Find tasks in incoming/ that haven't been processed."""
    tasks = []
    if not INCOMING_DIR.exists():
        return tasks
    for f in INCOMING_DIR.glob("*.json"):
        try:
            with open(f, "r", encoding="utf-8") as fh:
                task = json.load(fh)
            if task.get("agent") == "mini" and task.get("status") == "pending":
                tasks.append((f, task))
        except Exception as e:
            log(f"Bad task file {f.name}: {e}")
    return tasks

def mark_task_claimed(task_file, task):
    """Mark task as claimed so other agents don't grab it."""
    task["status"] = "claimed"
    task["claimed_by"] = "mini"
    task["claimed_at"] = datetime.now(timezone.utc).isoformat()
    with open(task_file, "w", encoding="utf-8") as f:
        json.dump(task, f, indent=2)

def create_local_task(task):
    """Create a local bridge file for the dispatcher to process."""
    task_id = task["id"]
    local_file = LOCAL_INCOMING / f"mini-{task_id}.txt"
    content = task.get("task", "")
    # Write in bridge format: prefix + task
    with open(local_file, "w", encoding="utf-8") as f:
        f.write(f"mini: {content}\n")
    log(f"Created local task: {local_file.name}")
    return local_file

def wait_for_result(task_id, timeout=120):
    """Wait for dispatcher to process the task and write a reply."""
    start = time.time()
    while time.time() - start < timeout:
        # Check outgoing for reply
        for f in LOCAL_OUTGOING.glob(f"*mini-{task_id}*"):
            return f
        # Also check if file moved to processed
        for f in LOCAL_PROCESSED.glob(f"mini-{task_id}*"):
            # Read any reply in outgoing that might match
            for out in LOCAL_OUTGOING.glob(f"*mini*{task_id}*"):
                return out
        time.sleep(2)
    return None

def read_result_file(result_file):
    """Read the result from the outgoing file."""
    try:
        with open(result_file, "r", encoding="utf-8") as f:
            return f.read().strip()
    except:
        return "[no result]"

def write_completed_result(task, result_text):
    """Write result back to GitHub tasks/completed/."""
    result = {
        "id": task["id"],
        "agent": "mini",
        "result": result_text,
        "completed_at": datetime.now(timezone.utc).isoformat(),
        "status": "completed"
    }
    result_file = COMPLETED_DIR / f"result-{task['id']}.json"
    result_file.parent.mkdir(parents=True, exist_ok=True)
    with open(result_file, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)
    log(f"Wrote result: {result_file.name}")

def process_task(task_file, task):
    """Full task processing pipeline."""
    task_id = task["id"]
    log(f"Processing task: {task_id}")
    
    # 1. Mark as claimed
    mark_task_claimed(task_file, task)
    
    # 2. Create local bridge file
    create_local_task(task)
    
    # 3. Wait for dispatcher to process
    result_file = wait_for_result(task_id, timeout=120)
    
    if result_file:
        result_text = read_result_file(result_file)
        log(f"Got result: {result_text[:100]}")
    else:
        result_text = "[timeout — no reply from dispatcher]"
        log(f"Task {task_id} timed out")
    
    # 4. Write result to completed/
    write_completed_result(task, result_text)
    
    # 5. Push to GitHub
    git_push()
    
    log(f"Task {task_id} complete")

def main():
    log("=" * 50)
    log("Mini PC Task Sync started")
    log(f"Repo: {REPO_DIR}")
    log(f"Poll interval: {POLL_INTERVAL}s")
    log("=" * 50)
    
    while True:
        try:
            # Update heartbeat
            update_heartbeat()
            
            # Pull latest from GitHub
            git_pull()
            
            # Find new tasks
            tasks = find_new_tasks()
            if tasks:
                log(f"Found {len(tasks)} new task(s)")
                for task_file, task in tasks:
                    process_task(task_file, task)
            else:
                log("No new tasks")
            
            # Push heartbeat update
            git_push()
            
        except Exception as e:
            log(f"Error: {str(e)}")
        
        time.sleep(POLL_INTERVAL)

if __name__ == "__main__":
    main()
