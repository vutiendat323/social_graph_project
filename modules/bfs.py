from collections import deque

class BFSProcessor:
    def __init__(self, graph, is_directed=False):
       
        self.graph = graph
        self.is_directed = is_directed
    
    def bfs_traversal(self, start):
        if start not in self.graph.adj_list:
            return []

        visited = set()
        queue = deque([start])
        traversal_order = []

        visited.add(start)
        traversal_order.append(start)

        while queue:
            current = queue.popleft()
            for neighbor in self.graph.get_neighbors(current):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
                    traversal_order.append(neighbor)

        return traversal_order

    def degrees_of_separation(self, start, end):
        
        if start not in self.graph.adj_list or end not in self.graph.adj_list:
            return -1, []
        if start == end:
            return 0, [start]

        visited = set()
        queue = deque([(start, 0)])
        visited.add(start)
        parent = {start: None}

        while queue:
            current, distance = queue.popleft()
            for neighbor in self.graph.get_neighbors(current):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, distance + 1))
                    parent[neighbor] = current
                    if neighbor == end:
                        path = []
                        step = end
                        while step is not None:
                            path.append(step)
                            step = parent[step]
                        path.reverse()
                        return distance + 1, path
        return -1, []

    def suggest_friends(self, node, max_depth=2):
        
        if node not in self.graph.adj_list:
            return []

        visited = set()
        queue = deque([(node, 0)])
        visited.add(node)
        suggestions = set()

        while queue:
            current, depth = queue.popleft()
            if depth > max_depth:
                break
            if depth > 0 and not self.graph.has_edge(node, current):
                suggestions.add(current)
            for neighbor in self.graph.get_neighbors(current):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, depth + 1))
        
        return list(suggestions)

    def influence_analysis(self, node, max_depth=None):
        
        if node not in self.graph.adj_list:
            return {"reachable_nodes": 0, "average_distance": 0}

        visited = set()
        queue = deque([(node, 0)])
        visited.add(node)
        distances = {node: 0}

        while queue:
            current, distance = queue.popleft()
            if max_depth is not None and distance > max_depth:
                continue
            for neighbor in self.graph.get_neighbors(current):
                if neighbor not in visited:
                    visited.add(neighbor)
                    distances[neighbor] = distance + 1
                    queue.append((neighbor, distance + 1))

        reachable_nodes = len(visited) - 1
        average_distance = sum(distances.values()) / reachable_nodes if reachable_nodes > 0 else 0
        return {"reachable_nodes": reachable_nodes, "average_distance": average_distance}

    def bidirectional_bfs(self, start, end):
        
        if start not in self.graph.adj_list or end not in self.graph.adj_list:
            return None, None
        if start == end:
            return 0, [start]

        queue_start = deque([(start, [start], 0)])
        queue_end = deque([(end, [end], 0)])
        visited_start = {start: (0, [start])}
        visited_end = {end: (0, [end])}

        while queue_start and queue_end:
            current_start, path_start, dist_start = queue_start.popleft()
            for neighbor in self.graph.get_neighbors(current_start):
                if neighbor not in visited_start:
                    new_dist = dist_start + 1
                    new_path = path_start + [neighbor]
                    visited_start[neighbor] = (new_dist, new_path)
                    queue_start.append((neighbor, new_path, new_dist))
                    if neighbor in visited_end:
                        dist_end, path_end = visited_end[neighbor]
                        return new_dist + dist_end, new_path + path_end[::-1][1:]

            current_end, path_end, dist_end = queue_end.popleft()
            for neighbor in self.graph.get_neighbors(current_end):
                if neighbor not in visited_end:
                    new_dist = dist_end + 1
                    new_path = path_end + [neighbor]
                    visited_end[neighbor] = (new_dist, new_path)
                    queue_end.append((neighbor, new_path, new_dist))
                    if neighbor in visited_start:
                        dist_start, path_start = visited_start[neighbor]
                        return dist_start + new_dist, path_start + new_path[::-1][1:]

        return None, None

    def has_cycle(self):
        
        visited = set()
        parent = {}

        for start in self.graph.adj_list:
            if start not in visited:
                queue = deque([start])
                visited.add(start)
                parent[start] = None

                while queue:
                    current = queue.popleft()
                    for neighbor in self.graph.get_neighbors(current):
                        if neighbor not in visited:
                            visited.add(neighbor)
                            queue.append(neighbor)
                            parent[neighbor] = current
                        elif not self.is_directed and neighbor != parent[current]:
                            return True
                        elif self.is_directed and neighbor in visited:
                            return True
        return False

    def find_communities(self):
       
        visited = set()
        communities = []

        for node in self.graph.adj_list:
            if node not in visited:
                community = []
                queue = deque([node])
                visited.add(node)

                while queue:
                    current = queue.popleft()
                    community.append(current)
                    for neighbor in self.graph.get_neighbors(current):
                        if neighbor not in visited:
                            visited.add(neighbor)
                            queue.append(neighbor)
                communities.append(community)
        return communities