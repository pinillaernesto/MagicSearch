import os
import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Archidekt Configuration from your documentation
ARCHIDEKT_API_BASE = "https://archidekt.com/api"
ARCHIDEKT_TOKEN = os.environ.get("ARCHIDEKT_TOKEN", "")

# Your Deck Library
USER_DECKS = {
    "Isshin, Two Heavens as One": "10972764",
    # You can add more Deck Name: ID pairs here
}

@app.route('/', methods=['GET', 'POST'])
def index():
    cards = []
    query = ""
    if request.method == 'POST':
        query = request.form.get('query')
        if query:
            response = requests.get(f"https://api.scryfall.com/cards/search?q={query}")
            if response.status_code == 200:
                cards = response.json().get('data', [])
    
    return render_template('index.html', cards=cards, query=query, decks=USER_DECKS)

@app.route('/import_deck/<deck_id>')
def import_deck(deck_id):
    # Logic to fetch deck cards from Archidekt
    url = f"{ARCHIDEKT_API_BASE}/decks/{deck_id}/"
    headers = {"Authorization": f"Token {ARCHIDEKT_TOKEN}"} if ARCHIDEKT_TOKEN else {}
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        deck_data = response.json()
        # Extract card names to build a Scryfall search string
        card_names = [card['card']['oracleCard']['name'] for card in deck_data.get('cards', [])]
        search_query = " or ".join([f'!"{name}"' for name in card_names[:20]]) # Limit for API stability
        return jsonify({"query": search_query})
    return jsonify({"error": "Failed to fetch deck"}), 400

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
