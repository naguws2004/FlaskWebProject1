from flask import Flask, request, render_template
from transformers import pipeline

app = Flask(__name__)

# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app

@app.route('/')
def index():
    return '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Generate a Song</title>
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
            <form action="/submit" method="post" class="form-container" onsubmit="return validateForm()">
                <h1>Generate a Song</h1>
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
                            <input type="submit" value="Generate">

                            <!-- Reset Button -->
                            <input type="reset" value="Reset">
                        </td>
                    </tr>
                </table>
            </form>
        </body>
        </html>
    '''

@app.route('/submit', methods=['POST'])
def submit():
    txtWords = request.form.get('txtWords')
    lstGenre = request.form.get('lstGenre')
    lstInstruments = request.form.getlist('lstInstruments')
    
    # Initialize the Hugging Face text generation pipeline
    generator = pipeline('text-generation', model='mistralai/Mixtral-8x7B-Instruct-v0.1', use_auth_token='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')

    # Generate text using the Hugging Face model
    prompt = f"Write a poem using words: {txtWords}"
    response = generator(prompt, max_length=250, num_return_sequences=1)
    
    generated_lyrics = response[0]['generated_text'].strip()

    # Process the form data as needed
    return render_template('form_submitted.html', 
                    generated_lyrics=generated_lyrics, txtWords=txtWords, lstGenre=lstGenre, lstInstruments=lstInstruments)

if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)
