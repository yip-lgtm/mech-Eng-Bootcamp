# Bootcamp Sunday Summary Skill

> **Purpose:** Sunday 8:00 PM HKT reminder + auto-update progress.md
> **Trigger:** OpenClaw cron, every Sunday 20:00 HKT
> **Cron command:** See `CRON_SETUP.md`

## How It Works

1. Cron triggers `bootcamp_sunday_summary.py` on Sunday evening
2. Script calculates current week + phase
3. Sends formatted summary request to user
4. When user replies with summary, parses + auto-updates `progress.md`

## User Reply Format

```
Week N Done:
- Courses: MAEGxxxx, MAEGyyyy
- Simulator: 你更新咗咩
- Blocker: 有冇困難
- Feeling: 1-10分
```

## What It Updates

`progress.md` Week N row:
- Status: ⬜ → ✅ (or 🟡 for in-progress)
- Notes: adds `Courses: ... | Sim: ... | Block: ... | Feel: .../10`

## Manual Trigger

```python
import sys
sys.path.insert(0, '/app/skills')
from bootcamp_sunday_summary import generate_summary_prompt, parse_user_summary

# Show the prompt
print(generate_summary_prompt(1))

# Update when user replies
user_text = """
Week 1 Done:
- Courses: MAEG1020
- Simulator: Initial setup
- Feeling: 8
"""
success, msg = parse_user_summary(1, user_text)
print(msg)
```

## Output Example

```
📅【Week 1 Sunday Summary】

請用以下格式回覆我:

Week 1 Done:
- Courses: MAEG1020, ENGG1110
- Simulator: Initial structure
- Blocker: None
- Feeling: 8
```

## Related Files

- `bootcamp_weekly.py` — Saturday reminder
- `bootcamp_log.py` — Quick progress logger
- `progress.md` — Updated automatically
- `progress_log.txt` — Append log

**Last Updated:** 2026-06-08
