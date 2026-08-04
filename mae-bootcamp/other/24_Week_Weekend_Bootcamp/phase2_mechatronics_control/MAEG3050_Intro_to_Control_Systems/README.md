# MAEG3050 Introduction to Control Systems

**Phase 2 | Priority: ⭐⭐⭐⭐⭐**  
**Why critical**: Foundation of all closed-loop control in the hybrid arm + gripper (PID, stability, root locus, frequency domain).

---

## 1. 5 Core Mental Models Every Expert Shares

1. **Feedback is the Fundamental Idea** — The essence of control is using measured output to correct the input, not open-loop precision.
2. **Stability is a System Property, not a Controller Property** — A controller can stabilize or destabilize the same plant depending on gain and dynamics.
3. **Time Domain ↔ Frequency Domain Duality** — Transient response and frequency response are two views of the same linear system.
4. **Poles Determine the Nature of the Response** — Location of closed-loop poles tells you stability, speed, and damping almost at a glance.
5. **Models are Always Approximations** — Linearization, order reduction, and neglected dynamics are inevitable; good control design accounts for model uncertainty.

---

## 2. 3 Places Experts Fundamentally Disagree

### Disagreement 1: Classical (Root Locus / Frequency) vs Modern (State-Space) as First Approach
- **Classical camp**: Root locus and Bode plots give unmatched intuition for single-loop design and are still the language of practicing engineers.
- **Modern camp**: State-space is more general, scales to MIMO, and is the natural language of optimal and robust control.

### Disagreement 2: How Much Model Uncertainty Should Be Explicitly Designed For in a First Course
- **Robustness early**: Students must learn that real plants differ from models; introduce gain/phase margins and basic robust ideas immediately.
- **Nominal first**: Master nominal design thoroughly before adding the complexity of uncertainty.

### Disagreement 3: Role of PID in Modern Control Education
- **PID still king**: The vast majority of industrial loops are still PID; students must deeply understand tuning and limitations.
- **PID is a special case**: Treat PID as one possible controller structure inside a broader state-space or optimal framework.

---

## 3. 10 Questions that Distinguish Deep Understanding

1. Why can increasing proportional gain make a system both faster and less stable at the same time?
2. What does a phase margin of 30° physically mean for the time response of a system?
3. Why is the Routh-Hurwitz criterion only a necessary and sufficient condition for stability of linear systems, and what does it miss?
4. How does the concept of “dominant poles” justify reducing a high-order system to second-order for design?
5. In what sense is a PID controller a lead-lag compensator, and when is that view useful?
6. Why does derivative control amplify noise, and what practical fixes exist?
7. Explain why the same plant can be stabilized by high-gain feedback in one frequency range and destabilized in another.
8. What is the fundamental limitation that prevents arbitrarily fast closed-loop response for a given plant?
9. How would you use root locus thinking to decide whether a soft-gripper pressure loop needs a lag compensator?
10. Why can a system have good stability margins yet still exhibit unacceptable transient response?

---

## Link to Your Hybrid System
- Your existing PID joint controllers and pressure control loops are direct applications of this course.
- Stability analysis of the force + pressure closed loops should use the tools from this course.
- Future trajectory tracking and impedance control build on these foundations.

## Status
- [ ] Theory notes completed
- [ ] Linked to existing PID implementation
- [ ] Root locus / Bode analysis of current arm controllers
