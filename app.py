from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from model.predict_asd import analyze_responses
from models import db, User, Prediction
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkey123'

# Set up database path
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'instance', 'user.db')
os.makedirs(os.path.dirname(db_path), exist_ok=True)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# ========== Routes ==========

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        if not (name and email and password):
            flash("Please fill out all fields.", 'error')
            return redirect(url_for('signup'))

        if User.query.filter_by(email=email).first():
            flash('Email already exists!', 'error')
            return redirect(url_for('signup'))

        hashed_password = generate_password_hash(password)
        user = User(name=name, email=email, password=hashed_password)
        db.session.add(user)
        db.session.commit()

        flash('Signup successful! Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password.', 'error')
            return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))


@app.route('/dashboard')
@login_required
def dashboard():
    last = Prediction.query.filter_by(user_id=current_user.id).order_by(Prediction.timestamp.desc()).first()

    return render_template(
        'dashboard.html',
        name=current_user.name,
        score=last.score if last else None,
        verdict=last.verdict if last else None,
        advice=last.advice if last else None,
        category_scores=last.category_scores if last and last.category_scores else None,
        timestamp=last.timestamp.strftime('%d %B %Y, %I:%M %p') if last else None
    )


@app.route('/predict', methods=['GET', 'POST'])
@login_required
def predict():
    questions = [
        "I prefer to do things on my own rather than with others.",
        "I find it hard to understand how other people feel.",
        "I like routines and get upset if they change.",
        "I find social situations confusing.",
        "I notice small details that others don’t.",
        "I find it difficult to imagine what other people are thinking.",
        "I tend to focus on one interest and pursue it obsessively.",
        "I often miss social cues like facial expressions or tone of voice.",
        "I find loud noises or bright lights overwhelming.",
        "I take things literally and find it hard to understand jokes.",
        "I prefer not to look people in the eye.",
        "I enjoy spinning objects or watching them spin.",
        "I struggle to start conversations.",
        "I flap my hands or rock my body when excited or stressed.",
        "I get very anxious in new environments.",
        "I repeat phrases or questions out of context.",
        "I have trouble adapting to changes in schedule.",
        "I line up toys or objects in a particular order.",
        "I don’t enjoy social games as much as others.",
        "I find it hard to make friends."
    ]

    if request.method == 'POST':
        try:
            responses = [int(request.form.get(f'q{i+1}')) for i in range(20)]
            result = analyze_responses(responses)

            prediction = Prediction(
                score=result['score'],
                verdict=result['verdict'],
                advice=result['advice'],
                category_scores=result['category_scores'],
                user_id=current_user.id
            )

            db.session.add(prediction)
            db.session.commit()

            return render_template(
                'result.html',
                questions=questions,
                responses=responses,
                verdict=result['verdict'],
                score=result['score'],
                advice=result['advice'],
                category_scores=result['category_scores'],
                current_user=current_user
            )

        except Exception as e:
            flash(f"Error processing responses: {str(e)}", 'error')
            return redirect(url_for('predict'))

    return render_template('predict.html', questions=questions)


# Quiz Route
@app.route('/quiz/<quiz_name>')
@login_required
def load_quiz(quiz_name):
    try:
        return render_template(f'quizzes/{quiz_name}.html')
    except:
        return "Quiz not found", 404


# Game Route
@app.route('/game/<game_name>')
@login_required
def load_game(game_name):
    try:
        return render_template(f'games/{game_name}.html')
    except:
        return "Game not found", 404


# ========== Run App ==========
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
