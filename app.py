import os
from flask import (
    Flask, 
    render_template, 
    request, 
    redirect, 
    url_for, 
    flash
)
from werkzeug.security import check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_babel import Babel, _
from flask_login import (
    LoginManager, 
    login_user, 
    logout_user, 
    login_required
)
from model import db, User  # Import db and User after defining the app

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')

# Initialize SQLAlchemy with the app
db.init_app(app)

migrate = Migrate(app, db)
babel = Babel(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'  # Redirect to login page if not logged in

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))  # Load user by ID

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Query the database for the user
        user = User.query.filter_by(email=email).first()
        
        # Check if the user exists and the password matches
        if user and user.check_password(password):
            login_user(user)  # Log in the user using Flask-Login
            flash(_("You have logged in successfully"), "success")
            return redirect(url_for('welcome'))  # Redirect to the welcome page after login
        else:
            flash(_("Login failed. Please check email and password"), "error")
            return render_template('login.html')

    return render_template('login.html')

@app.route('/logout')
@login_required  # Ensure the user is logged in before accessing this route
def logout():
    logout_user()  # Log out the user using Flask-Login
    flash(_("You have been logged out successfully."), "success")
    return redirect(url_for('home'))

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/welcome')
@login_required
def welcome():
    return render_template('welcome.html')

if __name__ == '__main__':
    app.run(debug=True)
