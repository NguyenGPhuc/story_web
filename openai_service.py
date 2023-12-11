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

# Complete the response. Truncate any unfinish sentence.
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

    originalLen = round(len(rawText))

    if rawText != '':
        averageMaxToken = round(len(rawText) * 1.2)

    else:
        originalLen = random.randint(100,200)
        averageMaxToken = round(originalLen *1.2)
        

    response = ''
    stop = ''
    
    print ('orignial max: ', originalLen)
    print ('average max: ', averageMaxToken)

    print('In re_theme')
    print("User text: " + rawText)
    # When text, author and category are used
    if rawText != '' and author != 'None' and category != 'None':
        try:
            while len(nltk.word_tokenize(response)) < originalLen:
                completion = client.completions.create(
                    model='gpt-3.5-turbo-instruct',
                    max_tokens = averageMaxToken,
                    prompt = "Rewite " + rawText +  " in the writing of " + author + " using " + category + " as them theme ",
                    stop = stop
                )

                response += completion.choices[0].text
                stop = response

            diffTheme = truncate_to_complete_sentence(response, originalLen)
            print(diffTheme)

            # diffTheme = completion.choices[0].text

            # Print out extra info
            print_info(diffTheme, completion)

            return diffTheme
        except openai.BadRequestError as e:
            print (f"API call failed: {e}")

    # When category NOT used
    elif rawText != '' and author != 'None' and category == 'None':
        print ('Text, author, NO category')
        try:
            while len(nltk.word_tokenize(response)) < originalLen:
                completion = client.completions.create(
                    model='gpt-3.5-turbo-instruct',
                    max_tokens = averageMaxToken,
                    prompt = "Rewite " + rawText + " in the writing style of " + author,
                    stop = stop
                )

                response += completion.choices[0].text
                stop = response

            diffTheme = truncate_to_complete_sentence(response, originalLen)
            # Print out extra info
            print_info(diffTheme, completion)

            return diffTheme
        except openai.BadRequestError as e:
            print (f"API call failed: {e}")

    # When author is NOT used
    elif rawText != '' and author == 'None' and category != 'None':
        try:
            while len(nltk.word_tokenize(response)) < originalLen:
                completion = client.completions.create(
                    model='gpt-3.5-turbo-instruct',
                    max_tokens = averageMaxToken,
                    prompt = "Rewite " + rawText + " in a " + category + " theme",
                    stop = stop
                )

                response += completion.choices[0].text
                stop = response

            diffTheme = truncate_to_complete_sentence(response, originalLen)

            # Print out extra info
            print_info(diffTheme, completion)

            return diffTheme

        except openai.BadRequestError as e:
            print (f"API call failed: {e}")

    # When user input is NOT used
    elif rawText == '' and author != 'None' and category != 'None':
        try:
            while len(nltk.word_tokenize(response)) < originalLen:
                completion = client.completions.create(
                    model='gpt-3.5-turbo-instruct',
                    max_tokens = averageMaxToken,
                    prompt = "Creates a short pargraph story in the writting style of " + author + " using a " + category + " theme",
                    stop = stop
                )
                
                response += completion.choices[0].text
                stop = response

            diffTheme = truncate_to_complete_sentence(response, originalLen)

            # Print out extra info
            print_info(diffTheme, completion)

            return diffTheme

        except openai.BadRequestError as e:
            print (f"API call failed: {e}")

    else:
        # Random story generation when no parameter is passed
        print("In random generate")
        try:
            while len(nltk.word_tokenize(response)) < originalLen:
                completion = client.completions.create(
                    model='gpt-3.5-turbo-instruct',
                    max_tokens = averageMaxToken,
                    prompt = 'Write a one pargraph story',
                    stop = stop
                )
                
                response += completion.choices[0].text
                stop = response

            diffTheme = truncate_to_complete_sentence(response, originalLen)


            # Print out extra info
            print_info(diffTheme, completion)

            return diffTheme
        except Exception as e:
            print ('Error: ', {e})


# When author and category is NOT used (Fix grammar)
def grammar_fix(rawText, author, category):

    averageMaxToken = len(rawText) * 1.2

    try: 
        if rawText != '':
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
            return 'Nothing to fix'
    except openai.BadRequestError as e:
            print (f"Bad openai request: {e}")


def translate_text(rawText, langFrom, langTo):

    print("In translate")
    print('Raw text: ', rawText)


    averageMaxToken = round(len(rawText) * 1.2)

    # if langFrom == "None" and langTo == "None":
    #     return "Need to select language"

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
    print ('In openAI image function')
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