import heapq
import numpy as np
# import networkx as nx
import matplotlib.pyplot as plt

class Node:
    def __init__(self, symbol, prob):
        self.symbol = symbol
        self.prob = prob
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.prob < other.prob


# Huffman 코드 생성 함수
def build_huffman_tree(probabilities):
    heap = [Node(symbol, prob) for symbol, prob in probabilities.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        merged_node = Node(None, left.prob + right.prob)
        merged_node.left = left
        merged_node.right = right
        heapq.heappush(heap, merged_node)

    return heap[0]


# Huffman 코드 테이블 생성 함수
def build_huffman_codes(root, prefix="", code_table=None):
    if code_table is None:
        code_table = {}

    if root is not None:
        if root.symbol is not None:
            code_table[root.symbol] = prefix
        build_huffman_codes(root.left, prefix + "0", code_table)
        build_huffman_codes(root.right, prefix + "1", code_table)
    sorted_code_table = {key: code_table[key] for key in sorted(code_table)}

    return sorted_code_table

def huffman_encode(data, huffman_codes):
    chunks = [data[i:i + 4] for i in range(0, len(data), 4)]
    encoded_data = ""
    for symbol in chunks:
        encoded_data += huffman_codes[symbol]

    return encoded_data

def cal_Entropy(sym_prob) :
    Entropy = 0

    for symbol, code in sym_prob.items():
        Entropy = Entropy - code*np.log2(code)

    return Entropy

def avg_bitpersym(huffmancode,probabilities) :
    avg = 0

    for (symbol, code), (sym,p) in zip(huffmancode.items(), probabilities.items()):
        avg = avg + p*len(code)

    return avg


# Huffman 트리를 시각화하기 위한 함수
# def visualize_huffman_tree(root):
#     G = nx.Graph()
#
#     def add_edges(node, parent_label=""):
#         if node is not None:
#             if node.symbol is not None:
#                 label = f"{node.symbol} ({node.prob})"
#             else:
#                 label = f"{node.prob}"
#             G.add_node(label)
#             if parent_label:
#                 G.add_edge(parent_label, label)
#             add_edges(node.left, label)
#             add_edges(node.right, label)
#
#     add_edges(root)
#     pos = nx.spring_layout(G)  # 레이아웃 설정
#     labels = nx.draw_networkx_labels(G, pos)
#     nx.draw(G, pos, with_labels=True, node_size=500, node_color='skyblue', font_size=10)
#     plt.axis('off')
#     plt.show()