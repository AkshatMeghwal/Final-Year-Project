import os
import re
from collections import defaultdict
from datacontainer import file_processing_info
import networkx as nx
import matplotlib.pyplot as plt

def extract_user_defined_functions(js_file):
    """
    Extracts all user-defined functions from a JavaScript file, including their names, parameters, and code,
    and represents them as JSON objects with keys: name, params, code, and file_path.
    """
    with open(js_file, 'r') as f:
        code = f.read()

    # Regex to match function definitions (traditional and arrow functions)
    function_pattern = re.compile(
        r'function\s+(?P<name>\w+)\s*\((?P<params>[^)]*)\)\s*{(?P<body>[^}]*)}'  # Matches traditional functions
        r'|(?P<arrow_name>\w+)\s*=\s*\((?P<arrow_params>[^)]*)\)\s*=>\s*{(?P<arrow_body>[^}]*)}'  # Matches arrow functions
    )
    matches = function_pattern.finditer(code)

    # Extract full function definitions as JSON
    functions = []
    for match in matches:
        if match.group("name"):  # Traditional function
            function_name = match.group("name")
            function_params = match.group("params").split(",") if match.group("params") else []
            function_code = f"function {function_name}({match.group('params')}) {{{match.group('body')}}}"
        elif match.group("arrow_name"):  # Arrow function
            function_name = match.group("arrow_name")
            function_params = match.group("arrow_params").split(",") if match.group("arrow_params") else []
            function_code = f"{function_name} = ({match.group('arrow_params')}) => {{{match.group('arrow_body')}}}"
        else:
            continue

        # Append the function as a JSON object with the file path
        functions.append({
            "name": function_name.strip(),
            "params": [param.strip() for param in function_params],
            "code": function_code.strip(),
            "code_with_docstring": "",
            "context": "",
            "calls": [],
            "file_path": js_file  # Add the file path
        })

    return functions


def extract_function_calls(func, all_funcs):
    called_functions = set()
    function_names = {f["name"] for f in all_funcs}  # Extract all function names from all_funcs

    # Regex to match function calls (e.g., funcName(...))
    function_call_pattern = re.compile(r'\b(' + '|'.join(re.escape(name) for name in function_names) + r')\s*\(')

    # Search for function calls in the code of the given function
    matches = function_call_pattern.finditer(func["code"])
    for match in matches:
        called_function = match.group(1)
        # Exclude calls to itself
        if called_function != func["name"]:
            called_functions.add(called_function)
            func["calls"].append(called_function)  # Add the called function to the current function's calls

    return called_functions


def get_graph_roots(graph):
    """
    Identifies the root nodes of all disjoint graphs in the dependency graph.

    Parameters:
        graph (networkx.DiGraph): The dependency graph.

    Returns:
        list: A list of root nodes for all disjoint graphs.
    """
    roots = []
    for component in nx.weakly_connected_components(graph):
        subgraph = graph.subgraph(component)
        for node in subgraph.nodes:
            if subgraph.in_degree(node) == 0:  # Nodes with no incoming edges are roots
                roots.append(node)

    # Include isolated nodes (nodes with no edges at all)
    isolated_nodes = list(nx.isolates(graph))
    roots.extend(isolated_nodes)

    # Remove duplicates in case isolated nodes are already included
    roots = list(set(roots))
    return roots


def build_dependency_graph(files: list[file_processing_info]):
    """
    Builds a dependency graph of user-defined functions across multiple files
    and identifies the roots of all disjoint graphs.
    """
    all_functions = []  # List to store all functions from all files

    # Extract functions from all files
    for file_info in files:
        file_path = file_info.filepath
        functions = extract_user_defined_functions(file_path)
        all_functions.extend(functions)

    # Build the dependency graph
    graph = nx.DiGraph()

    # Add all functions as nodes
    for func in all_functions:
        graph.add_node(func["name"], file_path=func["file_path"])

    # Add edges based on function calls
    for func in all_functions:
        print(f"Processing function: {func['name']}")
        called_funcs = extract_function_calls(func, all_functions)
        for called_func in called_funcs:
            graph.add_edge(func["name"], called_func)  # Add an edge from the current function to the called function

    # Ensure all nodes are part of the graph, even if they are isolated
    for func in all_functions:
        if func["name"] not in graph.nodes:
            graph.add_node(func["name"], file_path=func["file_path"])

    # Get roots of all disjoint graphs
    roots = get_graph_roots(graph)
    print(f"Identified roots: {roots}")

    return graph, all_functions, roots


def plot_dependency_graph(graph, file_name, folder_name="graph"):
    """
    Plots the combined dependency graph using NetworkX and saves it to a file.
    
    Parameters:
        graph (networkx.DiGraph): The dependency graph to plot.
        file_name (str): The name of the file to save the graph as.
        folder_name (str): The name of the folder to save the graph in. Defaults to "graph".
    """
    folder_name = './graph'  # Ensure the graph is saved in the correct folder
    os.makedirs(folder_name, exist_ok=True)

    # Plot the graph
    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(graph)
    nx.draw(graph, pos, with_labels=True, node_size=2000, node_color="lightblue", font_size=10, font_weight="bold", edge_color="gray")
    plt.title("Combined Function Dependency Graph")

    # Save the graph to the specified file
    file_path = os.path.join(folder_name, file_name)
    plt.savefig(file_path)
    plt.close()  # Close the plot to free memory
    print(f"Graph saved to {file_path}")

