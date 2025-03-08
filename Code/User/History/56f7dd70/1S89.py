initial_state = (3, 3, 1)
goal_state = (0, 0, 0)
MOVES = [(1, 0), (2, 0), (0, 1), (0, 2), (1, 1)]

def is_valid(state):
    m, c, _ = state
    m_right, c_right = 3 - m, 3 - c
    return 0 <= m <= 3 and 0 <= c <= 3 and (m == 0 or m >= c) and (m_right == 0 or m_right >= c_right)

def get_next_states(state):
    m, c, b = state
    return [(m - dm, c - dc, 0) if b else (m + dm, c + dc, 1) for dm, dc in MOVES if is_valid((m - dm, c - dc, 0) if b else (m + dm, c + dc, 1))]

def bfs():
    queue, visited = [(initial_state, [])], []
    while queue:
        state, path = queue.pop(0)
        if state in visited:
            continue
        visited.append(state)
        if state == goal_state:
            return path + [state]
        queue.extend((next_state, path + [state]) for next_state in get_next_states(state))
    return None

solution = bfs()
if solution:
    for step in solution:
        print(step)
else:
    print("No solution found.")
