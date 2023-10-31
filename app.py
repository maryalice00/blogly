"""Blogly application."""

from flask import Flask, render_template, redirect, request, url_for
from models import db, connect_db, User

app = Flask(__name)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

# Connect to the database
connect_db(app)

# Define routes for users

@app.route('/')
def home():
    # Redirect to the list of users. You can change this to the actual URL for user listing.
    return redirect(url_for('list_users'))

@app.route('/users')
def list_users():
    # Show all users.
    users = User.query.all()
    return render_template('user_list.html', users=users)

@app.route('/users/new', methods=['GET', 'POST'])
def add_user():
    # Show the add form for users and process the form when submitted.
    if request.method == 'POST':
        # Handle form submission and add a new user to the database.
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        image_url = request.form['image_url']
        new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('list_users'))
    return render_template('new_user_form.html')

@app.route('/users/<int:user_id>')
def user_detail(user_id):
    # Show information about the given user.
    user = User.query.get_or_404(user_id)
    return render_template('user_detail.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
def edit_user(user_id):
    # Show the edit page for a user and process the edit form when submitted.
    user = User.query.get_or_404(user_id)
    if request.method == 'POST':
        # Handle form submission and update the user in the database.
        user.first_name = request.form['first_name']
        user.last_name = request.form['last_name']
        user.image_url = request.form['image_url']
        db.session.commit()
        return redirect(url_for('user_detail', user_id=user_id))
    return render_template('edit_user.html', user=user)

@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    # Delete the user.
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('list_users'))

if __name__ == '__main__':
    app.run(debug=True)
