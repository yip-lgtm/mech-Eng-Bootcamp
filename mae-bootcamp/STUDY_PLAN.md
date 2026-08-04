# BEng Mechanical and Automation Engineering — Study Plan (CUHK)

> **Programme:** BEng Mechanical and Automation Engineering
> **University:** The Chinese University of Hong Kong (CUHK)
> **Source:** https://www4.mae.cuhk.edu.hk/mechanical-and-automation-engineering/
> **Status:** Self-Study Reference | Last Updated: 2026-08

---

## Programme Overview

The MAE Programme emphasizes the impact of modern automation technologies on current and future developments in mechanical engineering. Balanced curriculum in both basic theory and hands-on practice, covering:

- Mechanics and Materials
- Thermodynamics
- Mechanical Design
- Manufacturing Processes
- Mechatronics and Robotics

### Credits Summary

| Category | Units | Notes |
|---|---|---|
| **Faculty Package** | **9** | ENGG1110, ENGG1120, ENGG1130, MATH1510, PHYS1110 |
| Foundation Courses | 13 | Math, physics, computational design |
| Major Required Courses | 33 | Core mechanical/automation knowledge |
| Research Component | 6 | FYP I + II |
| Major Electives | 14+ | Specialized streams (≥5 to graduate) |
| **Total** | **~75 units** | Standard 4-year BEng |

---

## Year 1 — Faculty Package (Semesters 1 & 2)

**Focus:** Programming, linear algebra, calculus, physics — the universal engineering toolkit

| Semester | Course | Title | Deep Study Format (5MM/3DG/10Q/5DD/10SL/5MR) |
|---|---|---|---|
| 1 | ENGG1110 | Problem Solving By Programming | ✅ |
| 1 | ENGG1120 | Linear Algebra for Engineers | ✅ |
| 1 | MATH1510 | Calculus for Engineers | ✅ |
| 2 | ENGG1130 | Multivariable Calculus for Engineers | ✅ |
| 2 | PHYS1110 | Engineering Physics: Mechanics & Thermo | ✅ |

All 5 Faculty Package courses now have full research-based content. See `courses/faculty-package/`.

**Projects:** Arduino LED sequence → Python kinematics → CAD first part

---

## Year 2 — Foundation + Core Mechanics

**Focus:** Math, physics, programming, first mechanism intuition

| Semester | Course | Title |
|---|---|---|
| 1 | ENGG1110 | Problem Solving By Programming |
| 1 | ENGG1120 | Linear Algebra for Engineers |
| 1 | MATH1510 | Calculus for Engineers |
| 1 | PHYS1110 | Engineering Physics: Mechanics & Thermo |
| 1 | — | University Core (EL/CL/GE/PE) |
| 2 | ENGG1130 | Multivariable Calculus for Engineers |
| 2 | MAEG1020 | Computational Design and Fabrication |
| 2 | MAEG2020 | Engineering Mechanics |
| 2 | — | University Core |

**Projects:** Arduino LED sequence → inverse kinematics in Python → CAD first part

---

## Year 2 — Core Mechanics + Circuits + Thermo

**Focus:** Build the mechanical + electrical foundation. Link theory to mechatronics.

| Semester | Course | Title |
|---|---|---|
| 1 | MAEG3010 | Mechanics of Materials |
| 1 | ELEG2202 | Fundamentals of Electric Circuits |
| 1 | MAEG2030 | Thermodynamics |
| 1 | MAEG2601 | Technology, Society and Engineering Practice |
| 2 | MAEG3020 | Manufacturing Technology |
| 2 | MAEG3030 | Fluid Mechanics |
| 2 | MAEG3040 | Mechanical Design |

**Projects:** Stress analysis of gripper link → circuit driver for DC motor → heat dissipation design for actuator

---

## Year 3 — Control + Robotics + Manufacturing + Electives

**Focus:** Control systems, robotics fundamentals, mechatronics integration. Heavy hands-on.

| Semester | Course | Title |
|---|---|---|
| 1 | MAEG3050 | Introduction to Control Systems |
| 1 | MAEG4030 | Heat Transfer |
| 1 | MAEG3060 | Introduction to Robotics *(highly recommended)* |
| 1 | MAEG2050 | Robot Development in Practice *(highly recommended)* |
| 2 | MAEG4040 | Mechatronic Systems |
| 2 | MAEG4010 | Computer-Integrated Manufacturing |
| 2 | MAEG4020 | Finite Element Analysis |

**Projects:** 3R arm forward/inverse kinematics → PID controller for motor speed → workspace analysis → state machine for warehouse robot

---

## Year 4 — FYP + Advanced Electives + Specialization

**Focus:** Final Year Project, advanced topics, specialization stream.

| Semester | Course | Title |
|---|---|---|
| 1 | MAEG4998 | Final Year Project I |
| 1 | — | Advanced electives (see streams below) |
| 2 | MAEG4999 | Final Year Project II |
| 2 | — | Remaining electives |

**FYP:** Physical prototype or advanced simulation — warehouse picking robot, soft gripper with tactile sensing, multi-agent coordination.

---

## Elective Streams

Choose ≥5 electives to graduate. Recommended paths:

### Stream A: Robotics & Automation 🤖
- MAEG3060 Introduction to Robotics
- MAEG4050 Modern Control Systems
- MAEG5060 Computational Intelligence
- MAEG5070 Nonlinear Control
- MAEG5090 Topics in Robotics
- MAEG5110 Quantum Control
- BMEG3420 Medical Robotics
- ENGG5402 Advanced Robotics
- ENGG5403 Linear System Theory

### Stream B: Design & Manufacturing 🔧
- MAEG4010 Computer-Integrated Manufacturing
- MAEG4020 Finite Element Analysis
- MAEG4060 Design for Manufacture
- MAEG4070 Advanced Manufacturing Processes
- MAEG5160 Design for Additive Manufacturing
- CSCI1020 Computer-Aided Design
- ENGG5404 MEMS and Nanotechnology

### Stream C: Energy & Sustainability ⚡
- EEEN2020 Renewable Energy Systems
- EEEN4010 Energy Harvesting
- EEEN4020 Photovoltaic Technology
- EEEN4030 Nuclear Energy Safety
- EEEN4050 Energy Storage Systems
- MAEG4080 Combustion Engineering
- MAEG5150 Advanced Heat Transfer

### Stream D: Software & AI 💻
- CSCI2040 C++ Object-Oriented Programming
- CSCI2100 Data Structures
- MAEG3080 Machine Intelligence
- MAEG5060 Computational Intelligence
- ENGG2760 Engineering Probability

### Stream E: Business & Management 📊
- MGNT1010 Introduction to Business
- SEEM2440 Engineering Economy
- SEEM3450 Technology Innovation and Entrepreneurship
- MGNT4090 Technology Innovation Management

See `courses/electives/` for full course content. Use `courses/COURSE_INDEX.md` to browse by stream.

---

## Personal Project Roadmap

| Timeline | Goal |
|---|---|
| Year 1–2 | Build foundation → Arduino LED → Python kinematics → CAD |
| Year 2–3 | Integrate state machine → Agent Loop → warehouse demo |
| Year 3–4 | Physical prototype or advanced simulation with learning |
| FYP | Full system: perception → planning → control → actuation |

---

## Links

- CUHK MAE Dept: https://www4.mae.cuhk.edu.hk/mechanical-and-automation-engineering/
- Course Index: `./courses/COURSE_INDEX.md`
- Electives: `./courses/electives/`
- Major Required: `./courses/major-required/`
- Foundation: `./courses/foundation/`
