# ENGG1120 Linear Algebra for Engineers

**Phase 1 | Priority: ★★★**  
**Why critical**: Essential for robot kinematics, dynamics, computer vision, control and almost every numerical method you will use.

---

## 1. 5 Core Mental Models Every Expert Shares

1. **Linear Transformations are the Core Object** — Matrices represent maps between vector spaces, not just arrays of numbers.
2. **Basis and Change of Basis** — The same vector looks different in different coordinate systems; change-of-basis matrices connect them.
3. **Null Space and Range** — They tell you what a linear map can and cannot do.
4. **Eigenvalues Reveal Intrinsic Behaviour** — Independent of coordinate choice; central to dynamics and stability.
5. **Least Squares as Projection** — The geometric view of solving inconsistent systems by orthogonal projection.

---

## 2. 3 Places Experts Fundamentally Disagree

### Disagreement 1: Geometric vs Algebraic First Approach
- Geometric builds intuition for engineers. Algebraic is more rigorous and general.

### Disagreement 2: How Much Abstract Vector-Space Theory
- Minimal (focus on Rⁿ) vs more (preparation for functional analysis and advanced control).

### Disagreement 3: Computation vs Hand Calculation
- Computation early for real problems. Hand calculation first for understanding mechanisms.

---

## 3. 10 Questions that Distinguish Deep Understanding

1. Why does changing basis not change the eigenvalues of a linear operator?
2. What does a singular matrix physically mean for a robot Jacobian?
3. Explain the geometric meaning of the null space of A.
4. How is the least-squares solution related to orthogonal projection?
5. Why can two different matrices represent the same linear transformation?
6. Relationship between rank, nullity and dimension of the domain?
7. How do you test linear independence without computing a determinant?
8. Why is SVD often preferred over eigendecomposition numerically?
9. In robot kinematics, what does loss of rank in the Jacobian imply?
10. How does an affine transformation differ from a linear one?

---

## Link to Your Hybrid System
- FK uses successive rotation/homogeneous matrices.
- Jacobian singularity analysis is pure linear algebra.
- Future vision and estimation modules rely on the same tools.

## Status
- [ ] Theory notes completed
- [ ] Linked to 3R FK / Jacobian code
- [ ] Practice problems done
