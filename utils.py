from os import path, walk
from typing import Union, List, Optional
import time
from argparse import ArgumentParser
from sys import maxsize
from dotenv import dotenv_values
from tree_sitter import Language, Parser, Node
import re
import json
from logger import logging


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