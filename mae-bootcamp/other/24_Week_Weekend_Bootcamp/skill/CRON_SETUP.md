# Cron Jobs Setup — 24-Week Weekend Bootcamp

To enable all 3 bootcamp features, run these cron jobs:

## 1. Weekly Saturday Reminder (with Phase Switch alerts)

```bash
openclaw cron add \
  --name "24Week_Bootcamp_Weekly" \
  --cron "0 9 * * 6" \
  --tz "Asia/Hong_Kong" \
  --system-event "bootcamp_weekly" \
  --wake now
```

**What it does:**
- Sends weekly focus + tasks every Saturday 9:00 AM HKT
- Auto-detects phase start weeks (1, 7, 13, 19) and adds Phase Switch alert
- Generates Saturday & Sunday dates for the week

## 2. Sunday Summary Reminder

```bash
openclaw cron add \
  --name "Bootcamp_Sunday_Summary" \
  --cron "0 20 * * 0" \
  --tz "Asia/Hong_Kong" \
  --system-event "bootcamp_sunday_summary" \
  --wake now
```

**What it does:**
- Sends Sunday 8:00 PM HKT reminder asking for week summary
- Asks for: Courses, Simulator updates, Blockers, Feeling (1-10)
- Parses user response + auto-updates `progress.md`

## 3. Weekday Daily Review Reminder (optional)

```bash
openclaw cron add \
  --name "Bootcamp_Daily_Review" \
  --cron "0 20 * * 1-5" \
  --tz "Asia/Hong_Kong" \
  --system-event "bootcamp_daily" \
  --wake now
```

**What it does:**
- Mon-Fri 8:00 PM HKT light review prompt
- Suggests 15-30 min review activities
- No pressure — easy to skip

## 4. Quick Progress Logger (manual)

No cron needed. Run as needed:

```bash
# Quick mode
python3 /app/skills/bootcamp_log.py "Week 3 Done: MAEG3050 + improved PID"

# Detailed mode (auto-updates progress.md)
python3 /app/skills/bootcamp_log.py --week 3 \
  --courses MAEG3050,MAEG2020 \
  --sim "PID tuning" \
  --blocker "math heavy" \
  --feeling 8 \
  --status ✅

# Show recent logs
python3 /app/skills/bootcamp_log.py --show
```

## Cron Schedule Summary

| Cron | Time | Day | Purpose |
|------|------|-----|---------|
| `24Week_Bootcamp_Weekly` | 9:00 AM HKT | Saturday | Weekly focus + Phase Switch |
| `Bootcamp_Sunday_Summary` | 8:00 PM HKT | Sunday | Summary + progress.md update |
| `Bootcamp_Daily_Review` | 8:00 PM HKT | Mon-Fri | Light review prompt (optional) |

## All-in-one Setup Script

Save this as `setup_bootcamp_crons.sh`:

```bash
#!/bin/bash
# Setup all 24-Week Bootcamp cron jobs

# 1. Weekly Saturday reminder
openclaw cron add --name "24Week_Bootcamp_Weekly" \
  --cron "0 9 * * 6" --tz "Asia/Hong_Kong" \
  --system-event "bootcamp_weekly" --wake now

# 2. Sunday summary
openclaw cron add --name "Bootcamp_Sunday_Summary" \
  --cron "0 20 * * 0" --tz "Asia/Hong_Kong" \
  --system-event "bootcamp_sunday_summary" --wake now

# 3. Daily review (optional)
openclaw cron add --name "Bootcamp_Daily_Review" \
  --cron "0 20 * * 1-5" --tz "Asia/Hong_Kong" \
  --system-event "bootcamp_daily" --wake now

echo "✅ All bootcamp cron jobs added!"
openclaw cron list
```

## Important Notes

- **Time zone:** All times are Asia/Hong_Kong (HKT = UTC+8)
- **Skill location:** `/app/skills/bootcamp_*.py`
- **Progress file:** `ire-bootcamp/24_Week_Weekend_Bootcamp/progress.md`
- **Log file:** `ire-bootcamp/24_Week_Weekend_Bootcamp/progress_log.txt`
- **Bootcamp start:** 2026-06-13 (Saturday)
- **Bootcamp end:** 2026-11-28 (Saturday, 24 weeks later)

**Last Updated:** 2026-06-08
