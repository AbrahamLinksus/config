def is_valid(state, visited):
    return state not in visited

def get_next_states(state, X, Y):
    a, b = state
    return [
        (X, b), (a, Y), (0, b), (a, 0),  # Fill and empty operations
        (a - min(a, Y - b), b + min(a, Y - b)),  # Pour A → B
        (a + min(b, X - a), b - min(b, X - a))   # Pour B → A
    ]

def bfs(X, Y, Z):
    queue = [((0, 0), [])]  # (current state, path)
    visited = set()

    while queue:
        state, path = queue.pop(0)
        if state in visited:
            continue
        visited.add(state)

        if state[0] == Z or state[1] == Z:
            return path + [state]

        for next_state in get_next_states(state, X, Y):
            if is_valid(next_state, visited):
                queue.append((next_state, path + [state]))
    return None

def dfs(X, Y, Z, state=(0, 0), path=[], visited=set()):
    if state in visited:
        return None
    visited.add(state)
    if state[0] == Z or state[1] == Z:
        return path + [state]
    for next_state in get_next_states(state, X, Y):
        result = dfs(X, Y, Z, next_state, path + [state], visited)
        if result:
            return result
    return None

# Example usage
X, Y, Z = 4, 3, 2  # Jug capacities and target
print("BFS Solution:", bfs(X, Y, Z))
print("DFS Solution:", dfs(X, Y, Z))
