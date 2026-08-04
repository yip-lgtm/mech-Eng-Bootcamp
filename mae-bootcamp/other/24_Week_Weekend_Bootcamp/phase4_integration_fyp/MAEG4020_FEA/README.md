# MAEG4020 Finite Element Modelling and Analysis

**Phase 4 | Priority: ★★★★**  
**Why critical**: Numerical stress, thermal and modal analysis for structures and soft bodies that lack simple closed-form solutions.

---

## 1. 5 Core Mental Models Every Expert Shares

1. **Discretisation Approximates the Continuum** — Elements and nodes turn PDEs into algebraic systems; accuracy depends on mesh and element choice.
2. **Boundary Conditions Dominate Results** — Wrong supports or loads produce confident but useless answers.
3. **Verification and Validation are Separate** — Verification: solving the equations correctly. Validation: solving the right equations for reality.
4. **Mesh Convergence is Mandatory** — If refining the mesh changes the answer significantly, you do not yet have a reliable result.
5. **Linear is the Gateway; Nonlinearity is the Reality** — Contact, large deformation and material nonlinearity appear quickly in robots and soft devices.

---

## 2. 3 Places Experts Fundamentally Disagree

### Disagreement 1: How Early to Trust Commercial FEA Without Deriving Elements
- Early trust enables practical design. Deep derivation prevents misuse of black-box software.

### Disagreement 2: Linear Static as Default vs Early Exposure to Contact and Large Deformation
- Linear static is the foundation. Soft robots and grippers immediately need nonlinear capability.

### Disagreement 3: FEA vs Experimental Testing Priority
- FEA reduces physical prototypes. Testing remains the final authority for critical parts.

---

## 3. 10 Questions that Distinguish Deep Understanding

1. Why can a fine mesh still give a wrong answer if boundary conditions are wrong?
2. What is the difference between h-refinement and p-refinement?
3. When is a shell element preferable to a solid element for a robot link?
4. How do you check mesh convergence for a stress concentration?
5. What does a singular stress at a sharp re-entrant corner mean, and how do you interpret it?
6. How would you model the contact between a soft gripper finger and a rigid object?
7. Why is nonlinear geometry important for thin or highly deformable structures?
8. How do you validate an FEA model of a 3R arm link against experiment?
9. What material model would you choose for Ecoflex in a soft-actuator simulation?
10. In your hybrid system, which component is the highest priority for FEA and why?

---

## Link to Your Hybrid System
- Arm links, mounts and soft gripper walls are natural FEA subjects.
- Use FEA to check stress under payload and to explore soft-actuator chamber designs.

## Status
- [ ] Theory notes completed
- [ ] Simple FEA of one arm link or gripper section
- [ ] Practice problems done
