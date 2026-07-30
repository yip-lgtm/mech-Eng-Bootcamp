# MAEG5060 Computational Intelligence

**Phase 4 | Priority: ★★★**  
**Why critical**: Neural nets, fuzzy systems and evolutionary algorithms for intelligent control and optimisation.

---

## 1. 5 Core Mental Models Every Expert Shares

1. **Approximation Power vs Interpretability** — Flexible models fit complex maps; simple models remain explainable and often more robust.
2. **Search and Learning are Related** — Evolutionary algorithms search parameter spaces; learning algorithms search hypothesis spaces.
3. **Representation Again Decides Difficulty** — Features, encodings and fitness functions shape what can be found.
4. **Hybrid Systems Often Win** — Combining classical control with learned components is frequently more practical than pure end-to-end learning.
5. **Generalisation is the Goal** — Performance on training data is not the product; behaviour on new situations is.

---

## 2. 3 Places Experts Fundamentally Disagree

### Disagreement 1: Neural Networks vs Classical AI / Fuzzy / Evolutionary Methods
- Neural nets dominate perception and many control tasks. Classical and fuzzy methods remain strong where rules and interpretability matter.

### Disagreement 2: Online Learning on the Robot vs Offline Training Only
- Online adaptation handles change. Offline training is safer and more reproducible.

### Disagreement 3: How Much Theory vs Empirical Practice
- Theory guides architecture and guarantees. Empirical practice drives most current robot learning results.

---

## 3. 10 Questions that Distinguish Deep Understanding

1. When is a fuzzy controller preferable to a PID or a neural controller?
2. What does the universal approximation theorem actually guarantee, and what does it not?
3. How would you use a genetic algorithm to tune gains or morphology of a soft gripper?
4. What is the difference between supervised fine-tuning and reinforcement learning for a grasping policy?
5. How do you prevent a learned controller from producing unsafe actions?
6. Why can ensemble or hybrid methods outperform a single powerful model?
7. What is catastrophic forgetting, and how does it affect sequential skill learning on a robot?
8. How would you encode a simple warehouse sorting policy so that an evolutionary method could improve it?
9. What metrics would you use to compare a learned grasp policy against your current state machine?
10. In your hybrid system, which subsystem is the best candidate for a computational-intelligence upgrade?

---

## Link to Your Hybrid System
- Natural extension of the rule-based agent toward adaptive grasping and decision-making.

## Status
- [ ] Theory notes completed
- [ ] One small CI experiment planned or run
- [ ] Practice problems done
