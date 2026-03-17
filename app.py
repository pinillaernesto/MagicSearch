import os
import requests
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    cards = []
    query = ""
    if request.method == 'POST':
        query = request.form.get('query')
        if query:
            # Conexión directa con la API de Scryfall
            response = requests.get(f"https://api.scryfall.com/cards/search?q={query}")
            if response.status_code == 200:
                cards = response.json().get('data', [])
    
    return render_template('index.html', cards=cards, query=query)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
