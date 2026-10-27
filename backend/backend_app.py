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
    return jsonify(POSTS)


@app.route("/api/posts", methods=["POST"])
def add_post():
    data = request.get_json()

    # 1. Validierung
    if not data or not data.get("title") or not data.get("content"):
        return jsonify({"error": "Title and content are required"}), 400

    # 2. Neue ID berechnen
    all_ids = []
    for post in POSTS:
        all_ids.append(post["id"])
    if len(all_ids) > 0:
        highest_id = max(all_ids)
    else:
        highest_id = 0
    new_id = highest_id + 1

    # 3. Neun Post erstellen und hinzufügen
    new_post = {
        "id": new_id,
        "title": data["title"],
        "content": data["content"],
    }
    POSTS.append(new_post)

    # 4. Antwort mit Statuscode 201
    return jsonify(new_post), 201


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
