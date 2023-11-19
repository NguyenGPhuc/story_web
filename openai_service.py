import os
import json
import openai
import logging
from openai import OpenAI

from config import api_key

# import api key and set in environment
os.environ['OPENAI_API_KEY'] = api_key

client = OpenAI()

# viet_text = "Một cậu bé đi qua một cái cầu tre gỗ."


# Handle rewriting a passage into a different theme
def re_theme (rawText, author):
    try:
        #Make your OpenAI API request here
        completion = client.completions.create(
            model='gpt-3.5-turbo-instruct',
            prompt = "Rewite this passage [" + rawText + "], mimicking the writing of author [" + author + "]"
        )
        
        diffTheme = completion.choices[0].text
        print(diffTheme)
        print(dict(completion).get('usage'))
        print(completion.model_dump_json(indent=2))

        return diffTheme
    except openai.BadRequestError as e:
        print (f"API call failed: {e}")


# Handle (optional) image genration for the whole page
def prompt_image(selectModel, texPrompt, size):
    try:
        # Calling Dall-e API
        response = client.images.generate(
            model=selectModel,
            prompt=texPrompt,
            size=size,
            quality="standard",
            n=1,
        )

        
        print(dict(response).get('usage'))
        print(response.model_dump_json(indent=2))

        image_url = response.data[0].url

        return image_url
    
    except Exception as e:
        logging.exception('Failed to generate image: %s', str(e))
        return None

    
# prompt_image(translate_viet2en(viet_text))