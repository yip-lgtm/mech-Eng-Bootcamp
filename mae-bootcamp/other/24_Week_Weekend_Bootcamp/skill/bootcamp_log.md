# Bootcamp Quick Log Skill

> **Purpose:** Quick progress logger — appends to log file + optionally updates `progress.md`
> **Usage:** `python3 bootcamp_log.py "..."` or `python3 bootcamp_log.py --week N ...`

## Quick Mode (log to file only)

```bash
python3 bootcamp_log.py "Week 3 Done: MAEG3050 + improved PID + force feedback"
```

## Detailed Mode (update progress.md)

```bash
python3 bootcamp_log.py --week 3 \
  --courses MAEG3050,MAEG2020 \
  --sim "PID tuning" \
  --blocker "math heavy" \
  --feeling 8 \
  --status ✅
```

## Show Recent Logs

```bash
python3 bootcamp_log.py --show
```

## Auto-detected Week

If you don't pass `--week`, it auto-detects current week from date.

## Log File Location

`/app/data-intelligence-architect/ire-bootcamp/24_Week_Weekend_Bootcamp/progress_log.txt`

Each line: `[2026-06-08 14:30:00] [Week N] Log text here`

## Related Files

- `bootcamp_weekly.py` — Saturday reminder
- `bootcamp_sunday_summary.py` — Sunday summary
- `progress.md` — Updated by detailed mode
- `progress_log.txt` — Append by all modes

**Last Updated:** 2026-06-08
