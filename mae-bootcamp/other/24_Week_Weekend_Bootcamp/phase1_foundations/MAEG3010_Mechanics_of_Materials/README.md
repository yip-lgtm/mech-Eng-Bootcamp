# MAEG3010 Mechanics of Materials

**Phase 1 | Priority: ★★★★**  
**Why critical**: Stress, strain, failure theories — essential for designing rigid and soft robot structures that do not break.

---

## 1. 5 Core Mental Models Every Expert Shares

1. **Stress is Force Intensity** — Not force itself; magnitude and orientation both matter.
2. **Strain is Purely Geometric** — Describes deformation independent of material until a constitutive law is applied.
3. **Constitutive Laws Link Stress and Strain** — Linear elastic is only the simplest useful model.
4. **Failure Criteria are Models of Strength** — von Mises, Tresca, max principal stress each embed assumptions.
5. **Saint-Venant’s Principle** — Local load details die out; far-field stress depends on resultant force and moment.

---

## 2. 3 Places Experts Fundamentally Disagree

### Disagreement 1: Strength-of-Materials vs Full Continuum Mechanics First
- Strength-of-materials is practical and fast. Continuum mechanics is more general and necessary for complex 3D and soft materials.

### Disagreement 2: How Early to Introduce Plasticity and Fracture
- Early: engineers design against failure. Later: elastic theory must be solid first.

### Disagreement 3: Analytical Solutions vs Numerical (FEA) Emphasis
- Analytical builds insight. Numerical is required for real geometries but risks blind trust in software.

---

## 3. 10 Questions that Distinguish Deep Understanding

1. Why can a stress component be zero while the corresponding strain is not?
2. What is the physical meaning of the shear modulus G?
3. How does Mohr’s circle help find principal stresses without an eigenvalue solve?
4. When is the maximum-principal-stress failure criterion inappropriate?
5. Explain engineering stress vs true stress and when each is useful.
6. What does a stress-concentration factor represent?
7. How would you decide plane stress vs plane strain for a soft-actuator wall?
8. Why do residual stresses matter after external loads are removed?
9. How do you combine axial, bending and torsional stresses for a robot link?
10. Which assumptions of elementary beam theory are most often violated in robots?

---

## Link to Your Hybrid System
- Used for sizing 3R arm links and joints under gravity and payload.
- Soft gripper walls rest on the same continuum foundations.

## Status
- [ ] Theory notes completed
- [ ] Simple stress check of current 3R design
- [ ] Practice problems done
