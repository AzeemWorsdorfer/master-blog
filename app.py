import json
from flask import Flask, render_template, request, redirect, url_for

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


def save_post(posts):
    """ Writes the current lists of posts back to the JSON."""
    try:
        with open(BLOG_POST_FILE, "w") as f:
            json.dumps(posts, f, indent=4)
        print(
            f"INFO: Successfully saved {len(posts)} posts to {BLOG_POST_FILE}.")
    except Exception as e:
        print(f"ERROR: Failed to save posts to {BLOG_POST_FILE}: {e}")


def get_next_id():
    """
    Generates the next sequential ID for a new blog post.
    Finds the highest existing ID and adds 1.
    """
    if not blog_posts:
        return 1

    max_id = max(post.get('id', 0) for post in blog_posts)
    return max_id + 1


# --- Application Initialization ---


# Loads data once when the application starts
blog_posts = load_posts()

app = Flask(__name__)

# --- Routes ---


@app.route('/')
def index():
    return render_template("index.html", posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        title = request.form.get('title')
        author = request.form.get('author')
        content = request.form.get('content')

        if not title or not author or not content:
            print("WARNING: Form submitted with missing data.")
            return render_template('add.html')

        # Create a new post dictionary with a unique ID
        new_post = {
            'id': get_next_id(),
            'title': title,
            'author': author,
            'content': content
        }

        # Append the new post to the global list
        blog_posts.append(new_post)

        # Save the updated list back to the JSON file
        save_post(blog_posts)

        # Redirect the user back to the index page to see the new post
        return redirect(url_for('index.html'))

        # Handle GET request (initial page load to display the form)
    return render_template('add.html')


if __name__ == "__main__":
    app.run(debug=True)
