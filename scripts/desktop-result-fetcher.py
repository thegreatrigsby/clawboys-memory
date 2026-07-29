#!/usr/bin/env python3
"""
Desktop PC Result Fetcher — pulls Mini PC results from GitHub back to outgoing/.
Runs on the Desktop PC.
"""
import json
import os
import time
import subprocess
from pathlib import Path
from datetime import datetime, timezone

REPO_DIR = Path(r"C:\Users\thegr\Documents\ClawBoys-Bridge\shared-memory")
BRIDGE_DIR = Path(r"C:\Users\thegr\Documents\ClawBoys-Bridge")
COMPLETED_DIR = REPO_DIR / "tasks" / "completed"
BRIDGE_OUTGOING = BRIDGE_DIR / "outgoing"

# Track which results we've already fetched
FETCHED_LOG = BRIDGE_DIR / "fetched-results.log"

LOG_FILE = BRIDGE_DIR / "desktop-result-fetcher.log"

def log(msg):
    line = f"[{datetime.now(timezone.utc).strftime('%H:%M:%S')}] [RESULT-FETCHER] {msg}"
    print(line)
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except:
        pass

def load_fetched_ids():
    """Load list of already-fetched result IDs."""
    if not FETCHED_LOG.exists():
        return set()
    try:
        with open(FETCHED_LOG, "r", encoding="utf-8") as f:
            return set(line.strip() for line in f if line.strip())
    except:
        return set()

def save_fetched_id(result_id):
    """Mark a result as fetched."""
    with open(FETCHED_LOG, "a", encoding="utf-8") as f:
        f.write(result_id + "\n")

def git_pull():
    os.chdir(REPO_DIR)
    result = subprocess.run(
        ["git", "pull", "origin", "main"],
        capture_output=True, text=True, timeout=30
    )
    return result.returncode == 0

def find_new_results(fetched_ids):
    """Find completed results not yet fetched."""
    results = []
    if not COMPLETED_DIR.exists():
        return results
    for f in COMPLETED_DIR.glob("result-*.json"):
        try:
            with open(f, "r", encoding="utf-8") as fh:
                result = json.load(fh)
            rid = result.get("id", f.stem)
            if rid not in fetched_ids:
                results.append((f, result))
        except Exception as e:
            log(f"Bad result file {f.name}: {e}")
    return results

def write_to_outgoing(result):
    """Write result to bridge outgoing/ folder."""
    task_id = result.get("id", "unknown")
    result_text = result.get("result", "[no result]")
    
    # Write in bridge reply format
    out_file = BRIDGE_OUTGOING / f"mini-result-{task_id}.txt"
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(f"=== Mini PC Result ===\n\n")
        f.write(f"Task ID: {task_id}\n")
        f.write(f"Result: {result_text}\n")
        f.write(f"Completed: {result.get('completed_at', '?')}\n")
    log(f"Wrote result to outgoing/: {out_file.name}")

def main():
    log("=" * 50)
    log("Desktop Result Fetcher started")
    log("=" * 50)
    
    fetched_ids = load_fetched_ids()
    
    while True:
        try:
            # Pull latest from GitHub
            git_pull()
            
            # Find new results
            results = find_new_results(fetched_ids)
            if results:
                log(f"Found {len(results)} new result(s)")
                for result_file, result in results:
                    rid = result.get("id", result_file.stem)
                    write_to_outgoing(result)
                    save_fetched_id(rid)
                    fetched_ids.add(rid)
            else:
                log("No new results")
                
        except Exception as e:
            log(f"Error: {str(e)}")
        
        time.sleep(15)  # Check every 15 seconds

if __name__ == "__main__":
    main()
