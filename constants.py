import os
from dotenv import load_dotenv, dotenv_values 
load_dotenv()
gemini_api_key=os.getenv("GEMINI_API_KEY")
openai_api_key=os.getenv("OPENAI_API_KEY")
# def fetch_api_keys():
#     gemini_api_key=os.getenv("GEMINI_API_KEY")
#     openai_api_key=os.getenv("OPENAI_API_KEY")

# if __name__== "__main__":
#     fetch_api_keys()
