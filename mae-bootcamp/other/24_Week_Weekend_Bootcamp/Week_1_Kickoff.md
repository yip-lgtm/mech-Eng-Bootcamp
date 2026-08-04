# 🚀 Week 1 Kickoff — 24-Week IRE Bootcamp

> **Week 1 / 24** | **Phase 1: Foundations** (Week 1-6) | **Date**: 13 June 2026 (Saturday) | **Start Day** 🦞

---

## 🎯 Welcome to Week 1!

今日係 **24-Week IRE Bootcamp 嘅正式開始**! 你已經 commit 好一段時間嘅 IRE MSc 旅程, 而家 24 個週末之後, 你會有一個堅實嘅 IRE foundation + 1 個完整 portfolio.

---

## 📚 Week 1 重點 Topics (Phase 1 Foundations)

### 核心 Courses (Week 1-6 全部)
- **MAEG2020 Engineering Mechanics** (Statics + Dynamics)
- **MAEG3010 Mechanics of Materials** (Stress, Strain, Failure)
- **MAEG2030 Thermodynamics** (Laws, Cycles, Efficiency)
- **MAEG3030 Fluid Mechanics** (Continuity, Bernoulli, Flow)

### Week 1 聚焦: **MAEG2020 Engineering Mechanics** (基礎中的基礎)

#### 學習目標
- 識別同分析 force systems
- 應用 equilibrium equations (ΣFx=0, ΣFy=0, ΣM=0)
- 解決 truss / frame 問題
- 理解 friction 同 center of gravity

#### 建議時間分配 (Week 1 週末, ~10-12 小時)
| 時段 | 活動 | 時間 |
|------|------|------|
| Sat 9-11 AM | 讀 MAEG2020 .md 全部 | 2h |
| Sat 11-12 PM | 整理 notes + 公式卡 | 1h |
| Sat 2-4 PM | 解 5-10 個 example problems | 2h |
| Sat 4-6 PM | 3R robot arm 力學分析 | 2h |
| Sun 9-11 AM | 3R arm 改進 + warehouse robot 力學 | 2h |
| Sun 11-12 PM | 整理 + 寫 reflection | 1h |

---

## 🦾 硬件 Project 選擇 (Week 1 開始其中 1 個)

### Option 1: 3R Robot Arm 力學分析
- **目標**: 對現有 3R arm 做 forward / inverse kinematics + force analysis
- **Week 1 任務**: 建立座標系 + 寫 DH parameters
- **Skills**: 力學, 矩陣運算, Python (NumPy)
- **產出**: 力學分析報告 + DH table

### Option 2: Warehouse Robot 路徑規劃
- **目標**: 在 grid map 上做 path planning
- **Week 1 任務**: 寫 basic A* algorithm
- **Skills**: Graph search, Heuristics, Python
- **產出**: A* demo + path visualisation

### Option 3: Soft Robotics 預習 (Week 3 會做, 但 Week 1 預習)
- **目標**: 認識 soft actuators, fluidic control
- **Week 1 任務**: 睇 2-3 個 YouTube demos + 寫 reading notes
- **Skills**: Material science, Fluid dynamics
- **產出**: Reading summary

**建議**: Week 1 揀 **Option 1 (3R Arm)** — 同 IRE MSc 直接相關, 將來可以延伸去 Week 3 嘅 grasping, Week 6 嘅 advanced kinematics.

---

## 📝 Week 1 Deliverables

1. ✅ **MAEG2020 全部 notes** (~5-10 頁 hand-written 或 digital)
2. ✅ **5 個 worked examples** (equilibrium, truss, friction)
3. ✅ **3R arm DH table** (Denavit-Hartenberg parameters)
4. ✅ **Week 1 reflection** (用 `bootcamp_log.py` 記錄)
5. ✅ **Force analysis diagram** (3R arm gravity loading)

---

## 🛠️ Tools 同 Resources

### Software
- **Python 3.x** + **NumPy**, **SciPy**, **Matplotlib**
- **Robotics Toolbox for Python** (Peter Corke) — `pip install roboticstoolbox-python`
- **SymPy** for symbolic math
- **Jupyter Notebook** for analysis

### Reading
- **MAEG2020 .md** (in `subjects/mae-cuhk/MAEG2020/`)
- **Hibbeler Statics** (textbook reference)
- **MIT OCW 6.01** (online lectures, optional)

