def read_edge_list(file_path):
    edge_list = []
    try:
        with open(file_path, 'r') as file:
            for line in file:
                line = line.strip()
                if line:
                    node1, node2 = line.split()
                    edge_list.append((node1, node2))
        return edge_list
    except FileNotFoundError:
        print(f"Không tìm thấy file: {file_path}")
        return []
    except ValueError:
        print("Định dạng file không đúng: mỗi dòng phải chứa đúng 2 nút.")
        return []

def save_adj_list_to_edge_file(adj_list, file_path, is_directed=False):
    if not adj_list:
        return False, "Adjacency list is empty"
    try:
        with open(file_path, 'w') as file:
            written_edges = set()
            for node1 in adj_list:
                for node2 in adj_list[node1]:
                    edge = (node1, node2)
                    if not is_directed:
                        reverse_edge = (node2, node1)
                        if reverse_edge in written_edges:
                            continue
                    file.write(f"{node1} {node2}\n")
                    written_edges.add(edge)
        print(f"Danh sách cạnh đã được lưu vào file: {file_path}")
        return True, None
    except IOError as e:
        print(f"Lỗi khi ghi file: {e}")
        return False, str(e)