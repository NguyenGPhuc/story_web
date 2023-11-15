from flask import Flask, render_template, request, jsonify
import openai_service
import logging

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
           

        except Exception as e:
            logging.exception('Failed to generate image: %s', str(e))
            return jsonify({'error': 'Failed to generate image'})

        return jsonify({'imageUrl':imageUrl})
    else:
        print('Unable to generate image')
        return jsonify({'error': 'Unable to generate image'})

    

if __name__ == '__main__':
    app.run(debug = True)



