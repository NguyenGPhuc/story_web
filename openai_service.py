import os
import json
import openai
import logging
from openai import OpenAI

from config import openai_key

# import api key and set in environment
os.environ['OPENAI_API_KEY'] = openai_key

client = OpenAI()

# viet_text = "Một cậu bé đi qua một cái cầu tre gỗ."


# Handle rewriting a passage into a different theme
def re_theme (rawText, author, category):
    # When text, author and category are used
    if rawText != None & author != None & category != None:
        try:
            #Make your OpenAI API request here
            completion = client.completions.create(
                model='gpt-3.5-turbo-instruct',
                prompt = "Rewite this passage [" + rawText + "]; mimicking the writing of [" + author + "] adapting this theme [" + category + "]"
            )
            
            diffTheme = completion.choices[0].text

            # Print out extra info
            print_info(diffTheme, completion)

            return diffTheme
        except openai.BadRequestError as e:
            print (f"API call failed: {e}")

    # When user text and author is used
    elif rawText != None & author != None & category == None:
            completion = client.completions.create(
                model='gpt-3.5-turbo-instruct',
                prompt = "Rewite this passage [" + rawText + "]; mimicking the writing style of [" + author + "]"
            )
            
            diffTheme = completion.choices[0].text

            # Print out extra info
            print_info(diffTheme, completion)

            return diffTheme

    # When user text and category is used
    elif rawText != None & author == None & category != None:
            completion = client.completions.create(
                model='gpt-3.5-turbo-instruct',
                prompt = "Rewite this passage [" + rawText + "]; in the theme of [" + category + "]"
            )
            
            diffTheme = completion.choices[0].text

            # Print out extra info
            print_info(diffTheme, completion)

            return diffTheme

    # When user text is use (Fix grammar)
    elif rawText != None & author == None & category == None:
        completion = client.completions.create(
            model='gpt-3.5-turbo-instruct',
            prompt = "Fix any grammar issues found in this [" + rawText + "]"
        )
        
        diffTheme = completion.choices[0].text

        # Print out extra info
        print_info(diffTheme, completion)

        return diffTheme

    # Random story generation when no parameter is passed
    elif rawText == None & author == None & category == None:
        completion = client.completions.create(
            model='gpt-3.5-turbo-instruct',
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
        return None


def print_info(text, api_reponse):
    print(text)
    print(dict(api_reponse).get('usage'))
    print(api_reponse.model_dump_json(indent=2))

    
# prompt_image(translate_viet2en(viet_text))