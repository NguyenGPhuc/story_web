from flask import Flask, render_template, request, jsonify
import openai_service
import logging
import os
from datetime import datetime
from PIL import Image
import requests

app = Flask(__name__)

# Start default site
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/translateText', methods=['POST'])
def translated_text():
    if request.method == "POST":

        global parseTranslate

        # Get user input (Vietamese text)
        inputText = request.form.get('inputText')

        #Funtion for translating from vietnamese to english
        try:
            # Gets transltion text from API
            translatedText = openai_service.translate_viet2en(request.form.get('inputText'))
            # Remove any extra characters winthin the translation string
            parseTranslate = translatedText.replace('\n', '').replace('"', '').replace('.', '')


        except:
            print('Unable to call from API')
        
        # Return translated text in json format
        return jsonify({'translatedText': parseTranslate, 'inputText': inputText})

    else: 
        print ("User input was not processed correctly")


    return render_template('index.html', inputText='', translatedText='')

# Generate image using translated text
@app.route('/generateImage', methods=['POST'])
def generate_image():
    if request.method == 'POST':
        try:

            # Get image url form API
            imageUrl = openai_service.prompt_image(parseTranslate)


            if imageUrl is not None:
                save_image(imageUrl)
           

        except Exception as e:
            logging.exception('Failed to generate image: %s', str(e))
            return jsonify({'error': 'Failed to generate image'})

        return jsonify({'imageUrl':imageUrl})
    else:
        print('Unable to generate image')
        return jsonify({'error': 'Unable to generate image'})

# Translate and generate image.
# Doesn't display translated text.
@app.route('/translateGenerate', methods=['POST'])
def translate_N_Generate():
    if request.method == 'POST':
        try:
            # Get user input (Vietnamese text)
            inputText = request.form.get('inputText')
            
            # Check if inputText is not None before proceeding
            if inputText is not None:

                print(inputText)

                # Gets translation text from API
                translatedText = openai_service.translate_viet2en(inputText)
                
                # Remove any extra characters within the translation string
                parseTranslate = translatedText.replace('\n', '').replace('"', '').replace('.', '')

                # Get generated image URL from API
                imageUrl = openai_service.prompt_image(parseTranslate)

                if imageUrl is not None:
                    save_image(imageUrl)

                # Return the results
                return jsonify({'inputText': inputText, 'translatedText': parseTranslate, 'imageUrl': imageUrl})
            else:
                return jsonify({'error': 'InputText is None'})
        except Exception as e:
            logging.exception('Failed to generate image: %s', str(e))
            return jsonify({'error': 'Failed to generate image'})

        # return jsonify({'imageUrl':imageUrl})

        return jsonify({'inputText': inputText, 'translatedText': parseTranslate, 'imageUrl':imageUrl})
    else:
        print('Unable to generate image')
        return jsonify({'error': 'Unable to generate image'})


def save_image(imageUrl):
    try:
        output_folder = 'output'
        os.makedirs(output_folder, exist_ok=True)

        # Use date and time for naming
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        imageFilename = f'generated_image_{timestamp}.jpeg'
        imagePath = os.path.join(output_folder, imageFilename)

        # Download the image from url
        imageData = requests.get(imageUrl).content
    
        # Save image
        with open(imagePath, 'wb') as f:
            f.write(imageData)

    except Exception as e:
        logging.exception('Failed to save image: %s', str(e))
        return jsonify({'error': 'Failed to save image'})


if __name__ == '__main__':
    app.run(debug = True)



