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


feature_1_user_response = "My plot has a ton of Johnson Grass and Privet, but I've been working to get rid of it."
# feature_1_user_response_v2 = "Dang, brother, I kinda got a lot of issues with m'land boy. I guess i got a buncha Privet, and luckily i ain't got no King Ranch"

# feature_1_database_store = f"You are already serving as a proxy between me and a farmer. This farmer has been giving information about a praire-land restoration project they're working on, and they need to provide some information to me about the properties of their land. You have already been asking questions to them on my behalf, and will be interpreting and parsing their responses to store in a database." \
#         "Most recently, you just asked a question to them about what types of invasive species are present on their land, and they had to pick between Johnson Grass, King Ranch, Privet. The following was their response: {feature_1_user_response}. Given this response, I need you to parse the farmer's response and provide to me a single string that indicates which invasive species is present on their land, choosing between one of the 3 options, such that this string will end up in a database. If their answer didn't clearly state one of the 3 options, please return an empty string."

feature_1_database_store = f"You are already serving as a proxy between me and a farmer. You just asked a question to them about what types of invasive species are present on their land, and they had to pick between Johnson Grass, King Ranch, Privet. The following was their response: {feature_1_user_response}. Given this response, I need you to parse the farmer's response and provide to me a single string that indicates which invasive species is present on their land, such that this string will end up in a database. If their answer didn't clearly state one of the 3 options, please return an empty string."
        
feature_2_prompt = f"You are already serving as a proxy between me and a farmer." \
        "The second question you should ask is: approximately what percentage of your plot contains woody species. Make sure to mention that the farmer should provide a number between 0 and 100, representing this percentage. Write this question as a string on a single line(i.e. don't use bullet points or unnecessary paragraph breaks) in a readable way, prompting the farmer for their response."


response = model.generate_content(feature_1_database_store)
text_response = response.text.strip() if hasattr(response, 'text') else response['text'].strip()

# print(text_response)
print(trim_quotes(text_response))

response = model.generate_content(feature_2_prompt)
text_response = response.text.strip() if hasattr(response, 'text') else response['text'].strip()

# print(text_response)
print(trim_quotes(text_response))