# MAEG4030 Heat Transfer

**Phase 2 | Priority: ★★★**  
**Why critical**: Thermal management of motors, drivers, electronics and soft actuators — overheating kills robots.

---

## 1. 5 Core Mental Models Every Expert Shares

1. **Three Modes, One Conservation Law** — Conduction, convection and radiation; energy balance still rules.
2. **Thermal Resistance Networks** — Analogous to electrical circuits; estimate temperature drops quickly.
3. **Biot and Fourier Numbers Guide Lumped vs Distributed Models** — Tell you when a simple lumped model is acceptable.
4. **Convection is an Interface Phenomenon** — The coefficient h hides complex fluid behaviour.
5. **Transient vs Steady State Matter Differently** — Duty cycles and thermal time constants often dominate ratings.

---

## 2. 3 Places Experts Fundamentally Disagree

### Disagreement 1: Analytical Correlations vs CFD for Convection
- Correlations are fast and sufficient for many cases. CFD is needed for complex geometries but requires validation.

### Disagreement 2: How Much Radiation Detail at Typical Mechatronic Temperatures
- Often secondary below ~100–150 °C. Critical for high-temperature actuators or precision thermal control.

### Disagreement 3: Lumped Models vs Full Transient Simulation Early
- Lumped enables rapid iteration. Full simulation is needed once geometry and duty cycle are fixed.

---

## 3. 10 Questions that Distinguish Deep Understanding

1. Why can two surfaces at the same temperature still exchange net radiative heat?
2. What does Biot number ≪ 1 mean for a motor housing?
3. How would you estimate steady-state temperature rise of a motor given power loss and a heat sink?
4. Why is forced convection usually far more effective than natural convection for electronics?
5. When is the lumped-capacity assumption invalid for a soft-actuator wall during rapid cycling?
6. Physical meaning of thermal diffusivity, and why it appears in transient problems?
7. How do contact resistances arise, and how can you reduce them?
8. Why do we often care more about maximum junction temperature than average PCB temperature?
9. In a pneumatic soft gripper, where are the main heat sources and sinks during repeated cycling?
10. How would you decide whether active cooling is required for your arm’s motor drivers?

---

## Link to Your Hybrid System
- Motor drivers, continuous operation and soft-actuator cycling all have thermal limits.

## Status
- [ ] Theory notes completed
- [ ] Rough thermal estimate for current drivers
- [ ] Practice problems done
