from os import path, walk, makedirs
from typing import Union, List, Optional
import time
from argparse import ArgumentParser
from sys import maxsize
from dotenv import dotenv_values
from tree_sitter import Language, Parser, Node
import re
import json
from logger import logging
import shutil
import tree_sitter_javascript as tsjavascript
from tree_sitter import Language, Parser

class Misc():
    @staticmethod
    def get_content(filepath: str) -> str:
        """Get file content

        Args:
            filepath (str): Path of file to be processed
            execdetails (ExecutionDetails): current execution details
        """
        if path.exists(filepath) is False:
            logging.error("File does not exists: %s", filepath)
            return ""

        codefile_content: str = ""
        try:
            with open(filepath, "r", encoding="utf-8") as file:
                codefile_content = file.read()
        except OSError:
            logging.exception(
                "Failed to read file. '%s'",
                filepath.replace(filepath),
            )
            return codefile_content
        except UnicodeDecodeError:
            logging.exception(
                "Failed to read file. '%s'",
                filepath.replace(filepath),
            )
            return codefile_content

        if len(codefile_content) == 0:
            logging.warning(
                "Empty file. '%s'",
                filepath.replace(filepath),
            )

        return codefile_content

    @staticmethod
    def get_js_files(directory: str) -> List[str]:
        """Get paths of JavaScript files in the given directory

        Args:
            directory (str): Path of the directory to search

        Returns:
            List[str]: List of JavaScript file paths
        """
        js_files:List[str] = []
        for root, _, files in walk(directory):
            for file in files:
                if file.endswith(".js"):
                    js_files.append(path.join(root, file))
        return js_files
    @staticmethod
    def generate_write_filepath(filepath: str) -> str:
        """Generate the write file path with '_copy' attached to the original file name

        Args:
            filepath (str): Original file path

        Returns:
            str: New file path with '_copy' attached
        """
        base, ext = path.splitext(filepath)
        return f"{base}_copy{ext}"
    
    @staticmethod
    def output_cleaner(output: str) -> str:
        """Clean the output by removing the first and last line

        Args:
            output (str): Output to be cleaned

        Returns:
            str: Cleaned output
        """
        output_lines = output.split("\n")
        if len(output_lines) > 2:
            output = "\n".join(output_lines[1:-1])
        return output

    @staticmethod
    def clean_temp_folders(*folders: str):
        """Clean up temporary folders."""
        for folder in folders:
            if path.exists(folder):
                shutil.rmtree(folder)

    @staticmethod
    def create_function_prompt(childs:List,code:str):
        """Clean up temporary folders."""
        attached_prompt:str=""
        for text in childs:
            attached_prompt+=text
            attached_prompt+="\n"
        attached_prompt+=code
        return attached_prompt

    
    @staticmethod
    def write_output_in_structure(output: str, original_filepath: str, base_input_dir: str, base_output_dir: str) -> None:
        """Write output in another folder with the same structure as the given folder

        Args:
            output (str): The output content to be written
            original_filepath (str): The original file path
            base_input_dir (str): The base input directory
            base_output_dir (str): The base output directory
        """
        relative_path = path.relpath(original_filepath, base_input_dir)
        output_filepath = path.join(base_output_dir, relative_path)
        output_dir = path.dirname(output_filepath)
        
        if not path.exists(output_dir):
            makedirs(output_dir)
        
        with open(output_filepath, "w", encoding="utf-8") as file:
            file.write(output)
    
    @staticmethod
    def insert_context_above_function(code: str, function_name: str, context: str) -> str:
        """
        Inserts the context directly above the specified function in the code without a line gap.

        Args:
            code (str): The JavaScript code.
            function_name (str): The name of the function to insert the context above.
            context (str): The context to insert.

        Returns:
            str: The updated code with the context inserted.
        """
        # Split the code into lines
        lines = code.split("\n")
        updated_lines = []
        function_pattern = re.compile(rf"function\s+{re.escape(function_name)}\s*\(")
        context_inserted = False  # Track if the context has been inserted

        for line in lines:
            # Check if the line contains the function definition
            if not context_inserted and function_pattern.search(line):
                # Insert the context directly above the function without a line gap
                updated_lines.append(context)
                context_inserted = True  # Mark context as inserted
            updated_lines.append(line)

        return "\n".join(updated_lines)
    
class CommentRemover:
    def __init__(self):
        self._JS_LANGUAGE = Language(tsjavascript.language())
        self._parser = Parser(self._JS_LANGUAGE)

    def remove_comments_from_js(self, js_code):
        """
        Removes comments from the given JavaScript code using Tree-sitter.
        """
        tree = self._parser.parse(bytes(js_code, "utf8"))
        root_node = tree.root_node
        def traverse_and_collect(node):
            """
            Recursively traverse the syntax tree and collect non-comment code.
            """
            if node.type in ["comment", "ERROR"]:
                return ""
            if len(node.children) == 0:
                return js_code[node.start_byte:node.end_byte]
            return "".join(traverse_and_collect(child) for child in node.children)

        return traverse_and_collect(root_node)