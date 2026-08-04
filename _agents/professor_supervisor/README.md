# AGENT 5: Professor Supervisor (Quality Gate — Mechanical & Automation Engineering)

## 職責
審稿每一個 course file。Decision:
- ✅ **APPROVED** — meets all quality gates, push
- ⚠️ **REVISE** — specific issues to fix, retry
- ❌ **REJECT** — fundamentally inadequate, redo from scratch

## Quality Gates (Rubric)

| Gate | Check | 拒絕 if |
|---|---|---|
| **G1 Length** | `wc -l` | < 300 lines |
| **G2 Format** | Deep Study Format sections | Missing 5MM, 3DG, 10Q, 5DD, 10SL, 5MR |
| **G3 Citations** | Real scholars + year | < 3 named scholars |
| **G4 Specificity** | Numbers + equations | < 3 equations |
| **G5 Bilingual** | 中英對照 | EN-only or 中文-only section |
| **G6 No Placeholder** | `[TBD]`, `待補充`, `Lorem` | Any placeholder text |
| **G7 Mermaid** | 5 diagrams | < 5 distinct diagrams |
| **G8 Solutions** | 10 detailed answers | Short < 5 line answers |
| **G9 Deep Dives** | 5 specific dives | Generic "Concept 1, Concept 2..." |
| **G10 No Template** | No T0/T1/T2 placeholders | `T0 — Core concept` style |

## Decision
- **APPROVED**: score >= 85
- **REVISE**: 70 <= score < 85
- **REJECT**: score < 70

## Pipeline integration
```bash
python3 _agents/professor_supervisor/review.py --all
```

**不通過不推送** — failed files quarantined.
