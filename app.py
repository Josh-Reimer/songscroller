import os
from flask import Flask,render_template,send_from_directory

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
    return render_template("Feed.html", valid_indices=valid_indices)

@app.route("/img/<filename>")
def serve_image(filename):
    return send_from_directory("img",filename)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5023)
