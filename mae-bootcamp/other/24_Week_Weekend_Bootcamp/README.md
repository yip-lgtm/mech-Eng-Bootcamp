# 24-Week Self-Study Bootcamp  
## CUHK BEng Mechanical & Automation Engineering + PolyU MSc Intelligent Robotics Engineering

**Goal**: Systematically master ~74 courses across both programmes through deep conceptual understanding, not rote memorization.

**Method** (applied to **every course**):

1. **5 Core Mental Models** — What every expert in this field shares  
2. **3 Fundamental Disagreements** — Where experts diverge + strongest arguments on each side  
3. **10 Deep Questions** — Questions that expose real understanding vs surface memorization  

---

## Programme Overview

| Programme | Focus | Approx. Courses |
|-----------|-------|-----------------|
| **CUHK BEng MAE** | Foundations → Mechatronics → Robotics → FYP | ~60+ units worth of core + electives |
| **PolyU MSc IRE** | Embodied AI, Mechanisms, Motion Planning, Soft Robotics, Advanced Control, Mechatronics | 6 cores + electives |

**Target**: Build a working **Hybrid 3R Rigid Arm + Soft Gripper + Warehouse Agent** system while covering the academic content.

---

## Structure

```
24_Week_Weekend_Bootcamp/
├── phase1_foundations/          # Week 1–6   Math, Physics, Mechanics, Materials, Circuits
├── phase2_mechatronics_control/ # Week 7–12  Control, Design, Manufacturing, Fluid, Heat, Mechatronics
├── phase3_robotics_advanced/    # Week 13–18 Robotics, Soft Robotics, Advanced Control, AI, Vision
├── phase4_integration_fyp/      # Week 19–24 FYP, Integration, Electives, Portfolio
├── demos/                       # Simulations (3R arm, soft gripper, hybrid, warehouse)
├── builds/                      # Physical builds (soft gripper, molds, firmware)
├── skill/                       # OpenClaw / automation helpers
└── progress.md
```

Each course folder contains a `README.md` with the fixed 3-part deep-learning format.

---

## Priority Order (Star Courses First)

### Phase 1 – Foundations
- **MAEG2020** Engineering Mechanics ⭐⭐⭐⭐⭐
- ENGG1110 / 1120 / 1130, MATH1510, PHYS1110
- MAEG3010 Mechanics of Materials
- ELEG2202 Electric Circuits

### Phase 2 – Mechatronics & Control
- **MAEG3050** Intro to Control Systems ⭐⭐⭐⭐⭐
- **MAEG4040** Mechatronic Systems ⭐⭐⭐⭐⭐
- MAEG3040 Mechanical Design, MAEG3020 Manufacturing

### Phase 3 – Robotics & Advanced (PolyU MSc Core Alignment)
- **Soft Robotics** ⭐⭐⭐⭐⭐ (already strong)
- **MAEG3060** Intro to Robotics ⭐⭐⭐⭐⭐
- **MAEG4050** Modern Control Systems ⭐⭐⭐⭐⭐
- MAEG5080 Smart Materials
- MAEG2050 Robot Development in Practice
- Embodied Robot Intelligence / Motion Planning / Advanced Control (map to existing + new folders)

### Phase 4 – Integration & FYP
- **MAEG4998 / 4999** FYP I & II ⭐⭐⭐⭐⭐
- Integration of Hybrid Arm + Soft Gripper + Agent
- Portfolio & documentation

---

## Learning Protocol for Every Course

For each course README:

1. Read the **5 Mental Models** — internalize the expert worldview  
2. Study the **3 Disagreements** — understand the live debates  
3. Attempt the **10 Deep Questions** without notes  
4. Only then write notes / code / simulator updates  
5. Link back to the physical Hybrid system whenever possible  

---

## Current Simulator & Hardware Focus

- 3R Rigid Arm (kinematics → dynamics → PID → trajectory)
- Soft Pneumatic Gripper (PCC model → force/pressure control → state machine)
- Hybrid integration (APPROACH → SOFT_CONTACT → GRIP → HOLD → LIFT → RELEASE)
- Warehouse Agent + future LLM thinking layer

---

## How to Use This Repo

1. Start from `phase1_foundations/MAEG2020_Engineering_Mechanics`
2. Follow the 3-part method for every course
3. Update `progress.md` after each course
4. Continuously improve `demos/` and `builds/`
5. Use weekend blocks (Sat theory + practice, Sun reflection + commit)

---

**Repo**: [yip-lgtm/Master-of-Science-in-Intelligent-Robotics-Engineering](https://github.com/yip-lgtm/Master-of-Science-in-Intelligent-Robotics-Engineering)

**Last major restructure**: 2026-07-30
