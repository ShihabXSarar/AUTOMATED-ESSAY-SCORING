from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
import pickle
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
from bson.objectid import ObjectId

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Change this to a random secret key

# MongoDB Configuration
client = MongoClient('mongodb://localhost:27017/')
db = client['essay_scoring_db']
users_collection = db['users']

# Flask-Login Configuration
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin):
    def __init__(self, user_data):
        self.id = str(user_data['_id'])
        self.username = user_data['username']
        self.email = user_data['email']

    @staticmethod
    def get(user_id):
        user_data = users_collection.find_one({'_id': ObjectId(user_id)})
        if user_data:
            return User(user_data)
        return None

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

# Load model and vectorizer
print("Loading model and vectorizer...")
try:
    with open('model.pkl', 'rb') as f:
        model = pickle.load(f)
    with open('vectorizer.pkl', 'rb') as f:
        vectorizer = pickle.load(f)
    print("Model loaded successfully.")
except FileNotFoundError:
    print("Error: Model files not found. Please run train_model.py first.")
    model = None
    vectorizer = None

# Ensure NLTK data is available
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('punkt_tab')

def clean_text(text):
    # Remove non-alphabetic characters
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    # Convert to lowercase
    text = text.lower()
    # Tokenize
    tokens = word_tokenize(text)
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word not in stop_words]
    return ' '.join(tokens)

@app.route('/')
@login_required
def home():
    return render_template('index.html', user=current_user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user_data = users_collection.find_one({'email': email})
        
        if user_data and check_password_hash(user_data['password'], password):
            user = User(user_data)
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('Invalid email or password')
            
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        if users_collection.find_one({'email': email}):
            flash('Email already registered')
            return redirect(url_for('register'))
            
        hashed_password = generate_password_hash(password)
        users_collection.insert_one({
            'username': username,
            'email': email,
            'password': hashed_password
        })
        
        flash('Registration successful! Please login.')
        return redirect(url_for('login'))
        
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/predict', methods=['POST'])
@login_required
def predict():
    if not model or not vectorizer:
        return jsonify({'error': 'Model not loaded'}), 500

    data = request.get_json()
    essay = data.get('essay')

    if not essay:
        return jsonify({'error': 'No essay provided'}), 400

    # Preprocess
    cleaned_essay = clean_text(essay)
    
    # Vectorize
    features = vectorizer.transform([cleaned_essay]).toarray()
    
    # Predict
    score = model.predict(features)[0]
    
    # Round to 2 decimal places
    score = round(score, 2)

    return jsonify({'score': score})

if __name__ == '__main__':
    app.run(debug=True)
