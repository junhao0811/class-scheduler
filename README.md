# 🎓 Class Scheduler (Max Flow)

Allocates students to classes using **network flow with lower bounds**, written from scratch in Python.

---

## How it works

**Problem.** Assign `n` students to `m` proposed classes so that:
- every student gets exactly one class
- every class stays between its **minimum and maximum** size
- each class runs in one of 20 time slots, and every student ranks all 20
- at least a given number of students get a class in one of their **top-5** time slots

**Approach.** It's modelled as a **flow network**:

```
Source ─▶ Students ─┬─(top-5 slot)──────────────────────────▶ Classes ─▶ Sink
                    └─▶ Unsatisfied ─(cap: n − minimum)─────▶ Classes
```

- **Top-5 placements** go straight from a student to a class.
- **All other placements** share one "unsatisfied" bottleneck, so at most `n − minimum` students can miss their top 5.
- **Class sizes** become **lower bounds** on the class → sink edges. The standard transformation removes them: lower bounds → demands → a super-source and super-sink.
- **Ford–Fulkerson** (BFS augmenting paths) then decides whether a valid allocation exists, and the allocation is read straight from the flow.

The full model, with every edge and why it's there, is in [`flow_network_design.md`](./flow_network_design.md).

```python
from class_scheduler import allocate_students
allocation = allocate_students(n, m, timePreferences, proposedClasses, minimumSatisfaction)
# -> list where allocation[i] is student i's class, or None if no valid allocation exists
```

**Complexity:** O(n²·m) time, O(n·m) space.

---

## ✅ Tests

```bash
python -m unittest test_class_scheduler
```

All 29 tests pass, including the tightly constrained edge cases. The solver was also checked against brute force on 3,000 random small inputs (feasible and infeasible) with no mismatches.

## 🛠️ Tech
Python 3 · network flow · Ford–Fulkerson · lower-bound circulation (no external libraries)
