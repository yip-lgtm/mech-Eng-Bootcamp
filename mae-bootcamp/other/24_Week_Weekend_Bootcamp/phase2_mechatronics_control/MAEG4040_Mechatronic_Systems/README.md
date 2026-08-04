# MAEG4040 Mechatronic Systems

**Phase 2 | Priority: ⭐⭐⭐⭐⭐**  
**Why critical**: The integration discipline that turns separate mechanical, electronic, control and software parts into a working robot. Directly maps to your Hybrid Arm + Soft Gripper project.

---

## 1. 5 Core Mental Models Every Expert Shares

1. **Concurrent Design, Not Sequential** — Mechanical, electrical, control and software decisions must be made together; late changes are expensive.
2. **Information Flow is as Important as Energy Flow** — Sensors, communication, and computation are first-class citizens, not afterthoughts.
3. **Hierarchy of Control** — From low-level current/torque loops up to task and supervisory levels; each layer has different bandwidth and abstraction.
4. **Real-Time and Determinism Matter** — Correctness includes timing; a late correct answer can be as bad as a wrong one.
5. **Interfaces and Modularity Determine Complexity** — Clean interfaces (electrical, mechanical, software) allow independent development and testing.

---

## 2. 3 Places Experts Fundamentally Disagree

### Disagreement 1: Model-Based Design vs Rapid Prototyping / Agile Hardware
- **Model-based camp**: High-fidelity simulation and formal methods catch errors early and scale to complex systems.
- **Agile / prototype camp**: Real hardware reveals issues that models miss; fast iteration with physical prototypes is more reliable for novel mechatronic devices (especially soft robots).

### Disagreement 2: Centralised vs Distributed Control Architectures
- **Centralised**: Easier to reason about, single point of truth, simpler for small systems.
- **Distributed**: Better scalability, fault tolerance, and modularity; required for multi-robot or highly sensor-rich systems.

### Disagreement 3: How Much Domain Knowledge vs General Systems Engineering
- **Domain-heavy**: Deep knowledge of mechanics, power electronics and control is irreplaceable.
- **Systems-first**: The hard problems are integration, interfaces, and requirements management; domain experts can be consulted as needed.

---

## 3. 10 Questions that Distinguish Deep Understanding

1. Why is “throwing the design over the wall” from mechanical to electrical to software almost always a failure mode?
2. What makes a sensor interface “clean”, and how do you test it in isolation?
3. How do you decide the sampling rate and control bandwidth hierarchy for a multi-loop robot system?
4. Explain the difference between hard real-time and soft real-time requirements with a concrete robot example.
5. When would you choose a single powerful central controller versus multiple distributed microcontrollers?
6. How does the concept of a “digital twin” change the mechatronic design process?
7. What are the typical failure modes at the mechanical–electrical interface (connectors, grounding, EMI)?
8. How would you systematically bring up a new hybrid rigid–soft system from power-on to first controlled motion?
9. Why is version control and automated testing still rare (but increasingly critical) in mechatronic projects?
10. In your soft gripper + 3R arm, which design decisions are truly concurrent and which can still be sequential?

---

## Link to Your Hybrid System
- Your current architecture (Arduino/ESP + state machine + force/pressure loops + 3R arm) is a classic mechatronic integration problem.
- Improving modularity (clear sensor, actuator, and communication interfaces) will make future upgrades far easier.
- The state machine (APPROACH → … → RELEASE) is the supervisory layer of a mechatronic control hierarchy.

## Status
- [ ] Theory notes completed
- [ ] Current hybrid system architecture diagram drawn
- [ ] Interface list (electrical, mechanical, software) documented
- [ ] Bring-up and test procedure refined
