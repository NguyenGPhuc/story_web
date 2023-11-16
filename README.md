*** Description ***
A local web UI that used OpenAI API to translate langauge text into English. The translated text get pass into Dall-E as prompt for image generation. Has build in interface that allows uers change
image dimension and batch number.

*** Purpose ***
My cousin owns a wedding arrangement company in Vietnam. The purpose of this program is to help him create concept arts in his own natural language (Vietnamese). This can also be use to create stock
images for advertisement to reach a wider audience. 

*** Requirements ***
Download and install Python - https://www.python.org/downloads/

Flask - A micro web framework written in Python. It is classified as a microframework because it does not require particular tools or libraries. It has no database abstraction layer, form validation, or any other components where pre-existing third-party libraries provide common functions - Wikipedia

OpenAI (GPT-3.5) - An artificial intelligence research laboratory consisting of the for-profit subsidiary OpenAI LP and its parent company, the non-profit OpenAI Inc. 
- pip install openai
<Your own OpenAI API key>
Sign up here -> https://beta.openai.com/signup

*** Instruction ***
1. run 'start_here.bat' - Check for virual environment and install venv and all dependencies if not found. Will start local server automatically when finish.
2. Descibe the image as detail as you in any language in "Input Text" square. OR you can type it in "Translated Text (English)" directly. Select the desire dimension  then click "Generate" button.
3. QUICK GENERATE* Type in "Input Text", select dimension and click "Translate & Generate". Option 2 is if the translation to English is off and you want to change it before generation.
4. All image are saves with "output" folder of the same directory. It will creates one if it doesn't already has it.