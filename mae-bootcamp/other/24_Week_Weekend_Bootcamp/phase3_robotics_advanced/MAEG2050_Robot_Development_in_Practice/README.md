# MAEG2050 Robot Development in Practice

**Phase 3 | Priority: ⭐⭐⭐⭐**  
**Why critical**: The messy reality of turning theory into a working robot — integration, testing, debugging and iteration.

---

## 1. 5 Core Mental Models Every Expert Shares

1. **Working Software / Hardware Beats Perfect Design** — A running, imperfect system teaches more than a perfect paper design.
2. **Interfaces are Where Systems Fail** — Most integration problems appear at mechanical, electrical and software boundaries.
3. **Test Early, Test Often, Test on the Real Thing** — Simulation is necessary but insufficient; real sensors and actuators surprise you.
4. **Version Control and Traceability Matter for Hardware Too** — Know which firmware, parameters and mechanical revision produced a given result.
5. **Bring-up is a Skill** — Power-on → sensors → actuators → low-level loops → behaviours is a deliberate sequence.

---

## 2. 3 Places Experts Fundamentally Disagree

### Disagreement 1: Simulation-First vs Hardware-First Development
- **Simulation-first**: cheaper iteration, safer. **Hardware-first**: discovers real physics and integration issues earlier.

### Disagreement 2: How Much Process (Agile, Documentation) for Small Robot Teams
- **Light process** enables speed. **Too little process** loses knowledge and makes debugging harder.

### Disagreement 3: Custom vs Off-the-Shelf Components
- **Custom**: optimized performance. **Off-the-shelf**: speed, reliability, support.

---

## 3. 10 Questions that Distinguish Deep Understanding

1. What is the first thing you should verify when a newly assembled robot does not move?
2. How do you systematically isolate whether a problem is mechanical, electrical, or software?
3. Why is a ‘hello world’ that simply reads one sensor and blinks an LED so valuable?
4. What information should be logged during every experimental run of a robot?
5. How would you design a bring-up checklist for your hybrid 3R + soft gripper system?
6. When is it rational to stop improving a subsystem and move on to integration?
7. What are common sources of non-reproducible behaviour in mechatronic prototypes?
8. How do you decide the minimum viable sensor suite for a new robot behaviour?
9. Why do many robot projects underestimate cable management and connector reliability?
10. In your current hybrid system, what is the single highest-risk interface?

---

## Link to Your Hybrid System
- This course is essentially the methodology behind your entire physical build and demo work.
- Apply the bring-up and interface thinking to every new addition to the arm or gripper.

## Status
- [ ] Theory notes completed
- [ ] Bring-up checklist written for current system
- [ ] Practice problems or mini-project done
