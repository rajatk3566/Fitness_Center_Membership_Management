from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models import User
from flask_login import login_user, logout_user, login_required

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("Email already exists.", "danger")
            return render_template('register.html')

        new_user = User(name=name, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        flash("Registration successful!", "success")
        return redirect(url_for('auth.login'))

    return render_template('register.html')

@auth.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            flash("Login successful!", "success")
            return redirect(url_for('members.add_member'))
        else:
            flash("Invalid credentials.", "danger")
            return render_template('login.html')

    return render_template('login.html')


@auth.route('/logout')
@login_required  
def logout():
    """Logout the user and redirect to login."""
    logout_user()  
    flash("You have been logged out.", "info")  
    return redirect('/')  