from flask import Flask, jsonify, request
import json

app = Flask(__name__)

# Load data from JSON
with open("cac1.json", "r") as file:
    data = json.load(file)

# -------------------- USER MANAGEMENT --------------------
@app.route("/users", methods=["GET"])
def get_users():
    return jsonify(data["users"])

@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = next((u for u in data["users"] if u["id"] == user_id), None)
    return jsonify(user) if user else ("User not found", 404)

@app.route("/users", methods=["POST"])
def create_user():
    new_user = request.json
    new_user["id"] = len(data["users"]) + 1
    data["users"].append(new_user)
    return jsonify(new_user), 201

@app.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    user = next((u for u in data["users"] if u["id"] == user_id), None)
    if not user:
        return ("User not found", 404)
    user.update(request.json)
    return jsonify(user)

@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    data["users"] = [u for u in data["users"] if u["id"] != user_id]
    return ("User deleted", 200)

# -------------------- SONG MANAGEMENT --------------------
@app.route("/songs", methods=["GET"])
def get_songs():
    return jsonify(data["songs"])

@app.route("/songs/<int:song_id>", methods=["GET"])
def get_song(song_id):
    song = next((s for s in data["songs"] if s["id"] == song_id), None)
    return jsonify(song) if song else ("Song not found", 404)

@app.route("/songs", methods=["POST"])
def add_song():
    new_song = request.json
    new_song["id"] = len(data["songs"]) + 1
    data["songs"].append(new_song)
    return jsonify(new_song), 201

@app.route("/songs/<int:song_id>", methods=["PUT"])
def update_song(song_id):
    song = next((s for s in data["songs"] if s["id"] == song_id), None)
    if not song:
        return ("Song not found", 404)
    song.update(request.json)
    return jsonify(song)

@app.route("/songs/<int:song_id>", methods=["DELETE"])
def delete_song(song_id):
    data["songs"] = [s for s in data["songs"] if s["id"] != song_id]
    return ("Song deleted", 200)

# -------------------- PLAYLIST MANAGEMENT --------------------
@app.route("/playlists", methods=["GET"])
def get_playlists():
    return jsonify(data["playlists"])

@app.route("/playlists/<int:playlist_id>", methods=["GET"])
def get_playlist(playlist_id):
    playlist = next((p for p in data["playlists"] if p["id"] == playlist_id), None)
    return jsonify(playlist) if playlist else ("Playlist not found", 404)

@app.route("/playlists", methods=["POST"])
def create_playlist():
    new_playlist = request.json
    new_playlist["id"] = len(data["playlists"]) + 1
    data["playlists"].append(new_playlist)
    return jsonify(new_playlist), 201

@app.route("/playlists/<int:playlist_id>", methods=["PUT"])
def update_playlist(playlist_id):
    playlist = next((p for p in data["playlists"] if p["id"] == playlist_id), None)
    if not playlist:
        return ("Playlist not found", 404)
    playlist.update(request.json)
    return jsonify(playlist)

@app.route("/playlists/<int:playlist_id>", methods=["DELETE"])
def delete_playlist(playlist_id):
    data["playlists"] = [p for p in data["playlists"] if p["id"] != playlist_id]
    return ("Playlist deleted", 200)

# -------------------- ALBUM MANAGEMENT --------------------
@app.route("/albums", methods=["GET"])
def get_albums():
    return jsonify(data["albums"])

@app.route("/albums/<int:album_id>", methods=["GET"])
def get_album(album_id):
    album = next((a for a in data["albums"] if a["id"] == album_id), None)
    return jsonify(album) if album else ("Album not found", 404)

# -------------------- SEARCH --------------------
@app.route("/search", methods=["GET"])
def search():
    query = request.args.get("q", "").lower()
    results = {
        "songs": [s for s in data["songs"] if query in s["title"].lower()],
        "artists": [a for a in data["artists"] if query in a["name"].lower()],
        "albums": [a for a in data["albums"] if query in a["title"].lower()]
    }
    return jsonify(results)

# -------------------- SHUFFLE & REPEAT --------------------
@app.route("/shuffle/<int:playlist_id>", methods=["POST"])
def shuffle_playlist(playlist_id):
    return jsonify({"message": f"Shuffling playlist {playlist_id}"})

@app.route("/repeat/<int:song_id>", methods=["POST"])
def repeat_song(song_id):
    return jsonify({"message": f"Repeating song {song_id}"})

# -------------------- DOWNLOAD --------------------
@app.route("/download/<int:song_id>", methods=["POST"])
def download_song(song_id):
    return jsonify({"message": f"Downloading song {song_id}"})

# -------------------- FAVORITE SONGS --------------------
@app.route("/users/<int:user_id>/favorites", methods=["GET"])
def get_favorites(user_id):
    user = next((u for u in data["users"] if u["id"] == user_id), None)
    if user:
        return jsonify(user.get("favorites", []))
    return ("User not found", 404)

@app.route("/users/<int:user_id>/favorites", methods=["POST"])
def add_favorite(user_id):
    song_id = request.json.get("song_id")
    user = next((u for u in data["users"] if u["id"] == user_id), None)
    if user:
        user.setdefault("favorites", []).append(song_id)
        return jsonify({"message": "Song added to favorites"})
    return ("User not found", 404)

# -------------------- PLAYLIST SONG MANAGEMENT --------------------
@app.route("/playlists/<int:playlist_id>/songs", methods=["POST"])
def add_song_to_playlist(playlist_id):
    song_id = request.json.get("song_id")
    playlist = next((p for p in data["playlists"] if p["id"] == playlist_id), None)
    if playlist:
        playlist.setdefault("songs", []).append(song_id)
        return jsonify({"message": "Song added to playlist"})
    return ("Playlist not found", 404)

@app.route("/playlists/<int:playlist_id>/songs/<int:song_id>", methods=["DELETE"])
def remove_song_from_playlist(playlist_id, song_id):
    playlist = next((p for p in data["playlists"] if p["id"] == playlist_id), None)
    if playlist and song_id in playlist.get("songs", []):
        playlist["songs"].remove(song_id)
        return jsonify({"message": "Song removed from playlist"})
    return ("Playlist or song not found", 404)

# -------------------- USER STATISTICS --------------------
@app.route("/users/<int:user_id>/stats", methods=["GET"])
def user_stats(user_id):
    user = next((u for u in data["users"] if u["id"] == user_id), None)
    if user:
        stats = {
            "total_playlists": sum(1 for p in data["playlists"] if p["user_id"] == user_id),
            "total_favorites": len(user.get("favorites", []))
        }
        return jsonify(stats)
    return ("User not found", 404)

if __name__ == "__main__":
    app.run(debug=True)
