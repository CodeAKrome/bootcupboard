#!env python3
import networkx as nx
import json
from pyvis.network import Network
import fnmatch
import sys

# FROM: https://cerfacs.fr/coop/pycallgraph
# pip install graphviz networkx pyvis pycg
# pycg $(find interpreter -type f -name "*.py") -o callgraph.json

graph_width="2000px"
graph_height="1500px"

color_filter={
    "cli": "red",
    "code_interpreters": "purple", 
    "core": "darkblue",
    "terminal_interface": "blue",
    "lib": "green",
    "llm": "red",
    "rag": "orange",
    "utils": "lightgreen",
    "huggingface": "yellow",
    "default": "black",
}

if len(sys.argv) > 1:
    rootnode = sys.argv[1]
    jsonfile = sys.argv[2]
    outfile = sys.argv[3]
else:
    rootnode = "create_code_interpreter"
    jsonfile = "callgraph.json"
    outfile = "callgraph.html"
    
def to_ntwx_json(data: dict)->  nx.DiGraph:

    nt = nx.DiGraph()

    def _ensure_key(name):
        if name not in nt:
            nt.add_node(name, size=50)
    for node in data:
        _ensure_key(node)
        for child in data[node]:
            _ensure_key(child)
            nt.add_edge(node,child)
    return nt


def ntw_pyvis(ntx:nx.DiGraph, root, size0=5, loosen=2):
    nt = Network(width=graph_width,height=graph_height, directed=True)
    for node in ntx.nodes:
        mass = ntx.nodes[node]["size"]/(loosen*size0)
        size = size0*ntx.nodes[node]["size"]**0.5
        label = node
        color=color_filter["default"]
        for key in color_filter:
            if key in node:
                color=color_filter[key]
        kwargs= {
            "label":label, 
            "mass":mass,
            "size":size,
            "color":color,
            "font": '30px arial black',
        }
        nt.add_node(node, **kwargs,)

    for link in ntx.edges:
        try:
            depth = nx.shortest_path_length(ntx, source=root, target=link[0])
            width =max(size0,size0*(12 - 4*depth))
        except:
            width=5

        nt.add_edge(link[0], link[1], width=width)

    nt.show_buttons(filter_=["physics"])
    nt.show(outfile, notebook=False)

    
def ntw_pyvis_simple(ntx:nx.DiGraph):
    net = Network(width="1000px",height="1000px", directed=True)
    for node in ntx.nodes:
        #print(node)
        net.add_node(node, **{"label":node},)

    for edge in ntx.edges:
        net.add_edge(edge[0], edge[1], width=1)
    net.show('graph.html', notebook=False)


def remove_hyperconnect(ntx: nx.DiGraph, treshold=5):
    """Remove hyperconnected nodes from the graph by incoming edges"""
    to_remove = []
    for node in ntx.nodes:
        if len(list(ntx.predecessors(node))) >= treshold:
            to_remove.append(node)

    for node in to_remove:
        ntx.remove_node(node)
    return ntx
        
def remove_by_patterns(ntx: nx.DiGraph,forbidden_names: list=[])-> nx.DiGraph:
    """Exclude nodes by name pattern matching"""
    def is_allowed(name):
        for pattern in forbidden_names:
            if fnmatch.filter([name], pattern):
                return False
        return True

    to_remove = []
    for node in ntx.nodes:
        if not is_allowed(node):
            to_remove.append(node)

    for node in to_remove:
        ntx.remove_node(node)

    return ntx

# --- MAIN ---

with open(jsonfile,"r") as fin:
    cgdata = json.load(fin)


ntx = to_ntwx_json(cgdata)
ntx = remove_hyperconnect(ntx)
ntx = remove_by_patterns(ntx, forbidden_names=[
     "<builtin>*",
     "numpy*",
     "tkinter*"
])

    
print(f"nodes: {ntx.number_of_nodes()}")
ntw_pyvis(ntx, rootnode)
