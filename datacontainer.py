from utils  import Misc
from os import path

class file_processing_info():
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.raw_code = Misc.get_content(filepath)
        self.raw_code_no_comment=""
        self.js_files = []
        self.src_filepath = ""
        self.write_filepath = Misc.generate_write_filepath(filepath)
        self.output_code_raw = ""
        self.output_code_raw_no_comment=""

    