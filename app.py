from flask import Flask, render_template, request
from openai import OpenAI
import os
import time


app = Flask(__name__)

client = OpenAI()

def askGPT(question):
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system",
            "content": "You are TARS from interstellar. Be very sarcastic."
            },
            {
            "role": "user",
            "content": question
            }
        ]
    )
    return completion

def createAudio(text):
    os.remove("static/output.mp3")   
    response = client.audio.speech.create(
        model="tts-1",
        voice="onyx",
        input=text,
    )
    response.stream_to_file("static/output.mp3")

def createImage(prompt):
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024",
        quality="standard",
        n=1,
    )
    return response.data[0].url

@app.route('/', methods=['GET', 'POST'])
def index():
    response = ''
    if request.method == 'POST':
        user_input = request.form['user_input']
        try:
            completion = askGPT(user_input)
            response = completion.choices[0].message.content.strip()
            createAudio(response)
            imageURL = createImage(response)
        except Exception as e:
            response = f"Fehler bei der Anfrage: {e}"
    return render_template('index.html', response=response, imageURL=imageURL, time=time.time())

@app.route('/home', methods=['GET', 'POST'])
def home():
    return render_template('index.html', time=time.time())


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
