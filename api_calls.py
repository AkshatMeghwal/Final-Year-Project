# from google import genai
# import enum

# class Instrument(enum.Enum):
#   PERCUSSION = "Percussion"
#   STRING = "String"
#   WOODWIND = "Woodwind"
#   BRASS = "Brass"
#   KEYBOARD = "Keyboard"

# client = genai.Client(api_key="GEMINI_API_KEY")
# response = client.models.generate_content(
#     model='gemini-2.0-flash',
#     contents='What type of instrument is an oboe?',
#     config={
#         'response_mime_type': 'text/x.enum',
#         'response_schema': Instrument,
#     },
# )

# print(response.text)
# # Woodwind



# from google import genai

# import enum
# from pydantic import BaseModel

# class Grade(enum.Enum):
#     A_PLUS = "a+"
#     A = "a"
#     B = "b"
#     C = "c"
#     D = "d"
#     F = "f"

# class Recipe(BaseModel):
#   recipe_name: str
#   rating: Grade

# client = genai.Client(api_key="GEMINI_API_KEY")
# response = client.models.generate_content(
#     model='gemini-2.0-flash',
#     contents='List 10 home-baked cookies and give them grades based on tastiness.',
#     config={
#         'response_mime_type': 'application/json',
#         'response_schema': list[Recipe],
#     },
# )

# print(response.text)
# # [{"rating": "a+", "recipe_name": "Classic Chocolate Chip Cookies"}, ...]



import openai
import constants

openai.api_key = constants.openai_api_key
response = openai.Completion.create(
  engine="text-davinci-003",
  prompt="Tell me a joke",
  max_tokens=50
)

print(response.choices[0].text.strip())