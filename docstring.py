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

def generate_context(graph: nx.DiGraph, all_functions: list[dict]):
    """
    Performs DFS on the dependency graph and generates context for nodes.

    Parameters:
        graph (networkx.DiGraph): The dependency graph.
        all_functions (list): A list of all functions with their details.

    Returns:
        dict: The updated context map with generated contexts.
    """
    # Create a mapping of function names to their corresponding function objects
    function_map = {func["name"]: func for func in all_functions}

    def dfs(node):
        # If the context for this node is already generated, skip it
        if function_map[node]["context"]:
            return function_map[node]["context"]

        # Get all children (successors) of the current node
        children = list(graph.successors(node))

        # Check if all children have their context generated
        for child in children:
            if not function_map[child]["context"]:
                dfs(child)  # Recursively generate context for the child

        # Generate context for the current node if it is a leaf or all children have context
        if not children or all(function_map[child]["context"] for child in children):
            function_map[node]["context"] = f"Context for {node}"  # Replace with actual context generation logic
            logging.info(f"Generated context for {node}")
        else:
            logging.info(f"Skipped context generation for {node} (waiting for children)")

        return function_map[node]["context"]

    # Perform DFS for all nodes in the graph
    for node in list(graph.nodes):
        dfs(node)

    # Return the updated all_functions list with contexts
    return all_functions


def process_js_files(folder_directory: str):
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
    dependency_tree, funcs = build_dependency_graph(files)
    plot_dependency_graph(dependency_tree, "dependency_graph.png")
    logging.info("Dependency Graph has been built successfully.")
    
    logging.info("Dependency Tree has been built successfully.")
    
    # generate_context(dependency_tree, {})
    logging.info("Context generation completed successfully.")
    prompt_start = constants.AIPrompts.GAI_DOCSTRING_PROMPT
    prompt_model = constants.AIPrompts.GAI_DOCSTRING_MODEL_PROMPT
    gemini_ai = api_calls.gemini_ai()

    # # Create an instance of CommentRemover
    comment_remover = CommentRemover()

    for fileprocessinginfo in files:
        fileprocessinginfo.raw_code_no_comment = comment_remover.remove_comments_from_js(fileprocessinginfo.raw_code)
        output_code_raw = gemini_ai.get_outputcoderaw_geminiai(
            prompt_start, fileprocessinginfo.raw_code, prompt_model
        )
        output_code_raw = Misc.output_cleaner(output_code_raw)
        fileprocessinginfo.output_code_raw = output_code_raw
        
        fileprocessinginfo.output_code_raw_no_comment = comment_remover.remove_comments_from_js(output_code_raw)
        if fileprocessinginfo.raw_code_no_comment == fileprocessinginfo.output_code_raw_no_comment:
            with open(fileprocessinginfo.write_filepath, "w") as f:
                f.write(fileprocessinginfo.output_code_raw)
        else:
            logging.warning("Invalid code received for %s", fileprocessinginfo.filepath)

    logging.info("Output written to files successfully.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        logging.error("Usage: python docstring.py <folder_directory>")
        sys.exit(1)

    folder_directory = sys.argv[1]
    process_js_files(folder_directory)
