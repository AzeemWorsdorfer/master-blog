MasterBlog: Simple Flask Blog Manager

MasterBlog is a lightweight, full-stack application built with Flask that demonstrates basic CRUD (Create, Read, Update, Delete) operations. It uses a local JSON file (blog_posts.json) for data persistence instead of a database, making it ideal for prototyping and simple use cases.

✨ Features

Create: Add new blog posts via a dedicated form (/add).

Read: View all existing blog posts on the homepage (/).

Update: Edit existing posts via the "Edit" link on each post card (/update/<id>).

Delete: Remove posts using a dedicated delete button.

Persistence: Data is stored locally in blog_posts.json.

🚀 Setup and Running

Prerequisites

You need Python 3 installed on your system.

Installation

Install Flask:

pip install Flask


Run the Application:
Navigate to the project directory and run the main application file:

python app.py


Access

After running the command, the application will be available at:
http://127.0.0.1:5000/ (or the local address shown in your console).

📂 File Structure

The project utilizes a standard Flask directory structure:

app.py: Contains all the Python application logic, routes, and JSON handling functions.

blog_posts.json: The data store for all blog content.

static/: Contains the style sheet.

styles.css: Basic styling for the application layout and components.

templates/: Contains the HTML template files.

base.html: The main layout used by all pages.

index.html: The home page, listing all posts.

add.html: The form for creating a new post.

update.html: The form for editing an existing post.

🛠️ Data Handling

The data is handled by two core functions in app.py:

load_posts(): Reads data from blog_posts.json.

save_posts(posts): Writes the current list of posts back to blog_posts.json.

All modifications (add, update, delete) trigger a save operation to ensure data changes are persistent.