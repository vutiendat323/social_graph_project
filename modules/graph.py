class SocialGraph:
    def __init__(self, is_directed=False):
       
        self.adj_list = {}    
        self.nodes = set() 
        self.num_edges = 0     
        self.num_nodes = 0    
        self.is_directed = is_directed

    def build_from_edges(self, edge_list):
        
        for node1, node2 in edge_list:
            self.add_edge(node1, node2)

    def add_node(self, node):
        
        if node not in self.adj_list:
            self.adj_list[node] = []
            self.nodes.add(node)
            self.num_nodes += 1
            return True
        return False

    def add_edge(self, node1, node2):
        
        # Thêm node nếu chưa tồn tại
        if node1 not in self.adj_list:
            self.add_node(node1)
        if node2 not in self.adj_list:
            self.add_node(node2)

        # Thêm cạnh nếu chưa tồn tại
        if node2 not in self.adj_list[node1]:
            self.adj_list[node1].append(node2)
            self.num_edges += 1
            if not self.is_directed and node1 not in self.adj_list[node2]:
                self.adj_list[node2].append(node1)

    def remove_node(self, node):
        
        if node not in self.adj_list:
            raise ValueError(f"Node {node} không tồn tại trong đồ thị")
        
        # Xóa các cạnh liên quan từ các nút khác
        for neighbor in list(self.adj_list[node]):
            self.remove_edge(node, neighbor)
        
        # Xóa nút
        del self.adj_list[node]
        self.nodes.remove(node)
        self.num_nodes -= 1

    def remove_edge(self, node1, node2):
        
        if not self.has_edge(node1, node2):
            raise ValueError(f"Cạnh {node1} -> {node2} không tồn tại trong đồ thị")
        
        self.adj_list[node1].remove(node2)
        self.num_edges -= 1
        if not self.is_directed:
            self.adj_list[node2].remove(node1)

    def get_neighbors(self, node):
        
        return self.adj_list.get(node, [])

    def get_num_nodes(self):
       
        return self.num_nodes

    def get_num_edges(self):
       
        return self.num_edges

    def has_edge(self, node1, node2):
        
        return node2 in self.adj_list.get(node1, [])

    def print_graph(self):
        """In đồ thị dưới dạng danh sách kề."""
        for node in self.adj_list:
            print(f"{node}: {', '.join(self.adj_list[node])}")