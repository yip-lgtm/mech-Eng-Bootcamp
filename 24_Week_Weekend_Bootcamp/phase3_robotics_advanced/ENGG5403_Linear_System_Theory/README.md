# ENGG5403 Linear System Theory and Design

**Phase 3 | Priority: ★★★★**  
**Why critical**: Rigorous foundation for modern control — controllability, observability, realizations and optimal design.

---

## 1. 5 Core Mental Models Every Expert Shares

1. **State is the Minimal Predictive Information** — Past inputs are irrelevant once the state is known (for linear Markov systems).
2. **Controllability and Observability are Structural** — They depend on the pair (A,B) or (A,C), not on a particular coordinate system.
3. **Realizations are Not Unique** — Many state-space models can represent the same input–output behaviour; canonical forms organise them.
4. **Stability, Performance and Robustness Trade Off** — You cannot optimize all three without limit.
5. **Frequency Domain and State Space are Complementary Views** — Transfer functions and state-space each reveal different aspects.

---

## 2. 3 Places Experts Fundamentally Disagree

### Disagreement 1: How Abstract the First Course Should Be
- Abstract: prepares for infinite-dimensional and advanced topics. Concrete: keeps engineers engaged with Rⁿ and standard examples.

### Disagreement 2: Optimal Control (LQR) vs Robust Control as the Capstone
- LQR is elegant and widely used. Robust methods address real uncertainty more directly.

### Disagreement 3: Continuous-Time vs Discrete-Time Emphasis
- Continuous is the classical theory. Discrete is what digital controllers actually implement.

---

## 3. 10 Questions that Distinguish Deep Understanding

1. Why can a system be stabilisable without being fully controllable?
2. What does the controllability matrix rank condition actually guarantee?
3. How do you convert a transfer function into a controllable canonical form realization?
4. Why are eigenvalues of A invariant under similarity transformation?
5. What is the dual relationship between controllability and observability?
6. How does the algebraic Riccati equation encode an optimal trade-off?
7. When is a minimal realization important, and how do you obtain one?
8. What is the difference between internal stability and BIBO stability?
9. How would you check observability of your soft-gripper pressure and force loops?
10. Why does pole placement alone not guarantee good robustness margins?

---

## Link to Your Hybrid System
- Deepens MAEG4050; supports rigorous design of joint and pressure controllers.

## Status
- [ ] Theory notes completed
- [ ] Simple state-space model of arm + gripper
- [ ] Practice problems done
