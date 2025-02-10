import enum
import constants
from google import genai

client = genai.Client(api_key=constants.environment_vars.gemini_api_key)

class Instrument(enum.Enum):
  PERCUSSION = "Percussion"
  STRING = "String"
  WOODWIND = "Woodwind"
  BRASS = "Brass"
  KEYBOARD = "Keyboard"

# client = genai.Client(api_key="GEMINI_API_KEY")
response = client.models.generate_content(
    model='gemini-2.0-flash',
    contents='What type of instrument is an oboe?',
    config={
        'response_mime_type': 'text/x.enum',
        'response_schema': Instrument,
    },
)
print(response.text)

# # import constants
# import os
# from openai import OpenAI

# client = OpenAI(
#     api_key=os.environ.get("OPENAI_API_KEY"),  # This is the default and can be omitted
# )

# chat_completion = client.chat.completions.create(
#     messages=[
#         {
#             "role": "user",
#             "content": "Say this is a test",
#         }
#     ],
#     model="gpt-4o",
# )
# # try:
    
# # except ImportError:
# #     print("something wrong")