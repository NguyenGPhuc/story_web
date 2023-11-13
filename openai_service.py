import os
import json
import openai
from openai import OpenAI

from config import api_key

# import api key and set in environment
os.environ['OPENAI_API_KEY'] = api_key

client = OpenAI()

# viet_text = "Một cậu bé đi qua một cái cầu tre gỗ."


# Handle translating from Vietnamese to English
def translate_viet2en (viet_text):
    # Attempt to use key form text file
    try:
        #Make your OpenAI API request here
        completion = client.completions.create(
            model='gpt-3.5-turbo-instruct',
            prompt = "Translate this Vietnamese passage or sentence < " + viet_text + " > to english",
        )
        print(completion.choices[0].text)
        # print(dict(completion).get('usage'))
        # print(completion.model_dump_json(indent=2))
    

    except openai.BadRequestError as e:
        print (f"API call failed: {e}")






