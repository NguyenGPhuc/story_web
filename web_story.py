from flask import Flask, render_template, request, jsonify, send_file
import openai_service
import logging
import os
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont 
from io import BytesIO
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

        
# Pass to openAI for to translate
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
@app.route('/generateImage', methods=['POST'])
def generate_image():
    if request.method == 'POST':
        try:
            # Set model and image size
            imageSize = request.form.get('imageDimensions')
            if imageSize == "512x512":
                imageModel = 'dall-e-2'
            else:
                imageModel = 'dall-e-3'

            if request.form.get('ModdedTextArea') != '':
                parseText = request.form.get('ModdedTextArea')
                print('Return from front end: ', parseText)
            elif request.form.get('ModdedTextArea') == None and request.form.get('inputText') != '':
                parseText = request.form.get('inputText')
                print('Return from front end: ', parseText)
            else:
                return jsonify({'parseText' : 'To generate image you need a prompt'}  )


            # Get image url form API
            imageUrl = openai_service.prompt_image(imageModel, parseText, imageSize)
            

            if imageUrl is not None:
                save_image(imageUrl)
           

        except Exception as e:
            logging.exception('Failed to generate image: %s', str(e))
            return jsonify({'error': 'Failed to generate image'})

        return jsonify({'imageUrl':imageUrl})
    else:
        print('Unable to generate image')
        return jsonify({'error': 'Unable to generate image'})


# Route to handle saving the story
@app.route('/saveStory', methods=['POST'])
def build_page():
    if request.method == 'POST':
        storyText = request.form.get('ModdedTextArea')
        imageUrl = request.form.get('generated_Image')

        # Dummy image
        image_width = 512
        image_height = 512

        composite_image, text_width = generate_composite_image(storyText, imageUrl)

         # Save the story
        file_path = save_story(composite_image, text_width, storyText)
        
        # Send the file as a response
        return send_file(file_path, as_attachment=True)

# Generate composite image
def generate_composite_image(user_text, imageUrl):
    # Dummy image and text generation logic using Pillow (PIL)
    image_width = 512
    image_height = 512

    composite_image = Image.new('RGB', (image_width, image_height), color='white')
    draw = ImageDraw.Draw(composite_image)

    # Font settings
    font_size = 20
    font = ImageFont.load_default()  # Use the default font

    # Padding and margin
    padding = 20
    text_margin = 20

    # Calculate text size before drawing the text
    text_bbox = draw.textbbox((padding, padding), user_text, font=font, spacing=text_margin)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]

    # Calculate text position
    text_position = ((image_width - text_width) // 2, padding)

    # Draw user text on top
    draw.text(text_position, user_text, font=font, fill='black', spacing=text_margin)


    # If imageUrl is provided, fetch and paste the image
    if imageUrl:
        try:
            response = requests.get(imageUrl)
            image_data = response.content  # Extract the content (bytes) from the response
            original_image = Image.open(BytesIO(image_data))

            # Resize the image while maintaining the aspect ratio
            max_image_height = image_height // 2  # Adjust this as needed
            aspect_ratio = original_image.width / original_image.height
            new_width = int(max_image_height * aspect_ratio)
            new_height = max_image_height
            resized_image = original_image.resize((new_width, new_height), Image.LANCZOS)

             # Calculate the starting position to center the image horizontally
            image_position = ((image_width - new_width) // 2, image_height // 2)

            composite_image.paste(resized_image, image_position)

        except Exception as e:
            print('Error fetching and pasting image:', e)

    return (composite_image, text_width)


# Save whole page
def save_story(composite_image, text_width, user_text):
    try:
        output_folder = 'story_output'
        os.makedirs(output_folder, exist_ok=True)

        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        image_filename = f'{timestamp}.jpeg'

        file_path = f'{output_folder}/{image_filename}'

        composite_image.save(file_path)

        return file_path

    except Exception as e:
        print('Error: ', e)
        return None



# Save image automatically
def save_image(imageUrl):
    print ('In main image function')
    try:
        output_folder = 'output'
        os.makedirs(output_folder, exist_ok=True)

        # Use date and time for naming
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        imageFilename = f'{timestamp}.jpeg'
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