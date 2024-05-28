from flask import render_template, redirect, url_for, request, Flask
from flask_login import current_user, login_required, login_user, logout_user

from models import User


def register_routes(app: Flask, db, bcrypt):
    @app.route('/', methods=['GET', 'POST'])
    def home():
        if current_user.is_authenticated:
            return render_template('home.html', current_user=current_user)
        return render_template('home.html')

    @app.route('/signup', methods=['GET', 'POST'])
    def signup():
        if request.method == 'GET':
            return render_template('signup.html')
        elif request.method == 'POST':
            username = request.form['username']
            password = request.form['password']

            hashed_password = bcrypt.generate_password_hash(password)

            user = User(username=username, password=hashed_password)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('login'))

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'GET':
            if current_user.is_authenticated:
                return redirect(url_for('home'))
            return render_template('login.html')
        elif request.method == 'POST':
            username = request.form['username']
            password = request.form['password']

            user = User.query.filter(User.username == username).first()

            if user.password and bcrypt.check_password_hash(user.password, password):
                login_user(user)
                return redirect(url_for('home'))
            else:
                return redirect(url_for('login'))

    @app.route('/logout', methods=['GET', 'POST'])
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('login'))

    @app.route('/<username>', methods=['GET'])
    @login_required
    def user(username):
        _ = User.query.filter(User.username == username).first()
        return render_template('user.html', user=_)
