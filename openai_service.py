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


# Handle translating from Vietnamese to English
def translate_viet2en (viet_text):
    try:
        #Make your OpenAI API request here
        completion = client.completions.create(
            model='gpt-3.5-turbo-instruct',
            prompt = "Translate this passage or sentence < " + viet_text + " > to english",
        )
        
        translateEN = completion.choices[0].text
        print(translateEN)
        print(dict(completion).get('usage'))
        print(completion.model_dump_json(indent=2))

        return translateEN
    

    except openai.BadRequestError as e:
        print (f"API call failed: {e}")

def prompt_image(texPrompt):
    try:
        # For Dall-e-3 actual generation ($.04)
        # response = client.images.generate(
        #     model="dall-e-3",
        #     prompt=texPrompt,
        #     size="1024x1024",
        #     quality="standard",
        #     n=1,
        # )

        # For Dall-e-2 sample and texting ($.016$)
        response = client.images.generate(
            model="dall-e-2",
            prompt=texPrompt,
            size="512x512",
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






