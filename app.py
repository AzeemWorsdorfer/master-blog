import json
import os
from flask import Flask, render_template, request, redirect, url_for, abort

BLOG_POST_FILE = "blog_posts.json"


def load_posts():
    """
    Loads blog posts from the JSON file.

    Returns:
        list: A list of blog post dictionaries. Returns an empty list on file error or absence.
    """
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
    """
    Writes the current list of posts back to the JSON file.

    Args:
        posts (list): The list of blog post dictionaries to save.
    """
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

    Returns:
        int: The next available ID.
    """

    current_posts = load_posts()
    if not current_posts:
        return 1

    max_id = max(post.get('id', 0) for post in current_posts)
    return max_id + 1


# --- Application Initialization ---

# Load data on start, and make sure the file exists if posts were loaded
initial_posts = load_posts()
if not os.path.exists(BLOG_POST_FILE):
    save_posts(initial_posts)

app = Flask(__name__)

# --- Routes ---


@app.route('/')
def index():
    """
    The main route, displays all blog posts.

    Returns:
        render_template: Renders the index.html template with the current posts.
    """
    # Simply load posts without modifying any global variable
    blog_posts = load_posts()
    return render_template("index.html", posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    """
    Handles adding a new blog post.

    GET: Displays the add post form.
    POST: Processes the form data, creates a new post, saves it, and redirects to index.
    """
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

        # Load, append, and save
        blog_posts = load_posts()
        blog_posts.append(new_post)
        save_posts(blog_posts)

        return redirect(url_for('index'))

    return render_template('add.html')


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    """
    Handles updating an existing blog post.

    Args:
        post_id (int): The ID of the post to update.

    GET: Shows the update form populated with existing data.
    POST: Processes the form data, updates the post, saves it, and redirects to index.
    """
    blog_posts = load_posts()
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

        # Update the post in the list
        post_to_edit['title'] = title
        post_to_edit['author'] = author
        post_to_edit['content'] = content

        save_posts(blog_posts)
        return redirect(url_for('index'))

    # GET request: Show the update form populated with existing data
    return render_template('update.html', post=post_to_edit)


@app.route('/delete/<int:post_id>', methods=['POST'])
def delete(post_id):
    """
    Handles deleting a post.

    Args:
        post_id (int): The ID of the post to delete.

    POST: Deletes the post, saves the updated list, and redirects to index.
    """
    blog_posts = load_posts()
    original_length = len(blog_posts)

    # Filter out the post to be deleted
    updated_posts = [post for post in blog_posts if post.get('id') != post_id]

    if len(updated_posts) < original_length:
        print(f"INFO: Deleted post ID {post_id}.")
        save_posts(updated_posts)  # Save the filtered list
    else:
        print(f"WARNING: Attempted to delete non-existent post ID {post_id}.")

    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)