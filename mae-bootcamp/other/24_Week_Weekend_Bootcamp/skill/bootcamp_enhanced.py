"""
Bootcamp Enhanced Skill
Adds 3 features on top of bootcamp_log.py:
1. Auto-write Sunday Summary to progress.md
2. Phase-start long encouraging messages
3. Daily lightweight reminder

Usage:
  python3 bootcamp_enhanced.py sunday       # Generate Sunday summary prompt
  python3 bootcamp_enhanced.py phase-start  # Show phase-start message
  python3 bootcamp_enhanced.py daily        # Show daily reminder
  python3 bootcamp_enhanced.py status       # Show current status
"""

import datetime
import os
import sys

# Paths (consistent with bootcamp_log.py)
PROGRESS_MD = "/app/data-intelligence-architect/ire-bootcamp/24_Week_Weekend_Bootcamp/progress.md"
PROGRESS_LOG = "/app/data-intelligence-architect/ire-bootcamp/24_Week_Weekend_Bootcamp/progress_log.txt"
BOOTCAMP_START = datetime.date(2026, 6, 13)
TOTAL_WEEKS = 24

# Phase definitions
PHASES = {
    1: {
        "name": "Phase 1: Foundations",
        "weeks": (1, 6),
        "focus": "Math, Physics, Mechanics, Materials, Circuits, Thermo",
        "color": "🟦",
        "courses": ["MAEG3010 Mechanics of Materials", "MAEG3030 Fluid Mechanics",
                    "MAEG2030 Thermodynamics", "MAEG2020 Engineering Mechanics"],
    },
    2: {
        "name": "Phase 2: Mechatronics & Control",
        "weeks": (7, 12),
        "focus": "Control Systems, Mechanical Design, Manufacturing, Fluid Mechanics, Heat Transfer, Mechatronics",
        "color": "🟩",
        "courses": ["MAEG3050 Intro to Control Systems", "MAEG3040 Mechanical Design",
                    "MAEG3020 Manufacturing Tech", "MAEG4040 Mechatronic Systems"],
    },
    3: {
        "name": "Phase 3: Robotics & Advanced",
        "weeks": (13, 18),
        "focus": "Robotics, Advanced Control, Smart Materials, AI, Vision, Soft Robotics",
        "color": "🟨",
        "courses": ["MAEG3060 Intro to Robotics", "MAEG5080 Smart Materials & Structures",
                    "MAEG2050 Robot Development in Practice"],
    },
    4: {
        "name": "Phase 4: Integration & FYP",
        "weeks": (19, 24),
        "focus": "FYP I/II + Portfolio + Electives",
        "color": "🟥",
        "courses": ["MAEG4998 FYP I", "MAEG4999 FYP II"],
    },
}


def get_current_week(today=None):
    if today is None:
        today = datetime.date.today()
    days_elapsed = (today - BOOTCAMP_START).days
    week_num = (days_elapsed // 7) + 1
    if week_num < 1:
        return 0, "not_started"
    if week_num > TOTAL_WEEKS:
        return TOTAL_WEEKS + 1, "completed"
    return week_num, "active"


def get_phase_for_week(week_num):
    for p_num, p_info in PHASES.items():
        if p_info["weeks"][0] <= week_num <= p_info["weeks"][1]:
            return p_num, p_info
    return None, None


def feature_1_sunday_prompt():
    """Generate Sunday summary prompt and write to progress_log"""
    week, status = get_current_week()
    if status != "active":
        print(f"⚠️ Not in active week (status: {status})")
        return

    phase_num, phase = get_phase_for_week(week)

    prompt = f"""
📅 **【Week {week} Sunday Summary】** 📅
{phase['color']} {phase['name']} (Week {week}/{TOTAL_WEEKS})

請直接回覆以下格式，我會自動記錄同更新 progress.md:

```
Week {week} Done:
- Courses: (e.g. MAEG3050, MAEG4040)
- Simulator: (e.g. 更新了 force feedback + state machine)
- Blocker: (e.g. 無 / math 難)
- Feeling: (1-10)
```

**Phase 重點**: {phase['focus']}

💡 **本週建議**:
- 完成 1-2 個 Phase {phase_num} 重點 topics
- 更新 3R robot arm 或 warehouse robot
- 整理 notes 同 code
- 預習下週內容
"""
    print(prompt)

    # Auto-write the Sunday prompt timestamp to progress_log
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] [Week {week} Sunday] Summary prompt sent\n"

    os.makedirs(os.path.dirname(PROGRESS_LOG), exist_ok=True)
    with open(PROGRESS_LOG, 'a', encoding='utf-8') as f:
        f.write(log_entry)

    print(f"📝 Sunday prompt logged to {PROGRESS_LOG}")
    print(f"\n💬 等你回覆格式後, 用以下 command 記錄:")
    print(f'   python3 bootcamp_log.py --week {week} --courses MAEG3050,MAEG4040 --sim "force feedback" --feeling 8')


