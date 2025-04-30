import os
from dotenv import load_dotenv, dotenv_values 
from utils import Misc
load_dotenv()
class environment_vars():
    gemini_api_key=os.getenv("GEMINI_API_KEY")
    openai_api_key=os.getenv("OPENAI_API_KEY")


class AIConsts():
    """AI related constants"""
    API_RETRY_MAXTRY = 3
    API_RETRY_SECONDS = 15
    API_RETRY_BACKOFF = 2

    GAI_APIMODEL_NAME = "gemini-2.0-flash"
    GAI_TEMPERATURE_KEY = "temperature"
    GAI_MAXOUTPUTTOKENS_KEY = "max_output_tokens"

    GAI_APIKEY_LENGTH_MIN = 36
    GAI_APIKEY_LENGTH_MAX = 56
    GAI_TEMPERATURE = 0
    GAI_CANDIDATECOUNT = 1
    GAI_MAXTOKENS = 8192

class PromptPaths():
    """Prompt related paths"""
    GAI_DOCSTRING_PROMPT = "prompts/gemini_js_docstring_prompt.txt"
    GAI_FUNCTION_DOCSTRING_PROMPT = "prompts/gemini_js_single_function_prompt.txt"
    GAI_MULTI_FUNCTION_DOCSTRING_PROMPT = "prompts/gemini_js_multi_function_prompt.txt"

class AIPrompts():
    """Ai related Prompts"""
    GAI_DOCSTRING_PROMPT =Misc.get_content(PromptPaths.GAI_DOCSTRING_PROMPT)
    GAI_FUNCTION_DOCSTRING_PROMPT= Misc.get_content(PromptPaths.GAI_FUNCTION_DOCSTRING_PROMPT)
    GAI_MULTI_FUNCTION_DOCSTRING_PROMPT= Misc.get_content(PromptPaths.GAI_MULTI_FUNCTION_DOCSTRING_PROMPT)

    GAI_DOCSTRING_MODEL_PROMPT = (
        "Understood, I will create function level docstrings for the code"
        " without making any changes to the code logic."
    )
    GAI_FUNCTION_DOCSTRING_MODEL_PROMPT = (
        "Understood, I will create function level docstring for the given"
        "code using the provided contexts."
    )
    # GAI_COMMENT_MODEL_PROMPT = (
    #     "Yes, I understand the prompt and the guidelines for adding informative comments to code files."
    #     " I am ready to analyze provided code and add comments that adhere to the specified criteria."
    #     " Please provide the code file you want me to work on. Remember, I cannot modify the code itself, only add comments."
    # )


class GeminiAIReqKeys():
    """Geminiai Request Keys"""

    ROLE = "role"
    PARTS = "parts"


class GeminiAIAPIRoles():
    """Geminiai API Roles"""

    USER = "user"
    MODEL = "model"
    ASSISTANT = "assistant"
