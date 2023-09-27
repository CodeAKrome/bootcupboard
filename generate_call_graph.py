#!env python3
import networkx as nx
import json
from pyvis.network import Network
import fnmatch
import sys

"""Generate an HTML file with a call graph including controls for view rendering"""


# FROM: https://cerfacs.fr/coop/pycallgraph
# pip install graphviz networkx pyvis pycg
# pycg $(find interpreter -type f -name "*.py") -o callgraph.json
# pycg $(find . -name "*.py" -type f -and ! -path "./archive/*") -o callgraph.json
# ./generate_call_graph.py '__init__' azure.json CGraph_20230925_init.html

# G = nx.DiGraph()
# print(dir(G))

if len(sys.argv) > 1:
    rootnode = sys.argv[1]
    jsonfile = sys.argv[2]
    outfile = sys.argv[3]
else:
    rootnode = "create_code_interpreter"
    jsonfile = "callgraph.json"
    outfile = "callgraph.html"

graph_width="2500px"
graph_height="1500px"
font = '50px arial black'
root_font = '60px arial red'

forbidden_names_list=[
    "<builtin>*",
    "archive*",
    "datetime*",
    "os.*",
    "argparse.*",
    "ast.*",
    "re.*",
    "rich.*",
]

color_filter={
    "cli": "tan",
    "code_interpreters": "darkred", 
    "languages": "red",
    "core": "yellow",
    "terminal_interface": "darkgreen",
    "components": "green",
    "lib": "blue",
    "llm": "indigo",
    "rag": "gold",
    "utils": "orange",
    "huggingface": "yellow",
    "archive": "darkpink",
    rootnode: "magenta",
    "default": "black",
}

    
def to_ntwx_json(data: dict)->  nx.DiGraph:
    """Build a nx.DiGraph from a dictionary"""
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


def ntw_pyvis(ntx:nx.DiGraph, root, size0=6, loosen=2):
    """Display nx.DiGraph"""
    nt = Network(width=graph_width,height=graph_height, directed=True)

    for node in ntx.nodes:
        mass = ntx.nodes[node]["size"]/(loosen*size0)


        size = size0*ntx.nodes[node]["size"]**0.5
        connections = ntx.in_degree(node) + ntx.out_degree(node)
        size = size0*connections

        
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
            "font": font,
        }
        # Target node is special case
        if rootnode in node:
            kwargs['color'] = color_filter[rootnode]
            kwargs['size'] = kwargs['size']*1.5
            kwargs['font'] = root_font
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


def pry(ntx: nx.DiGraph, mark="X"):
    """Diagnostics"""
    for node in ntx.nodes:
        print(f"{mark}\t{node}\n<- {ntx.in_degree(node)} {ntx.in_edges(node)}\n->{ntx.out_degree(node)} {ntx.out_edges(node)}\n")

def remove_underconnect(ntx: nx.DiGraph, treshold=1):
    """Remove underconnected nodes from the graph if no edges"""
    to_remove = []

    for node in ntx.nodes:
        if ntx.in_degree(node) == 0 and ntx.out_degree(node) == 0:
            to_remove.append(node)

    for node in to_remove:
        ntx.remove_node(node)
    return ntx
    

# =====--- MAIN ---=====


with open(jsonfile,"r") as fin:
    cgdata = json.load(fin)


ntx = to_ntwx_json(cgdata)
original_node_cnt = ntx.number_of_nodes()
ntx = remove_by_patterns(ntx, forbidden_names=forbidden_names_list)
# pry(ntx)
# print("\n\n--------------------------------\n\n")
ntx = remove_underconnect(ntx)
#ntx = remove_hyperconnect(ntx)

# for ent in dir(ntx):
#     print(ent)
    
# pry(ntx, "Y")
diff = original_node_cnt - ntx.number_of_nodes()
print(f"nodes[{ntx.number_of_nodes()}] = {original_node_cnt} - {diff}")
ntw_pyvis(ntx, rootnode)
