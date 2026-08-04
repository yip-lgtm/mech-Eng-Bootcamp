"""
Bootcamp Sunday Summary Skill
Sends Sunday evening reminder asking for week's reflection.
Updates progress.md automatically when user replies.

Used by OpenClaw cron job: 0 20 * * 0 (Asia/Hong_Kong)
"""
import datetime
import json
import os
import re


BOOTCAMP_START = datetime.date(2026, 6, 13)
TOTAL_WEEKS = 24

# Path to the progress.md (in the IRE repo)
PROGRESS_MD = "/app/data-intelligence-architect/ire-bootcamp/24_Week_Weekend_Bootcamp/progress.md"


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


def get_phase(week_num):
    """Determine (phase_num, phase_name) from week number"""
    if week_num <= 6:
        return 1, "Phase 1: Foundations"
    if week_num <= 12:
        return 2, "Phase 2: Mechatronics & Control"
    if week_num <= 18:
        return 3, "Phase 3: Robotics & Advanced"
    return 4, "Phase 4: Integration & FYP"


def generate_summary_prompt(week_num):
    """Generate Sunday evening summary prompt"""
    if week_num > TOTAL_WEEKS:
        return """🎉 **24-Week Bootcamp 已完成! 恭喜你!**

你已經完成晒 CUHK BEng + PolyU MSc IRE 全部 24 週!

下一步:
- 整理 portfolio
- 寫 FYP 完整 paper
- 或者開新嘅學習旅程! 🚀"""

    if week_num < 1:
        return f"""🚀 **24-Week Bootcamp** 仲未開始!

開始日期: {BOOTCAMP_START} (第一個星期六)
仲有 {(BOOTCAMP_START - datetime.date.today()).days} 日!"""

    phase_num, phase_name = get_phase(week_num)
    saturday = BOOTCAMP_START + datetime.timedelta(days=(week_num - 1) * 7)
    sunday = saturday + datetime.timedelta(days=1)

    return f"""📅 **【Week {week_num} Sunday Summary】**

🎯 Phase: {phase_name}
📆 週末: {saturday} (Sat) - {sunday} (Sun)

請用以下格式回覆我 (我會幫你記錄 + 更新 progress.md):

```
Week {week_num} Done:
- Courses: MAEGxxxx, MAEGyyyy, ...
- Simulator: 你更新咗咩 (例: PID tuning, IK fix, ...)
- Blocker: 有冇困難 (例: 數學, 時間, ...)
- Feeling: 1-10分
```

完成後我會自動 update [`progress.md`](./progress.md) 嘅 Week {week_num} 行 📝

💪 寫下嚟啦! 反思係進步嘅第一步!"""


def update_progress_md(week_num, courses="", simulator="", blocker="", feeling="", status="✅"):
    """Update the progress.md file with week's summary"""
    if not os.path.exists(PROGRESS_MD):
        return False, f"progress.md not found at {PROGRESS_MD}"
    
    with open(PROGRESS_MD, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Build the new row content
    note_parts = []
    if courses:
        note_parts.append(f"Courses: {courses}")
    if simulator:
        note_parts.append(f"Sim: {simulator}")
    if blocker:
        note_parts.append(f"Block: {blocker}")
    if feeling:
        note_parts.append(f"Feel: {feeling}/10")
    notes = " | ".join(note_parts) if note_parts else ""
    
    # Find the row for this week
    # Pattern: | N | YYYY-MM-DD | Phase X | ... | ⬜ | (empty) |
    pattern = re.compile(
        rf'(\|\s*{week_num}\s*\|\s*\d{{4}}-\d{{2}}-\d{{2}}\s*\|[^|]*\|[^|]*\|[^|]*\|\s*)(⬜|🟡|✅)(\s*\|\s*)([^|\n]*)',
        re.MULTILINE
    )
    
    new_row = f"\\1{status}\\3{notes}"
    new_content, count = pattern.subn(new_row, content)
    
    if count == 0:
        return False, f"Week {week_num} row not found in progress.md"
    
    with open(PROGRESS_MD, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    return True, f"Updated Week {week_num} row: status={status}, notes={notes}"


def parse_user_summary(week_num, user_text):
    """Parse user's summary response and update progress.md"""
    courses = ""
    simulator = ""
    blocker = ""
    feeling = ""
    
    # Parse line by line
    for line in user_text.split('\n'):
        line = line.strip()
        if line.lower().startswith('courses:'):
            courses = line[len('courses:'):].strip()
        elif line.lower().startswith('simulator:'):
            simulator = line[len('simulator:'):].strip()
        elif line.lower().startswith('blocker:'):
            blocker = line[len('blocker:'):].strip()
        elif line.lower().startswith('feeling:'):
            feeling = line[len('feeling:'):].strip()
    
    if not any([courses, simulator, blocker, feeling]):
        return False, "No data found in user response. Please use format:\nCourses: ...\nSimulator: ...\nBlocker: ...\nFeeling: 1-10"
    
    return update_progress_md(week_num, courses, simulator, blocker, feeling, status="✅")


def main():
    today = datetime.date.today()
    week_num, status = get_current_week(today)
    msg = generate_summary_prompt(week_num)
    print(msg)
    print("\n--- JSON ---")
    print(json.dumps({
        "today": today.isoformat(),
        "week_num": week_num,
        "status": status,
        "message": msg,
    }, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
