# MAEG3080 Fundamentals of Machine Intelligence

**Phase 3 | Priority: ★★★★**  
**Why critical**: Learning, perception and decision-making for embodied agents — the path from rule-based state machines to adaptive behaviour.

---

## 1. 5 Core Mental Models Every Expert Shares

1. **Representation Determines What Can Be Learned** — Features, embeddings and state abstractions shape the difficulty of every learning problem.
2. **Bias–Variance and Under/Overfitting are Universal** — Every model class trades flexibility against generalization.
3. **Embodiment Changes the Learning Problem** — Physical interaction, real-time constraints and safety make robot learning different from pure software ML.
4. **Exploration vs Exploitation is Fundamental** — An agent must try new things to improve, yet must also use what it already knows.
5. **Data Quality Beats Algorithm Cleverness for Many Real Problems** — Clean, relevant, well-distributed data often matters more than the latest architecture.

---

## 2. 3 Places Experts Fundamentally Disagree

### Disagreement 1: End-to-End Learning vs Modular Pipelines
- **End-to-end**: can discover unexpected strategies. **Modular**: interpretable, easier to debug, safer to deploy.

### Disagreement 2: Model-Based vs Model-Free Reinforcement Learning for Robots
- **Model-based**: sample-efficient, can use planning. **Model-free**: simpler, can handle complex dynamics that are hard to model.

### Disagreement 3: How Much Classical Robotics Should Precede Learning Methods
- **Classical first**: provides structure and safety baselines. **Learning early**: students see modern practice sooner.

---

## 3. 10 Questions that Distinguish Deep Understanding

1. Why is sample efficiency especially critical for physical robots compared with simulated agents?
2. What makes a representation ‘good’ for a robot learning a manipulation skill?
3. Explain the difference between supervised, unsupervised and reinforcement learning with a robot example of each.
4. Why can a policy that performs well in simulation fail dramatically on the real robot (sim-to-real gap)?
5. How does the concept of a Markov Decision Process (MDP) map onto your current state-machine gripper controller?
6. When would you prefer a simple classical controller over a learned policy?
7. What safety constraints must be enforced when a learning algorithm is allowed to control a physical arm?
8. How can you use demonstration (imitation learning) to bootstrap a soft-gripper grasping policy?
9. What is catastrophic forgetting, and why does it matter for lifelong robot learning?
10. In your warehouse agent, which parts of the decision-making are best left rule-based and which could benefit from learning?

---

## Link to Your Hybrid System
- Natural next step beyond the current rule-based state machine.
- Useful for adaptive grasping, slip recovery, and higher-level warehouse decisions.

## Status
- [ ] Theory notes completed
- [ ] Mapped current state machine to MDP concepts
- [ ] Practice problems or mini-project done
