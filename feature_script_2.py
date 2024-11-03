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


feature_1_user_response = "User: My plot has a ton of Johnson Grass and Privet, but I've been working to get rid of it.\n\n"
print(feature_1_user_response)

feature_1_database_store = f"You are already serving as a proxy between me and a farmer. You just asked a question to them about what types of invasive species are present on their land, and they had to pick between Johnson Grass, King Ranch, Privet. The following was their response: {feature_1_user_response}. Given this response, I need you to parse the farmer's response and provide to me a single string that indicates which invasive species is present on their land, such that this string will end up in a database. If their answer didn't clearly state one of the 3 options, please return an empty string."
        
feature_2_prompt = f"You are already serving as a proxy between me and a farmer." \
        "Firstly, thank the user for answering the previous question they gave. The second question you should ask is: approximately what percentage of your plot contains woody species. Make sure to mention that the farmer should provide a number between 0 and 100, representing this percentage. Write this question as a string on a single line(i.e. don't use bullet points or unnecessary paragraph breaks) in a readable way, prompting the farmer for their response."


response = model.generate_content(feature_1_database_store)
text_response = response.text.strip() if hasattr(response, 'text') else response['text'].strip()
text_response = trim_quotes(text_response)

database_response = ""

if(text_response == "Johnson Grass"):
    database_response = "JG"
elif(text_response == "King Ranch"):
    database_response = "KR"
elif(text_response == "Privet"):
    database_response = "P"
else:
    database_response = ""

# print(text_response)
print(f"RTW_Bot to Database: {database_response}\n")

response = model.generate_content(feature_2_prompt)
text_response = response.text.strip() if hasattr(response, 'text') else response['text'].strip()

# print(text_response)
print(f"RTW_Bot: {trim_quotes(text_response)}")