import os
import json
import openai
import logging
from openai import OpenAI
from config import openai_key
import random

# import api key and set in environment
os.environ['OPENAI_API_KEY'] = openai_key

client = OpenAI()

# viet_text = "Một cậu bé đi qua một cái cầu tre gỗ."


# Handle rewriting a passage into a different theme
def re_theme (rawText, author, category):

    if rawText != '':
        averageMaxToken = len(rawText) * 2
    else:
        averageMaxToken = random.randint(150,300)

    print('In re_theme')
    print("User text: " + rawText)
    # When text, author and category are used
    if rawText != '' and author != 'None' and category != 'None':
        try:
            #Make your OpenAI API request here
            completion = client.completions.create(
                model='gpt-3.5-turbo-instruct',
                max_tokens = averageMaxToken,
                prompt = "Rewite [" + rawText +  "], mimicking the writing of [" + author + "] in a theme of [" + category + "]"
            )
            
            diffTheme = completion.choices[0].text

            # Print out extra info
            print_info(diffTheme, completion)

            return diffTheme
        except openai.BadRequestError as e:
            print (f"API call failed: {e}")

    # When category not used
    elif rawText != '' and author != 'None' and category == 'None':
            completion = client.completions.create(
                model='gpt-3.5-turbo-instruct',
                max_tokens = averageMaxToken,
                prompt = "Rewite [" + rawText + "]; mimicking the writing style of [" + author + "]"
            )
            
            diffTheme = completion.choices[0].text

            # Print out extra info
            print_info(diffTheme, completion)

            return diffTheme

    # When author is not used
    elif rawText != '' and author == 'None' and category != 'None':
            completion = client.completions.create(
                model='gpt-3.5-turbo-instruct',
                max_tokens = averageMaxToken,
                prompt = "Rewite [" + rawText + "]; in the theme of [" + category + "]"
            )
            
            diffTheme = completion.choices[0].text

            # Print out extra info
            print_info(diffTheme, completion)

            return diffTheme

    # When author and category is not used (Fix grammar)
    elif rawText != '' and author == 'None' and category == 'None':
        completion = client.completions.create(
            model='gpt-3.5-turbo-instruct',
            max_tokens = averageMaxToken,
            prompt = "Fix any grammar issues found in this [" + rawText + "]"
        )
        
        diffTheme = completion.choices[0].text

        # Print out extra info
        print_info(diffTheme, completion)

        return diffTheme

    # Random story generation when no parameter is passed
    elif rawText == '' and author == 'None' and category == 'None':
        completion = client.completions.create(
            model='gpt-3.5-turbo-instruct',
            max_tokens = averageMaxToken,
            prompt = "Creates a one pargraph story mimicking writting style of [" + author + "] in the theme of [" + category + "]" 
        )
        
        diffTheme = completion.choices[0].text

        # Print out extra info
        print_info(diffTheme, completion)

        return diffTheme
    

    

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
        return ''


def print_info(text, api_reponse):
    print(text)
    print(dict(api_reponse).get('usage'))
    print(api_reponse.model_dump_json(indent=2))

    
# prompt_image(translate_viet2en(viet_text))