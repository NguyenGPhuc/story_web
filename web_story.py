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

    # read the options from file
    with open('author.txt', 'r') as file:
        authors_data = json.load(file)
        # For missing parameters
        authors = authors_data.get('authors', [])
    with open ('category.txt', 'r') as file:
        categories_data = json.load(file)
        categories = categories_data.get('categories', [])

    # print(json.dumps(authors))
    return render_template('index.html', categories=categories, authors=authors)


# @app.route('/changeTheme', methods=['POST'])
# def change_theme():
#     if request.method == "POST":

#         # Get user input (Any language text)
#         inputText = request.form.get('inputText')

#         # 
#         try:
#             # Get modified text from API
#             modText = openai_service.re_theme(inputText)
#             # Remove any extra characters winthin the string
#             parseText = modText.replace('"', '')


#         except Exception as e:
#             print('Error:', str(e))
#             return jsonify({'error': 'Unable to call from API'})
        
#         # Return translated text in json format
#         return jsonify({'parseText': parseText})

#     else: 
#         print ("User input was not processed correctly")


#     return render_template('index.html', inputText='', modText='')

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


# # Doesn't display translated text.
# @app.route('/translateText', methods=['POST'])
# def g_translate():
#     if request.method == 'POST':
#         try:
#             # Get user input (Vietnamese text)
#             inputText = request.form.get('inputText')
            
#             # Check if inputText is not None before proceeding
#             if inputText is not None:

#                 print(inputText)

#                 # Gets translation text from API
#                 modText = openai_service.re_theme(inputText)
                
#                 # Remove any extra characters within the translation string
#                 parseText = modText.replace('\n', '').replace('"', '').replace('.', '')


#                 # Get generated image URL from API
#                 imageUrl = openai_service.prompt_image(imageModel, parseText, imageSize)

#                 if imageUrl is not None:
#                     save_image(imageUrl)

#                 # Return the results
#                 return jsonify({'inputText': inputText, 'modText': parseText, 'imageUrl': imageUrl})
#             else:
#                 return jsonify({'error': 'InputText is None'})
#         except Exception as e:
#             logging.exception('Failed to generate image: %s', str(e))
#             return jsonify({'error': 'Failed to generate image'})


#         return jsonify({'inputText': inputText, 'modText': parseText, 'imageUrl':imageUrl})
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