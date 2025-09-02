from flask import Blueprint, render_template, request, jsonify, session
from app.controllers.recommendation_controller import RecommendationController
from app.models.user import User

api_bp = Blueprint('api', __name__)
controller = RecommendationController()

# Stockage en mémoire des utilisateurs
users_db = {}

@api_bp.route('/')
def index():
    """Render main page"""
    return render_template('index.html')

@api_bp.route('/api/products', methods=['GET'])
def get_products():
    """Get all products"""
    return controller.get_products()

@api_bp.route('/api/track-click', methods=['POST'])
def track_click():
    """Track product click"""
    return controller.track_click()

@api_bp.route('/api/recommendations', methods=['GET'])
def get_recommendations():
    """Get recommendations"""
    return controller.get_recommendations()

@api_bp.route('/signup', methods=['POST'])
def signup():
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    if not username or not email or not password:
        return jsonify({'error': 'Missing fields'}), 400
    if email in users_db:
        return jsonify({'error': 'Email already registered'}), 400
    user = User(username, email, password)
    users_db[email] = user
    return jsonify({'message': 'User created successfully'})

@api_bp.route('/signin', methods=['POST'])
def signin():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    user = users_db.get(email)
    if user and user.check_password(password):
        session['user_email'] = email
        return jsonify({'message': 'Signed in successfully'})
    return jsonify({'error': 'Invalid credentials'}), 401

@api_bp.route('/auth')
def auth():
    """Render authentication page"""
    return render_template('auth.html')