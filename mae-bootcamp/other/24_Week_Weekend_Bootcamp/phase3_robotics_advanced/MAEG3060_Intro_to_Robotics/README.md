# MAEG3060 Introduction to Robotics

**Phase 3 | Priority: ⭐⭐⭐⭐⭐**  
**Why critical**: Core of robot kinematics, dynamics, and control. Direct foundation for your 3R arm + future manipulators.

---

## 1. 5 Core Mental Models Every Expert Shares

1. **Configuration Space (C-space)** — The real space a robot lives in is the space of its joint configurations, not Cartesian space. Obstacles, singularities, and paths must be understood in C-space.
2. **Forward vs Inverse Kinematics are Dual Problems** — FK is unique and straightforward (product of transforms). IK is often multi-valued, non-linear, and may have no solution or infinite solutions.
3. **Jacobian is the Bridge** — It maps joint velocities to end-effector velocities and reveals singularities, manipulability, and force transmission.
4. **Serial vs Parallel Architectures Trade Precision, Workspace, and Stiffness** — Most industrial arms are serial; many precision or high-force devices are parallel or hybrid.
5. **Kinematics First, then Dynamics, then Control** — Geometry of motion must be mastered before forces, and both before designing stable controllers.

---

## 2. 3 Places Experts Fundamentally Disagree

### Disagreement 1: Analytical IK vs Numerical IK as Primary Approach
- **Analytical camp**: Closed-form solutions (when they exist) are fast, exact, and give insight into the number and nature of solutions. Prefer them for common 6R industrial arms.
- **Numerical camp**: Most modern robots (7-DOF, redundant, continuum, soft) have no closed form. Numerical methods (Newton, damped least-squares, optimization) are more general and robust.

### Disagreement 2: DH Parameters vs Product-of-Exponentials (PoE) / Screw Theory
- **DH camp**: Classic, widely taught, sufficient for most serial manipulators, easy to implement in code.
- **PoE / Screw Theory camp**: More elegant, singularity-free representation of rigid motion, better for advanced dynamics, calibration, and continuum robots. Should be the modern foundation.

### Disagreement 3: How Early to Emphasize Singularity Handling and Redundancy Resolution
- **Early emphasis**: Singularities and redundancy are central practical problems; students should confront them from the first IK exercises.
- **Later emphasis**: First master non-singular, non-redundant cases thoroughly; otherwise students get lost in special cases.

---

## 3. 10 Questions that Distinguish Deep Understanding

1. Why can a 6-DOF serial arm have up to 16 inverse kinematic solutions, and what geometric features determine the actual number?
2. What does a singularity of the Jacobian physically mean for the robot’s ability to move and to resist forces?
3. Explain why the inverse of the Jacobian is almost never used directly in real-time control.
4. How does the concept of manipulability ellipsoid help you choose a good posture for a given task?
5. Why is the Product-of-Exponentials formulation often preferred for calibration and continuum robots over classical DH?
6. In what sense is the forward kinematic map a many-to-one function while the inverse is one-to-many?
7. How would you systematically resolve redundancy for a 7-DOF arm when the primary task is end-effector pose tracking?
8. What is the difference between a kinematic singularity and a representation singularity (e.g., Euler angles)?
9. Why does a closed-chain (parallel) robot typically have a more complicated forward kinematics problem than inverse kinematics?
10. How would you use the Jacobian transpose method for force control, and under what conditions does it work well?

---

## Link to Your Hybrid System
- Your 3R arm FK is a direct application of successive homogeneous transforms.
- Future IK for the arm (and soft gripper base pose) will use the ideas above.
- Singularity awareness is critical when planning trajectories near workspace boundaries.

## Status
- [ ] Theory notes completed
- [ ] FK verified against simulator
- [ ] Basic numerical IK implemented
- [ ] Jacobian + singularity analysis of current 3R design
