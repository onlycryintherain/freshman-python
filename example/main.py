from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)
ANILIST = "https://graphql.anilist.co"

def anilist(query, variables={}):
    r = requests.post(ANILIST, json={"query": query, "variables": variables},
                      headers={"Content-Type": "application/json"}, timeout=6)
    return r.json().get("data", {})

TRENDING_Q = """
query ($page: Int) {
  trending: Page(page: $page, perPage: 12) {
    media(sort: TRENDING_DESC, type: ANIME) {
      id title { romaji english }
      coverImage { large }
      averageScore episodes status
      genres startDate { year }
      bannerImage
    }
  }
  popular: Page(perPage: 6) {
    media(sort: POPULARITY_DESC, type: ANIME) {
      id title { romaji english }
      coverImage { large }
      averageScore episodes
      genres startDate { year }
    }
  }
}
"""

DETAIL_Q = """
query ($id: Int) {
  Media(id: $id, type: ANIME) {
    id title { romaji english native }
    coverImage { extraLarge }
    bannerImage description averageScore popularity
    episodes duration status season seasonYear
    genres studios(isMain: true) { nodes { name } }
    staff(perPage: 6) { edges { role node { name { full } } } }
    characters(perPage: 8, sort: ROLE) {
      edges { role node { name { full } image { medium } } }
    }
    trailer { id site }
    relations {
      edges {
        relationType(version: 2)
        node { id title { romaji } coverImage { medium } type }
      }
    }
  }
}
"""

SEARCH_Q = """
query ($search: String, $genre: String, $sort: [MediaSort]) {
  Page(perPage: 20) {
    media(search: $search, genre: $genre, sort: $sort, type: ANIME) {
      id title { romaji english }
      coverImage { large }
      averageScore episodes genres startDate { year } status
    }
  }
}
"""

GENRES_Q = "query { GenreCollection }"

@app.route("/")
def index():
    data = anilist(TRENDING_Q, {"page": 1})
    trending = data.get("trending", {}).get("media", [])
    popular  = data.get("popular", {}).get("media", [])
    return render_template("index.html", trending=trending, popular=popular)

@app.route("/anime/<int:anime_id>")
def detail(anime_id):
    data = anilist(DETAIL_Q, {"id": anime_id})
    m = data.get("Media")
    if not m:
        return "Not found", 404
    return render_template("detail.html", m=m)

@app.route("/search")
def search():
    q     = request.args.get("q", "")
    genre = request.args.get("genre", "")
    sort  = request.args.get("sort", "TRENDING_DESC")
    variables = {"search": q or None, "genre": genre or None, "sort": [sort]}
    data = anilist(SEARCH_Q, variables)
    results = data.get("Page", {}).get("media", [])
    genres_data = anilist(GENRES_Q)
    genres = genres_data.get("GenreCollection", [])
    return render_template("search.html", results=results, q=q,
                           genre=genre, sort=sort, genres=genres)

@app.route("/api/autocomplete")
def autocomplete():
    q = request.args.get("q", "")
    if not q:
        return jsonify([])
    data = anilist(SEARCH_Q, {"search": q, "genre": None, "sort": ["POPULARITY_DESC"]})
    items = data.get("Page", {}).get("media", [])[:6]
    return jsonify([{
        "id": m["id"],
        "title": m["title"]["english"] or m["title"]["romaji"],
        "year": m["startDate"]["year"],
        "score": m["averageScore"],
        "poster": m["coverImage"]["large"]
    } for m in items])

if __name__ == "__main__":
    app.run(debug=True)