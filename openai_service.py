import os
import json
import openai
import logging
from openai import OpenAI
from config import openai_key
import random

import sys
print('Virual environment path: ', sys.executable)

import nltk
nltk.download('punkt')


# import api key and set in environment
os.environ['OPENAI_API_KEY'] = openai_key

client = OpenAI()

# viet_text = "Một cậu bé đi qua một cái cầu tre gỗ."


def truncate_to_complete_sentence(text, max_tokens):
    sentences = nltk.sent_tokenize(text)
    truncated_text = ""
    current_tokens = 0

    for sentence in sentences:
        sentence_tokens = len(nltk.word_tokenize(sentence))
        if current_tokens + sentence_tokens <= max_tokens:
            truncated_text += sentence + " "
            current_tokens += sentence_tokens
        else:
            break

    return truncated_text.strip()


# Handle rewriting a passage into a different theme
def re_theme (rawText, author, category):

    if rawText != '':
        averageMaxToken = round(len(rawText) * 1.2)
        max_tokens = 1024
    else:
        averageMaxToken = random.randint(150,300)
        max_tokens = 1024
    
    print (averageMaxToken)

    print('In re_theme')
    print("User text: " + rawText)
    # When text, author and category are used
    if rawText != '' and author != 'None' and category != 'None':
        try:
            #Make your OpenAI API request here
            completion = client.completions.create(
                model='gpt-3.5-turbo-instruct',
                max_tokens = averageMaxToken,
                prompt = "Rewite [" + rawText +  "], mimicking the writing of [" + author + "] in a theme of [" + category + "] ",
                stop = '',
                temperature=0.2
            )

            # while len(nltk.word_tokenize(reponse)) < averageMaxToken:
            #     completion = cllient.completion.create(
            #         model='gpt-3.5-turbo-instruct',
            #         max_tokens = max_tokens,
            #          prompt = "Rewite [" + rawText +  "], mimicking the writing of [" + author + "] in a theme of [" + category + "] ",
            #         stop = ''
            #     )

            #     response += completion.choices[0].text
            #     stop = reponse

            # diffTheme = truncate_to_complete_sentence(response, averageMaxToken)
            # print(diffTheme)

            diffTheme = completion.choices[0].text

            # Print out extra info
            print_info(diffTheme, completion)

            return diffTheme
        except openai.BadRequestError as e:
            print (f"API call failed: {e}")

    # When category NOT used
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

    # When author is NOT used
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

    # When user input is NOT used
    elif rawText == '' and author != 'None' and category != 'None':
        completion = client.completions.create(
            model='gpt-3.5-turbo-instruct',
            max_tokens = averageMaxToken,
            prompt = "Creates a short pargraph story mimicking writting style of [" + author + "] in the theme of [" + category + "]" 
        )

        diffTheme = completion.choices[0].text
        print_info(diffTheme, completion)

        return diffTheme

    # Random story generation when no parameter is passed
    elif rawText == '' and author == 'None' and category == 'None':
        completion = client.completions.create(
            model='gpt-3.5-turbo-instruct',
            max_tokens = averageMaxToken,
            prompt = "Creates a one pargraph story"
        )
        
        diffTheme = completion.choices[0].text
        # Print out extra info
        print_info(diffTheme, completion)

        return diffTheme


# When author and category is NOT used (Fix grammar)
def grammar_fix(rawText, author, category):

    averageMaxToken = len(rawText) * 1.2

    try: 
        if rawText != '' and author == 'None' and category == 'None':
            completion = client.completions.create(
                model='gpt-3.5-turbo-instruct',
                max_tokens = averageMaxToken,
                prompt = "Fix any grammar issues found in this [" + rawText + "]"
            )
            
            diffTheme = completion.choices[0].text

            # Print out extra info
            print_info(diffTheme, completion)

            return diffTheme
        else:
            return rawText
    except openai.BadRequestError as e:
            print (f"Bad openai request: {e}")


def translate_text(rawText, langFrom, langTo):

    print("In translate")
    print('Raw text: ', rawText)


    averageMaxToken = round(len(rawText) * 1.2)

    if langFrom == "None" or langTo == "None":
        return "Need to select language"

    try: 
        if rawText != '' and langFrom != 'None' and langTo != 'None':
            completion = client.completions.create(
                model='gpt-3.5-turbo-instruct',
                max_tokens = averageMaxToken,
                prompt = "Translate this " + langFrom + "[" + rawText + "] to " +  langTo
            )
            
            diffTheme = completion.choices[0].text

            # Print out extra info
            print_info(diffTheme, completion)

            return diffTheme
        else:
            return rawText
    except openai.BadRequestError as e:
            print (f"Bad openai request: {e}")
    

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