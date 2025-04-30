import enum
import logging.config
from constants import AIConsts, AIPrompts ,GeminiAIReqKeys,GeminiAIAPIRoles
from logger import logging
# from google import genai
import google.api_core
import google.generativeai as genai
from google.generativeai.types import generation_types, HarmCategory, HarmBlockThreshold

# client = genai.Client(api_key=constants.environment_vars.gemini_api_key)


class Instrument(enum.Enum):
    PERCUSSION = "Percussion"
    STRING = "String"
    WOODWIND = "Woodwind"
    BRASS = "Brass"
    KEYBOARD = "Keyboard"


# client = genai.Client(api_key="GEMINI_API_KEY")
# *******************************************************************************
# This call is crashing loggging module.
# *******************************************************************************
# response = client.models.generate_content(
#     model='gemini-2.0-flash',
#     contents='What type of instrument is an oboe?',
#     config={
#         'response_mime_type': 'text/x.enum',
#         'response_schema': Instrument,
#     },
# )
# print(response.text)

# def gemini_call(code:str,prompt:str)->str:
#     response = client.models.generate_content(
#         model='gemini-2.0-flash',
#         contents=prompt+code,
#     )
#     return response.text

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


class gemini_ai:
    def __init__(self):
        self.aimodel = self._setup_geminiai()
        modelresp: generation_types.GenerateContentResponse = None

    def _setup_geminiai(
        self,
    ) -> genai.GenerativeModel:
        """Initial gemini ai setup"""
        generation_config = {
            AIConsts.GAI_TEMPERATURE_KEY: AIConsts.GAI_TEMPERATURE,
            AIConsts.GAI_MAXOUTPUTTOKENS_KEY: AIConsts.GAI_MAXTOKENS,
        }
        safety_settings = {
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
        }

        aimodel = genai.GenerativeModel(
            model_name=AIConsts.GAI_APIMODEL_NAME,
            generation_config=generation_config,
            safety_settings=safety_settings,
        )
        return aimodel

    def get_outputcoderaw_geminiai(self, prompt_start: str, code: str = "", prompt_model: str = "") -> str:
        """Generate doctrings through gemini and update the output

        Args:
            fileprocessinginfo ( DocstringFileProcessingInfo): Info of file to be proccessed
        """
        # chunk_sizes: List[int] = []
        modelresp: generation_types.GenerateContentResponse = None

        output_code_raw: str = ""
        try:
            # Send initial prompt
            chat_session = self._start_chatwith_gemini(prompt_start, self.aimodel, prompt_model)

            # Send the code content
            modelresp = chat_session.send_message(code)
            output_code_raw += modelresp.text
        except google.api_core.exceptions.ResourceExhausted as e:
            logging.error("Rate limit exceeded: %s", e)
            raise RuntimeError("Rate limit exceeded. Please try again later.") from e
        except Exception as e:
            logging.error("An error occurred while generating output: %s", e)
            raise RuntimeError("Failed to generate output.") from e

        return output_code_raw

    def _start_chatwith_gemini(
        self,
        promptstart: str,
        aimodel: genai.GenerativeModel,
        modelprompt: str = AIPrompts.GAI_DOCSTRING_MODEL_PROMPT,
    ) -> genai.ChatSession:
        """Create the connection with AI and send initial prompts

        Args:
            aimodel ( genai.GenerativeModel ): A wrapper object containing gemini settings
            fileprocessinginfo ( DocstringFileProcessingInfo ): Info of file to be proccessed
            modelprompt ( str ): GenAI model prompt
        """
        return aimodel.start_chat(
            history=[
                {
                    GeminiAIReqKeys.ROLE: GeminiAIAPIRoles.USER,
                    GeminiAIReqKeys.PARTS: promptstart,
                },
                {
                    GeminiAIReqKeys.ROLE: GeminiAIAPIRoles.MODEL,
                    GeminiAIReqKeys.PARTS: modelprompt,
                },
            ]
        )
