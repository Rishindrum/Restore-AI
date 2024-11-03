import google.generativeai as genai

import os
from dotenv import load_dotenv, dotenv_values 
load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')

from tqdm.notebook import tqdm

def trim_quotes(s):
    s_stripped = s.strip()
    if s_stripped and s_stripped[0] == '"':
        s_stripped = s_stripped[1:]
    if s_stripped and s_stripped[-1] == '"':
        s_stripped = s_stripped[:-1]
    
    start_spaces = len(s) - len(s.lstrip())
    end_spaces = len(s) - len(s.rstrip())
    return ' ' * start_spaces + s_stripped + ' ' * end_spaces


feature_3_user_response = "User: My plot has a stream running by the fence.\n\n"
print(feature_3_user_response)

feature_3_database_store = f"You are already serving as a proxy between me and a farmer. You just asked a question to them about what bodies of water are nearby their plot of land, if any. The following was their response: {feature_3_user_response}. Given this response, I need you to parse the farmer's response and provide to me a single string that indicates which types of bodies of water are near their land, such that this string will end up in a database. If their answer didn't clearly state one of the 4 options, please return an empty string."
        
feature_4_prompt = f"You are already serving as a proxy between me and a farmer." \
        "Firstly, thank the user for answering the previous question they gave. The fourth question you should ask is: What does your seed mix consist of: wildflower or native grass, or both? Make sure to mention that the farmer should pick between the options of wildflower, native grass, or both. Write this question as a string on a single line(i.e. don't use bullet points or unnecessary paragraph breaks) in a readable way, prompting the farmer for their response."




response = model.generate_content(feature_3_database_store)
text_response = response.text.strip() if hasattr(response, 'text') else response['text'].strip()

# print(text_response)
print(f"RTW_Bot to Database: {trim_quotes(text_response)}\n")

response = model.generate_content(feature_4_prompt)
text_response = response.text.strip() if hasattr(response, 'text') else response['text'].strip()

# print(text_response)
print(f"RTW_Bot: {trim_quotes(text_response)}")