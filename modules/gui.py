import tkinter as tk
from tkinter import messagebox, ttk, scrolledtext, filedialog
from modules.graph import SocialGraph
from modules.bfs import BFSProcessor
from modules.dfs import DFSProcessor
from modules.utils import read_edge_list, save_adj_list_to_edge_file
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import networkx as nx

class SocialGraphApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Social Graph Analyzer")
        self.graph = None
        self.is_directed = tk.BooleanVar(value=False)
        self.canvas = None

        # Thanh menu
        menubar = tk.Menu(root)
        root.config(menu=menubar)
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open File", command=self.open_file)
        file_menu.add_command(label="Save File", command=self.save_file)

        # Khung chính
        main_frame = ttk.Frame(root, padding="10")
        main_frame.grid(row=0, column=0, sticky="nsew")

        # Nút chọn loại đồ thị
        ttk.Label(main_frame, text="Graph Type:").grid(row=0, column=0, sticky="w")
        ttk.Radiobutton(main_frame, text="Directed", variable=self.is_directed, value=True).grid(row=0, column=1)
        ttk.Radiobutton(main_frame, text="Undirected", variable=self.is_directed, value=False).grid(row=0, column=2)

        # Notebook (các tab)
        notebook = ttk.Notebook(main_frame)
        notebook.grid(row=1, column=0, columnspan=3, pady=10, sticky="nsew")

        # Tab 1: Thao tác đồ thị
        graph_tab = ttk.Frame(notebook)
        notebook.add(graph_tab, text="Graph Operations")
        self.setup_graph_tab(graph_tab)

        # Tab 2: DFS
        dfs_tab = ttk.Frame(notebook)
        notebook.add(dfs_tab, text="DFS")
        self.setup_dfs_tab(dfs_tab)

        # Tab 3: BFS
        bfs_tab = ttk.Frame(notebook)
        notebook.add(bfs_tab, text="BFS")
        self.setup_bfs_tab(bfs_tab)

        # Tìm độ tách biệt
        ttk.Label(main_frame, text="Degrees of Separation:").grid(row=2, column=0, sticky="w")
        self.sep_start = ttk.Entry(main_frame, width=10)
        self.sep_start.grid(row=2, column=1)
        self.sep_end = ttk.Entry(main_frame, width=10)
        self.sep_end.grid(row=2, column=2)
        ttk.Button(main_frame, text="Find", command=self.find_degrees_of_separation).grid(row=2, column=3)

        # Khu vực kết quả
        self.results_text = scrolledtext.ScrolledText(main_frame, width=60, height=10)
        self.results_text.grid(row=3, column=0, columnspan=4, pady=10)

        # Khu vực hiển thị đồ thị
        self.graph_frame = ttk.Frame(main_frame)
        self.graph_frame.grid(row=4, column=0, columnspan=4, pady=10, sticky="nsew")
        self.update_graph_visualization()

        # Cấu hình trọng số lưới
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(4, weight=1)

    def setup_graph_tab(self, tab):
        ttk.Label(tab, text="Add Node:").grid(row=0, column=0, sticky="w")
        self.node_entry = ttk.Entry(tab, width=20)
        self.node_entry.grid(row=0, column=1)
        ttk.Button(tab, text="Add", command=self.add_node).grid(row=0, column=2)

        ttk.Label(tab, text="Add Edge:").grid(row=1, column=0, sticky="w")
        self.edge_node1 = ttk.Entry(tab, width=10)
        self.edge_node1.grid(row=1, column=1)
        self.edge_node2 = ttk.Entry(tab, width=10)
        self.edge_node2.grid(row=1, column=2)
        ttk.Button(tab, text="Add", command=self.add_edge).grid(row=1, column=3)

        ttk.Button(tab, text="Remove Node", command=self.remove_node).grid(row=2, column=0)
        ttk.Button(tab, text="Remove Edge", command=self.remove_edge).grid(row=2, column=1)
        ttk.Button(tab, text="Show Graph Info", command=self.show_graph_info).grid(row=2, column=2)

    def setup_dfs_tab(self, tab):
        ttk.Label(tab, text="Node:").grid(row=0, column=0, sticky="w")
        self.dfs_node_entry = ttk.Entry(tab, width=10)
        self.dfs_node_entry.grid(row=0, column=1)

        ttk.Button(tab, text="DFS Traversal", command=self.dfs_traversal).grid(row=1, column=0)
        ttk.Button(tab, text="Detect Cycle", command=self.dfs_has_cycle).grid(row=1, column=1)
        ttk.Button(tab, text="Find Communities", command=self.dfs_find_communities).grid(row=1, column=2)
        ttk.Button(tab, text="Suggest Friends", command=self.dfs_suggest_friends).grid(row=2, column=0)
        ttk.Button(tab, text="Influence Analysis", command=self.dfs_influence_analysis).grid(row=2, column=1)

    def setup_bfs_tab(self, tab):
        ttk.Label(tab, text="Node:").grid(row=0, column=0, sticky="w")
        self.bfs_node_entry = ttk.Entry(tab, width=10)
        self.bfs_node_entry.grid(row=0, column=1)

        ttk.Button(tab, text="BFS Traversal", command=self.bfs_traversal).grid(row=1, column=0)
        ttk.Button(tab, text="Detect Cycle", command=self.bfs_has_cycle).grid(row=1, column=1)
        ttk.Button(tab, text="Find Communities", command=self.bfs_find_communities).grid(row=1, column=2)
        ttk.Button(tab, text="Suggest Friends", command=self.bfs_suggest_friends).grid(row=2, column=0)
        ttk.Button(tab, text="Influence Analysis", command=self.bfs_influence_analysis).grid(row=2, column=1)

        ttk.Label(tab, text="Start Node:").grid(row=3, column=0, sticky="w")
        self.bfs_start_node = ttk.Entry(tab, width=10)
        self.bfs_start_node.grid(row=3, column=1)
        ttk.Label(tab, text="End Node:").grid(row=3, column=2, sticky="w")
        self.bfs_end_node = ttk.Entry(tab, width=10)
        self.bfs_end_node.grid(row=3, column=3)
        ttk.Button(tab, text="Bidirectional BFS", command=self.bfs_bidirectional).grid(row=3, column=4)

    def update_graph_visualization(self):
        if self.canvas:
            self.canvas.get_tk_widget().destroy()
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.set_title("Graph Visualization")
        if self.graph and self.graph.adj_list:
            G = nx.DiGraph() if self.is_directed.get() else nx.Graph()
            for node in self.graph.adj_list:
                G.add_node(node)
                for neighbor in self.graph.get_neighbors(node):
                    G.add_edge(node, neighbor)
            pos = nx.spring_layout(G)
            nx.draw(G, pos, with_labels=True, node_color="lightblue", node_size=500, font_size=10, ax=ax)
        else:
            ax.text(0.5, 0.5, "No graph loaded", horizontalalignment="center", verticalalignment="center")
        self.canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        plt.close(fig)

    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            edges = read_edge_list(file_path)
            if edges:
                self.graph = SocialGraph(is_directed=self.is_directed.get())
                self.graph.build_from_edges(edges)
                self.results_text.delete(1.0, tk.END)
                self.results_text.insert(tk.END, f"Loaded graph from {file_path}\n")
                self.update_graph_visualization()
            else:
                messagebox.showerror("Error", "Invalid file format or file not found")

    def save_file(self):
        if self.graph is None or not self.graph.adj_list:
            messagebox.showwarning("Warning", "No graph to save")
            return
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file_path:
            success, error_msg = save_adj_list_to_edge_file(self.graph.adj_list, file_path, self.is_directed.get())
            if success:
                self.results_text.delete(1.0, tk.END)
                self.results_text.insert(tk.END, f"Saved graph to {file_path}\n")
                self.update_graph_visualization()
            else:
                messagebox.showerror("Error", f"Failed to save file: {error_msg}")

    def add_node(self):
        node = self.node_entry.get().strip()
        if not node:
            messagebox.showwarning("Warning", "Please enter a node name")
            return
        if self.graph is None:
            self.graph = SocialGraph(is_directed=self.is_directed.get())
        if self.graph.add_node(node):
            self.results_text.insert(tk.END, f"Added node: {node}\n")
            self.update_graph_visualization()
        else:
            messagebox.showwarning("Warning", f"Node {node} already exists")

    def add_edge(self):
        node1 = self.edge_node1.get().strip()
        node2 = self.edge_node2.get().strip()
        if not node1 or not node2:
            messagebox.showwarning("Warning", "Please enter both nodes")
            return
        if self.graph is None:
            self.graph = SocialGraph(is_directed=self.is_directed.get())
        self.graph.add_edge(node1, node2)
        self.results_text.insert(tk.END, f"Added edge: {node1} -> {node2}\n")
        self.update_graph_visualization()

    def remove_node(self):
        node = self.node_entry.get().strip()
        if not node or self.graph is None:
            messagebox.showwarning("Warning", "Please enter a node and load a graph")
            return
        try:
            self.graph.remove_node(node)
            self.results_text.insert(tk.END, f"Removed node: {node}\n")
            self.update_graph_visualization()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def remove_edge(self):
        node1 = self.edge_node1.get().strip()
        node2 = self.edge_node2.get().strip()
        if not node1 or not node2 or self.graph is None:
            messagebox.showwarning("Warning", "Please enter both nodes and load a graph")
            return
        try:
            self.graph.remove_edge(node1, node2)
            self.results_text.insert(tk.END, f"Removed edge: {node1} -> {node2}\n")
            self.update_graph_visualization()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def show_graph_info(self):
        if self.graph is None or not self.graph.adj_list:
            messagebox.showwarning("Warning", "No graph loaded")
            return
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, "Graph Info:\n")
        for node in self.graph.adj_list:
            neighbors = self.graph.get_neighbors(node)
            if neighbors:
                self.results_text.insert(tk.END, f"{node}: {', '.join(neighbors)}\n")
            else:
                self.results_text.insert(tk.END, f"{node}: (no connections)\n")
        self.results_text.insert(tk.END, f"Total nodes: {self.graph.get_num_nodes()}\n")
        self.results_text.insert(tk.END, f"Total edges: {self.graph.get_num_edges()}\n")
        self.update_graph_visualization()

    def dfs_traversal(self):
        if self.graph is None:
            messagebox.showwarning("Warning", "No graph loaded")
            return
        node = self.dfs_node_entry.get().strip()
        if not node:
            messagebox.showwarning("Warning", "Please enter a start node")
            return
        dfs = DFSProcessor(self.graph, self.is_directed.get())
        result = dfs.dfs_traversal(node)
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, f"DFS Traversal from {node}: {result}\n")
        self.update_graph_visualization()

    def dfs_has_cycle(self):
        if self.graph is None:
            messagebox.showwarning("Warning", "No graph loaded")
            return
        dfs = DFSProcessor(self.graph, self.is_directed.get())
        result = dfs.has_cycle()
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, f"Has Cycle: {result}\n")
        self.update_graph_visualization()

    def dfs_find_communities(self):
        if self.graph is None:
            messagebox.showwarning("Warning", "No graph loaded")
            return
        dfs = DFSProcessor(self.graph, self.is_directed.get())
        result = dfs.find_communities()
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, f"Communities: {result}\n")
        self.update_graph_visualization()

    def dfs_suggest_friends(self):
        if self.graph is None:
            messagebox.showwarning("Warning", "No graph loaded")
            return
        node = self.dfs_node_entry.get().strip()
        if not node:
            messagebox.showwarning("Warning", "Please enter a node")
            return
        dfs = DFSProcessor(self.graph, self.is_directed.get())
        result = dfs.suggest_friends(node)  # Giả định có hàm này
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, f"Suggested Friends for {node}: {result}\n")
        self.update_graph_visualization()

    def dfs_influence_analysis(self):
        if self.graph is None:
            messagebox.showwarning("Warning", "No graph loaded")
            return
        node = self.dfs_node_entry.get().strip()
        if not node:
            messagebox.showwarning("Warning", "Please enter a node")
            return
        dfs = DFSProcessor(self.graph, self.is_directed.get())
        result = dfs.influence_analysis(node)  # Giả định có hàm này
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, f"Influence Analysis for {node}: {result}\n")
        self.update_graph_visualization()

    def bfs_traversal(self):
        if self.graph is None:
            messagebox.showwarning("Warning", "No graph loaded")
            return
        node = self.bfs_node_entry.get().strip()
        if not node:
            messagebox.showwarning("Warning", "Please enter a start node")
            return
        bfs = BFSProcessor(self.graph, self.is_directed.get())
        result = bfs.bfs_traversal(node)
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, f"BFS Traversal from {node}: {result}\n")
        self.update_graph_visualization()

    def bfs_has_cycle(self):
        if self.graph is None:
            messagebox.showwarning("Warning", "No graph loaded")
            return
        bfs = BFSProcessor(self.graph, self.is_directed.get())
        result = bfs.has_cycle()
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, f"Has Cycle: {result}\n")
        self.update_graph_visualization()

    def bfs_find_communities(self):
        if self.graph is None:
            messagebox.showwarning("Warning", "No graph loaded")
            return
        bfs = BFSProcessor(self.graph, self.is_directed.get())
        result = bfs.find_communities()
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, f"Communities: {result}\n")
        self.update_graph_visualization()

    def bfs_suggest_friends(self):
        if self.graph is None:
            messagebox.showwarning("Warning", "No graph loaded")
            return
        node = self.bfs_node_entry.get().strip()
        if not node:
            messagebox.showwarning("Warning", "Please enter a node")
            return
        bfs = BFSProcessor(self.graph, self.is_directed.get())
        result = bfs.suggest_friends(node)  # Giả định có hàm này
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, f"Suggested Friends for {node}: {result}\n")
        self.update_graph_visualization()

    def bfs_influence_analysis(self):
        if self.graph is None:
            messagebox.showwarning("Warning", "No graph loaded")
            return
        node = self.bfs_node_entry.get().strip()
        if not node:
            messagebox.showwarning("Warning", "Please enter a node")
            return
        bfs = BFSProcessor(self.graph, self.is_directed.get())
        result = bfs.influence_analysis(node)  # Giả định có hàm này
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, f"Influence Analysis for {node}: {result}\n")
        self.update_graph_visualization()

    def bfs_bidirectional(self):
        if self.graph is None:
            messagebox.showwarning("Warning", "No graph loaded")
            return
        start = self.bfs_start_node.get().strip()
        end = self.bfs_end_node.get().strip()
        if not start or not end:
            messagebox.showwarning("Warning", "Please enter both start and end nodes")
            return
        bfs = BFSProcessor(self.graph, self.is_directed.get())
        result = bfs.bidirectional_bfs(start, end)  # Giả định có hàm này
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, f"Bidirectional BFS from {start} to {end}: {result}\n")
        self.update_graph_visualization()

    def find_degrees_of_separation(self):
        if self.graph is None:
            messagebox.showwarning("Warning", "No graph loaded")
            return
        start = self.sep_start.get().strip()
        end = self.sep_end.get().strip()
        if not start or not end:
            messagebox.showwarning("Warning", "Please enter both start and end nodes")
            return
        bfs = BFSProcessor(self.graph, self.is_directed.get())
        distance, path = bfs.degrees_of_separation(start, end)
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, f"Degrees of Separation {start} -> {end}: Distance={distance}, Path={path}\n")
        self.update_graph_visualization()