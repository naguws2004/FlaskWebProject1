from flask import Flask, request, render_template_string, render_template
import requests
import json

app = Flask(__name__)

def render_song_form(txtPrompt, generated_lyrics, txtWords, lstGenre, lstInstruments):
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Song Prompt</title>
    </head>
    <body>
        <h1>Song Prompt!</h1>
        <p>Genre: {{ lstGenre }}</p>
        <p>Words: {{ txtWords }}</p>
        <p>Instruments: {{ lstInstruments }}</p>
        <p>Prompt: {{ txtPrompt }}</p>
        <p>Lyrics: <textarea id="txtlyrics" name="txtlyrics" style="vertical-align:middle;" rows="10" cols="75" readonly>{{ generated_lyrics }}</textarea></p>
    </body>
    </html>
    ''', txtPrompt=txtPrompt, generated_lyrics=generated_lyrics, txtWords=txtWords, lstGenre=lstGenre, lstInstruments=lstInstruments)

@app.route('/submit', methods=['POST'])
def submit():
    txtWords = request.form.get('txtWords')
    lstGenre = request.form.get('lstGenre')
    lstInstruments = request.form.getlist('lstInstruments')
    
    # Generate text
    prompt = f"Write a song using words: {txtWords}. Song genre is: {lstGenre}. Song will use instruments: {lstInstruments}."
    
    url = "https://api.x.ai/v1/chat/completions"
    headers = {
      "Authorization": "Bearer xai-P2VrBOBKw2Z2apm7eu5CA0s6ryOf9E32rNfnXVmmuafPvLWsX4G8eaXLBtgTvFd86kgMDyeyQ0JN1akK",
      "Content-Type": "application/json"
    }
    data = {
        "model": "grok-beta",
        "messages": [
        { "role": "user", "content": prompt }
        ],
        "temperature": 0,
        "stream": False
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
      print(response.json())
    else:
      print(response.text)
    
    # Check if the request was successful
    if response.status_code == 200:
        response_json = json.loads(response.text)
        generated_lyrics = response_json['choices'][0]['message']['content'].strip()
    else:
        generated_lyrics = 'Error generating lyrics.'

    # Process the form data as needed
    return render_template('song.html')

