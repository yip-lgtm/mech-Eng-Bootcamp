# ENGG2020 Digital Logic and Systems

**Phase 3 | Priority: ★★★**  
**Why critical**: Combinational/sequential logic and FSMs — the basis of discrete state machines in robot control.

---

## 1. 5 Core Mental Models Every Expert Shares

1. **Boolean Algebra is the Algebra of Decisions** — AND, OR, NOT (and their compositions) describe every digital choice.
2. **Combinational vs Sequential** — Combinational outputs depend only on current inputs; sequential has memory (state).
3. **Finite State Machines are the Standard Model of Discrete Behaviour** — States, transitions, inputs and outputs.
4. **Timing and Hazards Matter** — Correct logic can still fail if signals race or setup/hold times are violated.
5. **Abstraction Layers Hide Complexity** — Gates → modules → processors; each level simplifies reasoning.

---

## 2. 3 Places Experts Fundamentally Disagree

### Disagreement 1: Hardware Description Languages Early vs Gate-Level First
- HDL early prepares for real design. Gate-level first builds intuition for what the hardware actually does.

### Disagreement 2: Synchronous vs Asynchronous Design Emphasis
- Synchronous is the industrial default and easier to reason about. Asynchronous can be faster or lower power but is harder.

### Disagreement 3: How Much Computer Architecture to Include
- Some architecture motivates the logic. Too much architecture displaces fundamental digital design.

---

## 3. 10 Questions that Distinguish Deep Understanding

1. Why can a combinational circuit have hazards even if the Boolean function is correct?
2. Difference between a Mealy and a Moore state machine, and when each is preferable?
3. How do you systematically derive a state diagram from a word description of robot behaviour?
4. What does setup time and hold time mean for a flip-flop, and what happens if they are violated?
5. Why is a clocked synchronous design usually preferred for robot controllers?
6. How would you encode the states of your gripper state machine (APPROACH…RELEASE) in hardware?
7. What is the difference between a latch and a flip-flop?
8. When does a finite state machine become an inadequate model of robot behaviour?
9. How do you test a sequential circuit for correct state transitions?
10. In your hybrid system, which parts of the control are naturally expressed as an FSM?

---

## Link to Your Hybrid System
- The gripper state machine is a classic FSM.
- Understanding digital logic helps when moving control from Arduino sketches toward more structured implementations.

## Status
- [ ] Theory notes completed
- [ ] Current state machine drawn as formal FSM
- [ ] Practice problems done
