import google.generativeai as genai

import os
from dotenv import load_dotenv, dotenv_values 
load_dotenv()


GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')

from tqdm.notebook import tqdm

def trim_quotes(s):
    # Strip whitespace, then check first/last non-blank characters
    s_stripped = s.strip()
    if s_stripped and s_stripped[0] == '"':
        s_stripped = s_stripped[1:]
    if s_stripped and s_stripped[-1] == '"':
        s_stripped = s_stripped[:-1]
    
    # Preserve original spacing by replacing middle part
    start_spaces = len(s) - len(s.lstrip())
    end_spaces = len(s) - len(s.rstrip())
    return ' ' * start_spaces + s_stripped + ' ' * end_spaces

feature_1_prompt = f"You are going to serve as a proxy between me and a farmer. This farmer will be giving information about a praire-land restoration project they're working on, and they need to provide some information to me about the properties of their land. You will be asking questions to them on my behalf, and will be interpreting and parsing their responses to store in a database." \
        "The first question you should ask is: what type of invasive species are present on the land. Make sure to mention that the farmer is able to select from one of three options: namely, Johnson Grass, King Ranch, Privet. Write this question as a string on a single line(i.e. don't use bullet points or unnecessary paragraph breaks) in a readable way, prompting the farmer for their response."

        
response = model.generate_content(feature_1_prompt)
text_response = response.text.strip() if hasattr(response, 'text') else response['text'].strip()

# print(text_response)
print(trim_quotes(text_response))