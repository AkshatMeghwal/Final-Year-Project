# Final-Year-Project
# Comprehensive DocString generation for Js code using GenAI


Initial Setup 
1. Create an .env file in the folder.
2. Format for the .env file will be provided below.
2. Add your api keys of the genAI provider eg. gemini and openai.

env file format

OPENAI_API_KEY="Your api key"
GEMINI_API_KEY="Your api key"


Obtaining Api keys
OpenAI
Steps
1. Goto https://platform.openai.com/api-keys
2. Login with email, generate the key and copy it.
3. Add this into .env file.

Gemini
Steps
1. Goto https://aistudio.google.com/app/apikey
2. Login with email, generate the key and copy it.
3. Add this into .env file.

## Running the Flask App

1. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Run the Flask app:
   ```
   python app.py
   ```

3. Open your browser and navigate to `http://127.0.0.1:5000`.

4. Upload a folder containing JavaScript files. The processed files will be available for download as a zip file.