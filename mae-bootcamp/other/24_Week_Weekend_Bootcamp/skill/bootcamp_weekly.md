# Bootcamp Weekly Skill

> **Purpose:** Generate the 24-Week Weekend Bootcamp weekly focus + tasks.
> **Trigger:** OpenClaw cron job, every Saturday 9:00 AM HKT.
> **Source:** `ire-bootcamp/24_Week_Weekend_Bootcamp/`

## How It Works

1. Cron triggers `bootcamp_weekly.py` on Saturday morning
2. Script calculates current week (1-24) from start date (2026-06-13)
3. Determines current phase (1-4) based on week number
4. Returns formatted message with:
   - Current week number
   - Phase + focus
   - 2-3 core courses to study
   - 2 simulator tasks
   - Reflection prompts

## Usage

```bash
python3 /app/skills/bootcamp_weekly.py
```

## Cron Job Setup

Recommended:
```bash
openclaw cron add \
  --name "24Week_Bootcamp_Weekly" \
  --cron "0 9 * * 6" \
  --tz "Asia/Hong_Kong" \
  --system-event "bootcamp_weekly" \
  --wake now
```

## Configuration

Edit `BOOTCAMP_START` in the script to change start date.

## Output Format

Returns a markdown-formatted message with:
- 🚀 Header
- 📅 Weekend dates
- 🎯 Phase info
- 📖 Theory section (courses to study)
- 💻 Practice section (simulator tasks)
- 📝 Reflection section

## Related Files

- `ire-bootcamp/24_Week_Weekend_Bootcamp/README.md` — Full 24-week plan
- `ire-bootcamp/24_Week_Weekend_Bootcamp/progress.md` — Progress tracker
- `ire-bootcamp/mae-cuhk/courses/` — All course .md files (75+)
- `ire-bootcamp/demos/` — Simulator (3R arm + warehouse robot)

## Phases Summary

| Phase | Weeks | Focus |
|-------|-------|-------|
| 1 | 1-6 | Foundations (Math, Physics, Mechanics) |
| 2 | 7-12 | Mechatronics & Control (PID, Design) |
| 3 | 13-18 | Robotics & Advanced (IK, AI, Soft) |
| 4 | 19-24 | Integration & FYP Prep |

**Last Updated:** 2026-06-08
