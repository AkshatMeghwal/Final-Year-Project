import logging.config
import api_calls
import constants
from logger import logging
logging.debug("Imported all the required modules successfully")
if __name__=="__main__":
    src_filepath="E:\\test.js"
    print("wyf")
    with open(src_filepath,"r") as f:
        code=f.read()
    logging.info("Code read from file successfully")
    prompt=constants.AIPrompts.GAI_DOCSTRING_PROMPT
    output=api_calls.gemini_call(code,prompt)
    
    # Remove the first and last line of the output
    output_lines =    output.split('\n')

    if len(output_lines) > 2:
        output = '\n'.join(output_lines[1:-1])
    logging.debug("Processed output by removing first and last lines")
    write_filepath="E:\\test_output.js"
    with open(write_filepath,"w") as f:
        f.write(output)
    logging.info("Output written to file successfully")