import os
import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Configuración de Archidekt (Usuario: Tonces)
ARCHIDEKT_API_BASE = "https://archidekt.com/api"
ARCHIDEKT_TOKEN = os.environ.get("ARCHIDEKT_TOKEN", "")

# Tu librería de Decks actualizada
DECKS = {
    "Aragorn": 10988300,
    "Ashaya": 10984036,
    "Dromoka": 19599339,
    "Isshin": 10972764,
    "Krenko": 11004127,
    "Prosper": 11006075,
    "Rocco": 11007392,
    "Tergrid": 10981623,
    "Teval": 13178654
}

@app.route('/', methods=['GET', 'POST'])
def index():
    cards = []
    query = ""
    if request.method == 'POST':
        query = request.form.get('query')
        if query:
            # Llamada a Scryfall API
            response = requests.get(f"https://api.scryfall.com/cards/search?q={query}")
            if response.status_code == 200:
                cards = response.json().get('data', [])
    
    return render_template('index.html', cards=cards, query=query, decks=DECKS)

@app.route('/import_deck/<deck_id>')
def import_deck(deck_id):
    url = f"{ARCHIDEKT_API_BASE}/decks/{deck_id}/"
    headers = {"Authorization": f"Token {ARCHIDEKT_TOKEN}"} if ARCHIDEKT_TOKEN else {}
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        deck_data = response.json()
        # Extraemos nombres de cartas (Límite 30 para estabilidad de URL)
        card_names = [card['card']['oracleCard']['name'] for card in deck_data.get('cards', [])]
        search_query = " or ".join([f'!"{name}"' for name in card_names[:30]])
        return jsonify({"query": search_query})
    return jsonify({"error": "Failed to fetch deck from Archidekt"}), 400

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
