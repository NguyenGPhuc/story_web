from flask import Flask, render_template, request, jsonify
import openai_service

app = Flask(__name__)

# Start default site
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/translateText', methods=['POST'])
def translated_text():
    if request.method == "POST":

        inputText = request.form.get('inputText')
        translatedText = ''

        #Funtion for translating from vietnamese to english
        try:
            translatedText = openai_service.translate_viet2en(request.form.get('inputText'))

        except:
            print('Unable to call from API')
        
        return jsonify({'translatedText': translatedText, 'inputText': inputText})

    else: 
        print ("User input was not processed correctly")

    return render_template('index.html', inputText='', translatedText='')

if __name__ == '__main__':
    app.run(debug = True)



