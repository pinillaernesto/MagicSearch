import os
import requests
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    cartas = []
    query = ""
    
    if request.method == 'POST':
        # Captura lo que el usuario escribió o seleccionó con los slicers
        query = request.form.get('query')
        
        if query:
            # Llamada a la API de Scryfall usando el query del usuario
            # Scryfall permite combinar filtros con espacios (ej: "c:w f:draw")
            url = f"https://api.scryfall.com/cards/search?q={query}"
            response = requests.get(url)
            
            if response.status_code == 200:
                data = response.json()
                cartas = data.get('data', [])
            else:
                # Si la búsqueda no da resultados o es inválida
                cartas = []
    
    return render_template('index.html', cartas=cartas, query=query)

if __name__ == '__main__':
    # Render usa la variable de entorno PORT
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
