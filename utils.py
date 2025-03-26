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
    
class CommentRemover:
    def __init(self):
        self._JS_LANGUAGE = Language("build/my-languages.so", "javascript")
        self._parser = Parser()
    def remove_comments_from_js(js_code):
        """
        Removes comments from the given JavaScript code using Tree-sitter.
        """
        parser = Parser(JS_LANGUAGE)
        tree = parser.parse(bytes(js_code, "utf8"))
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
# class CommentRemover:
#     """Class to handle comment removal"""

#     def __init__(self):
#         """Initalize and build languages

#         Args:
#             listoflang (List[str]): list of languages
#         """

#         # to be editted for genralizing
#         Language.build_library(
#             # Store the library in the `build` directory
#             "build/my-languages.so",
#             # Include one or more languages
#             [
#                 "build/tree-sitter-python",
#                 "build/tree-sitter-php/php",
#                 "build/tree-sitter-javascript",
#             ],
#         )
#         self._JS_LANGUAGE = Language("build/my-languages.so", "javascript")
#         self._lang = {
#             fte.PYTHON: self._PY_LANGUAGE,
#             fte.PHP: self._PHP_LANGUAGE,
#             fte.JAVASCRIPT: self._JS_LANGUAGE,
#         }
#         self._commentremover = {
#             fte.PYTHON: self._remove_commentsfrom_python,
#             fte.PHP: self._remove_commentsfrom_php,
#             fte.JAVASCRIPT: self._remove_commentsfrom_javascript,
#         }

#         # Initialize the parser
#         self._parser = Parser()

#     def remove_comment(self, code: str, lang: str) -> str:
#         """Removes comments from the given code based on the specified language.

#         Args:
#             code (str): The code from which comments need to be removed.
#             lang (str): The language of the code. Supported languages are determined
#             by the parser set during initialization.
#         """
#         self._parser.set_language(self._lang[lang])
#         # Parse the code
#         tree = self._parser.parse(bytes(code, "utf8"))
#         lines = code.split("\n")
#         self._commentremover[lang](tree.root_node, lines)
#         code_without_comments = "\n".join(lines)
#         code_without_comments = self._clean_the_code(code_without_comments)
#         return code_without_comments

#     def _clean_the_code(self, text):
#         # Remove any number of tabs
#         text = re.sub("\t+", "", text)
#         # Remove multiple newlines
#         text = re.sub("\n+", "", text)
#         # Remove extra spaces
#         text = re.sub(" +", " ", text)
#         return text

#     def _remove_commentsfrom_javascript(self, node: Node, lines: List[str]):
#         """
#         Removes comments from the given JavaScript code.

#         Args:
#             node (Node): node to be processed.
#             lines (List[str]): code lines.
#         """
#         if node.type == "comment":
#             start_line, start_col = node.start_point
#             end_line, end_col = node.end_point

#             # Handle React.js style comments embedded in brackets
#             if (
#                 start_line == end_line
#                 and lines[start_line][start_col - 1 : start_col + 2] == "{/*"
#             ):
#                 lines[start_line] = (
#                     lines[start_line][: start_col - 1]
#                     + lines[start_line][end_col + 2 :]
#                 )
#             elif start_line != end_line:
#                 if lines[start_line][start_col - 1 : start_col + 2] == "{/*":
#                     lines[start_line] = lines[start_line][: start_col - 1]
#                 if lines[end_line][end_col : end_col + 2] == "*/}":
#                     lines[end_line] = lines[end_line][end_col + 2 :]

#             # Handle rest js style comments embedded in brackets
#             if start_line == end_line:  # Single-line comment
#                 lines[start_line] = (
#                     lines[start_line][:start_col] + lines[start_line][end_col:]
#                 )
#             else:  # Multi-line comment
#                 lines[start_line] = lines[start_line][:start_col]
#                 for line_num in range(start_line + 1, end_line):
#                     lines[line_num] = ""
#                 lines[end_line] = lines[end_line][end_col:]
#         elif node.type == "string":
#             # Strings in JavaScript can contain comments, so no need to remove them
#             pass
#         else:
#             for child in node.children:
#                 self._remove_commentsfrom_javascript(child, lines)
