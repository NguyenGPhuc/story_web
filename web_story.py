from flask import Flask, render_template, request
import openai_service

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/translateText', methods=['POST'])
def picture_prompt():
    if request.method == "POST":
        user_input = request.form.get('user_input')

        try:
            openai_service.translate_viet2en(user_input)
        except:
            print('Unable to call from API')

    else: 
        print ("Input was not correctly process")

    return render_template('result.html', user_input=user_input, generated_text=generated_text)

if __name__ == '__main__':
    app.run(debug = True)



