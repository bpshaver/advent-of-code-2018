### Sample Output From Part II

0

Available nodes: [node: C, Started: False, Duration: 3, Parents: [], Children: ['A', 'F']]

Assigning node C to worker 0

Decrementing node C by 1

Done:

---

1

Available nodes: []

Decrementing node C by 1

Done:

---

2

Available nodes: []

Decrementing node C by 1

Done:

---

3

node C finished!

Available nodes: [node: F, Started: False, Duration: 6, Parents: [], Children: ['E'], node: A, Started: False, Duration: 1, Parents: [], Children: ['B', 'D']]

Assigning node A to worker 0

Decrementing node A by 1

Assigning node F to worker 1

Decrementing node F by 1

Done: C

---

4

node A finished!

Available nodes: [node: D, Started: False, Duration: 4, Parents: [], Children: ['E'], node: B, Started: False, Duration: 2, Parents: [], Children: ['E']]

Assigning node B to worker 0

Decrementing node B by 1

Decrementing node F by 1

Done: CA

---

5

Available nodes: [node: D, Started: False, Duration: 4, Parents: [], Children: ['E']]

Decrementing node B by 1

Decrementing node F by 1

Done: CA

---

6

node B finished!

Available nodes: [node: D, Started: False, Duration: 4, Parents: [], Children: ['E']]

Assigning node D to worker 0

Decrementing node D by 1

Decrementing node F by 1

Done: CAB

---

7

Available nodes: []

Decrementing node D by 1

Decrementing node F by 1

Done: CAB

---

8

Available nodes: []

Decrementing node D by 1

Decrementing node F by 1

Done: CAB

---

9

node F finished!

Available nodes: []

Decrementing node D by 1

Done: CABF

---

10

node D finished!

Available nodes: [node: E, Started: False, Duration: 5, Parents: [], Children: []]

Assigning node E to worker 0

Decrementing node E by 1

Done: CABFD

---

11

Available nodes: []

Decrementing node E by 1

Done: CABFD

---

12

Available nodes: []

Decrementing node E by 1

Done: CABFD

---

13

Available nodes: []

Decrementing node E by 1

Done: CABFD

---

14

Available nodes: []

Decrementing node E by 1

Done: CABFD

---

15

node E finished!

Available nodes: []

Done: CABFDE

---
