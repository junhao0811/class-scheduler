# Flow Network Design

## Constraints

- `n` students, each of whom must get **exactly one** class
- `m` proposed classes, each with a time slot and a size range `[min_students, max_students]`
- every student ranks all 20 time slots, so any student can attend any class
- at least `minimumSatisfaction` students must get a class in one of their **top-5** time slots

## Network

Each edge has a lower bound and a capacity, written `[lower, capacity]`.

```
                   [1,1]                [0,1] (top-5 slot only)                 [min_j, max_j]
        source ──────────▶ student i ─────────────────────────────▶ class j ─────────────────▶ sink
          ▲                    │                                       ▲                      │
          │                    │ [0,1]                                 │ [0,n]                │
          │                    ▼                                       │                      │
          │            unsatisfied_in ──[0, n − minimumSatisfaction]──▶ unsatisfied_out       │
          │                                                                                   │
          └───────────────────────────────────────── [0,n] ───────────────────────────────────┘
```

| Edge | Bounds | Why |
|---|---|---|
| source → student *i* | [1, 1] | every student is allocated exactly once |
| student *i* → class *j* | [0, 1] | only when class *j*'s slot is in student *i*'s top 5 (a "satisfied" placement) |
| student *i* → unsatisfied_in | [0, 1] | the route for students who do not get a top-5 slot |
| unsatisfied_in → unsatisfied_out | [0, n − minimumSatisfaction] | at most this many students can miss their top 5 |
| unsatisfied_out → class *j* | [0, n] | any class is allowed, since everyone accepts every slot |
| class *j* → sink | [min_j, max_j] | class size limits |
| sink → source | [0, n] | closes the loop, turning the problem into a circulation |

## Removing the lower bounds

Each edge `(u, v, l, c)` becomes `(u, v, c − l)`, and its `l` units become a demand: `v` gains `l` and `u` loses `l`.

- A super-source connects to every vertex with a surplus.
- Every vertex with a deficit connects to a super-sink.

A valid allocation exists **if and only if** the maximum flow from the super-source fills every super-source edge. Ford–Fulkerson with BFS augmenting paths finds that flow.

## Reading the answer back

- A student with flow on a direct student → class edge goes to that class, and is satisfied.
- Students with flow into `unsatisfied_in` are interchangeable, because every student accepts every slot. They are paired, in any order, with the class units leaving `unsatisfied_out`.

## Complexity

- **Graph size:** O(n + m) vertices and O(n·m) edges.
- **Total flow:** at most 2n.
- **Time:** O(n²·m) overall.
- **Space:** O(n·m).
