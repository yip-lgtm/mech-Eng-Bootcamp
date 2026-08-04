# mech Eng. Bootcamp 🤖

> Mechanical Engineering Self-Study Bootcamp — CUHK BEng MAE + Real-World Projects

---

## 📚 自學課程

- [mae-bootcamp/](mae-bootcamp/) — CUHK BEng Mechanical & Automation Engineering curriculum
  - [STUDY_PLAN.md](mae-bootcamp/STUDY_PLAN.md) — Year 1-4 自學路徑
  - [courses/COURSE_INDEX.md](mae-bootcamp/courses/COURSE_INDEX.md) — 64 courses 總索引
  - [courses/faculty-package/](mae-bootcamp/courses/faculty-package/) — 5 Faculty Package courses (ENGG1110/1120/1130, MATH1510, PHYS1110)
  - [courses/electives/](mae-bootcamp/courses/electives/) — 43 major electives (5 streams)
  - [courses/major-required/](mae-bootcamp/courses/major-required/) — 13 major required courses
  - [courses/foundation/](mae-bootcamp/courses/foundation/) — foundation courses

## 🚀 Demos

[Week 1 Gary 倉庫機械人 Demo](mae-bootcamp/other/demos/)
- `demos/snapshots/` — state machine screenshots

## 📅 每週計劃

[week-plans/](mae-bootcamp/other/week-plans/)

## 📖 Subject Notes

[subjects/](mae-bootcamp/other/subjects/) — 每科深度筆記 (robotics, control, AI, etc.)

## 🏗️ 24-Week Weekend Bootcamp

[24_Week_Weekend_Bootcamp/](mae-bootcamp/other/24_Week_Weekend_Bootcamp/) — Phase 1-4 curriculum + builds

## 📂 課程格式 — 袁騰飛格式 (5MM / 3DG / 10Q / 5DD / 10SL / 5MR)

每一個 course file 都係用 **袁騰飛格式** 寫成，呢個格式係由袁騰飛老師嘅教學風格啟發 — 用紮實嘅研究材料 + 嚴密嘅邏輯結構，取代一般嘅 template 填空。

### 🧱 結構組成

| 元素 | 數量 | 內容 | 範例 |
|---|---|---|---|
| **5MM** | 5 | 核心心智模型 (Mental Models) — 方程式 + 真實數字 + 歷史學者 | Newton's 2nd Law: F=ma, F=1.5N at m=0.3kg, a=5m/s² (Newton 1687) |
| **3DG** | 3 | 根本分歧 (Divergent views) — A/B 兩方 + 引用 | Lagrangian vs Newtonian (Goldstein 1980) |
| **10Q** | 10 | 深度問題 (Questions) — 由淺入深 | "Why is ∇·B=0?" |
| **5DD** | 5 | 深度 dive (中英對照) — 兩個 paragraph 講核心概念 | Strain tensor 嘅 geometric meaning |
| **10SL** | 10 | Solutions — 完整 worked example + Python code | Runge-Kutta 4 用嚟解 pendulum equation |
| **5MR** | 5 | Mermaid 圖 — state machine / flowchart / sequence | ```mermaid stateDiagram-v2``` |

### 🎯 核心原則

1. **真實研究材料 (No template)** — 唔用 placeholder、唔用 "[TBD]"、唔用 "Lorem ipsum"。每個方程式、每個數字、每個學者都要查過 web。
2. **中英對照 (Bilingual)** — DD 段落、技術名詞都英中並列，方便香港雙語環境。
3. **學者真名 + 出版年份** — 例：Euler 1755, Lagrange 1788, Hamilton 1834, Maxwell 1865, Noether 1918 — 唔寫 "someone famous"。
4. **Python code 可運行** — 每個 solution 都有 `python3` executable code，唔係 pseudocode。
5. **Mermaid diagram 必須 render** — 唔寫爛 syntax，要直接喺 GitHub 渲染得到。

### 🛠️ Course Generation Pipeline

課程生成嘅 setup：

```
┌─────────────────────────────────────────┐
│  1. Web Research (per course)           │
│     - Wikipedia / Scholarpedia          │
│     - Original papers (DOI, arXiv)      │
│     - CUHK MAE official syllabus        │
│     - Historical figures + dates        │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│  2. Outline 5MM/3DG/10Q/5DD/10SL/5MR    │
│     - Map topics → each section         │
│     - Identify 5 mental models          │
│     - Find 3 historical debates         │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│  3. Write bilingual content             │
│     - Each DD: EN paragraph + 中文      │
│     - Each SL: code + math + 中文解釋   │
│     - Citations inline (Author Year)    │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│  4. Mermaid diagrams                    │
│     - 5 distinct diagrams per course    │
│     - stateDiagram / flowchart / class  │
│     - GitHub-renderable syntax          │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│  5. Verify & Push                       │
│     - Code runs: `python3 test.py`      │
│     - Mermaid renders on GitHub         │
│     - No "[TBD]", no template placeholders │
│     - git commit + push                 │
└─────────────────────────────────────────┘
```

### 📏 Quality Bar

- ❌ **拒絕**: Template 填空、`[TBD]`、`待補充`、generic paragraphs
- ❌ **拒絕**: Pseudocode (必須 executable Python)
- ❌ **拒絕**: "Some scientists believe..." 含糊 attribution
- ✅ **接受**: Real scholars (Newton 1687, Maxwell 1865, Noether 1918)
- ✅ **接受**: Specific numbers (F=ma where F=1.5N, m=0.3kg, a=5m/s²)
- ✅ **接受**: Bilingual DD (EN + 中文) 
- ✅ **接受**: Runnable Python + 5 Mermaid diagrams per course

### 🧪 Verification (per course)

```bash
# 1. Check file size (should be 300+ lines)
wc -l mae-bootcamp/courses/electives/MAEG1010.md
# 2. Extract and run Python code blocks
grep -A 20 '```python' mae-bootcamp/courses/electives/MAEG1010.md | python3
# 3. Validate Mermaid syntax
grep -c '```mermaid' mae-bootcamp/courses/electives/MAEG1010.md  # should be 5
# 4. Check no placeholder text
grep -E "\[TBD\]|待補充|Lorem" mae-bootcamp/courses/**/*.md  # should be empty
```

## 📊 Progress

[progress/Bootcamp_Progress.md](mae-bootcamp/other/progress/Bootcamp_Progress.md)
