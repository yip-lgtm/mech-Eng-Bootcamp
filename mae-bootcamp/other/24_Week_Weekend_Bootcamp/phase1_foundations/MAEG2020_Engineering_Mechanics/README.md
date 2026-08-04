# MAEG2020 Engineering Mechanics

**Phase 1 | Priority: ⭐⭐⭐⭐⭐**  
**Why critical**: Foundation of all robot kinematics, statics, dynamics for the 3R arm.

---

## 1. 5 Core Mental Models Every Expert Shares

1. **Free Body Diagram First** — Always isolate the system and draw all forces/moments before writing equations.
2. **Equilibrium is a Special Case of Dynamics** — ΣF = 0 and ΣM = 0 are just Newton’s 2nd law with a = 0.
3. **Kinematics before Kinetics** — Geometry of motion must be understood before forces that cause it.
4. **Work-Energy & Impulse-Momentum as Alternative Forms** — Same physics, different computational paths; choose the one that eliminates unknowns.
5. **Rigid Body Assumption is a Model** — Real bodies deform; know when the rigid-body idealization is valid.

---

## 2. 3 Places Experts Fundamentally Disagree

### Disagreement 1: Vector Mechanics vs Scalar / Energy Methods as Primary Teaching Path
- **Vector camp**: Forces and moments as vectors give the most general and scalable approach (especially in 3D and robotics).
- **Energy camp**: Work-energy methods are faster for many practical problems and build better intuition for conservative systems.

### Disagreement 2: How Early to Introduce 3D Rigid Body Dynamics
- **Early 3D**: Students need spatial thinking from day one for modern engineering.
- **2D first**: Master planar cases thoroughly before adding the complexity of 3D rotations and Euler angles.

### Disagreement 3: Role of Computational Tools (MATLAB / Python) in First Mechanics Course
- **Computation early**: Real problems are numerical; students should learn to verify analytical results with code.
- **Hand calculation first**: Symbolic understanding must precede numerical black boxes.

---

## 3. 10 Questions that Distinguish Deep Understanding

1. Why can the same rigid body have different moment of inertia values depending on the axis chosen?
2. When is the work-energy principle more powerful than Newton’s laws for a multi-body system?
3. Explain why static friction can do no work, yet is essential for rolling without slipping.
4. How does the concept of instantaneous center of rotation simplify kinematics of rigid bodies?
5. In what situations does the rigid-body assumption break down for a robot arm link?
6. Why is angular momentum about a fixed point conserved even if there are internal forces?
7. How would you systematically choose between force-moment equations and energy methods for a given problem?
8. What is the physical meaning of the product of inertia terms in the inertia tensor?
9. How does the distinction between kinetics and kinematics affect the design of a trajectory planner?
10. Why can a system be in equilibrium under a non-zero force system if the forces form a couple of zero moment?

---

## Link to Your 3R Arm
- Forward kinematics relies on successive coordinate transformations (rotation matrices from this course).
- Static force analysis of the arm under gravity or payload comes directly from equilibrium equations.
- Future dynamics (inertia, Coriolis) build on rigid-body kinetics.

## Status
- [ ] Theory notes completed
- [ ] Linked to 3R arm kinematics code
- [ ] Practice problems done
