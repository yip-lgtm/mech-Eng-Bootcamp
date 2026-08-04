"""
Bootcamp Weekly Skill — 24-Week Weekend Bootcamp
Generates weekly focus + tasks + Phase Switch alerts.

Used by OpenClaw cron job: 0 9 * * 6 (Asia/Hong_Kong)
"""
import datetime
import json


# Bootcamp configuration
BOOTCAMP_START = datetime.date(2026, 6, 13)  # First Saturday
TOTAL_WEEKS = 24
PHASE_START_WEEKS = {1: 1, 2: 7, 3: 13, 4: 19}


def get_phase(week_num):
    """Determine (phase_num, phase_name, phase_focus) from week number"""
    if week_num <= 0:
        return 0, "Not Started", ""
    if week_num <= 6:
        return 1, "Phase 1: Foundations", "Math, Physics, Mechanics, Materials, Circuits, Thermo"
    if week_num <= 12:
        return 2, "Phase 2: Mechatronics & Control", "Control Systems, Mechanical Design, Manufacturing, Fluid, Heat Transfer, Mechatronics"
    if week_num <= 18:
        return 3, "Phase 3: Robotics & Advanced", "Robotics, Advanced Control, Smart Materials, AI, Vision"
    return 4, "Phase 4: Integration & FYP", "FYP I/II + Portfolio + Remaining Electives"


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


def is_phase_start(week_num):
    """Check if this is a phase switch week (1, 7, 13, 19)"""
    return week_num in [1, 7, 13, 19]


def get_phase_saturday(week_num):
    """Calculate Saturday date for a given week number"""
    saturday = BOOTCAMP_START + datetime.timedelta(days=(week_num - 1) * 7)
    sunday = saturday + datetime.timedelta(days=1)
    return saturday, sunday


def generate_weekly_message(week_num, include_phase_switch=True):
    """Generate the weekly focus message with optional phase switch alert"""
    if week_num < 1:
        saturday = BOOTCAMP_START
        days_until = (saturday - datetime.date.today()).days
        return f"""🚀 **24-Week Bootcamp 仲未開始!**

開始日期: **{saturday}** (第一個星期六)
今日: {datetime.date.today()}

仲有 **{days_until} 日!**

準備好嘅話, 之後可以隨時開始. 💪"""

    if week_num > TOTAL_WEEKS:
        return """🎉 **恭喜! 24-Week Bootcamp 完成!**

你已經完成晒 CUHK BEng + PolyU MSc IRE 全部課程!

下一步:
- 📂 整理 portfolio
- 📝 寫 FYP 完整 paper
- 🚀 或者開新嘅學習旅程!"""

    phase_num, phase_name, phase_focus = get_phase(week_num)
    saturday, sunday = get_phase_saturday(week_num)

    msg = ""
    
    # Phase Switch alert
    if is_phase_start(week_num) and include_phase_switch:
        msg += "\n🚨 **【Phase Switch】進入 " + phase_name + "!**\n\n"
        msg += "本 Phase 重點: " + phase_focus + "\n\n"
        msg += "呢個週末係 Phase 嘅開始, 花多少少時間:\n"
        msg += "1. 回顧上一 Phase 嘅總結\n"
        msg += "2. 規劃今個 Phase 嘅 6 週目標\n"
        msg += "3. 重新睇下 `progress.md` 嘅 phase" + str(phase_num) + "_* notes\n\n"
        msg += "📌 Phase 1 係基礎, Phase 2 開始, Phase 3 係核心, Phase 4 係整合!\n"
        msg += "─" * 50 + "\n\n"

    msg += f"""🚀 **【24-Week Bootcamp】Week {week_num} / 24**

📅 週末: **{saturday} (Sat) - {sunday} (Sun)**
🎯 Phase: {phase_name}
📚 焦點: {phase_focus}

---

**📖 理論 (Saturday AM, 3-4 小時):**
- 讀相關課程 .md
- 睇重點 lecture / textbook
- 更新課程 .md 筆記

**💻 實踐 (Saturday PM, 3-4 小時):**
- 更新 3R arm / warehouse robot
- Git commit (寫清楚做了咩)

**📝 反思 (Sunday AM, 2-3 小時):**
- 更新 progress.md 嘅 Week {week_num} 行
- 寫 short reflection

---

💪 加油! Week {week_num} 衝刺!
"""
    return msg


def get_daily_reminder(week_num):
    """Generate weekday evening reminder (lighter, 15-30 min review)"""
    phase_num, phase_name, phase_focus = get_phase(week_num)
    if phase_num == 0 or phase_num > 4:
        return None
    
    return f"""📚 **24-Week Bootcamp Week {week_num}** - 平日 review 提示

🎯 Phase: {phase_name}
📚 焦點: {phase_focus}

今晚 15-30 分鐘可以 review 嘅:
- 返睇上週嘅 simulator commit
- 重温本週 Phase 嘅 courses
- 或者睇下 Week {week_num + 1} 嘅預習

💪 唔使強迫, 輕鬆就好! 🚀"""


def main():
    today = datetime.date.today()
    week_num, status = get_current_week(today)
    if status == "not_started":
        msg = generate_weekly_message(0)
    elif status == "completed":
        msg = generate_weekly_message(TOTAL_WEEKS + 1)
    else:
        msg = generate_weekly_message(week_num)
    print(msg)
    output = {
        "today": today.isoformat(),
        "week_num": week_num,
        "status": status,
        "phase": get_phase(week_num)[0] if status == "active" else None,
        "is_phase_start": is_phase_start(week_num) if status == "active" else False,
        "message": msg,
    }
    print("\n--- JSON ---")
    print(json.dumps(output, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
