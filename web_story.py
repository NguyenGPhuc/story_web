from flask import Flask, render_template, request, jsonify
import openai_service
import logging
import os
from datetime import datetime
from PIL import Image
import requests
import json

app = Flask(__name__)

# Start default site
@app.route('/')
def home():

    # read author from file
    with open('author.txt', 'r') as file:
        authors_data = json.load(file)
        # For missing parameters
        authors = authors_data.get('authors', [])

    # read category from file
    with open ('category.txt', 'r') as file:
        categories_data = json.load(file)
        categories = categories_data.get('categories', [])

    # read langauge from file
    with open ('languages.txt', 'r') as file:
        language_data = json.load(file)
        languages = language_data.get('languages', [])


    # print(json.dumps(authors))
    return render_template('index.html', categories=categories, authors=authors, languages=languages)


@app.route('/changeTheme', methods=['POST'])
def change_theme():
    if request.method == "POST":

        # Get user input, author and category from front-end
        inputText = request.form.get('inputText')
        selectAuthor = request.form.get('author')
        selectCategory = request.form.get('category')


        print("User input: ", inputText)
        print("Author: ", selectAuthor)
        print("Category: ", selectCategory)

        try:
            # Get modified text from API
            modText = openai_service.re_theme(inputText, selectAuthor, selectCategory)
            # Remove any extra characters winthin the string

            if inputText != '':
                print('In IF')
                parseText = modText.replace('\n', '')
                return jsonify({'parseText': parseText})
            else:
                print('In ELSE')
                parseText = modText.replace('\n', '')
                return jsonify({'parseText': parseText})

        except Exception as e:
            print('Error:', str(e))
            return jsonify({'error': 'Unable to call from API'})
        
        # Return translated text in json format
        # return jsonify({'parseText': parseText})

    else: 
        print ("User input was not processed correctly")

    return render_template('index.html', inputText='', modText='')

        

@app.route('/translateText', methods=['POST'])
def translate_text():
    if request.method == 'POST':

        data = request.get_json()
        if data:
            unTranslate = data.get('inputText')
            selectFrom = data.get('languageFrom')
            selectTo = data.get('languageTo')

        print('unTranslate:', unTranslate)
        print('selectFrom:', selectFrom)
        print('selectTo:', selectTo)

        try:
            # Get modified text from API
            modText = openai_service.translate_text(unTranslate, selectFrom, selectTo)

            # Remove any extra characters winthin the string
            if modText != None:
                print('In IF')
                translateText = modText.replace('\n', '')
                return jsonify({'translateText': translateText})
            else:
                print('In ELSE')
                return jsonify({'translateText': modText})

        except Exception as e:
            print('Error:', str(e))
            return jsonify({'error': 'Unable to call from API'})



# Generate image using translated text
# @app.route('/generateImage', methods=['POST'])
# def generate_image():
#     if request.method == 'POST':
#         try:

#             # Set model and image size
#             imageSize = request.form.get('imageDimensions')
#             if imageSize == "512x512":
#                 imageModel = 'dall-e-2'
#             else:
#                 imageModel = 'dall-e-3'


#             parseText = request.form.get('modTextArea')

#             # Get image url form API
#             imageUrl = openai_service.prompt_image(imageModel, parseText, imageSize)
            


#             if imageUrl is not None:
#                 save_image(imageUrl)
           

#         except Exception as e:
#             logging.exception('Failed to generate image: %s', str(e))
#             return jsonify({'error': 'Failed to generate image'})

#         return jsonify({'imageUrl':imageUrl})
#     else:
#         print('Unable to generate image')
#         return jsonify({'error': 'Unable to generate image'})


# def save_image(imageUrl):
#     try:
#         output_folder = 'output'
#         os.makedirs(output_folder, exist_ok=True)

#         # Use date and time for naming
#         timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
#         imageFilename = f'{timestamp}.jpeg'
#         imagePath = os.path.join(output_folder, imageFilename)

#         # Download the image from url
#         imageData = requests.get(imageUrl).content
    
#         # Save image
#         with open(imagePath, 'wb') as f:
#             f.write(imageData)

#     except Exception as e:
#         logging.exception('Failed to save image: %s', str(e))
#         return jsonify({'error': 'Failed to save image'})


if __name__ == '__main__':
    app.run(debug = True)