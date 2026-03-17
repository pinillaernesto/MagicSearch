import os
from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    cartas = []
    busqueda = ""
    if request.method == 'POST':
        busqueda = request.form.get('query')
        if busqueda:
            url = f"https://api.scryfall.com/cards/search?q={busqueda}"
            response = requests.get(url)
            if response.status_code == 200:
                cartas = response.json().get('data', [])
    
    return render_template('index.html', cartas=cartas, busqueda=busqueda)

if __name__ == '__main__':
    # Usamos el puerto que nos asigne la nube (Render/Google)
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
