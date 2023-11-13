from flask import Flask, render_template, request
import openai_service

app = Flask(__name__)

# Start default site
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/translateText', methods=['POST'])
def picture_prompt():
    if request.method == "POST":

        translatedText = ''

        #Funtion for translating from vietnamese to english
        try:
            inputText = request.form.get('inputText')
            translatedText = openai_service.translate_viet2en(request.form.get('inputText'))

        except:
            print('Unable to call from API')

    else: 
        print ("Input was not correctly process")

    return render_template('index.html', inputText=inputText, translatedText=translatedText)

if __name__ == '__main__':
    app.run(debug = True)



