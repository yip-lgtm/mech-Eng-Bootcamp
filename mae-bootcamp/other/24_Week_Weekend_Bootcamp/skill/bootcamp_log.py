"""
Bootcamp Log Skill
Quick progress logger — appends to progress_log.txt AND optionally updates progress.md.

Usage:
  python3 bootcamp_log.py "Week 3 Done: MAEG3050 + improved PID + force feedback"
  python3 bootcamp_log.py --week 3 --courses MAEG3050,MAEG2020 --sim "PID tuning" --feeling 8
  python3 bootcamp_log.py --quick "Quick note about Week 3"
"""
import datetime
import json
import os
import sys


# Log file path
LOG_FILE = "/app/data-intelligence-architect/ire-bootcamp/24_Week_Weekend_Bootcamp/progress_log.txt"
PROGRESS_MD = "/app/data-intelligence-architect/ire-bootcamp/24_Week_Weekend_Bootcamp/progress.md"
BOOTCAMP_START = datetime.date(2026, 6, 13)
TOTAL_WEEKS = 24


def get_current_week(today=None):
    """Calculate current bootcamp week number (1-24)"""
    if today is None:
        today = datetime.date.today()
    days_elapsed = (today - BOOTCAMP_START).days
    week_num = (days_elapsed // 7) + 1
    if week_num < 1:
        return 0, "not_started"
    if week_num > TOTAL_WEEKS:
        return TOTAL_WEEKS + 1, "completed"
    return week_num, "active"


def log_to_file(log_text, week_num=None):
    """Append to progress_log.txt"""
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if week_num:
        full_log = f"[{timestamp}] [Week {week_num}] {log_text}\n"
    else:
        full_log = f"[{timestamp}] {log_text}\n"
    
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(full_log)
    return True


def update_progress_md(week_num, status="✅", notes=""):
    """Update a specific week's row in progress.md"""
    if not os.path.exists(PROGRESS_MD):
        return False, "progress.md not found"
    
    import re
    with open(PROGRESS_MD, 'r', encoding='utf-8') as f:
        content = f.read()
    
    pattern = re.compile(
        rf'(\|\s*{week_num}\s*\|\s*\d{{4}}-\d{{2}}-\d{{2}}\s*\|[^|]*\|[^|]*\|[^|]*\|\s*)(⬜|🟡|✅)(\s*\|\s*)([^|\n]*)',
        re.MULTILINE
    )
    
    new_content, count = pattern.subn(f"\\1{status}\\3{notes}", content)
    
    if count == 0:
        return False, f"Week {week_num} row not found"
    
    with open(PROGRESS_MD, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    return True, f"Updated Week {week_num}"


def show_usage():
    print("""📝 **Bootcamp Log** - Quick progress logger

**Usage:**
```
# Quick mode (just log to file):
python3 bootcamp_log.py "Week 3 Done: MAEG3050 + improved PID"

# Detailed mode (update progress.md too):
python3 bootcamp_log.py --week 3 --courses MAEG3050,MAEG2020 \\
  --sim "PID tuning" --blocker "math heavy" --feeling 8

# Show recent logs:
python3 bootcamp_log.py --show
```""")


def show_recent_logs(n=10):
    """Show the most recent log entries"""
    if not os.path.exists(LOG_FILE):
        print("📭 No logs yet")
        return
    
    with open(LOG_FILE, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    recent = lines[-n:] if len(lines) > n else lines
    print(f"📜 **最近 {len(recent)} 條 logs:**\n")
    for line in recent:
        print(line.rstrip())


def main():
    if len(sys.argv) < 2:
        show_usage()
        return
    
    # Parse args
    args = sys.argv[1:]
    
    # Show recent logs
    if '--show' in args:
        show_recent_logs()
        return
    
    # Quick mode: just text
    if not any(arg.startswith('--') for arg in args):
        log_text = ' '.join(args)
        week_num, _ = get_current_week()
        log_to_file(log_text, week_num)
        print(f"✅ 已記錄: {log_text}")
        if week_num >= 1:
            print(f"📅 (Week {week_num})")
        return
    
    # Detailed mode
    week = None
    courses = ""
    simulator = ""
    blocker = ""
    feeling = ""
    status = "✅"
    
    i = 0
    while i < len(args):
        arg = args[i]
        if arg == '--week' and i + 1 < len(args):
            week = int(args[i + 1])
            i += 2
        elif arg == '--courses' and i + 1 < len(args):
            courses = args[i + 1]
            i += 2
        elif arg == '--sim' and i + 1 < len(args):
            simulator = args[i + 1]
            i += 2
        elif arg == '--blocker' and i + 1 < len(args):
            blocker = args[i + 1]
            i += 2
        elif arg == '--feeling' and i + 1 < len(args):
            feeling = args[i + 1]
            i += 2
        elif arg == '--status' and i + 1 < len(args):
            status = args[i + 1]
            i += 2
        else:
            i += 1
    
    if week is None:
        week, _ = get_current_week()
        if week < 1 or week > TOTAL_WEEKS:
            print(f"⚠️  No active week (current: {week}). Use --week N")
            return
    
    # Build log text
    note_parts = []
    if courses:
        note_parts.append(f"Courses: {courses}")
    if simulator:
        note_parts.append(f"Sim: {simulator}")
    if blocker:
        note_parts.append(f"Block: {blocker}")
    if feeling:
        note_parts.append(f"Feel: {feeling}/10")
    
    log_text = " | ".join(note_parts)
    if not log_text:
        log_text = f"Week {week} logged"
    
    # Log to file
    log_to_file(log_text, week)
    print(f"✅ Logged: {log_text}")
    
    # Update progress.md
    if status and note_parts:
        success, msg = update_progress_md(week, status=status, notes=" | ".join(note_parts))
        if success:
            print(f"📝 Updated progress.md: {msg}")
        else:
            print(f"⚠️  {msg}")


if __name__ == "__main__":
    main()
