# AGENT 4: Diagram (Mechanical & Automation Engineering)

## 職責
產出 **5 個 Mermaid 圖**，每個必須：
- 直接對應本課程核心概念
- 唔係 template 圖
- GitHub-renderable syntax

## 5 個圖嘅類型
1. **stateDiagram-v2** — system states / regimes
2. **flowchart TD/LR** — decision flow / algorithm
3. **sequenceDiagram** — process steps / interactions
4. **classDiagram** — components / relationships
5. **erDiagram** — entities / relationships (or `gantt`/`timeline`)

## 品質門檻
- ❌ **拒絕**: 5 個 graph TD 全部一樣嘅 template
- ❌ **拒絕**: Empty node labels
- ❌ **拒絕**: 唔 render 嘅 syntax
- ✅ **必須**: 5 個圖都係 distinct type
- ✅ **必須**: 至少 1 個 diagram 包含 course-specific entities

## Output
Inserted into course file as ```mermaid ... ``` blocks.

## Validation
- `grep -c '\`\`\`mermaid'` should return 5 per file
