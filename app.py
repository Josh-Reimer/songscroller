import os
import re
import hashlib
from flask import Flask, render_template, send_from_directory, abort, jsonify

def _get_version_hash():
  """Generate a hash based on key files to detect updates."""
  files_to_hash = ['sw.js', 'manifest.json', 'app.py']
  hasher = hashlib.md5()
  for fname in files_to_hash:
    if os.path.exists(fname):
      with open(fname, 'rb') as f:
        hasher.update(f.read())
  return hasher.hexdigest()[:8]

def _images_ready():
    if not os.path.exists("img"):
        return False
    return any(
        f.startswith("songscroller") and f.endswith(".jpg")
        for f in os.listdir("img")
    )

def ensure_images():
    if not _images_ready():
        import download_and_convert
        download_and_convert.main()

app = Flask(__name__)

@app.route("/")
def index():
    valid_indices = []
    if os.path.exists("img"):
        for f in os.listdir("img"):
            if f.startswith("songscroller") and f.endswith(".jpg"):
                if os.path.getsize(os.path.join("img", f)) > 30000:
                    idx = f.replace("songscroller", "").replace(".jpg", "")
                    if idx.isdigit():
                        valid_indices.append(int(idx))
    return render_template("Feed.html", valid_indices=valid_indices, version=_get_version_hash())

@app.route("/api/version")
def get_version():
    return jsonify({"version": _get_version_hash()})

@app.route("/img/<filename>")
def serve_image(filename):
    if not re.fullmatch(r'songscroller\d+\.jpg', filename):
        abort(404)
    return send_from_directory("img", filename)

@app.route("/manifest.json")
def serve_manifest():
    return send_from_directory(".", "manifest.json")

@app.route("/sw.js")
def serve_sw():
    response = send_from_directory(".", "sw.js")
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response

@app.route("/icon.svg")
def serve_icon():
    return send_from_directory(".", "icon.svg")

if __name__ == "__main__":
    ensure_images()
    app.run(debug=True, host="0.0.0.0", port=5023)
