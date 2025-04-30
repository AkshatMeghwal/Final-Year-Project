import logging.config
import api_calls
from dependencyGraph import build_dependency_graph, plot_dependency_graph
import constants
from logger import logging
import os
import sys
from utils import Misc
from datacontainer import file_processing_info
from utils import CommentRemover
import networkx as nx
import matplotlib.pyplot as plt

def generate_context(dependency_tree: nx.DiGraph, all_functions: list[dict], roots: list):
    """
    Performs DFS on the dependency tree for all root nodes and generates context for each function.

    Parameters:
        dependency_tree (networkx.DiGraph): The dependency graph of functions.
        all_functions (list): A list of all functions with their details.
        roots (list): A list of root nodes for all disjoint graphs.

    Returns:
        list: The updated list of all functions with generated contexts.
    """
    # Create a mapping of function names to their corresponding function objects
    prompt_start = constants.AIPrompts.GAI_FUNCTION_DOCSTRING_PROMPT
    prompt_model = constants.AIPrompts.GAI_FUNCTION_DOCSTRING_MODEL_PROMPT
    gemini_ai = api_calls.gemini_ai()
    function_map = {func["name"]: func for func in all_functions}

    def dfs(node):
        # If the context for this node is already generated, skip it
        if function_map[node]["context"] != "":
            return function_map[node]["context"]

        # Get the code of the current function
        current_code = function_map[node]["code"]

        # Get the contexts of all child functions (successors)
        child_contexts = []
        for child in dependency_tree.successors(node):
            child_context = dfs(child)  # Recursively generate context for the child
            if child_context:  # Ensure child_context is valid before appending
                child_contexts.append(child_context)
        
        # Combine the current function's code with the contexts of its children
        attached_code_prompt = Misc.create_function_prompt(child_contexts, current_code)
        combined_context = gemini_ai.get_outputcoderaw_geminiai(
            prompt_start, attached_code_prompt, prompt_model
        )
        combined_context = "\n".join(combined_context.split("\n")[1:])  # Trim the first line
        logging.info(f"{function_map[node]['name']} ----  context: {combined_context}")
        function_map[node]["context"] = combined_context
        logging.info(f"Generated context for {node}")
        return combined_context

    # Perform DFS for all root nodes in the graph
    visited = set()
    for root in roots:
        if root not in visited:
            dfs(root)
            visited.add(root)

    # Ensure all nodes are visited in case of disconnected graphs
    for node in dependency_tree.nodes:
        if node not in visited:
            dfs(node)

    # Return the updated all_functions list with contexts
    return all_functions

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
    logging.info(f"Graph saved to {file_path}")

def process_js_files(folder_directory: str, review_mode: bool = False):
    """Process all JavaScript files in the given folder."""
    js_files_paths = Misc.get_js_files(folder_directory)
    if len(js_files_paths) == 0:
        logging.error("No JavaScript files found in the directory")
        return

    files: list[file_processing_info] = []
    for js_file in js_files_paths:
        files.append(file_processing_info(js_file))

    logging.info("Files read successfully.")
    
    # Build the dependency graph
    dependency_tree, funcs, roots = build_dependency_graph(files)
    print(roots)
    plot_dependency_graph(dependency_tree, "dependency_graph.png", folder_name='./graph')
    logging.info("Dependency Graph has been built successfully.")
    
    # Generate context for each function using DFS
    context_funcs = generate_context(dependency_tree, funcs, roots)
    logging.debug(f"Generated contexts for functions: {context_funcs}")  # Debugging line
    
    logging.info("Context generation completed successfully.")
    
    prompt_start = constants.AIPrompts.GAI_DOCSTRING_PROMPT
    prompt_model = constants.AIPrompts.GAI_DOCSTRING_MODEL_PROMPT
    gemini_ai = api_calls.gemini_ai()

    # Create an instance of CommentRemover
    comment_remover = CommentRemover()

    changes_for_review = {}
    for fileprocessinginfo in files:
        fileprocessinginfo.raw_code_no_comment = comment_remover.remove_comments_from_js(fileprocessinginfo.raw_code)
        output_code_raw = fileprocessinginfo.raw_code
        fileprocessinginfo.output_code_raw = output_code_raw
        
        fileprocessinginfo.output_code_raw_no_comment = comment_remover.remove_comments_from_js(output_code_raw)
        if fileprocessinginfo.raw_code_no_comment == fileprocessinginfo.output_code_raw_no_comment:
            # Insert context above each function in the file
            for func in context_funcs:
                function_name = func["name"]
                function_context = func["context"]
                fileprocessinginfo.output_code_raw = Misc.insert_context_above_function(
                    fileprocessinginfo.output_code_raw, function_name, function_context
                )
            if review_mode:
                # Highlight changes for review
                changes_for_review[fileprocessinginfo.filepath] = {
                    "original": fileprocessinginfo.raw_code,
                    "modified": Misc.highlight_changes(
                        fileprocessinginfo.raw_code, fileprocessinginfo.output_code_raw
                    ),
                    "functions": context_funcs,  # Include functions with context
                }
            else:
                with open(fileprocessinginfo.write_filepath, "w") as f:
                    f.write(fileprocessinginfo.output_code_raw)
        else:
            logging.warning("Invalid code received for %s", fileprocessinginfo.filepath)

    if review_mode:
        return changes_for_review

    logging.info("Output written to files successfully.")

if __name__ == "__main__":
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        logging.error("Usage: python docstring.py <folder_directory> [review_mode]")
        sys.exit(1)

    folder_directory = sys.argv[1]
    review_mode = sys.argv[2].lower() == 'true' if len(sys.argv) == 3 else False
    process_js_files(folder_directory, review_mode)
