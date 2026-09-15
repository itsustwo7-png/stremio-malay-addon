from flask import Flask, jsonify
import requests

app = Flask(__name__)

import os
TMDB_API_KEY = os.getenv("142f373ce3f212d473a6d25667243b5e")


MANIFEST = {
    "id": "com.astratutor.globalmalay",
    "version": "1.0.0",
    "name": "Global & Malay Add-on",
    "description": "Carian filem dunia dan Malaysia menggunakan TMDB",
    "resources": ["catalog"],
    "types": ["movie", "series"],
    "catalogs": [
        {
            "type": "movie",
            "id": "top_malay",
            "name": "Carian Filem",
            "extra": [{"name": "search", "isRequired": True}]
        }
    ]
}

@app.route('/manifest.json')
def manifest():
    return jsonify(MANIFEST)

@app.route('/catalog/movie/<id>/search=<query>.json')
def search_catalog(id, query):
    # Panggil TMDB untuk carian
    url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={query}&language=ms-MY"
    response = requests.get(url).json()
    
    metas = []
    for item in response.get('results', []):
        metas.append({
            "id": f"tmdb:{item['id']}",
            "name": item['title'],
            "poster": f"https://image.tmdb.org/t/p/w500{item['poster_path']}",
            "type": "movie"
        })
    
    return jsonify({"metas": metas})

if __name__ == '__main__':
    app.run(port=7000)
