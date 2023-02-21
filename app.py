"""Blogly application."""

from flask import Flask, render_template, request, redirect
from models import db, connect_db,User
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
    """Displays users"""
    return redirect('/users')

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
    return redirect('/users')

@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    """Deletes the user in question"""
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect('/users')
