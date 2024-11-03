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


feature_4_user_response = "User: I'm planting bot wildflower and native grass seeds on my land.\n\n"
print(feature_4_user_response)

feature_4_database_store = f"You are already serving as a proxy between me and a farmer. You just asked a question to them about what does their seed mix consist of: wildflower or native grass, or both. The following was their response: {feature_4_user_response}. Given this response, I need you to parse the farmer's response and provide to me a single string that indicates which type of seed mix they used, choosing between wildflower, native grass, or both, such that this string will end up in a database. If their answer didn't clearly state one of the 3 options, please return an empty string."
        
feature_5_prompt = f"You are already serving as a proxy between me and a farmer." \
        "Firstly, thank the user for answering the previous question they gave. The fifth question you should ask is: how many years ago was the last prescribed burn on your plot? Make sure to mention to the user that if they're not sure, then indicate that they weren't sure.  Make sure to mention that the farmer should write a whole number indicating the number of years since the last prescribed burn, or indicate that they weren't sure when the last one was. Write this question as a string on a single line(i.e. don't use bullet points or unnecessary paragraph breaks) in a readable way, prompting the farmer for their response."




response = model.generate_content(feature_4_database_store)
text_response = (response.text.strip() if hasattr(response, 'text') else response['text'].strip()).lower()

# if (text_response == "both") #TODO

# print(text_response)
print(f"RTW_Bot to Database: {trim_quotes(text_response)}\n")

response = model.generate_content(feature_5_prompt)
text_response = response.text.strip() if hasattr(response, 'text') else response['text'].strip()

# print(text_response)
print(f"RTW_Bot: {trim_quotes(text_response)}")