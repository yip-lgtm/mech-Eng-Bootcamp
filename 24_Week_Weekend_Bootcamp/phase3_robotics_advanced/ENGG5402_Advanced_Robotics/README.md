# ENGG5402 Advanced Robotics

**Phase 3 | Priority: ★★★★**  
**Why critical**: Advanced kinematics, dynamics, planning and control beyond the introductory level.

---

## 1. 5 Core Mental Models Every Expert Shares

1. **Task Space vs Joint Space** — Many objectives are natural in task space; actuation and dynamics live in joint space.
2. **Redundancy is Opportunity and Burden** — Extra degrees of freedom enable secondary tasks and obstacle avoidance but require resolution strategies.
3. **Dynamics Couple Everything** — Inertia, Coriolis, gravity and friction make the equations nonlinear and coupled.
4. **Motion Planning is Search Under Constraints** — Collision-free, dynamically feasible paths in high-dimensional spaces.
5. **Stability and Passivity are Design Goals** — Especially under contact, uncertainty and interaction with humans.

---

## 2. 3 Places Experts Fundamentally Disagree

### Disagreement 1: Sampling-Based vs Optimization-Based Planning
- Sampling (PRM, RRT): good for high-dimensional and complex obstacles. Optimization: smoother, can include dynamics, but may get stuck in local minima.

### Disagreement 2: Model-Based Control vs Learning-Based Control at the Advanced Level
- Model-based: interpretable, certifiable, sample-efficient. Learning-based: handles unmodelled effects and complex perception-action maps.

### Disagreement 3: How Much Contact and Hybrid Dynamics
- Contact is central to real manipulation. Some curricula still treat free-motion dynamics as the core.

---

## 3. 10 Questions that Distinguish Deep Understanding

1. Why is the inverse dynamics problem usually easier than the forward dynamics problem for serial arms?
2. How does the operational-space formulation allow control of end-effector behaviour while using joint actuators?
3. What is the null-space of the Jacobian used for in redundant robots?
4. Explain the difference between kinematic and dynamic singularities.
5. When would you prefer RRT-Connect over trajectory optimization for a pick-and-place task?
6. How do friction cones and complementarity conditions appear in contact models?
7. What does passivity of a controller buy you when the robot interacts with an unknown environment?
8. How would you incorporate the soft gripper’s compliance into a whole-arm motion plan?
9. Why is calibration still necessary even with a good kinematic model?
10. In your hybrid system, what advanced capability (planning, redundancy, contact) is the highest-value next step?

---

## Link to Your Hybrid System
- Natural extension of MAEG3060 toward full dynamics, planning and contact-rich tasks with the soft gripper.

## Status
- [ ] Theory notes completed
- [ ] Identified next advanced feature for the hybrid system
- [ ] Practice problems done
