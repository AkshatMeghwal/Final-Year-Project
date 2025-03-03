import logging.config
import api_calls
import constants
from logger import logging
import os
import sys
from utils import Misc
from datacontainer import file_processing_info

if __name__ == "__main__":
    if len(sys.argv) != 2:
        logging.error("Usage: python docstring.py <folder_directory>")
        sys.exit(1)

    folder_directory = sys.argv[1]

    js_files_paths = Misc.get_js_files(folder_directory)
    if len(js_files_paths) == 0:
        logging.error("No JavaScript files found in the directory")
        sys.exit(1)
    files: list[file_processing_info] = []
    for js_file in js_files_paths:
        files.append(file_processing_info(js_file))

    logging.info("Files read successfully.")
    prompt_start = constants.AIPrompts.GAI_DOCSTRING_PROMPT
    prompt_model = constants.AIPrompts.GAI_DOCSTRING_MODEL_PROMPT
    gemini_ai=api_calls.gemini_ai()
    for fileprocessinginfo in files:
        output_code_raw = gemini_ai.get_outputcoderaw_geminiai(prompt_start,fileprocessinginfo.codefile_content,prompt_model)
        fileprocessinginfo.output_code_raw = output_code_raw
        with open(fileprocessinginfo.write_filepath, "w") as f:
            f.write(Misc.output_cleaner(output_code_raw))

    # Remove the first and last line of the output
    # output_lines = output.split("\n")

    # if len(output_lines) > 2:
    #     output = "\n".join(output_lines[1:-1])
    # logging.debug("Processed output by removing first and last lines")

    # with open(write_filepath, "w") as f:
    #     f.write(output)
    logging.info("Output written to file successfully")
