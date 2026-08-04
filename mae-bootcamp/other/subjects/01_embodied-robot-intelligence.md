# 01 Embodied Robot Intelligence

## Week 1 自學總結 (2026-05-15)
科目：Embodied Robot Intelligence + Advanced Artificial Intelligence 
完成度：✅ 100% 
核心成果：建成本地 Pygame + Web 版 Embodied Agent Demo，並以 Figure AI "Gary" 直播倉庫機械人作為真實案例。

## 1. 核心概念 (Task 1A)
| 英文概念 | 中文 | 解釋 | 實際例子 |
|---------------------------|---------------|-------------------------------------------|---------------------------|
| Perception-Action Loop | 感知-動作閉環 | 感官輸入 → 處理 → 動作輸出 → 再感官輸入 | Gary 看見包裹 → 決定動作 → 執行 |
| Embodiment Hypothesis | 具身假設 | 智能來自「身體 + 環境」互動 | 無身體就無真正智能 |
| Multi-modal Fusion | 多模態融合 | 視覺 + 觸覺 + 力覺等感官融合 | 機械臂同時用 camera + touch sensor |
| Situated Cognition | 情境認知 | 智能在真實環境中產生 | Gary 在真倉庫學習而非 simulation |

## 2. Advanced AI + Robot Integration (Task 1B)
- VLA 模型（Vision-Language-Action）：LLM 直接輸出動作指令
- 最新例子：RT-2、PaLM-E、LLaVA、Gemini Robotics 1.5、GEN-1
- 核心想法：LLM 不再只是聊天工具，而是真正 Robot Brain

## 3. 實作 Demo (Task 2)
- Pygame 2D 遊戲 + 手機友好 Web 版
- Demo 連結：https://yip-lgtm.github.io/Master-of-Science-in-Intelligent-Robotics-Engineering/demos/index.html
- 功能：按 SPACE 執行一次完整 Perception → LLM Think → Action 閉環
- 融入 Gary 直播案例：藍色 Agent 模擬 Gary 在倉庫分揀包裹

## 4. 真實案例研究 – Gary (Figure AI)
- Gary 連續 8+ 小時全自主分揀包裹
- 真實展示 Embodied AI 在工業環境的應用
- 啟發：Perception-Action Loop 已在真實倉庫落地

## 個人心得
- 智能不單止係 code，而是「身體 + 環境 + 即時互動」共同產生
- Gary 直播讓我真正感受到理論與現實的距離已經非常近
- Week 1 最大收穫：從抽象概念到可視化 Demo + 真實案例，全流程走通

## 下週目標 (Week 2)
- Principles of Robotic Mechanisms + Advanced Product Mechatronics
- 開始研究機械臂運動學 + 系統整合

Week 1 Done! 🚀 
更新日期：2026-05-15