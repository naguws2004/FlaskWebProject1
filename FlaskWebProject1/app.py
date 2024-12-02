from flask import Flask, request, render_template_string, render_template
import magenta
from magenta.models.music_vae import configs
from magenta.models.music_vae import music_vae_model
import requests
import json

app = Flask(__name__)

# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app

@app.route('/')
def index():
    return '''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Generate Lyrics</title>
            <style>
                .form-container {
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                }
                .form-table {
                    margin: 0 auto;
                }
                .field-width {
                    width: 250px;
                }
            </style>
            <script>
                function validateForm() {
                    var txtWords = document.getElementById('txtWords').value;
                    var lstGenre = document.getElementById('lstGenre').value;
                    var lstInstruments = document.getElementById('lstInstruments').selectedOptions;
                    
                    if (lstGenre === '') {
                        alert('Please select a genre.');
                        return false;
                    }
                    if (txtWords.trim() === '') {
                        alert('Words cannot be empty.');
                        return false;
                    }
                    if (lstInstruments.length === 0) {
                        alert('Please select at least one instrument.');
                        return false;
                    }
                    return true;
                }
            </script>
        </head>
        <body>
            <form action="/songform" method="post" class="form-container" onsubmit="return validateForm()">
                <h1>Generate Lyrics</h1>
                <table class="form-table">
                    <tr>
                        <td>
                            <label for="lblGenre">Select Genre:</label>
                        </td>
                        <td colspan="2">
                            <select id="lstGenre" name="lstGenre" class="field-width">
                                <option value="Pop">Pop</option>
                                <option value="Hip-hop">Hip-hop</option>
                                <option value="EDM">EDM</option>
                                <option value="Rock">Rock</option>
                                <option value="Country">Country</option>
                                <option value="Classical">Classical</option>
                                <option value="R&B">R&B</option>
                                <option value="Jazz">Jazz</option>
                                <option value="Reggae">Reggae</option>
                                <option value="Latin">Latin</option>
                                <option value="Techno">Techno</option>
                                <option value="Metal">Metal</option>
                            </select>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <label for="lblWords">Enter words for Song:</label>
                        </td>
                        <td>
                            <input type="text" id="txtWords" name="txtWords" style="width:243px;" placeholder="example: cute, beautiful, sweet, etc.,">
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <label for="lblInstruments">Select Instruments:</label>
                        </td>
                        <td>
                            <select id="lstInstruments" name="lstInstruments" class="field-width" multiple>
                                <option value="Guitar">Guitar</option>
                                <option value="Piano">Piano</option>
                                <option value="Keyboard">Keyboard</option>
                                <option value="Saxophone">Saxophone</option>
                                <option value="Drums">Drums</option>
                                <option value="Violin">Violin</option>
                                <option value="Flute">Flute</option>
                                <option value="Trumpet">Trumpet</option>
                                <option value="Cello">Cello</option>
                                <option value="Electronic Guitar">Electronic Guitar</option>
                            </select>
                        </td>
                    </tr>
                    <tr>
                        <td>
                        </td>
                        <td>
                            <!-- Submit Button -->
                            <input type="submit" value="Generate Lyrics">

                            <!-- Reset Button -->
                            <input type="reset" value="Reset">
                        </td>
                    </tr>
                </table>
            </form>
        </body>
        </html>
    '''

@app.route('/songform', methods=['POST'])
def songform():
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

    #response = requests.post(url, headers=headers, json=data)

    # Check if the request was successful
    # if response.status_code == 200:
    #     response_json = json.loads(response.text)
    #     generated_lyrics = response_json['choices'][0]['message']['content'].strip()
    # else:
    generated_lyrics = 'Error generating lyrics.'

    # Process the form data as needed
    return render_song_form(prompt, generated_lyrics, txtWords, lstGenre, lstInstruments)

def render_song_form(txtPrompt, generated_lyrics, txtWords, lstGenre, lstInstruments):
    return render_template_string('''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Song Lyrics</title>
            <style>
                .form-container {
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                }
                .form-table {
                    margin: 0 auto;
                }
                .field-width {
                    width: 250px;
                }
            </style>
        </head>
        <body>
            <form action="/yoursong" method="post" class="form-container">
                <h1>Song Lyrics</h1>
                <div>Genre: {{ lstGenre }}</div><br/>
                <div>Words: {{ txtWords }}</div><br/>
                <div>Instruments: {{ lstInstruments }}</div><br/>
                <div>Prompt: {{ txtPrompt }}</div><br/>
                <div>Lyrics: <textarea id="txtlyrics" name="txtlyrics" style="vertical-align:middle;" rows="10" cols="75">{{ generated_lyrics }}</textarea></div><br/>
                <!-- Submit Button -->
                <div>
                <input type="submit" value="Create Song">
                <input type="button" onclick="history.back()" value="Back">
                </div>
            </form>
        </body>
        </html>
    ''', txtPrompt=txtPrompt, generated_lyrics=generated_lyrics, txtWords=txtWords, lstGenre=lstGenre, lstInstruments=lstInstruments)

@app.route('/yoursong', methods=['POST'])
def yoursong():
    txtlyrics = request.form.get('txtlyrics')
    
    lyrics = "I'm a little teapot, short and stout"
    style = "pop"
    song_data = generate_song(lyrics, style)

    # Process the form data as needed
    return render_template_string('''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Your Song</title>
            <style>
                .form-container {
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                }
                .form-table {
                    margin: 0 auto;
                }
                .field-width {
                    width: 250px;
                }
            </style>
        </head>
        <body>
            <form class="form-container">
                <h1>Your Song</h1>
                <div><a href="{{ txtLink }}">Song Link</a></div>
            </form>
        </body>
        </html>
    ''', txtLink=song_data)

def generate_song(lyrics, style):
    url = "https://api.topmediai.com/v2/music"  # Replace with the actual endpoint
    headers = {
        "Authorization": "Bearer YOUR_API_KEY"
    }
    data = {
        "lyrics": lyrics,
        "style": style
    }

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Request failed with status code {response.status_code}")
        return None 

if __name__ == '__main__':
    # import os
    # HOST = os.environ.get('SERVER_HOST', 'localhost')
    # try:
    #     PORT = int(os.environ.get('SERVER_PORT', '5555'))
    # except ValueError:
    #     PORT = 5555
    # app.run(HOST, PORT)

    from huggingface_hub import hf_hub_download
    hf_hub_download(repo_id="facebook/musicgen-large", filename="config.json")