import json
import os
from flask import Flask, render_template, request, redirect, url_for, abort

BLOG_POST_FILE = "blog_posts.json"


def load_posts():
    """ Loads blog posts from JSON file"""
    if not os.path.exists(BLOG_POST_FILE) or os.path.getsize(BLOG_POST_FILE) == 0:
        return []

    try:
        with open(BLOG_POST_FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(
            f"ERROR: Could not decode JSON from {BLOG_POST_FILE}. Check file format.")
        return []


def save_posts(posts):
    """ Writes the current lists of posts back to the JSON (CRITICAL FIX)."""
    try:
        # Use json.dump to write directly to the file object
        with open(BLOG_POST_FILE, "w") as f:
            json.dump(posts, f, indent=4)
        print(
            f"INFO: Successfully saved {len(posts)} posts to {BLOG_POST_FILE}.")
    except Exception as e:
        print(f"ERROR: Failed to save posts to {BLOG_POST_FILE}: {e}")


def get_next_id():
    """
    Generates the next sequential ID for a new blog post.
    Finds the highest existing ID and adds 1.
    """

    current_posts = load_posts()
    if not current_posts:
        return 1

    max_id = max(post.get('id', 0) for post in current_posts)
    return max_id + 1


# --- Application Initialization ---

# Load data on start, and make sure it exists
blog_posts = load_posts()
if not os.path.exists(BLOG_POST_FILE):
    save_posts(blog_posts)

app = Flask(__name__)

# --- Routes ---


@app.route('/')
def index():
    # Reload posts to ensure the latest version is always displayed
    global blog_posts
    blog_posts = load_posts()
    return render_template("index.html", posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    global blog_posts
    if request.method == 'POST':
        title = request.form.get('title')
        author = request.form.get('author')
        content = request.form.get('content')

        if not title or not author or not content:
            return render_template('add.html')

        new_post = {
            'id': get_next_id(),
            'title': title,
            'author': author,
            'content': content
        }

        # Append to the list in memory and save to file
        blog_posts.append(new_post)
        save_posts(blog_posts)

        return redirect(url_for('index'))

    return render_template('add.html')


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    """Handles updating an existing blog post."""
    global blog_posts

    post_to_edit = next(
        (post for post in blog_posts if post.get('id') == post_id), None)

    if post_to_edit is None:
        abort(404, description="Post not found")

    if request.method == 'POST':
        title = request.form.get('title')
        author = request.form.get('author')
        content = request.form.get('content')

        if not title or not author or not content:
            return render_template('update.html', post=post_to_edit)

        # Update the post in the in-memory list
        post_to_edit['title'] = title
        post_to_edit['author'] = author
        post_to_edit['content'] = content

        save_posts(blog_posts)
        return redirect(url_for('index'))

    # GET request: Show the update form populated with existing data
    return render_template('update.html', post=post_to_edit)


@app.route('/delete/<int:post_id>', methods=['POST'])
def delete(post_id):
    """Handles deleting a post (now uses POST method)."""
    global blog_posts

    original_length = len(blog_posts)
    blog_posts = [post for post in blog_posts if post.get('id') != post_id]

    if len(blog_posts) < original_length:
        print(f"INFO: Deleted post ID {post_id}.")
        save_posts(blog_posts)
    else:
        print(f"WARNING: Attempted to delete non-existent post ID {post_id}.")

    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)