### Code Templates
- **3R arm starter** (in `demos/robot-arm/`)
- **DH parameters** (in `demos/robot-arm/dh_table.py`)

---

## ⏰ Schedule (Week 1)

### Saturday 13 June 2026
- 09:00 — 讀 MAEG2020 全部
- 11:00 — 整理 notes + 公式
- 14:00 — 解 5 個 examples
- 16:00 — 3R arm 力學 setup
- 19:00 — 寫 reflection

### Sunday 14 June 2026
- 09:00 — 3R arm DH table + 數值驗證
- 11:00 — Week 1 wrap-up
- 14:00 — 預習 Week 2 (Robot Arm dynamics)
- 16:00 — 整理 bootcamp_log

### Weekday 15-19 June
- 每日 30 min: 讀 1 段補充材料
- 每日 30 min: 寫 1 個 small test

### Friday 19 June 2026
- 19:00 — Week 1 最終 review

### Saturday 20 June 2026 (Week 2 開始)
- 09:00 — `bootcamp_weekly` 自動觸發 Week 2 reminder (cron)

---

## 📊 評估指標 (Week 1)

| Metric | Target | How to measure |
|--------|--------|----------------|
| MAEG2020 .md 讀完 | ✅ | 自我 checklist |
| Worked examples 完成 | 5/5 | 寫晒喺 notes |
| 3R arm DH table | ✅ | demo/robot-arm/dh_table.py |
| 公式卡 (Formula cards) | ≥ 15 張 | 用 Quizlet / Anki |
| Reflection 寫完 | 1 篇 | 300+ 字 |
| **Overall Week 1 進度** | **100%** | 全部 deliverable done |

---

## 🆘 Week 1 可能嘅 Blocker

| Blocker | 解決方法 |
|---------|----------|
| 力學底子唔夠 | 讀 MAEG2020 prerequisite (高中 Physics) |
| Python NumPy 唔熟 | YouTube: "NumPy tutorial for engineers" |
| 3R arm hardware 唔喺度 | 用 simulation only (no hardware needed) |
| 時間唔夠 | 將 worked examples 減到 3 個 |

---

## 💪 Week 1 Mindset

1. **Start small**: 唔好一次過讀晒所有嘢. 每日 1-2 小時就夠.
2. **Build incrementally**: 3R arm 唔需要 Week 1 完成, 慢慢 build.
3. **Reflect weekly**: 用 `bootcamp_log.py` 記錄 progress.
4. **Ask for help**: 遇到困難即問 (我自己, or OpenClaw).
5. **Celebrate small wins**: 完成 1 個 example = 1 個 milestone.

---

## 🎯 Week 1 完成後 (Sunday 14 June)

完成晒 Week 1 嘅 deliverables 之後, 用以下 command 記錄:

```bash
python3 bootcamp_log.py --week 1 \
  --courses MAEG2020 \
  --sim "3R arm DH table + force analysis" \
  --blocker "無" \
  --feeling 8
```

或者 quick mode:
```bash
python3 bootcamp_log.py "Week 1 Done: MAEG2020 + 3R arm DH table"
```

---

## 🚀 24-Week 大圖

| Week | Phase | 重點 |
|------|-------|------|
| 1-6 | Phase 1: Foundations | 力學, 材料, 流體, 熱力, 電路 |
| 7-12 | Phase 2: Mechatronics | 控制, 機械設計, 製造, 機電一體化 |
| 13-18 | Phase 3: Robotics | 機器人學, 智能材料, 視覺, 軟機器人 |
| 19-24 | Phase 4: FYP | 畢業論文 + Portfolio |

**完成所有 24 Week 之後**:
- ✅ IRE MSc 堅實基礎
- ✅ 1 個完整 portfolio (3R arm, warehouse, soft robot, FYP)
- ✅ 同期 IPD / CEng 進度 (CEng MICE PR 2026-2027)
- ✅ 工作 (Kam Tat YLC) 持續 professional growth

---

**Week 1 — 加油!** 🚀🦞💪

**記住**: 24 個週末, 每個週末 1 個 milestone. 一年後回望, 你會驚訝自己走咗幾遠!

— 2026-06-13, KANG YIP SZE
