"""Blogly application."""

from flask import Flask, render_template, request, redirect, flash
from models import db, connect_db,User,Post
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "SECRET!"
debug = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

app.app_context().push()
connect_db(app)
db.create_all()

@app.route('/')
def home_page():
    """Displays 5 most recent posts"""
    posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()
    return render_template('homepage.html', posts=posts)

@app.route('/users')
def users_page():
    """Displays all users"""
    users = User.query.order_by(User.last_name,User.first_name).all()
    return render_template('index.html', users=users)

@app.route('/users/new', methods=['GET'])
def new_user():
    """Displays page for adding new user"""
    return render_template('new_user.html')

@app.route('/users/new', methods=["POST"])
def new_post_user():
    """Adds new user"""
    new_user = User(
        first_name = request.form['first_name'],
        last_name = request.form['last_name'],
        image_url = request.form['image_url'] or None)

    db.session.add(new_user)
    db.session.commit()
    flash(f"User {new_user.full_name} added!")
    return redirect(f"/users")

@app.route('/users/<int:user_id>')
def show_user(user_id):
    """Shows specific info about single user"""
    user = User.query.get_or_404(user_id)
    return render_template('user_detail.html', user=user)

@app.route('/users/<int:user_id>/edit')
def edit_user(user_id):
    """Displays page for editing user"""
    user = User.query.get_or_404(user_id)
    return render_template('user_edit.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=['POST'])
def edit_post_user(user_id):
    """Posts edit of the user"""
    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()
    flash(f"User {user.full_name} has been edited!")
    return redirect('/users')

@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    """Deletes the user in question"""
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect('/users')

@app.errorhandler(404)
def page_missing(evt):
    """Displays 404 not found page"""
    return render_template('404.html'), 404

@app.route('/users/<int:user_id>/posts/new')
def new_post(user_id):
    """Displays page for new post"""
    user = User.query.get_or_404(user_id)
    return render_template('new_post.html', user=user)

@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def new_post_post(user_id):
    """Handle add form, add post and redirect to details page"""
    user = User.query.get_or_404(user_id)
    new_post = Post(title = request.form['title'], content = request.form['content'],user=user)

    db.session.add(new_post)
    db.session.commit()
    flash(f"Post '{new_post.title}' has been posted!")
    return redirect(f"/users/{user_id}")

@app.route('/posts/<int:post_id>')
def show_posts(post_id):
    """Displays page with information about post"""
    post = Post.query.get_or_404(post_id)
    return render_template('show_posts.html', post=post)

@app.route('/posts/<int:post_id>/edit')
def posts_edit(post_id):
    """Displays form for editing posts"""
    post = Post.query.get_or_404(post_id)
    return render_template('post_edit.html', post = post)

@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def update_post(post_id):
    """Handles form submisssion for updating post"""
    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']

    db.session.add(post)
    db.session.commit()
    flash(f"Post '{post.title}' has been edited!")

    return redirect (f"/users/{post.user_id}")

@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def posts_destroy(post_id):
    """Handle form submission for deleting an existing post"""

    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash(f"Post '{post.title} deleted.")

    return redirect(f"/users/{post.user_id}")