# MAEG3040 Mechanical Design

**Phase 2 | Priority: ★★★★**  
**Why critical**: Systematic design of machine elements, failure prevention, and the decisions that turn a kinematic concept into a reliable robot.

---

## 1. 5 Core Mental Models Every Expert Shares

1. **Function Before Form** — Clarify the required function, constraints and interfaces before sketching geometry.
2. **Load Paths and Stress Flow** — Forces must travel continuously through the structure to ground; interruptions create stress concentrations.
3. **Failure Modes are Predictable** — Yield, fracture, fatigue, wear, buckling, creep — each has models and design rules.
4. **Factor of Safety is a Decision Under Uncertainty** — It encodes ignorance of loads, material, and consequences of failure.
5. **Iteration is the Real Design Process** — Concept → analysis → redesign is the normal loop, not a linear waterfall.

---

## 2. 3 Places Experts Fundamentally Disagree

### Disagreement 1: Calculation-Heavy vs Catalogue / Standard-Component Design
- **Calculation**: necessary for novel or critical parts. **Catalogue**: faster, more reliable for standard machine elements when available.

### Disagreement 2: How Early to Introduce Fatigue and Fracture Mechanics
- **Early**: most real failures are fatigue. **Later**: static strength must be solid first.

### Disagreement 3: CAD-Centric vs Hand-Sketch + First-Principles First
- **CAD** enables complex geometry and FEA. **Hand methods** build judgment and prevent ‘pretty but wrong’ designs.

---

## 3. 10 Questions that Distinguish Deep Understanding

1. Why is a sharp internal corner almost always a fatigue initiation site?
2. How do you decide between a bolted joint and a welded joint for a robot frame?
3. What is the difference between a safe-life and a fail-safe design philosophy?
4. Explain why the endurance limit concept is controversial for some materials and loading types.
5. When would you deliberately design a component to be the ‘weak link’ in a load path?
6. How does the choice of bearing type affect the overall stiffness and accuracy of a robot joint?
7. What information must you have before you can meaningfully apply a factor of safety?
8. Why do press fits and shrink fits create residual stresses, and when is that beneficial?
9. In your 3R arm, which components are most likely to be fatigue-critical and why?
10. How would you systematically reduce the part count of a mechanical assembly without losing function?

---

## Link to Your Hybrid System
- Apply to 3R arm links, joints, base and gripper mounting.
- Use failure-mode thinking when deciding materials and cross-sections.

## Status
- [ ] Theory notes completed
- [ ] Linked to arm mechanical design
- [ ] Practice problems or mini-project done
