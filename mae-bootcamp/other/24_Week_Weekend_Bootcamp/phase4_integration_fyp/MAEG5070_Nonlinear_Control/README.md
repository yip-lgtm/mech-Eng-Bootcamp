# MAEG5070 Nonlinear Control Systems

**Phase 4 | Priority: ★★★**  
**Why critical**: Lyapunov methods, feedback linearization and sliding mode — tools for real plants that leave the linear regime.

---

## 1. 5 Core Mental Models Every Expert Shares

1. **Equilibria and Their Stability are Local Notions** — Global behaviour can be very different from linearisation.
2. **Lyapunov Functions are Certificates** — Finding a suitable energy-like function proves stability without solving the ODE.
3. **Feedback Can Cancel or Dominate Nonlinearity** — Feedback linearization and high-gain / sliding designs are two major strategies.
4. **Invariant Sets and Ultimate Boundedness** — Practical goals are often “stay near a set” rather than asymptotic convergence to a point.
5. **Robustness Must Be Designed In** — Model error and disturbance are the norm; pure cancellation is fragile.

---

## 2. 3 Places Experts Fundamentally Disagree

### Disagreement 1: Feedback Linearization vs Lyapunov / Passivity-Based Design
- Feedback linearization is systematic when the model is accurate. Lyapunov and passivity methods often degrade more gracefully under uncertainty.

### Disagreement 2: How Early to Leave Linear Control
- Master linear methods thoroughly first. Introduce nonlinearity early because most real robots need it.

### Disagreement 3: Analytical Nonlinear Design vs Numerical / Learning Approaches
- Analytical design gives insight and guarantees. Numerical and learning methods scale to higher complexity.

---

## 3. 10 Questions that Distinguish Deep Understanding

1. Why can a linearisation be stable while the nonlinear system is not (or vice versa)?
2. What is the difference between Lyapunov stability, asymptotic stability and exponential stability?
3. How do you construct a Lyapunov function for a simple mechanical system?
4. When is feedback linearization applicable, and what are its main practical limitations?
5. What is a sliding surface, and why does sliding mode control offer robustness?
6. How does the concept of passivity help in designing robot interaction controllers?
7. What is input-to-state stability (ISS), and why is it useful under disturbance?
8. How would you analyse stability of the soft-gripper pressure loop with a nonlinear valve characteristic?
9. Why are limit cycles possible in nonlinear systems but not in linear ones?
10. In your hybrid system, which nonlinearity is most important to treat explicitly rather than ignore?

---

## Link to Your Hybrid System
- Soft gripper pressure dynamics, contact and friction are nonlinear.
- Joint friction and actuator limits also push beyond pure linear PID.

## Status
- [ ] Theory notes completed
- [ ] One nonlinear effect in the system analysed
- [ ] Practice problems done
