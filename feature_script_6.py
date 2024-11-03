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


feature_5_user_response = "User: I'm pretty sure that the last prescribed burn happened 10 years ago.\n\n"
print(feature_5_user_response)

feature_5_database_store = f"You are already serving as a proxy between me and a farmer. You just asked a question to them about how many years ago was the last prescribed burn on their plot. The following was their response: {feature_5_user_response}. Given this response, I need you to parse the farmer's response and provide to me a single integer that indicates how long ago the most recent prescribed burn, such that this integer will end up in a database. If they said that they weren't sure how long ago the last prescribed burn was, please return the integer 20."


response = model.generate_content(feature_5_database_store)
text_response = response.text.strip() if hasattr(response, 'text') else response['text'].strip()

# print(text_response)
print(f"RTW_Bot to Database: {trim_quotes(text_response)}")

# response = model.generate_content(feature_5_prompt)
# text_response = response.text.strip() if hasattr(response, 'text') else response['text'].strip()

# # print(text_response)
# print(trim_quotes(text_response))