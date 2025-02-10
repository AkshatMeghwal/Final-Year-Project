import os
from dotenv import load_dotenv, dotenv_values 
load_dotenv()
class environment_vars():
    gemini_api_key=os.getenv("GEMINI_API_KEY")
    openai_api_key=os.getenv("OPENAI_API_KEY")

class AIPrompts():
    """Ai related Prompts"""
    GAI_DOCSTRING_PROMPT =("You have to add Docstring to the javascript code."
                           "**Strict Instructions**"
                           "1. The docstring should be added to the function level."
                           "2. The docstring should be added at the beginning of the function."
                           "3. Output should be an valid js code with same fuctionality and better readability."
                           "Java script code is given below:\n"
                           )
    # GAI_DOCSTRING_MODEL_PROMPT = (
    #     "Understood, I will create function level docstrings for the code"
    #     " without making any changes to the code logic."
    # )
    # GAI_COMMENT_MODEL_PROMPT = (
    #     "Yes, I understand the prompt and the guidelines for adding informative comments to code files."
    #     " I am ready to analyze provided code and add comments that adhere to the specified criteria."
    #     " Please provide the code file you want me to work on. Remember, I cannot modify the code itself, only add comments."
    # )

    # DOCSTRING_SMALLFILE_ASSISTANT_PROMPT = (
    #     "Understood, I will provide output in same format as input which have added comments to its code"
    #     " without changing any other part except code."
    #     "In code, I will add comments whereever needed without changing code logic."
    # )

    # COMMENT_SMALLFILE_ASSISTANT_PROMPT = (
    #     "Acknowledged. I will maintain the original format of the input and augment the code with comments, "
    #     "ensuring that the logic remains unchanged. "
    #     "Comments will be added as necessary to enhance clarity and understanding without altering the code's functionality."
    # )

    # OAI_DOCSTRING_ASSISTANT_PROMPT = (
    #     "Understood, I will create function level docstrings for the code and"
    #     " provide the modified code without making any modifications to the code logic."
    # )
    # OAI_COMMENT_ASSISTANT_PROMPT = (
    #     "Yes, I understand the task."
    #     " I will be inserting 'Code section comments' for entire code without modifying the code other than embedding comments,"
    #     " following the strict instructions provided. Let's proceed with the task."
    # )
