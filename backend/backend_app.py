from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]


@app.route('/api/posts', methods=['GET'])
def get_posts():
    """gets all posts"""
    return jsonify(POSTS)


@app.route("/api/posts", methods=["POST"])
def add_post():
    """adds a new post"""
    data = request.get_json()

    # 1. Validierung, ob Felder gefüllt
    if not data or not data.get("title") or not data.get("content"):
        return jsonify({"error": "Title and content are required"}), 400

    # 2. Neue ID berechnen (höchste bislang vergebene ID +1)
    all_ids = []
    for post in POSTS:
        all_ids.append(post["id"])
    if len(all_ids) > 0:
        highest_id = max(all_ids)
    else:
        highest_id = 0
    new_id = highest_id + 1

    # 3. Neuen Post erstellen, inhalte vom Frontend hinzufügen
    new_post = {
        "id": new_id,
        "title": data["title"],
        "content": data["content"],
    }
    POSTS.append(new_post)

    # 4. Antwort mit Statuscode 201 ("Created")
    return jsonify(new_post), 201


@app.route('/api/posts/<int:id>', methods=['DELETE'])
def delete_post(id):
    """deletes a post"""
    post_to_delete = None

    # 1. Post suchen
    for post in POSTS:
        if post["id"] == id:
            post_to_delete = post
            break

    # 2. Wenn nicht gefunden -> Fehlermeldung 404
    if post_to_delete is None:
        return jsonify({"error": f"Post with id {id} not found."}), 404

    # 3. Post aus Liste entfernen
    POSTS.remove(post_to_delete)

    # 4. Erfolgsmeldung mit 200 OK
    return jsonify({"message": f"Post with id {id} has been deleted successfully."}), 200


@app.route('/api/posts/<int:id>', methods=['PUT'])
def update_post(id):
  """updates an existing post"""
  data = request.get_json() or {}

  # 1. Post in der Liste POSTS suchen
  post = None
  for p in POSTS:
    if p["id"] == id:
      post = p
      break

  # 2. Falls nicht gefunden -> 404
  if post is None:
    return jsonify({"error": f"Post with id {id} not found."}), 404

  # 3. Felder optional aktualisieren (Fallback auf alten Wert, falls keine Eingabe gemacht wurde)
  post["title"] = data.get("title", post["title"])
  post["content"] = data.get("content", post["content"])

  # 4. Aktualisierten Post mit Statuscode 200 zurückgeben
  return jsonify(post), 200


@app.route('/api/posts/search', methods=['GET'])
def search_posts():
  """searches posts by title or content query parameters"""
  title_query = request.args.get('title')
  content_query = request.args.get('content')

  filtered_posts = []

  for post in POSTS:
    # 1. Prüfen, ob der Suchbegriff im Titel vorkommt
    title_matches = (
        title_query and title_query.lower() in post['title'].lower()
    )

    # 2. Prüfen, ob der Suchbegriff im Content vorkommt
    content_matches = (
        content_query and content_query.lower() in post['content'].lower()
    )

    # 3. Wenn mindestens eines der Kriterien zutrifft, hinzufügen
    if title_matches or content_matches:
      filtered_posts.append(post)

  return jsonify(filtered_posts), 200


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
