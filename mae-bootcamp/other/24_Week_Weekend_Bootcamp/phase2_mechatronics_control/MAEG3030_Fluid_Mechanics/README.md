# MAEG3030 Fluid Mechanics

**Phase 2 | Priority: ★★★**  
**Why critical**: Essential for pneumatic soft actuators, hydraulic systems, and understanding flow, pressure and losses in your gripper.

---

## 1. 5 Core Mental Models Every Expert Shares

1. **Continuum Hypothesis** — We treat fluids as continuous media even though they are molecular. This enables the Navier–Stokes and Euler equations.
2. **Conservation Laws Govern Flow** — Mass, momentum and energy balances (in integral or differential form) are the starting point of every analysis.
3. **Dimensionless Numbers Reveal Regimes** — Reynolds, Mach, Froude, etc., tell you which forces dominate and which terms can be neglected.
4. **Bernoulli is a Special Case** — It is a statement of energy conservation along a streamline under strong assumptions; know when it fails.
5. **Boundary Layers and Separation Control Drag and Losses** — Most practical losses and forces originate near walls.

---

## 2. 3 Places Experts Fundamentally Disagree

### Disagreement 1: Analytical Solutions vs CFD as Primary Tool
- **Analytical**: builds deep understanding of simplified cases. **CFD**: necessary for real geometries, but can hide ignorance of the underlying physics.

### Disagreement 2: Compressible vs Incompressible Emphasis for Mechatronics
- **Incompressible** is sufficient for most liquid hydraulics and low-speed air. **Compressible** effects matter for fast pneumatic valves and high-speed exhaust.

### Disagreement 3: How Much Viscous Flow Theory Before Turbulence
- **Laminar theory first** for clarity. **Early turbulence**: most engineering flows are turbulent.

---

## 3. 10 Questions that Distinguish Deep Understanding

1. Why can Bernoulli’s equation not be applied across a shock wave or through a pump?
2. What does a high Reynolds number physically mean for the flow inside a soft-actuator air channel?
3. How does the concept of head loss influence the sizing of tubing and valves in a pneumatic gripper?
4. Explain the difference between static, dynamic and total pressure, and where each is measured.
5. When is the continuum assumption invalid for gas flow in micro-channels or MEMS valves?
6. Why does flow separation increase drag, and how do soft-robot designers sometimes exploit or avoid it?
7. What is the physical origin of the no-slip condition, and when does it break down?
8. How would you estimate the time to pressurize a soft gripper chamber of known volume?
9. Why are pneumatic systems often slower and less stiff than hydraulic systems of similar size?
10. In your soft gripper, which fluid-mechanics effects most limit the maximum actuation speed?

---

## Link to Your Hybrid System
- Directly relevant to pneumatic soft gripper design, tubing, valves and response time.
- Use these ideas when sizing the air supply and diagnosing slow or weak actuation.

## Status
- [ ] Theory notes completed
- [ ] Linked to soft gripper pneumatic design
- [ ] Practice problems or mini-project done
