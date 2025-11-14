import json
from flask import Flask, render_template

BLOG_POST_FILE = "blog_posts.json"


def load_posts():
    """ Loads blog posts from JSON file"""
    try:
        with open(BLOG_POST_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"ERROR: The file {BLOG_POST_FILE} was not found.")
        return []
    except json.JSONDecodeError:
        print(
            f"ERROR: Could not decode JSON from {BLOG_POST_FILE}. Check file format.")
        return []


blog_posts = load_posts()

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html", posts=blog_posts)


if __name__ == "__main__":
    app.run(debug=True)
