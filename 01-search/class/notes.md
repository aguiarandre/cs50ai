# URL
https://cs50.harvard.edu/ai/2020/notes/0/

# Slides
https://cdn.cs50.net/ai/2020/spring/lectures/0/lecture0.pdf

# My notes

## Search Problems

- Agent
    - Entity that perceives its environment and act upon that env
- State
    - A configuration of the agent in the environment
    - `initial state` -> `end state` via actions
- Actions
    - choices that can be made in a state
    - Action(s) takes the state as an input and returns the set of actions that are available to be applied to that state 
- Transition model
    - Result(s, a) takes a state and an action, and ouputs the resulting state
- State Space
    - The set of all states reachable from the initial state by any sequence of actions
- Goal test
    - Some way to determine whether a given state is the goal state
- Path cost function
    - numerical cost associated with a given path p
- [optimal] solution
    - a sequence of actions that has the lowest cost among all solutions

## Data Structures

### Node
- a State
- a Parent (node that generated this node)
- an Action (action applied to the parent to get node)
- a path cost (from initial to state node)

### Frontier 
- All available options, that we could explore next

## Approach

- start with a frontier that contains the initial state
- repeat:
    - if the frontier is empty, there is no solution
    - remove a node from the frontier 
        - frontier as a `stack - LIFO` (depth first search)
            - maybe not the optimal solution
        - frontier as a `queue - FIFO` (breadth first search)
            - finds the optimal path

    - if node contains goal state, return the solution
    - add the node to the explored set
    - expand node, add resulting nodes to the frontier if they are not already in the frontier or the explored set

### Uninformed Search
- DFS and BFS - no previous knowledge

### Informed Search
- Use knowledge problem-specific knowledge
- Greedy best first search
    - heuristic function h(n), takes a state as input, returns an estimate of how close we are
        - h(n) could be the manhattan distance, e.g.
- A* search
    - heuristic function g(n) + h(n)
    - g(n) = cost to reach the node
        - optimal if 
            - h(n) is admissible (never overestimates the true cost)
            - h(n) is consistent ()

## Adversarial Search

### Minimax

