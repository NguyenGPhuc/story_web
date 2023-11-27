*** Description ***
A local Web UI for creative story tellers. Offers a variety of toosl to help put your ideas into writing as quickly as possible.
Uses Google API for multi language translations, OpenAI for theme adaptations, and Grammarly API for sentence errors.
Able to generate images to go along with text for a more immersive narritive. Uses OenAI's Dall-E for image generate using user prompt.

*** Purpose ***
I have many narratives that I keeps in my mind. The problem is I don't the time nor patients to put them on paper. 
I wrote this program for myself and those who share similar dilema. The purpose is to quickly writes, fix, and modify
a narrative with AI assistant. 

*** Requirements ***
Download and install Python - https://www.python.org/downloads/

Flask - A micro web framework written in Python. It is classified as a microframework because it does not require particular tools or libraries. It has no database abstraction layer, form validation, or any other components where pre-existing third-party libraries provide common functions - Wikipedia

OpenAI (GPT-3.5) - An artificial intelligence research laboratory consisting of the for-profit subsidiary OpenAI LP and its parent company, the non-profit OpenAI Inc. 
<Your own OpenAI API key>
Sign up here -> https://beta.openai.com/signup

1. Create a new file within this directory call 'config.py'
2. Write the API key in this format : openai_key = 'sk-abc123...'


*** Instruction ***
1. run 'start_here.bat' - Check for virual environment and install venv and all dependencies if not found. Will start local server automatically when finish.