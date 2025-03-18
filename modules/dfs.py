class DFSProcessor:
    def __init__(self, graph, is_directed=False):
       
        self.graph = graph
        self.is_directed = is_directed
    
    def dfs_traversal(self, start):
        
        if start not in self.graph.adj_list:
            return []

        visited = set()
        traversal_order = []

        def dfs_helper(node):
            visited.add(node)
            traversal_order.append(node)
            for neighbor in self.graph.get_neighbors(node):
                if neighbor not in visited:
                    dfs_helper(neighbor)

        dfs_helper(start)
        return traversal_order

    def has_cycle(self):
       
        visited = set()
        rec_stack = set()

        def dfs_cycle(node, parent=None):
            visited.add(node)
            rec_stack.add(node)
            for neighbor in self.graph.get_neighbors(node):
                if not self.is_directed and neighbor == parent:
                    continue  # Bỏ qua cạnh ngược trong đồ thị vô hướng
                if neighbor not in visited:
                    if dfs_cycle(neighbor, node):
                        return True
                elif neighbor in rec_stack:
                    return True
            rec_stack.remove(node)
            return False

        for node in self.graph.adj_list:
            if node not in visited:
                if dfs_cycle(node):
                    return True
        return False

    def find_communities(self):
        
        visited = set()
        communities = []

        def dfs_community(node, community):
            visited.add(node)
            community.append(node)
            for neighbor in self.graph.get_neighbors(node):
                if neighbor not in visited:
                    dfs_community(neighbor, community)

        for node in self.graph.adj_list:
            if node not in visited:
                current_community = []
                dfs_community(node, current_community)
                communities.append(current_community)
        return communities

    def suggest_friends(self, node, max_depth=2):
        
        if node not in self.graph.adj_list:
            return []
        
        visited = set()
        suggestions = set()

        def dfs_suggest(current, depth):
            if depth > max_depth:
                return
            visited.add(current)
            if depth > 0 and current != node and not self.graph.has_edge(node, current):
                suggestions.add(current)
            for neighbor in self.graph.get_neighbors(current):
                if neighbor not in visited:
                    dfs_suggest(neighbor, depth + 1)

        dfs_suggest(node, 0)
        return list(suggestions)

    def influence_analysis(self, node):
        
        if node not in self.graph.adj_list:
            return {"reachable_nodes": 0, "max_depth": 0, "average_distance": 0}

        visited = set()
        depths = {node: 0}  # Lưu độ sâu của từng nút

        def dfs_influence(current, depth):
            visited.add(current)
            depths[current] = depth
            max_depth = depth
            for neighbor in self.graph.get_neighbors(current):
                if neighbor not in visited:
                    child_depth = dfs_influence(neighbor, depth + 1)
                    max_depth = max(max_depth, child_depth)
            return max_depth

        max_depth = dfs_influence(node, 0)
        reachable_nodes = len(visited) - 1  # Không tính chính node
        average_distance = sum(depths.values()) / reachable_nodes if reachable_nodes > 0 else 0
        
        return {
            "reachable_nodes": reachable_nodes,
            "max_depth": max_depth,
            "average_distance": average_distance
        }