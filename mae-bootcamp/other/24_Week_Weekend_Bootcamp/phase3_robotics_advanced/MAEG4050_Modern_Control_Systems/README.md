# MAEG4050 Modern Control Systems

**Phase 3 | Priority: ⭐⭐⭐⭐⭐**  
**Why critical**: State-space methods, observability, controllability, optimal control — the language of advanced robot control and soft-system closed loops.

---

## 1. 5 Core Mental Models Every Expert Shares

1. **State is the Minimal Information that Predicts the Future** — Once you have the state, past inputs are irrelevant for future evolution (for Markovian systems).
2. **Controllability and Observability are Dual Structural Properties** — They tell you whether you can drive the state anywhere and whether you can reconstruct it from outputs.
3. **Linear State-Space is the Gateway to Almost Everything Else** — Nonlinear, robust, adaptive, and optimal methods all build on or linearize around this framework.
4. **Feedback Changes the Eigenvalues** — The fundamental act of control is relocating the closed-loop poles (or shaping the singular values).
5. **Models are Always Wrong; Some are Useful** — Uncertainty, unmodelled dynamics, and noise are inevitable; good design accounts for them explicitly.

---

## 2. 3 Places Experts Fundamentally Disagree

### Disagreement 1: Classical Frequency-Domain vs Modern State-Space as the Primary Framework
- **Classical camp**: Bode, Nyquist, and root locus give unmatched intuition for loop shaping and robustness margins; still the daily language of many practising engineers.
- **Modern camp**: State-space scales naturally to MIMO, time-varying, and optimal control; it is the proper foundation for contemporary robotics and soft systems.

### Disagreement 2: LQR / LQG as the Default Optimal Controller vs More Advanced Robust Methods
- **LQR/LQG camp**: Simple, elegant, widely implemented, and often “good enough” when the model is decent and noise is well-characterised.
- **Robust camp**: Real plants have structured and unstructured uncertainty; H∞, μ-synthesis, or tube-based MPC are required for guaranteed performance.

### Disagreement 3: How Much Nonlinear Control Should Be Taught Alongside Linear Modern Control
- **Linear-first**: Master linear theory thoroughly; most industrial systems operate near operating points where linearisation works.
- **Early nonlinear**: Soft robots, contact, and large-motion manipulators are inherently nonlinear; students need Lyapunov and feedback linearisation early.

---

## 3. 10 Questions that Distinguish Deep Understanding

1. Why can a system be stabilisable even if it is not fully controllable?
2. What is the physical meaning of the controllability Gramian, and how does it relate to the energy needed to reach a state?
3. Explain why pole placement alone does not guarantee good robustness.
4. How does the separation principle allow you to design a state-feedback controller and an observer independently?
5. What happens to LQR performance when the model used for design differs significantly from the real plant?
6. Why is the Kalman filter the dual of the LQR controller?
7. In what sense does the algebraic Riccati equation encode an optimal trade-off between control effort and state regulation?
8. How would you check whether your soft-gripper pressure loop + force feedback system is observable from the sensors you have?
9. Why do we often prefer state-space realisations that are balanced or in controllable canonical form?
10. What is the fundamental limitation that prevents arbitrarily fast closed-loop response even with perfect state feedback?

---

## Link to Your Hybrid System
- Your existing PID loops can be re-interpreted and improved in state-space form.
- Force + pressure closed-loop design for the soft gripper benefits from observability and robustness analysis.
- Trajectory tracking and future impedance / hybrid force-motion control sit naturally in this framework.

## Status
- [ ] Theory notes completed
- [ ] State-space model of 3R arm + gripper derived
- [ ] Simple LQR or pole-placement controller tested in simulation
- [ ] Observability check of current sensor suite
