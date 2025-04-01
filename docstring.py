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

def generate_context(dependency_tree: nx.DiGraph, all_functions: list[dict]):
    """
    Performs DFS on the dependency tree and generates context for each function.

    Parameters:
        dependency_tree (networkx.DiGraph): The dependency graph of functions.
        all_functions (list): A list of all functions with their details.

    Returns:
        list: The updated list of all functions with generated contexts.
    """
    # Create a mapping of function names to their corresponding function objects
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
            child_contexts.append(child_context)

        # Combine the current function's code with the contexts of its children
        # combined_context = AI_generated_context(current_code, child_contexts)
        combined_context = "Context for function " + function_map[node]["name"]
        function_map[node]["context"] = combined_context
        logging.info(f"Generated context for {node}")
        return combined_context

    # Perform DFS for all nodes in the graph
    for node in list(dependency_tree.nodes):
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
    
    context_funcs = generate_context(dependency_tree, funcs)
    print(context_funcs)
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
