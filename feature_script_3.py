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


feature_2_user_response = "User: My plot is 15% wooded.\n\n"
print(feature_2_user_response)

feature_2_database_store = f"You are already serving as a proxy between me and a farmer. You just asked a question to them about approximately what percentage of their plot contains woody species, and they responded with a percentage between 0 and 100. The following was their response: {feature_2_user_response}. Given this response, I need you to parse the farmer's response and provide to me a single floating point number that indicates the percentage the farmer indicated, such that this floating point will end up in a database. If their answer didn't clearly give a response, please return an empty output."
        
feature_3_prompt = f"You are already serving as a proxy between me and a farmer." \
        "Firstly, thank the user for answering the previous question they gave. The third question you should ask is: What bodies of water are nearby your plot of land, if any? Make sure to mention that the farmer should pick between river, spring, lake, and none. Write this question as a string on a single line(i.e. don't use bullet points or unnecessary paragraph breaks) in a readable way, prompting the farmer for their response."



response = model.generate_content(feature_2_database_store)
text_response = response.text.strip() if hasattr(response, 'text') else response['text'].strip()

# print(text_response)
print(f"RTW_Bot to Database: {trim_quotes(text_response)}\n")

response = model.generate_content(feature_3_prompt)
text_response = response.text.strip() if hasattr(response, 'text') else response['text'].strip()

# print(text_response)
print(f"RTW_Bot: {trim_quotes(text_response)}")