def feature_2_phase_start(week_num=None):
    """Show long encouraging message for Phase start (weeks 1, 7, 13, 19)"""
    if week_num is None:
        week_num, _ = get_current_week()

    phase_num, phase = get_phase_for_week(week_num)
    if phase_num is None:
        print(f"⚠️ No phase found for week {week_num}")
        return

    long_msg = f"""
╔══════════════════════════════════════════════════════════╗
║  🚨【Phase Switch Alert】🚨                              ║
║                                                          ║
║  📅 Week {week_num} / {TOTAL_WEEKS}                                    ║
║  🎯 {phase['color']} **{phase['name']}**              ║
║  📚 Focus: {phase['focus']}                    ║
╚══════════════════════════════════════════════════════════╝

🎉 **歡迎嚟到新 Phase!** 呢個係一個重要 milestone — 你已經完成咗之前嘅 Phase!

📚 **本 Phase 重點 topics**:
"""
    for i, course in enumerate(phase['courses'], 1):
        long_msg += f"   {i}. {course}\n"

    long_msg += f"""
💪 **記住**: 
   ✓ 24 個 Week, 24 個週末, 24 個 milestone
   ✓ 每完成 1 Week = 4.17% 進度
   ✓ 完成整個 Bootcamp = IRE MSc 基礎
   ✓ 同時可以兼顧 IPD (CEng) + work (Kam Tat)

🎯 **建議你做**:
   1. 睇 Phase 內所有 courses 嘅 .md
   2. 揀 1 個 hardware project 做 (3R arm, warehouse, soft robot)
   3. 寫 weekly reflection (用 bootcamp_log.py)
   4. 預下週嘅 content

🚀 **加油!** 24 週後你就會有一個堅實嘅 IRE foundation + 1 個完整 portfolio!

— KANG YIP SZE 嘅 Phase {phase_num} 旅程正式開始 💪🦞
"""
    print(long_msg)

    # Log the phase start
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] [Phase {phase_num} START] {phase['name']}\n"
    os.makedirs(os.path.dirname(PROGRESS_LOG), exist_ok=True)
    with open(PROGRESS_LOG, 'a', encoding='utf-8') as f:
        f.write(log_entry)


def feature_3_daily_reminder():
    """Show lightweight daily reminder"""
    week, status = get_current_week()
    if status != "active":
        print(f"⏸️ Bootcamp {status} (week {week})")
        return

    phase_num, phase = get_phase_for_week(week)

    today = datetime.date.today()
    days_to_saturday = (5 - today.weekday()) % 7  # 0=Mon, 5=Sat
    if days_to_saturday == 0:
        days_to_saturday = 0  # Today is Saturday

    weekday = today.strftime("%A")
    time_of_day = "morning" if today.hour < 12 else "afternoon" if today.hour < 18 else "evening"

    reminder = f"""
🌅 **【{weekday} {time_of_day} Daily Reminder】** 🌅

📅 Bootcamp Day {((today - BOOTCAMP_START).days) + 1} (Week {week}/{TOTAL_WEEKS})
{phase['color']} {phase['name']}

⏰ 距離週末: {days_to_saturday} 日

💡 **今日可以做嘅小任務** (15-30 min):
   ✓ 讀 1 個 course .md (e.g. MAEG course)
   ✓ 寫 5 行程式 / 改 1 個 bug
   ✓ 睇 1 段 YouTube tutorial
   ✓ Update 3R arm / warehouse robot 嘅 1 個 feature

🎯 **本週目標** (Week {week}):
   Phase {phase_num} 重點: {phase['focus']}

📝 完成後記錄:
   python3 bootcamp_log.py "Week {week} ...your update..."

💪 加油! 24 週旅程每一步都重要 🚀
"""
    print(reminder)


def show_status():
    week, status = get_current_week()
    if status == "not_started":
        print(f"⏳ Bootcamp 未開始. 開始日: {BOOTCAMP_START} (仲有 {(BOOTCAMP_START - datetime.date.today()).days} 日)")
        return
    if status == "completed":
        print(f"🎉 Bootcamp 已完成! 全部 {TOTAL_WEEKS} 週 done.")
        return

    phase_num, phase = get_phase_for_week(week)
    today = datetime.date.today()
    days_elapsed = (today - BOOTCAMP_START).days + 1
    progress = int(days_elapsed / (TOTAL_WEEKS * 7) * 100)

    print(f"""
╔════════════════════════════════════════════╗
║  📊 **Bootcamp Status**                   ║
╠════════════════════════════════════════════╣
║  📅 今日: {today}                        ║
║  🚀 Bootcamp Day: {days_elapsed} / {TOTAL_WEEKS * 7}             ║
║  📆 Week: {week} / {TOTAL_WEEKS}                          ║
║  {phase['color']} Phase: {phase_num} - {phase['name']}  ║
║  📈 整體進度: {progress}%                            ║
║  📚 本 Phase Focus:                       ║
║     {phase['focus'][:40]:<40} ║
╚════════════════════════════════════════════╝
""")


def show_usage():
    print("""
🎓 **Bootcamp Enhanced Skill**

**Usage**:
```
python3 bootcamp_enhanced.py sunday        # Sunday summary prompt
python3 bootcamp_enhanced.py phase-start   # Phase start long message
python3 bootcamp_enhanced.py daily         # Daily lightweight reminder
python3 bootcamp_enhanced.py status        # Show current status
```
""")


def main():
    if len(sys.argv) < 2:
        show_usage()
        return

    cmd = sys.argv[1].lower()

    if cmd in ("sunday", "summary"):
        feature_1_sunday_prompt()
    elif cmd in ("phase-start", "phase", "start"):
        week_arg = int(sys.argv[2]) if len(sys.argv) > 2 else None
        feature_2_phase_start(week_arg)
    elif cmd in ("daily", "reminder", "today"):
        feature_3_daily_reminder()
    elif cmd in ("status", "stat"):
        show_status()
    else:
        print(f"❌ Unknown command: {cmd}")
        show_usage()


if __name__ == "__main__":
    main()
