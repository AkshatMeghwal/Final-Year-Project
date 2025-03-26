from utils  import Misc
from os import path

class file_processing_info():
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.codefile_content = Misc.get_content(filepath)
        self.js_files = []
        self.src_filepath = ""
        self.write_filepath = Misc.generate_write_filepath(filepath)
        self.output_code_raw = ""

    