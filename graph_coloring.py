
def build_conflict_graph(subjects, students):
    """Build a graph based on shared student enrolments."""
    graph = {subject: set() for subject in subjects}

    for enrolled_subjects in students.values():
        valid_subjects = [
            subject for subject in enrolled_subjects
            if subject in graph
        ]

        for i in range(len(valid_subjects)):
            for j in range(i + 1, len(valid_subjects)):
                subject1 = valid_subjects[i]
                subject2 = valid_subjects[j]

                graph[subject1].add(subject2)
                graph[subject2].add(subject1)

    return graph


def color_graph_backtracking(graph, max_colors):
    """Find a valid coloring using backtracking."""
    vertices = sorted(
        graph,
        key=lambda vertex: len(graph[vertex]),
        reverse=True
    )

    coloring = {}
    attempts = 0

    def is_safe(vertex, color):
        return all(
            coloring.get(neighbour) != color
            for neighbour in graph[vertex]
        )

    def solve(index):
        nonlocal attempts

        if index == len(vertices):
            return True

        vertex = vertices[index]

        for color in range(max_colors):
            attempts += 1

            if is_safe(vertex, color):
                coloring[vertex] = color

                if solve(index + 1):
                    return True

                del coloring[vertex]

        return False

    if solve(0):
        return coloring, attempts

    return None, attempts



def find_minimum_coloring(graph, max_slots=None):
    if not graph:
        return {}, 0, 0

    if max_slots is None:
        max_slots = len(graph)

    # Sort subjects by highest number of conflicts
    vertices = sorted(
        graph.keys(),
        key=lambda v: (-len(graph[v]), v)
    )

    total_attempts = 0

    def solve_with_slots(slot_count):
        coloring = {}

        def backtrack(index):
            nonlocal total_attempts

            if index == len(vertices):
                return True

            vertex = vertices[index]

            # Find colors already used by neighbours
            used_colors = {
                coloring[neighbour]
                for neighbour in graph[vertex]
                if neighbour in coloring
            }

            for color in range(slot_count):
                total_attempts += 1

                if color not in used_colors:
                    coloring[vertex] = color

                    if backtrack(index + 1):
                        return True

                    del coloring[vertex]

            return False

        if backtrack(0):
            return coloring

        return None

    for slot_count in range(1, max_slots + 1):
        result = solve_with_slots(slot_count)

        if result is not None:
            return result, slot_count, total_attempts

    return None, 0, total_attempts
